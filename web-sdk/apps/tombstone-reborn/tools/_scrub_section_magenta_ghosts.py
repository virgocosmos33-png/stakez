"""Build truly blank section_magenta* plates (no baked PAYOUT / title glyphs).

Bet Menu bug: HTML "SELECT YOUR BET" sat on a plate with transparent cutouts /
residual PAYOUT stems → vertical black bars under the label.

Pipeline:
  1. Prefer *_from_ref.png (full glyph signal) else shipped plate
  2. Solid plate mask via magenta + morphological close/fill
  3. DIRECT-replace dark ink with plate color + grain (do not rely on
     cv2.inpaint alone — it ignores seeded pixels inside the mask)
  4. Light TELEA only on a thin fringe
  5. Resize + sync package / static / node_modules
"""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT.parents[1] / "packages" / "components-ui-html" / "src" / "assets" / "paytable"
STATIC = ROOT / "static" / "assets" / "paytable_ui"
TMP = ROOT / ".tmp_paytable_chrome"
NM = ROOT / "node_modules" / "components-ui-html" / "src" / "assets" / "paytable"
TARGETS = [PKG, STATIC, NM]

SIZES = {
	"section_magenta.png": (900, 310),
	"section_magenta_wide.png": (1100, 150),
}


def load_rgba(path: Path) -> np.ndarray:
	return np.array(Image.open(path).convert("RGBA"), dtype=np.uint8)


def magenta_mask(rgb: np.ndarray, al: np.ndarray) -> np.ndarray:
	r, g = rgb[..., 0], rgb[..., 1]
	return (r > 80) & (r > g * 1.1) & ((r - g) > 15) & (al > 20)


def solid_plate_mask(a: np.ndarray) -> np.ndarray:
	rgb = a[..., :3].astype(np.float32)
	al = a[..., 3]
	mag = magenta_mask(rgb, al)
	closed = ndimage.binary_closing(mag, iterations=5)
	closed = ndimage.binary_dilation(closed, iterations=1)
	return ndimage.binary_fill_holes(closed)


