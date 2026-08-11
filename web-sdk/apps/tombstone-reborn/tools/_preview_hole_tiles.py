"""Scratch: quarter the bullet-hole sheets and preview every tile.

Run:  python tools/_preview_hole_tiles.py
Used to pick the tile indices baked by tools/make_bullet_hole_atlas.py.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "assets-raw" / "scenario_western_vfx"
OUT = HERE.parent / "qa-shots" / "hole_tiles.png"
SHEETS = ("holes_sheet_a", "holes_sheet_b", "holes_sheet_c")
TILE = 220


def quarters(image: Image.Image) -> list[Image.Image]:
	w, h = image.size
	hw, hh = w // 2, h // 2
	return [
		image.crop((0, 0, hw, hh)),
		image.crop((hw, 0, w, hh)),
		image.crop((0, hh, hw, h)),
		image.crop((hw, hh, w, h)),
	]


def main() -> None:
	sheet = Image.new("RGB", (4 * TILE, len(SHEETS) * (TILE + 18)), (24, 20, 16))
	draw = ImageDraw.Draw(sheet)
	for row, name in enumerate(SHEETS):
		image = Image.open(RAW / f"{name}.png").convert("RGBA")
		for col, tile in enumerate(quarters(image)):
			plate = Image.new("RGBA", tile.size, (24, 20, 16, 255))
			plate.alpha_composite(tile)
			thumb = plate.convert("RGB")
			thumb.thumbnail((TILE, TILE))
			x = col * TILE
			y = row * (TILE + 18) + 16
			sheet.paste(thumb, (x, y))
			draw.text((x + 3, y - 14), f"{name[-1]}{col}", fill=(255, 215, 120))
	OUT.parent.mkdir(parents=True, exist_ok=True)
	sheet.save(OUT)
	print(f"-> {OUT}")


if __name__ == "__main__":
	main()
