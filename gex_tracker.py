#!/usr/bin/env python3
"""
SPX GEX touch log: standalone and data-only.

  snapshot  (morning)     Pull the delayed SPX option chain from Cboe, compute GEX levels,
                          add a few random "control" levels as a baseline, save them.
  review    (after close) Pull the day's 1-minute SPX bars, log every touch of those levels
                          and what price did next.
  summary                 Rebuild SUMMARY.md from everything logged so far.
  auto                    Pick the right task for the current Eastern time (used by the scheduler).

No broker connection, no orders, no API keys.
"""
from __future__ import annotations

import argparse
import math
import os
import random
import re
import sys
import time
from datetime import date, datetime, time as dtime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import requests

ET = ZoneInfo("America/New_York")
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CHAIN_DIR = DATA / "chain"
LEVELS_CSV = DATA / "levels.csv"
TOUCHES_CSV = DATA / "touches.csv"
SESSIONS_CSV = DATA / "sessions.csv"
SUMMARY_MD = ROOT / "SUMMARY.md"

CHAIN_URL = "https://cdn.cboe.com/api/global/delayed_quotes/options/_SPX.json"
BARS_SYMBOL = "^GSPC"  # S&P 500 cash index (same underlying as the SPX chain)

CFG = {
    "max_dte": 60,            # expirations included in the GEX calc
    "strike_band": 0.08,      # strikes within +/-8% of spot
    "rate": 0.04,             # risk-free rate for Black-Scholes gamma
    "flip_sweep": 0.06,       # search +/-6% of spot for the zero-gamma flip
    "major_band": 0.03,       # 'major' strikes must sit within +/-3% of spot
    "n_major": 3,
    "n_control": 8,           # random baseline levels per day (was 4; more = faster fair comparison)
    "level_gap": 10.0,        # min pts between majors/controls and any other level
    "touch_tol": 1.0,         # pts: within this of a level = touch
    "rearm_dist": 5.0,        # pts: price must get this far away before the next touch counts
    "reject_pts": 5.0,        # pts back toward the approach side = reject
    "break_pts": 3.0,         # pts beyond the level on a 1-min close...
    "break_bars": 5,          # ...for this many consecutive closes = break
    "resolve_min": 30,        # minutes to resolve reject/break, otherwise 'chop'
    "windows": [15, 30, 60],  # excursion windows logged for every touch
}

LEVEL_COLS = ["date", "data_time", "spot", "regime", "net_gex_bn", "level_type", "price", "gex_bn"]
SESSION_COLS = ["date", "status", "data_time", "spot", "regime", "net_gex_bn",
                "open", "high", "low", "close", "range", "n_touches"]
TOUCH_COLS = (["date", "level_type", "level_price", "regime", "touch_time", "minute_of_session",
               "approach", "close_at_touch", "result", "minutes_to_result"]
              + [f"{k}_{w}m" for w in CFG["windows"] for k in ("bounce", "through")]
              + ["window_truncated"])

OCC = re.compile(r"^([A-Z]+)(\d{6})([CP])(\d{8})$")


# ----------------------------------------------------------------------------- io helpers

def read_csv(path: Path) -> pd.DataFrame:
    if path.exists() and path.stat().st_size > 0:
        return pd.read_csv(path, dtype={"date": str})
    return pd.DataFrame()


def append_csv(path: Path, rows: list[dict], cols: list[str]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows).reindex(columns=cols)
    df.to_csv(path, mode="a", header=not path.exists(), index=False)


# ----------------------------------------------------------------------------- chain + GEX

def fetch_chain() -> dict:
    test_file = os.environ.get("GEX_CHAIN_FILE")  # offline testing hook
    if test_file:
        import json
        return json.loads(Path(test_file).read_text())
    last = None
    for attempt in range(4):
        try:
            r = requests.get(CHAIN_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=90)
            r.raise_for_status()
            return r.json()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"Chain fetch failed: {last}")


