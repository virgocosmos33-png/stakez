"""TOMBSTONE REBORN - spin flow.

Base / bought single spins are one enhanced reveal: draw, run the special
system, evaluate ways with the accumulated WIN multiplier, settle.

The WIN multiplier starts at 1x. It is sticky across SUPER / big-bonus
spins and resets every SMALL bonus spin (and every base / single-spin book).

BONUS ROUNDS (natural 3/4+ scatter triggers, or bought as freespins /
superspins): fs_spins spins on the scatter-free FR0 strip. The SMALL tier
keeps the special bar awake every spin; the BIG tier opens the grave lane
permanently on top. No retriggers - but ~1 in 100 small rounds drops a 4th
scatter mid-round and UPGRADES to the big tier: the lane opens for the rest
of the round and the spin count is topped back up to a full fresh round.
"""

import random

from game_override import GameStateOverride
from game_events import bonus_upgrade_event


class GameState(GameStateOverride):
    """Spin logic for all bet modes."""

    def run_spin(self, sim: int, simulation_seed=None) -> None:
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            self.draw_board(emit_event=True)

            self.apply_features()
            self.evaluate_ways_board()

            self.win_manager.update_gametype_wins(self.gametype)

            if self.check_fs_condition() and self.check_freespin_entry():
                count = self.count_special_symbols("scatter")
                self.fs_tier = "big" if count >= 4 else "small"
                # force-record the trigger OURSELVES with kind clamped to 4:
                # the optimizer fences bind books through force_search
                # ({"kind": 3/4, "symbol": "scatter"}), and a 5-scatter round
                # must land in the same freegame_big fence as a 4-scatter one.
                self.record(
                    {"kind": min(count, 4), "symbol": "scatter", "gametype": self.gametype}
                )
                self.update_freespin_amount()
                self.run_freespin()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self) -> None:
        self.reset_fs_spin()
        self.win_multiplier = 1
        conditions = self.get_current_distribution_conditions()
        while self.fs < self.tot_fs:
            self.update_freespin()
            # SMALL bonus: reset the WIN stack every spin. SUPER / upgraded
            # rounds keep it sticky. Check BEFORE the upgrade so the upgrade
            # spin starts fresh, then carries forward.
            if self.fs_tier == "small" and not self.fs_upgraded:
                self.win_multiplier = 1

            # the 4th-scatter UPGRADE: rolled per spin on un-upgraded small
            # rounds; wincap books force it onto spin 1 (the cap is only
            # reachable through the upgrade)
            upgrade_now = (
                self.fs_tier == "small"
                and not self.fs_upgraded
                and (
                    (bool(conditions.get("fs_force_upgrade")) and self.fs == 1)
                    or random.random() < self.config.fs_upgrade_per_spin
                )
            )
            if upgrade_now:
                # takes effect THIS spin: the lane is open under the scatter
                # that just dropped, and the round is topped back up
                self.fs_upgraded = True
                self._pending_upgrade = True
                self.tot_fs = self.fs + self.config.fs_spins

            self.draw_board(emit_event=True)

            if upgrade_now:
                self._pending_upgrade = False
                bonus_upgrade_event(self, self._upgrade_scatter, self.fs, self.tot_fs)

            self.apply_features()
            self.evaluate_ways_board()
            self.win_manager.update_gametype_wins(self.gametype)

        self.end_freespin()
