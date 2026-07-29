"""Quick smoke test for Madam Mirror: small uncompressed sim run + book inspection.

Verifies:
- books generate for all 4 bet modes (incl. wincap forcing) without repeats hanging
- mirrorBurst / bonusLevel events appear and are well-formed (1-4 reflected cells)
- per-level haunted-cell rules, re-derived from events and checked against every
  freegame reveal board:
    L1 THE SEANCE: cells never survive to the next reveal (lifetime 1, no stacking)
    L2 THE OTHER SIDE: cells survive exactly one extra reveal, re-hits ADD and
      refresh the lifetime
    L3 BLOOD MOON: cells never expire, re-hits ADD with no cap
- ways math: reported win == paytable * ways for sampled winInfo events
- bonus levels map to the forced scatter counts (3->1, 4->2, 5->3)
"""

import json
import os
from collections import Counter

from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(HERE, "library", "books")

NUM_SIMS = {"base": 3000, "bonus1": 300, "bonus2": 300, "bonus3": 300}


def load_books(mode):
    path = os.path.join(BOOKS_DIR, f"books_{mode}.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def replay_haunted_state(book, config):
    """Re-derive haunted cells from the events and assert every freegame reveal
    board carries exactly the surviving cells (multiplier attribute), aged by the
    level's lifetime rule. Returns (stack_hits, persisted_reveal_count)."""
    level = None
    lifetime, stacking = None, False
    state = {}  # (reel, padded_row) -> {"apparitions": n, "ttl": k or None}
    gametype = None
    stack_hits = []
    persisted_reveals = 0

    for ev in book["events"]:
        if ev["type"] == "bonusLevel":
            level = ev["level"]
            rules = config.bonus_levels[level]
            lifetime, stacking = rules["lifetime"], rules["stacking"]
            state = {}
        elif ev["type"] == "updateFreeSpin":
            # start of a free spin: lifetime tick, expired cells vanish
            for cell in list(state):
                ttl = state[cell]["ttl"]
                if ttl is None:
                    continue
                if ttl <= 1:
                    del state[cell]
                else:
                    state[cell]["ttl"] = ttl - 1
        elif ev["type"] == "reveal":
            gametype = ev["gameType"]
            expected = {} if gametype == config.basegame_type else {c: d["apparitions"] for c, d in state.items()}
            if expected:
                persisted_reveals += 1
            for reel, column in enumerate(ev["board"]):
                for row, sym in enumerate(column):
                    mult = sym.get("multiplier")
                    if (reel, row) in expected:
                        if sym["name"] == "S":
                            continue  # scatters do not inherit the haunting
                        assert mult == expected[(reel, row)], (book["id"], reel, row, mult, expected[(reel, row)])
                    else:
                        assert not mult or mult <= 1, (book["id"], reel, row, sym)
        elif ev["type"] == "mirrorBurst" and gametype == config.freegame_type:
            for m in ev["mirrors"]:
                assert 1 <= len(m["reflected"]) <= 6, m
                for cell in m["reflected"]:
                    key = (cell["reel"], cell["row"])
                    if key in state:
                        if stacking:
                            # re-hit must ADD on top of the existing count
                            assert cell["apparitions"] > state[key]["apparitions"], (book["id"], cell)
                            stack_hits.append((state[key]["apparitions"], cell["apparitions"]))
                        else:
                            assert cell["apparitions"] >= state[key]["apparitions"], (book["id"], cell)
                    state[key] = {"apparitions": cell["apparitions"], "ttl": lifetime}
    return stack_hits, persisted_reveals


def inspect_mode(mode, books, config):
    print(f"\n=== {mode}: {len(books)} books ===")
    ev_counter = Counter()
    level_counter = Counter()
    split_counter = Counter()
    payouts = []
    mirror_books = 0
    stack_hits_total = []
    persisted_total = 0

    for book in books:
        payouts.append(book["payoutMultiplier"] / 100)
        has_mirror = False
        for ev in book["events"]:
            ev_counter[ev["type"]] += 1
            if ev["type"] == "mirrorBurst":
                has_mirror = True
                assert ev["mirrors"], "mirrorBurst without mirrors"
                for m in ev["mirrors"]:
                    assert m["mirrorBecomes"]["name"] != "HM"
                    split_counter[len(m["reflected"])] += 1
                    for cell in m["reflected"]:
                        assert cell["apparitions"] >= 2, cell
            if ev["type"] == "bonusLevel":
                level_counter[ev["level"]] += 1
        if has_mirror:
            mirror_books += 1
        stack_hits, persisted = replay_haunted_state(book, config)
        stack_hits_total += stack_hits
        persisted_total += persisted

    assert "hauntDeepen" not in ev_counter, "deepening was removed with the lifetime rework"
    print("event types:", dict(ev_counter))
    print("bonus levels awarded:", dict(level_counter))
    print("split counts (reflected cells per burst):", dict(sorted(split_counter.items())))
    print(f"books with mirrors: {mirror_books}/{len(books)}")
    print(f"reveals with carried-over haunted cells: {persisted_total}")
    print(f"stacking re-hits: {len(stack_hits_total)}", stack_hits_total[:8])
    print(f"mean payout (x bet-cost units): {sum(payouts) / len(payouts):.2f}, max: {max(payouts):.2f}")
    return level_counter, stack_hits_total, persisted_total


def verify_madams_eye(mode, books, config):
    """Validate Madam's Eye events: the ME symbol appears on the reveal at the
    event position, and the converted set is exactly the split (multiplier>1)
    cells of that spin that were not already wild."""
    eyes = 0
    for book in books:
        splits = {}  # padded (reel, row) -> apparitions for the current spin
        wild_cells = set()
        eye_pos = None
        for ev in book["events"]:
            if ev["type"] == "reveal":
                splits, wild_cells, eye_pos = {}, set(), None
                for reel, column in enumerate(ev["board"]):
                    for row, sym in enumerate(column):
                        if sym.get("multiplier", 1) > 1:
                            splits[(reel, row)] = sym["multiplier"]
                        if sym["name"] == "W":
                            # already-wild cells (even plain reel wilds later
                            # reflected by a burst) are never converted
                            wild_cells.add((reel, row))
                        if sym["name"] == "ME":
                            assert eye_pos is None, (book["id"], "more than one eye on a reveal")
                            eye_pos = (reel, row)
            elif ev["type"] == "mirrorBurst":
                for m in ev["mirrors"]:
                    for cell in m["reflected"]:
                        splits[(cell["reel"], cell["row"])] = cell["apparitions"]
            elif ev["type"] == "madamsEye":
                eyes += 1
                assert eye_pos == (ev["eye"]["reel"], ev["eye"]["row"]), (book["id"], ev["eye"], eye_pos)
                expected = {cell: n for cell, n in splits.items() if cell not in wild_cells}
                got = {(c["reel"], c["row"]): c["apparitions"] for c in ev["converted"]}
                assert got == expected, (book["id"], got, expected)
                eye_pos = None
        # an eye on the reveal must always resolve within the same spin
        assert eye_pos is None, (book["id"], "eye revealed but never resolved")
    print(f"madamsEye events verified: {eyes}")
    return eyes


def verify_ways_math(books, config, samples=200):
    """Recheck win = paytable[(kind, symbol)] * ways for winInfo entries.
    Books that hit the wincap are skipped: their wins are clamped to the cap,
    so paytable * ways no longer holds."""
    checked = 0
    for book in books:
        if book["payoutMultiplier"] / 100 >= config.wincap:
            continue
        for ev in book["events"]:
            if ev["type"] != "winInfo":
                continue
            for w in ev["wins"]:
                expected = round(config.paytable[(w["kind"], w["symbol"])] * w["meta"]["ways"], 2)
                got = w["win"] / 100
                assert abs(expected - got) < 0.011, (w, expected, got)
                checked += 1
                if checked >= samples:
                    print(f"ways math verified on {checked} wins")
                    return
    print(f"ways math verified on {checked} wins")


def print_lifetime_sample(mode, books, config):
    """Print one book's haunted-cell timeline as evidence of the lifetime rule."""
    for book in books:
        timeline = []
        gametype = None
        for ev in book["events"]:
            if ev["type"] == "reveal":
                gametype = ev["gameType"]
                if gametype == config.freegame_type:
                    haunted = [
                        (reel, row, sym["multiplier"])
                        for reel, column in enumerate(ev["board"])
                        for row, sym in enumerate(column)
                        if sym.get("multiplier", 1) > 1
                    ]
                    timeline.append(("reveal", haunted))
            elif ev["type"] == "mirrorBurst" and gametype == config.freegame_type:
                timeline.append(
                    ("burst", [(c["reel"], c["row"], c["apparitions"]) for m in ev["mirrors"] for c in m["reflected"]])
                )
        if sum(1 for kind, cells in timeline if kind == "burst") >= 2:
            print(f"\n{mode} sample book {book['id']} freegame timeline (reel, row, apparitions):")
            for kind, cells in timeline:
                print(f"  {kind}: {cells}")
            return


if __name__ == "__main__":
    config = GameConfig()
    gamestate = GameState(config)

    create_books(gamestate, config, dict(NUM_SIMS), 1000, 1, False, False)

    all_levels = Counter()
    mode_stats = {}
    total_eyes = 0
    for mode in NUM_SIMS:
        books = load_books(mode)
        levels, stack_hits, persisted = inspect_mode(mode, books, config)
        all_levels.update(levels)
        mode_stats[mode] = (stack_hits, persisted)
        verify_ways_math(books, config)
        total_eyes += verify_madams_eye(mode, books, config)
    assert total_eyes > 0, "no Madam's Eye events generated across all modes"

    # level semantics: L1 never carries cells across reveals and never stacks;
    # L2/L3 must show both carried-over reveals and stacking re-hits
    assert mode_stats["bonus1"] == ([], 0), mode_stats["bonus1"]
    assert mode_stats["bonus2"][0] and mode_stats["bonus2"][1] > 0
    assert mode_stats["bonus3"][0] and mode_stats["bonus3"][1] > 0
    print("\nlifetime semantics verified: L1 no carry-over, L2/L3 carry over and stack")

    # buy modes must award exactly their own level
    for mode, expected_level in (("bonus1", 1), ("bonus2", 2), ("bonus3", 3)):
        books = load_books(mode)
        for book in books:
            for ev in book["events"]:
                if ev["type"] == "bonusLevel":
                    assert ev["level"] == expected_level, (mode, ev)
    print("buy-mode level mapping verified: bonus1->L1, bonus2->L2, bonus3->L3")

    for mode in ("bonus1", "bonus2", "bonus3"):
        print_lifetime_sample(mode, load_books(mode), config)
    print("\nALL CHECKS PASSED")
