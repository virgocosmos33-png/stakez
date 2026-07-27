"""Process paytable chrome plates → RGBA PNGs (package + static sync).

Preferred path: extract_paytable_chrome_from_refs.py (user refs → blank plates).
This script keys black backgrounds from Scenario/raw dumps when regenerating.
"""

from pathlib import Path

import numpy as np
from PIL import Image

RAW = Path(__file__).resolve().parent.parent / ".tmp_paytable_chrome"
OUT = (
	Path(__file__).resolve().parents[3]
	/ "packages"
	/ "components-ui-html"
	/ "src"
	/ "assets"
	/ "paytable"
)
STATIC_UI = Path(__file__).resolve().parent.parent / "static" / "assets" / "paytable_ui"


def key_black(
	src: Path,
	dest_name: str,
	thresh: float = 28,
	soft: float = 18,
	crop: bool = True,
	punch_center: bool = False,
	max_w: int = 900,
) -> None:
	im = Image.open(src).convert("RGBA")
	arr = np.asarray(im).astype(np.float32)
	rgb = arr[..., :3]
	lum = rgb.mean(axis=2)
	a = np.clip((lum - thresh) / soft, 0, 1) * 255.0
	mx = rgb.max(axis=2)
	a = np.where(mx < thresh, 0, a)
	# keep saturated magenta even when darker than thresh
	r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
	mag = (r > 90) & (r > g * 1.25) & (r > b * 1.1) & ((r - g) > 25)
	a = np.where(mag, np.maximum(a, 220.0), a)
	arr[..., 3] = a
	out_im = Image.fromarray(arr.astype(np.uint8), "RGBA")

	if punch_center:
		w, h = out_im.size
		px = np.asarray(out_im).astype(np.float32)
		yy, xx = np.mgrid[0:h, 0:w]
		cx, cy = w / 2, h / 2
		rx, ry = w * 0.42, h * 0.36
		inside = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 < 1.0
		dark = px[..., :3].mean(axis=2) < 55
		px[..., 3] = np.where(inside & dark, 0, px[..., 3])
		out_im = Image.fromarray(px.astype(np.uint8), "RGBA")

	if crop:
		bbox = out_im.getbbox()
		if bbox:
			out_im = out_im.crop(bbox)

	if out_im.width > max_w:
		nh = int(out_im.height * (max_w / out_im.width))
		out_im = out_im.resize((max_w, nh), Image.Resampling.LANCZOS)

	OUT.mkdir(parents=True, exist_ok=True)
	STATIC_UI.mkdir(parents=True, exist_ok=True)
	out_im.save(OUT / dest_name, optimize=True)
	out_im.save(STATIC_UI / dest_name, optimize=True)
	print(f"wrote {dest_name} {out_im.size}")


if __name__ == "__main__":
	# Prefer ref-extraction pipeline for magenta/torn-white chrome.
	print("Use: python tools/extract_paytable_chrome_from_refs.py")
	print("Optional raw keying if dumps exist in", RAW)
	for src_name, dest, kwargs in [
		("title_plate_raw.png", "title_plate_blank.png", {"thresh": 18, "soft": 12, "max_w": 1100}),
		("section_magenta_raw.png", "section_magenta.png", {"thresh": 14, "soft": 10, "max_w": 900}),
		(
			"section_magenta_wide_raw.png",
			"section_magenta_wide.png",
			{"thresh": 14, "soft": 10, "max_w": 1100},
		),
		("accent_stain_raw.png", "accent_stain.png", {"thresh": 18, "soft": 14, "max_w": 512}),
		(
			"card_frame_raw.png",
			"card_frame_blank.png",
			{"thresh": 20, "soft": 14, "punch_center": True},
		),
	]:
		src = RAW / src_name
		if src.exists():
			key_black(src, dest, **kwargs)
	print("done ->", OUT)
