"""Extract curated REAL books that showcase each Wild Reel case for Storybook.

Pulls resolving books straight from the freshly built publish_files so the FE
stories play the exact same events the RGS would send. Writes:
  web-sdk/apps/white-room/src/stories/data/wild_reel_books.ts
"""

from __future__ import annotations

import io
import json
import os

import zstandard

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "library", "publish_files")
OUT = os.path.abspath(
    os.path.join(HERE, "..", "..", "..", "web-sdk", "apps", "white-room", "src", "stories", "data")
)


def iter_books(mode: str, limit: int = 60000):
    path = os.path.join(PUB, f"books_{mode}.jsonl.zst")
    dctx = zstandard.ZstdDecompressor()
    with open(path, "rb") as f:
        for i, line in enumerate(io.TextIOWrapper(dctx.stream_reader(f), encoding="utf-8")):
            if i >= limit:
                break
            if '"wildReel"' not in line:
                continue
            yield json.loads(line)


def wild_reel_events(book):
    return [e for e in book["events"] if e.get("type") == "wildReel"]


def has_win_after_wild(book):
    """True if a winInfo with totalWin>0 follows the first wildReel event."""
    seen = False
    for e in book["events"]:
        if e.get("type") == "wildReel":
            seen = True
        if seen and e.get("type") == "winInfo" and e.get("totalWin", 0) > 0:
            return True
    return False


def base_reels(book):
    """Distinct middle reels grown by the FIRST wildReel event of a base book."""
    wr = wild_reel_events(book)
    return {r["reel"] for r in wr[0]["reels"]} if wr else set()


def max_mult(book):
    m = 0
    for e in wild_reel_events(book):
        for r in e["reels"]:
            for c in r["cells"]:
                m = max(m, c["multiplier"])
    return m


def is_clean_base(book):
    """Single base spin that resolves on its own - NO bonus detour so the
    Storybook action finishes immediately and the reel-grow reads clearly."""
    if book.get("criteria") != "basegame":
        return False
    types = {e.get("type") for e in book["events"]}
    if "freeSpinTrigger" in types:
        return False
    # exactly one reveal (one spin) keeps the showcase short and legible
    return sum(1 for e in book["events"] if e.get("type") == "reveal") == 1


def pick():
    """Choose one representative CLEAN base book per showcase category."""
    picks: dict[str, dict] = {}
    for book in iter_books("base"):
        if book["payoutMultiplier"] / 100 >= 30000:
            continue  # skip wincap-clamped books
        if not is_clean_base(book):
            continue
        wr = wild_reel_events(book)
        if not wr:
            continue
        reels = base_reels(book)
        win = has_win_after_wild(book)
        n = len(wr[0]["reels"])

        # single reel 1 (3 -> 4, one wild) that resolves into a win
        if reels == {1} and win:
            prev = picks.get("single_reel1")
            if prev is None or book["payoutMultiplier"] > prev["payoutMultiplier"]:
                picks["single_reel1"] = book
        # single reel 2 (2 -> 4, two wilds), prefer a chunky multiplier + win
        if reels == {2} and win and max_mult(book) >= 2:
            prev = picks.get("single_reel2")
            if prev is None or max_mult(book) > max_mult(prev):
                picks["single_reel2"] = book
        # two middle reels growing together, resolving into a win
        if n == 2 and win:
            prev = picks.get("double_reel")
            if prev is None or book["payoutMultiplier"] > prev["payoutMultiplier"]:
                picks["double_reel"] = book
        # all three middle reels (the 7-wide "best case")
        if n == 3:
            prev = picks.get("triple_reel")
            if prev is None or book["payoutMultiplier"] > prev["payoutMultiplier"]:
                picks["triple_reel"] = book
        # best-paying CLEAN base wild-reel book
        if win:
            prev = picks.get("big_win")
            if prev is None or book["payoutMultiplier"] > prev["payoutMultiplier"]:
                picks["big_win"] = book
    return picks


def slim(book):
    """Keep only the fields the FE needs (id, payoutMultiplier, events)."""
    return {
        "id": book["id"],
        "payoutMultiplier": book.get("payoutMultiplier", 0),
        "events": book["events"],
    }


