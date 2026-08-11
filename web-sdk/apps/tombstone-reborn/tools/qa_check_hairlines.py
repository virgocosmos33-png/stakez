"""Regression guard: no bright hairlines and no flat pale slabs over the reels.

Run:  python tools/qa_check_hairlines.py [story-id ...]
      python tools/qa_check_hairlines.py --selftest

Two failure classes, both of which have shipped to the player before:

1. HAIRLINE — a narrow, tall, bright column drawn down a card (the "prison bar"
   split divider). A run of >=RUN_PX rows where a column is brighter than BRIGHT
   while both neighbours 3px out are much darker.

2. FLAT SLAB — a large, flat, pale, warm region sitting over a cell: the
   corner-to-corner beige diagonal band, and the full-cell cream wash a morph
   flash leaves behind. What separates these from real art is TEXTURE: painted
   symbols, smoke plates and dust all carry high-frequency detail, while a
   vector fill or a stretched gradient strip is locally flat. So a block is
   suspect when it is pale AND warm AND its local standard deviation is near
   zero, and the frame fails when such blocks join into a region larger than a
   good chunk of a cell.
"""

from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "qa-shots" / "split_lock"
# The whole diamond board in 1280x800 page space. This must cover the OUTER
# reels: a tighter crop silently ignored a washed-out cell on the right-hand
# column, which is exactly the artifact the check exists to catch.
BOARD = (300, 90, 800, 510)

# --- hairline ---
BRIGHT = 150
CONTRAST = 60
RUN_PX = 24

# --- flat slab ---
BLOCK = 8
PALE_MIN = 125.0  # darker than this is board timber / shadow, not a pale bar
FLAT_STD = 10.0  # painted art and dust plates sit far above this
WARM_MIN = 4.0  # mean(R) - mean(B): beige/tan/cream, not a cold grey UI chip
MIN_AREA = 2600  # px; a 2X badge is ~900px, a washed-out cell is ~15000px
BAR_THIN_PX = 56  # a bar is thin in one direction; a hero art plate is not
# A diagonal band across a cell fills under a tenth of its bounding box. Warm
# blobs that are NOT artifacts — hero art, and cards lit up by the fire — measure
# 0.35-0.44 here, so the cut sits well below them rather than between them.
BAR_FILL_MAX = 0.22


def scan_hairlines(path: Path) -> list[tuple[int, int]]:
	image = Image.open(path).convert("L").crop(BOARD)
	pixels = image.load()
	w, h = image.size
	hits: list[tuple[int, int]] = []
	for x in range(3, w - 3):
		run = 0
		for y in range(h):
			here = pixels[x, y]
			left = pixels[x - 3, y]
			right = pixels[x + 3, y]
			if here > BRIGHT and here - left > CONTRAST and here - right > CONTRAST:
				run += 1
				if run >= RUN_PX:
					hits.append((x + BOARD[0], y + BOARD[1]))
					run = 0
			else:
				run = 0
	return hits


def _blocks(rgb: np.ndarray) -> np.ndarray:
	"""Per-BLOCK mask of pale + warm + texture-free cells."""
	h, w, _ = rgb.shape
	by, bx = h // BLOCK, w // BLOCK
	tiles = rgb[: by * BLOCK, : bx * BLOCK].reshape(by, BLOCK, bx, BLOCK, 3)
	tiles = tiles.transpose(0, 2, 1, 3, 4).reshape(by, bx, BLOCK * BLOCK, 3)

	lum = tiles @ np.array([0.299, 0.587, 0.114])
	mean = lum.mean(axis=2)
	std = lum.std(axis=2)
	warm = tiles[..., 0].mean(axis=2) - tiles[..., 2].mean(axis=2)
	return (mean >= PALE_MIN) & (std < FLAT_STD) & (warm >= WARM_MIN)


NEIGHBOURS = [(dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy, dx) != (0, 0)]


def largest_region(mask: np.ndarray) -> int:
	"""Area in px of the biggest connected run of flagged blocks.

	8-connected on purpose: a diagonal band only ever touches the next block
	corner-to-corner, so 4-connectivity would score every diagonal stripe as a
	chain of unrelated single blocks and never fire.
	"""
	return _largest_region_shape(mask)[0]


def _largest_region_shape(mask: np.ndarray) -> tuple[int, float, int]:
	"""(area_px, fill_ratio, thinnest_bbox_side_px) for the biggest region."""
	seen = np.zeros_like(mask, dtype=bool)
	by, bx = mask.shape
	best = 0
	for y0 in range(by):
		for x0 in range(bx):
			if not mask[y0, x0] or seen[y0, x0]:
				continue
			queue = deque([(y0, x0)])
			seen[y0, x0] = True
			count = 0
			top = bottom = y0
			left = right = x0
			while queue:
				y, x = queue.popleft()
				count += 1
				top, bottom = min(top, y), max(bottom, y)
				left, right = min(left, x), max(right, x)
				for dy, dx in NEIGHBOURS:
					ny, nx = y + dy, x + dx
					if 0 <= ny < by and 0 <= nx < bx and mask[ny, nx] and not seen[ny, nx]:
						seen[ny, nx] = True
						queue.append((ny, nx))
			if count > best:
				box_h = bottom - top + 1
				box_w = right - left + 1
				best = count
				best_fill = count / float(box_h * box_w)
				best_thin = min(box_h, box_w) * BLOCK
	if best == 0:
		return 0, 1.0, 0
	return best * BLOCK * BLOCK, best_fill, best_thin


