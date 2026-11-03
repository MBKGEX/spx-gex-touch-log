# SPX GEX touch log: summary

Sessions logged: **4** (2026-10-29 to 2026-11-03). Touches: **29**. Updated 2026-11-03 17:18 ET.

GEX levels only earn a place if they clearly beat the **control** rows (random strikes) on reject rate and bounce vs. through, over a real sample. Treat any row with fewer than ~30 touches as noise.

## GEX levels vs. control

| levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| all GEX levels | 22 | 45% | 50% | 5% | 6.6 | 7.4 |
| control (random) | 7 | 57% | 43% | 0% | 14.6 | 10.2 |

## By level type

| level | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| gamma_flip | 3 | 33% | 67% | 0% | 7.1 | 10.7 |
| 0dte_call_wall | 2 | 50% | 50% | 0% | 8.4 | 11.8 |
| 0dte_put_wall | 12 | 50% | 42% | 8% | 5.5 | 6.8 |
| major | 5 | 40% | 60% | 0% | 8.2 | 11.6 |
| control | 7 | 57% | 43% | 0% | 14.6 | 10.2 |

## By gamma regime

| regime | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| negative | GEX | 22 | 45% | 50% | 5% | 6.6 | 7.4 |
| negative | control | 7 | 57% | 43% | 0% | 14.6 | 10.2 |

## By approach

| approach | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| from_above | GEX | 15 | 47% | 53% | 0% | 4.4 | 7.4 |
| from_above | control | 5 | 60% | 40% | 0% | 14.6 | 10.2 |
| from_below | GEX | 7 | 43% | 43% | 14% | 7.1 | 4.7 |
| from_below | control | 2 | 50% | 50% | 0% | 9.1 | 12.8 |

Definitions: a touch = price within 1.0 pt of a level after being at least 5.0 pts away. Reject = 5.0 pts back toward the approach side within 30 min. Break = 5 straight 1-min closes 3.0+ pts beyond. Otherwise chop. Bounce/through = max move away vs. max move past the level (pts).
