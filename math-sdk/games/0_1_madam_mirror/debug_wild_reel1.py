"""Repro: a wild on reel 1 (e.g. from the Madam's Eye conversion) must open
every paying symbol's ways - the stock engine only seeds symbols physically
present on reel 1, so wild-heavy eye boards pay nothing.

Board (5x4, rows top-down), W = wild:
  reel1: W  L5 L5 L5
  reel2: H1 L4 L4 L4
  reel3: H1 L3 L3 L3
  reel4: L2 L2 L2 L2
  reel5: L1 L1 L1 L1

Expected: H1 3-of-a-kind through the reel-1 wild (1*1*1 = 1 way, pay 1.0).
Buggy engine: H1 never evaluated (not on reel 1) -> only L5 pays.
"""

from game_config import GameConfig
from src.calculations.ways import Ways
from src.calculations.symbol import SymbolStorage

config = GameConfig()
all_names = {name for _, name in config.paytable} | {"W", "S", "HM", "ME"}
storage = SymbolStorage(config, sorted(all_names))

COLUMNS = [
    ["W", "L5", "L5", "L5"],
    ["H1", "L4", "L4", "L4"],
    ["H1", "L3", "L3", "L3"],
    ["L2", "L2", "L2", "L2"],
    ["L1", "L1", "L1", "L1"],
]
board = [[storage.create_symbol(name) for name in column] for column in COLUMNS]

data = Ways.get_ways_data(config, board)
print("wins:")
for w in data["wins"]:
    print(f"  {w['symbol']} x{w['kind']}  ways={w['meta']['ways']}  win={w['win']}")
print("totalWin:", data["totalWin"])

h1 = [w for w in data["wins"] if w["symbol"] == "H1"]
assert h1, "BUG REPRODUCED: H1 3-kind through the reel-1 wild was not paid"
assert h1[0]["kind"] == 3 and h1[0]["meta"]["ways"] == 1, h1
print("OK: reel-1 wild opens H1 ways")

# fullscreen-of-wilds sanity: an all-wild board must pay (every symbol's
# 5-kind through substitution), not zero
wild_board = [[storage.create_symbol("W") for _ in range(4)] for _ in range(5)]
wd = Ways.get_ways_data(config, wild_board)
print("all-wild board totalWin:", wd["totalWin"])
assert wd["totalWin"] > 0, "BUG REPRODUCED: full screen of wilds pays ZERO"
print("OK: full wild screen pays")
