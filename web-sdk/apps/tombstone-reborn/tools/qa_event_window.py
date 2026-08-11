"""Montage the frames where a feature event is actually on screen.

Scoring by raw frame-to-frame difference (qa_peak_frames.py) picks reel spins,
because a spinning strip moves far more pixels than a muzzle flash. The feature
VFX in this game are all hot and warm — flash, ember, brass, lantern — so this
scores each frame by how much bright warm light it carries and montages a
contiguous run around the strongest moment.

Pass an explicit `from` index to skip the boot carousel, whose paytable art is
warmer and brighter than any of the events.

Run:  python tools/qa_event_window.py <story-id> [tiles] [stride] [from]
"""

from __future__ import annotations

import glob
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.normpath(os.path.join(HERE, "..", "qa-shots", "feature_vfx"))
COLUMNS = 3
THUMB_W = 620
# a lit VFX pixel: clearly bright, and clearly warmer than it is blue
WARM_MIN = 165
WARM_BIAS = 55


def warm_mass(path: str) -> float:
	small = np.asarray(Image.open(path).convert("RGB").resize((240, 150)), dtype=np.int16)
	red = small[:, :, 0]
	blue = small[:, :, 2]
	return float(np.count_nonzero((red > WARM_MIN) & (red - blue > WARM_BIAS)))


def main() -> None:
	if len(sys.argv) < 2:
		raise SystemExit("usage: qa_event_window.py <story-id> [tiles] [stride] [from]")
	story = sys.argv[1]
	tiles_wanted = int(sys.argv[2]) if len(sys.argv) > 2 else 9
	stride = int(sys.argv[3]) if len(sys.argv) > 3 else 3
	first = int(sys.argv[4]) if len(sys.argv) > 4 else 0

	paths = sorted(glob.glob(os.path.join(SHOTS, story, "*.jpg")))[first:]
	if not paths:
		raise SystemExit(f"no frames captured for {story}")

	scores = np.array([warm_mass(path) for path in paths], dtype=np.float32)
	# centre the window on the busiest run, not a single spike
	window = max(1, tiles_wanted * stride)
	rolling = np.convolve(scores, np.ones(window) / window, mode="same")
	centre = int(np.argmax(rolling))
	start = max(0, centre - window // 2)
	picked = [min(len(paths) - 1, start + i * stride) for i in range(tiles_wanted)]

	images = [Image.open(paths[index]).convert("RGB") for index in picked]
	scale = THUMB_W / images[0].width
	size = (THUMB_W, round(images[0].height * scale))
	rows = (len(images) + COLUMNS - 1) // COLUMNS
	sheet = Image.new("RGB", (size[0] * COLUMNS, size[1] * rows), (0, 0, 0))
	draw = ImageDraw.Draw(sheet)
	for slot, image in enumerate(images):
		x = (slot % COLUMNS) * size[0]
		y = (slot // COLUMNS) * size[1]
		sheet.paste(image.resize(size), (x, y))
		draw.text((x + 6, y + 4), f"{first + picked[slot]}", fill=(255, 220, 120))

	out = os.path.join(SHOTS, f"_event_{story}.jpg")
	sheet.save(out, quality=90)
	print(f"{story}: peak {centre}, frames {picked} -> {out}")


if __name__ == "__main__":
	main()
