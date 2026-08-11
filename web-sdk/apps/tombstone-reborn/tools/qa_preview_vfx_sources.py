"""Contact sheet + alpha report for a folder of VFX source plates.

Run:  python tools/qa_preview_vfx_sources.py <folder> [out.png]

Composites every PNG over the game's dark board colour so it is obvious which
plates still carry a baked-in black/white background instead of real alpha.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

BOARD = (24, 20, 16, 255)
TILE = 240


def main() -> None:
	folder = Path(sys.argv[1] if len(sys.argv) > 1 else "assets-raw/scenario_western_vfx")
	out = Path(sys.argv[2] if len(sys.argv) > 2 else "qa-shots/vfx_sources.png")
	files = sorted(folder.glob("*.png"))
	if not files:
		raise SystemExit(f"no PNGs in {folder}")

	cols = 5
	rows = (len(files) + cols - 1) // cols
	sheet = Image.new("RGB", (cols * TILE, rows * (TILE + 20)), BOARD[:3])
	draw = ImageDraw.Draw(sheet)

	for index, path in enumerate(files):
		image = Image.open(path).convert("RGBA")
		low, high = image.getchannel("A").getextrema()
		opaque = sum(1 for a in image.getchannel("A").getdata() if a > 250)
		total = image.width * image.height
		plate = Image.new("RGBA", image.size, BOARD)
		plate.alpha_composite(image)
		thumb = plate.convert("RGB")
		thumb.thumbnail((TILE, TILE))
		x = (index % cols) * TILE
		y = (index // cols) * (TILE + 20) + 18
		sheet.paste(thumb, (x, y))
		draw.text((x + 3, y - 15), f"{path.stem} {image.size}", fill=(255, 215, 120))
		print(
			f"{path.stem:22s} size={image.size} alpha={low}-{high} "
			f"opaque={opaque * 100 // total}%",
			flush=True,
		)

	out.parent.mkdir(parents=True, exist_ok=True)
	sheet.save(out)
	print(f"-> {out}")


if __name__ == "__main__":
	main()
