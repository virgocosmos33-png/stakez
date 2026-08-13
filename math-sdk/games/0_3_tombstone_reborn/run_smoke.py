"""Tiny-sim smoke test for the bonus-round feature (NO optimization).

Runs a few thousand sims per changed mode to shake out crashes and validate
event shapes / trigger rates before committing to the multi-hour full run.
Overwrites library/books files - fine, the full run regenerates them.
"""

import json
import zstandard as zstd

from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books

if __name__ == "__main__":
    num_sim_args = {
        "base": 20000,
        "freespins": 1500,
        "superspins": 800,
    }

    config = GameConfig()
    gamestate = GameState(config)
    create_books(gamestate, config, num_sim_args, 500, 1, True, False)

    # ---- inspect the produced books --------------------------------------
    for mode in num_sim_args:
        path = f"library/books_compressed/books_{mode}.jsonl.zst"
        try:
            raw = zstd.ZstdDecompressor().decompress(
                open(path, "rb").read(), max_output_size=2_000_000_000
            )
        except FileNotFoundError:
            path = f"library/books/books_{mode}.jsonl.zst"
            raw = zstd.ZstdDecompressor().decompress(
                open(path, "rb").read(), max_output_size=2_000_000_000
            )
        books = [json.loads(line) for line in raw.decode().splitlines() if line]
        n = len(books)
        trig = sum(
            1 for b in books if any(e["type"] == "freeSpinTrigger" for e in b["events"])
        )
        upg = sum(
            1 for b in books if any(e["type"] == "bonusUpgrade" for e in b["events"])
        )
        pays = [b["payoutMultiplier"] for b in books]
        print(
            f"{mode}: {n} books, fsTrigger {trig}, upgrades {upg}, "
            f"avg pay {sum(pays)/n/100:.2f}x, max {max(pays)/100:.0f}x"
        )
