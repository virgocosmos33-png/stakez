"""Quantify the reel-1-wild ways bug against the published books.

For every spin in the books, reconstruct the final evaluated board (reveal ->
mirrorBurst mutations -> madamsEye conversion) and re-evaluate it with the
FIXED ways engine. Compare with the winInfo total the book recorded (produced
by the old engine). Spins where fixed > recorded are wins the old math missed.

Sanity: spins without a wild on reel 1 must match exactly (delta 0).
"""

import io
import json
import os
import sys

import zstandard

from game_config import GameConfig
from src.calculations.ways import Ways
from src.calculations.symbol import SymbolStorage

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLISH = os.path.join(HERE, "library", "publish_files")

MODES = sys.argv[1:] or ["bonus1", "bonus2", "bonus3"]
MAX_BOOKS = 20_000

config = GameConfig()
all_names = {name for _, name in config.paytable} | {"W", "S", "HM", "ME"}
storage = SymbolStorage(config, sorted(all_names))


def make_board(reveal):
    """Padded reveal -> 5x4 window of Symbols (rows 1..4)."""
    board = []
    for column in reveal["board"]:
        col = []
        for sym_json in column[1:-1]:
            sym = storage.create_symbol(sym_json["name"])
            if sym_json.get("multiplier", 1) > 1:
                sym.assign_attribute({"multiplier": sym_json["multiplier"]})
            col.append(sym)
        board.append(col)
    return board


def evaluate(board):
    return Ways.get_ways_data(config, board)["totalWin"]


def scan(mode):
    path = os.path.join(PUBLISH, f"books_{mode}.jsonl.zst")
    books_seen = 0
    spins = 0
    mismatch_unaffected = 0
    affected = 0          # spins with >=1 wild on reel 1 at evaluation time
    missed = 0            # affected spins where fixed engine pays MORE
    duds = 0              # affected spins that paid ZERO but should pay
    missed_total = 0.0    # sum of missed pay (x bet)
    worst = 0.0

    with open(path, "rb") as fh:
        reader = zstandard.ZstdDecompressor().stream_reader(fh)
        text = io.TextIOWrapper(reader, encoding="utf-8")
        for line in text:
            if books_seen >= MAX_BOOKS:
                break
            book = json.loads(line)
            books_seen += 1
            if book["payoutMultiplier"] >= config.wincap * 100:
                continue  # capped books: recorded wins are clamped

            board = None
            recorded = 0

            def close_spin():
                nonlocal spins, affected, missed, duds, missed_total, worst, mismatch_unaffected
                if board is None:
                    return
                spins += 1
                wild_reel1 = any(s.name == "W" for s in board[0])
                fixed = round(evaluate(board), 2)
                rec = round(recorded / 100.0, 2)
                delta = round(fixed - rec, 2)
                if wild_reel1:
                    affected += 1
                    if delta > 0.005:
                        missed += 1
                        missed_total += delta
                        worst = max(worst, delta)
                        if rec == 0:
                            duds += 1
                else:
                    if abs(delta) > 0.005:
                        mismatch_unaffected += 1

            for ev in book["events"]:
                if ev["type"] == "reveal":
                    close_spin()
                    board = make_board(ev)
                    recorded = 0
                elif ev["type"] == "mirrorBurst":
                    for m in ev["mirrors"]:
                        r, w = m["mirror"]["reel"], m["mirror"]["row"] - 1
                        board[r][w] = storage.create_symbol(m["mirrorBecomes"]["name"])
                        for c in m["reflected"]:
                            board[c["reel"]][c["row"] - 1].assign_attribute(
                                {"multiplier": c["apparitions"]}
                            )
                elif ev["type"] == "madamsEye":
                    for c in ev["converted"]:
                        wild = storage.create_symbol("W")
                        wild.assign_attribute({"multiplier": c["apparitions"]})
                        board[c["reel"]][c["row"] - 1] = wild
                    board[ev["eye"]["reel"]][ev["eye"]["row"] - 1] = storage.create_symbol("W")
                elif ev["type"] == "winInfo":
                    recorded = ev["totalWin"]
            close_spin()

    print(f"\n=== {mode} ({books_seen} books, {spins} spins, uncapped) ===")
    print(f"  sanity mismatches on unaffected spins: {mismatch_unaffected}")
    print(f"  spins with wild on reel 1:  {affected}")
    print(f"  ...underpaid by old engine: {missed}")
    print(f"  ...total ZERO-pay duds:     {duds}")
    if missed:
        print(f"  missed pay: total {missed_total:.1f}x, avg {missed_total / missed:.2f}x, worst {worst:.1f}x")


for m in MODES:
    scan(m)
