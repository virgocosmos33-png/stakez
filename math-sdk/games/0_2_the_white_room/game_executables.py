from game_calculations import GameCalculations
from src.calculations.ways import Ways


class GameExecutables(GameCalculations):
    """Ways evaluation (Cell Seal expand-as-wild aware)."""

    def evaluate_ways_board(self):
        """Populate win-data, record wins, transmit events."""
        # Game-local ways: wild-on-reel-0 can start pays (SDK seeds only reel-0 names).
        self.win_data = self.get_ways_data()
        if self.win_data["totalWin"] > 0:
            Ways.record_ways_wins(self)
            self.win_manager.update_spinwin(self.win_data["totalWin"])
        Ways.emit_wayswin_events(self)
