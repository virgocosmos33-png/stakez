"""Key prop_19 / bullets and install Kenney wound overlays for Gunsmoke.

Masters: assets-raw/gunsmoke_props/prop_{19,22,23,24}.png
Kenney haul: assets-raw/kenney/gunsmoke-wounds/ (CC0 particle + splat + flash)

Outputs go to assets-src/sprites/fx/ and static/assets/sprites/fx/.
Also writes src/game/gunsmokeArt.generated.ts with measured pivots.

Run:  python tools/bake_gunsmoke_props.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
RAW_PROPS = os.path.join(APP, "assets-raw", "gunsmoke_props")
RAW_WOUNDS = os.path.join(APP, "assets-raw", "kenney", "gunsmoke-wounds")
OUT_DIRS = [
	os.path.join(APP, "assets-src", "sprites", "fx"),
	os.path.join(APP, "static", "assets", "sprites", "fx"),
]
GEN_TS = os.path.join(APP, "src", "game", "gunsmokeArt.generated.ts")

sys.path.insert(0, HERE)
from alpha_key import ALPHA_FLOOR, alpha_crop, bleed_alpha, fit_longest, key_black  # noqa: E402

SENTINEL = (255, 0, 255)
GUN_FLOOD_THRESH = 16
GUN_LONGEST = 1024
BULLET_LONGEST = 256
HOLE_LONGEST = 256
BLOOD = (138, 16, 22)

HOLE_SOURCES = (
	("scratch", "scratch_01.png", "gs_wound_hole_1.png"),
	("scorch", "scorch_01.png", "gs_wound_hole_2.png"),
	("scorch", "scorch_02.png", "gs_wound_hole_3.png"),
	("scorch", "scorch_03.png", "gs_wound_hole_4.png"),
	("dirt", "dirt_01.png", "gs_wound_hole_5.png"),
	("dirt", "dirt_02.png", "gs_wound_hole_6.png"),
	("slash", "slash_01.png", "gs_wound_hole_7.png"),
	("slash", "slash_02.png", "gs_wound_hole_8.png"),
)

BLOOD_SOURCES = (
	"splat00.png",
	"splat04.png",
	"splat08.png",
	"splat14.png",
	"splat19.png",
	"splat26.png",
	"splat28.png",
	"splat33.png",
)


def save_all(image: Image.Image, name: str) -> None:
	for folder in OUT_DIRS:
		os.makedirs(folder, exist_ok=True)
		path = os.path.join(folder, name)
		image.save(path, "PNG")
		print(f"wrote {path}")


def key_black_flood(image: Image.Image, thresh: int = GUN_FLOOD_THRESH) -> Image.Image:
	"""Drop the border-connected black void. Dark metal inside the silhouette stays."""
	work = image.convert("RGB")
	flood = work.copy()
	width, height = flood.size
	seeds = [
		(0, 0),
		(width - 1, 0),
		(0, height - 1),
		(width - 1, height - 1),
		(width // 2, 0),
		(width // 2, height - 1),
		(0, height // 2),
		(width - 1, height // 2),
	]
	for seed in seeds:
		if flood.getpixel(seed) != SENTINEL:
			ImageDraw.floodfill(flood, seed, SENTINEL, thresh=thresh)

	marked = np.asarray(flood)
	is_bg = (
		(marked[..., 0] == SENTINEL[0])
		& (marked[..., 1] == SENTINEL[1])
		& (marked[..., 2] == SENTINEL[2])
	)
	src = np.asarray(work).astype(np.float32)
	# punch fully-black pockets (trigger guard) that flood cannot reach
	luma = src.max(axis=2)
	is_bg = is_bg | (luma < 7.0)
	alpha = np.where(is_bg, 0.0, 255.0)
	out = np.dstack([src, alpha]).astype(np.uint8)
	return Image.fromarray(out, "RGBA")


def finish_plate(image: Image.Image, longest: int) -> Image.Image:
	return fit_longest(bleed_alpha(alpha_crop(image)), longest)


def weighted_centroid(alpha: np.ndarray, weights: np.ndarray | None = None) -> tuple[float, float]:
	if weights is None:
		weights = alpha
	mass = weights.sum()
	if mass <= 1e-4:
		ys, xs = np.nonzero(alpha > 16)
		return float(xs.mean()), float(ys.mean())
	ys, xs = np.indices(alpha.shape)
	return float((xs * weights).sum() / mass), float((ys * weights).sum() / mass)


def measure_gun(image: Image.Image) -> dict[str, float]:
	data = np.asarray(image).astype(np.float32)
	rgb = data[..., :3] / 255.0
	alpha = data[..., 3] / 255.0
	visible = np.maximum(alpha - 0.12, 0.0)

	# cylinder: warm gold / brass cluster
	gold = np.clip(rgb[..., 0] * 1.15 * rgb[..., 1] - rgb[..., 2] * 0.85, 0.0, 1.0)
	gold *= visible
	gold *= gold > 0.12
	cx, cy = weighted_centroid(visible, gold if gold.sum() > 20 else visible)

	# muzzle: farthest visible pixel from the cylinder along the bright-metal axis
	ys, xs = np.nonzero(visible > 0.2)
	dx = xs.astype(np.float32) - cx
	dy = ys.astype(np.float32) - cy
	# barrel is the long bright direction — prefer pixels that are both far and lit
	lit = rgb[ys, xs].max(axis=1)
	score = np.hypot(dx, dy) * (0.55 + 0.45 * lit)
	tip = int(np.argmax(score))
	mx, my = float(xs[tip]), float(ys[tip])
	native = float(np.arctan2(my - cy, mx - cx))
	return {
		"width": float(image.width),
		"height": float(image.height),
		"anchorX": cx / image.width,
		"anchorY": cy / image.height,
		"muzzleX": mx / image.width,
		"muzzleY": my / image.height,
		"nativeBarrel": native,
	}


def measure_bullet(image: Image.Image) -> float:
	data = np.asarray(image).astype(np.float32)
	alpha = data[..., 3] / 255.0
	ys, xs = np.nonzero(alpha > 0.2)
	if xs.size < 8:
		return -np.pi / 4
	pts = np.stack([xs.astype(np.float32), ys.astype(np.float32)], axis=1)
	mean = pts.mean(axis=0)
	cov = np.cov((pts - mean).T)
	vals, vecs = np.linalg.eigh(cov)
	axis = vecs[:, int(np.argmax(vals))]
	# tip is the extreme in the brighter / narrower direction
	proj = (pts - mean) @ axis
	lo, hi = pts[int(np.argmin(proj))], pts[int(np.argmax(proj))]
	# the tip is usually the smaller cluster — pick the end farther from the mass centre of fat pixels
	fat = alpha[ys, xs]
	fat_mean = np.array([(xs * fat).sum(), (ys * fat).sum()]) / max(fat.sum(), 1e-4)
	tip = hi if np.linalg.norm(hi - fat_mean) > np.linalg.norm(lo - fat_mean) else lo
	return float(np.arctan2(tip[1] - fat_mean[1], tip[0] - fat_mean[0]))


def recolor_blood(image: Image.Image) -> Image.Image:
	data = np.asarray(image.convert("RGBA")).astype(np.float32)
	alpha = data[..., 3]
	# Kenney splats are dark ink — keep their coverage, paint blood
	coverage = np.clip(alpha / 255.0, 0.0, 1.0)
	out = np.zeros_like(data)
	out[..., 0] = BLOOD[0]
	out[..., 1] = BLOOD[1]
	out[..., 2] = BLOOD[2]
	out[..., 3] = alpha * (0.55 + 0.45 * coverage)
	return Image.fromarray(out.astype(np.uint8), "RGBA")


def bake_gun() -> dict[str, float]:
	src = Image.open(os.path.join(RAW_PROPS, "prop_19.png"))
	keyed = key_black_flood(src)
	plate = finish_plate(keyed, GUN_LONGEST)
	save_all(plate, "tr_gunsmoke_revolver.png")
	layout = measure_gun(plate)
	print("gun", json.dumps(layout, indent=2))
	return layout


def bake_bullets() -> list[dict[str, float | str]]:
	out: list[dict[str, float | str]] = []
	names = (("prop_22.png", "gunsmoke_bullet_a.png", "gunsmokeBulletA"),
	         ("prop_23.png", "gunsmoke_bullet_b.png", "gunsmokeBulletB"),
	         ("prop_24.png", "gunsmoke_bullet_c.png", "gunsmokeBulletC"))
	for src_name, dest_name, key in names:
		src = Image.open(os.path.join(RAW_PROPS, src_name))
		plate = finish_plate(key_black(src, 0.03, 0.11), BULLET_LONGEST)
		save_all(plate, dest_name)
		native = measure_bullet(plate)
		print(f"bullet {key} native={native:.3f} {plate.size}")
		out.append({"key": key, "file": dest_name, "native": native})
	return out


def bake_wounds() -> tuple[list[str], list[str]]:
	holes: list[str] = []
	for folder, src_name, dest_name in HOLE_SOURCES:
		src = Image.open(os.path.join(RAW_WOUNDS, folder, src_name)).convert("RGBA")
		plate = finish_plate(src, HOLE_LONGEST)
		save_all(plate, dest_name)
		holes.append(dest_name.replace(".png", ""))

	bloods: list[str] = []
	for index, src_name in enumerate(BLOOD_SOURCES, start=1):
		src = Image.open(os.path.join(RAW_WOUNDS, "splat", src_name)).convert("RGBA")
		plate = finish_plate(recolor_blood(src), HOLE_LONGEST)
		dest_name = f"gs_wound_blood_{index}.png"
		save_all(plate, dest_name)
		bloods.append(dest_name.replace(".png", ""))

	# muzzle glow helpers (Kenney light masks)
	for src_name, dest_name in (
		("circle_a.png", "gs_muzzle_glow.png"),
		("circle_a_streaks.png", "gs_muzzle_streak.png"),
	):
		src = Image.open(os.path.join(RAW_WOUNDS, "light", src_name)).convert("RGBA")
		save_all(finish_plate(src, 384), dest_name)
	return holes, bloods


def write_ts(gun: dict[str, float], bullets: list[dict[str, float | str]]) -> None:
	lines = [
		"/** Generated by tools/bake_gunsmoke_props.py — re-run the baker to refresh. */",
		"export const GUNSMOKE_ART = {",
		"	gun: {",
		f"		width: {gun['width']:.1f},",
		f"		height: {gun['height']:.1f},",
		f"		anchorX: {gun['anchorX']:.4f},",
		f"		anchorY: {gun['anchorY']:.4f},",
		f"		muzzleX: {gun['muzzleX']:.4f},",
		f"		muzzleY: {gun['muzzleY']:.4f},",
		f"		nativeBarrel: {gun['nativeBarrel']:.4f},",
		"	},",
		"	bullets: [",
	]
	for bullet in bullets:
		lines.append(
			f"		{{ key: '{bullet['key']}', native: {float(bullet['native']):.4f} }},"
		)
	lines += [
		"	],",
		"} as const;",
		"",
	]
	os.makedirs(os.path.dirname(GEN_TS), exist_ok=True)
	with open(GEN_TS, "w", encoding="utf-8", newline="\n") as handle:
		handle.write("\n".join(lines))
	print(f"wrote {GEN_TS}")


def main() -> None:
	for required in ("prop_19.png", "prop_22.png", "prop_23.png", "prop_24.png"):
		path = os.path.join(RAW_PROPS, required)
		if not os.path.exists(path):
			raise SystemExit(f"missing {path}")
	gun = bake_gun()
	bullets = bake_bullets()
	holes, bloods = bake_wounds()
	write_ts(gun, bullets)
	print("holes", holes)
	print("bloods", bloods)


if __name__ == "__main__":
	main()
