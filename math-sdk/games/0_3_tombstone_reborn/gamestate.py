"""TOMBSTONE REBORN - spin flow.

Every mode (base, small bonus, super bonus) is a SINGLE enhanced spin: draw,
run the special system, evaluate ways with the accumulated WIN multiplier,
settle. There is no free-spin loop.
"""

from game_override import GameStateOverride


class GameState(GameStateOverride):
    """Single-spin game logic for all bet modes."""

    def run_spin(self, sim: int, simulation_seed=None) -> None:
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            self.draw_board(emit_event=True)

            self.apply_features()
            self.evaluate_ways_board()

            self.win_manager.update_gametype_wins(self.gametype)
            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self) -> None:
        # No free spins - single enhanced spins only. Required by the engine ABC.
        pass
