"""Force-blank section_magenta* plates: zero baked glyph ink.

Dark letter stems are NOT magenta — magenta-only masks leave holes.
Use alpha silhouette + close/fill, then paint the entire interior.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT.parents[1] / "packages" / "components-ui-html" / "src" / "assets" / "paytable"
STATIC = ROOT / "static" / "assets" / "paytable_ui"
TMP = ROOT / ".tmp_paytable_chrome"
NM = ROOT / "node_modules" / "components-ui-html" / "src" / "assets" / "paytable"
TARGETS = [PKG, STATIC, NM]

# Locked stroke paint (matches SPECIAL SYMBOLS family)
TARGET = np.array([208.0, 38.0, 108.0], dtype=np.float32)


def load_rgba(path: Path) -> np.ndarray:
	return np.array(Image.open(path).convert("RGBA"), dtype=np.uint8)


def is_magenta(rgb: np.ndarray, al: np.ndarray) -> np.ndarray:
	r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
	return (al > 40) & (r > 140) & (r > g * 1.4) & (r > b * 1.2) & ((r - g) > 40)


def silhouette(a: np.ndarray) -> np.ndarray:
	al = a[..., 3] > 40
	al = ndimage.binary_opening(al, iterations=1)
	closed = ndimage.binary_closing(al, iterations=5)
	filled = ndimage.binary_fill_holes(closed)
	labeled, n = ndimage.label(filled)
	if n == 0:
		return filled
	counts = np.bincount(labeled.ravel())
	counts[0] = 0
	return labeled == counts.argmax()


def paint_magenta(rgb: np.ndarray, mask: np.ndarray, rng: np.random.Generator, sigma: float = 3.5) -> None:
	"""Write locked magenta + grain; clamp so every pixel stays magenta."""
	if not mask.any():
		return
	grain = rng.normal(0, sigma, size=(int(mask.sum()), 3))
	vals = TARGET + grain
	# Keep R dominant / vivid
	vals[:, 0] = np.clip(vals[:, 0], 185, 235)
	vals[:, 1] = np.clip(vals[:, 1], 18, 70)
	vals[:, 2] = np.clip(vals[:, 2], 70, 140)
	# Enforce r > g*1.4 and r-g > 40
	vals[:, 1] = np.minimum(vals[:, 1], vals[:, 0] / 1.45 - 1)
	vals[:, 2] = np.minimum(vals[:, 2], vals[:, 0] / 1.25 - 1)
	rgb[mask] = vals


def blank_plate(arr: np.ndarray, edge_keep: int = 4) -> np.ndarray:
	out = arr.copy()
	rgb = out[..., :3].astype(np.float32)
	al = out[..., 3].astype(np.uint8)
	body = silhouette(out)
	if not body.any():
		return out

	mag = is_magenta(rgb, al)
	# Preserve only a thin ORIGINAL magenta edge ring for distress
	eroded = ndimage.binary_erosion(body, iterations=edge_keep)
	edge_ring = body & ~eroded
	keep_edge = edge_ring & mag

	rng = np.random.default_rng(19)
	# Paint everything in body that is NOT the preserved edge
	fill = body & ~keep_edge
	paint_magenta(rgb, fill, rng, sigma=3.5)

	# Paranoia: any remaining non-magenta / dark in body → paint
	mag2 = is_magenta(rgb, al)
	lum = rgb.mean(axis=2)
	bad = body & (~mag2 | (lum < 140) | (rgb[..., 0] < 170))
	# Don't destroy preserved edge unless it's actually ink
	bad_edge_ink = keep_edge & ((lum < 120) | (rgb[..., 0] < 150) | ~mag2)
	paint_magenta(rgb, (bad & ~keep_edge) | bad_edge_ink, rng, sigma=2.5)

	# Repair alpha holes inside deep interior
	deep = ndimage.binary_erosion(body, iterations=edge_keep + 2)
	al[deep & (al < 220)] = 255

	out[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
	out[..., 3] = al
	return out


def residual_ink(arr: np.ndarray) -> int:
	"""True leftover glyph ink: dark / low-R pixels inside the stroke body."""
	body = silhouette(arr)
	interior = ndimage.binary_erosion(body, iterations=3)
	rgb = arr[..., :3].astype(np.float32)
	# Vivid stroke paint sits ~R208; glyph stems are much darker / low-R
	return int((interior & (rgb[..., 0] < 170)).sum())


def save_sync(name: str, arr: np.ndarray) -> None:
	im = Image.fromarray(arr, "RGBA")
	for d in TARGETS:
		d.mkdir(parents=True, exist_ok=True)
		dest = d / name
		im.save(dest, optimize=True)
		print(f"  wrote {dest} ({dest.stat().st_size} bytes)")
	TMP.mkdir(parents=True, exist_ok=True)
	im.save(TMP / f"blanked_{name}")
	# ink debug (green = bad low-R)
	body = silhouette(arr)
	interior = ndimage.binary_erosion(body, iterations=3)
	rgb = arr[..., :3].astype(np.float32)
	bad = interior & (rgb[..., 0] < 170)
	dbg = np.zeros_like(arr)
	dbg[body] = [200, 40, 120, 255]
	dbg[bad] = [0, 255, 0, 255]
	Image.fromarray(dbg).save(TMP / f"inkmap_{name}")


def pick_source(name: str) -> Path:
	"""Prefer from_ref (has full glyph holes to prove fill works), else shipped."""
	candidates = [
		TMP / name.replace(".png", "_from_ref.png"),
		PKG / name,
	]
	for c in candidates:
		if c.exists():
			return c
	raise FileNotFoundError(name)


def main() -> None:
	for name in ("section_magenta.png", "section_magenta_wide.png"):
		src = pick_source(name)
		print(f"\n=== blank {name} from {src.name} ===")
		raw = load_rgba(src)
		shipped = PKG / name
		if shipped.exists():
			tw, th = Image.open(shipped).size
			if (raw.shape[1], raw.shape[0]) != (tw, th):
				raw = np.array(Image.fromarray(raw, "RGBA").resize((tw, th), Image.NEAREST))
				print(f"  resized -> {(tw, th)}")
		print(f"  before residual_ink={residual_ink(raw)}")
		edge = 3 if "wide" in name else 5
		cleaned = blank_plate(raw, edge_keep=edge)
		cleaned = blank_plate(cleaned, edge_keep=edge)
		ink = residual_ink(cleaned)
		print(f"  after  residual_ink={ink}")
		if ink != 0:
			# Last-resort: paint 100% of eroded body with zero edge keep on third pass
			cleaned = blank_plate(cleaned, edge_keep=2)
			ink = residual_ink(cleaned)
			print(f"  after3 residual_ink={ink}")
		assert ink == 0, f"residual ink remains: {ink}"
		save_sync(name, cleaned)

	print("\nDone. Hard-refresh (Ctrl+Shift+R) so Vite drops cached PNGs.")


if __name__ == "__main__":
	main()
