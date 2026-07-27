"""Generate THE WHITE ROOM stacked brand logo — clean, high-contrast.

Outputs (cache-busted v2):
  assets/sprites/mirror/logo_v2.png   — runtime Pixi sprite (transparent PNG)
  assets/sprites/mirror/logo_v2.svg   — vector source
  static/assets/sprites/mirror/logo_v2.png/.svg — public/static mirror
  assets-raw/mirror/logo_v2_master.png
  assets-raw/mirror/logo_v2.svg
  assets-raw/mirror/logo_v2@1x/@2x/@3x.png

Design:
  - Stacked THE / WHITE / ROOM
  - Near-white #f4f1ec solid fill (no grain / distress / texture)
  - Fully transparent background (PNG alpha)
  - Impact (condensed bold) → Anton → Arial Narrow Bold
  - Supersampled then LANCZOS-down for sharp HUD edges
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT_DIR = ROOT / "assets" / "sprites" / "mirror"
STATIC_DIR = ROOT / "static" / "assets" / "sprites" / "mirror"
RAW_DIR = ROOT / "assets-raw" / "mirror"

# High-contrast clinical lockup — readable on dark mottled HUD
TEXT = (244, 241, 236, 255)  # #f4f1ec
# Thin solid outline only (no noise) so letters hold against mottled scene midtones
OUTLINE = (12, 12, 14, 255)  # #0c0c0e
OUTLINE_PX_SS = 10  # at 2× supersample → ~5px at master

# Runtime / master canvas
W, H = 2048, 1792
ASPECT = H / W  # 0.875
SS = 2


def _font_path() -> Path:
	# Impact first: heaviest condensed punch at HUD sizes
	impact = Path(r"C:\Windows\Fonts\impact.ttf")
	if impact.exists():
		return impact
	anton = Path(r"C:\Users\xheih\AppData\Local\Microsoft\Windows\Fonts\anton.ttf")
	if anton.exists():
		return anton
	arialn = Path(r"C:\Windows\Fonts\ARIALNB.TTF")
	if arialn.exists():
		return arialn
	raise FileNotFoundError("Need Impact, Anton, or Arial Narrow Bold")


def _fit_sizes(font_path: Path, canvas_w: int, target_frac: float = 0.82) -> tuple[int, int, int]:
	"""Pick THE / WHITE / ROOM point sizes so WHITE drives canvas width."""
	target_w = int(canvas_w * target_frac)
	lo = int(240 * (canvas_w / W))
	hi = int(560 * (canvas_w / W))
	for white_size in range(hi, lo, -4):
		the_size = max(int(white_size * 0.38), 48)
		room_size = white_size
		f_the = ImageFont.truetype(str(font_path), the_size)
		f_white = ImageFont.truetype(str(font_path), white_size)
		f_room = ImageFont.truetype(str(font_path), room_size)
		tmp = Image.new("RGBA", (canvas_w, int(canvas_w * ASPECT)))
		d = ImageDraw.Draw(tmp)
		widths = []
		for text, font in (("THE", f_the), ("WHITE", f_white), ("ROOM", f_room)):
			bb = d.textbbox((0, 0), text, font=font)
			widths.append(bb[2] - bb[0])
		if max(widths) <= target_w:
			return the_size, white_size, room_size
	raise RuntimeError("could not fit stacked logo into target width")


def _draw_stack(
	canvas_w: int,
	canvas_h: int,
	font_path: Path,
	the_size: int,
	white_size: int,
	room_size: int,
) -> Image.Image:
	f_the = ImageFont.truetype(str(font_path), the_size)
	f_white = ImageFont.truetype(str(font_path), white_size)
	f_room = ImageFont.truetype(str(font_path), room_size)

	# Transparent — no plate fighting the scene
	img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
	d = ImageDraw.Draw(img)

	bb_the = d.textbbox((0, 0), "THE", font=f_the)
	bb_white = d.textbbox((0, 0), "WHITE", font=f_white)
	bb_room = d.textbbox((0, 0), "ROOM", font=f_room)

	def metrics(bb: tuple[int, int, int, int]) -> tuple[int, int]:
		return bb[2] - bb[0], bb[3] - bb[1]

	_, h_the = metrics(bb_the)
	_, h_white = metrics(bb_white)
	_, h_room = metrics(bb_room)

	gap_the_white = int(white_size * 0.12)
	gap_white_room = int(white_size * 0.04)
	total_h = h_the + gap_the_white + h_white + gap_white_room + h_room
	y0 = (canvas_h - total_h) // 2 - int(canvas_h * 0.01)

	placements: list[tuple[str, ImageFont.FreeTypeFont, int, tuple[int, int, int, int]]] = []
	y = y0
	placements.append(("THE", f_the, y, bb_the))
	y += h_the + gap_the_white
	placements.append(("WHITE", f_white, y, bb_white))
	y += h_white + gap_white_room
	placements.append(("ROOM", f_room, y, bb_room))

	# Pass 1: solid outline (expand via max filter — clean, no noise)
	outline_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
	od = ImageDraw.Draw(outline_layer)
	for text, font, ty, bb in placements:
		tw = bb[2] - bb[0]
		x = (canvas_w - tw) // 2 - bb[0]
		od.text((x, ty - bb[1]), text, font=font, fill=OUTLINE)

	# Dilate alpha into a crisp ring
	alpha = outline_layer.split()[-1]
	dilated = alpha
	for _ in range(max(1, OUTLINE_PX_SS // 2)):
		dilated = dilated.filter(ImageFilter.MaxFilter(3))
	outline_solid = Image.new("RGBA", (canvas_w, canvas_h), OUTLINE)
	outline_solid.putalpha(dilated)

	# Pass 2: solid fill on top
	fill_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
	fd = ImageDraw.Draw(fill_layer)
	for text, font, ty, bb in placements:
		tw = bb[2] - bb[0]
		x = (canvas_w - tw) // 2 - bb[0]
		fd.text((x, ty - bb[1]), text, font=font, fill=TEXT)

	img = Image.alpha_composite(outline_solid, fill_layer)
	return img


def _svg(the_size: int, white_size: int, room_size: int, font_css: str) -> str:
	# Transparent SVG — no background rect
	return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="THE WHITE ROOM">
  <title>THE WHITE ROOM</title>
  <g fill="#f4f1ec" text-anchor="middle"
     font-family="{font_css}"
     font-weight="700"
     stroke="#0c0c0e" stroke-width="8" paint-order="stroke fill">
    <text x="{W // 2}" y="28%" font-size="{int(the_size * 0.92)}" letter-spacing="16">THE</text>
    <text x="{W // 2}" y="55%" font-size="{int(white_size * 0.92)}" letter-spacing="2">WHITE</text>
    <text x="{W // 2}" y="82%" font-size="{int(room_size * 0.92)}" letter-spacing="6">ROOM</text>
  </g>
</svg>
"""


