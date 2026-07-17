from src.executables.executables import Executables


class GameCalculations(Executables):
    """Board-level helpers for the xMirror mechanic.

    Apparition counts ride on the engine's `multiplier` symbol attribute:
    Ways.get_ways_data (multiplier_strategy="symbol") counts a symbol with
    multiplier=m as m symbols on its reel, which is exactly dynamic ways.
    """

    def count_board_ways(self) -> int:
        """Total possible ways of the current board: product of per-reel apparition sums."""
        total = 1
        for reel in self.board:
            reel_count = 0
            for sym in reel:
                if sym.check_attribute("multiplier"):
                    reel_count += sym.get_attribute("multiplier")
                else:
                    reel_count += 1
            total *= reel_count
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
