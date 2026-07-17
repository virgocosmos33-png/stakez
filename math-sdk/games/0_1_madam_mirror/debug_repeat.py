"""Reproduce a stuck wincap sim: print per-attempt final wins for sim 263."""

from gamestate import GameState
from game_config import GameConfig
from src.wins.win_manager import WinManager


class Instrumented(GameState):
    def check_repeat(self):
        super().check_repeat()
        if self.repeat_count <= 50 or self.repeat_count % 500 == 0:
            print(
                f"attempt {self.repeat_count}: final={self.final_win} "
                f"triggered_fg={self.triggered_freegame} repeat={self.repeat}"
            )
        if self.repeat_count >= 2000:
            raise SystemExit("still repeating after 2000 attempts")


if __name__ == "__main__":
    config = GameConfig()
    gamestate = Instrumented(config)
    gamestate.win_manager = WinManager(config.basegame_type, config.freegame_type, 30000)
    gamestate.library = {}
    gamestate.recorded_events = {}
    gamestate.betmode = "base"
    gamestate.criteria = "wincap"
    gamestate.run_spin(263)
    print("sim 263 done:", gamestate.library[264]["payoutMultiplier"] / 100)
