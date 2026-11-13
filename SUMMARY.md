# SPX GEX touch log: summary

Sessions logged: **12** (2026-10-29 to 2026-11-13). Touches: **164**. Updated 2026-11-13 16:29 ET.

GEX levels only earn a place if they clearly beat the **control** rows (random strikes) on reject rate and bounce vs. through, over a real sample. Treat any row with fewer than ~30 touches as noise.

## GEX levels vs. control

| levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| all GEX levels | 79 | 59% | 37% | 4% | 8.0 | 9.2 |
| control (random) | 85 | 75% | 24% | 1% | 14.8 | 12.4 |

## By level type

| level | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| put_wall | 6 | 33% | 50% | 17% | 4.0 | 15.0 |
| gamma_flip | 12 | 83% | 17% | 0% | 7.9 | 11.7 |
| 0dte_call_wall | 16 | 69% | 31% | 0% | 9.0 | 10.9 |
| 0dte_put_wall | 29 | 55% | 38% | 7% | 7.2 | 7.4 |
| major | 16 | 50% | 50% | 0% | 9.3 | 10.7 |
| control | 85 | 75% | 24% | 1% | 14.8 | 12.4 |

## By gamma regime

| regime | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| positive | GEX | 24 | 58% | 33% | 8% | 7.5 | 11.9 |
| positive | control | 6 | 67% | 33% | 0% | 12.8 | 25.5 |
| negative | GEX | 55 | 60% | 38% | 2% | 8.2 | 9.1 |
| negative | control | 79 | 76% | 23% | 1% | 14.8 | 12.4 |

## By approach

| approach | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| from_above | GEX | 46 | 57% | 39% | 4% | 7.2 | 8.6 |
| from_above | control | 45 | 76% | 22% | 2% | 14.9 | 16.6 |
| from_below | GEX | 33 | 64% | 33% | 3% | 8.2 | 11.0 |
| from_below | control | 40 | 75% | 25% | 0% | 13.6 | 6.7 |

Definitions: a touch = price within 1.0 pt of a level after being at least 5.0 pts away. Reject = 5.0 pts back toward the approach side within 30 min. Break = 5 straight 1-min closes 3.0+ pts beyond. Otherwise chop. Bounce/through = max move away vs. max move past the level (pts).
