"""Extract exact zigzag CTA + torn ribbon PNGs from Bonus Buy reference sheets."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ASSETS = Path(
	r"C:\Users\xheih\.cursor\projects"
	r"\c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios\assets"
)
OUT = Path(__file__).resolve().parent / "_buy_ui_extract"


def find_asset(substr: str) -> Path:
	for p in ASSETS.iterdir():
		if substr in p.name and p.suffix.lower() == ".png":
			return p
	raise FileNotFoundError(substr)


def to_rgba_key_black(im: Image.Image, thr: int = 22) -> Image.Image:
	im = im.convert("RGBA")
	arr = np.array(im)
	rgb = arr[..., :3].astype(np.int16)
	mask = rgb.max(axis=2) <= thr
	arr[..., 3] = np.where(mask, 0, 255)
	return Image.fromarray(arr, "RGBA")


def autocrop(im: Image.Image, pad: int = 2) -> Image.Image:
	bbox = im.split()[3].getbbox()
	if not bbox:
		return im
	x0, y0, x1, y1 = bbox
	x0 = max(0, x0 - pad)
	y0 = max(0, y0 - pad)
	x1 = min(im.width, x1 + pad)
	y1 = min(im.height, y1 + pad)
	return im.crop((x0, y0, x1, y1))


def split_horizontal_subjects(im: Image.Image, min_width: int = 8) -> list[tuple[int, int]]:
	alpha = np.array(im)[..., 3]
	col = (alpha > 10).any(axis=0)
	segments: list[tuple[int, int]] = []
	in_seg = False
	start = 0
	for i, v in enumerate(col):
		if v and not in_seg:
			in_seg = True
			start = i
		elif not v and in_seg:
			in_seg = False
			if i - start >= min_width:
				segments.append((start, i))
	if in_seg and len(col) - start >= min_width:
		segments.append((start, len(col)))
	return segments


def mean_rgb(im: Image.Image) -> tuple[float, float, float]:
	arr = np.array(im)
	m = arr[..., 3] > 20
	if not m.any():
		return (0.0, 0.0, 0.0)
	return tuple(arr[..., :3][m].mean(axis=0).tolist())  # type: ignore[return-value]


def keep_paper_band(im: Image.Image) -> Image.Image:
	"""Drop purple/art bleed above the white torn ribbon; keep paper + black ink."""
	arr = np.array(im.convert("RGBA"))
	r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
	# paper-ish (bright, low chroma) OR dark ink
	bright = (r > 170) & (g > 170) & (b > 170)
	ink = (r < 90) & (g < 90) & (b < 90) & (a > 20)
	keep = (bright | ink) & (a > 20)
	# kill saturated purple/magenta leftovers
	purple = (r > 90) & (b > 90) & (g < r * 0.85) & (g < b * 0.85) & ~bright
	keep = keep & ~purple
	arr[..., 3] = np.where(keep, 255, 0)
	return autocrop(Image.fromarray(arr, "RGBA"), pad=1)


def upscale_nearest(im: Image.Image, scale: int = 4) -> Image.Image:
	w, h = im.size
	return im.resize((w * scale, h * scale), Image.Resampling.NEAREST)


def main() -> None:
	OUT.mkdir(parents=True, exist_ok=True)
	btn_path = find_asset("50f2a3fd")
	rib_path = find_asset("26a738c4")
	# prefer non-suffixed hud if long uuid path is broken on OneDrive
	hud_path = None
	for p in ASSETS.iterdir():
		if "f5a73b90" in p.name and p.suffix.lower() == ".png" and "990533da" not in p.name:
			hud_path = p
			break
	if hud_path is None:
		for p in ASSETS.iterdir():
			if "f5a73b90" in p.name and p.suffix.lower() == ".png":
				try:
					p.stat()
					hud_path = p
					break
				except OSError:
					continue

	btn = Image.open(btn_path)
	print("btn", btn.size, btn_path.name)
	btn_rgba = to_rgba_key_black(btn, thr=22)
	btn_rgba.save(OUT / "_btn_sheet.png")
	segs = split_horizontal_subjects(btn_rgba)
	print("btn segs", len(segs), segs)
	for i, (a, b) in enumerate(segs):
		crop = autocrop(btn_rgba.crop((a, 0, b, btn_rgba.height)))
		crop.save(OUT / f"btn_seg_{i:02d}.png")
		print(i, crop.size, mean_rgb(crop))

	means = [mean_rgb(Image.open(OUT / f"btn_seg_{i:02d}.png")) for i in range(len(segs))]
	pink_idxs = [i for i, m in enumerate(means) if m[0] > 160 and m[0] > m[1] + 40]
	grey_idxs = [
		i
		for i, m in enumerate(means)
		if m[0] < 210 and abs(m[0] - m[1]) < 45 and abs(m[1] - m[2]) < 45
	]
	act_i = pink_idxs[0] if pink_idxs else 0
	buy_i = grey_idxs[0] if grey_idxs else len(segs) - 1

	cta_act = Image.open(OUT / f"btn_seg_{act_i:02d}.png")
	cta_buy = Image.open(OUT / f"btn_seg_{buy_i:02d}.png")
	# 4x nearest keeps sawtooth crisp for HUD use; Scenario will also hi-res regenerate
	upscale_nearest(cta_act, 6).save(OUT / "cta_activate.png")
	upscale_nearest(cta_buy, 6).save(OUT / "cta_buy.png")
	cta_act.save(OUT / "cta_activate_src.png")
	cta_buy.save(OUT / "cta_buy_src.png")
	print("cta_activate from", act_i, "cta_buy from", buy_i)

	rib = Image.open(rib_path)
	print("rib", rib.size, rib_path.name)
	rib_rgba = to_rgba_key_black(rib, thr=22)
	rib_rgba.save(OUT / "_rib_sheet.png")
	rsegs = split_horizontal_subjects(rib_rgba)
	print("rib segs", len(rsegs), rsegs)
	names = [
		"scatter",
		"observation",
		"observation_plus",
		"observation_plusplus",
		"fractured",
		"deepness",
	]
	for i, (a, b) in enumerate(rsegs[:6]):
		crop = keep_paper_band(rib_rgba.crop((a, 0, b, rib_rgba.height)))
		name = names[i]
		upscale_nearest(crop, 6).save(OUT / f"ribbon_{name}.png")
		crop.save(OUT / f"ribbon_{name}_src.png")
		print(i, name, crop.size, "->", Image.open(OUT / f"ribbon_{name}.png").size)

	# Blank reusable ribbon: erase dark ink from SCATTER plate
	blank_src = Image.open(OUT / "ribbon_scatter_src.png").convert("RGBA")
	ba = np.array(blank_src)
	dark = (ba[..., 0] < 80) & (ba[..., 1] < 80) & (ba[..., 2] < 80) & (ba[..., 3] > 20)
	ba[dark, 0] = 244
	ba[dark, 1] = 241
	ba[dark, 2] = 236
	blank = Image.fromarray(ba)
	blank.save(OUT / "ribbon_blank_src.png")
	upscale_nearest(blank, 6).save(OUT / "ribbon_blank.png")

	if hud_path is not None:
		try:
			Image.open(hud_path).save(OUT / "_hud_ref.png")
			print("hud", hud_path.name)
		except OSError as e:
			print("hud skip", e)

	meta = {
		"btn_segs": len(segs),
		"rib_segs": min(6, len(rsegs)),
		"activate_seg": act_i,
		"buy_seg": buy_i,
		"out": str(OUT),
	}
	(OUT / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
	print("DONE", json.dumps(meta))


if __name__ == "__main__":
	main()
