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

MODES = ["base", "bonus_small", "bonus_super"]

# label -> (mode preference order, predicate on the set of event types)
WANTS = [
    ("base_dead",      ["base"],        lambda t, p: p == 0),
    ("base_special",   ["base"],        lambda t, p: ("splitGang" in t or "gunsmoke" in t or "coffinOpen" in t) and p > 0),
    ("coffin_open",    ["bonus_small", "bonus_super"], lambda t, p: "coffinOpen" in t and p > 0),
    ("gunsmoke",       ["bonus_small", "bonus_super"], lambda t, p: "gunsmoke" in t and p > 0),
    ("split_gang",     ["bonus_small", "bonus_super"], lambda t, p: "splitGang" in t and p > 0),
    ("split_outlaws",  ["bonus_small", "bonus_super"], lambda t, p: "splitOutlaws" in t and p > 0),
    ("dig_up",         ["bonus_small"], lambda t, p: "digUp" in t and p > 0),
    ("bounty",         ["bonus_super", "bonus_small"], lambda t, p: "bounty" in t and p > 0),
    ("nudge",          ["bonus_super", "bonus_small"], lambda t, p: "nudge" in t and p > 0),
    ("super_split",    ["bonus_super"], lambda t, p: "superSplit" in t and p > 0),
    ("small_bonus_win", ["bonus_small"], lambda t, p: p >= 200),
    ("super_bonus_win", ["bonus_super"], lambda t, p: 2000 <= p < 90000),
    ("max_win",        ["bonus_super", "bonus_small", "base"], lambda t, p: p >= 99999),
]


def load(mode):
    path = os.path.join(BOOKS, f"books_{mode}.json")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    libs = {m: load(m) for m in MODES}
    for m in MODES:
        print(f"  loaded {len(libs[m]):>6} books for {m}")

    showcase = []
    index = {}
    for label, mode_pref, pred in WANTS:
        chosen = None
        for mode in mode_pref:
            for b in libs.get(mode, []):
                types = {e["type"] for e in b["events"]}
                payout = b["payoutMultiplier"] / 100.0
                if pred(types, payout):
                    chosen = (mode, b, payout, types)
                    break
            if chosen:
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
            "coffinOpen", "gunsmoke", "splitGang", "splitOutlaws", "digUp",
            "bounty", "nudge", "superSplit",
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
