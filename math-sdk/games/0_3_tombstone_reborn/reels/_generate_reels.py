"""Deterministic reel-strip generator for TOMBSTONE REBORN (6-reel ways).

The special symbols never live on the reel strips - they drop from the special
bar / last-reel lane at runtime. So the strips only carry paying symbols
(H1-H5, L1-L5, W).

  BR0   base strip: premium-sparse, low-heavy, few wilds. Most spins do NOT
        connect a 3-of-a-kind on their own - that is where the ~92% dead-spin
        base rate comes from; the specials are what turn the rare connecting
        board into a blowout.
  WCAP  premium-dense strip used only by the forced-wincap distribution, so a
        boosted spin easily forms 6-of-a-kind premium chains to ride up to the
        99,999x cap.

Run from this folder:
    ../../../env/Scripts/python.exe _generate_reels.py
"""

import os
import random

random.seed(1877)  # Tombstone, AZ - 1877

NUM_REELS = 6
STRIP_LEN = 240

# H1 Gunslinger, H2 Duchess, H3 Butcher, H4 Card Shark, H5 Preacher
# L1..L5 western trinkets, W wild (revolver)
BASE_WEIGHTS = {
    "H1": 4, "H2": 5, "H3": 7, "H4": 9, "H5": 11,
    "L1": 16, "L2": 16, "L3": 18, "L4": 18, "L5": 20,
    "W": 4,
}

# premium-dense, near no lows: for forced max-win chains only
WCAP_WEIGHTS = {
    "H1": 20, "H2": 20, "H3": 20, "H4": 20, "H5": 20,
    "L1": 2, "L2": 2, "L3": 2, "L4": 2, "L5": 2,
    "W": 14,
}


def build_strip(weights: dict) -> list[list[str]]:
    symbols = list(weights.keys())
    probs = list(weights.values())
    columns = []
    for _ in range(NUM_REELS):
        col = random.choices(symbols, weights=probs, k=STRIP_LEN)
        present = set(col)
        for sym in symbols:
            if sym not in present:
                col[random.randrange(STRIP_LEN)] = sym
        columns.append(col)
    return columns


def write_csv(path: str, columns: list[list[str]]) -> None:
    with open(path, "w", encoding="UTF-8") as fh:
        for row in zip(*columns):
            fh.write(",".join(row) + "\n")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    write_csv(os.path.join(here, "BR0.csv"), build_strip(BASE_WEIGHTS))
    write_csv(os.path.join(here, "WCAP.csv"), build_strip(WCAP_WEIGHTS))
    print("wrote BR0.csv, WCAP.csv")
    print("DONE reel generation")
