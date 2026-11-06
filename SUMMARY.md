# SPX GEX touch log: summary

Sessions logged: **7** (2026-10-29 to 2026-11-06). Touches: **102**. Updated 2026-11-06 16:21 ET.

GEX levels only earn a place if they clearly beat the **control** rows (random strikes) on reject rate and bounce vs. through, over a real sample. Treat any row with fewer than ~30 touches as noise.

## GEX levels vs. control

| levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| all GEX levels | 41 | 56% | 41% | 2% | 7.2 | 9.1 |
| control (random) | 61 | 75% | 25% | 0% | 14.7 | 12.2 |

## By level type

| level | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| put_wall | 1 | 0% | 100% | 0% | 2.4 | 80.6 |
| gamma_flip | 3 | 33% | 67% | 0% | 7.1 | 10.7 |
| 0dte_call_wall | 10 | 70% | 30% | 0% | 7.7 | 8.3 |
| 0dte_put_wall | 20 | 60% | 35% | 5% | 6.6 | 7.3 |
| major | 7 | 43% | 57% | 0% | 9.8 | 11.6 |
| control | 61 | 75% | 25% | 0% | 14.7 | 12.2 |

## By gamma regime

| regime | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| positive | GEX | 3 | 33% | 67% | 0% | 9.8 | 80.6 |
| positive | control | 2 | 100% | 0% | 0% | 12.8 | 67.6 |
| negative | GEX | 38 | 58% | 39% | 3% | 7.2 | 7.5 |
| negative | control | 59 | 75% | 25% | 0% | 14.8 | 11.7 |

## By approach

| approach | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| from_above | GEX | 29 | 59% | 41% | 0% | 7.2 | 7.5 |
| from_above | control | 33 | 70% | 30% | 0% | 14.6 | 14.1 |
| from_below | GEX | 12 | 50% | 42% | 8% | 7.7 | 11.1 |
| from_below | control | 28 | 82% | 18% | 0% | 15.1 | 5.6 |

Definitions: a touch = price within 1.0 pt of a level after being at least 5.0 pts away. Reject = 5.0 pts back toward the approach side within 30 min. Break = 5 straight 1-min closes 3.0+ pts beyond. Otherwise chop. Bounce/through = max move away vs. max move past the level (pts).