def slice_one_spin(book, wild_index):
    """Extract the single spin around events[wild_index] as a clean, self-
    resolving BASE book: reveal -> wildReel -> winInfo -> setTotalWin/finalWin.
    Lets us showcase a rare (e.g. 3-reel) Wild Reel without the bonus detour."""
    events = book["events"]
    # find the reveal that owns this spin
    start = wild_index
    while start > 0 and events[start]["type"] != "reveal":
        start -= 1
    end = wild_index + 1
    while end < len(events) and events[end]["type"] != "reveal":
        end += 1
    spin = [dict(e) for e in events[start:end]]
    spin[0] = dict(spin[0], gameType="basegame")
    # the win total for a clean finish
    total = 0
    for e in spin:
        if e.get("type") == "winInfo":
            total = e.get("totalWin", 0)
    # drop bonus / free-spin bookkeeping so the sliced spin plays as a clean
    # base showcase (no CONTINUE banner, no free-spin counter detour)
    _DROP = {
        "updateFreeSpin",
        "setTotalWin",
        "freeSpinTrigger",
        "freeSpinRetrigger",
        "bonusLevel",
        "freeSpinEnd",
        "createBonusSnapshot",
    }
    spin = [e for e in spin if e.get("type") not in _DROP]
    spin += [
        {"type": "setTotalWin", "amount": total},
        {"type": "finalWin", "amount": total},
    ]
    for i, e in enumerate(spin):
        e["index"] = i
    return {"id": book["id"], "payoutMultiplier": total, "events": spin}


def find_triple_spin():
    """First spin (any mode) whose wildReel grows all three middle reels."""
    for mode in ("base", "bonus", "feature"):
        try:
            for book in iter_books(mode):
                for i, e in enumerate(book["events"]):
                    if e.get("type") == "wildReel" and len(e["reels"]) == 3:
                        return slice_one_spin(book, i)
        except FileNotFoundError:
            continue
    return None


def main():
    picks = pick()
    # a real 3-reel Wild Reel in a single spin is too rare to sample cleanly in
    # base; slice one out of any mode so the "7-wide" case still showcases.
    if "triple_reel" not in picks:
        triple = find_triple_spin()
        if triple is not None:
            picks["triple_reel"] = triple
    order = ["single_reel1", "single_reel2", "double_reel", "triple_reel"]
    exports = {k: picks[k] for k in order if k in picks}

    os.makedirs(OUT, exist_ok=True)
    ts_path = os.path.join(OUT, "wild_reel_books.ts")
    with open(ts_path, "w", encoding="utf-8") as f:
        f.write(
            "// GENERATED by math-sdk/games/0_2_the_white_room/make_showcase_books.py\n"
            "// Real Wild Reel books pulled from the build - each plays through the\n"
            "// live Game so the reel-grow + multiplier-wild resolution is exact.\n"
            "import type { BookEvent } from '../../game/typesBookEvent';\n\n"
            "type ShowcaseBook = { id: number; payoutMultiplier: number; events: BookEvent[] };\n\n"
        )
        for key in order:
            if key not in exports:
                continue
            name = {
                "single_reel1": "wildReelSingleReel1Book",
                "single_reel2": "wildReelSingleReel2Book",
                "double_reel": "wildReelDoubleBook",
                "triple_reel": "wildReelTripleBook",
                "big_win": "wildReelBigWinBook",
            }[key]
            f.write(
                f"export const {name}: ShowcaseBook =\n"
                f"\t{json.dumps(slim(exports[key]), indent=1)} as ShowcaseBook;\n\n"
            )
        names = [
            {
                "single_reel1": "wildReelSingleReel1Book",
                "single_reel2": "wildReelSingleReel2Book",
                "double_reel": "wildReelDoubleBook",
                "triple_reel": "wildReelTripleBook",
                "big_win": "wildReelBigWinBook",
            }[k]
            for k in order
            if k in exports
        ]
        f.write(f"export default [{', '.join(names)}];\n")

    summary = {
        k: {
            "id": exports[k]["id"],
            "payoutMultiplier": exports[k]["payoutMultiplier"],
            "reels": [
                (r["reel"], r["baseRows"], r["added"], [c["multiplier"] for c in r["cells"]])
                for e in wild_reel_events(exports[k])
                for r in e["reels"]
            ],
        }
        for k in order
        if k in exports
    }
    print(json.dumps({"out": ts_path, "picks": summary}, indent=2))
    missing = [k for k in order if k not in exports]
    if missing:
        print("WARN missing categories:", missing)


if __name__ == "__main__":
    main()
