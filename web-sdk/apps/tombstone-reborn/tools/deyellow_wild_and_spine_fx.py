"""
Strip Madam/clinical yellow energy from Tombstone wild cards + Spine FX frames.

Edits in place under static/assets (junctioned as assets/):
  - sprites/mirror/wr_wild.png
  - sprites/mirror/wr_wild_expand.png
  - sprites/symbolsStatic/symbolsStatic.png (w.png / w_burn.png frames)
  - spines/mm_symbols/mm_symbols.png (+ .webp) fx_streak / fx_wisp / fx_ring / shards

Yellow wisps → gunsmoke grey / dusty amber. White clinical FX → dusty brown smoke masks.
Keeps dark steel / wood; softens neon-gold borders toward iron.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "static" / "assets"
MIRROR = STATIC / "sprites" / "mirror"
SYMBOLS = STATIC / "sprites" / "symbolsStatic"
SPINE = STATIC / "spines" / "mm_symbols"
KENNEY = ROOT / "assets-raw" / "kenney_haul_western" / "yellow_fx_replace"


def rgb_to_hsv(r: np.ndarray, g: np.ndarray, b: np.ndarray):
	r = r / 255.0
	g = g / 255.0
	b = b / 255.0
	mx = np.maximum(np.maximum(r, g), b)
	mn = np.minimum(np.minimum(r, g), b)
	df = mx - mn
	h = np.zeros_like(mx)
	mask = df > 1e-6
	# red
	idx = mask & (mx == r)
	h[idx] = ((g[idx] - b[idx]) / df[idx]) % 6
	# green
	idx = mask & (mx == g)
	h[idx] = (b[idx] - r[idx]) / df[idx] + 2
	# blue
	idx = mask & (mx == b)
	h[idx] = (r[idx] - g[idx]) / df[idx] + 4
	h = h / 6.0
	s = np.where(mx > 1e-6, df / mx, 0.0)
	v = mx
	return h, s, v


def hsv_to_rgb(h: np.ndarray, s: np.ndarray, v: np.ndarray):
	h6 = h * 6.0
	i = np.floor(h6).astype(np.int32) % 6
	f = h6 - np.floor(h6)
	p = v * (1.0 - s)
	q = v * (1.0 - s * f)
	t = v * (1.0 - s * (1.0 - f))
	out = np.zeros(h.shape + (3,), dtype=np.float64)
	for ii, (a, b, c) in enumerate(
		[(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]
	):
		m = i == ii
		out[..., 0][m] = a[m]
		out[..., 1][m] = b[m]
		out[..., 2][m] = c[m]
	return out[..., 0], out[..., 1], out[..., 2]


def deyellow_rgba(arr: np.ndarray) -> np.ndarray:
	"""Push yellow/gold energy toward dusty gunsmoke; keep dark metals."""
	out = arr.astype(np.float64).copy()
	r, g, b, a = out[..., 0], out[..., 1], out[..., 2], out[..., 3]
	h, s, v = rgb_to_hsv(r, g, b)

	# yellow / amber / neon-gold hues (approx 20°–70°)
	yellow = (a > 20) & (s > 0.18) & (v > 0.22) & (
		((h >= 0.05) & (h <= 0.20)) | ((r > g * 0.85) & (g > b * 1.15) & (r > 90))
	)
	# hot cylinder / bullet flare (very bright yellow)
	hot = yellow & (v > 0.55) & (s > 0.35)
	# soft wisps (mid sat / mid value)
	wisp = yellow & ~hot

	# target dusty hues ~ brown/gunsmoke
	dust_h = np.full_like(h, 0.09)  # warm brown
	smoke_h = np.full_like(h, 0.08)

	# wisps → low-sat gunsmoke
	h[wisp] = smoke_h[wisp]
	s[wisp] = np.clip(s[wisp] * 0.28 + 0.08, 0, 0.45)
	v[wisp] = np.clip(v[wisp] * 0.62, 0, 0.55)

	# hot gold → dim spent brass / powder, not neon
	h[hot] = dust_h[hot]
	s[hot] = np.clip(s[hot] * 0.4, 0, 0.5)
	v[hot] = np.clip(v[hot] * 0.55, 0, 0.62)

	# thin neon-gold card border: high sat, near-edge-ish yellow line
	# soften any remaining bright yellow outline to iron
	borderish = (a > 180) & (s > 0.35) & (v > 0.45) & (r > 140) & (g > 100) & (b < 110)
	h[borderish] = 0.07
	s[borderish] = np.clip(s[borderish] * 0.25, 0, 0.35)
	v[borderish] = np.clip(v[borderish] * 0.45, 0, 0.4)

	nr, ng, nb = hsv_to_rgb(h, s, v)
	out[..., 0] = nr * 255
	out[..., 1] = ng * 255
	out[..., 2] = nb * 255
	return np.clip(out, 0, 255).astype(np.uint8)


def tint_mask_to_dust(mask: Image.Image, size: tuple[int, int], color=(110, 96, 72)) -> Image.Image:
	"""Turn a white Kenney / clinical mask into dusty western smoke."""
	m = mask.convert("L").resize(size, Image.Resampling.LANCZOS)
	arr = np.array(m, dtype=np.float64) / 255.0
	rgba = np.zeros(size[::-1] + (4,), dtype=np.uint8)  # H,W,4 but size is W,H
	# size is (w,h); array is (h,w)
	h, w = size[1], size[0]
	rgba = np.zeros((h, w, 4), dtype=np.float64)
	rgba[..., 0] = color[0]
	rgba[..., 1] = color[1]
	rgba[..., 2] = color[2]
	rgba[..., 3] = arr * 220
	return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA")


def paste_region(sheet: Image.Image, region: Image.Image, box: tuple[int, int, int, int]):
	x, y, w, h = box
	sheet.paste(region.resize((w, h), Image.Resampling.LANCZOS), (x, y))


def process_wild_pngs():
	for name in ("wr_wild.png", "wr_wild_expand.png"):
		path = MIRROR / name
		if not path.exists():
			print("MISS", path)
			continue
		bak = path.with_suffix(".pre_deyellow.bak.png")
		if not bak.exists():
			Image.open(path).save(bak)
		im = Image.open(path).convert("RGBA")
		out = Image.fromarray(deyellow_rgba(np.array(im)), "RGBA")
		out.save(path, optimize=True)
		print("WROTE", path)


def process_symbols_static_w():
	png = SYMBOLS / "symbolsStatic.png"
	meta = SYMBOLS / "symbolsStatic.json"
	if not png.exists() or not meta.exists():
		print("MISS symbolsStatic")
		return
	bak = png.with_suffix(".pre_deyellow.bak.png")
	if not bak.exists():
		Image.open(png).save(bak)
	data = json.loads(meta.read_text(encoding="utf-8"))
	sheet = Image.open(png).convert("RGBA")
	arr = np.array(sheet)
	for key in ("w.png", "w_burn.png"):
		fr = data["frames"].get(key, {}).get("frame")
		if not fr:
			print("MISS frame", key)
			continue
		x, y, w, h = fr["x"], fr["y"], fr["w"], fr["h"]
		tile = arr[y : y + h, x : x + w].copy()
		arr[y : y + h, x : x + w] = deyellow_rgba(tile)
		print("PATCHED symbolsStatic", key)
	Image.fromarray(arr, "RGBA").save(png, optimize=True)
	webp = SYMBOLS / "symbolsStatic.webp"
	if webp.exists():
		Image.fromarray(arr, "RGBA").save(webp, "WEBP", quality=90)
		print("WROTE", webp)


def process_spine_fx():
	atlas_png = SPINE / "mm_symbols.png"
	if not atlas_png.exists():
		print("MISS", atlas_png)
		return
	bak = atlas_png.with_suffix(".pre_deyellow.bak.png")
	if not bak.exists():
		Image.open(atlas_png).save(bak)

	sheet = Image.open(atlas_png).convert("RGBA")
	# atlas bounds from mm_symbols.atlas
	regions = {
		"fx_streak": (2, 1212, 140, 460),
		"fx_wisp": (144, 1212, 96, 96),
		"fx_ring": (242, 1212, 176, 176),
		"fx_shard_a": (420, 1212, 64, 64),
		"fx_shard_b": (486, 1212, 64, 64),
		"fx_shard_c": (552, 1212, 64, 64),
	}

	smoke = KENNEY / "smoke_05.png"
	puff = KENNEY / "whitePuff08.png"
	circle = KENNEY / "circle_b.png"
	dirt = KENNEY / "dirt_01.png"
	flash = KENNEY / "flash00.png"

	# streak → soft dusty slash (not clinical white needle)
	src = Image.open(puff if puff.exists() else smoke).convert("RGBA")
	paste_region(sheet, tint_mask_to_dust(src, (140, 460), (90, 78, 58)), regions["fx_streak"])

	# wisp → gunsmoke blob
	src = Image.open(smoke if smoke.exists() else puff).convert("RGBA")
	paste_region(sheet, tint_mask_to_dust(src, (96, 96), (100, 88, 68)), regions["fx_wisp"])

	# ring → iron sight ring (dust, not white glow)
	src = Image.open(circle if circle.exists() else puff).convert("RGBA")
	paste_region(sheet, tint_mask_to_dust(src, (176, 176), (120, 100, 70)), regions["fx_ring"])

	# shards → dirt / flash crumbs
	for key, path, color in (
		("fx_shard_a", dirt, (120, 90, 55)),
		("fx_shard_b", flash, (140, 110, 70)),
		("fx_shard_c", dirt, (90, 75, 55)),
	):
		src = Image.open(path if path.exists() else smoke).convert("RGBA")
		x, y, w, h = regions[key]
		paste_region(sheet, tint_mask_to_dust(src, (w, h), color), regions[key])

	# also deyellow card tiles in the same atlas (w / highs may still carry gold)
	for bounds in (
		(606, 606, 300, 300),  # w
		(2, 2, 300, 300),
		(304, 2, 300, 300),
		(606, 2, 300, 300),
		(908, 2, 300, 300),
		(2, 304, 300, 300),
		(304, 304, 300, 300),
		(606, 304, 300, 300),
		(908, 304, 300, 300),
		(2, 606, 300, 300),
		(304, 606, 300, 300),
		(908, 606, 300, 300),
		(2, 908, 300, 300),
		(304, 908, 300, 300),
	):
		x, y, w, h = bounds
		tile = np.array(sheet.crop((x, y, x + w, y + h)))
		sheet.paste(Image.fromarray(deyellow_rgba(tile), "RGBA"), (x, y))

	sheet.save(atlas_png, optimize=True)
	webp = SPINE / "mm_symbols.webp"
	sheet.save(webp, "WEBP", quality=90)
	print("WROTE", atlas_png, webp)


def main():
	process_wild_pngs()
	process_symbols_static_w()
	process_spine_fx()
	print("OK deyellow pass complete")


if __name__ == "__main__":
	main()
