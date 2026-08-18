"""Ways evaluation for TOMBSTONE REBORN.

Two multiplier layers combine here:
  * WAYS multipliers - split / nudge / supersplit / last-reel premium stamp a
    per-cell `multiplier` that folds into the ways COUNT (cells on one reel
    add together; reels multiply).
  * WIN multiplier - features tick `self.win_multiplier` (identity 1x), which
    multiplies the whole spin's win AFTER the ways total is computed.

The evaluation is GAME-LOCAL (not the shared src/calculations/ways.py) to
enforce two published rules the shared engine does not:
  * Wilds never complete a way on their own - a way must include at least one
    regular paying symbol. Pure-wild ways pay ONLY through the dedicated
    (6, W) paytable line.
  * The wild line counts every W cell exactly once. The shared engine seeds
    W into its own potential-wins table AND its wild table whenever a wild
    sits on reel 0, double-counting every wild cell (2x ways per cell).
"""

from game_calculations import GameCalculations
from src.calculations.ways import Ways


class GameExecutables(GameCalculations):
    """Ways evaluation with a post-hoc global WIN multiplier."""

    def _tr_ways_data(self) -> dict:
        """Ways calculation. Identical to the shared engine's "symbol"
        strategy for ordinary boards; differs only on wild-flooded boards
        (see module docstring)."""
        config = self.config
        board = self.board
        wild_names = set(config.special_symbols["wild"])
        nreels = len(board)

        def cell_mult(sym) -> int:
            if sym.check_attribute("multiplier"):
                val = sym.get_attribute("multiplier")
                if isinstance(val, int) and val > 0:
                    return val
            return 1

        paying = {name for _, name in config.paytable} - wild_names

        wild_sum = [0] * nreels
        wild_cells = [[] for _ in range(nreels)]
        sym_sum = {name: [0] * nreels for name in paying}
        sym_cells = {name: [[] for _ in range(nreels)] for name in paying}
        for reel in range(nreels):
            for row, sym in enumerate(board[reel]):
                name = sym.name
                if name in wild_names:
                    wild_sum[reel] += cell_mult(sym)
                    wild_cells[reel].append({"reel": reel, "row": row})
                elif name in paying:
                    sym_sum[name][reel] += cell_mult(sym)
                    sym_cells[name][reel].append({"reel": reel, "row": row})

        return_data = {"totalWin": 0, "wins": []}

        def push_win(symbol, kind, ways, positions):
            sym_mult = 0
            for reel in range(kind):
                for pos in wild_cells[reel]:
                    val = cell_mult(board[pos["reel"]][pos["row"]])
                    if val > 1:
                        sym_mult += val
            win = round(config.paytable[(kind, symbol)] * ways, 2)
            return_data["wins"].append(
                {
                    "symbol": symbol,
                    "kind": kind,
                    "win": win,
                    "positions": positions,
                    "meta": {
                        "ways": ways,
                        "globalMult": 1,
                        "winWithoutMult": win,
                        "symbolMult": sym_mult,
                    },
                }
            )
            return_data["totalWin"] += win

        # The pure-wild line: consecutive wild reels from reel 0, every W cell
        # counted once. Pays only where the paytable has a W entry (6-wide).
        wild_kind = 0
        for reel in range(nreels):
            if wild_sum[reel] > 0:
                wild_kind += 1
            else:
                break
        if wild_kind > 0 and (wild_kind, config.wild_symbol) in config.paytable:
            ways = 1
            positions = []
            for reel in range(wild_kind):
                ways *= wild_sum[reel]
                positions += wild_cells[reel]
            push_win(config.wild_symbol, wild_kind, ways, positions)

        # Paying symbols: leftmost-longest run of (symbol or wild). Ways that
        # would run through wilds ALONE are excluded - they belong to the wild
        # line above, so a way always includes a regular paying symbol.
        for name in paying:
            if not any(sym_sum[name]):
                continue
            kind = 0
            for reel in range(nreels):
                if sym_sum[name][reel] > 0 or wild_sum[reel] > 0:
                    kind += 1
                else:
                    break
            if kind == 0 or (kind, name) not in config.paytable:
                continue
            ways = 1
            pure = 1
            all_wild = True
            for reel in range(kind):
                ways *= sym_sum[name][reel] + wild_sum[reel]
                if wild_sum[reel] > 0:
                    pure *= wild_sum[reel]
                else:
                    all_wild = False
            effective = ways - (pure if all_wild else 0)
            if effective <= 0:
                continue
            positions = []
            for reel in range(kind):
                positions += sym_cells[name][reel]
                positions += wild_cells[reel]
            push_win(name, kind, effective, positions)

        return return_data

    def evaluate_ways_board(self):
        """Populate win-data (ways count already includes split ways), apply the
        WIN multiplier, record wins and transmit the win events."""
        data = self._tr_ways_data()

        wm = max(1, int(getattr(self, "win_multiplier", 1) or 1))
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
