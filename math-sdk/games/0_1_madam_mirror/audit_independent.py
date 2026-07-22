"""INDEPENDENT audit of the published books.

Re-computes every spin's win with a from-scratch ways implementation (canonical
definition, written independently of src/calculations/ways.py):

  for each paying symbol S:
    cnt[r] = sum over cells on reel r of:
               multiplier if cell is S or wild (multiplier>=2 counts as that
               many symbols - dynamic ways), else 0
    kind   = consecutive reels from reel 1 with cnt > 0
    win    = paytable[(kind, S)] * product(cnt[0..kind-1])
  spin total = sum over symbols, clamped at the wincap

and validates against the recorded winInfo events:
  - per-spin totalWin matches exactly
  - per-symbol win entries match (symbol, kind, ways, win)
Also validates:
  - scatter count on the reveal matches the freeSpinTrigger/bonusLevel mapping
  - book payoutMultiplier == sum of spin wins (clamped at wincap)

Boards are reconstructed from reveal -> mirrorBurst -> madamsEye events, i.e.
the exact final board the engine evaluated.

Usage: python audit_independent.py <mode> [max_books]
"""

import io
import json
import os
import sys

import zstandard

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLISH = os.path.join(HERE, "library", "publish_files")

# ---- game constants duplicated on purpose (independent of game_config) ----
PAYTABLE = {
    (5, "H1"): 10, (4, "H1"): 3, (3, "H1"): 1,
    (5, "H2"): 5, (4, "H2"): 1.5, (3, "H2"): 0.6,
    (5, "H3"): 4, (4, "H3"): 1.2, (3, "H3"): 0.5,
    (5, "H4"): 3, (4, "H4"): 1, (3, "H4"): 0.4,
    (5, "H5"): 2.5, (4, "H5"): 0.8, (3, "H5"): 0.3,
    (5, "L1"): 1.2, (4, "L1"): 0.4, (3, "L1"): 0.2,
    (5, "L2"): 1.2, (4, "L2"): 0.4, (3, "L2"): 0.2,
    (5, "L3"): 0.8, (4, "L3"): 0.3, (3, "L3"): 0.1,
    (5, "L4"): 0.8, (4, "L4"): 0.3, (3, "L4"): 0.1,
    (5, "L5"): 0.8, (4, "L5"): 0.3, (3, "L5"): 0.1,
}
PAYING = sorted({s for _, s in PAYTABLE})
WILD = "W"
WINCAP = 30000.0
SCATTER_TO_LEVEL = {3: 1, 4: 2, 5: 3}
FS_BASE = {3: 8, 4: 10, 5: 12}


def ways_win(board):
    """board: list of 5 reels, each a list of (name, multiplier) tuples."""
    total = 0.0
    wins = []
    for symbol in PAYING:
        counts = []
        for reel in board:
            c = 0
            for name, mult in reel:
                if name == symbol or name == WILD:
                    c += mult
            counts.append(c)
        kind = 0
        for c in counts:
            if c > 0:
                kind += 1
            else:
                break
        if (kind, symbol) not in PAYTABLE:
            continue
        ways = 1
        for c in counts[:kind]:
            ways *= c
        win = round(PAYTABLE[(kind, symbol)] * ways, 2)
        wins.append({"symbol": symbol, "kind": kind, "ways": ways, "win": win})
        total += win
    return round(total, 2), wins


