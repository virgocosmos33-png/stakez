"""Preview the baked split-VFX atlas frame by frame, over the board colour.

Run:  python tools/qa_preview_vfx_atlas.py
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
FX = HERE.parent / "static" / "assets" / "sprites" / "fx"
OUT = HERE.parent / "qa-shots" / "vfx_atlas_frames.png"
BOARD = (26, 22, 18, 255)
CELL = 128
TILE = 150
COLS = 7


def main() -> None:
	atlas = Image.open(FX / "tombstone_split_vfx.png").convert("RGBA")
	meta = json.loads((FX / "tombstone_split_vfx.json").read_text(encoding="utf-8"))
	names = meta["meta"].get("frame_order") or list(meta["frames"])
	count = atlas.width // CELL

	rows = (count + COLS - 1) // COLS
	sheet = Image.new("RGB", (COLS * TILE, rows * (TILE + 18)), BOARD[:3])
	draw = ImageDraw.Draw(sheet)
	for index in range(count):
		frame = atlas.crop((index * CELL, 0, (index + 1) * CELL, CELL))
		peak = max(frame.getchannel("A").getdata())
		plate = Image.new("RGBA", frame.size, BOARD)
		plate.alpha_composite(frame)
		x = (index % COLS) * TILE + (TILE - CELL) // 2
		y = (index // COLS) * (TILE + 18) + 16
		sheet.paste(plate.convert("RGB"), (x, y))
		label = names[index] if index < len(names) else str(index)
		draw.text(((index % COLS) * TILE + 3, y - 14), f"{index} {label} A{peak}", fill=(255, 215, 120))

	OUT.parent.mkdir(parents=True, exist_ok=True)
	sheet.save(OUT)
	print(f"-> {OUT} ({count} frames)")


if __name__ == "__main__":
	main()
