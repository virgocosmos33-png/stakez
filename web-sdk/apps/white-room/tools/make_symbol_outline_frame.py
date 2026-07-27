"""Build the reusable HIGH-SYMBOL outline frame UI element.

This is a HOLLOW clinical observation-bezel sprite (transparent center) used by
Symbol.svelte — NOT baked into symbol card art.

Writes:
  assets/sprites/mirror/symbol_outline_frame.png
  static/assets/sprites/mirror/symbol_outline_frame.png

Run:  python tools/make_symbol_outline_frame.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

APP = Path(__file__).resolve().parents[1]
OUTS = [
	APP / "assets" / "sprites" / "mirror" / "symbol_outline_frame.png",
	APP / "static" / "assets" / "sprites" / "mirror" / "symbol_outline_frame.png",
]
SIZE = 512

BONE = (244, 241, 236)
SILVER = (200, 196, 188)
STEEL = (138, 134, 128)
CHARCOAL = (58, 54, 50)
DARK = (26, 24, 22)
PAD = (228, 224, 216)
BLOOD = (107, 42, 40)
FLUOR = (236, 242, 230)


def build() -> Image.Image:
	"""Padded/steel observation bezel — replaces thin grey Graphics strokes."""
	img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
	d = ImageDraw.Draw(img)

	outer = 4
	band = 22
	# padded outer housing
	d.rounded_rectangle([outer, outer, SIZE - outer, SIZE - outer], radius=22, fill=(*PAD, 245))
	d.rounded_rectangle(
		[outer + 5, outer + 5, SIZE - outer - 5, SIZE - outer - 5],
		radius=18,
		fill=(*PAD, 255),
	)
	steel0 = outer + band
	d.rounded_rectangle([steel0, steel0, SIZE - steel0, SIZE - steel0], radius=14, fill=(*DARK, 255))
	steel1 = steel0 + 7
	d.rounded_rectangle([steel1, steel1, SIZE - steel1, SIZE - steel1], radius=12, fill=(*STEEL, 255))
	lip = steel1 + 8
	d.rounded_rectangle([lip, lip, SIZE - lip, SIZE - lip], radius=10, fill=(*SILVER, 255))

	# fluorescent tube
	tube_y0, tube_y1 = steel0 + 2, steel0 + 16
	tube_x0, tube_x1 = steel0 + 40, SIZE - steel0 - 40
	d.rounded_rectangle([tube_x0, tube_y0, tube_x1, tube_y1], radius=5, fill=(*DARK, 255))
	d.rounded_rectangle(
		[tube_x0 + 3, tube_y0 + 3, tube_x1 - 3, tube_y1 - 3],
		radius=3,
		fill=(*FLUOR, 235),
	)
	glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
	gd = ImageDraw.Draw(glow)
	gd.ellipse([tube_x0 - 10, tube_y0 - 8, tube_x1 + 10, tube_y1 + 16], fill=(*FLUOR, 55))
	img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(12)))

	# hole mask: 255 keep frame, 0 clear aperture
	ap = lip + 6
	hole = Image.new("L", (SIZE, SIZE), 255)
	hd = ImageDraw.Draw(hole)
	hd.rounded_rectangle([ap, ap, SIZE - ap, SIZE - ap], radius=9, fill=0)

	# restraint buckles on steel band (outside aperture)
	d = ImageDraw.Draw(img)
	buckle_w, buckle_h = 18, 10
	inset = steel0 + 16
	for cx, cy in (
		(inset, inset + 12),
		(SIZE - inset, inset + 12),
		(inset, SIZE - inset),
		(SIZE - inset, SIZE - inset),
	):
		d.rounded_rectangle(
			[cx - buckle_w, cy - buckle_h // 2, cx + buckle_w, cy + buckle_h // 2],
			radius=3,
			fill=(*CHARCOAL, 255),
		)
		d.rounded_rectangle(
			[cx - buckle_w + 3, cy - buckle_h // 2 + 2, cx + buckle_w - 3, cy + buckle_h // 2 - 2],
			radius=2,
			fill=(*STEEL, 255),
		)
		d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(*BONE, 255))
		if cy > SIZE // 2:
			d.ellipse([cx - 4, cy + 5, cx + 6, cy + 12], fill=(*BLOOD, 80))

	img.putalpha(ImageChops.multiply(img.split()[3], hole))

	cx = cy = SIZE // 2
	if img.getpixel((cx, cy))[3] != 0:
		raise SystemExit(f"aperture not transparent at center: {img.getpixel((cx, cy))}")
	return img


def main() -> None:
	img = build()
	for out in OUTS:
		out.parent.mkdir(parents=True, exist_ok=True)
		img.save(out, "PNG")
		print(f"wrote {out}  center_alpha={img.getpixel((SIZE // 2, SIZE // 2))[3]}")


if __name__ == "__main__":
	main()
