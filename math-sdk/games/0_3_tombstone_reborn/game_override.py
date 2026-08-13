"""TOMBSTONE REBORN - board draw + special-system pipeline (built from scratch).

A spin is a single enhanced reveal. After the board is drawn we:
  1. resolve the top SPECIAL BAR cards,
  2. apply their board-wide effects in a fixed order,
  3. resolve the LAST-REEL lane (if open),
  4. then hand the mutated board to the ways evaluator, which also applies the
     accumulated WIN multiplier.

Ordering matters: every effect that changes the ways COUNT (coffin growth,
gunsmoke wildify, gang/outlaw splits, supersplit) is applied BEFORE the single
ways evaluation, and the WIN multiplier (bounty/nudge) is the last thing set so
a nudge counts premiums on the fully-enriched board.
"""

import random

from game_executables import GameExecutables
from src.calculations.statistics import get_random_outcome
from src.events.events import reveal_event
from game_events import (
    special_bar_event,
    dig_up_event,
    coffin_open_event,
    gunsmoke_event,
    split_event,
    super_split_event,
    bounty_event,
    nudge_event,
)


class GameStateOverride(GameExecutables):
    """Draw the board and run the whole special system for a single spin."""

    # ------------------------------------------------------------------ setup
    def reset_book(self):
        super().reset_book()
        self.win_multiplier = 1
        self.bar_mode = "off"
        self.boost = "none"
        self.last_unlocked = False
        self.special_bar = []
        self.last_reel_feature = "none"
        # bonus-round state: which tier triggered ("small"/"big"), whether the
        # small round has upgraded, and the pending 4th-scatter drop
        self.fs_tier = "small"
        self.fs_upgraded = False
        self._pending_upgrade = False
        self._upgrade_scatter = None

    def assign_special_sym_function(self):
        # Wild flag is derived from special_symbols by the board reader; no
        # per-symbol attribute function is needed.
        self.special_symbol_functions = {}

    # ---------------------------------------------------------- pick helpers
    def _boosting(self) -> bool:
        return self.boost == "max"

    def _pick_factor(self, weights: dict):
        """Numeric-keyed roll; boosted spins take the maximum factor."""
        if self._boosting():
            return max(weights.keys())
        return get_random_outcome(weights)

    def _present_types(self, candidates) -> dict:
        """Return {name: count} for candidate symbol names present on the board."""
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

    # ----------------------------------------------------------- board draw
    def draw_board(self, emit_event=True, trigger_symbol="scatter"):
        conditions = self.get_current_distribution_conditions()
        self.boost = conditions.get("boost", "none")

        if self.gametype == self.config.freegame_type:
            # BONUS-ROUND spin: the bar and lane come from the fs_* condition
            # keys plus the live upgrade state. The lane is open every spin of
            # the big bonus (fs_last) or once the small bonus has upgraded.
            self.bar_mode = conditions.get("fs_bar", "wake")
            self.last_unlocked = bool(conditions.get("fs_last", False)) or self.fs_upgraded
            self.create_board_reelstrips()
            if self._pending_upgrade:
                self._place_upgrade_scatter()
            if emit_event:
                reveal_event(self)
            self.roll_special_bar(conditions)
            special_bar_event(self)
            return

        # BASE spin: honour this book's scatter target. "none" books redraw
        # any accidental 3+ away (sparse strip, cheap); trigger books draw the
        # dense BRT strip until the exact tier lands (P ~ 0.26 / 0.11 a draw).
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
        else:  # pragma: no cover - odds are astronomical, redraw the spin
            self.repeat = True
        if emit_event:
            reveal_event(self)

        self.roll_special_bar(conditions)
        special_bar_event(self)

    def _place_upgrade_scatter(self):
        """The 1-in-100 UPGRADE: the 4th scatter drops into the round.

        Placed on one of the two short right-hand columns (3/4) so it reads as
        the missing 4th scatter marching toward the sealed lane. Overwrites
        the drawn symbol BEFORE the reveal so the book's board carries it.
        """
        reel = random.choice((3, 4))
        row = random.randrange(len(self.board[reel]))
        self.board[reel][row] = self.create_symbol("S")
        self._upgrade_scatter = {"reel": reel, "row": row}

    def roll_special_bar(self, conditions):
        """Fill the top bar cells with cards for this spin."""
        cfg = self.config.special_bar_config
        cells = cfg["cells"]
        weights = cfg["weights"].get(self.bar_mode, cfg["weights"]["off"])
        force_count = int(conditions.get("force_special_count", 0))

        # boosted (forced-wincap) bars fire a fixed, maximal set of cards
        if self._boosting():
            forced = ["split_gang", "split_gang", "split_outlaws", "gunsmoke", "coffin", "digup"]
            self.special_bar = [
                {"reel": i, "kind": forced[i % len(forced)]} for i in range(cells)
            ]
            return

        bar = [{"reel": i, "kind": get_random_outcome(weights)} for i in range(cells)]

        # guarantee a minimum number of non-empty cards (super bonus = 6)
        if force_count > 0:
            non_none = {k: w for k, w in weights.items() if k != "none"} or {"coffin": 1}
            empties = [c for c in bar if c["kind"] == "none"]
            random.shuffle(empties)
            need = force_count - (cells - len(empties))
            for c in empties[:max(0, need)]:
                c["kind"] = get_random_outcome(non_none)

        self.special_bar = bar

    # ------------------------------------------------------ feature pipeline
    def apply_features(self):
        kinds = [c["kind"] for c in self.special_bar]

        # 1. DIG UP - opens the last-reel lane for this spin (base/small)
        if "digup" in kinds and not self.last_unlocked:
            self.last_unlocked = True
            dig_up_event(self)

        # 2. TOMBSTONE OPEN - grow the short reels (never the last-reel lane)
        if "coffin" in kinds:
            self._apply_coffin()

        # 3. GUNSMOKE - one whole type becomes wild (per card)
        for _ in [k for k in kinds if k == "gunsmoke"]:
            self._apply_gunsmoke()

        # 4. SPLIT-GANG - +ways to every premium (per card)
        for _ in [k for k in kinds if k == "split_gang"]:
            self._apply_split("gang")

        # 5. SPLIT-OUTLAWS - +ways to every low (per card)
        for _ in [k for k in kinds if k == "split_outlaws"]:
            self._apply_split("outlaws")

        # 6. LAST-REEL lane
        if self.last_unlocked:
            self._apply_last_reel()

    # ---- individual effects ------------------------------------------------
    def _apply_coffin(self):
        """Grow ONLY the reel under each coffin bar card, by at most +1 row.
        The last-reel special lane is never grown."""
        cfg = self.config.coffin_config
        last = self.config.num_reels - 1
        max_added = int(cfg.get("max_added", 1))
        coffin_reels = sorted({
            c["reel"] for c in self.special_bar
            if c["kind"] == "coffin" and c["reel"] != last
        })
        grown = []
        for reel in coffin_reels:
            added = max_added
            strip = self.reelstrip[reel]
            new_cells = []
            for _ in range(added):
                sym = self.create_symbol(random.choice(strip))
                self.board[reel].append(sym)
                new_cells.append({"row": len(self.board[reel]) - 1, "name": sym.name})
            grown.append({"reel": reel, "added": added, "cells": new_cells})
        if grown:
            coffin_open_event(self, grown)

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
            self.board[c["reel"]][c["row"]] = self.create_symbol(self.config.wild_symbol)
        gunsmoke_event(self, source, cells)

    def _apply_split(self, kind):
        cfg = self.config.split_config
        if kind == "gang":
            factor = self._pick_factor(cfg["gang_weights"])
            targets = set(self.config.premium_symbols)
        else:
            factor = self._pick_factor(cfg["outlaw_weights"])
            targets = set(self.config.low_symbols)
        cells = []
        for c in self._cells_of(targets):
            new_mult = self.add_cell_ways(c["reel"], c["row"], factor)
            cells.append({"reel": c["reel"], "row": c["row"], "multiplier": new_mult})
        if cells:
            split_event(self, kind, factor, cells)

    def _apply_last_reel(self):
        cfg = self.config.last_reel_config
        if self._boosting():
            feature = "supersplit"
        else:
            # bonus-round spins draw the diluted lane rate; single enhanced
            # spins (base digup / bought super) keep the full 78% rate
            key = (
                "round"
                if self.gametype == self.config.freegame_type
                else "unlocked"
            )
            feature = get_random_outcome(cfg["weights"][key])
        self.last_reel_feature = feature
        if feature == "none":
            return
        if feature == "supersplit":
            self._apply_supersplit()
        elif feature == "bounty":
            self._apply_bounty(slide=False)
        elif feature == "nudge":
            self._apply_bounty(slide=True)

    def _apply_supersplit(self):
        last = self.config.num_reels - 1
        factor = self._pick_factor(self.config.supersplit_config["all_ways_weights"])
        # last reel turns wild
        wild_cells = []
        for row in range(len(self.board[last])):
            self.board[last][row] = self.create_symbol(self.config.wild_symbol)
            wild_cells.append({"reel": last, "row": row})
        # every paying cell on each reel's live visible height (diamond /
        # coffin-grown) — never invent rows past len(board[reel])
        split_cells = []
        for reel in range(self.config.num_reels):
            for row in range(len(self.board[reel])):
                new_mult = self.add_cell_ways(reel, row, factor)
                split_cells.append({"reel": reel, "row": row, "multiplier": new_mult})
        super_split_event(self, factor, wild_cells, split_cells)

    def _apply_bounty(self, slide: bool):
        cfg = self.config.last_reel_config
        last = self.config.num_reels - 1
        if self._boosting():
            symbol = "H1"
            base_mult = max(cfg["bounty_mult_weights"].keys())
        else:
            symbol = get_random_outcome(cfg["premium_weights"])
            base_mult = get_random_outcome(cfg["bounty_mult_weights"])
        # the premium lands in the lane (top cell of the last reel)
        self.board[last][0] = self.create_symbol(symbol)

        if not slide:
            self.win_multiplier = max(1, int(base_mult))
            bounty_event(self, symbol, self.win_multiplier)
            return

        # NUDGE: xNudge sideways. The NUDGE WILD lands in the lane, then racks
        # LEFT one notch per reel, stepping onto exactly ONE cell of each
        # column: a random half-step up/down out of the centred lane, straight
        # or diagonal notches across the middle, and a forced diagonal at the
        # end so it always comes to rest on the FIRST reel's middle cell.
        # Every cell it steps through is left as a WILD (one per reel — a full
        # horizontal wild line), and every premium it crushes on the way adds
        # to the WIN multiplier.
        add_per = cfg["nudge_add_per_premium"]
        path = self._nudge_path(last)
        steps = []
        passed = 0
        for reel, row in path:
            sym_name = self.board[reel][row].name
            is_prem = self.is_premium(sym_name)
            passed += 1 if is_prem else 0
            steps.append({"reel": reel, "row": row, "name": sym_name, "premium": is_prem})
        win_mult = int(base_mult) + passed * add_per
        self.win_multiplier = max(1, win_mult)
        # the lane cell itself is the rider's origin: it keeps a wild too, so
        # the wake is one wild on every reel, lane included
        self.board[last][0] = self.create_symbol(self.config.wild_symbol)
        for reel, row in path:
            self.board[reel][row] = self.create_symbol(self.config.wild_symbol)
        nudge_event(self, "W", int(base_mult), passed, self.win_multiplier, steps)

    def _nudge_path(self, last):
        """The cells the nudge wild steps onto, right-to-left (reel last-1..0).

        Board rows are vertically centred (diamond board), so adjacency is by
        CENTRE distance, exactly as the frontend lays cells out: a notch may
        shift the rider at most one symbol-height up or down. The walk is
        random where the grid allows a choice, but filtered so the first
        reel's middle cell always stays within reach (one vertical unit per
        remaining reel).
        """
        max_rows = max(len(r) for r in self.board[:last]) if last > 0 else 1

        def centre(reel, row):
            rows = len(self.board[reel])
            if reel == last:
                nb = len(self.board[reel - 1])
                off = (max_rows - nb) / 2 + (nb - rows) / 2
            else:
                off = (max_rows - rows) / 2
            return off + row + 0.5

        target_row = (len(self.board[0]) - 1) // 2

        # Backward reachability (per-reel row sets), so the walk can NEVER
        # paint itself into a corner: a row is reachable if some row of the
        # next reel leftward is both reachable and within one notch of it.
        # A pure distance-budget bound is NOT enough on coffin-grown boards —
        # mixed offsets mean a step can't always move a full symbol toward the
        # target, and the old guard then teleported the rider.
        reachable = {0: {target_row}}
        for reel in range(1, last):
            reachable[reel] = {
                row
                for row in range(len(self.board[reel]))
                if any(
                    abs(centre(reel, row) - centre(reel - 1, nxt)) <= 1.01
                    for nxt in reachable[reel - 1]
                )
            }

        path = []
        cy = centre(last, 0)
        for reel in range(last - 1, -1, -1):
            candidates = [
                row
                for row in sorted(reachable[reel])
                if abs(centre(reel, row) - cy) <= 1.01
            ]
            if not candidates:  # cannot happen by construction; keep a guard
                candidates = [
                    min(
                        sorted(reachable[reel]),
                        key=lambda row: abs(centre(reel, row) - cy),
                    )
                ]
            row = random.choice(candidates)
            path.append((reel, row))
            cy = centre(reel, row)
        return path
