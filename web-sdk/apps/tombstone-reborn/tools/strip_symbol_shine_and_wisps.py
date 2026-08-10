"""
1) Kill remaining warm wisps on wild cards (force to cool gunsmoke).
2) Kill clinical diagonal glass shine bands across ALL paying symbol tiles
   in symbolsStatic (bright near-white diagonal streaks).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "static" / "assets" / "sprites" / "mirror"
SYMBOLS = ROOT / "static" / "assets" / "sprites" / "symbolsStatic"
SMOKE = ROOT / "assets-raw" / "kenney_haul_western" / "yellow_fx_replace" / "blackSmoke08.png"


def kill_warm_wisps(arr: np.ndarray) -> np.ndarray:
	out = arr.astype(np.float64).copy()
	r, g, b, a = out[..., 0], out[..., 1], out[..., 2], out[..., 3]
	lum = 0.299 * r + 0.587 * g + 0.114 * b
	# anything with warm chroma relative to blue
	warm = (a > 8) & ((r + g) * 0.5 > b + 12) & (lum > 28) & (lum < 230)
	# also any yellow-tan fringe
	tan = (a > 8) & (r > 70) & (g > 55) & (b < r - 15) & (b < g + 5)
	mask = warm | tan
	# solid gun body stays if dark and low sat
	sat = (np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)) / np.maximum(
		np.maximum(np.maximum(r, g), b), 1
	)
	body = (a > 200) & (lum < 90) & (sat < 0.22)
	mask = mask & ~body

	# force cool gunsmoke
	r[mask] = lum[mask] * 0.35 + 14
	g[mask] = lum[mask] * 0.34 + 13
	b[mask] = lum[mask] * 0.33 + 12
	a[mask] = np.clip(a[mask] * 0.92, 0, 255)

	# second pass: leftover yellow chroma
	still = (a > 8) & (r > b + 18) & (g > b + 8)
	avg = (r + g + b) / 3.0
	r[still] = avg[still] * 0.9
	g[still] = avg[still] * 0.88
	b[still] = avg[still] * 0.86

	out[..., 0] = r
	out[..., 1] = g
	out[..., 2] = b
	out[..., 3] = a
	return np.clip(out, 0, 255).astype(np.uint8)


def kill_diagonal_shine(arr: np.ndarray) -> np.ndarray:
	"""Suppress bright near-white diagonal glass bands on a 300x300 card."""
	out = arr.astype(np.float64).copy()
	r, g, b, a = out[..., 0], out[..., 1], out[..., 2], out[..., 3]
	lum = 0.299 * r + 0.587 * g + 0.114 * b
	h, w = lum.shape
	yy, xx = np.mgrid[0:h, 0:w]
	# diagonal band family (top-left → bottom-right), a few offsets
	diag = (xx - yy).astype(np.float64)
	shine = np.zeros_like(lum, dtype=bool)
	for center in (-40, -10, 20, 50, 80):
		band = np.abs(diag - center) < 14
		bright = (lum > 145) & (a > 40) & (np.abs(r - g) < 35) & (np.abs(g - b) < 40)
		shine |= band & bright
	# also any very bright desaturated streak anywhere (clinical glass)
	glass = (lum > 175) & (a > 30) & (a < 250) & (np.abs(r - g) < 28) & (np.abs(g - b) < 28) & (
		sat_of(r, g, b) < 0.18
	)
	mask = shine | glass
	# pull down to local neighborhood darkness
	r[mask] = r[mask] * 0.35 + 25
	g[mask] = g[mask] * 0.35 + 22
	b[mask] = b[mask] * 0.35 + 18
	a[mask] = np.clip(a[mask] * 0.95, 0, 255)
	out[..., 0] = r
	out[..., 1] = g
	out[..., 2] = b
	out[..., 3] = a
	return np.clip(out, 0, 255).astype(np.uint8)


def sat_of(r, g, b):
	mx = np.maximum(np.maximum(r, g), b)
	mn = np.minimum(np.minimum(r, g), b)
	return (mx - mn) / np.maximum(mx, 1)


def main():
	for name in ("wr_wild.png", "wr_wild_expand.png"):
		path = MIRROR / name
		arr = kill_warm_wisps(np.array(Image.open(path).convert("RGBA")))
		Image.fromarray(arr, "RGBA").save(path, optimize=True)
		print("WISP", path)

	png = SYMBOLS / "symbolsStatic.png"
	meta = json.loads((SYMBOLS / "symbolsStatic.json").read_text(encoding="utf-8"))
	arr = np.array(Image.open(png).convert("RGBA"))
	keys = [
		k
		for k in meta["frames"]
		if k.endswith((".webp", ".png"))
		and not k.endswith("_blur.webp")
		and not k.endswith("_blur.png")
		and "exploded" not in k
	]
	for key in keys:
		fr = meta["frames"][key]["frame"]
		x, y, w, h = fr["x"], fr["y"], fr["w"], fr["h"]
		tile = arr[y : y + h, x : x + w].copy()
		if key.startswith("w"):
			tile = kill_warm_wisps(tile)
		tile = kill_diagonal_shine(tile)
		arr[y : y + h, x : x + w] = tile
		print("SHINE", key)
	Image.fromarray(arr, "RGBA").save(png, optimize=True)
	Image.fromarray(arr, "RGBA").save(SYMBOLS / "symbolsStatic.webp", "WEBP", quality=90)
	print("OK")


if __name__ == "__main__":
	main()
