"""Main file for generating results for Madam Mirror."""

from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from utils.game_analytics.run_analysis import create_stat_sheet
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":

    # bonus books are event-heavy: small batches keep the per-process JSON
    # buffer modest (large batches OOM during zstd compression). Peak RAM in
    # the book-gen phase ~= num_threads x batching_size x avg_book_size, so
    # this scales with FREE memory, not core count.
    # Tuned for an i9-14900HX / 32GB box with ~17GB free (Storybook + IDE up):
    # 6 x 2000 buffers stay inside that headroom. Close other apps to push
    # num_threads to 8. rust_threads is the CPU-bound, memory-light optimizer
    # phase, so it uses most of the 32 logical cores.
    num_threads = 6
    rust_threads = 24
    batching_size = 2000
    compression = True
    profiling = False

    # Stake math verification wants 100k-1M sims per mode for outcome diversity;
    # we max out the range so every mode has a deep pool of distinct outcomes
    # RE-OPTIMIZE FEATURE MODES ONLY: their books are valid, but the first
    # optimization pass used two hr="x" fences and landed 0.865/0.915/0.940
    # instead of 0.965. Books/LUTs for base/ante/bonus1-3 stay untouched.
    num_sim_args = {
        "feature1": int(2.5e5),
        "feature2": int(2.5e5),
        "feature3": int(2.5e5),
    }

    run_conditions = {
        "run_sims": False,  # books already exist from the full run
        "run_optimization": True,
        "run_analysis": True,
        "run_format_checks": True,
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
        custom_keys = [{"symbol": "scatter"}]
        create_stat_sheet(gamestate, custom_keys=custom_keys)

    if run_conditions["run_format_checks"]:
        execute_all_tests(config)