def render() -> dict:
	OUT_DIR.mkdir(parents=True, exist_ok=True)
	STATIC_DIR.mkdir(parents=True, exist_ok=True)
	RAW_DIR.mkdir(parents=True, exist_ok=True)

	font_path = _font_path()
	font_css = "Impact, 'Arial Black', 'Arial Narrow', sans-serif"
	if font_path.name.lower() == "anton.ttf":
		font_css = "Anton, Impact, 'Arial Black', 'Arial Narrow', sans-serif"

	sw, sh = W * SS, H * SS
	the_ss, white_ss, room_ss = _fit_sizes(font_path, sw)
	hi = _draw_stack(sw, sh, font_path, the_ss, white_ss, room_ss)
	img = hi.resize((W, H), Image.Resampling.LANCZOS)

	# Verify: must have real transparency + bright text
	alpha = img.split()[-1]
	a_min, a_max = alpha.getextrema()
	if a_min >= 250:
		raise RuntimeError("logo_v2 PNG is opaque — transparent BG required")

	the_size = max(int(the_ss / SS), 1)
	white_size = max(int(white_ss / SS), 1)
	room_size = max(int(room_ss / SS), 1)

	out_png = OUT_DIR / "logo_v2.png"
	static_png = STATIC_DIR / "logo_v2.png"
	raw_png = RAW_DIR / "logo_v2_master.png"
	out_svg = OUT_DIR / "logo_v2.svg"
	static_svg = STATIC_DIR / "logo_v2.svg"
	raw_svg = RAW_DIR / "logo_v2.svg"

	img.save(out_png, "PNG", optimize=True)
	img.save(static_png, "PNG", optimize=True)
	img.save(raw_png, "PNG", optimize=True)
	svg = _svg(the_size, white_size, room_size, font_css)
	out_svg.write_text(svg, encoding="utf-8")
	static_svg.write_text(svg, encoding="utf-8")
	raw_svg.write_text(svg, encoding="utf-8")

	for scale, name in ((1, "logo_v2@1x.png"), (2, "logo_v2@2x.png"), (3, "logo_v2@3x.png")):
		base_w = 512 * scale
		base_h = int(round(base_w * ASPECT))
		scaled = hi.resize((base_w, base_h), Image.Resampling.LANCZOS)
		scaled.save(RAW_DIR / name, "PNG", optimize=True)

	# Preview on dark mottled-ish plate for visual QA (not shipped to runtime)
	preview = Image.new("RGBA", (W, H), (22, 20, 24, 255))
	preview = Image.alpha_composite(preview, img)
	preview.convert("RGB").save(RAW_DIR / "logo_v2_preview_dark.jpg", "JPEG", quality=92)

	return {
		"out_png": str(out_png),
		"out_svg": str(out_svg),
		"static_png": str(static_png),
		"static_svg": str(static_svg),
		"font": str(font_path),
		"sizes": (the_size, white_size, room_size),
		"canvas": (W, H),
		"aspect": ASPECT,
		"bytes": out_png.stat().st_size,
		"alpha_range": (a_min, a_max),
	}


if __name__ == "__main__":
	info = render()
	print("white_room_logo_v2:", info)
