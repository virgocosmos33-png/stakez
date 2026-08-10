"""Hard pass: erase remaining warm/yellow wisps on wild card into gunsmoke grey."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "static" / "assets" / "sprites" / "mirror"
SYMBOLS = ROOT / "static" / "assets" / "sprites" / "symbolsStatic"
import json


def hard_deyellow(arr: np.ndarray) -> np.ndarray:
	out = arr.astype(np.float64).copy()
	r, g, b, a = out[..., 0], out[..., 1], out[..., 2], out[..., 3]
	# warm pixels: R+G dominate B (gold / amber / yellow energy)
	warm = (a > 18) & ((r + g) > (b * 2.05 + 40)) & (r > 55) & (g > 40)
	# bright yellow-ish
	bright = warm & (r > 120) & (g > 90) & (b < 140)
	# soft amber wisps
	wisp = warm & ~bright

	lum = 0.299 * r + 0.587 * g + 0.114 * b

	# wisps → cool gunsmoke grey-brown
	r[wisp] = lum[wisp] * 0.55 + 28
	g[wisp] = lum[wisp] * 0.5 + 24
	b[wisp] = lum[wisp] * 0.48 + 22
	a[wisp] = np.clip(a[wisp] * 0.85, 0, 255)

	# bright gold sparks / bullet flare → dim brass dust, not neon
	r[bright] = lum[bright] * 0.5 + 40
	g[bright] = lum[bright] * 0.42 + 32
	b[bright] = lum[bright] * 0.28 + 18
	a[bright] = np.clip(a[bright] * 0.75, 0, 255)

	# thin gold border → iron
	border = (a > 160) & (r > 100) & (g > 70) & (b < 100) & ((r + g) > b * 2.3)
	r[border] = 55
	g[border] = 48
	b[border] = 40

	out[..., 0] = r
	out[..., 1] = g
	out[..., 2] = b
	out[..., 3] = a
	return np.clip(out, 0, 255).astype(np.uint8)


def main():
	for name in ("wr_wild.png", "wr_wild_expand.png"):
		path = MIRROR / name
		im = np.array(Image.open(path).convert("RGBA"))
		Image.fromarray(hard_deyellow(im), "RGBA").save(path, optimize=True)
		print("HARD", path)

	png = SYMBOLS / "symbolsStatic.png"
	meta = json.loads((SYMBOLS / "symbolsStatic.json").read_text(encoding="utf-8"))
	arr = np.array(Image.open(png).convert("RGBA"))
	for key in ("w.png", "w_burn.png"):
		fr = meta["frames"][key]["frame"]
		x, y, w, h = fr["x"], fr["y"], fr["w"], fr["h"]
		arr[y : y + h, x : x + w] = hard_deyellow(arr[y : y + h, x : x + w].copy())
	Image.fromarray(arr, "RGBA").save(png, optimize=True)
	Image.fromarray(arr, "RGBA").save(SYMBOLS / "symbolsStatic.webp", "WEBP", quality=90)
	print("HARD symbolsStatic w")


if __name__ == "__main__":
	main()
