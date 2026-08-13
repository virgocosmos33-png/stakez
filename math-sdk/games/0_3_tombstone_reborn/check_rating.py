"""Recompute the Stake Engine rating metrics from the published lookup tables.

Reads library/publish_files/lookUpTable_<mode>_0.csv (id, weight, payout-in-
cents-of-base-bet) and prints, per mode, every number on the Stake rating
screen so a retune can be verified locally BEFORE uploading:

    RTP, std dev (per stake), P(x >= 5000), P(x >= 10000),
    CVaR 0.1% (per stake and absolute), ETL share above 40x-cost and 10,000x.

3-star limits (from the dashboard): std <= 60, P(10k) <= 0.01,
CVaR_abs <= 50,000, P(5k) <= 0.05, CVaR_stake <= 700, ETL40 <= 0.90,
ETL10k <= 0.80.
"""

import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MODES = {
    "base": 1.0,
    "bonus_small": 80.0,
    "bonus_super": 1000.0,
    "freespins": 80.0,
    "superspins": 2000.0,
}


def load(mode):
    path = os.path.join(HERE, "library", "publish_files", f"lookUpTable_{mode}_0.csv")
    rows = []
    with open(path, newline="") as fh:
        for rec in csv.reader(fh):
            rows.append((int(rec[1]), int(rec[2]) / 100.0))  # (weight, x in base-bet multiples)
    return rows


def analyze(mode, cost):
    rows = load(mode)
    tw = sum(w for w, _ in rows)
    mean = sum(w * x for w, x in rows) / tw
    rtp = mean / cost
    # per-stake variance (x/cost)
    var = sum(w * (x / cost - rtp) ** 2 for w, x in rows) / tw
    std = math.sqrt(var)

    def tail_p(t):
        return sum(w for w, x in rows if x >= t) / tw

    # CVaR: expected payout of the worst (largest-liability) 0.1% of rounds
    q = 0.001 * tw
    acc_w = 0
    acc_wx = 0.0
    for w, x in sorted(rows, key=lambda r: -r[1]):
        take = min(w, q - acc_w)
        if take <= 0:
            break
        acc_w += take
        acc_wx += take * x
    cvar_abs = acc_wx / acc_w if acc_w else 0.0
    cvar_stake = cvar_abs / cost

    total_wx = sum(w * x for w, x in rows)

    def etl_share(t):
        return sum(w * x for w, x in rows if x > t) / total_wx if total_wx else 0.0

    print(f"--- {mode} (cost {cost:g}) ---")
    print(f"  RTP                 {rtp:.5f}")
    print(f"  std dev (per stake) {std:.2f}   (3-star limit 60, base only)")
    print(f"  P(x >= 5,000x)      {tail_p(5000):.4f} (3-star limit 0.0500)")
    print(f"  P(x >= 10,000x)     {tail_p(10000):.4f} (3-star limit 0.0100)")
    print(f"  CVaR0.1% per stake  {cvar_stake:.1f}   (3-star limit 700)")
    print(f"  CVaR0.1% absolute   {cvar_abs:.1f}   (3-star limit 50000)")
    print(f"  ETL share > 40x cost   {etl_share(40 * cost):.3f} (limit 0.900)")
    print(f"  ETL share > 10,000x    {etl_share(10000):.3f} (limit 0.800)")


if __name__ == "__main__":
    for m, c in MODES.items():
        analyze(m, c)
