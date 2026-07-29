"""Smoke test for the new ante + feature-spin modes.

Verifies on small uncompressed sims:
- ante: every base reveal shows a scatter on reel 1
- feature1/2/3: the base spin's mirrorBurst has >= 1/2/3 mirrors
"""

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(HERE, "library", "books")

NUM = {"ante": 2000, "feature1": 600, "feature2": 600, "feature3": 400}


def load(mode):
    with open(os.path.join(BOOKS_DIR, f"books_{mode}.json"), encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    config = GameConfig()
    gamestate = GameState(config)
    create_books(gamestate, config, dict(NUM), 200, 1, False, False)

    books = load("ante")
    triggers = 0
    for b in books:
        first = next(e for e in b["events"] if e["type"] == "reveal")
        col = first["board"][0]
        assert any(s["name"] == "S" for s in col), (b["id"], [s["name"] for s in col])
        if any(e["type"] == "freeSpinTrigger" for e in b["events"]):
            triggers += 1
    print(f"ante OK: {len(books)} books, all with reel-1 scatter; "
          f"raw sim triggers: {triggers} ({triggers / len(books):.3f})")

    for mode, n in (("feature1", 1), ("feature2", 2), ("feature3", 3)):
        books = load(mode)
        counts = {}
        for b in books:
            mb = None
            reveals = 0
            for e in b["events"]:
                if e["type"] == "reveal":
                    reveals += 1
                    if reveals > 1:
                        break
                elif e["type"] == "mirrorBurst" and reveals == 1:
                    mb = len(e["mirrors"])
                    break
                elif e["type"] == "freeSpinTrigger":
                    break
            assert mb is not None and mb >= n, (mode, b["id"], mb)
            counts[mb] = counts.get(mb, 0) + 1
        avg = sum(b["payoutMultiplier"] for b in books) / len(books) / 100
        print(f"{mode} OK: {len(books)} books, mirror counts {dict(sorted(counts.items()))}, "
              f"raw mean pay {avg:.2f}x")

    print("SMOKE PASSED")
