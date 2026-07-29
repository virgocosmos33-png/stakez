import random

from game_executables import GameExecutables
from game_events import (
    bonus_level_event,
    wild_reel_event,
    unlocked_slots_event,
    stretch_reel_event,
    clone_symbol_event,
    split_symbols_event,
)
from src.calculations.statistics import get_random_outcome
from src.events.events import reveal_event


class GameStateOverride(GameExecutables):
    """Wild Reel placement, bonus unlocked slots, and 3-level bonus handling.

    The legacy xMirror / Haunted-Mirror "split" feature (HM fractures + apparition
    multipliers + Madam's Eye wild conversion) has been fully removed. Wins come
    from plain ways plus the Wild Reel (a bottom-slot WILD grows its middle reel)
    and the bonus Unlocked Slots (bottom/right/left board expansion).
    """

    def reset_book(self):
        super().reset_book()
        self.fs_level = 1
        # Wild Reel: {reel: {"base_rows", "added", "target", "mults"}} planned
        # before the reveal and grown after it (commit_wild_reels).
        self.cell_seals = {}
        self.cell_seal_info = []
        # Reels that have actually GROWN into wild columns this spin. A plan in
        # cell_seals is not the same thing as a committed column, and SPLIT
        # needs to know which columns really exist before it tears through them.
        self._wild_reels = set()
        # Unlocked Slots (bonus board expansion): planned bottom-slot PREMIUMS
        # ({reel: premium_name}) and the resolved slot payload for the frontend.
        self._bottom_premiums = {}
        self.slot_info = []
        # New feature cells rolled into the bottom slots ({reel: "stretch"|"split"
        # |"clone"}) and the resolved payloads for the frontend events.
        self._bottom_features = {}
        # Board-wide features (CLONE / SPLIT) rolled into the SIDE columns:
        # [{"side": "right"|"left", "slotRow": int, "kind": "clone"|"split"}].
        self._side_features = []
        # winning symbols already split this spin (so multiple splits differ)
        self._split_used = set()
        self.stretch_info = []
        self.clone_info = {}
        self.split_info = {}

    def assign_special_sym_function(self):
        self.special_symbol_functions = {}

    def current_level_rules(self) -> dict:
        return self.config.bonus_levels[self.fs_level]

    def draw_board(self, emit_event=True, trigger_symbol="scatter"):
        """Draw the board, plan Wild Reels, reveal, open the bonus Unlocked Slots
        (premiums + side columns + side feature rolls), then fire every special-cell
        feature ONE AFTER ANOTHER in the fixed activation order (bottom cells
        left->right, right column bottom->top, left column top->bottom), each
        emitting its own event so the frontend plays them in exactly this order."""
        super().draw_board(emit_event=False, trigger_symbol=trigger_symbol)
        self.force_ante_scatter()
        self.plan_wild_reels()
        self.get_special_symbols_on_board()
        if emit_event:
            reveal_event(self)
        # Bonus board expansion (bottom premiums + right/left columns).
        self.apply_unlocked_slots(emit_event)
        # Special-cell features in strict activation order, one event per cell.
        self.apply_features_in_order(emit_event)

    def _plan_wild_rise(self, reel: int, target: int, mult_weights: dict):
        """Mark a middle reel to grow into a rising wild after the reveal."""
        base_rows = self.config.num_rows[reel]
        added = max(target - base_rows, 0)
        if added <= 0:
            return
        mults = [int(get_random_outcome(mult_weights)) for _ in range(added)]
        self.cell_seals[reel] = {
            "base_rows": base_rows,
            "added": added,
            "target": target,
            "mults": mults,
        }

    def plan_wild_reels(self):
        """Roll each bottom special-cell (under middle reels 1, 2, 3) for BOTH the
        base game and the bonus.

        Bonus: while the BOTTOM group is unlocked (level 1+), every cell rolls the
        rich content table (empty / premium / wild / stretch / split / clone).
        Base game: the cells are LOCKED - each rolls the sparse `content_weights_base`
        table, so a special symbol only very rarely drops and unlocks THAT one cell.

        Outcomes are recorded here and resolved after the reveal:
          wild    -> _plan_wild_rise (commit_wild_reels grows the reel)
          premium -> _bottom_premiums (apply_unlocked_slots drops it, bonus only)
          feature -> _bottom_features (apply_stretch / apply_clone / apply_split)."""
        self.cell_seals = {}
        self.cell_seal_info = []
        self._wild_reels = set()
        self._bottom_premiums = {}
        self._bottom_features = {}
        self._side_features = []
        self._split_used = set()
        self.slot_info = []
        self.stretch_info = []
        self.clone_info = {}
        self.split_info = {}

        win_criteria = self.get_current_betmode_distributions().get_win_criteria()
        if win_criteria == 0:
            return

        slot_cfg = getattr(self.config, "unlocked_slot_config", None) or {}
        wild_cfg = getattr(self.config, "wild_reel_config", None) or {}
        if not slot_cfg.get("enabled", False):
            return

        in_freegame = self.gametype == self.config.freegame_type
        bonus_bottom_open = (
            in_freegame
            and "bottom" in slot_cfg.get("unlock_by_level", {}).get(self.fs_level, [])
        )

        target = int(wild_cfg.get("target_rows", max(self.config.num_rows)))
        premium_weights = slot_cfg.get("premium_weights") or {"H1": 1}
        mult_weights = slot_cfg.get("mult_weights") or {1: 1}
        content_weights = (
            slot_cfg.get("content_weights")
            if bonus_bottom_open
            else slot_cfg.get("content_weights_base")
        ) or {"empty": 1}

        for reel in slot_cfg.get("bottom_reels", []):
            if reel < 0 or reel >= self.config.num_reels:
                continue
            outcome = get_random_outcome(content_weights)
            if outcome == "wild":
                self._plan_wild_rise(reel, target, mult_weights)
            elif outcome == "premium":
                self._bottom_premiums[reel] = str(get_random_outcome(premium_weights))
            elif outcome in ("stretch", "split", "clone"):
                self._bottom_features[reel] = outcome

    def _commit_wild_reel(self, reel: int, emit_event=True):
        """Grow ONE owned middle reel to its target height, appending WILD cells
        (each with a random multiplier) at the bottom - the existing symbols stay
        on top (pushed up). Emits its own wildReel event (single reel)."""
        data = self.cell_seals.get(reel)
        if not data:
            return
        wild_name = (self.config.special_symbols.get("wild") or ["W"])[0]
        cells = []
        for k in range(data["added"]):
            sym = self.create_symbol(wild_name)
            mult = int(data["mults"][k])
            if mult > 1:
                sym.assign_attribute({"multiplier": mult})
            self.board[reel].append(sym)
            cells.append({"row": len(self.board[reel]) - 1, "mult": mult})
        self._wild_reels.add(reel)
        self.cell_seal_info = [
            {
                "reel": reel,
                "base_rows": data["base_rows"],
                "added": data["added"],
                "cells": cells,
            }
        ]
        self.get_special_symbols_on_board()
        if emit_event:
            wild_reel_event(self)

    def commit_wild_reels(self, emit_event=True):
        """Grow every owned middle reel (kept for callers outside draw_board;
        the live pipeline fires them per cell via apply_features_in_order)."""
        for reel in sorted(self.cell_seals.keys()):
            self._commit_wild_reel(reel, emit_event)

    def _roll_side_column(self, side: str, slot_cfg: dict):
        """Roll one side column: `side_rows` independent slots. Each slot is a full
        FEATURE CELL - it can roll PREMIUM / WILD / EMPTY or a board-wide feature
        (CLONE / SPLIT). Returns:
          cells: filled premium/wild cells top-to-bottom [{"row", "name", "mult"?}]
          syms:  the built Symbol list (premium/wild only) appended as an extra reel
          feats: side feature cards [{"side", "slotRow", "kind"}] (clone/split) - a
                 feature cell places NO board symbol (it's a marker; the effect is
                 board-wide), so it doesn't add ways to the side reel itself."""
        rows = int(slot_cfg.get("side_rows", 3))
        # SIDE cells use their own content table (includes clone/split, no stretch).
        content_weights = (
            slot_cfg.get("content_weights_side")
            or slot_cfg.get("content_weights")
            or {"empty": 1}
        )
        premium_weights = slot_cfg.get("premium_weights") or {"H1": 1}
        mult_weights = slot_cfg.get("mult_weights") or {1: 1}
        wild_name = (self.config.special_symbols.get("wild") or ["W"])[0]
        cells, syms, feats = [], [], []
        for row in range(rows):
            outcome = get_random_outcome(content_weights)
            if outcome == "empty":
                continue
            if outcome in ("clone", "split"):
                feats.append({"side": side, "slotRow": row, "kind": outcome})
                continue
            if outcome == "wild":
                sym = self.create_symbol(wild_name)
                mult = int(get_random_outcome(mult_weights))
                if mult > 1:
                    sym.assign_attribute({"multiplier": mult})
                cells.append({"row": row, "name": wild_name, "mult": mult})
            else:
                name = str(get_random_outcome(premium_weights))
                sym = self.create_symbol(name)
                cells.append({"row": row, "name": name})
            syms.append(sym)
        return cells, syms, feats

    def apply_unlocked_slots(self, emit_event=True):
        """Free-spin board expansion. Drops the planned bottom-slot PREMIUMS and
        rolls the unlocked RIGHT / LEFT side columns for the current bonus level,
        appending every filled slot to the board as a real cell so the ways
        engine connects across 6 (RIGHT) or 7 (LEFT) reels. Emitted after the
        reveal / wild-reel events."""
        slot_cfg = getattr(self.config, "unlocked_slot_config", None) or {}
        if self.gametype != self.config.freegame_type or not slot_cfg.get("enabled", False):
            return
        if self.get_current_betmode_distributions().get_win_criteria() == 0:
            return

        groups = slot_cfg.get("unlock_by_level", {}).get(self.fs_level, [])
        bottom_cells, sides = [], []

        # BOTTOM premiums (wild bottom slots already rose via commit_wild_reels).
        for reel in sorted(self._bottom_premiums.keys()):
            if reel in self.cell_seals:  # reel already grew a rising wild
                continue
            name = self._bottom_premiums[reel]
            sym = self.create_symbol(name)
            self.board[reel].append(sym)
            bottom_cells.append({"reel": reel, "row": len(self.board[reel]) - 1, "name": name})

        # RIGHT then LEFT side columns become new reels (only when they hold >=1
        # premium/wild symbol, so the ways engine never sees a blank reel). CLONE /
        # SPLIT feature cards are recorded separately (they add no board symbol) so
        # they still fire even if the column has no premium/wild.
        for side in ("right", "left"):
            if side not in groups:
                continue
            cells, syms, feats = self._roll_side_column(side, slot_cfg)
            self._side_features.extend(feats)
            if not syms:
                continue
            reel_index = len(self.board)
            self.board.append(syms)
            sides.append({"side": side, "reel": reel_index, "cells": cells})

        self.slot_info = {"level": self.fs_level, "unlocked": groups, "bottom": bottom_cells, "sides": sides}
        # Emit whenever this level has any unlocked group so the frontend keeps
        # those cells OPEN for the whole bonus (level 1 = bottom, level 2 =
        # bottom+right, level 3 = all). Every open cell lands SOMETHING every
        # spin: a premium/wild here, or a feature card via the feature events
        # (with _fallback_premium_drop covering a card that can't fire).
        if groups:
            if bottom_cells or sides:
                self.get_special_symbols_on_board()
            if emit_event:
                unlocked_slots_event(self)

    def _fallback_premium_drop(self, placement: dict, emit_event=True):
        """A feature card that cannot fire (a SPLIT with nothing to split, a
        CLONE with no source symbol) must not leave its open cell empty: every
        unlocked cell lands SOMETHING every free spin. The dead card is replaced
        by a random premium dropped into the same cell — appended to the board
        exactly like any unlocked-slot premium (so it genuinely pays) and
        announced by re-emitting unlockedSlots with the updated payload, which
        the frontend resolves by reeling in just the new cell."""
        if self.gametype != self.config.freegame_type or not isinstance(self.slot_info, dict):
            return  # base game: a dead feature leaves the cell locked, as before
        slot_cfg = getattr(self.config, "unlocked_slot_config", None) or {}
        premium_weights = slot_cfg.get("premium_weights") or {"H1": 1}
        name = str(get_random_outcome(premium_weights))
        sym = self.create_symbol(name)
        if placement.get("reel") is not None:
            reel = placement["reel"]
            self.board[reel].append(sym)
            self.slot_info.setdefault("bottom", []).append(
                {"reel": reel, "row": len(self.board[reel]) - 1, "name": name}
            )
        elif placement.get("side") is not None:
            # the side column may not exist as a reel yet (every cell rolled a
            # feature card) — create it so the premium contributes ways too.
            entry = next(
                (s for s in self.slot_info.setdefault("sides", []) if s["side"] == placement["side"]),
                None,
            )
            if entry is None:
                entry = {"side": placement["side"], "reel": len(self.board), "cells": []}
                self.board.append([])
                self.slot_info["sides"].append(entry)
            self.board[entry["reel"]].append(sym)
            # cells are stored in board-row order with "row" = the visual slot
            # row, matching _roll_side_column / unlocked_slots_event.
            entry["cells"].append({"row": placement["slotRow"], "name": name})
        else:
            return
        self.get_special_symbols_on_board()
        if emit_event:
            unlocked_slots_event(self)

    def apply_features_in_order(self, emit_event=True):
        """Fire every special-cell feature ONE AFTER ANOTHER in the fixed
        activation order, each emitting its own event:

          1. BOTTOM cells left -> right (a cell's outcome is a rising WILD reel,
             a STRETCH, a CLONE or a SPLIT),
          2. RIGHT column bottom -> top (slotRow 2, 1, 0),
          3. LEFT column top -> bottom (slotRow 0, 1, 2).

        The frontend plays each event with that cell's border electrified while
        its feature animation runs, then moves to the next."""
        bottoms = sorted(set(self.cell_seals.keys()) | set(self._bottom_features.keys()))
        for reel in bottoms:
            if reel in self.cell_seals:
                self._commit_wild_reel(reel, emit_event)
                continue
            kind = self._bottom_features.get(reel)
            if kind == "stretch":
                self._apply_stretch_reel(reel, emit_event)
            elif kind == "clone":
                self._apply_clone_cell({"reel": reel}, emit_event)
            elif kind == "split":
                self._apply_split_cell({"reel": reel}, emit_event)

        rights = sorted(
            (f for f in self._side_features if f["side"] == "right"),
            key=lambda f: -f["slotRow"],
        )
        lefts = sorted(
            (f for f in self._side_features if f["side"] == "left"),
            key=lambda f: f["slotRow"],
        )
        for f in rights + lefts:
            placement = {"side": f["side"], "slotRow": f["slotRow"]}
            if f["kind"] == "clone":
                self._apply_clone_cell(placement, emit_event)
            elif f["kind"] == "split":
                self._apply_split_cell(placement, emit_event)

    def _reel_ways_sum(self, reel_index: int) -> int:
        """Ways contribution of one reel: symbols summed, a multiplier cell counts
        as its multiplier (matches count_board_ways / the ways engine)."""
        total = 0
        for sym in self.board[reel_index]:
            total += sym.get_attribute("multiplier") if sym.check_attribute("multiplier") else 1
        return total

    def _cap_stretch_added(self, reel: int, added: int, ways_cap: int) -> int:
        """Trim `added` rows so the total board ways stays within ways_cap."""
        if added <= 0:
            return 0
        others = 1
        for r in range(len(self.board)):
            if r == reel:
                continue
            others *= max(self._reel_ways_sum(r), 1)
        current = self._reel_ways_sum(reel)
        max_reel_sum = ways_cap // max(others, 1)
        allowed = max(0, max_reel_sum - current)
        return min(added, allowed)

    def apply_stretch(self, emit_event=True):
        """STRETCH: the stretch cell stretches ITS reel and gives the symbols on that
        reel extra x-ways.

        - NORMAL reel: every symbol on the reel gets a weighted-random x-ways
          multiplier (volatile 1-3 common, tail to 10). The frontend stretches each
          symbol a little in place and shows the multiplier (when > 5). The reel's
          total ways (sum of the per-symbol multipliers) is capped by ways_cap (500).
        - WILD reel (all symbols wild): treated as one full-reel wild column; it still
          gets the same per-symbol multipliers (so the reel's ways sum up), and the
          frontend shows the wild column + a single centred 'N WAYS' total.

        count_board_ways() counts a symbol with multiplier=m as m symbols on its reel,
        so summing the multipliers is exactly the reel's ways contribution.
        """
        for reel in sorted(r for r, v in self._bottom_features.items() if v == "stretch"):
            self._apply_stretch_reel(reel, emit_event)

    def _apply_stretch_reel(self, reel: int, emit_event=True):
        """Stretch ONE reel (see apply_stretch docstring) and emit its own
        stretchReel event (single reel)."""
        cfg = getattr(self.config, "stretch_config", {}) or {}
        ways_weights = cfg.get("ways_weights") or {1: 1}
        ways_cap = int(cfg.get("ways_cap", 500))
        wild_chance = float(cfg.get("wild_chance", 0.0))
        wilds = set(self.config.special_symbols.get("wild", []))
        wild_name = next(iter(self.config.special_symbols.get("wild", [])), None)
        symbols = self.board[reel]
        rows = len(symbols)
        if rows == 0:
            return
        # WILD stretch happens ONLY when the reel is already all-wild (an edge
        # kept for safety). wild_chance stays honoured for experiments, but ships
        # at 0: a card that says STRETCH must never manufacture a wild column,
        # that is the WILD card's job.
        is_wild = all(sym.name in wilds for sym in symbols)
        if not is_wild and wild_name is not None and random.random() < wild_chance:
            for row in range(rows):
                self.board[reel][row] = self.create_symbol(wild_name)
            symbols = self.board[reel]
            is_wild = True
        cells = []
        total = 0
        for row, sym in enumerate(symbols):
            remaining_after = rows - row - 1  # reserve >=1 way for each later symbol
            headroom = max(1, ways_cap - total - remaining_after)
            mult = int(get_random_outcome(ways_weights))
            mult = max(1, min(mult, headroom))
            sym.assign_attribute({"multiplier": mult})
            cells.append({"row": row, "multiplier": mult})
            total += mult
        # A wild-mode stretch leaves a column of real W symbols, which makes it a
        # wild reel in every sense that matters — including being torn by SPLIT.
        if is_wild:
            self._wild_reels.add(reel)
        self.stretch_info = [
            {
                "reel": reel,
                "mode": "wild" if is_wild else "normal",
                "base_rows": rows,
                "cells": cells,
                "reel_ways": total,
            }
        ]
        self.get_special_symbols_on_board()
        if emit_event:
            stretch_reel_event(self)

    def apply_clone(self, emit_event=True):
        """CLONE: EACH clone cell picks ONE symbol type present on the board
        (source_weights bias the pick toward common/low symbols) and converts every
        copy of it into a weighted-random premium (H1-H5). Multiple clone cells each
        fire in turn (emitting one cloneSymbol event apiece)."""
        # a CLONE card can land in a BOTTOM cell ({reel}) or a SIDE slot
        # ({side, slotRow}); both fire the same board-wide conversion.
        placements = [
            {"reel": r} for r in sorted(r for r, v in self._bottom_features.items() if v == "clone")
        ] + [
            {"side": f["side"], "slotRow": f["slotRow"]}
            for f in self._side_features if f["kind"] == "clone"
        ]
        for placement in placements:
            self._apply_clone_cell(placement, emit_event)

    def _apply_clone_cell(self, placement: dict, emit_event=True):
        """Fire ONE clone card (board-wide conversion) and emit its event."""
        cfg = getattr(self.config, "clone_config", {}) or {}
        source_weights = cfg.get("source_weights") or {}
        premium_weights = cfg.get("premium_weights") or {"H1": 1}
        wilds = set(self.config.special_symbols.get("wild", []))
        scatters = set(self.config.special_symbols.get("scatter", []))
        features = {"STRETCH", "SPLIT", "CLONE"}

        # cells behind a wild-reel overlay are invisible to the player, so
        # cloning them reads as nothing happening — exclude those reels both
        # as clone sources and as conversion targets.
        wild_reels = getattr(self, "_wild_reels", set())

        # re-scan the live board: an earlier clone may have already changed it
        present = {}
        for r, reel in enumerate(self.board):
            if r in wild_reels:
                continue
            for sym in reel:
                n = sym.name
                if n in wilds or n in scatters or n in features:
                    continue
                present[n] = present.get(n, 0) + 1
        if not present:
            self._fallback_premium_drop(placement, emit_event)
            return

        pick_weights = {n: source_weights.get(n, 1) for n in present}
        from_name = str(get_random_outcome(pick_weights))
        to_name = str(get_random_outcome(premium_weights))

        cells = []
        for r, reel in enumerate(self.board):
            if r in wild_reels:
                continue
            for row, sym in enumerate(reel):
                if sym.name == from_name:
                    new_sym = self.create_symbol(to_name)
                    # a clone must NEVER cost the player anything: if the old
                    # cell carried extra ways (from a split or stretch), the
                    # new premium inherits them instead of resetting to 1.
                    if sym.check_attribute("multiplier"):
                        new_sym.assign_attribute({"multiplier": sym.get_attribute("multiplier")})
                    self.board[r][row] = new_sym
                    cells.append({"reel": r, "row": row})
        if not cells:
            self._fallback_premium_drop(placement, emit_event)
            return
        self.clone_info = {"cell": placement, "from": from_name, "to": to_name, "cells": cells}
        self.get_special_symbols_on_board()
        if emit_event:
            clone_symbol_event(self)

    def apply_split(self, emit_event=True):
        """SPLIT: after wins are known, EACH split cell picks ONE winning symbol type
        and ADDS a weighted +1..+10 ways to each of its winning (non-wild) cells, so
        the ways engine counts extra copies. Multiple split cells each fire in turn
        (re-reading the wins so a later split can target a different symbol). No-op on
        a losing spin."""
        # a SPLIT card can land in a BOTTOM cell ({reel}) or a SIDE slot
        # ({side, slotRow}); both boost one winning symbol's cells.
        placements = [
            {"reel": r} for r in sorted(r for r, v in self._bottom_features.items() if v == "split")
        ] + [
            {"side": f["side"], "slotRow": f["slotRow"]}
            for f in self._side_features if f["kind"] == "split"
        ]
        for placement in placements:
            self._apply_split_cell(placement, emit_event)

    def _apply_split_cell(self, placement: dict, emit_event=True):
        """Fire ONE split card and emit its event. Each split this spin MUST hit
        a DIFFERENT winning symbol (self._split_used, reset per reveal); once
        every winning symbol has been split, later cards only tear the wild
        columns. Splitting the same symbol twice read as the feature repeating
        itself, so it is simply not allowed."""
        cfg = getattr(self.config, "split_config", {}) or {}
        split_weights = cfg.get("split_weights") or {1: 1}
        wins = (self.get_ways_data() or {}).get("wins", [])
        choices = [w for w in wins if w["symbol"] not in self._split_used]
        factor = int(get_random_outcome(split_weights))
        cells = []
        symbol = None
        if choices:
            win = random.choice(choices)
            symbol = win["symbol"]
            self._split_used.add(symbol)
            for pos in win.get("positions", []):
                r, row = pos["reel"], pos["row"]
                sym = self.board[r][row]
                if sym.name != symbol:  # wilds are handled below, on the whole column
                    continue
                existing = (
                    sym.get_attribute("multiplier") if sym.check_attribute("multiplier") else 1
                )
                # ADDITIVE, never multiplicative: a split is worth "+1 to +10 ways"
                # on the cell it hits, exactly what the card promises. Multiplying
                # stacked features (a 10x stretch cell hit by a 10-split becoming
                # 100x) ran away from that promise instantly.
                new_mult = existing + factor
                sym.assign_attribute({"multiplier": new_mult})
                cells.append({"reel": r, "row": row, "multiplier": new_mult})

        cells += self._split_wild_reels(factor)
        if not cells:
            # nothing to split (no winning symbol, no wild column): the card is
            # dead — a premium drops into its cell instead, never an empty cell.
            self._fallback_premium_drop(placement, emit_event)
            return
        if symbol is None:
            # wild-reels-only split: no symbol name to report, use the wild
            symbol = (self.config.special_symbols.get("wild") or ["W"])[0]
        self.split_info = {
            "cell": placement,
            "symbol": symbol,
            "mult": factor,
            "cells": cells,
            # the columns the split tore through, with what each is now worth,
            # so the frontend can re-stamp their badges
            "wild_reels": [
                {"reel": reel, "ways": self.reel_ways(reel)}
                for reel in sorted(self._wild_reels)
            ],
        }
        self.get_special_symbols_on_board()
        if emit_event:
            split_symbols_event(self)

    def _split_wild_reels(self, factor: int) -> list:
        """A split also tears through every risen wild column, adding its factor
        to each wild cell (the same additive rule as paying cells: a 5x wild
        caught by a 3-split becomes 8x).

        One difference from the paying-symbol case, deliberate: it takes the
        WHOLE column, not just the cells that happened to complete the winning
        way. The feature reads as the split cutting through the column, and
        cutting through half of it would look like a bug.
        """
        wild_name = (self.config.special_symbols.get("wild") or ["W"])[0]
        cells = []
        for reel in sorted(self._wild_reels):
            for row, sym in enumerate(self.board[reel]):
                if sym.name != wild_name:
                    continue
                existing = (
                    sym.get_attribute("multiplier") if sym.check_attribute("multiplier") else 1
                )
                new_mult = existing + factor
                sym.assign_attribute({"multiplier": new_mult})
                cells.append({"reel": reel, "row": row, "multiplier": new_mult, "wild": True})
        return cells

    def force_ante_scatter(self):
        """ANTE mode: every base spin is guaranteed a scatter on the forced
        reel (condition "force_scatter_reel"). The scatter replaces a random
        plain symbol in the window before the reveal, so the rest of the
        pipeline treats it like a natural scatter."""
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
        ]
        row = random.choice(plain_rows if plain_rows else list(range(self.config.num_rows[reel])))
        self.board[reel][row] = self.create_symbol(scatters[0])
        self.get_special_symbols_on_board()

    def update_freespin_amount(self, scatter_key: str = "scatter"):
        """Scatter count picks the bonus level."""
        if self.gametype == self.config.basegame_type:
            scatter_count = min(self.count_special_symbols(scatter_key), 5)
            self.fs_level = self.config.scatter_to_level[max(scatter_count, 3)]
        super().update_freespin_amount(scatter_key)
        if self.gametype == self.config.basegame_type:
            bonus_level_event(self)
