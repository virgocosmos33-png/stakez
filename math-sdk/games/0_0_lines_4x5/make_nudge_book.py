"""Generate a showcase book featuring the xNudge wild feature.

Forces the nudge probability to 100% and simulates spins until one produces a
wild-nudge round that also pays a boosted (multiplied) line win. The book is
exported as storybook data for the web-sdk lines app.
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
        "web-sdk", "apps", "lines", "src", "stories", "data", "nudge_books.ts",
    )
)


def is_showcase_book(book: dict) -> bool:
    """Book must contain a multi-step nudge and a win boosted by the wild multiplier."""
    nudge_events = [ev for ev in book["events"] if ev["type"] == "wildNudge"]
    if not nudge_events or nudge_events[0]["nudges"] < 2:
        return False
    for ev in book["events"]:
        if ev["type"] == "winInfo":
            if any(w["meta"]["multiplier"] > 1 for w in ev["wins"]):
                return True
    return False


if __name__ == "__main__":
    config = GameConfig()
    config.nudge_config["probability"] = {config.basegame_type: 1.0, config.freegame_type: 1.0}
    gamestate = GameState(config)

    # Minimal simulation context, mirroring state.run_sims setup
    mode_max_win = next(bm._wincap for bm in config.bet_modes if bm._name == "base")
    gamestate.win_manager = WinManager(config.basegame_type, config.freegame_type, mode_max_win)
    gamestate.library = {}
    gamestate.recorded_events = {}
    gamestate.betmode = "base"
    gamestate.criteria = "basegame"

    showcase_book = None
    for sim in range(500):
        gamestate.run_spin(sim, sim)
        book = gamestate.library[sim + 1]
        if is_showcase_book(book):
            showcase_book = book
            break

    assert showcase_book is not None, "no nudge showcase book found in 500 sims"

    nudge_ev = [ev for ev in showcase_book["events"] if ev["type"] == "wildNudge"][0]
    print("payoutMultiplier:", showcase_book["payoutMultiplier"])
    print("nudge event:", {k: v for k, v in nudge_ev.items() if k != "finalReel"})

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("export default ")
        json.dump([showcase_book], f, indent=1)
        f.write(";\n")
    print(f"Wrote nudge showcase book -> {OUT_PATH}")
