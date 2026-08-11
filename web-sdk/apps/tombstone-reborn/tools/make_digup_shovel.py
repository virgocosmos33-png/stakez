"""Bake the digUp hero art: the planted shovel and the dug-earth scar under it.

Sources are Layer AI generations (workspace "Back's Workspace", session
"Tombstone Reborn - digUp shovel"), downloaded into assets-raw/layer_digup.
Nothing here is generated in Scenario.

Two different keys, because the two plates were generated differently.

  black  The spade was re-generated against a pure black void with rim light,
         which is the only backdrop that unmixes exactly: the observed pixel is
         alpha * foreground, so dividing by alpha recovers the true colour and
         no backdrop tint can survive into the edge. The earlier studio-backdrop
         spade left a cream rim on the shaft that read as a stray outline at
         cell scale, which is why it was thrown away.
  plate  Distance from the backdrop colour sampled at the frame border, for the
         scar, which is still a studio-backdrop plate. Deliberately NOT limited
         to the border-connected region, so enclosed background also drops.

Outputs
  static/assets/sprites/fx/fx_shovel.png    planted spade, blade at the bottom
  static/assets/sprites/fx/fx_dig_scar.png  turned earth decal

Run:  python tools/make_digup_shovel.py
"""

from __future__ import annotations

import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
RAW = os.path.join(APP, "assets-raw", "layer_digup")
# the fx sprites live in BOTH trees: static/ is served, assets/ is what the
# bundler resolves (game/assets.ts imports ../../assets/...). Write to both so
# the two never drift.
OUT_DIRS = [
	os.path.join(APP, "static", "assets", "sprites", "fx"),
	os.path.join(APP, "assets", "sprites", "fx"),
]

ALPHA_FLOOR = 8
BLEED_PASSES = 8

# The board is near-black, so both plates get lifted or they land as
# silhouettes. The spade is lifted hardest: its blade is oiled iron, which sits
# at almost exactly the cell's own value.
#
# `knee` rolls off everything brighter than it (1.0 = off). The scar plate is
# full of lit straw and pale grit that survives shrinking to a cell as a
# scatter of white specks, which is the stray-dot artefact this game has been
# burned by before. The spade keeps its highlights: the rim light IS the read.
JOBS = [
	dict(src="blk_a.png", out="fx_shovel", key="black", longest=768, low=0.035, high=0.14, gain=1.55, knee=0.86),
	dict(src="scar_a.png", out="fx_dig_scar", key="plate", longest=640, low=0.075, high=0.135, gain=1.0, knee=0.45),
	# impact-strike decal on a black void. Keyed HARD (high low/high, no exposure
	# lift) so only the rim-lit crack edges and lit splinters survive and the dark
	# fill dirt drops to transparent — the decal must READ AS CRACKS the symbol
	# shows through, not an opaque dusty disc washing the card. knee tames the
	# hottest chips so they don't survive the downscale as white specks.
	dict(src="impact_a.png", out="fx_dig_impact", key="black", longest=768, low=0.13, high=0.34, gain=1.0, knee=0.5),
]


def key_black(image: Image.Image, low: float, high: float) -> Image.Image:
	"""Key a subject off a black void and unmix the backdrop out of the edge.

	Against black the render is alpha * foreground, so the recovered colour is
	simply observed / alpha. That is why this key cannot leave a coloured rim:
	there is no backdrop colour to leave behind.
	"""
	data = np.array(image.convert("RGB")).astype(np.float32) / 255.0
	luma = data.max(axis=2)
	alpha = np.clip((luma - low) / max(high - low, 1e-4), 0.0, 1.0)
	rgb = np.where(alpha[..., None] > 0.004, data / np.maximum(alpha[..., None], 1e-4), 0.0)
	out = np.dstack([np.clip(rgb, 0.0, 1.0) * 255.0, alpha * 255.0]).astype(np.uint8)
	return Image.fromarray(out, "RGBA")


def key_plate(image: Image.Image, tolerance: float, feather_to: float) -> Image.Image:
	data = np.array(image.convert("RGB")).astype(np.float32) / 255.0
	edges = np.concatenate(
		[data[0, :, :], data[-1, :, :], data[:, 0, :], data[:, -1, :]], axis=0
	)
	backdrop = np.median(edges, axis=0)
	distance = np.linalg.norm(data - backdrop, axis=2) / np.sqrt(3.0)
	# ramp across the feather band so the silhouette keeps its antialiased edge
	alpha = np.clip(
		(distance - tolerance) / max(feather_to - tolerance, 1e-4), 0.0, 1.0
	)
	out = np.dstack([data * 255.0, alpha * 255.0]).astype(np.uint8)
	return Image.fromarray(out, "RGBA")


