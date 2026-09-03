"""Install the TR2 coffin sheet as aligned cover + open interiors.

Crop, then scale UNIFORMLY. Canvas size comes from the wood hex
(cover + opened bone) — jewelry / gold contain-fit inside that box so
the plank stand cannot widen the live sprite.

Outputs
  assets/sprites/fx/fx_nudge_coffin_cover.png
  assets/sprites/fx/fx_nudge_coffin_open.png      bone (ways 2-3)
  assets/sprites/fx/fx_nudge_coffin_gold.png      gold (ways 4-6)
  assets/sprites/fx/fx_nudge_coffin_jewel.png     gold + jewelry (ways 7-9)
  static/assets/sprites/fx/ (same)
"""

from __future__ import annotations

import os
import shutil

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
RAW_DIR = os.path.join(APP, "assets-raw", "layer_nudge", "coffin_sheet")
SRC_DIR = os.path.join(
	os.path.expanduser("~"),
	"Desktop",
	"TR2 FInal symbopls sheet",
	"TR2 FInal symbopls sheet for TR2 Symbols",
	"new symbols",
	"coffin sheet",
	"coffin sheet",
)
SHARED_H = 1674
WOOD = (
	("coffin cover.png", "coffin_cover.png", "fx_nudge_coffin_cover.png"),
	("opened coffin.png", "opened_coffin.png", "fx_nudge_coffin_open.png"),
)
TIERS = (
	("gold skeleton.png", "gold_skeleton.png", "fx_nudge_coffin_gold.png"),
	("gold skeleton + jewlerry.png", "gold_skeleton_jewel.png", "fx_nudge_coffin_jewel.png"),
)
OUT_DIRS = [
	os.path.join(APP, "assets", "sprites", "fx"),
	os.path.join(APP, "static", "assets", "sprites", "fx"),
]


def crop_rgba(path: str) -> Image.Image:
	im = Image.open(path).convert("RGBA")
	mask = im.split()[-1].point(lambda a: 255 if a > 16 else 0)
	box = mask.getbbox()
	return im.crop(box) if box else im


def fit_height(im: Image.Image, height: int) -> Image.Image:
	scale = height / max(1, im.size[1])
	width = max(1, round(im.size[0] * scale))
	return im.resize((width, height), Image.Resampling.LANCZOS)


def fit_contain(im: Image.Image, box_w: int, box_h: int) -> Image.Image:
	scale = min(box_w / max(1, im.size[0]), box_h / max(1, im.size[1]))
	width = max(1, round(im.size[0] * scale))
	height = max(1, round(im.size[1] * scale))
	return im.resize((width, height), Image.Resampling.LANCZOS)


def paste_center(im: Image.Image, box_w: int, box_h: int) -> Image.Image:
	canvas = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
	canvas.paste(im, ((box_w - im.size[0]) // 2, (box_h - im.size[1]) // 2), im)
	return canvas


def main() -> None:
	all_src = [name for name, _, _ in (*WOOD, *TIERS)]
	missing = [name for name in all_src if not os.path.isfile(os.path.join(SRC_DIR, name))]
	if missing:
		raise SystemExit(f"missing {missing} in {SRC_DIR}")

	os.makedirs(RAW_DIR, exist_ok=True)
	wood: list[tuple[str, Image.Image]] = []
	for src_name, raw_name, out_name in WOOD:
		src = os.path.join(SRC_DIR, src_name)
		shutil.copy2(src, os.path.join(RAW_DIR, raw_name))
		wood.append((out_name, fit_height(crop_rgba(src), SHARED_H)))

	width = max(im.size[0] for _, im in wood)
	height = SHARED_H
	outs = [(name, paste_center(im, width, height)) for name, im in wood]

	for src_name, raw_name, out_name in TIERS:
		src = os.path.join(SRC_DIR, src_name)
		shutil.copy2(src, os.path.join(RAW_DIR, raw_name))
		fitted = fit_contain(crop_rgba(src), width, height)
		outs.append((out_name, paste_center(fitted, width, height)))

	for out_dir in OUT_DIRS:
		os.makedirs(out_dir, exist_ok=True)
		for out_name, canvas in outs:
			canvas.save(os.path.join(out_dir, out_name))
		print("wrote", out_dir, width, height, "aspect", round(width / height, 4))


if __name__ == "__main__":
	main()
