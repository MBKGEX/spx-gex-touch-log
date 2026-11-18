# SPX GEX touch log: summary

Sessions logged: **15** (2026-10-29 to 2026-11-18). Touches: **218**. Updated 2026-11-18 16:33 ET.

GEX levels only earn a place if they clearly beat the **control** rows (random strikes) on reject rate and bounce vs. through, over a real sample. Treat any row with fewer than ~30 touches as noise.

## GEX levels vs. control

| levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| all GEX levels | 107 | 63% | 35% | 3% | 8.9 | 10.6 |
| control (random) | 111 | 69% | 29% | 2% | 12.8 | 13.1 |

## By level type

| level | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| put_wall | 6 | 33% | 50% | 17% | 4.0 | 15.0 |
| gamma_flip | 12 | 83% | 17% | 0% | 7.9 | 11.7 |
| 0dte_call_wall | 21 | 71% | 29% | 0% | 11.4 | 9.2 |
| 0dte_put_wall | 39 | 59% | 36% | 5% | 7.2 | 8.2 |
| major | 29 | 59% | 41% | 0% | 16.8 | 11.6 |
| control | 111 | 69% | 29% | 2% | 12.8 | 13.1 |

## By gamma regime

| regime | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| positive | GEX | 24 | 58% | 33% | 8% | 7.5 | 11.9 |
| positive | control | 6 | 67% | 33% | 0% | 12.8 | 25.5 |
| negative | GEX | 83 | 64% | 35% | 1% | 9.7 | 9.2 |
| negative | control | 105 | 70% | 29% | 2% | 12.8 | 13.1 |

## By approach

| approach | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| from_above | GEX | 62 | 60% | 37% | 3% | 7.4 | 9.9 |
| from_above | control | 58 | 71% | 28% | 2% | 14.6 | 16.4 |
| from_below | GEX | 45 | 67% | 31% | 2% | 10.3 | 10.7 |
| from_below | control | 53 | 68% | 30% | 2% | 12.2 | 9.9 |

Definitions: a touch = price within 1.0 pt of a level after being at least 5.0 pts away. Reject = 5.0 pts back toward the approach side within 30 min. Break = 5 straight 1-min closes 3.0+ pts beyond. Otherwise chop. Bounce/through = max move away vs. max move past the level (pts).
