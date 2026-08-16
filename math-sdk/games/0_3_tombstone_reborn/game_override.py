"""TOMBSTONE REBORN - board draw + special-system pipeline.

A spin is a single enhanced reveal. After the board is drawn we:
  1. plant feature symbols onto the board (no left special bar),
  2. if the last-reel lane is open, fill it with a premium+WIN-mult or MARK
     or SUPERSPLIT — never a low,
  3. apply feature effects in a fixed order,
  4. transform every remaining feature symbol into the revolver WILD,
  5. then hand the mutated board to the ways evaluator, which applies the
     stacked WIN multiplier.

Ordering matters: every effect that changes the ways COUNT (gunsmoke wildify,
split, nudge-ways, supersplit) is applied BEFORE the single ways evaluation.
WIN multiplier (bounty / MARK) is last so MARK counts premiums on the
fully-enriched board.
"""

import random

from game_executables import GameExecutables
from src.calculations.statistics import get_random_outcome
from src.events.events import reveal_event
from game_events import (
    board_specials_event,
    tombstone_event,
    gunsmoke_event,
    split_event,
    nudge_ways_event,
    super_split_event,
    bounty_event,
    shooter_event,
    specials_wild_event,
    win_mult_event,
)


KIND_TO_SYM = {
    "split": "SP",
    "gunsmoke": "GS",
    "nudge": "NW",
}

NUDGE_REELS = (1, 2)