def blank_plate(src: np.ndarray) -> np.ndarray:
	out = src.copy()
	rgb = out[..., :3].astype(np.float32)
	al = out[..., 3].astype(np.float32)
	lum = rgb.mean(2)

	# key pure black bg
	al = np.where(lum < 22, 0.0, al)

	plate = solid_plate_mask(np.dstack([out[..., :3], al.astype(np.uint8)]))
	if not plate.any():
		out[..., 3] = al.astype(np.uint8)
		return out

	# Sample plate color from upper-percentile magenta (avoid dark ink)
	r = rgb[..., 0]
	sample = plate & (r >= np.percentile(r[plate], 55))
	if sample.sum() < 50:
		sample = plate & (r > 140)
	mean = rgb[sample].mean(0) if sample.any() else np.array([200.0, 28.0, 85.0], np.float32)
	plate_lum = float(mean.mean())

	edge = plate & ~ndimage.binary_erosion(plate, iterations=3)
	interior = plate & ~edge

	# Dark / grey ink relative to THIS plate (plate_lum ~90 for from_ref)
	chroma = rgb.max(2) - rgb.min(2)
	ink = interior & (
		(lum < plate_lum - 8)
		| ((lum < plate_lum - 4) & (chroma < 70))
		| (r < mean[0] - 18)
	)
	ink = ndimage.binary_dilation(ink, iterations=2) & interior

	rng = np.random.default_rng(42)
	grain = rng.normal(0, 3.5, size=rgb.shape)

	# DIRECT fill — do not trust inpaint for large glyph regions
	fill = ink | (interior & (al < 40))
	for c in range(3):
		rgb[fill, c] = mean[c] + grain[fill, c]

	# Homogenize full text band (kills soft imprint even if ink mask missed AA)
	h, _ = plate.shape
	yy = np.arange(h)[:, None]
	band = interior & (yy > h * 0.16) & (yy < h * 0.84)
	dev = np.abs(rgb - mean).mean(2)
	soft = band & (dev > 4.0)
	for c in range(3):
		rgb[soft, c] = mean[c] + grain[soft, c] * 0.85
		# keep mild texture elsewhere in band
		ok = band & ~soft
		rgb[ok, c] = 0.85 * rgb[ok, c] + 0.15 * (mean[c] + grain[ok, c] * 0.4)

	# Tiny fringe inpaint for seam blend (mask must be SMALL so neighbors exist)
	fringe = ndimage.binary_dilation(fill, iterations=1) & ~fill & interior
	if fringe.any():
		bgr = cv2.cvtColor(np.clip(rgb, 0, 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
		m = fringe.astype(np.uint8) * 255
		bgr = cv2.inpaint(bgr, m, 3, cv2.INPAINT_TELEA)
		rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32)

	out[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
	out[..., 3] = np.where(plate, np.maximum(al, 235), 0).astype(np.uint8)
	return out


def ink_count(a: np.ndarray, *, band_only: bool = True) -> int:
	"""Count pixels significantly darker than plate mean (text-band by default).

	Edge silhouette distress is excluded — those darker tips are intentional.
	"""
	plate = solid_plate_mask(a)
	# Stay away from ragged paint edge
	interior = ndimage.binary_erosion(plate, iterations=5)
	if not interior.any():
		return 0
	rgb = a[..., :3].astype(np.float32)
	lum = rgb.mean(2)
	r = rgb[..., 0]
	sample = interior & (r >= np.percentile(r[interior], 55))
	mean_lum = float(rgb[sample].mean()) if sample.any() else float(lum[interior].mean())
	ink = interior & (lum < mean_lum - 10)
	if band_only:
		h = a.shape[0]
		yy = np.arange(h)[:, None]
		ink = ink & (yy > h * 0.18) & (yy < h * 0.82)
	return int(ink.sum())


def save_sync(name: str, arr: np.ndarray) -> None:
	im = Image.fromarray(arr, "RGBA")
	for d in TARGETS:
		d.mkdir(parents=True, exist_ok=True)
		dest = d / name
		im.save(dest)
		print(f"  wrote {dest} ({dest.stat().st_size} bytes)")
	TMP.mkdir(parents=True, exist_ok=True)
	im.save(TMP / f"scrubbed_{name}")


def preview(name: str, arr: np.ndarray, label: str) -> None:
	im = Image.fromarray(arr, "RGBA")
	disp_w = 232 if "wide" not in name else 320
	disp_h = max(1, int(im.height * (disp_w / im.width)))
	scaled = im.resize((disp_w, disp_h), Image.Resampling.NEAREST)
	bg = Image.new("RGBA", (disp_w + 40, disp_h + 40), (10, 10, 12, 255))
	bg.paste(scaled, (20, 20), scaled)
	draw = ImageDraw.Draw(bg)
	try:
		font = ImageFont.truetype(
			"C:/Windows/Fonts/impact.ttf", 18 if "wide" not in name else 22
		)
	except OSError:
		font = ImageFont.load_default()
	bb = draw.textbbox((0, 0), label, font=font)
	tw, th = bb[2] - bb[0], bb[3] - bb[1]
	draw.text(
		(20 + (disp_w - tw) // 2, 20 + (disp_h - th) // 2 - 2),
		label,
		fill=(10, 10, 10, 255),
		font=font,
	)
	bg.save(TMP / f"composite_after_{name}")
	only = Image.new("RGBA", (disp_w + 40, disp_h + 40), (10, 10, 12, 255))
	only.paste(scaled, (20, 20), scaled)
	only.save(TMP / f"plate_only_after_{name}")


def pick_source(name: str) -> Path:
	stem = name.replace(".png", "")
	# Always prefer from_ref when present — shipped may already be half-scrubbed
	for c in (TMP / f"{stem}_from_ref.png", PKG / name, STATIC / name):
		if c.exists():
			return c
	raise FileNotFoundError(name)


def main() -> None:
	labels = {
		"section_magenta.png": "SELECT YOUR BET",
		"section_magenta_wide.png": "BET MENU",
	}
	for name, label in labels.items():
		src = pick_source(name)
		print(f"\n=== {name} from {src.name} ===")
		raw = load_rgba(src)
		print(f"  before ink={ink_count(raw)} size={raw.shape[1]}x{raw.shape[0]}")

		cleaned = blank_plate(raw)
		cleaned = blank_plate(cleaned)

		tw, th = SIZES[name]
		# Nearest upscale preserves hard paint edges; blank again at target res
		im = Image.fromarray(cleaned, "RGBA").resize((tw, th), Image.Resampling.NEAREST)
		arr = blank_plate(np.array(im))
		arr = blank_plate(arr)

		# Final: force-uniform text band (HTML labels live here)
		plate = solid_plate_mask(arr)
		interior = ndimage.binary_erosion(plate, iterations=4)
		rgb = arr[..., :3].astype(np.float32)
		r = rgb[..., 0]
		sample = interior & (r >= np.percentile(r[interior], 55)) if interior.any() else interior
		mean = rgb[sample].mean(0) if sample.any() else np.array([200.0, 28.0, 85.0])
		h = arr.shape[0]
		yy = np.arange(h)[:, None]
		band = interior & (yy > h * 0.16) & (yy < h * 0.84)
		rng = np.random.default_rng(7)
		grain = rng.normal(0, 3.2, size=rgb.shape)
		for c in range(3):
			rgb[band, c] = mean[c] + grain[band, c]
		arr[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)

		ink = ink_count(arr)
		print(f"  after  band_ink={ink} size={arr.shape[1]}x{arr.shape[0]}")
		if ink >= 40:
			raise SystemExit(f"FAIL {name}: residual band ink={ink}")
		save_sync(name, arr)
		preview(name, arr, label)

	print("\nDone. Hard-refresh the game.")


if __name__ == "__main__":
	main()
