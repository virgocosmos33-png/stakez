"""Shared alpha-cutting helpers for Layer AI plates.

Both the digUp spade and the nudge UI art are generated against a pure black
void and cut here. Black is the only backdrop that unmixes exactly — the render
is alpha * foreground, so dividing by alpha recovers the true colour and no
backdrop tint can survive into the edge. An earlier spade generated on a light
studio backdrop left a cream rim on its shaft that read as a stray outline at
cell scale, which is the failure this module exists to prevent.

`key_plate` is the fallback for plates that were NOT generated on black. It is
deliberately not limited to the border-connected region, so enclosed background
(the hole in a shovel's D-grip, the open centre of a frame) also drops.
"""

from __future__ import annotations

import numpy as np
from PIL import Image

ALPHA_FLOOR = 8
BLEED_PASSES = 8


def key_black(image: Image.Image, low: float, high: float) -> Image.Image:
	"""Key a subject off a black void and unmix the backdrop out of the edge."""
	data = np.array(image.convert("RGB")).astype(np.float32) / 255.0
	luma = data.max(axis=2)
	alpha = np.clip((luma - low) / max(high - low, 1e-4), 0.0, 1.0)
	rgb = np.where(alpha[..., None] > 0.004, data / np.maximum(alpha[..., None], 1e-4), 0.0)
	out = np.dstack([np.clip(rgb, 0.0, 1.0) * 255.0, alpha * 255.0]).astype(np.uint8)
	return Image.fromarray(out, "RGBA")


def key_plate(image: Image.Image, tolerance: float, feather_to: float) -> Image.Image:
	"""Key on distance from the backdrop colour sampled at the frame border."""
	data = np.array(image.convert("RGB")).astype(np.float32) / 255.0
	edges = np.concatenate(
		[data[0, :, :], data[-1, :, :], data[:, 0, :], data[:, -1, :]], axis=0
	)
	backdrop = np.median(edges, axis=0)
	distance = np.linalg.norm(data - backdrop, axis=2) / np.sqrt(3.0)
	# ramp across the feather band so the silhouette keeps its antialiased edge
	alpha = np.clip((distance - tolerance) / max(feather_to - tolerance, 1e-4), 0.0, 1.0)
	out = np.dstack([data * 255.0, alpha * 255.0]).astype(np.uint8)
	return Image.fromarray(out, "RGBA")


def lift_exposure(image: Image.Image, gain: float) -> Image.Image:
	"""Raise a plate into range for a near-black board, with a warm bias so lit
	iron stays iron instead of turning into flat grey."""
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
	"""Dilate opaque colour into the transparent margin, then zero the RGB that
	is still fully transparent — a halo-free plate with no colour under alpha 0."""
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
	"""Resize through premultiplied alpha, so transparent black cannot bleed
	into the visible edge and darken a soft plate."""
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


def fit_longest(image: Image.Image, longest: int) -> Image.Image:
	scale = min(1.0, longest / max(image.width, image.height))
	return resize_rgba(
		image, (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
	)