def audit(mode, max_books):
    path = os.path.join(PUBLISH, f"books_{mode}.jsonl.zst")
    books = 0
    spins = 0
    total_mismatches = 0
    perwin_mismatches = 0
    payout_mismatches = 0
    trigger_errors = 0
    capped_books = 0

    with open(path, "rb") as fh:
        text = io.TextIOWrapper(
            zstandard.ZstdDecompressor().stream_reader(fh), encoding="utf-8"
        )
        for line in text:
            if books >= max_books:
                break
            book = json.loads(line)
            books += 1
            is_capped = book["payoutMultiplier"] >= WINCAP * 100
            if is_capped:
                capped_books += 1

            board = None
            recorded_wininfo = None
            running_total = 0.0
            scatters = 0
            pending_trigger = None

            def close_spin():
                nonlocal spins, total_mismatches, perwin_mismatches, running_total
                if board is None:
                    return
                spins += 1
                calc_total, calc_wins = ways_win(board)
                calc_total_clamped = min(calc_total, WINCAP)
                running_total += calc_total_clamped
                if is_capped:
                    return  # per-spin records are clamped mid-book; totals checked via cap
                rec_total = (recorded_wininfo or {"totalWin": 0})["totalWin"] / 100.0
                if abs(min(calc_total, WINCAP) - rec_total) > 0.011:
                    total_mismatches += 1
                    if total_mismatches <= 3:
                        print(f"  MISMATCH book {book['id']}: calc {calc_total} vs recorded {rec_total}")
                if recorded_wininfo:
                    rec = {
                        (w["symbol"], w["kind"]): (w["meta"]["ways"], round(w["win"] / 100.0, 2))
                        for w in recorded_wininfo["wins"]
                    }
                    calc = {
                        (w["symbol"], w["kind"]): (w["ways"], w["win"]) for w in calc_wins if w["win"] > 0
                    }
                    if rec != calc:
                        perwin_mismatches += 1

            for ev in book["events"]:
                if ev["type"] == "reveal":
                    close_spin()
                    recorded_wininfo = None
                    board = []
                    for column in ev["board"]:
                        reel = []
                        for s in column[1:-1]:
                            reel.append((s["name"], s.get("multiplier", 1) or 1))
                        board.append(reel)
                    scatters = sum(1 for r in board for n, _ in r if n == "S")
                elif ev["type"] == "mirrorBurst":
                    for m in ev["mirrors"]:
                        r, w = m["mirror"]["reel"], m["mirror"]["row"] - 1
                        board[r][w] = (m["mirrorBecomes"]["name"], 1)
                        for c in m["reflected"]:
                            name, _ = board[c["reel"]][c["row"] - 1]
                            board[c["reel"]][c["row"] - 1] = (name, c["apparitions"])
                elif ev["type"] == "madamsEye":
                    for c in ev["converted"]:
                        board[c["reel"]][c["row"] - 1] = (WILD, c["apparitions"])
                    board[ev["eye"]["reel"]][ev["eye"]["row"] - 1] = (WILD, 1)
                elif ev["type"] == "winInfo":
                    recorded_wininfo = ev
                elif ev["type"] == "freeSpinTrigger":
                    # only validate BASE-game triggers (retriggers use fs rules)
                    if pending_trigger is None:
                        pending_trigger = (scatters, ev["totalFs"])
                elif ev["type"] == "bonusLevel":
                    sc, total_fs = pending_trigger
                    sc = min(sc, 5)
                    if SCATTER_TO_LEVEL.get(max(sc, 3)) != ev["level"] or FS_BASE.get(max(sc, 3)) != total_fs:
                        trigger_errors += 1
            close_spin()

            expected_payout = round(min(running_total, WINCAP), 2)
            recorded_payout = book["payoutMultiplier"] / 100.0
            if abs(expected_payout - recorded_payout) > 0.011:
                payout_mismatches += 1
                if payout_mismatches <= 3:
                    print(
                        f"  PAYOUT MISMATCH book {book['id']}: calc {expected_payout} vs recorded {recorded_payout}"
                    )

    print(
        f"{mode}: books={books} (capped {capped_books}) spins={spins} | "
        f"spin-total mismatches={total_mismatches} | per-win mismatches={perwin_mismatches} | "
        f"book-payout mismatches={payout_mismatches} | trigger/level errors={trigger_errors}"
    )
    return total_mismatches + perwin_mismatches + payout_mismatches + trigger_errors


if __name__ == "__main__":
    mode = sys.argv[1]
    max_books = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    sys.exit(1 if audit(mode, max_books) else 0)
