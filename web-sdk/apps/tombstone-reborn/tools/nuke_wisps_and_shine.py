"""
Final nuclear pass:
- wild: any pixel warmer/lighter than gun body → cool charcoal smoke
- horseshoe/all cards: detect thin bright diagonal ridges and crush them
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "static" / "assets" / "sprites" / "mirror"
SYMBOLS = ROOT / "static" / "assets" / "sprites" / "symbolsStatic"


def nuke_wisps(arr: np.ndarray) -> np.ndarray:
	out = arr.astype(np.float64).copy()
	r, g, b, a = out[..., 0], out[..., 1], out[..., 2], out[..., 3]
	lum = 0.299 * r + 0.587 * g + 0.114 * b
	mx = np.maximum(np.maximum(r, g), b)
	mn = np.minimum(np.minimum(r, g), b)
	sat = (mx - mn) / np.maximum(mx, 1.0)

	# smoke / energy candidates: not opaque dark metal
	smoke = (a > 5) & (
		((r > b + 8) & (g > b + 2) & (lum > 40))
		| ((lum > 55) & (sat > 0.08) & (r >= g * 0.9) & (r > b))
		| ((a < 200) & (lum > 45) & (r + g > b * 1.4))
	)
	# keep very dark engraved steel
	keep = (a > 220) & (lum < 70) & (sat < 0.25)
	mask = smoke & ~keep

	# charcoal gunsmoke
	r[mask] = 22 + lum[mask] * 0.18
	g[mask] = 20 + lum[mask] * 0.16
	b[mask] = 18 + lum[mask] * 0.14
	a[mask] = np.clip(np.where(a[mask] < 80, a[mask] * 0.5, a[mask] * 0.75), 0, 255)

	# bullet trail: bright small blobs → dim brass dust only
	hot = (a > 40) & (lum > 120) & (r > 90) & (r > b + 20)
	r[hot] = 55
	g[hot] = 48
	b[hot] = 38
	a[hot] = np.clip(a[hot] * 0.55, 0, 255)

	out[..., 0] = r
	out[..., 1] = g
	out[..., 2] = b
	out[..., 3] = a
	return np.clip(out, 0, 255).astype(np.uint8)


def nuke_shine(arr: np.ndarray) -> np.ndarray:
	out = arr.astype(np.float64).copy()
	r, g, b, a = out[..., 0], out[..., 1], out[..., 2], out[..., 3]
	lum = 0.299 * r + 0.587 * g + 0.114 * b
	h, w = lum.shape
	yy, xx = np.mgrid[0:h, 0:w]
	# directional high-pass along diagonal
	# compare each pixel to diagonal-neighborhood mean
	shifted = np.roll(np.roll(lum, 1, axis=0), -1, axis=1)
	ridge = lum - shifted
	bright = (lum > 110) & (a > 20)
	desat = (np.abs(r - g) < 40) & (np.abs(g - b) < 45)
	diag = np.abs((xx - yy) % 28 - 14) < 9  # periodic diagonal strips
	mask = bright & desat & ((ridge > 8) | diag | (lum > 160))

	# crush
	r[mask] = r[mask] * 0.25 + lum[mask] * 0.15
	g[mask] = g[mask] * 0.25 + lum[mask] * 0.14
	b[mask] = b[mask] * 0.25 + lum[mask] * 0.12
	# extra pass for stubborn white bands
	stub = (lum > 140) & desat & (a > 15) & (a < 255)
	r[stub] = np.minimum(r[stub], 55)
	g[stub] = np.minimum(g[stub], 50)
	b[stub] = np.minimum(b[stub], 45)

	out[..., 0] = r
	out[..., 1] = g
	out[..., 2] = b
	out[..., 3] = a
	img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")
	# slight blur on alpha edges only — keep detail by blending 85% original dark
	return np.array(img)


def main():
	for name in ("wr_wild.png", "wr_wild_expand.png"):
		path = MIRROR / name
		Image.fromarray(nuke_wisps(np.array(Image.open(path).convert("RGBA"))), "RGBA").save(
			path, optimize=True
		)
		print("NUKEW", path)

	png = SYMBOLS / "symbolsStatic.png"
	meta = json.loads((SYMBOLS / "symbolsStatic.json").read_text(encoding="utf-8"))
	arr = np.array(Image.open(png).convert("RGBA"))
	for key, fr in meta["frames"].items():
		if "blur" in key or "exploded" in key:
			continue
		f = fr["frame"]
		x, y, w, h = f["x"], f["y"], f["w"], f["h"]
		tile = arr[y : y + h, x : x + w].copy()
		if key.startswith("w"):
			tile = nuke_wisps(tile)
		tile = nuke_shine(tile)
		arr[y : y + h, x : x + w] = tile
	Image.fromarray(arr, "RGBA").save(png, optimize=True)
	Image.fromarray(arr, "RGBA").save(SYMBOLS / "symbolsStatic.webp", "WEBP", quality=88)
	print("NUKE shine sheet")


if __name__ == "__main__":
	main()
