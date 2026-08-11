"""Pick the busiest frames out of a qa_capture_feature_vfx run and montage them.

Guessing frame indices by hand wastes captures: this scores every frame by how
much it changed from the one before, keeps peaks that are spread apart (so one
long event cannot eat every slot), and writes a contact sheet.

Run:  python tools/qa_peak_frames.py <story-id> [count]
"""

from __future__ import annotations

import glob
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.normpath(os.path.join(HERE, "..", "qa-shots", "feature_vfx"))
COLUMNS = 3
THUMB_W = 640
MIN_GAP = 4


def frame_scores(paths: list[str]) -> np.ndarray:
	previous = None
	scores = np.zeros(len(paths), dtype=np.float32)
	for index, path in enumerate(paths):
		small = np.asarray(
			Image.open(path).convert("L").resize((160, 100)), dtype=np.float32
		)
		if previous is not None:
			scores[index] = np.abs(small - previous).mean()
		previous = small
	return scores


def pick_peaks(scores: np.ndarray, count: int) -> list[int]:
	picked: list[int] = []
	for index in np.argsort(scores)[::-1]:
		if len(picked) >= count:
			break
		if all(abs(int(index) - other) >= MIN_GAP for other in picked):
			picked.append(int(index))
	return sorted(picked)


def main() -> None:
	if len(sys.argv) < 2:
		raise SystemExit("usage: qa_peak_frames.py <story-id> [count]")
	story = sys.argv[1]
	count = int(sys.argv[2]) if len(sys.argv) > 2 else 9

	paths = sorted(glob.glob(os.path.join(SHOTS, story, "*.jpg")))
	if not paths:
		raise SystemExit(f"no frames captured for {story}")

	picked = pick_peaks(frame_scores(paths), count)
	tiles = [Image.open(paths[index]).convert("RGB") for index in picked]
	scale = THUMB_W / tiles[0].width
	size = (THUMB_W, round(tiles[0].height * scale))
	rows = (len(tiles) + COLUMNS - 1) // COLUMNS
	sheet = Image.new("RGB", (size[0] * COLUMNS, size[1] * rows), (0, 0, 0))
	for slot, tile in enumerate(tiles):
		sheet.paste(
			tile.resize(size), ((slot % COLUMNS) * size[0], (slot // COLUMNS) * size[1])
		)

	out = os.path.join(SHOTS, f"_peaks_{story}.jpg")
	sheet.save(out, quality=90)
	print(f"{story}: frames {picked} -> {out}")


if __name__ == "__main__":
	main()
