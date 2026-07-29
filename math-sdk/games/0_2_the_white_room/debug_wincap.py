"""Measure the win distribution of wincap-condition sims (no repeat filtering).

Temporarily strips win_criteria from the wincap distribution so every attempt
is recorded, then reports percentiles - tells us how reachable 30,000x is.
"""

import statistics
import sys

from gamestate import GameState
from game_config import GameConfig
from src.wins.win_manager import WinManager

N = 400

if __name__ == "__main__":
    config = GameConfig()
    gamestate = GameState(config)

    mode = sys.argv[1] if len(sys.argv) > 1 else "base"
    for bm in config.bet_modes:
        if bm.get_name() == mode:
            config.wincap = bm.get_wincap()
            for d in bm.get_distributions():
                if d.get_criteria() == "wincap":
                    d._win_criteria = None  # record every attempt

    gamestate.win_manager = WinManager(config.basegame_type, config.freegame_type, 30000)
    gamestate.library = {}
    gamestate.recorded_events = {}
    gamestate.betmode = mode
    gamestate.criteria = "wincap"

    wins = []
    for sim in range(N):
        gamestate.run_spin(sim, sim)
        wins.append(gamestate.library[sim + 1]["payoutMultiplier"] / 100)

    wins.sort()
    print(f"attempts: {N}")
    print(f"min/median/mean/max: {wins[0]:.0f} / {wins[N//2]:.0f} / {statistics.mean(wins):.0f} / {wins[-1]:.0f}")
    for pct in (50, 75, 90, 95, 99):
        print(f"p{pct}: {wins[int(N * pct / 100) - 1]:.0f}")
    over = sum(1 for w in wins if w >= 30000)
    print(f">=30000x: {over}/{N}")
