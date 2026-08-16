"""Bake the TOMBSTONE REBORN sheriff wordmark.

Flat Rye wood-type, gold fill, iron outline, one star. No stone, no 3D.
Writes assets-src and static (same relative path).
"""

from __future__ import annotations

import math
from pathlib import Path

from fontTools.ttLib.woff2 import decompress
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WOFF = ROOT / "static" / "assets" / "fonts" / "webfont" / "rye-400-latin.woff2"
SRC = ROOT / "assets-src" / "sprites" / "mirror"
STATIC = ROOT / "static" / "assets" / "sprites" / "mirror"

GOLD = (232, 214, 168, 255)
GOLD_HI = (248, 236, 200, 255)
IRON = (18, 13, 10, 255)
W, H = 2200, 980
SS = 2


def rye_font(size: int) -> ImageFont.FreeTypeFont:
	tmp = Path(__file__).with_name("_rye_logo.ttf")
	if not tmp.exists():
		decompress(str(WOFF), str(tmp))
	return ImageFont.truetype(str(tmp), size)


def star(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
	pts = []
	for i in range(10):
		ang = math.radians(-90 + i * 36)
		rad = r if i % 2 == 0 else r * 0.38
		pts.append((cx + math.cos(ang) * rad, cy + math.sin(ang) * rad))
	return pts


def stroke_text(draw: ImageDraw.ImageDraw, xy, text, font, fill, outline, width):
	x, y = xy
	for dx in range(-width, width + 1):
		for dy in range(-width, width + 1):
			if dx * dx + dy * dy > width * width:
				continue
			draw.text((x + dx, y + dy), text, font=font, fill=outline, anchor="mm")
	draw.text(xy, text, font=font, fill=fill, anchor="mm")


def bake() -> Image.Image:
	cw, ch = W * SS, H * SS
	img = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
	d = ImageDraw.Draw(img)
	f_top = rye_font(int(268 * SS))
	f_bot = rye_font(int(196 * SS))

	cx = cw / 2
	star_y = ch * 0.18
	top_y = ch * 0.42
	bot_y = ch * 0.72
	r = 42 * SS
	d.polygon(star(cx, star_y, r + 6 * SS), fill=IRON)
	d.polygon(star(cx, star_y, r), fill=GOLD)
	d.polygon(star(cx, star_y, r * 0.42), fill=IRON)

	stroke_text(d, (cx, top_y), "TOMBSTONE", f_top, GOLD_HI, IRON, int(14 * SS))
	stroke_text(d, (cx, bot_y), "REBORN", f_bot, GOLD, IRON, int(12 * SS))

	rule_w = 420 * SS
	rule_y = (top_y + bot_y) / 2
	x0, y0 = cx - rule_w / 2, rule_y - 2.5 * SS
	x1, y1 = cx + rule_w / 2, rule_y + 2.5 * SS
	d.rectangle((x0 - 3 * SS, y0 - 3 * SS, x1 + 3 * SS, y1 + 3 * SS), fill=IRON)
	d.rectangle((x0, y0, x1, y1), fill=GOLD)

	bbox = img.getbbox()
	if bbox:
		pad = 28 * SS
		l, t, rgt, b = bbox
		img = img.crop((max(0, l - pad), max(0, t - pad), min(cw, rgt + pad), min(ch, b + pad)))
	out = img.resize((img.width // SS, img.height // SS), Image.Resampling.LANCZOS)
	# slight sharpen so HUD sizes stay crisp
	return out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=2))


def main() -> None:
	out = bake()
	for folder in (SRC, STATIC):
		folder.mkdir(parents=True, exist_ok=True)
		dest = folder / "tr_logo.png"
		out.save(dest)
		print(dest, out.size)
	tmp = Path(__file__).with_name("_rye_logo.ttf")
	if tmp.exists():
		tmp.unlink()


if __name__ == "__main__":
	main()
