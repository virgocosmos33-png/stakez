"""Download Scenario buy-card illustrations and normalize into buy_*.webp slots."""

from __future__ import annotations

import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
STAGE = Path(__file__).resolve().parent / "_buycard_stage_wr"
DST_STATIC = ROOT / "static" / "assets" / "sprites" / "mirror"
DST_ASSETS = ROOT / "assets" / "sprites" / "mirror"

# Scenario asset download URLs (png) — filled by agent at run time via argv/env or edit.
MAP = {
	"buy_ante.webp": "asset_JiSsHQ7esFfyHq3g5PriRmBQ",
	"buy_feature1.webp": "asset_stuspnH7B4NoB37o2PrMBR7T",
	"buy_feature2.webp": "asset_q4MyF4RpZaE2PdS19PfjmCNd",
	"buy_feature3.webp": "asset_HmF1fMqsdvRX5izRNdbh5REy",
	"buy_seance.webp": "asset_KpGAw8xBAcYubfQKDJATykSK",
	"buy_otherside.webp": "asset_tvcv5mo3X8FHiZeRgCDZkAni",
	"buy_bloodmoon.webp": "asset_7eejV674yn17Ng4i1s8KGUSf",
}

CANVAS = 1024
SUBJECT_FRAC = 0.92
FRINGE_ALPHA = 12


def clean_alpha(im: Image.Image) -> Image.Image:
	im = im.convert("RGBA")
	r, g, b, a = im.split()
	a = a.point(lambda v: 0 if v <= FRINGE_ALPHA else v)
	return Image.merge("RGBA", (r, g, b, a))


def autocrop(im: Image.Image) -> Image.Image:
	bbox = im.split()[3].getbbox()
	return im.crop(bbox) if bbox else im


def normalize(im: Image.Image) -> Image.Image:
	im = autocrop(clean_alpha(im))
	w, h = im.size
	target = int(CANVAS * SUBJECT_FRAC)
	scale = min(target / w, target / h)
	new = (max(1, round(w * scale)), max(1, round(h * scale)))
	im = im.resize(new, Image.LANCZOS)
	canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
	ox = (CANVAS - new[0]) // 2
	oy = (CANVAS - new[1]) // 2
	canvas.alpha_composite(im, (ox, oy))
	return canvas


def key_near_black(im: Image.Image, thr: int = 14) -> Image.Image:
	"""If generation came on solid black, punch transparency."""
	import numpy as np

	arr = np.array(im.convert("RGBA"))
	rgb = arr[..., :3].astype("int16")
	mask = rgb.max(axis=2) <= thr
	arr[..., 3] = np.where(mask, 0, arr[..., 3])
	return Image.fromarray(arr, "RGBA")


def main() -> None:
	import json
	import sys

	STAGE.mkdir(parents=True, exist_ok=True)
	url_map_path = Path(sys.argv[1]) if len(sys.argv) > 1 else STAGE / "urls.json"
	urls = json.loads(url_map_path.read_text(encoding="utf-8"))

	DST_STATIC.mkdir(parents=True, exist_ok=True)
	DST_ASSETS.mkdir(parents=True, exist_ok=True)

	for dst_name, asset_id in MAP.items():
		url = urls[asset_id]
		raw = STAGE / f"{asset_id}.png"
		print(f"GET {asset_id} -> {dst_name}", flush=True)
		urllib.request.urlretrieve(url, raw)
		im = Image.open(raw)
		im = key_near_black(im)
		# if still mostly opaque black-bg, photoroom may be needed; try edge key first
		out = normalize(im)
		for dst in (DST_STATIC / dst_name, DST_ASSETS / dst_name):
			# backup once
			if dst.exists() and not (dst.with_name(dst.stem + "_mm_bak.webp")).exists():
				dst.replace(dst.with_name(dst.stem + "_mm_bak.webp"))
			out.save(dst, "WEBP", lossless=True, method=4)
			print(f"  wrote {dst}", flush=True)
	print("DONE")


if __name__ == "__main__":
	main()
