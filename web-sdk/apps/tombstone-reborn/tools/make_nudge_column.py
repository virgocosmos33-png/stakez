"""Bake the NUDGE WAYS grave to a full-reel rectangle.

The source is a hexagonal coffin. Keep the NUDGE plaque and the wide
shaft, stretch those rows to the shoulder width, drop the pointy foot,
snap to the 6-color vector palette, resize to the pocket.

Outputs
  static/assets/sprites/fx/fx_nudge_column.png
  assets/sprites/fx/fx_nudge_column.png

Run:  python tools/make_nudge_column.py
"""

from __future__ import annotations

import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
RAW_DIR = os.path.join(APP, "assets-raw", "layer_nudge")
RAW_NAME = "column_coffin.png"
OUT_DIRS = [
	os.path.join(APP, "static", "assets", "sprites", "fx"),
	os.path.join(APP, "assets", "sprites", "fx"),
]

CARD_W_OVER_SIZE = (292 / 300) * 0.775
POCKET_H_OVER_SIZE = 3.0 + (292 / 300)
TARGET_W = 448
TARGET_H = round(TARGET_W * POCKET_H_OVER_SIZE / CARD_W_OVER_SIZE)
# Must match NudgeWays HEADER_FRAC * image height (200 / 2360).
HEADER_PX = 200
IRON = (18, 13, 10)
PALETTE = [
	IRON,
	(92, 61, 40),
	(139, 90, 43),
	(232, 214, 168),
	(240, 230, 208),
	(192, 57, 43),
]
SHAFT_FRAC = 0.86


def ensure_raw() -> str:
	os.makedirs(RAW_DIR, exist_ok=True)
	dest = os.path.join(RAW_DIR, RAW_NAME)
	if not os.path.isfile(dest):
		raise SystemExit(f"missing nudge column source: {dest}")
	return dest


def is_paint(pixel: tuple[int, ...]) -> bool:
	r, g, b, a = pixel
	return a > 20 and r + g + b > 40


def is_wood(pixel: tuple[int, ...]) -> bool:
	"""Pine / gold / bone / blood — not the iron gutter that hides a taper."""
	r, g, b, a = pixel
	return a > 20 and (r > 40 or g > 35)


def row_span(px, width: int, y: int) -> tuple[int, int, int] | None:
	left = None
	right = None
	for x in range(width):
		if not is_paint(px[x, y]):
			continue
		if left is None:
			left = x
		right = x
	if left is None or right is None:
		return None
	return left, right, right - left + 1


def stretch_row(src: Image.Image, y: int, left: int, right: int, dest_w: int) -> Image.Image:
	strip = src.crop((left, y, right + 1, y + 1))
	return strip.resize((dest_w, 1), Image.Resampling.NEAREST)


def snap_six(image: Image.Image) -> Image.Image:
	rgb = image.convert("RGB")
	pal = Image.new("P", (1, 1))
	flat: list[int] = []
	for color in PALETTE:
		flat.extend(color)
	flat.extend([0, 0, 0] * (256 - len(PALETTE)))
	pal.putpalette(flat)
	snapped = rgb.quantize(palette=pal, dither=Image.Dither.NONE).convert("RGB")
	px = snapped.load()
	w, h = snapped.size
	for y in range(h):
		for x in range(w):
			if px[x, y] == (0, 0, 0):
				px[x, y] = IRON
	return snapped.convert("RGBA")


def flatten_iron(image: Image.Image) -> Image.Image:
	rgba = image.convert("RGBA")
	bg = Image.new("RGB", rgba.size, IRON)
	bg.paste(rgba, mask=rgba.getchannel("A"))
	return bg


def band_to_width(src: Image.Image, y0: int, y1: int, dest_w: int) -> Image.Image:
	"""Stretch each painted row in [y0, y1) to dest_w. Skip empty rows."""
	px = src.load()
	width = src.size[0]
	rows: list[Image.Image] = []
	for y in range(y0, y1):
		span = row_span(px, width, y)
		if span is None:
			continue
		left, right, _ = span
		rows.append(stretch_row(src, y, left, right, dest_w))
	if not rows:
		raise SystemExit(f"no painted rows in {y0}..{y1}")
	out = Image.new("RGBA", (dest_w, len(rows)), (*IRON, 255))
	for i, row in enumerate(rows):
		out.paste(row, (0, i))
	return out


def compose(src: Image.Image) -> Image.Image:
	rgba = src.convert("RGBA")
	width, height = rgba.size
	px = rgba.load()
	spans = [row_span(px, width, y) for y in range(height)]
	max_span = max((span[2] for span in spans if span), default=0)
	if max_span < 8:
		raise SystemExit("nudge column source has no painted shaft")
	cut = max_span * SHAFT_FRAC
	shaft_ys = [y for y, span in enumerate(spans) if span and span[2] >= cut]
	if not shaft_ys:
		raise SystemExit("nudge column source has no full-width shaft")
	shaft_start = shaft_ys[0]
	shaft_end = shaft_ys[-1] + 1
	# Plaque is everything above the shoulders. Stretch it to the same width.
	plaque = band_to_width(rgba, 0, max(1, shaft_start), max_span)
	shaft = band_to_width(rgba, shaft_start, shaft_end, max_span)
	plaque_r = flatten_iron(plaque).resize((TARGET_W, HEADER_PX), Image.Resampling.NEAREST)
	shaft_r = flatten_iron(shaft).resize((TARGET_W, TARGET_H - HEADER_PX), Image.Resampling.NEAREST)
	out = Image.new("RGB", (TARGET_W, TARGET_H), IRON)
	out.paste(plaque_r.convert("RGB"), (0, 0))
	out.paste(shaft_r.convert("RGB"), (0, HEADER_PX))
	locked = force_rectangle(out.convert("RGBA"))
	return force_rectangle(snap_six(locked))


def wood_span(px, width: int, y: int) -> tuple[int, int, int] | None:
	left = None
	right = None
	for x in range(width):
		if not is_wood(px[x, y]):
			continue
		if left is None:
			left = x
		right = x
	if left is None or right is None:
		return None
	return left, right, right - left + 1


def force_rectangle(src: Image.Image) -> Image.Image:
	"""Last lock: wood fills every row edge to edge. Iron gutters cannot hide a taper."""
	rgba = src.convert("RGBA")
	width, height = rgba.size
	px = rgba.load()
	out = Image.new("RGBA", (width, height), (*IRON, 255))
	built: list[Image.Image | None] = []
	for y in range(height):
		span = wood_span(px, width, y)
		if span is None:
			built.append(None)
			continue
		built.append(stretch_row(rgba, y, span[0], span[1], width))
	first = next((row for row in built if row is not None), None)
	if first is None:
		raise SystemExit("force_rectangle found no wood rows")
	current = first
	for y, row in enumerate(built):
		if row is not None:
			current = row
		out.paste(current, (0, y))
	return out


def main() -> None:
	art = compose(Image.open(ensure_raw()))
	for out_dir in OUT_DIRS:
		os.makedirs(out_dir, exist_ok=True)
		path = os.path.join(out_dir, "fx_nudge_column.png")
		art.save(path, optimize=True)
		print(f"[nudge-column] {art.width}x{art.height} rectangle 6c -> {path}")


if __name__ == "__main__":
	main()
