"""Quick LOCAL math build for The White Room.

The source repo shipped without generated books (library/ is gitignored), so
this regenerates a small-but-valid build purely for local frontend testing
against the mock RGS: real books + lookup tables + index.json for every mode,
at reduced sim counts so it finishes in minutes instead of hours. NOT for
production/compliance - use run.py for that.
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

    # small counts - enough distinct outcomes for the optimizer to weight and
    # for the mock RGS to sample varied spins, without the multi-hour full run.
    n = int(2e4)
    num_sim_args = {
        "base": n,
        "ante": n,
        "bonus1": n,
        "bonus2": n,
        "bonus3": n,
    }

    run_conditions = {
        "run_sims": True,
        "run_optimization": True,
        "run_analysis": False,
        "run_format_checks": False,
    }
    target_modes = list(num_sim_args.keys())

    config = GameConfig()
    gamestate = GameState(config)
    if run_conditions["run_optimization"] or run_conditions["run_analysis"]:
        optimization_setup_class = OptimizationSetup(config)

    if run_conditions["run_sims"]:
        create_books(
            gamestate,
            config,
            num_sim_args,
            batching_size,
            num_threads,
            compression,
            profiling,
        )

    generate_configs(gamestate)

    if run_conditions["run_optimization"]:
        OptimizationExecution().run_all_modes(config, target_modes, rust_threads)
        generate_configs(gamestate)

    if run_conditions["run_analysis"]:
        create_stat_sheet(gamestate, custom_keys=[{"symbol": "scatter"}])

    if run_conditions["run_format_checks"]:
        execute_all_tests(config)

    print("LOCAL BUILD COMPLETE")
