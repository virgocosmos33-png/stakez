"""Curate SHOWCASE books for TOMBSTONE REBORN.

There is no frontend Storybook app for this game yet, so this instead builds a
data fixture the future Storybook can load: one representative book per feature
(the first clean example found), one per bonus mode, and a guaranteed MAX WIN.

Reads the already-generated library books (run run_local.py / run_super.py
first) and writes:
    library/books/books_showcase.json   - the selected books, in showcase order
    library/books/showcase_index.json    - {label: {mode, sourceId, payoutX, ...}}

    ../../env/Scripts/python.exe make_showcase_books.py
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS = os.path.join(HERE, "library", "books")

MODES = ["base", "bonus_small", "bonus_super", "freespins", "superspins"]

# The 99,999x cap. A feature story must stay BELOW this: the selector takes the
# first library book whose predicate matches, so any unbounded `p > 0` predicate
# happily picked a wincap book and then presented BOOT HILL / MAX WIN instead of
# the feature it was named after. That made small_bonus_win, base_special,
# dig_up and super_split four copies of the max_win presentation.
WINCAP_X = 99999
# headroom under the cap, so a near-cap book can't sneak in either
FEATURE_MAX_X = 90000


def feature(*names, lo=0.01, hi=FEATURE_MAX_X, any_of=False):
    """Predicate: the book contains the named event(s) and pays inside a band.

    Bounding the top end is what keeps a feature story representative of its
    mechanic rather than of the win cap.
    """
    def check(types, payout):
        if any_of:
            if not any(n in types for n in names):
                return False
        elif not all(n in types for n in names):
            return False
        return lo <= payout < hi

    return check


# label -> (mode preference order, predicate on the set of event types)
WANTS = [
    ("base_dead",      ["base"],        lambda t, p: p == 0),
    ("base_special",   ["base"],        feature("split", "gunsmoke", "nudgeWays", any_of=True)),
    ("gunsmoke",       ["bonus_small", "bonus_super"], feature("gunsmoke")),
    ("split",          ["bonus_small", "bonus_super"], feature("split")),
    ("nudge_ways",     ["bonus_small", "bonus_super"], feature("nudgeWays")),
    ("tombstone",      ["bonus_small"], feature("tombstone")),
    ("bounty",         ["bonus_super", "bonus_small"], feature("bounty")),
    ("shooter",        ["bonus_super", "superspins"], feature("shooter")),
    ("super_split",    ["bonus_super"], feature("superSplit")),
    # A genuinely small win. This used to be an unbounded `p >= 200`, which kept
    # resolving to a 99,999x wincap book — the same presentation as max_win, so
    # the low end of the win ladder could never be verified from the showcase.
    # 25x..50x is the BOUNTY band, the lowest TITLED celebration tier in
    # web-sdk/apps/tombstone-reborn/src/game/winCelebrationMap.ts.
    ("small_bonus_win", ["bonus_small"], lambda t, p: 25 <= p < 50),
    ("super_bonus_win", ["bonus_super"], lambda t, p: 2000 <= p < FEATURE_MAX_X),
    # BONUS ROUNDS: a natural base trigger, a bought small round with a decent
    # win, the 1-in-100 mid-round UPGRADE, and a bought big round
    ("natural_trigger", ["base"],       feature("freeSpinTrigger", lo=1)),
    ("small_round",    ["freespins"],   feature("freeSpinTrigger", lo=100, hi=2000)),
    ("bonus_upgrade",  ["freespins"],   feature("bonusUpgrade")),
    ("big_round",      ["superspins"],  feature("freeSpinTrigger", lo=2000, hi=FEATURE_MAX_X)),
    ("max_win",        ["bonus_super", "bonus_small", "base"], lambda t, p: p >= WINCAP_X),
]


def iter_books(mode):
    """STREAM a mode's books one at a time: the uncompressed library file when
    present, otherwise the compressed publish file (what run.py writes now).

    Streaming matters: base alone is 1M books / multi-GB decompressed, and
    loading that in one shot ground the machine into swap. A book is yielded,
    inspected and dropped."""
    path = os.path.join(BOOKS, f"books_{mode}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            yield from json.load(fh)
        return
    zst_path = os.path.join(HERE, "library", "publish_files", f"books_{mode}.jsonl.zst")
    if not os.path.exists(zst_path):
        return
    import io

    import zstandard as zstd

    with open(zst_path, "rb") as fh:
        reader = zstd.ZstdDecompressor().stream_reader(fh)
        for line in io.TextIOWrapper(reader, encoding="utf-8"):
            line = line.strip()
            if line:
                yield json.loads(line)


def main():
    # One streaming pass per mode: every WANT that prefers this mode keeps the
    # FIRST matching book (per mode), then the preference order picks between
    # modes afterwards. Same selections as the old all-in-memory scan.
    found = {}  # (label, mode) -> (book, payout, types)
    for mode in MODES:
        wants_here = [(lbl, pred) for lbl, pref, pred in WANTS if mode in pref]
        open_wants = {lbl: pred for lbl, pred in wants_here}
        count = 0
        for b in iter_books(mode):
            count += 1
            types = {e["type"] for e in b["events"]}
            payout = b["payoutMultiplier"] / 100.0
            for lbl in list(open_wants):
                if open_wants[lbl](types, payout):
                    found[(lbl, mode)] = (b, payout, types)
                    del open_wants[lbl]
            if not open_wants:
                break
        print(f"  scanned {count:>7} books for {mode} "
              f"({len(wants_here) - len(open_wants)}/{len(wants_here)} wants)")

    showcase = []
    index = {}
    for label, mode_pref, _pred in WANTS:
        chosen = None
        for mode in mode_pref:
            if (label, mode) in found:
                b, payout, types = found[(label, mode)]
                chosen = (mode, b, payout, types)
                break
        if not chosen:
            print(f"  [skip] no book found for {label}")
            continue
        mode, b, payout, types = chosen
        pos = len(showcase) + 1  # 1-based index within the showcase file
        clone = json.loads(json.dumps(b))
        clone["id"] = pos
        showcase.append(clone)
        feats = [t for t in (
            "gunsmoke", "split", "nudgeWays", "tombstone",
            "bounty", "shooter", "superSplit",
        ) if t in types]
        index[label] = {
            "showcaseId": pos,
            "mode": mode,
            "sourceId": b["id"],
            "payoutX": round(payout, 2),
            "features": feats,
        }
        print(f"  [{pos:>2}] {label:16s} {mode:12s} payout={payout:>10.2f}x  {feats}")

    with open(os.path.join(BOOKS, "books_showcase.json"), "w", encoding="utf-8") as fh:
        json.dump(showcase, fh)
    with open(os.path.join(BOOKS, "showcase_index.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, indent=2)

    # Emit an embeddable data file for the standalone draft viewer (no build /
    # no fetch needed - the HTML just includes this script).
    id_to_label = {v["showcaseId"]: k for k, v in index.items()}
    preview = []
    for b in showcase:
        label = id_to_label.get(b["id"], f"book_{b['id']}")
        meta = index.get(label, {})
        preview.append({
            "label": label,
            "mode": meta.get("mode"),
            "payoutX": meta.get("payoutX"),
            "events": b["events"],
        })
    app_src = os.path.join(
        HERE, "..", "..", "..", "web-sdk", "apps", "tombstone-reborn", "src"
    )
    os.makedirs(app_src, exist_ok=True)
    with open(os.path.join(app_src, "showcase.generated.json"), "w", encoding="utf-8") as fh:
        json.dump(preview, fh, indent=1)

    print("\nDONE. Wrote", len(showcase), "showcase books + src/showcase.generated.json")


if __name__ == "__main__":
    main()
