"""Regenerate library books for the Tombstone Reborn Storybook / frontend.

Sim-only (no optimization): produces uncompressed library/books/books_base.json
for sampling into Storybook fixtures and eyeballing the reveal / winInfo event
stream.

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
    {"base": 60, "bonus_small": 60, "bonus_super": 60}
    if SMOKE
    else {"base": 6000, "bonus_small": 4000, "bonus_super": 4000}
)

if __name__ == "__main__":
    config = GameConfig()
    gamestate = GameState(config)
    threads = 1 if SMOKE else 4
    create_books(gamestate, config, dict(NUM_SIMS), 1000, threads, False, False)

    configs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library", "configs")
    for mode in NUM_SIMS:
        sidecar = os.path.join(configs_dir, f"books_{mode}.verification.json")
        if os.path.exists(sidecar):
            os.remove(sidecar)

    print("DONE storybook book gen:", dict(NUM_SIMS))
