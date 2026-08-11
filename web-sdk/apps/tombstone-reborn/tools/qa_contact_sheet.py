"""Contact sheet + board crops for a captured story, to actually look at the VFX.

Run:  python tools/qa_contact_sheet.py <story-id> [every-nth]
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "qa-shots" / "split_lock"
COLS = 5
TILE_W = 420
# the reels, in 1280x800 page space
BOARD = (280, 90, 780, 500)


def main() -> None:
	story = sys.argv[1]
	step = int(sys.argv[2]) if len(sys.argv) > 2 else 4
	folder = ROOT / story
	shots = sorted(folder.glob("f*.jpg"))[::step]
	if not shots:
		raise SystemExit(f"no frames in {folder}")

	first = Image.open(shots[0]).crop(BOARD)
	scale = TILE_W / first.width
	tile_h = round(first.height * scale)
	rows = (len(shots) + COLS - 1) // COLS
	sheet = Image.new("RGB", (COLS * TILE_W, rows * (tile_h + 16)), (16, 14, 12))
	draw = ImageDraw.Draw(sheet)
	for index, path in enumerate(shots):
		thumb = (
			Image.open(path).convert("RGB").crop(BOARD).resize((TILE_W, tile_h), Image.LANCZOS)
		)
		x = (index % COLS) * TILE_W
		y = (index // COLS) * (tile_h + 16) + 14
		sheet.paste(thumb, (x, y))
		draw.text((x + 3, y - 12), path.stem, fill=(255, 210, 120))
	out = folder.parent / f"{story}_sheet.png"
	sheet.save(out)
	print(f"-> {out} ({len(shots)} of {len(sorted(folder.glob('f*.jpg')))} frames)")


if __name__ == "__main__":
	main()
