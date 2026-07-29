"""Extract curated REAL books that showcase the UNLOCKED SLOTS board expansion.

Generates small bonus samples (one per level), then slices a single free-spin
that unlocks the slots and resolves into a win - sliced clean so the Storybook
action finishes immediately. Writes:
  web-sdk/apps/white-room/src/stories/data/unlocked_slot_books.ts

Level 1 -> bottom slots only, level 2 -> +right column, level 3 -> +left column
(the full 7-wide board). Each pick prefers a spin that shows BOTH a premium and
a wild in the slots and pays across the expanded board.
"""

from __future__ import annotations

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
LEVEL_MODE = {1: "bonus1", 2: "bonus2", 3: "bonus3"}
NUM = {"bonus1": 400, "bonus2": 400, "bonus3": 400}

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


def elevate_slots(config: GameConfig):
    cfg = dict(config.unlocked_slot_config or {})
    cfg["enabled"] = True
    # bias toward premium+wild so a clean showcase is easy to sample. NEVER
    # "empty": an unlocked cell is guaranteed content every spin, and the
    # showcase books must show exactly that.
    cfg["content_weights"] = {"premium": 55, "wild": 45}
    config.unlocked_slot_config = cfg


def slice_spin(book, slot_index):
    """Extract the single spin around events[slot_index] as a clean self-
    resolving book (reveal -> ... -> unlockedSlots -> winInfo -> totals)."""
    events = book["events"]
    start = slot_index
    while start > 0 and events[start]["type"] != "reveal":
        start -= 1
    end = slot_index + 1
    while end < len(events) and events[end]["type"] != "reveal":
        end += 1
    spin = [dict(e) for e in events[start:end]]
    spin[0] = dict(spin[0], gameType="basegame")
    total = 0
    for e in spin:
        if e.get("type") == "winInfo":
            total = e.get("totalWin", 0)
    spin = [e for e in spin if e.get("type") not in _DROP]
    spin += [
        {"type": "setTotalWin", "amount": total},
        {"type": "finalWin", "amount": total},
    ]
    for i, e in enumerate(spin):
        e["index"] = i
    return {"id": book["id"], "payoutMultiplier": total, "events": spin}


def spin_stats(events, slot_index):
    """Look at the spin owning events[slot_index]: gather the slot event and the
    first following winInfo (win total + best kind)."""
    slot_ev = events[slot_index]
    end = slot_index + 1
    while end < len(events) and events[end]["type"] != "reveal":
        end += 1
    win_total, best_kind = 0, 0
    for e in events[slot_index:end]:
        if e.get("type") == "winInfo":
            win_total = max(win_total, e.get("totalWin", 0))
            for w in e.get("wins", []):
                best_kind = max(best_kind, w.get("kind", 0))
    has_premium = any(
        c["name"] != "W"
        for c in slot_ev.get("bottom", [])
    ) or any(
        c["name"] != "W"
        for s in slot_ev.get("sides", [])
        for c in s["cells"]
    )
    has_wild = any(c["name"] == "W" for c in slot_ev.get("bottom", [])) or any(
        c["name"] == "W" for s in slot_ev.get("sides", []) for c in s["cells"]
    )
    return win_total, best_kind, has_premium, has_wild


def pick_for_level(level: int):
    mode = LEVEL_MODE[level]
    with open(os.path.join(BOOKS_DIR, f"books_{mode}.json"), encoding="utf-8") as f:
        books = json.load(f)
    best = None
    best_score = (-1, -1, -1)
    for book in books:
        if book["payoutMultiplier"] / 100 >= 30000:
            continue
        events = book["events"]
        for i, e in enumerate(events):
            if e.get("type") != "unlockedSlots":
                continue
            win_total, best_kind, has_premium, has_wild = spin_stats(events, i)
            if win_total <= 0:
                continue
            # want to SEE both a premium and a wild land, a wide connection, and
            # a MODERATE win (~150x) so the slot mechanic - not a minutes-long
            # max-win celebration - is what the showcase actually reads.
            target = 15000  # cents (~150x)
            score = (
                int(has_premium and has_wild),
                best_kind,
                -abs(min(win_total, 80000) - target),
            )
            if score > best_score:
                best_score = score
                best = slice_spin(book, i)
    return best, best_score


def main():
    config = GameConfig()
    elevate_slots(config)
    gamestate = GameState(config)
    create_books(gamestate, config, dict(NUM), 80, 1, False, False)

    order = [1, 2, 3]
    names = {1: "unlockedSlotsLevel1Book", 2: "unlockedSlotsLevel2Book", 3: "unlockedSlotsLevel3Book"}
    exports, summary = {}, {}
    for level in order:
        book, score = pick_for_level(level)
        if book is None:
            print(f"WARN no winning unlocked-slots spin found for level {level}")
            continue
        exports[level] = book
        summary[level] = {"id": book["id"], "payoutMultiplier": book["payoutMultiplier"], "score": score}

    os.makedirs(OUT, exist_ok=True)
    ts_path = os.path.join(OUT, "unlocked_slot_books.ts")
    with open(ts_path, "w", encoding="utf-8") as f:
        f.write(
            "// GENERATED by math-sdk/games/0_2_the_white_room/make_slot_books.py\n"
            "// Real UNLOCKED SLOTS books pulled from the build - each plays through\n"
            "// the live Game so the slot-drop + 6/7-wide resolution is exact.\n"
            "import type { BookEvent } from '../../game/typesBookEvent';\n\n"
            "type ShowcaseBook = { id: number; payoutMultiplier: number; events: BookEvent[] };\n\n"
        )
        for level in order:
            if level not in exports:
                continue
            f.write(
                f"export const {names[level]}: ShowcaseBook =\n"
                f"\t{json.dumps(exports[level], indent=1)} as ShowcaseBook;\n\n"
            )
        exported_names = [names[level] for level in order if level in exports]
        f.write(f"export default [{', '.join(exported_names)}];\n")

    print(json.dumps({"out": ts_path, "picks": summary}, indent=2))


if __name__ == "__main__":
    main()
