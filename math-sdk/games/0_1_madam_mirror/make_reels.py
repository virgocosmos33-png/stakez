"""Generate reel strips for Madam Mirror.

Rules:
- Base reels (BR0): scatter-rich on reels 1/3/5 (index 0/2/4), scarce on 2/4.
  All reels need >=1 scatter so 4- and 5-scatter triggers (bonus levels 2/3)
  can be forced by force_special_board.
- Wilds only on reels 2/3/4 (index 1/2/3), sparse in base, richer in free reels.
- Haunted Mirrors (HM) are NOT on strips - they are placed by game_override.
- Free reels (FR0) carry scatters on all reels (retriggers) and more wilds.
- Wincap reels (FRWCAP) are wild/high heavy for forcing 30,000x sims.
"""

import os
import random

STRIP_LEN = 250
NUM_REELS = 5
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reels")

# per-reel symbol weights
BASE_WEIGHTS = {"H1": 4, "H2": 5, "H3": 6, "H4": 7, "L1": 12, "L2": 13, "L3": 14, "L4": 14, "L5": 15}
FREE_WEIGHTS = {"H1": 6, "H2": 7, "H3": 8, "H4": 8, "L1": 11, "L2": 12, "L3": 12, "L4": 12, "L5": 12}
WCAP_WEIGHTS = {"H1": 14, "H2": 12, "H3": 8, "H4": 6, "L1": 6, "L2": 6, "L3": 5, "L4": 5, "L5": 5}

# scatters per base reel: rich on 0/2/4 (anticipation reels), rare on 1/3
BASE_SCATTERS_PER_REEL = [8, 2, 8, 2, 8]
WILD_REELS = [1, 2, 3]
MIN_SCATTER_GAP = 12  # rows between scatters on a strip (board shows 4 rows)


def build_strip(weights, num_scatters, num_wilds, allow_scatter, allow_wild, rng):
    names = list(weights.keys())
    wts = list(weights.values())
    strip = [rng.choices(names, weights=wts)[0] for _ in range(STRIP_LEN)]

    def spaced_positions(count, taken):
        positions = []
        attempts = 0
        while len(positions) < count and attempts < 5000:
            attempts += 1
            p = rng.randrange(STRIP_LEN)
            if all(min(abs(p - q), STRIP_LEN - abs(p - q)) >= MIN_SCATTER_GAP for q in positions + taken):
                positions.append(p)
        return positions

    scatter_positions = spaced_positions(num_scatters, []) if allow_scatter else []
    for p in scatter_positions:
        strip[p] = "S"
    wild_positions = spaced_positions(num_wilds, scatter_positions) if allow_wild else []
    for p in wild_positions:
        strip[p] = "W"
    return strip


def write_csv(filename, strips):
    with open(os.path.join(HERE, filename), "w", encoding="utf-8", newline="") as f:
        for row in range(STRIP_LEN):
            f.write(",".join(strips[reel][row] for reel in range(NUM_REELS)) + "\n")
    print(f"wrote {filename}")


if __name__ == "__main__":
    rng = random.Random(1897)
    os.makedirs(HERE, exist_ok=True)

    base = [
        build_strip(
            BASE_WEIGHTS,
            num_scatters=BASE_SCATTERS_PER_REEL[reel],
            num_wilds=5,
            allow_scatter=True,
            allow_wild=(reel in WILD_REELS),
            rng=rng,
        )
        for reel in range(NUM_REELS)
    ]
    free = [
        build_strip(
            FREE_WEIGHTS,
            num_scatters=5,
            num_wilds=9,
            allow_scatter=True,
            allow_wild=(reel in WILD_REELS),
            rng=rng,
        )
        for reel in range(NUM_REELS)
    ]
    wcap = [
        build_strip(
            WCAP_WEIGHTS,
            num_scatters=4,
            num_wilds=16,
            allow_scatter=True,
            allow_wild=(reel in WILD_REELS),
            rng=rng,
        )
        for reel in range(NUM_REELS)
    ]
    # base wincap strip: wild/H1 heavy, NO scatters (a base wincap spin must
    # not trigger the bonus) - only ever drawn by the base wincap search
    base_wcap = [
        build_strip(
            WCAP_WEIGHTS,
            num_scatters=0,
            num_wilds=22,
            allow_scatter=False,
            allow_wild=(reel in WILD_REELS),
            rng=rng,
        )
        for reel in range(NUM_REELS)
    ]

    write_csv("BR0.csv", base)
    write_csv("FR0.csv", free)
    write_csv("FRWCAP.csv", wcap)
    write_csv("BRWCAP.csv", base_wcap)
