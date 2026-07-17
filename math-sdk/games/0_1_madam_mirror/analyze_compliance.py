"""Grade the optimized math against Stake Engine's Math Verification checklist.

Reads the post-optimization lookup tables (sim, weight, payout-x100) and reports
per-mode and cross-mode compliance:
  - RTP within 90.0-96.7%, all modes within 0.5% of each other
  - non-zero hit rate (< 1 in 20), zero-payout share
  - base-mode standard deviation within 0.6-60.0 (3-star)
  - maxwin reachable, more frequent than ~1 in 10,000,000
  - P(>=5000x) <= 1e-2 and P(>=10000x) <= 2e-2 after cost-multiplier scaling
  - CVaR (worst 0.1% expected payout / cost) <= 800
  - ETL: RTP share from wins >= 40x cost <= 0.9, RTP share above 10000x <= 0.8
  - win-range hit rates (gap detection between small pays and the cap)
  - dominance of the single most likely non-zero payout
"""

import csv
import math
import os

from game_config import GameConfig

HERE = os.path.dirname(os.path.abspath(__file__))
# the optimizer writes the weighted tables to publish_files; the plain
# lookup_tables copies keep weight=1 and must not be graded
LOOKUP_DIR = os.path.join(HERE, "library", "publish_files")

RTP_MIN, RTP_MAX, RTP_SPREAD = 0.90, 0.967, 0.005
P5000_LIMIT, P10000_LIMIT = 1e-2, 2e-2
CVAR_LIMIT = 800
ETL40_LIMIT, ETL10K_LIMIT = 0.9, 0.8
STD_MIN, STD_MAX = 0.6, 60.0


def cost_scaling(cost):
    if cost >= 1000:
        return 0.2
    if cost >= 500:
        return 0.5
    if cost >= 200:
        return 0.8
    return 1.0


def load_lookup(mode):
    path = os.path.join(LOOKUP_DIR, f"lookUpTable_{mode}_0.csv")
    if not os.path.exists(path):
        path = os.path.join(LOOKUP_DIR, f"lookUpTable_{mode}.csv")
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) < 3:
                continue
            rows.append((int(row[0]), int(row[1]), int(row[2]) / 100.0))
    return rows


def analyze_mode(mode, cost, wincap):
    rows = load_lookup(mode)
    total_weight = sum(w for _, w, _ in rows)
    probs = [(payout, w / total_weight) for _, w, payout in rows if w > 0]
    zero_weight_rows = sum(1 for _, w, _ in rows if w == 0)

    rtp = sum(p * pr for p, pr in probs) / cost
    nonzero_prob = sum(pr for p, pr in probs if p > 0)
    zero_prob = 1 - nonzero_prob

    mean = sum(p * pr for p, pr in probs)
    variance = sum(pr * (p - mean) ** 2 for p, pr in probs)
    std_normalized = math.sqrt(variance) / cost

    p5000 = sum(pr for p, pr in probs if p >= 5000) * cost_scaling(cost)
    p10000 = sum(pr for p, pr in probs if p >= 10000) * cost_scaling(cost)
    p_wincap = sum(pr for p, pr in probs if p >= wincap)

    # CVaR: expected payout in the worst (largest-payout) 0.1% of outcomes
    tail = 0.001
    acc_prob, acc_pay = 0.0, 0.0
    for p, pr in sorted(probs, key=lambda x: -x[0]):
        take = min(pr, tail - acc_prob)
        acc_pay += p * take
        acc_prob += take
        if acc_prob >= tail - 1e-15:
            break
    cvar_norm = (acc_pay / tail) / cost

    total_return = sum(p * pr for p, pr in probs)
    etl40 = sum(p * pr for p, pr in probs if p >= 40 * cost) / total_return if total_return else 0
    etl10k = sum(p * pr for p, pr in probs if p >= 10000) / total_return if total_return else 0

    # win-range gap check (payouts in x-cost bands)
    bands = [(0, 1), (1, 5), (5, 20), (20, 100), (100, 500), (500, 2000), (2000, 10000), (10000, wincap + 1)]
    band_hits = {}
    for lo, hi in bands:
        band_hits[f"{lo}-{hi}x"] = sum(pr for p, pr in probs if lo <= p / cost < hi)

    nonzero = [(p, pr) for p, pr in probs if p > 0]
    dominant = max(nonzero, key=lambda x: x[1]) if nonzero else (0, 0)

    return {
        "mode": mode,
        "cost": cost,
        "rtp": rtp,
        "zero_prob": zero_prob,
        "nonzero_hit": nonzero_prob,
        "std_normalized": std_normalized,
        "p5000_scaled": p5000,
        "p10000_scaled": p10000,
        "p_wincap": p_wincap,
        "cvar_norm": cvar_norm,
        "etl40": etl40,
        "etl10k": etl10k,
        "band_hits": band_hits,
        "dominant": dominant,
        "zero_weight_rows": zero_weight_rows,
        "rows": len(rows),
    }


