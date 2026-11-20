# SPX GEX touch log: summary

Sessions logged: **16** (2026-10-29 to 2026-11-19). Touches: **266**. Updated 2026-11-20 17:23 ET.

GEX levels only earn a place if they clearly beat the **control** rows (random strikes) on reject rate and bounce vs. through, over a real sample. Treat any row with fewer than ~30 touches as noise.

## GEX levels vs. control

| levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| all GEX levels | 127 | 65% | 32% | 2% | 9.9 | 11.0 |
| control (random) | 139 | 65% | 33% | 1% | 14.4 | 16.0 |

## By level type

| level | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|
| call_wall | 3 | 67% | 33% | 0% | 31.0 | 12.3 |
| put_wall | 6 | 33% | 50% | 17% | 4.0 | 15.0 |
| gamma_flip | 12 | 83% | 17% | 0% | 7.9 | 11.7 |
| 0dte_call_wall | 22 | 73% | 27% | 0% | 10.6 | 9.9 |
| 0dte_put_wall | 42 | 62% | 33% | 5% | 7.4 | 8.4 |
| major | 42 | 64% | 36% | 0% | 16.9 | 13.1 |
| control | 139 | 65% | 33% | 1% | 14.4 | 16.0 |

## By gamma regime

| regime | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| positive | GEX | 24 | 58% | 33% | 8% | 7.5 | 11.9 |
| positive | control | 6 | 67% | 33% | 0% | 12.8 | 25.5 |
| negative | GEX | 103 | 67% | 32% | 1% | 11.4 | 10.6 |
| negative | control | 133 | 65% | 33% | 2% | 14.6 | 16.0 |

## By approach

| approach | levels | touches | reject | break | chop | med bounce 30m | med through 30m |
|---|---|---|---|---|---|---|---|
| from_above | GEX | 74 | 64% | 34% | 3% | 8.6 | 11.2 |
| from_above | control | 74 | 65% | 34% | 1% | 14.7 | 19.3 |
| from_below | GEX | 53 | 68% | 30% | 2% | 11.3 | 11.0 |
| from_below | control | 65 | 66% | 32% | 2% | 12.9 | 10.8 |

Definitions: a touch = price within 1.0 pt of a level after being at least 5.0 pts away. Reject = 5.0 pts back toward the approach side within 30 min. Break = 5 straight 1-min closes 3.0+ pts beyond. Otherwise chop. Bounce/through = max move away vs. max move past the level (pts).
