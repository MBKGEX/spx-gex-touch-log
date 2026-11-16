# SPX GEX touch log: summary

Sessions logged: **13** (2026-10-29 to 2026-11-16). Touches: **175**. Updated 2026-11-16 17:23 ET.

GEX levels only earn a place if they clearly beat the **control** rows (random strikes) on reject rate and bounce vs. through, over a real sample. Treat any row with fewer than ~30 touches as noise.

## GEX levels vs. control

| levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| all GEX levels | 83 | 60% | 36% | 4% | 8.0 | 9.2 |
| control (random) | 92 | 72% | 27% | 1% | 14.5 | 12.4 |

## By level type

| level | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| put_wall | 6 | 33% | 50% | 17% | 4.0 | 15.0 |
| gamma_flip | 12 | 83% | 17% | 0% | 7.9 | 11.7 |
| 0dte_call_wall | 18 | 67% | 33% | 0% | 9.0 | 11.6 |
| 0dte_put_wall | 30 | 57% | 37% | 7% | 7.2 | 7.3 |
| major | 17 | 53% | 47% | 0% | 9.8 | 9.8 |
| control | 92 | 72% | 27% | 1% | 14.5 | 12.4 |

## By gamma regime

| regime | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| positive | GEX | 24 | 58% | 33% | 8% | 7.5 | 11.9 |
| positive | control | 6 | 67% | 33% | 0% | 12.8 | 25.5 |
| negative | GEX | 59 | 61% | 37% | 2% | 8.2 | 9.1 |
| negative | control | 86 | 72% | 27% | 1% | 14.6 | 12.4 |

## By approach

| approach | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| from_above | GEX | 50 | 58% | 38% | 4% | 7.2 | 8.6 |
| from_above | control | 50 | 72% | 26% | 2% | 14.7 | 15.9 |
| from_below | GEX | 33 | 64% | 33% | 3% | 8.2 | 11.0 |
| from_below | control | 42 | 71% | 29% | 0% | 13.1 | 8.2 |

Definitions: a touch = price within 1.0 pt of a level after being at least 5.0 pts away. Reject = 5.0 pts back toward the approach side within 30 min. Break = 5 straight 1-min closes 3.0+ pts beyond. Otherwise chop. Bounce/through = max move away vs. max move past the level (pts).
