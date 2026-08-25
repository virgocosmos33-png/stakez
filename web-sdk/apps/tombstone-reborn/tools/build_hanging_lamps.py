"""Extract PSD hanging lamps and write a Spine 4.1.23 idle (pendulum + flicker).

The live runtime is spine-pixi-v8 (4.2), same as every other koan spine.
A 3.8 skeleton (angle keys, object skins) loads as a still pose — that is
why the lamps sat dead after Crystal.

Pivot is the chain rest at the TOP of each chain (the nail in the beam).
The baked globe is dimmed on the body; flame + wash live on additive slots
so the flicker can actually read.

Run: python tools/build_hanging_lamps.py
"""
from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from psd_tools import PSDImage

from export_western_scene2 import HIDE_FOR_PLATE, PSD_NAME, RAW, STATIC, VITE, sync_from_desktop
from restore_crystal_layers import READY, SCALE, SRC

APP = Path(__file__).resolve().parents[1]
SPINE_NAME = "hanging_lamps"
SPINE_VERSION = "4.1.23"
SPINE_DIRS = (
	APP / "assets" / "spines" / SPINE_NAME,
	APP / "static" / "assets" / "spines" / SPINE_NAME,
)
# PSD names: "left hanging lamp" / "right  hanging lamp" (double space).
LAMP_SIDES = (("left", "l"), ("right", "r"))
G = 980.0
ALPHA_T = 12
GLOW_PAD = 48
SWING_STEPS = 16
FLICKER_STEPS = 20
AMP_L = 13.0
AMP_R = 16.0


def norm(name: str) -> str:
	return " ".join(name.lower().split())


def walk_lamps(layers, found: dict) -> None:
	for layer in layers:
		key = norm(layer.name)
		if key in ("left hanging lamp", "right hanging lamp"):
			found[key] = layer
		if layer.is_group():
			walk_lamps(list(layer), found)


def hide_named(layers, names: tuple[str, ...]) -> None:
	want = {norm(n) for n in names}
	for layer in layers:
		if layer.name in names or norm(layer.name) in want:
			layer.visible = False
		if layer.is_group():
			hide_named(list(layer), names)


def alpha_crop(im: Image.Image, pad: int = 1) -> tuple[Image.Image, tuple[int, int, int, int]]:
	arr = np.array(im)
	a = arr[:, :, 3]
	ys, xs = np.where(a >= ALPHA_T)
	if ys.size == 0:
		raise SystemExit("lamp layer has no visible pixels")
	l, t, r, b = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
	l = max(0, l - pad)
	t = max(0, t - pad)
	r = min(im.width, r + pad)
	b = min(im.height, b + pad)
	return im.crop((l, t, r, b)), (l, t, r, b)


def chain_rest(im: Image.Image) -> tuple[float, float]:
	a = np.array(im.split()[-1])
	ys, xs = np.where(a >= ALPHA_T)
	top = int(ys.min())
	band = xs[ys <= top + 10]
	return float(np.median(band)), float(top + 1)


def mass_center(im: Image.Image) -> tuple[float, float]:
	a = np.array(im.split()[-1]).astype(np.float64)
	ys, xs = np.indices(a.shape)
	w = a.sum()
	return float((xs * a).sum() / w), float((ys * a).sum() / w)


def _gauss_mask(mask: np.ndarray, radius: float) -> np.ndarray:
	core = Image.fromarray((mask.astype(np.uint8) * 255), "L")
	return np.array(core.filter(ImageFilter.GaussianBlur(radius)), dtype=np.float64) / 255.0


