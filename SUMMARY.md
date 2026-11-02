# SPX GEX touch log: summary

Sessions logged: **3** (2026-10-29 to 2026-11-02). Touches: **24**. Updated 2026-11-02 17:18 ET.

GEX levels only earn a place if they clearly beat the **control** rows (random strikes) on reject rate and bounce vs. through, over a real sample. Treat any row with fewer than ~30 touches as noise.

## GEX levels vs. control

| levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| all GEX levels | 17 | 41% | 53% | 6% | 6.0 | 7.4 |
| control (random) | 7 | 57% | 43% | 0% | 14.6 | 10.2 |

## By level type

| level | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| gamma_flip | 3 | 33% | 67% | 0% | 7.1 | 10.7 |
| 0dte_call_wall | 2 | 50% | 50% | 0% | 8.4 | 11.8 |
| 0dte_put_wall | 7 | 43% | 43% | 14% | 3.7 | 7.2 |
| major | 5 | 40% | 60% | 0% | 8.2 | 11.6 |
| control | 7 | 57% | 43% | 0% | 14.6 | 10.2 |

## By gamma regime

| regime | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| negative | GEX | 17 | 41% | 53% | 6% | 6.0 | 7.4 |
| negative | control | 7 | 57% | 43% | 0% | 14.6 | 10.2 |

## By approach

| approach | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| from_above | GEX | 11 | 36% | 64% | 0% | 3.7 | 9.1 |
| from_above | control | 5 | 60% | 40% | 0% | 14.6 | 10.2 |
| from_below | GEX | 6 | 50% | 33% | 17% | 7.7 | 4.2 |
| from_below | control | 2 | 50% | 50% | 0% | 9.1 | 12.8 |

Definitions: a touch = price within 1.0 pt of a level after being at least 5.0 pts away. Reject = 5.0 pts back toward the approach side within 30 min. Break = 5 straight 1-min closes 3.0+ pts beyond. Otherwise chop. Bounce/through = max move away vs. max move past the level (pts).
