"""Re-run ONLY the optimization for base + bonus_super over the existing books.

Used for the Stake 3-star retune (smaller wincap fences + tail-starving
scaling in game_optimization.py): the simulated books are unchanged, only the
lookup-table weights move, so re-simulating would be wasted hours.
bonus_small already passes every 3-star check and is left untouched.

Verify afterwards with check_rating.py.
"""

from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from utils.rgs_verification import execute_all_tests
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":
    rust_threads = 24
    target_modes = ["base", "bonus_super"]

    config = GameConfig()
    gamestate = GameState(config)
    OptimizationSetup(config)

    generate_configs(gamestate)
    OptimizationExecution().run_all_modes(config, target_modes, rust_threads)
    generate_configs(gamestate)
    execute_all_tests(config)
