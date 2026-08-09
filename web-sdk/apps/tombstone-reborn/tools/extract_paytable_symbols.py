"""Crop individual symbol PNGs out of the packed symbolsStatic atlas so the HTML
pay-table / info menu can show them with plain <img> tags.

Outputs to static/assets/paytable/<key>.png (trimmed transparent border kept).

Run:  python tools/extract_paytable_symbols.py
"""

import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ATLAS_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "symbolsStatic"))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "paytable"))

# atlas frame name -> output file name
WANTED = {
    "h1.webp": "h1", "h2.webp": "h2", "h3.webp": "h3", "h4.webp": "h4", "h5.webp": "h5",
    "l1.webp": "l1", "l2.webp": "l2", "l3.webp": "l3", "l4.webp": "l4", "l5.webp": "l5",
    "w.png": "w", "s.png": "s", "me.png": "me", "hm_intact.png": "hm",
}


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(ATLAS_DIR, "symbolsStatic.json"), encoding="utf-8") as f:
        atlas = json.load(f)
    sheet = Image.open(os.path.join(ATLAS_DIR, "symbolsStatic.webp")).convert("RGBA")

    for frame_name, out_name in WANTED.items():
        entry = atlas["frames"].get(frame_name)
        if not entry:
            print(f"! missing frame {frame_name}")
            continue
        r = entry["frame"]
        crop = sheet.crop((r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]))
        crop.save(os.path.join(OUT_DIR, f"{out_name}.png"))
        print(f"wrote {out_name}.png ({r['w']}x{r['h']})")

    print(f"done -> {OUT_DIR}")