def scan_flat_slab(path: Path) -> int:
	"""Area of the biggest pale flat region, but only if it is BAR-SHAPED.

	Area alone cannot tell a stripe from legitimate art: the win-celebration
	hero plate is a large flat warm rectangle and tripped this on every frame it
	was on screen, which is exactly the kind of noise that gets a guard ignored.
	The artifacts this exists to catch are bars and stripes, so a region only
	counts when it is thin in one direction (an upright or flat bar) or fills
	little of its own bounding box (a diagonal band cutting across a cell). A
	solid plate is thick in both directions AND fills its box, so it stays quiet.
	"""
	rgb = np.asarray(Image.open(path).convert("RGB").crop(BOARD), dtype=np.float32)
	area, fill, thinnest = _largest_region_shape(_blocks(rgb))
	if area < MIN_AREA:
		return 0
	return area if (thinnest <= BAR_THIN_PX or fill <= BAR_FILL_MAX) else 0


def selftest() -> None:
	"""The detector must fire on a synthetic beige diagonal and stay quiet on noise."""
	size = (BOARD[3] - BOARD[1], BOARD[2] - BOARD[0])
	rng = np.random.default_rng(7)

	def verdict(rgb: np.ndarray) -> int:
		area, fill, thinnest = _largest_region_shape(_blocks(rgb))
		if area < MIN_AREA:
			return 0
		return area if (thinnest <= BAR_THIN_PX or fill <= BAR_FILL_MAX) else 0

	noise = rng.integers(20, 90, size=(*size, 3)).astype(np.float32)
	quiet = verdict(noise)

	band = noise.copy()
	yy, xx = np.mgrid[0 : size[0], 0 : size[1]]
	band[np.abs(yy - xx) < 14] = np.array([206.0, 186.0, 150.0])
	diagonal = verdict(band)

	bar = noise.copy()
	bar[:, 200:224] = np.array([206.0, 186.0, 150.0])
	upright = verdict(bar)

	# The win-celebration hero plate is a big flat warm rectangle and is NOT an
	# artifact. It used to fail every frame it was on screen.
	plate = noise.copy()
	plate[60:300, 80:420] = np.array([196.0, 170.0, 132.0])
	art = verdict(plate)

	print(f"selftest: textured board  -> {quiet}px (want 0)")
	print(f"selftest: beige diagonal  -> {diagonal}px (want >={MIN_AREA})")
	print(f"selftest: upright bar     -> {upright}px (want >={MIN_AREA})")
	print(f"selftest: hero art plate  -> {art}px (want 0)")
	ok = quiet == 0 and diagonal >= MIN_AREA and upright >= MIN_AREA and art == 0
	print("selftest:", "PASS" if ok else "FAIL")
	raise SystemExit(0 if ok else 1)


def is_blank(path: Path) -> bool:
	"""True for Storybook's white pre-render page, which passes every check."""
	return float(np.asarray(Image.open(path).convert("L"), dtype=np.float32).mean()) > 200.0


def probe(story: str, stem: str) -> None:
	"""Print the slab area for one frame, to calibrate against a known-bad capture."""
	path = ROOT / story / f"{stem}.jpg"
	rgb = np.asarray(Image.open(path).convert("RGB").crop(BOARD), dtype=np.float32)
	mask = _blocks(rgb)
	print(f"{stem}: {mask.sum()} suspect blocks, largest region {largest_region(mask)}px")
	raise SystemExit(0)


def main() -> None:
	if "--selftest" in sys.argv:
		selftest()
	if "--probe" in sys.argv:
		at = sys.argv.index("--probe")
		probe(sys.argv[at + 1], sys.argv[at + 2])
	# story NAMES, not paths — but accept a path to a capture dir too, since
	# passing one used to resolve to nothing and report a cheerful "ok" over
	# zero frames, which is the worst possible failure mode for a regression
	# guard: every typo passes.
	stories = sys.argv[1:] or [p.name for p in ROOT.iterdir() if p.is_dir()]
	failed = False
	for story in stories:
		folder = Path(story)
		if not folder.is_dir():
			folder = ROOT / Path(story).name
		frames = sorted(folder.glob("f*.jpg"))
		if not frames:
			print(f"[FAIL] {story}: no frames found under {folder}")
			failed = True
			continue
		hairlines: list[str] = []
		slabs: list[tuple[str, int]] = []
		blank = 0
		for frame in frames:
			if is_blank(frame):
				blank += 1
				continue
			if scan_hairlines(frame):
				hairlines.append(frame.name)
			area = scan_flat_slab(frame)
			if area >= MIN_AREA:
				slabs.append((frame.name, area))
		# A capture that never got past Storybook's white "Initialising..." page
		# has nothing on it to find, and a white page is neither warm nor
		# hairlined — so it scores a clean pass. A 614-frame run of those once
		# reported "ok" while the feature under test had not rendered at all.
		if blank > len(frames) // 2:
			print(f"[FAIL] {story}: {blank}/{len(frames)} frames never rendered (blank page)")
			failed = True
			continue
		bad = hairlines or slabs
		failed = failed or bool(bad)
		print(f"[{'FAIL' if bad else 'ok'}] {story}: {len(frames)} frames, "
			f"{len(hairlines)} hairline, {len(slabs)} flat-slab")
		# name the offenders: "3 hairline" with no frame to open is useless
		for name in hairlines[:6]:
			print(f"         hairline {name}")
		for name, area in slabs[:6]:
			print(f"         slab {name} {area}px")
	raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
	main()
