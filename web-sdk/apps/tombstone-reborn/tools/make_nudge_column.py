"""Bake the full-reel NUDGE WAYS column from ONE generated card.

The source is a single 9:16 NUDGE plaque. Header and foot keep their
proportions; only the arrow shaft is stretched to the 4-row pocket.

Outputs
  static/assets/sprites/fx/fx_nudge_column.png
  assets/sprites/fx/fx_nudge_column.png

Run:  python tools/make_nudge_column.py
"""

from __future__ import annotations

import os
import shutil

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
RAW_DIR = os.path.join(APP, "assets-raw", "layer_nudge")
RAW_NAME = "column_v2.png"
CURSOR_SRC = os.path.join(
	os.path.expanduser("~"),
	".cursor",
	"projects",
	"c-Users-Emex33-Desktop-stakez",
	"assets",
	"fx_nudge_column_v2.png",
)
OUT_DIRS = [
	os.path.join(APP, "static", "assets", "sprites", "fx"),
	os.path.join(APP, "assets", "sprites", "fx"),
]

CARD_W_OVER_SIZE = (292 / 300) * 0.775
POCKET_H_OVER_SIZE = 3.0 + (292 / 300)
TARGET_W = 448
TARGET_H = round(TARGET_W * POCKET_H_OVER_SIZE / CARD_W_OVER_SIZE)
# share of the source kept as header / foot; the middle is the shaft
HEAD = 0.28
FOOT = 0.22


def ensure_raw() -> str:
	os.makedirs(RAW_DIR, exist_ok=True)
	dest = os.path.join(RAW_DIR, RAW_NAME)
	if os.path.isfile(CURSOR_SRC):
		shutil.copy2(CURSOR_SRC, dest)
	if not os.path.isfile(dest):
		raise SystemExit(f"missing nudge column source: {dest}")
	return dest


def flatten_rgb(image: Image.Image) -> Image.Image:
	rgba = image.convert("RGBA")
	bg = Image.new("RGB", rgba.size, (28, 22, 18))
	bg.paste(rgba, mask=rgba.getchannel("A"))
	return bg


def to_pocket(src: Image.Image) -> Image.Image:
	fitted = src.resize(
		(TARGET_W, max(1, round(src.height * TARGET_W / src.width))),
		Image.LANCZOS,
	)
	if fitted.height >= TARGET_H:
		return fitted.resize((TARGET_W, TARGET_H), Image.LANCZOS)

	head_h = max(1, round(fitted.height * HEAD))
	foot_h = max(1, round(fitted.height * FOOT))
	shaft = fitted.crop((0, head_h, TARGET_W, fitted.height - foot_h))
	shaft_h = TARGET_H - head_h - foot_h
	if shaft_h < 1:
		return fitted.resize((TARGET_W, TARGET_H), Image.LANCZOS)
	shaft = shaft.resize((TARGET_W, shaft_h), Image.LANCZOS)

	out = Image.new("RGB", (TARGET_W, TARGET_H), (28, 22, 18))
	out.paste(fitted.crop((0, 0, TARGET_W, head_h)), (0, 0))
	out.paste(shaft, (0, head_h))
	out.paste(
		fitted.crop((0, fitted.height - foot_h, TARGET_W, fitted.height)),
		(0, TARGET_H - foot_h),
	)
	return out


def main() -> None:
	art = to_pocket(flatten_rgb(Image.open(ensure_raw()))).convert("RGBA")
	for out_dir in OUT_DIRS:
		os.makedirs(out_dir, exist_ok=True)
		path = os.path.join(out_dir, "fx_nudge_column.png")
		art.save(path, optimize=True)
		print(f"[nudge-column] {art.width}x{art.height} opaque -> {path}")


if __name__ == "__main__":
	main()
