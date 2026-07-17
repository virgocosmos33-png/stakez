import random

from game_executables import GameExecutables
from game_events import mirror_burst_event, bonus_level_event
from src.calculations.statistics import get_random_outcome
from src.events.events import reveal_event


class GameStateOverride(GameExecutables):
    """xMirror placement, per-level haunted-cell lifetime/stacking, and 3-level bonus handling."""

    def reset_book(self):
        super().reset_book()
        # {(reel, row): {"apparitions": n, "ttl": reveals-left or None (sticky)}}
        self.haunted_cells = {}
        self.mirror_info = []
        self.fs_level = 1

    def assign_special_sym_function(self):
        self.special_symbol_functions = {}

    def current_level_rules(self) -> dict:
        return self.config.bonus_levels[self.fs_level]

    def update_freespin(self):
        super().update_freespin()
        self.age_haunted_cells()

    def age_haunted_cells(self):
        """Lifetime tick at the start of every free spin; expired cells vanish
        from the coming reveal. Sticky cells (lifetime None) never age."""
        for cell in list(self.haunted_cells.keys()):
            ttl = self.haunted_cells[cell]["ttl"]
            if ttl is None:
                continue
            if ttl <= 1:
                del self.haunted_cells[cell]
            else:
                self.haunted_cells[cell]["ttl"] = ttl - 1

    def draw_board(self, emit_event=True, trigger_symbol="scatter"):
        """Draw normally, re-apply surviving haunted cells, then roll the xMirror feature."""
        super().draw_board(emit_event=False, trigger_symbol=trigger_symbol)
        self.apply_haunted_persistence()
        self.apply_mirrors(emit_event)

    def apply_haunted_persistence(self):
        """Free spins: symbols landing on surviving haunted cells inherit the apparition count."""
        if self.gametype != self.config.freegame_type or not self.haunted_cells:
            return
        for (reel, row), data in self.haunted_cells.items():
            sym = self.board[reel][row]
            if sym.name in self.config.special_symbols["scatter"]:
                continue
            sym.assign_attribute({"multiplier": data["apparitions"]})

    def apply_mirrors(self, emit_event=True):
        """Roll for Haunted Mirrors.

        If triggered: the reveal shows HM symbols on the board, a mirrorBurst event
        describes each mirror reflecting a weighted 1-4 of its orthogonal neighbors
        into apparitions (stored on the engine's `multiplier` attribute, which the
        ways calculation counts as extra symbols), and each mirror resolves into its
        highest-paying neighbor for the final evaluated board.
        """
        self.mirror_info = []
        cfg = self.config.mirror_config
        win_criteria = self.get_current_betmode_distributions().get_win_criteria()

        in_freegame = self.gametype == self.config.freegame_type
        level = self.current_level_rules() if in_freegame else None
        mirror_chance = level["mirror_chance"] if in_freegame else cfg["probability"].get(self.gametype, 0.0)
        split_weights = level["split_count_weights"] if in_freegame else cfg["split_count_weights"]
        stacking = in_freegame and level["stacking"]
        lifetime = level["lifetime"] if in_freegame else None

        # wincap sims: bias the search (mirrors on every spin, max split count),
        # otherwise a 30,000x round would be near-unfindable at the lower levels
        forced = bool(self.get_current_distribution_conditions().get("force_mirrors", False))
        triggered = forced or random.random() < mirror_chance
        # forced zero-win sims must stay winless: mirrors only ever add ways
        if win_criteria == 0:
            triggered = False

        candidates = []
        if triggered:
            for reel in cfg["allowed_reels"]:
                for row in range(self.config.num_rows[reel]):
                    sym = self.board[reel][row]
                    if sym.name in self.config.special_symbols["scatter"]:
                        continue
                    if sym.name in self.config.special_symbols["wild"]:
                        continue
                    # a mirror never lands ON a surviving haunted cell (it may
                    # still reflect into one - that is how stacking happens)
                    if (reel, row) in self.haunted_cells:
                        continue
                    candidates.append((reel, row))
            triggered = len(candidates) > 0

        if not triggered:
            if emit_event:
                reveal_event(self)
            return

        num_mirrors = max(cfg["mirror_count_weights"]) if forced else get_random_outcome(cfg["mirror_count_weights"])
        num_mirrors = min(num_mirrors, len(candidates))
        random.shuffle(candidates)
        mirror_cells = []
        for cell in candidates:
            if len(mirror_cells) == num_mirrors:
                break
            # mirrors never touch each other (a mirror cannot reflect a mirror)
            if all(cell not in self.get_neighbors(*placed, diagonal=True) for placed in mirror_cells):
                mirror_cells.append(cell)

        # Reveal shows the mirrors as landed.
        for reel, row in mirror_cells:
            self.board[reel][row] = self.create_symbol("HM")
        self.get_special_symbols_on_board()
        if emit_event:
            reveal_event(self)

        # Burst: reflect a weighted 1-6 block of the surrounding cells (full
        # 8-neighborhood), then resolve each mirror into its best neighbor.
        # Mirrors excite each other: every extra mirror on the spin widens all
        # bursts by one - a triple-mirror drop tends toward full 6-cell blocks,
        # which is the game's natural (~1 in 10M) path to the wincap.
        for reel, row in mirror_cells:
            eligible = []
            best_name, best_pay = None, -1.0

            def reflect_value(position):
                sym = self.board[position[0]][position[1]]
                if sym.name in self.config.special_symbols["wild"]:
                    return float("inf")
                return self.config.paytable.get((5, sym.name), 0.0)

            for n_reel, n_row in self.get_neighbors(reel, row, diagonal=True):
                sym = self.board[n_reel][n_row]
                if sym.name in self.config.special_symbols["scatter"] or sym.name == "HM":
                    continue
                pay = reflect_value((n_reel, n_row))
                if pay > best_pay:
                    best_name, best_pay = sym.name, pay
                eligible.append((n_reel, n_row))

            if forced:
                split_count = max(split_weights)
                # wincap search: reflect the most valuable cells, not random ones
                eligible.sort(key=reflect_value, reverse=True)
                chosen = eligible[:split_count]
            else:
                split_count = min(get_random_outcome(split_weights) + num_mirrors - 1, max(split_weights))
                chosen = random.sample(eligible, min(split_count, len(eligible)))

            reflected = []
            for n_reel, n_row in chosen:
                sym = self.board[n_reel][n_row]
                # wincap searches roll maximum apparitions - level rules unchanged
                apparitions = (
                    max(cfg["apparition_weights"]) if forced else get_random_outcome(cfg["apparition_weights"])
                )
                if sym.check_attribute("multiplier"):
                    if stacking:
                        # re-hit: new apparitions ADD on top (no cap)
                        apparitions += sym.get_attribute("multiplier")
                    else:
                        apparitions = max(apparitions, sym.get_attribute("multiplier"))
                sym.assign_attribute({"multiplier": apparitions})
                reflected.append({"reel": n_reel, "row": n_row, "apparitions": apparitions})
                if in_freegame:
                    # re-hits refresh the lifetime: the cell lives this spin + (lifetime - 1) more
                    self.haunted_cells[(n_reel, n_row)] = {"apparitions": apparitions, "ttl": lifetime}

            if best_name is None:
                best_name = "L5"  # all neighbors were scatters: show something harmless
            self.board[reel][row] = self.create_symbol(best_name)
            self.mirror_info.append({"reel": reel, "row": row, "reflected": reflected, "becomes": best_name})

        self.get_special_symbols_on_board()
        if emit_event:
            mirror_burst_event(self)

    def update_freespin_amount(self, scatter_key: str = "scatter"):
        """Scatter count picks the bonus level."""
        if self.gametype == self.config.basegame_type:
            scatter_count = min(self.count_special_symbols(scatter_key), 5)
            self.fs_level = self.config.scatter_to_level[max(scatter_count, 3)]
        super().update_freespin_amount(scatter_key)
        if self.gametype == self.config.basegame_type:
            self.haunted_cells = {}
            bonus_level_event(self)

    def check_repeat(self):
        super().check_repeat()
