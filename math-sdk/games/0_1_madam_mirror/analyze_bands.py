"""Reproduce the Stake Engine dashboard's hit-rate/RTP-contribution table
locally from an optimized lookup table, so distribution shape is verified
BEFORE uploading.

Usage:
    python analyze_bands.py [mode ...]     (default: base)

Prints, per win-range band (in x bet):
    distribution count, weight probability, effective hit-rate (1 in N),
    and total RTP contribution %.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# publish_files holds the OPTIMIZED weights (lookup_tables/ has raw unit
# weights from the sim phase and says nothing about the final distribution)
LOOKUP_DIR = os.path.join(HERE, "library", "publish_files")

MODE_COSTS = {
    "base": 1.0,
    "ante": 1.25,
    "feature1": 10.0,
    "feature2": 20.0,
    "feature3": 40.0,
    "bonus1": 100.0,
    "bonus2": 400.0,
    "bonus3": 1000.0,
}

# same bands the Stake Engine dashboard uses (x bet)
BANDS = [
    (0, 0.1), (0.1, 1), (1, 2), (2, 5), (5, 10), (10, 20), (20, 50),
    (50, 100), (100, 200), (200, 500), (500, 1000), (1000, 2000),
    (2000, 5000), (5000, 10000), (10000, 20000), (20000, 100000),
]


def analyze(mode):
    path = os.path.join(LOOKUP_DIR, f"lookUpTable_{mode}_0.csv")
    cost = MODE_COSTS[mode]
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            _, weight, payout = line.strip().split(",")
            rows.append((float(weight), float(payout) / 100.0))  # payout in x bet

    total_weight = sum(w for w, _ in rows)
    total_rtp = sum(w * p for w, p in rows) / total_weight / cost
    zero_weight = sum(w for w, p in rows if p == 0)

    print(f"\n=== {mode} (cost {cost}x) ===")
    print(f"books: {len(rows):,}   RTP: {total_rtp * 100:.2f}%   zero rate: {zero_weight / total_weight * 100:.2f}%")
    print(f"{'range (x bet)':>18} | {'count':>7} | {'hit-rate 1 in':>14} | {'rtp contrib':>11}")
    print("-" * 62)
    prev_contrib = None
    for lo, hi in BANDS:
        in_band = [(w, p) for w, p in rows if lo < p <= hi]
        count = len(in_band)
        band_weight = sum(w for w, _ in in_band)
        contrib = sum(w * p for w, p in in_band) / total_weight / cost / total_rtp * 100
        hr = (total_weight / band_weight) if band_weight else float("inf")
        hr_str = f"{hr:,.0f}" if band_weight else "never"
        # flag inversions above 100x: a bigger-win band should not be MORE
        # likely than the band below it (the 'cliff' the old table had)
        flag = ""
        if lo >= 500 and prev_contrib is not None and band_weight:
            if contrib > prev_contrib * 3:
                flag = "  <-- spike"
        print(f"{f'({lo}, {hi})':>18} | {count:>7,} | {hr_str:>14} | {contrib:>10.2f}%{flag}")
        prev_contrib = contrib

    # cliff check: for every adjacent pair of bands >= 100x, effective
    # hit-rate should not jump by more than ~50x between neighbours
    print("\ntaper check (bands >= 100x, adjacent hit-rate ratio):")
    prev = None
    for lo, hi in BANDS:
        if lo < 100:
            continue
        band_weight = sum(w for w, p in rows if lo < p <= hi)
        hr = (total_weight / band_weight) if band_weight else float("inf")
        if prev is not None and prev > 0:
            ratio = hr / prev
            status = "OK" if ratio < 50 else "CLIFF"
            print(f"  ({lo}, {hi}): 1 in {hr:,.0f}   x{ratio:,.1f} vs previous band   {status}")
        prev = hr


if __name__ == "__main__":
    modes = sys.argv[1:] or ["base"]
    for m in modes:
        analyze(m)
