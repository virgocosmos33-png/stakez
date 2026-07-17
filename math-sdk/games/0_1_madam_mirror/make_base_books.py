"""Export a varied sample of real base-game books to the ways app Storybook.

Replaces the sample game's base_books.ts (which still referenced H5/M symbols
from the old demo) with books produced by the Madam Mirror math.

Run after run.py / test_quick.py has produced library/books/books_base.json:
    ../../env/Scripts/python.exe make_base_books.py
"""

import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS_PATH = os.path.join(HERE, "library", "books", "books_base.json")
OUT_PATH = os.path.abspath(
    os.path.join(
        HERE,
        "..", "..", "..",
        "web-sdk", "apps", "ways", "src", "stories", "data", "base_books.ts",
    )
)

SAMPLE_SIZE = 40

if __name__ == "__main__":
    with open(BOOKS_PATH, encoding="utf-8") as f:
        books = json.load(f)

    def has_event(book, ev_type):
        return any(ev["type"] == ev_type for ev in book["events"])

    rng = random.Random(7)
    zeros = [b for b in books if b["payoutMultiplier"] == 0]
    wins = [b for b in books if 0 < b["payoutMultiplier"] <= 2000]
    big_wins = [b for b in books if b["payoutMultiplier"] > 2000]
    mirrors = [b for b in books if has_event(b, "mirrorBurst")]
    bonuses = [b for b in books if has_event(b, "freeSpinTrigger")]

    picked = []
    picked += rng.sample(zeros, min(10, len(zeros)))
    picked += rng.sample(wins, min(15, len(wins)))
    picked += rng.sample(big_wins, min(5, len(big_wins)))
    picked += rng.sample(mirrors, min(6, len(mirrors)))
    picked += rng.sample(bonuses, min(4, len(bonuses)))

    # de-dup by id, cap the sample
    seen = set()
    unique = []
    for book in picked:
        if book["id"] not in seen:
            seen.add(book["id"])
            unique.append(book)
    unique = unique[:SAMPLE_SIZE]
    rng.shuffle(unique)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("export default ")
        json.dump(unique, f, indent=1)
        f.write(";\n")

    print(
        f"wrote {len(unique)} books "
        f"({sum(has_event(b, 'mirrorBurst') for b in unique)} with mirrors, "
        f"{sum(has_event(b, 'freeSpinTrigger') for b in unique)} with bonuses) -> {OUT_PATH}"
    )

    # bonus_books.ts: a mix of the three buyable bonus levels
    bonus_out = os.path.join(os.path.dirname(OUT_PATH), "bonus_books.ts")
    bonus_sample = []
    for mode in ("bonus1", "bonus2", "bonus3"):
        with open(os.path.join(HERE, "library", "books", f"books_{mode}.json"), encoding="utf-8") as f:
            mode_books = json.load(f)
        bonus_sample += rng.sample(mode_books, min(5, len(mode_books)))
    rng.shuffle(bonus_sample)

    with open(bonus_out, "w", encoding="utf-8") as f:
        f.write("export default ")
        json.dump(bonus_sample, f, indent=1)
        f.write(";\n")
    print(f"wrote {len(bonus_sample)} bonus books -> {bonus_out}")
