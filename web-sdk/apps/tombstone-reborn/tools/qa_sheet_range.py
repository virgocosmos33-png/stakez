"""Contact sheet for a frame RANGE of an already-captured story, cropped to the
board so a single beat can be inspected closely.

Run: python tools/qa_sheet_range.py <story-id> <first> <last> [step] [crop]
     crop = left,top,right,bottom in 1280x800 page pixels (default board box)
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "qa-shots" / "feature_vfx"
DEFAULT_CROP = (150, 60, 800, 500)
COLUMNS = 4
TILE_W = 480


def main() -> None:
	story = sys.argv[1]
	first = int(sys.argv[2])
	last = int(sys.argv[3])
	step = int(sys.argv[4]) if len(sys.argv) > 4 else 2
	crop = tuple(int(v) for v in sys.argv[5].split(",")) if len(sys.argv) > 5 else DEFAULT_CROP

	src = ROOT / story
	picks = []
	for index in range(first, last + 1, step):
		path = src / f"f{index:04d}.jpg"
		if path.exists():
			picks.append((index, Image.open(path).convert("RGB").crop(crop)))
	if not picks:
		raise SystemExit(f"no frames in {src} for {first}..{last}")

	ratio = picks[0][1].height / picks[0][1].width
	tile_h = int(TILE_W * ratio)
	rows = (len(picks) + COLUMNS - 1) // COLUMNS
	sheet = Image.new("RGB", (TILE_W * COLUMNS, tile_h * rows), (12, 12, 14))
	draw = ImageDraw.Draw(sheet)
	for slot, (index, tile) in enumerate(picks):
		col = slot % COLUMNS
		row = slot // COLUMNS
		sheet.paste(tile.resize((TILE_W, tile_h)), (col * TILE_W, row * tile_h))
		draw.text((col * TILE_W + 6, row * tile_h + 4), str(index), fill=(255, 220, 120))
	out = ROOT / f"{story}_range_{first}_{last}.jpg"
	sheet.save(out, quality=90)
	print(f"-> {out}")


if __name__ == "__main__":
	main()