class GameStateOverride(GameExecutables):
    """Draw the board and run the whole special system for a single spin."""

    # ------------------------------------------------------------------ setup
    def reset_book(self):
        super().reset_book()
        # WIN multi resets per BASE book. Bonus rounds keep a sticky stack
        # (run_freespin zeros it once at round start).
        if getattr(self, "gametype", None) != getattr(self.config, "freegame_type", "freegame"):
            self.win_multiplier = 0
        self.bar_mode = "off"
        self.boost = "none"
        self.last_unlocked = False
        self.special_bar = []
        self.board_specials = []
        self.last_reel_feature = "none"
        self._pending_bounty_mult = 0
        self._emit_tombstone = False
        self._nudge_drops = []
        self.fs_tier = "small"
        self.fs_upgraded = False
        self._pending_upgrade = False
        self._upgrade_scatter = None

    def assign_special_sym_function(self):
        self.special_symbol_functions = {}

    # ---------------------------------------------------------- pick helpers
    def _boosting(self) -> bool:
        return self.boost == "max"

    def _pick_factor(self, weights: dict):
        if self._boosting():
            return max(weights.keys())
        return get_random_outcome(weights)

    def _present_types(self, candidates) -> dict:
        counts = {}
        for reel in range(len(self.board)):
            for sym in self.board[reel]:
                name = sym.name
                if name in candidates:
                    counts[name] = counts.get(name, 0) + 1
        return counts

    def _cells_of(self, names) -> list:
        cells = []
        for reel in range(len(self.board)):
            for row in range(len(self.board[reel])):
                if self.board[reel][row].name in names:
                    cells.append({"reel": reel, "row": row})
        return cells

    def _add_win_mult(self, amount: int, source: str):
        """Stack onto the round/spin WIN multiplier."""
        added = max(0, int(amount))
        self.win_multiplier = int(getattr(self, "win_multiplier", 0) or 0) + added
        return self.win_multiplier

    def _weighted_sample(self, weights: dict, k: int) -> list:
        picked = []
        pool = dict(weights)
        for _ in range(min(k, len(pool))):
            choice = get_random_outcome(pool)
            picked.append(choice)
            del pool[choice]
        return picked

    # ----------------------------------------------------------- board draw
    def draw_board(self, emit_event=True, trigger_symbol="scatter"):
        conditions = self.get_current_distribution_conditions()
        self.boost = conditions.get("boost", "none")

        if self.gametype == self.config.freegame_type:
            self.bar_mode = conditions.get("fs_bar", "wake")
            self.last_unlocked = bool(conditions.get("fs_last", False)) or self.fs_upgraded
            self.create_board_reelstrips()
            if self._pending_upgrade:
                self._place_upgrade_scatter()
            self._place_board_specials(conditions)
            self._unlock_lane_from_super_scatter()
            if self.last_unlocked:
                self._fill_unlocked_lane()
            if emit_event:
                reveal_event(self)
            board_specials_event(self)
            return

        self.bar_mode = conditions.get("bar_mode", "off")
        self.last_unlocked = bool(conditions.get("last_unlocked", False))
        target = conditions.get("scatters", "none")
        for _ in range(2000):
            self.create_board_reelstrips()
            n = self.count_special_symbols(trigger_symbol)
            if (
                (target == "none" and n < 3)
                or (target == "exactly3" and n == 3)
                or (target == "atleast4" and n >= 4)
            ):
                break
        else:  # pragma: no cover
            self.repeat = True
        if target == "atleast4":
            self._mark_super_scatter()
        self._place_board_specials(conditions)
        self._unlock_lane_from_super_scatter()
        if self.last_unlocked:
            self._fill_unlocked_lane()
        if emit_event:
            reveal_event(self)
        board_specials_event(self)

    def _mark_super_scatter(self):
        """The 4th scatter that opens the big bonus — and this spin's last reel."""
        cells = [
            (reel, row)
            for reel, strip in enumerate(self.board)
            for row, sym in enumerate(strip)
            if sym.name == "S"
        ]
        if not cells:
            return
        reel, row = max(cells, key=lambda pos: pos[0])
        self.board[reel][row] = self.create_symbol("SU")
        self.get_special_symbols_on_board()

    def _place_upgrade_scatter(self):
        reel = random.choice((3, 4))
        row = random.randrange(len(self.board[reel]))
        self.board[reel][row] = self.create_symbol("SU")
        self._upgrade_scatter = {"reel": reel, "row": row}
        self.get_special_symbols_on_board()

    def _place_board_specials(self, conditions):
        """Roll the old 6-slot rates, then plant those cards onto the board."""
        cfg = self.config.special_bar_config
        cells = cfg["cells"]
        weights = cfg["weights"].get(self.bar_mode, cfg["weights"]["off"])
        force_count = int(conditions.get("force_special_count", 0))

        if self._boosting():
            kinds = ["split", "split", "gunsmoke", "split", "nudge", "nudge"]
        else:
            kinds = [get_random_outcome(weights) for _ in range(cells)]
            if force_count > 0:
                non_none = {k: w for k, w in weights.items() if k != "none"} or {"split": 1}
                empties = [i for i, k in enumerate(kinds) if k == "none"]
                random.shuffle(empties)
                need = force_count - (cells - len(empties))
                for i in empties[: max(0, need)]:
                    kinds[i] = get_random_outcome(non_none)

        nudge_kinds = [k for k in kinds if k == "nudge"]
        other_kinds = [k for k in kinds if k != "none" and k != "nudge" and k in KIND_TO_SYM]

        placed = []
        self._nudge_drops = []
        reserved = set()

        available = [r for r in NUDGE_REELS if r < len(self.board)]
        random.shuffle(available)
        for _nk, reel in zip(nudge_kinds, available):
            drop = self._plant_nudge(reel)
            if not drop:
                continue
            self._nudge_drops.append(drop)
            for row in drop["rows"]:
                reserved.add((reel, row))
                placed.append({"reel": reel, "row": row, "kind": "nudge"})

        last = self.config.num_reels - 1
        eligible = []
        for reel in range(last):
            for row in range(len(self.board[reel])):
                if (reel, row) in reserved:
                    continue
                name = self.board[reel][row].name
                if name in ("S", "SU") or name in self.config.feature_symbols:
                    continue
                eligible.append((reel, row, name))
        lows = [c for c in eligible if c[2] in self.config.low_symbols]
        pool = list(lows if len(lows) >= len(other_kinds) else eligible)
        random.shuffle(pool)

        for kind, (reel, row, _) in zip(other_kinds, pool):
            self.board[reel][row] = self.create_symbol(KIND_TO_SYM[kind])
            placed.append({"reel": reel, "row": row, "kind": kind})

        self.board_specials = placed
        self.special_bar = [{"reel": c["reel"], "kind": c["kind"]} for c in placed]

    def _plant_nudge(self, reel):
        """Plant Nudge Ways on reel 1 or 2: one cell, or the whole reel."""
        cfg = self.config.nudge_ways_config
        height = len(self.board[reel])
        free = [
            row for row in range(height)
            if self.board[reel][row].name not in ("S", "SU")
            and self.board[reel][row].name not in self.config.feature_symbols
        ]
        if not free:
            return None

        initial = (
            max(cfg["initial_ways_weights"].keys())
            if self._boosting()
            else get_random_outcome(cfg["initial_ways_weights"])
        )
        place = (
            0
            if self._boosting()
            else get_random_outcome(cfg["place_weights"])
        )

        if place == "full" and len(free) == height:
            rows = list(range(height))
            for row in rows:
                self.board[reel][row] = self.create_symbol("NW")
            return {
                "reel": reel,
                "start_row": 0,
                "rows": rows,
                "full_reel": True,
                "initial_ways": int(initial),
            }

        if place == "full":
            place = max(free)

        start = int(place) if isinstance(place, int) else random.choice(free)
        if start not in free:
            start = min(free, key=lambda r: abs(r - start))
        self.board[reel][start] = self.create_symbol("NW")
        return {
            "reel": reel,
            "start_row": start,
            "rows": [start],
            "full_reel": False,
            "initial_ways": int(initial),
        }

    def _unlock_lane_from_super_scatter(self):
        """SUPER scatter opens the last-reel lane BEFORE reveal so the cell is
        already a premium / MARK / SUPERSPLIT under the lid, never a leftover low."""
        if not self._cells_of({"SU"}):
            return
        if not self.last_unlocked:
            self.last_unlocked = True
            self._emit_tombstone = True
        elif self._pending_upgrade:
            self._emit_tombstone = True

    def _fill_unlocked_lane(self):
        """Open last reel: premium+WIN-mult, MARK, or SUPERSPLIT. Never a low."""
        cfg = self.config.last_reel_config
        last = self.config.num_reels - 1
        if self._boosting():
            drop = "supersplit"
        else:
            key = (
                "round"
                if self.gametype == self.config.freegame_type
                else "unlocked"
            )
            drop = get_random_outcome(cfg["drop_weights"][key])

        self.last_reel_feature = drop
        if drop == "shooter":
            self.board[last][0] = self.create_symbol("SH")
            self._pending_bounty_mult = 0
        elif drop == "supersplit":
            self.board[last][0] = self.create_symbol("SS")
            self._pending_bounty_mult = 0
        else:
            symbol = (
                "H1"
                if self._boosting()
                else get_random_outcome(cfg["premium_weights"])
            )
            self.board[last][0] = self.create_symbol(symbol)
            self._pending_bounty_mult = (
                max(cfg["bounty_mult_weights"].keys())
                if self._boosting()
                else get_random_outcome(cfg["bounty_mult_weights"])
            )
            self.last_reel_feature = "bounty"

    # ------------------------------------------------------ feature pipeline
    def apply_features(self):
        if self._cells_of({"SU"}) and not self.last_unlocked:
            self.last_unlocked = True
            self._fill_unlocked_lane()
            self._emit_tombstone = True
        if self._emit_tombstone:
            tombstone_event(self)
            self._emit_tombstone = False

        for _ in self._cells_of({"GS"}):
            self._apply_gunsmoke()

        for _ in self._cells_of({"SP"}):
            self._apply_split()

        for drop in list(self._nudge_drops):
            self._apply_nudge_ways(drop)

        if self.last_unlocked:
            self._apply_last_reel()

        self._wildify_features()

    def _apply_gunsmoke(self):
        cfg = self.config.gunsmoke_config
        present = self._present_types(set(cfg["source_weights"].keys()))
        if not present:
            return
        if self._boosting():
            lows = [n for n in self.config.low_symbols if n in present]
            source = lows[0] if lows else max(present, key=present.get)
        else:
            weights = {n: cfg["source_weights"][n] for n in present}
            source = get_random_outcome(weights)
        cells = self._cells_of({source})
        for c in cells:
            self.replace_keep_ways(c["reel"], c["row"], self.config.wild_symbol)
        gunsmoke_event(self, source, cells)

    def _apply_split(self):
        cfg = self.config.split_config
        present = self._present_types(set(cfg["source_weights"].keys()))
        if not present:
            return
        n = 1
        weights = {name: cfg["source_weights"][name] for name in present}
        symbols = self._weighted_sample(weights, max(1, n))
        factor = self._pick_factor(cfg["ways_weights"])
        cells = []
        for c in self._cells_of(set(symbols)):
            new_mult = self.add_cell_ways(c["reel"], c["row"], factor)
            cells.append({"reel": c["reel"], "row": c["row"], "multiplier": new_mult})
        if cells:
            split_event(self, factor, symbols, cells)

    def _apply_nudge_ways(self, drop):
        reel = drop["reel"]
        initial = int(drop["initial_ways"])
        height = len(self.board[reel])
        if drop["full_reel"]:
            cells = []
            for row in range(height):
                if self.board[reel][row].name in ("S", "SU"):
                    continue
                self.replace_keep_ways(reel, row, self.config.wild_symbol)
                self.set_cell_ways(reel, row, initial)
                cells.append({"reel": reel, "row": row, "multiplier": initial})
            nudge_ways_event(self, reel, True, 0, initial, initial, [], cells)
            return

        start = int(drop["start_row"])
        ways = initial
        filled = [start]
        if self.board[reel][start].name not in ("S", "SU"):
            self.replace_keep_ways(reel, start, self.config.wild_symbol)
            self.set_cell_ways(reel, start, ways)

        steps = []
        for row in range(start + 1, height):
            if self.board[reel][row].name in ("S", "SU"):
                continue
            ways *= 2
            self.replace_keep_ways(reel, row, self.config.wild_symbol)
            filled.append(row)
            for r in filled:
                self.set_cell_ways(reel, r, ways)
            steps.append({"row": row, "ways": ways})

        cells = [{"reel": reel, "row": r, "multiplier": ways} for r in filled]
        nudge_ways_event(self, reel, False, start, initial, ways, steps, cells)

    def _apply_last_reel(self):
        last = self.config.num_reels - 1
        name = self.board[last][0].name
        if name == "SH":
            self._apply_shooter()
        elif name == "SS":
            self._apply_supersplit()
        elif name in self.config.premium_symbols:
            self._apply_bounty(name)

    def _apply_supersplit(self):
        last = self.config.num_reels - 1
        factor = self._pick_factor(self.config.supersplit_config["all_ways_weights"])
        wild_cells = []
        for row in range(len(self.board[last])):
            self.replace_keep_ways(last, row, self.config.wild_symbol)
            wild_cells.append({"reel": last, "row": row})
        split_cells = []
        for reel in range(self.config.num_reels):
            for row in range(len(self.board[reel])):
                new_mult = self.add_cell_ways(reel, row, factor)
                split_cells.append({"reel": reel, "row": row, "multiplier": new_mult})
        super_split_event(self, factor, wild_cells, split_cells)

    def _apply_bounty(self, symbol):
        cfg = self.config.last_reel_config
        last = self.config.num_reels - 1
        base_mult = int(self._pending_bounty_mult or 0)
        if base_mult <= 0:
            base_mult = (
                max(cfg["bounty_mult_weights"].keys())
                if self._boosting()
                else get_random_outcome(cfg["bounty_mult_weights"])
            )
        total = self._add_win_mult(base_mult, "bounty")
        bounty_event(self, symbol, total, added=base_mult)
        win_mult_event(self, base_mult, total, "bounty")

    def _apply_shooter(self):
        """MARK: shoot every premium on the board, +1 stacked WIN multi each."""
        cfg = self.config.last_reel_config
        add_per = int(cfg.get("shooter_add_per_premium", 1))
        hits = self._cells_of(set(self.config.premium_symbols))
        added = len(hits) * add_per
        total = self._add_win_mult(added, "shooter")
        shooter_event(self, hits, added, total)
        if added:
            win_mult_event(self, added, total, "shooter")

    def _wildify_features(self):
        """Every remaining feature symbol becomes the revolver WILD."""
        names = set(self.config.feature_symbols)
        cells = []
        for reel in range(len(self.board)):
            for row in range(len(self.board[reel])):
                if self.board[reel][row].name in names:
                    self.replace_keep_ways(reel, row, self.config.wild_symbol)
                    cells.append({"reel": reel, "row": row})
        if cells:
            specials_wild_event(self, cells)
