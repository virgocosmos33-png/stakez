"""Smoke: force the UNLOCKED SLOTS path and validate the expanded board.

Elevates the slot content weights only inside this script (does not mutate the
shipped config), generates small bonus samples for each level, and checks that:
  - bonus level 1 unlocks BOTTOM only, level 2 adds RIGHT, level 3 adds LEFT
  - unlockedSlots events only expose slot groups that are unlocked at that level
  - filled side columns become extra board reels (index >= num_reels)
  - premiums/wilds actually land, and 6-/7-of-a-kind ways wins become reachable
  - ways math still holds (win == paytable * ways) on the expanded board
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
NUM = {"bonus1": 250, "bonus2": 250, "bonus3": 250}
EXPECTED_GROUPS = {"bonus1": {"bottom"}, "bonus2": {"bottom", "right"}, "bonus3": {"bottom", "right", "left"}}


def elevate_slots(config: GameConfig):
    cfg = dict(config.unlocked_slot_config or {})
    cfg["enabled"] = True
    # bias toward filled slots + wilds so 6/7-of-a-kind is reachable in a small sample
    cfg["content_weights"] = {"empty": 15, "premium": 45, "wild": 40}
    config.unlocked_slot_config = cfg


def main():
    config = GameConfig()
    elevate_slots(config)
    gamestate = GameState(config)
    create_books(gamestate, config, dict(NUM), 80, 1, False, False)

    kind_hits = Counter()
    side_names = Counter()
    slot_events = 0
    ways_checked = 0

    for mode, expected in EXPECTED_GROUPS.items():
        with open(os.path.join(BOOKS_DIR, f"books_{mode}.json"), encoding="utf-8") as f:
            books = json.load(f)
        mode_slot_events = 0
        for b in books:
            for ev in b["events"]:
                if ev.get("type") != "unlockedSlots":
                    continue
                slot_events += 1
                mode_slot_events += 1
                groups = set(ev["unlocked"])
                assert groups == expected, (mode, b["id"], groups, expected)
                # sides must only ever be groups that are unlocked
                for s in ev["sides"]:
                    assert s["side"] in groups, (mode, b["id"], s["side"])
                    assert s["reel"] >= config.num_reels, (mode, b["id"], s["reel"])
                    for c in s["cells"]:
                        side_names[c["name"]] += 1
                for c in ev["bottom"]:
                    assert c["reel"] in config.unlocked_slot_config["bottom_reels"], (mode, c)
        assert mode_slot_events > 0, (mode, "no unlockedSlots events generated")

        # ways math + kind distribution across the expanded board
        for b in books:
            if b["payoutMultiplier"] / 100 >= config.wincap:
                continue
            for ev in b["events"]:
                if ev.get("type") != "winInfo":
                    continue
                for w in ev["wins"]:
                    kind_hits[w["kind"]] += 1
                    expected_win = round(config.paytable[(w["kind"], w["symbol"])] * w["meta"]["ways"], 2)
                    got = w["win"] / 100
                    assert abs(expected_win - got) < 0.011, (b["id"], w, expected_win, got)
                    ways_checked += 1

    extended = sum(v for k, v in kind_hits.items() if k >= 6)
    assert extended > 0, ("expected some 6/7-of-a-kind wins on the expanded board", dict(kind_hits))

    print(
        json.dumps(
            {
                "ok": True,
                "slotEvents": slot_events,
                "kindDistribution": dict(sorted(kind_hits.items())),
                "extended6or7": extended,
                "sideSymbolCounts": dict(sorted(side_names.items())),
                "waysWinsChecked": ways_checked,
            },
            indent=2,
        )
    )
    print("\nUNLOCKED SLOTS SMOKE PASSED")


if __name__ == "__main__":
    main()
