"""Board-level helpers for TOMBSTONE REBORN."""

from src.executables.executables import Executables


class GameCalculations(Executables):
    """Ways bookkeeping + symbol-class helpers used by the feature pipeline."""

    def is_premium(self, name: str) -> bool:
        return name in self.config.premium_symbols

    def is_low(self, name: str) -> bool:
        return name in self.config.low_symbols

    def is_wild(self, name: str) -> bool:
        return name == self.config.wild_symbol

    def cell_ways(self, sym) -> int:
        """How many ways a single cell contributes (its stamped multiplier, or 1)."""
        if sym.check_attribute("multiplier"):
            val = sym.get_attribute("multiplier")
            if isinstance(val, int) and val > 0:
                return val
        return 1

    def reel_ways(self, reel: int) -> int:
        """Sum of per-cell ways contributions on a reel."""
        return sum(self.cell_ways(sym) for sym in self.board[reel])

    def count_board_ways(self) -> int:
        """Total ways on the current board: product of per-reel ways sums."""
        total = 1
        for reel in range(len(self.board)):
            total *= max(1, self.reel_ways(reel))
        return total

    def add_cell_ways(self, reel: int, row: int, factor: int) -> int:
        """Add `factor` ways to a cell (capped), return the new per-cell mult."""
        return self.set_cell_ways(reel, row, self.cell_ways(self.board[reel][row]) + factor)

    def mul_cell_ways(self, reel: int, row: int, factor: int) -> int:
        """Multiply a cell's ways (capped), return the new per-cell mult."""
        return self.set_cell_ways(reel, row, self.cell_ways(self.board[reel][row]) * max(1, int(factor)))

    def set_cell_ways(self, reel: int, row: int, value: int) -> int:
        """SET a cell's ways multiplier (capped), return the stamped value."""
        cap = self.config.split_config["cell_cap"]
        new_val = min(max(1, int(value)), cap)
        self.board[reel][row].assign_attribute({"multiplier": new_val})
        return new_val

    def replace_keep_ways(self, reel: int, row: int, name: str):
        """Swap the face, keep any ways already stamped on the cell."""
        ways = self.cell_ways(self.board[reel][row])
        self.board[reel][row] = self.create_symbol(name)
        if ways > 1:
            self.board[reel][row].assign_attribute({"multiplier": ways})
        return self.board[reel][row]
