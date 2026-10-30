# SPX GEX touch log: summary

Sessions logged: **2** (2026-10-29 to 2026-10-30). Touches: **11**. Updated 2026-10-30 18:11 ET.

GEX levels only earn a place if they clearly beat the **control** rows (random strikes) on reject rate and bounce vs. through, over a real sample. Treat any row with fewer than ~30 touches as noise.

## GEX levels vs. control

| levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| all GEX levels | 11 | 45% | 45% | 9% | 6.0 | 4.7 |
| control (random) | 0 | - | - | - | - | - |

## By level type

| level | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| gamma_flip | 1 | 100% | 0% | 0% | 14.5 | 3.0 |
| 0dte_put_wall | 5 | 40% | 40% | 20% | 3.7 | 4.7 |
| major | 5 | 40% | 60% | 0% | 8.2 | 11.6 |

## By gamma regime

| regime | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| negative | GEX | 11 | 45% | 45% | 9% | 6.0 | 4.7 |

## By approach

| approach | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| from_above | GEX | 6 | 33% | 67% | 0% | 3.5 | 8.1 |
| from_below | GEX | 5 | 60% | 20% | 20% | 8.2 | 3.6 |

Definitions: a touch = price within 1.0 pt of a level after being at least 5.0 pts away. Reject = 5.0 pts back toward the approach side within 30 min. Break = 5 straight 1-min closes 3.0+ pts beyond. Otherwise chop. Bounce/through = max move away vs. max move past the level (pts).