def parse_chain(raw: dict, now: datetime) -> tuple[float, datetime, pd.DataFrame]:
    data = raw.get("data", raw)
    spot = float(data["current_price"])
    ts = raw.get("timestamp") or data.get("last_trade_time")
    stamp = pd.to_datetime(ts, errors="coerce") if ts else pd.NaT
    if pd.isna(stamp):
        data_time = now - timedelta(minutes=15)
    else:
        data_time = stamp.to_pydatetime()
        if data_time.tzinfo is None:
            data_time = data_time.replace(tzinfo=ET)
            if data_time > now + timedelta(minutes=30):  # stamp was really UTC
                data_time = data_time.replace(tzinfo=ZoneInfo("UTC")).astimezone(ET)
        else:
            data_time = data_time.astimezone(ET)
        data_time = min(data_time, now)

    rows = []
    for o in data.get("options", []):
        m = OCC.match(str(o.get("option", "")).replace(" ", ""))
        if not m:
            continue
        root, ymd, cp, k = m.groups()
        rows.append({
            "root": root,
            "expiry": datetime.strptime(ymd, "%y%m%d").date(),
            "type": cp,
            "strike": int(k) / 1000.0,
            "oi": float(o.get("open_interest") or 0),
            "iv": float(o.get("iv") or 0),
            "gamma_cboe": float(o.get("gamma") or 0),
            "volume": float(o.get("volume") or 0),
        })
    return spot, data_time, pd.DataFrame(rows)


def prepare(df: pd.DataFrame, spot: float, at: datetime) -> pd.DataFrame:
    df = df.copy()
    if df["iv"].median() > 3:  # guard in case IV arrives in percent
        df["iv"] = df["iv"] / 100.0
    # SPX monthlies are AM-settled (gone at the open on expiry day); SPXW settles at 16:00.
    exp_dt = [datetime.combine(d, dtime(9, 30) if r == "SPX" else dtime(16, 0), tzinfo=ET)
              for r, d in zip(df["root"], df["expiry"])]
    secs = np.array([(e - at).total_seconds() for e in exp_dt])
    dte = np.array([(d - at.date()).days for d in df["expiry"]])
    df["T"] = np.maximum(secs, 15 * 60) / (365 * 24 * 3600)  # floor at 15 minutes
    keep = ((df["oi"] > 0) & (df["iv"] > 0) & (secs > 0) & (dte <= CFG["max_dte"])
            & (df["strike"].between(spot * (1 - CFG["strike_band"]), spot * (1 + CFG["strike_band"]))))
    df = df[keep].reset_index(drop=True)
    df["sign"] = np.where(df["type"] == "C", 1.0, -1.0)  # dealers long calls / short puts convention
    return df


def bs_gamma(S, K, T, iv, r):
    sq = np.sqrt(T)
    d1 = (np.log(S / K) + (r + 0.5 * iv ** 2) * T) / (iv * sq)
    return np.exp(-0.5 * d1 ** 2) / (math.sqrt(2 * math.pi) * S * iv * sq)


def gex(S, df: pd.DataFrame):
    """$ gamma per 1% move. S may be a scalar or an (n, 1) column of spots."""
    g = bs_gamma(S, df["strike"].values, df["T"].values, df["iv"].values, CFG["rate"])
    return df["sign"].values * g * df["oi"].values * 100 * S ** 2 * 0.01


def by_strike(df: pd.DataFrame) -> pd.DataFrame:
    t = df.pivot_table(index="strike", columns="type", values="gex", aggfunc="sum", fill_value=0.0)
    for c in ("C", "P"):
        if c not in t:
            t[c] = 0.0
    t["net"] = t["C"] + t["P"]
    return t


