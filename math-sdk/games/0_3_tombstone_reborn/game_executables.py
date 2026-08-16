"""Ways evaluation for TOMBSTONE REBORN.

Two multiplier layers combine here:
  * WAYS multipliers - split / gunsmoke stamp a per-cell `multiplier` that the
    engine's default "symbol" strategy folds straight into the ways COUNT.
  * WIN multiplier - bounty / MARK set `self.win_multiplier`, which multiplies
    the whole spin's win AFTER the ways total is computed.
"""

from game_calculations import GameCalculations
from src.calculations.ways import Ways


class GameExecutables(GameCalculations):
    """Ways evaluation with a post-hoc global WIN multiplier."""

    def evaluate_ways_board(self):
        """Populate win-data (ways count already includes split ways), apply the
        WIN multiplier, record wins and transmit the win events."""
        data = Ways.get_ways_data(self.config, self.board)

        wm = max(1, int(getattr(self, "win_multiplier", 0) or 0))
        if wm > 1 and data["totalWin"] > 0:
            for w in data["wins"]:
                w["win"] = round(w["win"] * wm, 2)
                w["meta"]["globalMult"] = wm
                w["meta"]["winWithoutMult"] = w["meta"].get("winWithoutMult", w["win"])
            data["totalWin"] = round(data["totalWin"] * wm, 2)

        self.win_data = data
        if self.win_data["totalWin"] > 0:
            Ways.record_ways_wins(self)
            self.win_manager.update_spinwin(self.win_data["totalWin"])
        Ways.emit_wayswin_events(self)
