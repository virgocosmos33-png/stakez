"""Crop pay-table PNGs for the HTML info menu.

ModalPayTable loads `assets/paytable/<key>.png` for every pay row and special.
Paying faces come out of the v13 atlas; feature cards are copied from the
board sprites already in static/assets/sprites/mirror/.

Run:  python tools/extract_paytable_symbols.py
"""

from __future__ import annotations

import json
import os
import shutil

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.normpath(os.path.join(HERE, "..", "static", "assets"))
ATLAS_DIR = os.path.join(STATIC, "sprites", "symbolsStatic")
MIRROR = os.path.join(STATIC, "sprites", "mirror")
TOMBSTONE = os.path.join(STATIC, "sprites", "tombstone")
OUT_DIR = os.path.join(STATIC, "paytable")

ATLAS_JSON = "symbolsStatic.v13.json"
ATLAS_IMAGE = "symbolsStatic.v13.webp"

WANTED = {
	"h1.webp": "h1",
	"h2.webp": "h2",
	"h3.webp": "h3",
	"h4.webp": "h4",
	"h5.webp": "h5",
	"l1.webp": "l1",
	"l2.webp": "l2",
	"l3.webp": "l3",
	"l4.webp": "l4",
	"l5.webp": "l5",
	"w.png": "w",
	"s.png": "s",
}

FEATURE_COPIES = {
	"split": os.path.join(MIRROR, "tr_sp.png"),
	"gunsmoke": os.path.join(MIRROR, "tr_gs.png"),
	"tombstone": os.path.join(MIRROR, "tr_ts.png"),
	"nudge": os.path.join(MIRROR, "tr_nw.png"),
	"shooter": os.path.join(MIRROR, "tr_sh.png"),
	"supersplit": os.path.join(MIRROR, "tr_ss.png"),
	"w": os.path.join(MIRROR, "wr_wild.png"),
	"s": os.path.join(MIRROR, "tr_scatter.png"),
	"bounty": os.path.join(TOMBSTONE, "lane_gold_bounty.webp"),
}


def write_png(src: str, dest_name: str) -> None:
	img = Image.open(src).convert("RGBA")
	img.save(os.path.join(OUT_DIR, f"{dest_name}.png"))
	print(f"wrote {dest_name}.png ({img.size[0]}x{img.size[1]}) from {os.path.basename(src)}")


if __name__ == "__main__":
	os.makedirs(OUT_DIR, exist_ok=True)
	with open(os.path.join(ATLAS_DIR, ATLAS_JSON), encoding="utf-8") as handle:
		atlas = json.load(handle)
	sheet = Image.open(os.path.join(ATLAS_DIR, ATLAS_IMAGE)).convert("RGBA")

	for frame_name, out_name in WANTED.items():
		entry = atlas["frames"].get(frame_name)
		if not entry:
			print(f"! missing atlas frame {frame_name}")
			continue
		r = entry["frame"]
		crop = sheet.crop((r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]))
		crop.save(os.path.join(OUT_DIR, f"{out_name}.png"))
		print(f"wrote {out_name}.png ({r['w']}x{r['h']}) from atlas")

	for out_name, src in FEATURE_COPIES.items():
		if not os.path.isfile(src):
			print(f"! missing feature art {src}")
			continue
		write_png(src, out_name)

	print(f"done -> {OUT_DIR}")