def compute_levels(df: pd.DataFrame, spot: float, at: datetime) -> tuple[list[dict], float, str]:
    df = df.copy()
    df["gex"] = gex(spot, df)
    bs = by_strike(df)
    levels: list[dict] = []

    def add(kind, price, val):
        levels.append({"level_type": kind, "price": round(float(price), 2),
                       "gex_bn": None if val is None else round(float(val) / 1e9, 3)})

    # Walls sit on their own side of spot: call wall at/above, put wall at/below (FIX 2026-11-02:
    # without this, a large ITM put stack above spot was being picked as the "put wall").
    up, dn = bs[bs.index >= spot], bs[bs.index <= spot]
    cw = up if len(up) else bs
    pw = dn if len(dn) else bs
    add("call_wall", cw["C"].idxmax(), cw["C"].max())
    add("put_wall", pw["P"].idxmin(), pw["P"].min())

    zero = df[df["expiry"] == at.date()]
    if len(zero):
        bz = by_strike(zero)
        add("0dte_call_wall", bz["C"].idxmax(), bz["C"].max())
        add("0dte_put_wall", bz["P"].idxmin(), bz["P"].min())

    grid = spot * np.linspace(1 - CFG["flip_sweep"], 1 + CFG["flip_sweep"], 241)
    net = gex(grid[:, None], df).sum(axis=1)
    idx = np.where(np.diff(np.sign(net)) != 0)[0]
    if len(idx):
        xs = [grid[i] - net[i] * (grid[i + 1] - grid[i]) / (net[i + 1] - net[i]) for i in idx]
        add("gamma_flip", min(xs, key=lambda x: abs(x - spot)), None)

    band, gap = CFG["major_band"], CFG["level_gap"]
    near = bs[(bs.index >= spot * (1 - band)) & (bs.index <= spot * (1 + band))]
    near = near.loc[near["net"].abs().sort_values(ascending=False).index]
    n = 0
    for k, row in near.iterrows():
        if any(abs(float(k) - l["price"]) < gap for l in levels):
            continue
        n += 1
        add(f"major_{n}", k, row["net"])
        if n >= CFG["n_major"]:
            break

    # Controls: random strikes (multiples of 5, like real strikes) placed at distances from spot
    # similar to the real levels, so the comparison is fair. Seeded by date so reruns match.
    # FIX 2026-11-02: sample distances only from levels within the major band (+/-3%), so far-away
    # walls don't push every control out of the day's range (Oct 29-30 controls got 0 touches).
    rng = random.Random(at.date().isoformat())
    dists = [abs(l["price"] - spot) for l in levels
             if abs(l["price"] - spot) <= spot * CFG["major_band"]] or [spot * 0.01]
    taken = [l["price"] for l in levels]
    c = tries = 0
    while c < CFG["n_control"] and tries < 5000:
        tries += 1
        d = max(rng.choice(dists) * rng.uniform(0.7, 1.3), gap)
        p = round((spot + rng.choice((-1, 1)) * d) / 5) * 5
        if any(abs(p - u) < gap for u in taken):
            continue
        c += 1
        taken.append(p)
        add(f"control_{c}", p, None)

    total = float(bs["net"].sum())
    return levels, total, ("positive" if total > 0 else "negative")


# ----------------------------------------------------------------------------- bars + touches

def fetch_bars() -> pd.DataFrame:
    test_file = os.environ.get("GEX_BARS_FILE")  # offline testing hook
    if test_file:
        b = pd.read_csv(test_file, index_col=0)
        b.index = pd.to_datetime(b.index, utc=True).tz_convert(ET)
        return b
    import yfinance as yf
    last = None
    for attempt in range(4):
        try:
            b = yf.Ticker(BARS_SYMBOL).history(period="7d", interval="1m", prepost=False, auto_adjust=False)
            if len(b):
                b.index = b.index.tz_convert(ET)
                return b[["Open", "High", "Low", "Close"]]
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(15 * (attempt + 1))
    raise RuntimeError(f"Bar fetch failed or empty: {last}")


def classify(i, side, lvl, hi, lo, cl):
    n = len(cl)
    streak = 0
    for j in range(i, min(n, i + CFG["resolve_min"] + 1)):
        beyond = (lvl - cl[j]) if side > 0 else (cl[j] - lvl)
        streak = streak + 1 if beyond >= CFG["break_pts"] else 0
        if streak >= CFG["break_bars"]:
            return "break", j - i
        if j > i:
            away = (hi[j] - lvl) if side > 0 else (lvl - lo[j])
            if away >= CFG["reject_pts"]:
                return "reject", j - i
    return "chop", None


