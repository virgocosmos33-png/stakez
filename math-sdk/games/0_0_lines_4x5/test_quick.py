"""Quick sanity check: generate a few books and print a sample 4x5 board."""

from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":
    num_sim_args = {"base": int(1e2), "bonus": int(1e2)}

    config = GameConfig()
    gamestate = GameState(config)

    create_books(
        gamestate,
        config,
        num_sim_args,
        batch_size=5000,
        threads=1,
        compress=False,
        profiling=False,
    )
    generate_configs(gamestate)

    print("\nBoard dimensions check:")
    print("num_reels:", config.num_reels)
    print("num_rows:", config.num_rows)
    print("paylines:", len(config.paylines))
