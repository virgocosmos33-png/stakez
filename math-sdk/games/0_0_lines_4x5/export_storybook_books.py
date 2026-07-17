"""Convert generated books JSON into TS data files for the web-sdk lines app storybook."""

import json
import os

WEB_SDK_DATA = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "web-sdk", "apps", "lines", "src", "stories", "data"
)

EXPORTS = {
    "books_base.json": "base_books.ts",
    "books_bonus.json": "bonus_books.ts",
}

if __name__ == "__main__":
    for src, dst in EXPORTS.items():
        src_path = os.path.join(os.path.dirname(__file__), "library", "books", src)
        with open(src_path, encoding="utf-8") as f:
            books = json.load(f)
        dst_path = os.path.abspath(os.path.join(WEB_SDK_DATA, dst))
        with open(dst_path, "w", encoding="utf-8") as f:
            f.write("export default ")
            json.dump(books, f, indent=1)
            f.write(";\n")
        print(f"Wrote {len(books)} books -> {dst_path}")
