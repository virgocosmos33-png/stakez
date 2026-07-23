import random

from game_executables import GameExecutables
from game_events import mirror_burst_event, bonus_level_event, madams_eye_event
from src.calculations.statistics import get_random_outcome
from src.events.events import reveal_event


class GameStateOverride(GameExecutables):
    """xMirror placement, per-level haunted-cell lifetime/stacking, and 3-level bonus handling."""

    def reset_book(self):
        super().reset_book()
        # {(reel, row): {"apparitions": n, "ttl": reveals-left or None (sticky)}}
        self.haunted_cells = {}
        self.mirror_info = []
        self.eye_info = None
        self.fs_level = 1
        # feature spins: set when the guaranteed mirror count could not be
        # placed (adjacency/candidate shortage) - the book is redrawn
        self.mirror_shortfall = False

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
        """Draw normally, re-apply surviving haunted cells, roll the xMirror
        feature, then resolve the Madam's Eye conversion (if the eye dropped)."""
        super().draw_board(emit_event=False, trigger_symbol=trigger_symbol)
        self.force_ante_scatter()
        self.apply_haunted_persistence()
        self.apply_mirrors(emit_event)
        self.resolve_madams_eye(emit_event)

    def force_ante_scatter(self):
        """ANTE mode: every base spin is guaranteed a scatter on the forced
        reel (condition "force_scatter_reel"). The scatter replaces a random
        plain symbol in the window, before mirrors/eye are rolled, so the
        rest of the feature pipeline treats it like a natural scatter."""
        reel = self.get_current_distribution_conditions().get("force_scatter_reel")
        if reel is None or self.gametype != self.config.basegame_type:
            return
        scatters = self.config.special_symbols["scatter"]
        if any(self.board[reel][row].name in scatters for row in range(self.config.num_rows[reel])):
            return
        plain_rows = [
            row
            for row in range(self.config.num_rows[reel])
            if self.board[reel][row].name not in self.config.special_symbols["wild"]
            and self.board[reel][row].name not in self.config.special_symbols["mirror"]
            and self.board[reel][row].name not in self.config.special_symbols["eye"]
        ]
        row = random.choice(plain_rows if plain_rows else list(range(self.config.num_rows[reel])))
        self.board[reel][row] = self.create_symbol(scatters[0])
        self.get_special_symbols_on_board()

    def apply_haunted_persistence(self):
        """Free spins: symbols landing on surviving haunted cells inherit the
        apparition count plus the cell's remaining lifetime (ttl, -1 = sticky)
        so the frontend can show how long each split cell will persist."""
        if self.gametype != self.config.freegame_type or not self.haunted_cells:
            return
        for (reel, row), data in self.haunted_cells.items():
            sym = self.board[reel][row]
            if sym.name in self.config.special_symbols["scatter"]:
                continue
            sym.assign_attribute(
                {
                    "multiplier": data["apparitions"],
                    "ttl": data["ttl"] if data["ttl"] is not None else -1,
                }
            )

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
        # otherwise a wincap (22,222x) round would be near-unfindable at the lower levels
        forced = bool(self.get_current_distribution_conditions().get("force_mirrors", False))
        # feature spins: the base spin is guaranteed N+ mirrors
        forced_min = (
            int(self.get_current_distribution_conditions().get("force_mirror_min", 0))
            if self.gametype == self.config.basegame_type
            else 0
        )
        triggered = forced or forced_min > 0 or random.random() < mirror_chance
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
            if forced_min > 0:
                self.mirror_shortfall = True  # no candidates: redraw the book
            self.place_madams_eye(has_mirrors=False)
            if emit_event:
                reveal_event(self)
            return

        if forced:
            num_mirrors = max(cfg["mirror_count_weights"])
        elif forced_min > 0:
            # natural count mix, truncated at the guaranteed minimum
            truncated = {k: v for k, v in cfg["mirror_count_weights"].items() if k >= forced_min}
            num_mirrors = get_random_outcome(truncated) if truncated else forced_min
        else:
            num_mirrors = get_random_outcome(cfg["mirror_count_weights"])
        num_mirrors = min(num_mirrors, len(candidates))
        random.shuffle(candidates)
        mirror_cells = []
        for cell in candidates:
            if len(mirror_cells) == num_mirrors:
                break
            # mirrors never touch each other (a mirror cannot reflect a mirror)
            if all(cell not in self.get_neighbors(*placed, diagonal=True) for placed in mirror_cells):
                mirror_cells.append(cell)

        if forced_min > 0 and len(mirror_cells) < forced_min:
            self.mirror_shortfall = True  # could not place the guarantee: redraw

        # Reveal shows the mirrors as landed.
        for reel, row in mirror_cells:
            self.board[reel][row] = self.create_symbol("HM")
        self.place_madams_eye(has_mirrors=True)
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
                # the Madam's Eye is never reflected (it has its own resolution)
                if sym.name in self.config.special_symbols["eye"]:
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
                entry = {"reel": n_reel, "row": n_row, "apparitions": apparitions}
                if in_freegame:
                    # re-hits refresh the lifetime: the cell lives this spin + (lifetime - 1) more
                    self.haunted_cells[(n_reel, n_row)] = {"apparitions": apparitions, "ttl": lifetime}
                    entry["ttl"] = lifetime if lifetime is not None else -1
                    sym.assign_attribute({"ttl": entry["ttl"]})
                reflected.append(entry)

            if best_name is None:
                best_name = "L5"  # all neighbors were scatters: show something harmless
            self.board[reel][row] = self.create_symbol(best_name)
            self.mirror_info.append({"reel": reel, "row": row, "reflected": reflected, "becomes": best_name})

        self.get_special_symbols_on_board()
        if emit_event:
            mirror_burst_event(self)

    def place_madams_eye(self, has_mirrors: bool):
        """Roll for the Madam's Eye BEFORE the reveal so it drops with the board.

        Only spins that will actually have split symbols are eligible: a fresh
        mirror burst is coming this spin, or haunted cells carried over by
        persistence. The eye replaces a plain cell (never a scatter, wild,
        mirror or haunted cell)."""
        self.eye_info = None
        win_criteria = self.get_current_betmode_distributions().get_win_criteria()
        # forced zero-win sims must stay winless: the conversion only adds wins
        if win_criteria == 0:
            return

        has_carried_splits = any(
            sym.check_attribute("multiplier") and sym.get_attribute("multiplier") > 1
            for reel in self.board
            for sym in reel
        )
        if not (has_mirrors or has_carried_splits):
            return
        chance = self.config.eye_config["probability"].get(self.gametype, 0.0)
        if random.random() >= chance:
            return

        candidates = []
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                sym = self.board[reel][row]
                if sym.name in self.config.special_symbols["scatter"]:
                    continue
                if sym.name in self.config.special_symbols["wild"]:
                    continue
                if sym.name in self.config.special_symbols["mirror"]:
                    continue
                if sym.check_attribute("multiplier") and sym.get_attribute("multiplier") > 1:
                    continue
                candidates.append((reel, row))
        if not candidates:
            return

        reel, row = random.choice(candidates)
        self.board[reel][row] = self.create_symbol("ME")
        self.eye_info = {"reel": reel, "row": row}

    def resolve_madams_eye(self, emit_event=True):
        """The Madam's Eye opens once the bursts settle: every split symbol on
        the board (fresh from this spin's burst or carried by persistence)
        turns WILD for this spin, keeping its apparition count; the eye itself
        resolves into a wild too. haunted_cells is untouched - on persistent
        levels the cell reverts to whatever lands on it next spin."""
        if not self.eye_info:
            return

        converted = []
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                sym = self.board[reel][row]
                if sym.name in self.config.special_symbols["wild"]:
                    continue
                if sym.name in self.config.special_symbols["scatter"]:
                    continue
                if sym.name in self.config.special_symbols["eye"]:
                    continue
                if sym.check_attribute("multiplier") and sym.get_attribute("multiplier") > 1:
                    apparitions = sym.get_attribute("multiplier")
                    ttl = sym.ttl
                    wild = self.create_symbol("W")
                    wild.assign_attribute({"multiplier": apparitions})
                    if ttl:
                        wild.assign_attribute({"ttl": ttl})
                    self.board[reel][row] = wild
                    converted.append({"reel": reel, "row": row, "apparitions": apparitions})

        eye_reel, eye_row = self.eye_info["reel"], self.eye_info["row"]
        self.board[eye_reel][eye_row] = self.create_symbol("W")
        self.eye_info["converted"] = converted
        self.get_special_symbols_on_board()
        if emit_event:
            madams_eye_event(self)

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
        # feature spins: the guaranteed mirror count must actually be on the board
        if self.mirror_shortfall:
            self.repeat = True
