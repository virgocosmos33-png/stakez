"""Definitively kill baked horizontal quilt/stitch dashes on padded reel-frame lips.

Root cause (2026-07-24 close-up proof):
  mirror_frame_wide.png left/right grey padded rails contain short dark horizontal
  dash clusters at regular vertical intervals. Prior strip_frame_cutline.py only
  sealed the BRIGHT 1px cut-path lip (SEAL_DEPTH=6) — it does NOT remove these
  darker stitch marks deeper in the padded / groove band.

  Nine-slice vertical stretch of the side rails spaces the baked dashes evenly
  down the live board height. Shared base+bonus asset (mirrorFrame).

Method:
  Rebuild each L/R lip band as a Y-constant X-profile (median along opening height)
  plus tiny column-zero-mean grain. Removes ALL horizontal structure while keeping
  the bevel/groove cross-section. Opening bbox bak-locked.

Writes static + assets mirror_frame_wide.png and legacy mirror_frame.png alias.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
STATIC_DIR = HERE.parent / "static" / "assets" / "sprites" / "mirror"
APP_ASSETS_DIR = HERE.parent / "assets" / "sprites" / "mirror"
OUT_NAME = "mirror_frame_wide.png"
PRE_BAK = "mirror_frame_wide_PRE_QUILT_DASH_STRIP.png"
QA_DIR = HERE.parent

# Full grey padded rail into the opening (x≈85→203 on 1803-wide art). Inner lip
# alone (depth 52) left outer grey band stitches intact for nine-slice L/R edges.
LIP_DEPTH = 118
# Keep 0 — any Y-noise gets misread as residual "dashes" in close-ups.
GRAIN_SIGMA = 0.0


def find_opening(a: np.ndarray) -> tuple[int, int, int, int]:
	alpha = a[..., 3]
	h, w = alpha.shape

	def max_run(row: np.ndarray) -> tuple[int, int]:
		padded = np.concatenate(([0], row.astype(np.int8), [0]))
		d = np.diff(padded)
		starts = np.where(d == 1)[0]
		ends = np.where(d == -1)[0]
		lengths = ends - starts
		k = int(lengths.argmax())
		return int(starts[k]), int(lengths[k])

	ox, ow = max_run((alpha[h // 2] < 20))
	oy, oh = max_run((alpha[:, w // 2] < 20))
	return ox, oy, ow, oh


def reseal_lips(arr: np.ndarray, lip_depth: int = LIP_DEPTH) -> tuple[np.ndarray, dict]:
	out = arr.copy()
	rgb = out[..., :3].astype(np.float32)
	alpha = out[..., 3]
	ox, oy, ow, oh = find_opening(out)
	h, w = alpha.shape
	y_mid0 = oy + oh // 4
	y_mid1 = oy + (3 * oh) // 4
	rng = np.random.default_rng(42)
	stats = {"opening": (ox, oy, ow, oh), "lip_depth": lip_depth}

	def reseal(x0: int, x1: int, side: str) -> None:
		if x1 <= x0:
			stats[f"{side}_px"] = 0
			return
		band = rgb[oy : oy + oh, x0:x1].copy()
		a_band = alpha[oy : oy + oh, x0:x1]
		bw = band.shape[1]
		mid = band[y_mid0 - oy : y_mid1 - oy]
		profile = np.median(mid, axis=0)  # (bw, 3) — Y-constant bevel cross-section
		grain = rng.normal(0, GRAIN_SIGMA, size=band.shape).astype(np.float32)
		grain -= grain.mean(axis=0, keepdims=True)  # no horizontal streaks
		rebuilt = profile[None, :, :] + grain
		opaque = a_band > 20
		for c in range(3):
			band[..., c] = np.where(opaque, rebuilt[..., c], band[..., c])
		rgb[oy : oy + oh, x0:x1] = band
		stats[f"{side}_px"] = int(opaque.sum())

		# Soft feather into corner approach above/below opening
		for y in range(max(0, oy - 20), oy):
			t = (y - (oy - 20)) / 20.0
			t = float(np.clip(t, 0.0, 1.0))
			for x in range(x0, x1):
				if alpha[y, x] <= 20:
					continue
				rgb[y, x] = rgb[y, x] * (1.0 - t) + profile[x - x0] * t
		for y in range(oy + oh, min(h, oy + oh + 20)):
			t = 1.0 - (y - (oy + oh)) / 20.0
			t = float(np.clip(t, 0.0, 1.0))
			for x in range(x0, x1):
				if alpha[y, x] <= 20:
					continue
				rgb[y, x] = rgb[y, x] * (1.0 - t) + profile[x - x0] * t

	reseal(max(0, ox - lip_depth), ox, "left")
	reseal(ox + ow, min(w, ox + ow + lip_depth), "right")
	out[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
	return out, stats


def _hf_energy(arr: np.ndarray, ox: int, oy: int, ow: int, oh: int) -> float:
	lum = (
		0.2126 * arr[:, :, 0].astype(np.float32)
		+ 0.7152 * arr[:, :, 1].astype(np.float32)
		+ 0.0722 * arr[:, :, 2].astype(np.float32)
	)
	band = lum[oy + 80 : oy + oh - 80, ox - 40 : ox]
	acc = 0.0
	for x in range(band.shape[1]):
		c = band[:, x]
		hp = c - np.convolve(c, np.ones(15) / 15, mode="same")
		acc += float(np.mean(hp**2))
	return acc / max(band.shape[1], 1)


def _hp_vis(arr: np.ndarray, ox: int, oy: int, ow: int, oh: int, dest: Path) -> None:
	lum = (
		0.2126 * arr[:, :, 0].astype(np.float32)
		+ 0.7152 * arr[:, :, 1].astype(np.float32)
		+ 0.0722 * arr[:, :, 2].astype(np.float32)
	)
	band = lum[oy + 80 : oy + oh - 80, ox - 40 : ox]
	hp = np.zeros_like(band)
	for x in range(band.shape[1]):
		c = band[:, x]
		hp[:, x] = c - np.convolve(c, np.ones(15) / 15, mode="same")
	vis = np.clip(128 + hp * 10, 0, 255).astype(np.uint8)
	Image.fromarray(vis).resize(
		(vis.shape[1] * 6, vis.shape[0]), Image.Resampling.NEAREST
	).save(dest)


def _atomic_save(im: Image.Image, dest: Path) -> None:
	dest.parent.mkdir(parents=True, exist_ok=True)
	tmp = dest.with_name(dest.name + ".tmp.png")
	im.save(tmp, format="PNG")
	try:
		tmp.replace(dest)
	except OSError as e:
		alt = dest.with_name(dest.stem + "_wr.png")
		im.save(alt)
		print(f"[warn] locked {dest.name} ({e}); wrote {alt.name}", flush=True)
	else:
		if tmp.exists():
			tmp.unlink(missing_ok=True)
		print(f"wrote {dest} ({dest.stat().st_size} bytes)", flush=True)


def main() -> None:
	bak = STATIC_DIR / PRE_BAK
	src = STATIC_DIR / OUT_NAME
	if bak.is_file():
		before_im = Image.open(bak).convert("RGBA")
		print(f"src=PRE bak {bak.name}", flush=True)
	elif src.is_file():
		before_im = Image.open(src).convert("RGBA")
		before_im.save(bak)
		print(f"src={src}; wrote PRE bak", flush=True)
	else:
		raise SystemExit(f"missing {src}")

	before = np.asarray(before_im)
	opening_before = find_opening(before)
	print(f"opening_before={opening_before}", flush=True)

	after_arr, stats = reseal_lips(before)
	opening_after = find_opening(after_arr)
	print(f"opening_after={opening_after}", flush=True)
	print(f"stats={stats}", flush=True)
	if opening_after != opening_before:
		raise SystemExit(
			f"OPENING GEOMETRY CHANGED {opening_before} -> {opening_after}; aborting"
		)

	ox, oy, ow, oh = opening_after
	e0 = _hf_energy(before, ox, oy, ow, oh)
	e1 = _hf_energy(after_arr, ox, oy, ow, oh)
	print(f"left_lip_hf_energy before={e0:.3f} after={e1:.3f}", flush=True)
	if e1 > e0 * 0.35:
		raise SystemExit(
			f"HF energy not reduced enough ({e0:.3f} -> {e1:.3f}); aborting"
		)

	out_im = Image.fromarray(after_arr, "RGBA")
	before_im.crop((ox - 55, oy + 80, ox + 8, oy + oh - 80)).resize(
		(189, 1200), Image.Resampling.NEAREST
	).save(QA_DIR / ".tmp_qa_quilt_left_BEFORE.png")
	out_im.crop((ox - 55, oy + 80, ox + 8, oy + oh - 80)).resize(
		(189, 1200), Image.Resampling.NEAREST
	).save(QA_DIR / ".tmp_qa_quilt_left_AFTER.png")
	out_im.crop((ox + ow - 8, oy + 80, ox + ow + 55, oy + oh - 80)).resize(
		(189, 1200), Image.Resampling.NEAREST
	).save(QA_DIR / ".tmp_qa_quilt_right_AFTER.png")
	_hp_vis(before, ox, oy, ow, oh, QA_DIR / ".tmp_qa_lip_hp_BEFORE.png")
	_hp_vis(after_arr, ox, oy, ow, oh, QA_DIR / ".tmp_qa_lip_hp_AFTER.png")

	b = Image.open(QA_DIR / ".tmp_qa_quilt_left_BEFORE.png")
	s = Image.open(QA_DIR / ".tmp_qa_quilt_left_AFTER.png")
	combo = Image.new("RGB", (b.width * 2 + 8, b.height), (20, 20, 20))
	combo.paste(b.convert("RGB"), (0, 0))
	combo.paste(s.convert("RGB"), (b.width + 8, 0))
	combo.save(QA_DIR / ".tmp_qa_quilt_left_COMPARE.png")
	print("wrote QA before/after + HP + compare", flush=True)

	_atomic_save(out_im, STATIC_DIR / OUT_NAME)
	_atomic_save(out_im, APP_ASSETS_DIR / OUT_NAME)
	_atomic_save(out_im, STATIC_DIR / "mirror_frame.png")
	_atomic_save(out_im, APP_ASSETS_DIR / "mirror_frame.png")
	print("OK: lip resealed (no quilt dashes); opening bak-locked", flush=True)


if __name__ == "__main__":
	main()
