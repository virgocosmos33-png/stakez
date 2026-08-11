"""Zoom into captured frames at native resolution, to inspect a single effect.

Run:  python tools/qa_zoom.py <story-id> <frame-stem> [frame-stem ...] [--rect x0,y0,x1,y1]
Frames are cropped (board by default, or --rect in page space) and upscaled.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "qa-shots"
BOARD = (280, 90, 780, 500)
TARGET_W = 1000


def main() -> None:
	args = list(sys.argv[1:])
	rect = BOARD
	if "--rect" in args:
		at = args.index("--rect")
		rect = tuple(int(v) for v in args[at + 1].split(","))  # type: ignore[assignment]
		del args[at : at + 2]
	story = args[0]
	stems = args[1:]
	folder = ROOT / "split_lock" / story
	out_dir = ROOT / "zoom"
	out_dir.mkdir(parents=True, exist_ok=True)
	for stem in stems:
		src = folder / f"{stem}.jpg"
		if not src.exists():
			raise SystemExit(f"missing {src}")
		img = Image.open(src).convert("RGB").crop(rect)
		zoom = max(1, round(TARGET_W / img.width))
		img = img.resize((img.width * zoom, img.height * zoom), Image.LANCZOS)
		out = out_dir / f"{story}_{stem}.png"
		img.save(out)
		print(f"-> {out} ({zoom}x)")


if __name__ == "__main__":
	main()
