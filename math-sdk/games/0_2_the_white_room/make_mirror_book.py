"""Generate showcase books for the Madam Mirror frontend (Storybook).

Book 1: base spin with a mirrorBurst whose apparitions boost a real ways win.
Book 2: THE SEANCE (level 1) bonus with mirrors (hauntings last one spin).
Book 3: THE OTHER SIDE (level 2) bonus with a stacking re-hit.
Book 4: BLOOD MOON (level 3) bonus with sticky, stacking haunted cells.
Exported as storybook data for the web-sdk ways app.
"""

import json
import os

from gamestate import GameState
from game_config import GameConfig
from src.wins.win_manager import WinManager


OUT_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..", "..", "..",
        "web-sdk", "apps", "ways", "src", "stories", "data", "mirror_books.ts",
    )
)


def get_events(book, ev_type):
    return [ev for ev in book["events"] if ev["type"] == ev_type]


def is_mirror_showcase(book):
    """Base-game book: a burst reflecting >=2 cells and a win that uses them."""
    bursts = get_events(book, "mirrorBurst")
    if not bursts or len(bursts[0]["mirrors"][0]["reflected"]) < 2:
        return False
    if get_events(book, "freeSpinTrigger"):
        return False
    for ev in get_events(book, "winInfo"):
        for w in ev["wins"]:
            if w["meta"]["ways"] >= 4 and w["win"] > 0:
                return True
    return False


def has_stack_hit(book):
    """A reflected cell above 4 apparitions can only come from a stacking re-hit."""
    for ev in get_events(book, "mirrorBurst"):
        for m in ev["mirrors"]:
            for cell in m["reflected"]:
                if cell["apparitions"] > 4:
                    return True
    return False


def make_bonus_predicate(level, min_payout, max_payout, needs_stack):
    """Bonus book of the given level with mirrors and a watchable payout."""

    def predicate(book):
        levels = get_events(book, "bonusLevel")
        if not levels or levels[0]["level"] != level:
            return False
        if not get_events(book, "mirrorBurst"):
            return False
        if needs_stack and not has_stack_hit(book):
            return False
        payout = book["payoutMultiplier"] / 100
        return min_payout <= payout <= max_payout

    return predicate


def find_book(gamestate, betmode, criteria, predicate, max_sims=2000):
    gamestate.betmode = betmode
    gamestate.criteria = criteria
    for sim in range(max_sims):
        gamestate.run_spin(sim, sim)
        book = gamestate.library[sim + 1]
        if predicate(book):
            return book
    raise AssertionError(f"no showcase book found for {betmode}/{criteria} in {max_sims} sims")


if __name__ == "__main__":
    config = GameConfig()
    # make mirrors frequent so the search is quick; rules are otherwise untouched
    config.mirror_config["probability"] = {config.basegame_type: 1.0}
    for rules in config.bonus_levels.values():
        rules["mirror_chance"] = 0.75
    gamestate = GameState(config)

    mode_max_win = next(bm._wincap for bm in config.bet_modes if bm._name == "base")
    gamestate.win_manager = WinManager(config.basegame_type, config.freegame_type, mode_max_win)
    gamestate.library = {}
    gamestate.recorded_events = {}

    mirror_book = find_book(gamestate, "base", "basegame", is_mirror_showcase)
    print("mirror showcase payout:", mirror_book["payoutMultiplier"] / 100)

    seance_book = find_book(
        gamestate, "bonus1", "freegame", make_bonus_predicate(1, 50, 2000, needs_stack=False)
    )
    print("seance (L1) showcase payout:", seance_book["payoutMultiplier"] / 100)

    other_side_book = find_book(
        gamestate, "bonus2", "freegame", make_bonus_predicate(2, 100, 5000, needs_stack=True)
    )
    print("other side (L2) showcase payout:", other_side_book["payoutMultiplier"] / 100)

    blood_moon_book = find_book(
        gamestate, "bonus3", "freegame", make_bonus_predicate(3, 500, 20000, needs_stack=True)
    )
    print("blood moon (L3) showcase payout:", blood_moon_book["payoutMultiplier"] / 100)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("export default ")
        json.dump([mirror_book, seance_book, other_side_book, blood_moon_book], f, indent=1)
        f.write(";\n")
    print(f"Wrote showcase books -> {OUT_PATH}")