def split_lamp(
	im: Image.Image,
) -> tuple[Image.Image, Image.Image, Image.Image, tuple[float, float]]:
	"""Dim the baked globe on the body; emit additive flame + kerosene wash."""
	arr = np.array(im).astype(np.float64)
	r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
	luma = 0.299 * r + 0.587 * g + 0.114 * b
	h, w = a.shape
	yy, xx = np.indices((h, w))
	warm = (r - b) > 40
	band = (yy > h * 0.42) & (yy < h * 0.82)
	mask = (luma > 140) & warm & (a >= ALPHA_T) & band
	if int(mask.sum()) < 40:
		gx, gy = w * 0.50, h * 0.75
		rad = min(w, h) * 0.22
		mask = np.sqrt((xx - gx) ** 2 + (yy - gy) ** 2) < rad
	else:
		gx = float(xx[mask].mean())
		gy = float(yy[mask].mean())

	fall = _gauss_mask(mask, 4.5)
	halo = _gauss_mask(mask, 14.0)
	wash = _gauss_mask(mask, 22.0)

	dim = 1.0 - 0.72 * fall
	body = arr.copy()
	body[:, :, 0] *= dim
	body[:, :, 1] *= dim
	body[:, :, 2] *= dim
	body[a < 1, :3] = 0

	light = np.zeros_like(arr)
	light[:, :, 0] = np.clip(255 * fall + r * fall * 0.35, 0, 255)
	light[:, :, 1] = np.clip(196 * fall + g * fall * 0.25, 0, 255)
	light[:, :, 2] = np.clip(72 * fall, 0, 255)
	light[:, :, 3] = np.clip(255 * np.clip(fall * 1.15, 0, 1), 0, 255)

	pad = GLOW_PAD
	glow = np.zeros((h + pad * 2, w + pad * 2, 4), np.float64)
	ys = slice(pad, pad + h)
	xs = slice(pad, pad + w)
	glow[ys, xs, 0] = 255 * np.clip(halo * 0.85 + wash * 0.45, 0, 1)
	glow[ys, xs, 1] = 168 * np.clip(halo * 0.70 + wash * 0.35, 0, 1)
	glow[ys, xs, 2] = 48 * np.clip(halo * 0.40 + wash * 0.25, 0, 1)
	glow[ys, xs, 3] = 255 * np.clip(halo * 0.55 + wash * 0.35, 0, 1)

	return (
		Image.fromarray(np.clip(body, 0, 255).astype(np.uint8), "RGBA"),
		Image.fromarray(np.clip(light, 0, 255).astype(np.uint8), "RGBA"),
		Image.fromarray(np.clip(glow, 0, 255).astype(np.uint8), "RGBA"),
		(gx, gy),
	)


def attach_xy(hang: tuple[float, float], im: Image.Image) -> tuple[float, float]:
	hx, hy = hang
	return round(im.width * 0.5 - hx, 3), round(hy - im.height * 0.5, 3)


def pack(images: dict[str, Image.Image]) -> tuple[Image.Image, dict[str, tuple[int, int, int, int]]]:
	pad = 2
	items = list(images.items())
	width = pad + sum(im.width + pad for _, im in items)
	height = pad + max(im.height for _, im in items) + pad
	sheet = Image.new("RGBA", (width, height), (0, 0, 0, 0))
	boxes: dict[str, tuple[int, int, int, int]] = {}
	x = pad
	for name, im in items:
		sheet.paste(im, (x, pad), im)
		boxes[name] = (x, pad, im.width, im.height)
		x += im.width + pad
	return sheet, boxes


def write_atlas(path: Path, png_name: str, sheet: Image.Image, boxes: dict[str, tuple[int, int, int, int]]) -> None:
	lines = [
		png_name,
		f"size: {sheet.width},{sheet.height}",
		"format: RGBA8888",
		"filter: Linear,Linear",
		"repeat: none",
	]
	for name, (x, y, w, h) in boxes.items():
		lines += [
			name,
			"  rotate: false",
			f"  xy: {x}, {y}",
			f"  size: {w}, {h}",
			f"  orig: {w}, {h}",
			"  offset: 0, 0",
			"  index: -1",
		]
	path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _soft() -> dict:
	return {"curve": 0.33, "c2": 0.0, "c3": 0.67, "c4": 1.0}


def _hex_rgba(r: float, g: float, b: float, a: float) -> str:
	return f"{int(round(r)):02x}{int(round(g)):02x}{int(round(b)):02x}{int(round(a)):02x}"


def pendulum_keys(amp: float, period: float, invert: bool) -> list[dict]:
	# Spine 4.1 uses `value`, not 3.8 `angle`. Cosine = harmonic hang.
	a = -abs(amp) if invert else abs(amp)
	out: list[dict] = []
	for i in range(SWING_STEPS + 1):
		angle = a * math.cos(2 * math.pi * i / SWING_STEPS)
		frame: dict = {"value": round(angle, 3)}
		if i:
			frame["time"] = round(period * i / SWING_STEPS, 4)
		if i < SWING_STEPS:
			frame.update(_soft())
		out.append(frame)
	return out


def flicker_rgba(period: float, phase: float) -> list[dict]:
	# Slow breath + faster lick + a rare dip. Deterministic, loops on `period`.
	out: list[dict] = []
	for i in range(FLICKER_STEPS + 1):
		u = i / FLICKER_STEPS
		p = u + phase
		breath = 0.62 + 0.28 * math.sin(2 * math.pi * p)
		shimmer = 0.08 * math.sin(2 * math.pi * p * 5.7 + 0.4)
		lick = 0.05 * math.sin(2 * math.pi * p * 11.3 + 1.1)
		dip = 0.12 if abs(math.sin(p * 17.0 + 2.2)) > 0.92 else 0.0
		k = max(0.38, min(1.0, breath + shimmer + lick - dip))
		frame: dict = {"color": _hex_rgba(255, 140 + 90 * k, 40 + 70 * k, 150 + 105 * k)}
		if i:
			frame["time"] = round(period * u, 4)
		if i < FLICKER_STEPS:
			frame.update(_soft())
		out.append(frame)
	return out