def flag(ok):
    return "PASS" if ok else "** FAIL **"


if __name__ == "__main__":
    config = GameConfig()
    results = []
    for bm in config.bet_modes:
        results.append(analyze_mode(bm.get_name(), bm.get_cost(), bm.get_wincap()))

    print("=" * 74)
    print("STAKE ENGINE MATH VERIFICATION - COMPLIANCE REPORT")
    print("=" * 74)

    rtps = [r["rtp"] for r in results]
    spread = max(rtps) - min(rtps)
    for r in results:
        print(f"\n--- {r['mode']} (cost {r['cost']}x, {r['rows']} sims, {r['zero_weight_rows']} zero-weight) ---")
        print(f"  RTP: {r['rtp'] * 100:.3f}%   {flag(RTP_MIN <= r['rtp'] <= RTP_MAX)}")
        print(f"  zero-payout share: {r['zero_prob'] * 100:.2f}%   non-zero hit rate: 1 in {1 / r['nonzero_hit']:.2f}"
              f"   {flag(r['nonzero_hit'] >= 1 / 20 if r['cost'] == 1 else True)}")
        if r["cost"] == 1:
            print(f"  std dev (normalized): {r['std_normalized']:.2f}   {flag(STD_MIN <= r['std_normalized'] <= STD_MAX)}")
        print(f"  P(>=5000x) scaled: {r['p5000_scaled']:.2e}   {flag(r['p5000_scaled'] <= P5000_LIMIT)}")
        print(f"  P(>=10000x) scaled: {r['p10000_scaled']:.2e}   {flag(r['p10000_scaled'] <= P10000_LIMIT)}")
        wincap_hr = 1 / r["p_wincap"] if r["p_wincap"] else float("inf")
        print(f"  maxwin (30000x) hit rate: 1 in {wincap_hr:,.0f}   {flag(r['p_wincap'] > 0)}")
        print(f"  CVaR (worst 0.1%, /cost): {r['cvar_norm']:.1f}   {flag(r['cvar_norm'] <= CVAR_LIMIT)}")
        print(f"  ETL share >=40x cost: {r['etl40']:.3f}   {flag(r['etl40'] <= ETL40_LIMIT)}")
        print(f"  ETL share >=10000x: {r['etl10k']:.3f}   {flag(r['etl10k'] <= ETL10K_LIMIT)}")
        dom_p, dom_pr = r["dominant"]
        print(f"  most likely non-zero payout: {dom_p:.2f} at {dom_pr * 100:.2f}% of spins")
        print("  win-band probabilities (x cost):")
        for band, pr in r["band_hits"].items():
            marker = "  <-- GAP" if pr == 0 else ""
            print(f"    {band:>14}: {pr:.5f}{marker}")

    print(f"\n--- cross-mode ---")
    print(f"  RTP spread across modes: {spread * 100:.3f}%   {flag(spread <= RTP_SPREAD)}")
    print(f"  worst P(>=5000x): {max(r['p5000_scaled'] for r in results):.2e}   "
          f"{flag(max(r['p5000_scaled'] for r in results) <= P5000_LIMIT)}")
    print(f"  worst P(>=10000x): {max(r['p10000_scaled'] for r in results):.2e}   "
          f"{flag(max(r['p10000_scaled'] for r in results) <= P10000_LIMIT)}")
