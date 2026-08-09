"""Quick LOCAL math build for TOMBSTONE REBORN (main game only).

Real books + lookup tables + index.json for the base mode, at reduced sim
counts so it finishes fast. NOT for production - use run.py for that.

    ../../env/Scripts/python.exe run_local.py
"""

from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":
    num_threads = 6
    rust_threads = 16
    batching_size = 2000
    compression = True
    profiling = False

    num_sim_args = {
        "base": int(1e5),
        "bonus_small": int(5e4),
        "bonus_super": int(5e4),
    }

    run_conditions = {"run_sims": True, "run_optimization": True}
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

    print("LOCAL BUILD COMPLETE")
