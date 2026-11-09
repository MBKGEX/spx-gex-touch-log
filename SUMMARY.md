# SPX GEX touch log: summary

Sessions logged: **8** (2026-10-29 to 2026-11-09). Touches: **121**. Updated 2026-11-09 17:20 ET.

GEX levels only earn a place if they clearly beat the **control** rows (random strikes) on reject rate and bounce vs. through, over a real sample. Treat any row with fewer than ~30 touches as noise.

## GEX levels vs. control

| levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| all GEX levels | 47 | 60% | 38% | 2% | 8.2 | 9.2 |
| control (random) | 74 | 77% | 23% | 0% | 14.8 | 13.6 |

## By level type

| level | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| put_wall | 1 | 0% | 100% | 0% | 2.4 | 80.6 |
| gamma_flip | 3 | 33% | 67% | 0% | 7.1 | 10.7 |
| 0dte_call_wall | 12 | 75% | 25% | 0% | 10.4 | 10.9 |
| 0dte_put_wall | 20 | 60% | 35% | 5% | 6.6 | 7.3 |
| major | 11 | 55% | 45% | 0% | 13.6 | 15.8 |
| control | 74 | 77% | 23% | 0% | 14.8 | 13.6 |

## By gamma regime

| regime | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| positive | GEX | 3 | 33% | 67% | 0% | 9.8 | 80.6 |
| positive | control | 2 | 100% | 0% | 0% | 12.8 | 67.6 |
| negative | GEX | 44 | 61% | 36% | 2% | 7.7 | 9.1 |
| negative | control | 72 | 76% | 24% | 0% | 14.8 | 13.1 |

## By approach

| approach | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| from_above | GEX | 34 | 65% | 35% | 0% | 9.1 | 8.3 |
| from_above | control | 42 | 76% | 24% | 0% | 14.9 | 17.1 |
| from_below | GEX | 13 | 46% | 46% | 8% | 7.1 | 11.6 |
| from_below | control | 32 | 78% | 22% | 0% | 13.6 | 7.8 |

Definitions: a touch = price within 1.0 pt of a level after being at least 5.0 pts away. Reject = 5.0 pts back toward the approach side within 30 min. Break = 5 straight 1-min closes 3.0+ pts beyond. Otherwise chop. Bounce/through = max move away vs. max move past the level (pts).
