"""
Nuclear strip of golden/yellow energy from wr_wild art.
Any warm mid-tone smoke pixel → gunsmoke grey. Keeps dark steel body.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "static" / "assets" / "sprites" / "mirror"
SYMBOLS = ROOT / "static" / "assets" / "sprites" / "symbolsStatic"
KENNEY_SMOKE = ROOT / "assets-raw" / "kenney_haul_western" / "yellow_fx_replace" / "blackSmoke08.png"


def strip_warm(arr: np.ndarray) -> np.ndarray:
	out = arr.astype(np.float64).copy()
	r, g, b, a = out[..., 0], out[..., 1], out[..., 2], out[..., 3]
	lum = 0.299 * r + 0.587 * g + 0.114 * b

	# Broad warm detection (covers soft yellow smoke the soft pass missed)
	warm = (a > 12) & (r + 8 > b) & (g + 5 > b) & ((r + g) > (1.55 * b + 25)) & (lum > 35)
	# Soft fringe smoke (semi-transparent warm)
	fringe = warm & (a < 220) & (lum < 200)
	# Hot gold cores
	core = warm & ((r > 100) | (lum > 140)) & ((r + g) > (2.0 * b + 30))

	# Replace warm smoke with gunsmoke grey matching luminance
	smoke_r = lum * 0.42 + 18
	smoke_g = lum * 0.40 + 16
	smoke_b = lum * 0.38 + 14

	r[fringe] = smoke_r[fringe]
	g[fringe] = smoke_g[fringe]
	b[fringe] = smoke_b[fringe]
	a[fringe] = np.clip(a[fringe] * 0.9, 0, 255)

	r[core] = smoke_r[core] * 0.9 + 10
	g[core] = smoke_g[core] * 0.85 + 8
	b[core] = smoke_b[core] * 0.8 + 6
	a[core] = np.clip(a[core] * 0.7, 0, 255)

	# Kill residual yellow chroma: if still yellower than grey, pull to grey
	still = (a > 12) & (r > b + 25) & (g > b + 10) & (r > 60)
	avg = (r + g + b) / 3.0
	r[still] = avg[still] * 0.95 + 8
	g[still] = avg[still] * 0.9 + 6
	b[still] = avg[still] * 0.85 + 5

	out[..., 0] = r
	out[..., 1] = g
	out[..., 2] = b
	out[..., 3] = a
	return np.clip(out, 0, 255).astype(np.uint8)


def overlay_kenney_dust(im: Image.Image) -> Image.Image:
	"""Optional soft dust swirl from Kenney black smoke, tinted brown-grey."""
	if not KENNEY_SMOKE.exists():
		return im
	base = im.convert("RGBA")
	smoke = Image.open(KENNEY_SMOKE).convert("L").resize(base.size, Image.Resampling.LANCZOS)
	smoke = smoke.filter(ImageFilter.GaussianBlur(1.2))
	arr = np.array(base).astype(np.float64)
	m = np.array(smoke, dtype=np.float64) / 255.0
	# only add dust where alpha already has atmosphere (not solid black void edges)
	alpha = arr[..., 3] / 255.0
	mix = m * 0.18 * np.clip(alpha, 0, 1)
	arr[..., 0] = arr[..., 0] * (1 - mix) + (70 * mix)
	arr[..., 1] = arr[..., 1] * (1 - mix) + (62 * mix)
	arr[..., 2] = arr[..., 2] * (1 - mix) + (52 * mix)
	return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")


def main():
	for name in ("wr_wild.png", "wr_wild_expand.png"):
		path = MIRROR / name
		im = Image.open(path).convert("RGBA")
		out = Image.fromarray(strip_warm(np.array(im)), "RGBA")
		out = overlay_kenney_dust(out)
		out.save(path, optimize=True)
		print("STRIP", path)

	png = SYMBOLS / "symbolsStatic.png"
	meta = json.loads((SYMBOLS / "symbolsStatic.json").read_text(encoding="utf-8"))
	arr = np.array(Image.open(png).convert("RGBA"))
	for key in ("w.png", "w_burn.png"):
		fr = meta["frames"][key]["frame"]
		x, y, w, h = fr["x"], fr["y"], fr["w"], fr["h"]
		tile = Image.fromarray(strip_warm(arr[y : y + h, x : x + w].copy()), "RGBA")
		tile = overlay_kenney_dust(tile)
		arr[y : y + h, x : x + w] = np.array(tile)
	Image.fromarray(arr, "RGBA").save(png, optimize=True)
	Image.fromarray(arr, "RGBA").save(SYMBOLS / "symbolsStatic.webp", "WEBP", quality=90)
	print("STRIP symbolsStatic")


if __name__ == "__main__":
	main()
