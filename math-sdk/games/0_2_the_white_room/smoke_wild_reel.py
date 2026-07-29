"""Smoke: force the WILD REEL path and validate the grown-reel bookkeeping.

Elevates the per-reel trigger probability only inside this script (does not
mutate the shipped config), generates a small base sample, and checks that:
  - wildReel events fire on the eligible middle reels (1, 2, 3)
  - each triggered reel grows from its baseRows to target_rows (4)
  - the risen cells are WILDs carrying a multiplier from mult_weights
  - ways math still holds (win == paytable * ways) with the grown board
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(HERE, "library", "books")
NUM = {"base": 1200}


def elevate_wild_reel(config: GameConfig):
    cfg = dict(config.wild_reel_config or {})
    cfg["enabled"] = True
    cfg["probability"] = {config.basegame_type: 0.6, config.freegame_type: 0.6}
    config.wild_reel_config = cfg


def main():
    config = GameConfig()
    elevate_wild_reel(config)
    gamestate = GameState(config)
    create_books(gamestate, config, dict(NUM), 80, 1, False, False)

    with open(os.path.join(BOOKS_DIR, "books_base.json"), encoding="utf-8") as f:
        books = json.load(f)

    wr_books = [b for b in books if any(e.get("type") == "wildReel" for e in b["events"])]
    assert wr_books, "expected wildReel events in elevated smoke"

    eligible = set(config.wild_reel_config["eligible_reels"])
    target = config.wild_reel_config["target_rows"]
    mult_keys = set(config.wild_reel_config["mult_weights"].keys())
    reel_hits = Counter()
    mult_hits = Counter()
    total_events = 0

    for b in books:
        for ev in b["events"]:
            if ev.get("type") != "wildReel":
                continue
            total_events += 1
            assert ev["reels"], (b["id"], "wildReel with no reels")
            for r in ev["reels"]:
                reel = r["reel"]
                assert reel in eligible, (b["id"], "wild reel on ineligible reel", reel)
                assert r["baseRows"] == config.num_rows[reel], (b["id"], r)
                assert r["added"] == target - r["baseRows"], (b["id"], r)
                assert len(r["cells"]) == r["added"], (b["id"], r)
                reel_hits[reel] += 1
                for k, cell in enumerate(r["cells"]):
                    # padding-adjusted row of the k-th risen cell
                    assert cell["row"] == r["baseRows"] + 1 + k, (b["id"], r, cell)
                    assert cell["multiplier"] in mult_keys, (b["id"], cell)
                    mult_hits[cell["multiplier"]] += 1

    # ways math must still hold with the grown board (skip wincap-clamped)
    checked = 0
    for b in books:
        if b["payoutMultiplier"] / 100 >= config.wincap:
            continue
        for ev in b["events"]:
            if ev["type"] != "winInfo":
                continue
            for w in ev["wins"]:
                expected = round(config.paytable[(w["kind"], w["symbol"])] * w["meta"]["ways"], 2)
                got = w["win"] / 100
                assert abs(expected - got) < 0.011, (b["id"], w, expected, got)
                checked += 1

    print(
        json.dumps(
            {
                "ok": True,
                "totalBooks": len(books),
                "wildReelBooks": len(wr_books),
                "wildReelEvents": total_events,
                "perReelHits": dict(sorted(reel_hits.items())),
                "multDistribution": dict(sorted(mult_hits.items())),
                "waysWinsChecked": checked,
            },
            indent=2,
        )
    )
    print("\nWILD REEL SMOKE PASSED")


if __name__ == "__main__":
    main()
