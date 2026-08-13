"""Bake the scatter reel family for the bonus-round feature.

Reads the pristine (scatter-free) BR0 and writes three strips:

  FR0.csv  the freegame strip: byte-for-byte the old BR0. Bonus-round spins
           draw from this, so a round can NEVER retrigger — the only scatter
           a round ever shows is the injected 1-in-100 upgrade drop.
  BR0.csv  the base strip: the same strip with a SPARSE sprinkle of S on
           columns 0-4 (never the sealed lane column). Sparse enough that
           3+ S is rare — natural-trigger books use BRT instead, and
           non-trigger books simply redraw the (cheap) 3+ case away. What
           this buys is real teaser scatters and 2-S anticipation in base.
  BRT.csv  the trigger strip: a DENSE sprinkle (P ~ 0.5 per column) used by
           forced-freegame books so the acceptance loop lands 'exactly 3'
           or '4 or more' scatters in a couple of draws.

S always REPLACES a low symbol (premium/wild counts are untouched) and
placements are spaced further apart than the tallest visible window of the
column, so at most ONE scatter can ever show per reel: 3/4/4/2/2 rows means
scatter counts are exact per-column presence counts, max 5 on the board.

Idempotent: always starts from FR0 if it already exists (so re-running
never stacks more scatters into BR0).
"""

import csv
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
LOWS = {"L1", "L2", "L3", "L4", "L5"}

# visible rows per column (num_rows in game_config); column 5 is the lane
WINDOWS = [3, 4, 4, 2, 2]

# how many S per column: sparse teasers for BR0, dense for BRT
SPARSE = [5, 5, 5, 4, 4]
DENSE = [34, 28, 28, 48, 48]


def read(path):
    with open(path, newline="") as fh:
        return [row for row in csv.reader(fh) if row]


def write(path, rows):
    with open(path, "w", newline="") as fh:
        csv.writer(fh).writerows(rows)


def sprinkle(rows, counts, seed):
    """Return a copy of `rows` with S replacing lows, spaced per column.

    Placement walks the strip at an even stride and snaps each slot to the
    nearest low symbol, so the required spacing always fits (a random greedy
    routinely paints itself into a corner at these densities).
    """
    rng = random.Random(seed)
    out = [list(r) for r in rows]
    n = len(out)
    for col, want in enumerate(counts):
        # spacing strictly greater than the window so two S can never be
        # visible at once (window + padding row safety margin of 1)
        gap = WINDOWS[col] + 2
        stride = n / want
        offset = rng.uniform(0, stride)
        placed = []
        for k in range(want):
            centre = int(offset + k * stride) % n
            # nearest low to the stride point that keeps the gap both ways
            best = None
            for d in range(n // 2):
                for i in ((centre + d) % n, (centre - d) % n):
                    if out[i][col] in LOWS and all(
                        min(abs(i - p), n - abs(i - p)) >= gap for p in placed
                    ):
                        best = i
                        break
                if best is not None:
                    break
            assert best is not None, f"col {col}: no slot near {centre}"
            placed.append(best)
        for i in placed:
            out[i][col] = "S"
    return out


if __name__ == "__main__":
    br0 = os.path.join(HERE, "BR0.csv")
    fr0 = os.path.join(HERE, "FR0.csv")
    # FR0 is the pristine source of truth once it exists
    if not os.path.exists(fr0):
        write(fr0, read(br0))
    base = read(fr0)

    write(br0, sprinkle(base, SPARSE, seed=133))
    write(os.path.join(HERE, "BRT.csv"), sprinkle(base, DENSE, seed=777))

    for name in ("FR0", "BR0", "BRT"):
        rows = read(os.path.join(HERE, f"{name}.csv"))
        per_col = [sum(1 for r in rows if r[c] == "S") for c in range(6)]
        print(f"{name}: {len(rows)} rows, S per column = {per_col}")
