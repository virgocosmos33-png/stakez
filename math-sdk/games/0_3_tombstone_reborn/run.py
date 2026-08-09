"""Main (production) results generation for TOMBSTONE REBORN (main game only)."""

from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from utils.game_analytics.run_analysis import create_stat_sheet
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":

    num_threads = 6
    rust_threads = 24
    batching_size = 2000
    compression = True
    profiling = False

    num_sim_args = {
        "base": int(1e6),
        "bonus_small": int(5e5),
        "bonus_super": int(5e5),
    }

    run_conditions = {
        "run_sims": True,
        "run_optimization": True,
        "run_analysis": True,
        "run_format_checks": True,
    }
    target_modes = list(num_sim_args.keys())

    config = GameConfig()
    gamestate = GameState(config)
    OptimizationSetup(config)

    if run_conditions["run_sims"]:
        create_books(gamestate, config, num_sim_args, batching_size, num_threads, compression, profiling)

    generate_configs(gamestate)

    if run_conditions["run_optimization"]:
        OptimizationExecution().run_all_modes(config, target_modes, rust_threads)
        generate_configs(gamestate)

    if run_conditions["run_analysis"]:
        create_stat_sheet(gamestate, custom_keys=[])

    if run_conditions["run_format_checks"]:
        execute_all_tests(config)
