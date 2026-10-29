# SPX GEX touch log

A standalone, data-only tracker. It logs whether price reacts at SPX gamma-exposure (GEX)
levels, and checks that against random levels as a baseline, so you can see whether
the levels are worth building on. It has no broker connection, places no orders, and
needs no API keys or links to any other project.

## What it does each trading day

**9:45 AM ET: snapshot.** It pulls the free, roughly 15-minute-delayed SPX option chain
from Cboe. From the open interest and implied volatility it computes these levels:

- call wall
- put wall
- 0DTE call wall and 0DTE put wall
- zero-gamma flip
- the 3 largest net-GEX strikes near spot

It also adds 4 random "control" strikes at similar distances from spot. The day's gamma
regime (positive or negative) is recorded too.

**4:40 PM ET: review.** It pulls the day's 1-minute SPX index bars and logs every touch of
every level. For each touch it records the approach direction and the result: reject,
break, or chop. It also records how far price bounced and how far it pushed through at
15, 30, and 60 minutes. Then it rebuilds `SUMMARY.md`.

Everything is committed back to this repo:

| File | Contents |
|---|---|
| `data/levels.csv` | One row per level per day |
| `data/touches.csv` | One row per touch, with outcome and excursions |
| `data/sessions.csv` | One row per day: regime, OHLC, range, touch count |
| `data/chain/DATE.csv.gz` | Compact copy of that morning's chain, so levels can be recomputed with other methods later |
| `SUMMARY.md` | The scoreboard: GEX levels vs. control, by level type, regime, and approach |

## Setup (about 5 minutes)

1. Create a new **private** GitHub repo, for example `spx-gex-touch-log`.
2. Upload `gex_tracker.py`, `requirements.txt`, and `README.md`.
3. Click **Add file → Create new file**, type `.github/workflows/gex-log.yml` as the name,
   paste in the workflow file's contents, and commit.
4. Go to **Actions** and enable workflows if GitHub asks.
5. Optional test: during market hours, open **Actions → gex-touch-log → Run workflow** with
   task `snapshot`. After 4:15 PM ET, run it again with task `review`.

After that it runs on its own every weekday. It skips market holidays automatically.

## Reading the results

Give it about 30 to 40 sessions before drawing conclusions. The question to answer is
whether GEX levels beat the control rows. A good reject rate means little if random
strikes reject just as often.

## Caveats

- **The levels are not TerraShade's.** They come from a standard open-interest GEX
  calculation, which assumes dealers are long calls and short puts. TerraShade's levels
  may differ.
- **The 15-minute delay doesn't matter here.** Touches are scored after the close, and
  scoring starts from the chain's own timestamp, so there's no look-ahead.
- **Settings can be tuned.** Thresholds (touch tolerance, reject and break points, windows)
  live in `CFG` at the top of `gex_tracker.py`. If you change them mid-stream, note the
  date, because older rows were scored under the old settings.
- **Days can be missed.** GitHub's scheduled runs sometimes start a few minutes late. If
  a snapshot hasn't run by 11:30 ET, that day is skipped rather than logged with stale levels.