def find_touches(bars: pd.DataFrame, levels: pd.DataFrame, start: datetime, open_time: datetime) -> list[dict]:
    b = bars[bars.index >= start]
    if b.empty:
        return []
    hi, lo, cl = b["High"].values, b["Low"].values, b["Close"].values
    times = b.index
    n = len(b)
    out = []
    for _, L in levels.iterrows():
        lvl = float(L["price"])
        armed, side = False, 0
        for i in range(n):
            if not armed:
                if lo[i] > lvl + CFG["rearm_dist"]:
                    armed, side = True, 1
                elif hi[i] < lvl - CFG["rearm_dist"]:
                    armed, side = True, -1
                continue
            touched = lo[i] <= lvl + CFG["touch_tol"] if side > 0 else hi[i] >= lvl - CFG["touch_tol"]
            if not touched:
                continue
            rec = {
                "date": L["date"], "level_type": L["level_type"], "level_price": lvl, "regime": L["regime"],
                "touch_time": times[i].strftime("%H:%M"),
                "minute_of_session": int((times[i] - open_time).total_seconds() // 60),
                "approach": "from_above" if side > 0 else "from_below",
                "close_at_touch": round(float(cl[i]), 2),
            }
            rec["result"], rec["minutes_to_result"] = classify(i, side, lvl, hi, lo, cl)
            for w in CFG["windows"]:
                end = min(n, i + w + 1)
                if side > 0:
                    bounce = hi[i + 1:end].max() - lvl if end > i + 1 else 0.0
                    through = lvl - lo[i:end].min()
                else:
                    bounce = lvl - lo[i + 1:end].min() if end > i + 1 else 0.0
                    through = hi[i:end].max() - lvl
                rec[f"bounce_{w}m"] = round(max(float(bounce), 0.0), 2)
                rec[f"through_{w}m"] = round(max(float(through), 0.0), 2)
            rec["window_truncated"] = i + max(CFG["windows"]) >= n
            out.append(rec)
            armed = False
    return out


# ----------------------------------------------------------------------------- tasks

def cmd_snapshot(now: datetime) -> None:
    today = now.date().isoformat()
    lv = read_csv(LEVELS_CSV)
    if len(lv) and today in set(lv["date"]):
        print(f"Snapshot for {today} already saved.")
        return
    spot, data_time, chain = parse_chain(fetch_chain(), now)
    if data_time.date() != now.date():
        print(f"Chain data is from {data_time.date()}, not today: market closed. Skipping.")
        return
    df = prepare(chain, spot, data_time)
    if df.empty:
        raise RuntimeError("No usable contracts after filtering.")
    levels, total, regime = compute_levels(df, spot, data_time)
    rows = [{"date": today, "data_time": data_time.strftime("%H:%M"), "spot": round(spot, 2),
             "regime": regime, "net_gex_bn": round(total / 1e9, 3), **l} for l in levels]
    append_csv(LEVELS_CSV, rows, LEVEL_COLS)

    # Compact copy of the chain so levels can be recomputed with other methods later.
    CHAIN_DIR.mkdir(parents=True, exist_ok=True)
    keep = chain[(chain["oi"] > 0) & chain["strike"].between(spot * 0.92, spot * 1.08)]
    keep.to_csv(CHAIN_DIR / f"{today}.csv.gz", index=False, compression="gzip")

    print(f"{today} {data_time:%H:%M} ET  spot {spot:.2f}  regime {regime}  net {total/1e9:+.2f}bn per 1%")
    for l in levels:
        print(f"  {l['level_type']:<15} {l['price']:>9.2f}")


def cmd_review(now: datetime) -> None:
    lv = read_csv(LEVELS_CSV)
    if lv.empty:
        print("No snapshots yet.")
        return
    se = read_csv(SESSIONS_CSV)
    done = set(se["date"]) if len(se) else set()
    pending = []
    for d in sorted(lv["date"].unique()):
        dd = date.fromisoformat(d)
        if d in done or (now.date() - dd).days > 6:
            continue
        if dd == now.date() and now.time() < dtime(16, 10):
            continue
        pending.append(d)
    if not pending:
        print("Nothing to review.")
        return

    bars_all = fetch_bars()
    for d in pending:
        dd = date.fromisoformat(d)
        open_time = datetime.combine(dd, dtime(9, 30), tzinfo=ET)
        day = bars_all[(bars_all.index >= open_time)
                       & (bars_all.index < datetime.combine(dd, dtime(16, 0), tzinfo=ET))]
        lv_d = lv[lv["date"] == d]
        first = lv_d.iloc[0]
        base = {"date": d, "data_time": first["data_time"], "spot": first["spot"],
                "regime": first["regime"], "net_gex_bn": first["net_gex_bn"]}
        if day.empty:
            append_csv(SESSIONS_CSV, [{**base, "status": "no_bars", "n_touches": 0}], SESSION_COLS)
            print(f"{d}: no bars found, marked no_bars.")
            continue
        hh, mm = map(int, str(first["data_time"]).split(":"))
        start = max(open_time, datetime.combine(dd, dtime(hh, mm), tzinfo=ET))
        touches = find_touches(day, lv_d, start, open_time)
        append_csv(TOUCHES_CSV, touches, TOUCH_COLS)
        append_csv(SESSIONS_CSV, [{
            **base, "status": "ok",
            "open": round(float(day["Open"].iloc[0]), 2), "high": round(float(day["High"].max()), 2),
            "low": round(float(day["Low"].min()), 2), "close": round(float(day["Close"].iloc[-1]), 2),
            "range": round(float(day["High"].max() - day["Low"].min()), 2), "n_touches": len(touches),
        }], SESSION_COLS)
        print(f"{d}: {len(touches)} touches logged.")


GROUP_ORDER = ["call_wall", "put_wall", "gamma_flip", "0dte_call_wall", "0dte_put_wall", "major", "control"]


def _table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def _stats(g: pd.DataFrame) -> dict:
    n = len(g)
    pct = lambda k: f"{100 * (g['result'] == k).mean():.0f}%" if n else "-"  # noqa: E731
    return {"touches": n, "reject": pct("reject"), "break": pct("break"), "chop": pct("chop"),
            "med bounce 30m": f"{g['bounce_30m'].median():.1f}" if n else "-",
            "med through 30m": f"{g['through_30m'].median():.1f}" if n else "-"}


def cmd_summary() -> None:
    t, s = read_csv(TOUCHES_CSV), read_csv(SESSIONS_CSV)
    ok = s[s["status"] == "ok"] if len(s) else s
    out = ["# SPX GEX touch log: summary", ""]
    if t.empty:
        out += ["No touches logged yet."]
        SUMMARY_MD.write_text("\n".join(out) + "\n")
        print("Summary written (empty).")
        return
    t["group"] = t["level_type"].str.replace(r"_\d+$", "", regex=True)
    t["is_control"] = t["group"] == "control"
    out += [f"Sessions logged: **{len(ok)}** ({ok['date'].min()} to {ok['date'].max()}). "
            f"Touches: **{len(t)}**. Updated {datetime.now(ET):%Y-%m-%d %H:%M} ET.", "",
            "GEX levels only earn a place if they clearly beat the **control** rows (random strikes) "
            "on reject rate and bounce vs. through, over a real sample. Treat any row with fewer than "
            "~30 touches as noise.", "", "## GEX levels vs. control", ""]

    rows = [{"levels": "all GEX levels", **_stats(t[~t["is_control"]])},
            {"levels": "control (random)", **_stats(t[t["is_control"]])}]
    out += [_table(pd.DataFrame(rows)), "", "## By level type", ""]
    rows = [{"level": g, **_stats(t[t["group"] == g])} for g in GROUP_ORDER if (t["group"] == g).any()]
    out += [_table(pd.DataFrame(rows)), "", "## By gamma regime", ""]
    rows = []
    for reg in ("positive", "negative"):
        for lab, mask in (("GEX", ~t["is_control"]), ("control", t["is_control"])):
            g = t[(t["regime"] == reg) & mask]
            if len(g):
                rows.append({"regime": reg, "levels": lab, **_stats(g)})
    out += [_table(pd.DataFrame(rows)) if rows else "-", "", "## By approach", ""]
    rows = [{"approach": a, "levels": lab, **_stats(t[(t["approach"] == a) & mask])}
            for a in ("from_above", "from_below")
            for lab, mask in (("GEX", ~t["is_control"]), ("control", t["is_control"]))
            if len(t[(t["approach"] == a) & mask])]
    out += [_table(pd.DataFrame(rows)), "",
            "Definitions: a touch = price within "
            f"{CFG['touch_tol']} pt of a level after being at least {CFG['rearm_dist']} pts away. "
            f"Reject = {CFG['reject_pts']} pts back toward the approach side within {CFG['resolve_min']} min. "
            f"Break = {CFG['break_bars']} straight 1-min closes {CFG['break_pts']}+ pts beyond. "
            "Otherwise chop. Bounce/through = max move away vs. max move past the level (pts)."]
    SUMMARY_MD.write_text("\n".join(out) + "\n")
    print("Summary written.")


def cmd_auto(now: datetime) -> None:
    if now.weekday() >= 5:
        print("Weekend.")
        return
    t = now.time()
    if dtime(9, 35) <= t < dtime(11, 30):
        cmd_snapshot(now)
    elif t >= dtime(16, 10):
        cmd_review(now)
        cmd_summary()
    else:
        print(f"{t:%H:%M} ET is outside the run windows. Nothing to do.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("task", nargs="?", default="auto", choices=["auto", "snapshot", "review", "summary"])
    task = ap.parse_args().task
    now = datetime.now(ET)
    if os.environ.get("GEX_NOW"):  # testing hook, e.g. 2026-10-28T16:30
        now = datetime.fromisoformat(os.environ["GEX_NOW"]).replace(tzinfo=ET)
    {"auto": lambda: cmd_auto(now), "snapshot": lambda: cmd_snapshot(now),
     "review": lambda: (cmd_review(now), cmd_summary()), "summary": cmd_summary}[task]()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
