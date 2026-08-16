"""Stake tile layers for Tombstone Reborn.

Same contract as tools/make_game_tile.py (THE WHITE ROOM):
  TombstoneReborn-BG.jpg   1024x1536 empty scene, no character, no title
  TombstoneReborn-FG.png   1024x1536 gunslinger bust, transparent

The tile editor composites Background + Foreground + Game Title itself, so
these two files must stay separate. Outputs go to submission/ — not static/ —
so they never ship in the player download.

Sources: generated masters in the Cursor assets folder, copied into
assets-raw/tile/ the first time this runs.

Run:  python tools/make_tombstone_tile.py
"""

from __future__ import annotations

import os
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
RAW = os.path.join(APP, "assets-raw", "tile")
OUT = os.path.join(APP, "submission")
GEN = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"

W, H = 1024, 1536
SENTINEL = (255, 0, 255)
FLOOD_THRESH = 24

sys.path.insert(0, HERE)
from alpha_key import ALPHA_FLOOR, bleed_alpha  # noqa: E402


def cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
	tw, th = size
	scale = max(tw / img.width, th / img.height)
	w, h = round(img.width * scale), round(img.height * scale)
	img = img.resize((w, h), Image.LANCZOS)
	return img.crop(((w - tw) // 2, (h - th) // 2, (w - tw) // 2 + tw, (h - th) // 2 + th))


def lift_edges(img: Image.Image) -> Image.Image:
	"""Wash the outer frame toward bone-cream.

	Stake rejected a tile for dark edges. This graveyard has charcoal fence
	posts that sit on the left/right crop, so a radial lift is not enough —
	blend every pixel within FADE px of the frame toward cream, harder where
	the source is dark.
	"""
	px = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
	yy, xx = np.mgrid[0:H, 0:W]
	dist = np.minimum.reduce([xx, yy, W - 1 - xx, H - 1 - yy]).astype(np.float32)
	fade = 110.0
	t = np.clip(1.0 - dist / fade, 0.0, 1.0) ** 1.15
	luma = px[..., 0] * 0.299 + px[..., 1] * 0.587 + px[..., 2] * 0.114
	dark = np.clip((0.62 - luma) / 0.62, 0.0, 1.0)
	mix = np.clip(t * (0.42 + 0.58 * dark), 0.0, 1.0)[..., None]
	cream = np.array([0.975, 0.955, 0.88], dtype=np.float32)
	px = px * (1.0 - mix) + cream * mix
	return Image.fromarray((np.clip(px, 0, 1) * 255).astype(np.uint8), "RGB")


def darkest_border(img: Image.Image, band: int = 24) -> tuple[float, tuple[int, int]]:
	px = np.asarray(img.convert("RGB"), dtype=np.float32)
	lum = px[..., 0] * 0.299 + px[..., 1] * 0.587 + px[..., 2] * 0.114
	edge = np.full_like(lum, 255.0)
	edge[:band] = lum[:band]
	edge[-band:] = lum[-band:]
	edge[:, :band] = lum[:, :band]
	edge[:, -band:] = lum[:, -band:]
	y, x = np.unravel_index(int(edge.argmin()), edge.shape)
	return float(edge[y, x]), (int(x), int(y))


def key_white(img: Image.Image) -> Image.Image:
	"""Flood near-white studio pad from the border, keep the bust."""
	work = cover(img.convert("RGB"), (W, H))
	flood = work.copy()
	seeds = [
		(0, 0),
		(W - 1, 0),
		(0, H - 1),
		(W - 1, H - 1),
		(W // 2, 0),
		(W // 2, H - 1),
		(0, H // 2),
		(W - 1, H // 2),
	]
	for seed in seeds:
		if flood.getpixel(seed) != SENTINEL:
			ImageDraw.floodfill(flood, seed, SENTINEL, thresh=FLOOD_THRESH)

	marked = np.asarray(flood)
	is_bg = (marked[..., 0] == SENTINEL[0]) & (marked[..., 1] == SENTINEL[1]) & (
		marked[..., 2] == SENTINEL[2]
	)
	alpha = np.where(is_bg, 0, 255).astype(np.uint8)
	alpha_img = Image.fromarray(alpha, "L")
	# chew the 1px white fringe, then soften the cut
	alpha_img = alpha_img.filter(ImageFilter.MinFilter(3))
	alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(0.8))

	out = work.convert("RGBA")
	out.putalpha(alpha_img)
	out = bleed_alpha(out)
	data = np.array(out)
	data[data[..., 3] <= ALPHA_FLOOR] = (0, 0, 0, 0)
	return Image.fromarray(data, "RGBA")


def ensure_masters() -> tuple[str, str]:
	os.makedirs(RAW, exist_ok=True)
	bg_src = os.path.join(GEN, "tile_bg_cream.png")
	fg_src = os.path.join(GEN, "tile_fg_gunslinger_face.png")
	bg_dst = os.path.join(RAW, "scene.png")
	fg_dst = os.path.join(RAW, "hero_face.png")
	for src, dst in ((bg_src, bg_dst), (fg_src, fg_dst)):
		if not os.path.isfile(src) and not os.path.isfile(dst):
			raise SystemExit(f"missing master: {src}")
		if os.path.isfile(src):
			shutil.copy2(src, dst)
	return bg_dst, fg_dst


if __name__ == "__main__":
	os.makedirs(OUT, exist_ok=True)
	bg_master, fg_master = ensure_masters()

	background = lift_edges(cover(Image.open(bg_master).convert("RGB"), (W, H)))
	bg_path = os.path.join(OUT, "TombstoneReborn-BG.jpg")
	background.save(bg_path, quality=93, subsampling=0)

	foreground = key_white(Image.open(fg_master))
	opaque = int((np.asarray(foreground)[..., 3] > ALPHA_FLOOR).sum())
	if opaque < 80_000:
		raise SystemExit(f"FG keyed to almost nothing ({opaque} opaque px) — loosen FLOOD_THRESH")
	fg_path = os.path.join(OUT, "TombstoneReborn-FG.png")
	foreground.save(fg_path, optimize=True, compress_level=9)

	total = (os.path.getsize(bg_path) + os.path.getsize(fg_path)) / 1e6
	darkest, at = darkest_border(background)
	print(f"bg   -> {bg_path}")
	print(f"        darkest border pixel {darkest:.0f}/255 at {at}")
	print(f"fg   -> {fg_path}")
	print(f"        opaque px {opaque:,}")
	print(f"BG + FG = {total:.2f} MB (Stake limit 3 MB)")
