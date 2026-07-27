"""Download Scenario buy illustrations + normalize into buy_*.webp (assets + static)."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
STAGE = Path(__file__).resolve().parent / "_buycard_stage_wr"
DST_STATIC = ROOT / "static" / "assets" / "sprites" / "mirror"
DST_ASSETS = ROOT / "assets" / "sprites" / "mirror"

# asset_id -> destination filename
MAP = {
	"asset_JiSsHQ7esFfyHq3g5PriRmBQ": "buy_ante.webp",
	"asset_stuspnH7B4NoB37o2PrMBR7T": "buy_feature1.webp",
	"asset_q4MyF4RpZaE2PdS19PfjmCNd": "buy_feature2.webp",
	"asset_HmF1fMqsdvRX5izRNdbh5REy": "buy_feature3.webp",
	"asset_KpGAw8xBAcYubfQKDJATykSK": "buy_seance.webp",
	"asset_tvcv5mo3X8FHiZeRgCDZkAni": "buy_otherside.webp",
	"asset_7eejV674yn17Ng4i1s8KGUSf": "buy_bloodmoon.webp",
}

CANVAS = 1024
SUBJECT_FRAC = 0.92
FRINGE = 12


def key_near_black(im: Image.Image, thr: int = 16) -> Image.Image:
	arr = np.array(im.convert("RGBA"))
	rgb = arr[..., :3].astype(np.int16)
	mask = rgb.max(axis=2) <= thr
	arr[..., 3] = np.where(mask, 0, 255)
	return Image.fromarray(arr, "RGBA")


def clean_alpha(im: Image.Image) -> Image.Image:
	r, g, b, a = im.split()
	a = a.point(lambda v: 0 if v <= FRINGE else v)
	return Image.merge("RGBA", (r, g, b, a))


def normalize(im: Image.Image) -> Image.Image:
	im = clean_alpha(im)
	bbox = im.split()[3].getbbox()
	if bbox:
		im = im.crop(bbox)
	w, h = im.size
	target = int(CANVAS * SUBJECT_FRAC)
	scale = min(target / max(w, 1), target / max(h, 1))
	new = (max(1, round(w * scale)), max(1, round(h * scale)))
	im = im.resize(new, Image.LANCZOS)
	canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
	canvas.alpha_composite(im, ((CANVAS - new[0]) // 2, (CANVAS - new[1]) // 2))
	return canvas


def main() -> None:
	urls = json.loads((STAGE / "urls.json").read_text(encoding="utf-8"))
	STAGE.mkdir(parents=True, exist_ok=True)
	DST_STATIC.mkdir(parents=True, exist_ok=True)
	DST_ASSETS.mkdir(parents=True, exist_ok=True)

	for asset_id, dst_name in MAP.items():
		url = urls[asset_id]
		if not url.startswith("http"):
			raise SystemExit(f"bad url for {asset_id}")
		raw = STAGE / f"{asset_id}.png"
		print(f"GET {asset_id}", flush=True)
		urllib.request.urlretrieve(url, raw)
		im = key_near_black(Image.open(raw))
		out = normalize(im)
		for dst in (DST_STATIC / dst_name, DST_ASSETS / dst_name):
			bak = dst.with_name(dst.stem + "_mm_bak.webp")
			if dst.exists() and not bak.exists():
				dst.replace(bak)
			out.save(dst, "WEBP", lossless=True, method=4)
			print(f"  -> {dst} {out.size}", flush=True)
	print("DONE")


if __name__ == "__main__":
	main()
