"""Generate Madam's Eye showcase books for the frontend (Storybook).

Book 1: base spin where the eye drops with a mirror burst and converts the
        split cells into wilds for a real ways win.
Book 2: THE OTHER SIDE (level 2) bonus where the eye converts split cells that
        include carried-over (persistent) hauntings.
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
        "web-sdk", "apps", "ways", "src", "stories", "data", "eye_books.ts",
    )
)


def get_events(book, ev_type):
    return [ev for ev in book["events"] if ev["type"] == ev_type]


def is_base_eye_showcase(book):
    """Base-game book: the eye converts >=2 split cells and the spin pays."""
    eyes = get_events(book, "madamsEye")
    if not eyes or len(eyes[0]["converted"]) < 2:
        return False
    if get_events(book, "freeSpinTrigger"):
        return False
    payout = book["payoutMultiplier"] / 100
    return 2 <= payout <= 2000


def is_bonus_eye_showcase(book):
    """Level-2 bonus book: an eye fires on a spin with carried-over hauntings."""
    levels = get_events(book, "bonusLevel")
    if not levels or levels[0]["level"] != 2:
        return False
    eyes = get_events(book, "madamsEye")
    if not eyes:
        return False
    # at least one eye spin must convert 2+ cells (a proper wild board moment)
    if not any(len(ev["converted"]) >= 2 for ev in eyes):
        return False
    payout = book["payoutMultiplier"] / 100
    return 100 <= payout <= 8000


def find_book(gamestate, betmode, criteria, predicate, max_sims=5000):
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
    # make mirrors and the eye frequent so the search is quick; feature rules
    # themselves are untouched
    config.mirror_config["probability"] = {config.basegame_type: 1.0}
    for rules in config.bonus_levels.values():
        rules["mirror_chance"] = 0.75
    config.eye_config["probability"] = {config.basegame_type: 1.0, config.freegame_type: 0.6}
    gamestate = GameState(config)

    mode_max_win = next(bm._wincap for bm in config.bet_modes if bm._name == "base")
    gamestate.win_manager = WinManager(config.basegame_type, config.freegame_type, mode_max_win)
    gamestate.library = {}
    gamestate.recorded_events = {}

    base_eye_book = find_book(gamestate, "base", "basegame", is_base_eye_showcase)
    print("base eye showcase payout:", base_eye_book["payoutMultiplier"] / 100)

    bonus_eye_book = find_book(gamestate, "bonus2", "freegame", is_bonus_eye_showcase)
    print("bonus2 eye showcase payout:", bonus_eye_book["payoutMultiplier"] / 100)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("export default ")
        json.dump([base_eye_book, bonus_eye_book], f, indent=1)
        f.write(";\n")
    print(f"Wrote showcase books -> {OUT_PATH}")
