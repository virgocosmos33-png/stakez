"""Build ONE self-contained Storybook spin that is a RICH but NATURAL feature spin:
as many CLONE / SPLIT / WILD-REEL / STRETCH features as a real level-3 bonus spin
rolls across all 9 special cells (bottom middle reels + left/right side columns).

Unlike the old version this does NOT monkeypatch draw_board. It runs the REAL sim
pipeline with the special-cell content cranked (same cranks as make_all_features_book)
so ONE ordinary bonus spin naturally lands lots of features, then slices the single
richest spin out. The result therefore plays exactly like a real spin.

    ../../env/Scripts/python.exe make_combo_book.py

Output: web-sdk/apps/white-room/src/stories/data/combo_features_book.ts
Then restore the real library: ../../env/Scripts/python.exe make_storybook_books.py
"""

from __future__ import annotations

import copy
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
OUT = os.path.abspath(
    os.path.join(HERE, "..", "..", "..", "web-sdk", "apps", "white-room", "src", "stories", "data")
)

MODE = "bonus3"
NUM = {MODE: 12000}

_DROP = {
    "updateFreeSpin",
    "setTotalWin",
    "freeSpinTrigger",
    "freeSpinRetrigger",
    "bonusLevel",
    "freeSpinEnd",
    "createBonusSnapshot",
    "updateGlobalMult",
}

REQUIRED = {"unlockedSlots", "wildReel", "stretchReel", "cloneSymbol", "splitSymbols"}


def crank(config: GameConfig):
    """Same cranks as the all-features showcase: heavily favour features on the
    bottom middle reels AND the left/right side columns so ONE natural spin lands
    a rich mix. Stretch stays a bottom-reel feature."""
    slot = dict(config.unlocked_slot_config or {})
    slot["enabled"] = True
    slot["bottom_reels"] = [1, 2, 3]
    slot["side_rows"] = 3
    slot["content_weights"] = {
        "premium": 6, "wild": 20, "stretch": 24, "split": 22, "clone": 22,
    }
    slot["content_weights_side"] = {
        "premium": 6, "wild": 12, "split": 26, "clone": 26,
    }
    config.unlocked_slot_config = slot

    # wild-mode stretch was REMOVED from the design (a STRETCH card must never
    # manufacture a wild column) — no wild_chance crank, stretch stays normal


def spin_bounds(events):
    idx = [i for i, e in enumerate(events) if e["type"] == "reveal"]
    return [(idx[k], idx[k + 1] if k + 1 < len(idx) else len(events)) for k in range(len(idx))]


def count_type(spin, t):
    return sum(1 for e in spin if e["type"] == t)


def stretch_modes(spin):
    modes = []
    for e in spin:
        if e["type"] == "stretchReel":
            modes += [r.get("mode") for r in e.get("reels", [])]
    return modes


def score_spin(spin):
	"""Prefer the richest natural composition: many clones + splits, at least one
	wild reel, a (normal) stretch, resolving into a win."""
	modes = stretch_modes(spin)
	clones = count_type(spin, "cloneSymbol")
	splits = count_type(spin, "splitSymbols")
	wild_reels = sum(len(e.get("reels", [])) for e in spin if e["type"] == "wildReel")
	win = 0
	for e in spin:
		if e["type"] == "winInfo":
			win = e.get("totalWin", 0)
	return (
		int(clones >= 2) + int(splits >= 2) + int(wild_reels >= 1) + int("normal" in modes),
		clones + splits + wild_reels,
		int(win > 0),
		-abs(min(win, 200000) - 40000),
	)


def slice_spin(book, start, end):
    spin = [copy.deepcopy(e) for e in book["events"][start:end]]
    total = 0
    for e in spin:
        if e.get("type") == "winInfo":
            total = e.get("totalWin", total)
    body = [e for e in spin if e.get("type") not in _DROP]
    level_ev = {"type": "bonusLevel", "level": 3, "name": "FEATURE STORM", "startHaunted": []}
    out = [level_ev, *body, {"type": "setTotalWin", "amount": total}, {"type": "finalWin", "amount": total}]
    for i, e in enumerate(out):
        e["index"] = i
    return {"id": book["id"], "payoutMultiplier": total, "events": out}


def main():
    config = GameConfig()
    crank(config)
    gamestate = GameState(config)
    create_books(gamestate, config, dict(NUM), 500, 1, False, False)

    with open(os.path.join(BOOKS_DIR, f"books_{MODE}.json"), encoding="utf-8") as f:
        books = json.load(f)

    best, best_score = None, None
    for book in books:
        if book["payoutMultiplier"] / 100 >= 30000:  # skip wincap marathons
            continue
        for start, end in spin_bounds(book["events"]):
            spin = book["events"][start:end]
            types = {e["type"] for e in spin}
            if not REQUIRED.issubset(types) or "winInfo" not in types:
                continue
            score = score_spin(spin)
            if best_score is None or score > best_score:
                best_score = score
                best = slice_spin(book, start, end)

    if best is None:
        print("NO combo spin found - raise NUM or crank weights harder")
        sys.exit(1)

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "combo_features_book.ts")
    with open(path, "w", encoding="utf-8") as f:
        f.write(
            "// GENERATED by math-sdk/games/0_2_the_white_room/make_combo_book.py\n"
            "// ONE NATURAL bonus spin picked for the richest feature mix: clones + splits\n"
            "// (across bottom AND side cells) + wild reel(s) + normal & wild stretch,\n"
            "// resolving into a real win. Plays through the live Game.\n"
            "import type { BookEvent } from '../../game/typesBookEvent';\n\n"
            "type ShowcaseBook = { id: number; payoutMultiplier: number; events: BookEvent[] };\n\n"
            f"export const comboFeaturesBook: ShowcaseBook =\n\t{json.dumps(best, indent=1)} as ShowcaseBook;\n\n"
            "export default comboFeaturesBook;\n"
        )

    summary = {
        "out": path,
        "id": best["id"],
        "payoutMultiplier": best["payoutMultiplier"],
        "score": best_score,
        "clones": count_type(best["events"], "cloneSymbol"),
        "splits": count_type(best["events"], "splitSymbols"),
        "stretchModes": stretch_modes(best["events"]),
        "wildReelReels": [len(e.get("reels", [])) for e in best["events"] if e["type"] == "wildReel"],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