def flicker_scale(period: float, phase: float) -> list[dict]:
	out: list[dict] = []
	for i in range(FLICKER_STEPS + 1):
		u = i / FLICKER_STEPS
		p = u + phase
		k = 0.96 + 0.08 * math.sin(2 * math.pi * p) + 0.03 * math.sin(2 * math.pi * p * 5.7)
		frame: dict = {"x": round(k, 4), "y": round(k, 4)}
		if i:
			frame["time"] = round(period * u, 4)
		if i < FLICKER_STEPS:
			frame.update(_soft())
		out.append(frame)
	return out


def export_plate_without_lamps(psd: PSDImage) -> None:
	hide_named(list(psd), HIDE_FOR_PLATE)
	img = psd.composite(force=False).convert("RGB")
	img.save(RAW / "western_scene2.png", "PNG")
	for dest in (VITE, STATIC):
		dest.mkdir(parents=True, exist_ok=True)
		img.save(dest / "western_scene2.webp", "WEBP", quality=90, method=6)
		img.save(dest / "western_scene2.png", "PNG")
	print(f"plate without hanging lamps {img.size[0]}x{img.size[1]}")


def lamps_from_crystal() -> dict[str, tuple[Image.Image, tuple[int, int, int, int]]] | None:
	if not (READY / "left_hanging_lamp.png").is_file():
		return None
	manifest = {item["slug"]: item for item in json.loads((SRC / "manifest.json").read_text(encoding="utf-8"))}
	out = {}
	for side_name, side in LAMP_SIDES:
		item = manifest[f"{side_name}_hanging_lamp"]
		cropped = Image.open(READY / f"{side_name}_hanging_lamp.png").convert("RGBA")
		x0, y0, _, _ = item["bbox"]
		l = int(round(x0 * SCALE))
		t = int(round(y0 * SCALE))
		box = (l, t, l + cropped.width, t + cropped.height)
		out[side] = (cropped, box)
	return out


