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
        self.bar_mode = conditions.get("bar_mode", "off")
        self.boost = conditions.get("boost", "none")
        self.last_unlocked = bool(conditions.get("last_unlocked", False))

        self.create_board_reelstrips()
        if emit_event:
            reveal_event(self)

        self.roll_special_bar(conditions)
        special_bar_event(self)

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
            feature = get_random_outcome(cfg["weights"]["unlocked"])
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

        # NUDGE: the premium slides LEFT from the last lane across each column.
        # Every premium it passes climbs the WIN multiplier AND is left as a WILD
        # so the ways eval that follows sees the scorched cells as wilds.
        add_per = cfg["nudge_add_per_premium"]
        hits = []
        for reel in range(last - 1, -1, -1):
            for row, sym in enumerate(self.board[reel]):
                if self.is_premium(sym.name):
                    hits.append({"reel": reel, "row": row, "name": sym.name})
        passed = len(hits)
        win_mult = int(base_mult) + passed * add_per
        self.win_multiplier = max(1, win_mult)
        for h in hits:
            self.board[h["reel"]][h["row"]] = self.create_symbol(self.config.wild_symbol)
        # hits listed right-to-left (the order the slide encounters them)
        nudge_event(self, symbol, int(base_mult), passed, self.win_multiplier, hits)
