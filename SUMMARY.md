# SPX GEX touch log: summary

Sessions logged: **9** (2026-10-29 to 2026-11-10). Touches: **134**. Updated 2026-11-10 16:22 ET.

GEX levels only earn a place if they clearly beat the **control** rows (random strikes) on reject rate and bounce vs. through, over a real sample. Treat any row with fewer than ~30 touches as noise.

## GEX levels vs. control

| levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| all GEX levels | 56 | 57% | 41% | 2% | 8.0 | 9.2 |
| control (random) | 78 | 76% | 23% | 1% | 14.8 | 13.1 |

## By level type

| level | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| put_wall | 1 | 0% | 100% | 0% | 2.4 | 80.6 |
| gamma_flip | 3 | 33% | 67% | 0% | 7.1 | 10.7 |
| 0dte_call_wall | 12 | 75% | 25% | 0% | 10.4 | 10.9 |
| 0dte_put_wall | 24 | 58% | 38% | 4% | 7.2 | 7.3 |
| major | 16 | 50% | 50% | 0% | 9.3 | 10.7 |
| control | 78 | 76% | 23% | 1% | 14.8 | 13.1 |

## By gamma regime

| regime | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| positive | GEX | 3 | 33% | 67% | 0% | 9.8 | 80.6 |
| positive | control | 2 | 100% | 0% | 0% | 12.8 | 67.6 |
| negative | GEX | 53 | 58% | 40% | 2% | 7.8 | 9.1 |
| negative | control | 76 | 75% | 24% | 1% | 14.8 | 12.8 |

## By approach

| approach | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| from_above | GEX | 38 | 61% | 39% | 0% | 8.6 | 8.6 |
| from_above | control | 44 | 75% | 23% | 2% | 14.9 | 16.7 |
| from_below | GEX | 18 | 50% | 44% | 6% | 7.4 | 10.2 |
| from_below | control | 34 | 76% | 24% | 0% | 13.6 | 7.8 |

Definitions: a touch = price within 1.0 pt of a level after being at least 5.0 pts away. Reject = 5.0 pts back toward the approach side within 30 min. Break = 5 straight 1-min closes 3.0+ pts beyond. Otherwise chop. Bounce/through = max move away vs. max move past the level (pts).
