# SPX GEX touch log: summary

Sessions logged: **6** (2026-10-29 to 2026-11-05). Touches: **58**. Updated 2026-11-05 16:25 ET.

GEX levels only earn a place if they clearly beat the **control** rows (random strikes) on reject rate and bounce vs. through, over a real sample. Treat any row with fewer than ~30 touches as noise.

## GEX levels vs. control

| levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| all GEX levels | 25 | 44% | 52% | 4% | 7.1 | 9.1 |
| control (random) | 33 | 76% | 24% | 0% | 14.6 | 6.6 |

## By level type

| level | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| put_wall | 1 | 0% | 100% | 0% | 2.4 | 80.6 |
| gamma_flip | 3 | 33% | 67% | 0% | 7.1 | 10.7 |
| 0dte_call_wall | 2 | 50% | 50% | 0% | 8.4 | 11.8 |
| 0dte_put_wall | 12 | 50% | 42% | 8% | 5.5 | 6.8 |
| major | 7 | 43% | 57% | 0% | 9.8 | 11.6 |
| control | 33 | 76% | 24% | 0% | 14.6 | 6.6 |

## By gamma regime

| regime | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| positive | GEX | 3 | 33% | 67% | 0% | 9.8 | 80.6 |
| positive | control | 2 | 100% | 0% | 0% | 12.8 | 67.6 |
| negative | GEX | 22 | 45% | 50% | 5% | 6.6 | 7.4 |
| negative | control | 31 | 74% | 26% | 0% | 14.7 | 5.7 |

## By approach

| approach | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| from_above | GEX | 17 | 41% | 59% | 0% | 4.4 | 9.1 |
| from_above | control | 19 | 74% | 26% | 0% | 14.6 | 12.2 |
| from_below | GEX | 8 | 50% | 38% | 12% | 7.7 | 7.2 |
| from_below | control | 14 | 79% | 21% | 0% | 14.1 | 5.1 |

Definitions: a touch = price within 1.0 pt of a level after being at least 5.0 pts away. Reject = 5.0 pts back toward the approach side within 30 min. Break = 5 straight 1-min closes 3.0+ pts beyond. Otherwise chop. Bounce/through = max move away vs. max move past the level (pts).
