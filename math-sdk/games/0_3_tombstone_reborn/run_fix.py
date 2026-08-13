"""Targeted rebuild after the first bonus-round run:

- re-SIM base only (the scatter force records now clamp kind to 4, which the
  freegame_big fence's force_search needs)
- re-OPTIMIZE base (fences now bind through force_search), bonus_super
  (10k+ bands re-starved for the scatter-diluted books) and superspins
  (smaller cap slice for the CVaR ceiling)

bonus_small and freespins already pass every 3-star check and keep their
books and lookup tables untouched. Verify afterwards with check_rating.py.
"""

from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":
    num_threads = 6
    rust_threads = 24
    batching_size = 2000

    num_sim_args = {"base": int(1e6)}
    target_modes = ["base", "bonus_super", "superspins"]

    config = GameConfig()
    gamestate = GameState(config)
    OptimizationSetup(config)

    create_books(gamestate, config, num_sim_args, batching_size, num_threads, True, False)
    generate_configs(gamestate)
    OptimizationExecution().run_all_modes(config, target_modes, rust_threads)
    generate_configs(gamestate)
    execute_all_tests(config)
