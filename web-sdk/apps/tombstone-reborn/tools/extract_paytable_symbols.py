"""Crop pay-table PNGs for the HTML info menu.

ModalPayTable loads `assets/paytable/<key>.png` for every pay row and special.
Paying faces come out of the current symbolsStatic atlas (v25); feature cards
are copied from the board sprites already in static/assets/sprites/mirror/.

Run:  python tools/extract_paytable_symbols.py
"""

from __future__ import annotations

import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
STATIC = os.path.join(APP, "static", "assets")
SRC = os.path.join(APP, "assets-src", "assets")
ATLAS_DIR = os.path.join(STATIC, "sprites", "symbolsStatic")
MIRROR = os.path.join(STATIC, "sprites", "mirror")
OUT_DIRS = (
	os.path.join(STATIC, "paytable"),
	os.path.join(SRC, "paytable"),
)

ATLAS_JSON = "symbolsStatic.v25.json"
ATLAS_IMAGE = "symbolsStatic.v25.webp"

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
}

FEATURE_COPIES = {
	"w": os.path.join(MIRROR, "wr_wild.png"),
	"s": os.path.join(MIRROR, "tr_scatter.png"),
	"su": os.path.join(MIRROR, "tr_scatter_super.png"),
	"split": os.path.join(MIRROR, "tr_sp.png"),
	"gunsmoke": os.path.join(MIRROR, "tr_gs.png"),
	"nudge": os.path.join(MIRROR, "tr_nw.png"),
	"shooter": os.path.join(MIRROR, "tr_sh.png"),
	"supersplit": os.path.join(MIRROR, "tr_ss.png"),
}


def write_png(img: Image.Image, dest_name: str) -> None:
	for out_dir in OUT_DIRS:
		os.makedirs(out_dir, exist_ok=True)
		path = os.path.join(out_dir, f"{dest_name}.png")
		img.save(path)
	print(f"wrote {dest_name}.png ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
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
		write_png(crop, out_name)

	for out_name, src in FEATURE_COPIES.items():
		if not os.path.isfile(src):
			print(f"! missing feature art {src}")
			continue
		write_png(Image.open(src).convert("RGBA"), out_name)

	print(f"done -> {OUT_DIRS[0]}")
