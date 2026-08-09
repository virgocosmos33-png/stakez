"""Targeted sim+optimize for bonus_super only (fast tuning loop)."""

from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":
    config = GameConfig()
    gamestate = GameState(config)
    OptimizationSetup(config)

    num_sim_args = {"bonus_super": int(1e5)}
    create_books(gamestate, config, num_sim_args, 2000, 6, True, False)
    generate_configs(gamestate)
    OptimizationExecution().run_all_modes(config, ["bonus_super"], 16)
    generate_configs(gamestate)
    print("SUPER TUNE COMPLETE")