def main() -> None:
	crystal = lamps_from_crystal()
	src = sync_from_desktop(RAW / PSD_NAME)
	psd = PSDImage.open(src)
	found: dict = {}
	walk_lamps(list(psd), found)

	parts: dict[str, dict] = {}
	images: dict[str, Image.Image] = {}
	for side_name, side in LAMP_SIDES:
		if crystal:
			cropped, box = crystal[side]
		else:
			key = f"{side_name} hanging lamp"
			if key not in found:
				raise SystemExit(f"PSD missing lamp layer: {key}")
			layer = found[key]
			raw = psd.composite(layer_filter=lambda L, target=layer: L is target)
			if raw is None:
				raise SystemExit(f"{side_name} hanging lamp composite is empty")
			cropped, box = alpha_crop(raw.convert("RGBA"))
		hang = chain_rest(cropped)
		cx, cy = mass_center(cropped)
		length = math.hypot(cx - hang[0], cy - hang[1])
		body_im, light_im, glow_im, globe = split_lamp(cropped)
		body_name = f"lamp_{side}"
		light_name = f"light_{side}"
		glow_name = f"glow_{side}"
		images[body_name] = body_im
		images[light_name] = light_im
		images[glow_name] = glow_im
		parts[side] = {
			"box": box,
			"hang_local": hang,
			"globe_local": globe,
			"hang_canvas": (box[0] + hang[0], box[1] + hang[1]),
			"length": length,
			"body": body_name,
			"light": light_name,
			"glow": glow_name,
			"body_attach": attach_xy(hang, body_im),
			"light_attach": attach_xy(globe, light_im),
			"glow_attach": attach_xy((globe[0] + GLOW_PAD, globe[1] + GLOW_PAD), glow_im),
		}
		print(
			f"{side}: canvas hang ({parts[side]['hang_canvas'][0]:.1f}, "
			f"{parts[side]['hang_canvas'][1]:.1f}) globe ({globe[0]:.1f},{globe[1]:.1f}) "
			f"L={length:.1f}px"
		)

	lengths = [p["length"] for p in parts.values()]
	# Period is screen-space. Crystal lamps are 2x scene px; cover-fit keeps the same on-screen length.
	period_len = (sum(lengths) / len(lengths)) / (SCALE if crystal else 1)
	period = 2 * math.pi * math.sqrt(period_len / G)
	period = round(max(1.6, period), 4)

	sheet, boxes = pack(images)
	atlas_name = f"{SPINE_NAME}.atlas"
	png_name = f"{SPINE_NAME}.png"

	def one_skeleton(side: str, invert: bool, amp: float) -> dict:
		p = parts[side]
		bw, bh = images[p["body"]].size
		lw, lh = images[p["light"]].size
		gw, gh = images[p["glow"]].size
		hang = p["hang_local"]
		globe = p["globe_local"]
		light_x = round(globe[0] - hang[0], 3)
		light_y = round(hang[1] - globe[1], 3)
		phase = 0.37 if invert else 0.0
		# 4.1 AABB is the setup-pose box, origin = hang nail.
		min_x = min(-bw * 0.5 + p["body_attach"][0], light_x - gw * 0.5 + p["glow_attach"][0])
		min_y = min(-bh * 0.5 + p["body_attach"][1], light_y - gh * 0.5 + p["glow_attach"][1])
		max_x = max(bw * 0.5 + p["body_attach"][0], light_x + gw * 0.5 + p["glow_attach"][0])
		max_y = max(bh * 0.5 + p["body_attach"][1], light_y + gh * 0.5 + p["glow_attach"][1])
		return {
			"skeleton": {
				"hash": f"hanging-lamp-{side}",
				"spine": SPINE_VERSION,
				"x": round(min_x, 3),
				"y": round(min_y, 3),
				"width": round(max_x - min_x, 3),
				"height": round(max_y - min_y, 3),
				"images": "./",
				"audio": "",
			},
			"bones": [
				{"name": "root"},
				{"name": "hang", "parent": "root", "length": round(p["length"], 3)},
				{"name": "light", "parent": "hang", "x": light_x, "y": light_y},
			],
			"slots": [
				{"name": p["glow"], "bone": "light", "attachment": p["glow"], "blend": "additive"},
				{"name": p["body"], "bone": "hang", "attachment": p["body"]},
				{"name": p["light"], "bone": "light", "attachment": p["light"], "blend": "additive"},
			],
			"skins": [
				{
					"name": "default",
					"attachments": {
						p["glow"]: {
							p["glow"]: {
								"x": p["glow_attach"][0],
								"y": p["glow_attach"][1],
								"width": gw,
								"height": gh,
							}
						},
						p["body"]: {
							p["body"]: {
								"x": p["body_attach"][0],
								"y": p["body_attach"][1],
								"width": bw,
								"height": bh,
							}
						},
						p["light"]: {
							p["light"]: {
								"x": p["light_attach"][0],
								"y": p["light_attach"][1],
								"width": lw,
								"height": lh,
							}
						},
					},
				}
			],
			"animations": {
				"idle": {
					"bones": {
						"hang": {"rotate": pendulum_keys(amp, period, invert=invert)},
						"light": {"scale": flicker_scale(period, phase)},
					},
					"slots": {
						p["light"]: {"rgba": flicker_rgba(period, phase)},
						p["glow"]: {"rgba": flicker_rgba(period, phase + 0.08)},
					},
				}
			},
		}

	skeletons = {
		"hanging_lamp_l.json": one_skeleton("l", invert=False, amp=AMP_L),
		"hanging_lamp_r.json": one_skeleton("r", invert=True, amp=AMP_R),
	}

	gen = {
		"period": period,
		"L": {
			"x": round(parts["l"]["hang_canvas"][0], 2),
			"y": round(parts["l"]["hang_canvas"][1], 2),
		},
		"R": {
			"x": round(parts["r"]["hang_canvas"][0], 2),
			"y": round(parts["r"]["hang_canvas"][1], 2),
		},
	}

	for dest in SPINE_DIRS:
		dest.mkdir(parents=True, exist_ok=True)
		sheet.save(dest / png_name, "PNG")
		write_atlas(dest / atlas_name, png_name, sheet, boxes)
		for json_name, skeleton in skeletons.items():
			(dest / json_name).write_text(json.dumps(skeleton, indent=2), encoding="utf-8")

	gen_ts = APP / "src" / "game" / "hangingLamps.generated.ts"
	gen_ts.write_text(
		"/** Hang pivots in SCENE_ART pixels (top of each chain). From tools/build_hanging_lamps.py. */\n"
		f"export const HANGING_LAMPS = {json.dumps(gen, indent=2)} as const;\n",
		encoding="utf-8",
	)

	if crystal:
		print("skipped PSD flatten; crystal plate already exported")
	else:
		export_plate_without_lamps(psd)
	print(f"spine idle period={period}s -> {SPINE_DIRS[0]}")


if __name__ == "__main__":
	main()