def lift_exposure(image: Image.Image, gain: float) -> Image.Image:
	"""Raise the plate into range for a near-black board, with a warm bias so
	lit iron stays iron instead of turning into flat grey."""
	if gain <= 1.0:
		return image
	data = np.array(image).astype(np.float32)
	rgb = data[..., :3] / 255.0
	rgb = 1.0 - np.power(1.0 - np.clip(rgb * gain, 0.0, 1.0), 1.1)
	rgb *= np.array([1.06, 1.0, 0.86], dtype=np.float32)
	data[..., :3] = np.clip(rgb, 0.0, 1.0) * 255.0
	return Image.fromarray(data.astype(np.uint8), "RGBA")


def tame_highlights(image: Image.Image, knee: float) -> Image.Image:
	"""Roll everything above `knee` back towards it, so bright grit does not
	survive the downscale to a cell as a scatter of white specks."""
	if knee >= 1.0:
		return image
	data = np.array(image).astype(np.float32)
	rgb = data[..., :3] / 255.0
	over = np.maximum(rgb - knee, 0.0)
	rgb = np.minimum(rgb, knee) + over / (1.0 + over / max(1.0 - knee, 1e-4)) * 0.45
	data[..., :3] = np.clip(rgb, 0.0, 1.0) * 255.0
	return Image.fromarray(data.astype(np.uint8), "RGBA")


def bleed_alpha(image: Image.Image) -> Image.Image:
	data = np.array(image).astype(np.float32)
	rgb = data[..., :3]
	alpha = data[..., 3]
	known = alpha > 24
	for _ in range(BLEED_PASSES):
		if known.all():
			break
		weight = known.astype(np.float32)
		acc_c = np.zeros_like(rgb)
		acc_w = np.zeros_like(alpha)
		for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
			acc_c += np.roll(rgb * weight[..., None], (dy, dx), axis=(0, 1))
			acc_w += np.roll(weight, (dy, dx), axis=(0, 1))
		fill = (~known) & (acc_w > 0)
		if not fill.any():
			break
		rgb[fill] = acc_c[fill] / acc_w[fill][..., None]
		known = known | fill
	out = np.dstack([rgb, alpha]).astype(np.uint8)
	out[alpha <= ALPHA_FLOOR] = (0, 0, 0, 0)
	return Image.fromarray(out, "RGBA")


def alpha_crop(image: Image.Image) -> Image.Image:
	mask = image.getchannel("A").point(lambda value: 255 if value > ALPHA_FLOOR else 0)
	box = mask.getbbox()
	if box is None:
		raise SystemExit("source keyed to nothing — loosen the tolerance")
	return image.crop(box)


def resize_rgba(image: Image.Image, size: tuple[int, int]) -> Image.Image:
	data = np.array(image).astype(np.float32)
	coverage = data[..., 3:4] / 255.0
	premultiplied = np.dstack([data[..., :3] * coverage, data[..., 3]]).astype(np.uint8)
	small = np.array(
		Image.fromarray(premultiplied, "RGBA").resize(size, Image.LANCZOS)
	).astype(np.float32)
	out_coverage = small[..., 3:4] / 255.0
	rgb = np.where(out_coverage > 0.004, small[..., :3] / np.maximum(out_coverage, 1e-4), 0.0)
	out = np.dstack([np.clip(rgb, 0, 255), small[..., 3]]).astype(np.uint8)
	out[small[..., 3] <= ALPHA_FLOOR] = (0, 0, 0, 0)
	return Image.fromarray(out, "RGBA")


def main() -> None:
	for out_dir in OUT_DIRS:
		os.makedirs(out_dir, exist_ok=True)
	for job in JOBS:
		path = os.path.join(RAW, job["src"])
		if not os.path.isfile(path):
			raise SystemExit(f"missing Layer AI source: {path}")
		image = Image.open(path)
		keyed = (
			key_black(image, job["low"], job["high"])
			if job["key"] == "black"
			else key_plate(image, job["low"], job["high"])
		)
		art = alpha_crop(
			bleed_alpha(tame_highlights(lift_exposure(keyed, job["gain"]), job["knee"]))
		)
		longest = job["longest"]
		scale = min(1.0, longest / max(art.width, art.height))
		art = resize_rgba(art, (max(1, round(art.width * scale)), max(1, round(art.height * scale))))
		for out_dir in OUT_DIRS:
			art.save(os.path.join(out_dir, f"{job['out']}.png"), optimize=True)
		coverage = np.array(art)[..., 3].mean() / 255.0
		print(
			f"[digup] {job['out']} {art.width}x{art.height} coverage {coverage:.2f}"
			f" <- layer_digup/{job['src']}"
		)


if __name__ == "__main__":
	main()
