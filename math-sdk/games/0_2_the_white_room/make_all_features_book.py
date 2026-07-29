"""Build ONE self-contained Storybook spin in which EVERY feature fires together:
Unlocked Slots + Wild Reel + Stretch + Clone + Split, resolving into a win.

Features can only drop into the bottom special cells (one outcome per cell), so a
normal spin can show at most a few. For this showcase ONLY we widen the bottom
cells to all 5 reels and crank the content weights so a single level-3 bonus spin
reliably rolls a wild + stretch + clone + split, then we slice that spin out into

    web-sdk/apps/white-room/src/stories/data/all_features_book.ts

This does NOT touch the real game config - the cranks live entirely in this script.

    ../../env/Scripts/python.exe make_all_features_book.py
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

MODE = "bonus3"  # forces bonus level 3 (all groups unlocked)
NUM = {MODE: 12000}

# events the frontend keeps out of a sliced single-spin showcase
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
RENDERED_BOTTOM = {1, 2, 3}  # bottom cells the frontend actually draws a card for


def crank(config: GameConfig):
    """Crank the special-cell content so ONE natural level-3 bonus spin reliably
    rolls features across BOTH the bottom middle reels AND the left/right side
    columns (features are cells everywhere). Stretch stays a bottom-reel feature."""
    slot = dict(config.unlocked_slot_config or {})
    slot["enabled"] = True
    slot["bottom_reels"] = [1, 2, 3]  # the 3 rendered bottom cells
    slot["side_rows"] = 3
    # bottom cells heavily favour the features; a little premium so clone/split
    # have targets to convert / split.
    slot["content_weights"] = {
        "premium": 6,
        "wild": 20,
        "stretch": 24,
        "split": 22,
        "clone": 22,
    }
    # side cells (right/left) heavily favour CLONE / SPLIT so the showcase shows
    # features living in the side columns too.
    slot["content_weights_side"] = {
        "premium": 6,
        "wild": 12,
        "split": 26,
        "clone": 26,
    }
    config.unlocked_slot_config = slot

    # showcase: give stretched reels big per-symbol x-ways so the numbers pop
    stretch = dict(getattr(config, "stretch_config", {}) or {})
    stretch["ways_weights"] = {3: 3, 4: 5, 5: 6, 6: 7, 8: 8, 10: 10}
    stretch["ways_cap"] = 500
    config.stretch_config = stretch

    # showcase: force SPLIT to go high (> 8) so a plain "Nx" number is shown
    split = dict(getattr(config, "split_config", {}) or {})
    split["split_weights"] = {8: 3, 9: 6, 10: 12}
    config.split_config = split


def spin_bounds(events):
    idx = [i for i, e in enumerate(events) if e["type"] == "reveal"]
    return [(idx[k], idx[k + 1] if k + 1 < len(idx) else len(events)) for k in range(len(idx))]


def feature_reel(spin, ev_type):
    reels = set()
    for e in spin:
        if e["type"] == ev_type:
            if ev_type in ("wildReel", "stretchReel"):
                reels |= {r["reel"] for r in e.get("reels", [])}
            else:
                cell = e.get("cell", {})
                reels.add(cell.get("reel") if cell.get("reel") is not None else cell.get("side"))
    return reels


def _drawn_count(spin, ev_type):
	"""How many of this feature's cards land on a RENDERED cell. Stretch is a
	bottom middle-reel feature (reels 1/2/3); clone/split render wherever they
	land now - a bottom cell OR a side column slot - so every event counts."""
	if ev_type == "stretchReel":
		return len({r["reel"] for e in spin if e["type"] == "stretchReel" for r in e.get("reels", [])} & RENDERED_BOTTOM)
	return sum(1 for e in spin if e["type"] == ev_type)


def score_spin(spin):
	"""Prefer a spin that shows ALL four new-feature cards, then MULTIPLE of each on
	the drawn bottom cells (reels 1/2/3) plus a wild reel, resolving into a win."""
	stretch_drawn = _drawn_count(spin, "stretchReel")
	clone_drawn = _drawn_count(spin, "cloneSymbol")
	split_drawn = _drawn_count(spin, "splitSymbols")
	wild_r = feature_reel(spin, "wildReel")
	variety = (
		int(stretch_drawn > 0)
		+ int(clone_drawn > 0)
		+ int(split_drawn > 0)
		+ int(bool(wild_r))
	)
	# reward up to 2 of each so the showcase reads as "multiple of every symbol"
	multiples = (
		min(stretch_drawn, 2)
		+ min(clone_drawn, 2)
		+ min(split_drawn, 2)
		+ min(len(wild_r), 2)
	)
	win = 0
	for e in spin:
		if e["type"] == "winInfo":
			win = e.get("totalWin", 0)
	moderate = -abs(min(win, 200000) - 40000)
	return (variety, multiples, int(win > 0), moderate)


def slice_spin(book, start, end):
    spin = [copy.deepcopy(e) for e in book["events"][start:end]]
    total = 0
    for e in spin:
        if e.get("type") == "winInfo":
            total = e.get("totalWin", total)
    body = [e for e in spin if e.get("type") not in _DROP]
    # open all groups up front (level 3) so the cells read unlocked immediately
    level_ev = {"type": "bonusLevel", "level": 3, "name": "ALL FEATURES", "startHaunted": []}
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
        print("NO all-features spin found - raise NUM or crank weights harder")
        sys.exit(1)

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "all_features_book.ts")
    with open(path, "w", encoding="utf-8") as f:
        f.write(
            "// GENERATED by math-sdk/games/0_2_the_white_room/make_all_features_book.py\n"
            "// ONE bonus spin where every feature fires: Unlocked Slots + Wild Reel +\n"
            "// Stretch + Clone + Split, resolving into a win. Plays through the live Game.\n"
            "import type { BookEvent } from '../../game/typesBookEvent';\n\n"
            "type ShowcaseBook = { id: number; payoutMultiplier: number; events: BookEvent[] };\n\n"
            f"export const allFeaturesBook: ShowcaseBook =\n\t{json.dumps(best, indent=1)} as ShowcaseBook;\n\n"
            "export default allFeaturesBook;\n"
        )

    feats = {t: sorted(feature_reel(best["events"], t), key=str) for t in ("wildReel", "stretchReel", "cloneSymbol", "splitSymbols")}
    print(json.dumps({"out": path, "id": best["id"], "payoutMultiplier": best["payoutMultiplier"], "score": best_score, "featureReels": feats}, indent=2))


if __name__ == "__main__":
    main()
