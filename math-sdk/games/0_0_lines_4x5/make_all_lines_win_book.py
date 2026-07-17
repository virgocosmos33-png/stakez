"""Generate a showcase book where all 50 paylines win, using the real win-evaluation engine.

Board: reels 1-4 are full wilds (W), reel 5 is full H1.
Every payline therefore reads W-W-W-W-H1 and pays as a 5-of-a-kind H1.
The resulting book is exported as storybook data for the web-sdk lines app.
"""

import json
import os

from gamestate import GameState
from game_config import GameConfig
from src.wins.win_manager import WinManager
from src.events.events import reveal_event

OUT_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..", "..", "..",
        "web-sdk", "apps", "lines", "src", "stories", "data", "all_lines_books.ts",
    )
)


def forced_draw_board(gs, emit_event=True, trigger_symbol="scatter"):
    """Replacement for draw_board: deterministic all-lines-win board."""
    config = gs.config
    gs.refresh_special_syms()
    gs.reelstrip_id = "BR0"
    gs.reelstrip = config.reels["BR0"]

    board = []
    for reel in range(config.num_reels):
        name = "W" if reel < config.num_reels - 1 else "H1"
        board.append([gs.create_symbol(name) for _ in range(config.num_rows[reel])])
    gs.board = board
    gs.get_special_symbols_on_board()

    gs.reel_positions = [0] * config.num_reels
    gs.padding_position = [0] * config.num_reels
    gs.anticipation = [0] * config.num_reels
    gs.top_symbols = [gs.create_symbol("L1") for _ in range(config.num_reels)]
    gs.bottom_symbols = [gs.create_symbol("L2") for _ in range(config.num_reels)]

    if emit_event:
        reveal_event(gs)


if __name__ == "__main__":
    config = GameConfig()
    gamestate = GameState(config)

    # Minimal simulation context, mirroring state.run_sims setup
    mode_max_win = next(bm._wincap for bm in config.bet_modes if bm._name == "base")
    gamestate.win_manager = WinManager(config.basegame_type, config.freegame_type, mode_max_win)
    gamestate.library = {}
    gamestate.recorded_events = {}
    gamestate.betmode = "base"
    gamestate.criteria = "basegame"

    gamestate.draw_board = lambda emit_event=True, trigger_symbol="scatter": forced_draw_board(
        gamestate, emit_event, trigger_symbol
    )

    gamestate.run_spin(0, 0)
    book = gamestate.library[1]

    win_info_events = [ev for ev in book["events"] if ev["type"] == "winInfo"]
    num_line_wins = sum(len(ev["wins"]) for ev in win_info_events)
    print("payoutMultiplier:", book["payoutMultiplier"])
    print("winInfo events:", len(win_info_events), "| total line wins:", num_line_wins)
    assert num_line_wins == len(config.paylines), f"expected {len(config.paylines)} line wins, got {num_line_wins}"

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("export default ")
        json.dump([book], f, indent=1)
        f.write(";\n")
    print(f"Wrote all-lines-win book -> {OUT_PATH}")
