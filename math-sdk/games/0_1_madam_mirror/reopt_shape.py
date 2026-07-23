"""Re-run ONLY the optimization phase for modes whose band distribution needed
re-shaping (books/sims stay valid - the optimizer just re-weights them).

Used after tuning the scaling in game_optimization.py:
    feature1/2/3: 500-1000x cliff (same shape base mode had)
    bonus3:       1000-2000x inversion (rarer than 2000-5000x)
"""

from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from src.write_data.write_configs import generate_configs

MODES = ["feature1", "feature2", "feature3"]
RUST_THREADS = 24

if __name__ == "__main__":
    config = GameConfig()
    gamestate = GameState(config)
    OptimizationSetup(config)
    OptimizationExecution().run_all_modes(config, MODES, RUST_THREADS)
    generate_configs(gamestate)
    print("reopt done for:", MODES)
