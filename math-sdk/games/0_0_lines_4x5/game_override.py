import random

from game_executables import GameExecutables
from game_events import wild_nudge_event
from src.calculations.statistics import get_random_outcome
from src.events.events import reveal_event


class GameStateOverride(GameExecutables):
    """
    This class is is used to override or extend universal state.py functions.
    e.g: A specific game may have custom book properties to reset
    """

    def reset_book(self):
        super().reset_book()
        self.nudge_info = None

    def assign_special_sym_function(self):
        self.special_symbol_functions = {
            "W": [self.assign_mult_property],
        }

    def assign_mult_property(self, symbol) -> dict:
        """Assign multiplier value to Wild symbol in freegame."""
        multiplier_value = 1
        if self.gametype == self.config.freegame_type:
            multiplier_value = get_random_outcome(
                self.get_current_distribution_conditions()["mult_values"][self.gametype]
            )
        symbol.assign_attribute({"multiplier": multiplier_value})

    def draw_board(self, emit_event=True, trigger_symbol="scatter"):
        """Draw the board as usual, then roll for the xNudge wild feature."""
        super().draw_board(emit_event=False, trigger_symbol=trigger_symbol)
        self.apply_wild_nudge(emit_event)

    def apply_wild_nudge(self, emit_event=True):
        """Roll for a nudging wild stack.

        If triggered: the reveal shows the stack landing `nudges` rows too high
        (its top wilds hidden above the window), a wildNudge event describes the
        downward nudges, and the final evaluated board holds a full reel of wilds
        each carrying a (1 + nudges) multiplier.
        """
        cfg = self.config.nudge_config
        probability = cfg["probability"].get(self.gametype, 0.0)
        win_criteria = self.get_current_betmode_distributions().get_win_criteria()

        triggered = win_criteria != 0 and random.random() < probability
        if triggered:
            scatter_reels = {pos["reel"] for pos in self.special_syms_on_board.get("scatter", [])}
            candidate_reels = [r for r in cfg["allowed_reels"] if r not in scatter_reels]
            triggered = len(candidate_reels) > 0

        if not triggered:
            if emit_event:
                reveal_event(self)
            return

        reel = random.choice(candidate_reels)
        rows = self.config.num_rows[reel]
        nudges = min(get_random_outcome(cfg["nudge_weights"]), rows - 1)
        multiplier = 1 + nudges

        # Misaligned reveal: bottom (rows - nudges) wilds of the stack in view at
        # the top of the window, remaining wilds hidden above (top padding = W).
        original_top_symbol = self.top_symbols[reel]
        for row in range(rows - nudges):
            self.board[reel][row] = self.create_symbol("W")
        self.top_symbols[reel] = self.create_symbol("W")
        self.get_special_symbols_on_board()
        if emit_event:
            reveal_event(self)

        # Final board used for win evaluation: full wild stack with the multiplier.
        for row in range(rows):
            wild = self.create_symbol("W")
            wild.assign_attribute({"multiplier": multiplier})
            self.board[reel][row] = wild
        self.top_symbols[reel] = original_top_symbol
        self.get_special_symbols_on_board()

        self.nudge_info = {"reel": reel, "nudges": nudges, "multiplier": multiplier}
        if emit_event:
            wild_nudge_event(self)

    def check_repeat(self):
        super().check_repeat()
        if self.repeat is False:
            win_criteria = self.get_current_betmode_distributions().get_win_criteria()
            if win_criteria is not None and self.final_win != win_criteria:
                self.repeat = True
                return
            if win_criteria is None and self.final_win == 0:
                self.repeat = True
                return
