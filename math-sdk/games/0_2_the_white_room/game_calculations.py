from src.executables.executables import Executables
from src.wins.multiplier_strategy import apply_mult


class GameCalculations(Executables):
    """Board-level helpers for the xMirror mechanic.

    Apparition counts ride on the engine's `multiplier` symbol attribute:
    ways evaluation (multiplier_strategy="symbol") counts a symbol with
    multiplier=m as m symbols on its reel, which is exactly dynamic ways.

    Cell Seal expands place WILD (`W`) on the reel; face art stays on the
    cellSeal event. Evaluation must allow wild-on-reel-0 to start pays for
    any paying symbol (SDK Ways.get_ways_data only seeds from reel-0 names).
    """

    def reel_ways(self, reel: int) -> int:
        """How many ways ONE reel contributes: the sum of its cells' apparition
        counts, where a cell with a multiplier counts as that many symbols.

        This is the number a Wild Reel shows the player. A reel grown to its
        full four rows is worth at least 4 on its own, before any multiplier,
        which is why the feature reads as "x4" the moment it lands.
        """
        count = 0
        for sym in self.board[reel]:
            if sym.check_attribute("multiplier"):
                count += sym.get_attribute("multiplier")
            else:
                count += 1
        return count

    def count_board_ways(self) -> int:
        """Total possible ways of the current board: product of per-reel apparition sums."""
        total = 1
        for reel in range(len(self.board)):
            total *= self.reel_ways(reel)
        return total

    def get_neighbors(self, reel: int, row: int, diagonal: bool = False) -> list:
        """Adjacent board positions; diagonal=True gives the full 8-neighborhood
        (a mirror can reflect a block of up to 6 surrounding cells)."""
        neighbors = []
        for d_reel in (-1, 0, 1):
            for d_row in (-1, 0, 1):
                if d_reel == 0 and d_row == 0:
                    continue
                if not diagonal and d_reel != 0 and d_row != 0:
                    continue
                n_reel, n_row = reel + d_reel, row + d_row
                if 0 <= n_reel < self.config.num_reels and 0 <= n_row < self.config.num_rows[n_reel]:
                    neighbors.append((n_reel, n_row))
        return neighbors

    def get_ways_data(self):
        """Ways with wild substitution from reel 0 (Cell Seal expand-as-wild)."""
        return ways_data_wild_start(self.config, self.board)


def _cell_ways_count(sym, multiplier_key: str = "multiplier") -> int:
    if sym.check_attribute(multiplier_key):
        return int(sym.get_attribute(multiplier_key))
    return 1


def ways_data_wild_start(
    config,
    board,
    wild_key: str = "wild",
    global_multiplier: int = 1,
    multiplier_key: str = "multiplier",
    multiplier_strategy: str = "symbol",
):
    """Left-to-right ways: each reel counts matching symbol OR wild.

    Unlike SDK Ways.get_ways_data, wilds on reel 0 can start a pay for any
    paytable symbol (required for Cell Seal full-reel wilds).
    """
    assert multiplier_strategy in ["symbol", "board", "global"]
    return_data = {"totalWin": 0, "wins": []}
    wild_names = set(config.special_symbols.get(wild_key) or [])
    paying = sorted({sym for (_, sym) in config.paytable.keys() if sym not in wild_names})

    for symbol in paying:
        kind = 0
        ways = 1
        cumulative_sym_mult = 0
        positions = []
        board_mult_count = 0

        for reel, _ in enumerate(board):
            reel_sym_count = 0
            reel_positions = []
            for row, sym in enumerate(board[reel]):
                is_match = sym.name == symbol
                is_wild = sym.name in wild_names
                if not (is_match or is_wild):
                    continue
                c = _cell_ways_count(sym, multiplier_key)
                if multiplier_strategy == "symbol":
                    reel_sym_count += c
                    if is_wild and c > 1:
                        cumulative_sym_mult += c
                elif multiplier_strategy == "board":
                    reel_sym_count += 1
                    if c > 1:
                        board_mult_count += c
                        if is_wild:
                            cumulative_sym_mult += c
                else:
                    reel_sym_count += 1
                reel_positions.append({"reel": reel, "row": row})

            if reel_sym_count <= 0:
                break
            kind += 1
            ways *= reel_sym_count
            positions.extend(reel_positions)

        match multiplier_strategy:
            case "global":
                win_multiplier = global_multiplier
            case "board":
                win_multiplier = max(board_mult_count, 1)
            case "symbol":
                win_multiplier = 1

        if kind >= 3 and (kind, symbol) in config.paytable:
            win = round(config.paytable[kind, symbol] * ways, 2)
            win_amt, multiplier = apply_mult(
                board=board,
                strategy="global",
                win_amount=win,
                global_multiplier=win_multiplier,
            )
            if multiplier_strategy == "symbol":
                assert win_amt == win
            return_data["wins"].append(
                {
                    "symbol": symbol,
                    "kind": kind,
                    "win": win_amt,
                    "positions": positions,
                    "meta": {
                        "ways": ways,
                        "globalMult": multiplier,
                        "winWithoutMult": win,
                        "symbolMult": cumulative_sym_mult,
                    },
                }
            )
            return_data["totalWin"] += win_amt

    return return_data
