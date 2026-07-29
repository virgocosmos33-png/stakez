"""Regenerate the base + bonus library books for the White Room Storybook.

Sim-only (no optimization / analysis / format checks): produces uncompressed
    library/books/books_{base,bonus1,bonus2,bonus3}.json
with the CURRENT math (Wild Reel + Stretch / Split / Clone special-cell
features), which make_base_books.py then samples into the Storybook fixtures.

    ../../env/Scripts/python.exe make_storybook_books.py        # full sample
    ../../env/Scripts/python.exe make_storybook_books.py smoke  # tiny smoke run
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books

SMOKE = len(sys.argv) > 1 and sys.argv[1] == "smoke"

NUM_SIMS = (
    {"base": 60, "bonus1": 30, "bonus2": 30, "bonus3": 30}
    if SMOKE
    else {"base": 6000, "bonus1": 1000, "bonus2": 1000, "bonus3": 1000}
)

if __name__ == "__main__":
    config = GameConfig()
    gamestate = GameState(config)
    threads = 1 if SMOKE else 4
    create_books(gamestate, config, dict(NUM_SIMS), 1000, threads, False, False)
    print("DONE storybook book gen:", dict(NUM_SIMS))
