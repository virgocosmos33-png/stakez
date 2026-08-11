"""Bake the NON-SPLIT feature-event VFX (nudge / gunsmoke / dig-up / coffin-open
/ special-bar / bounty) into one Tombstone-tinted atlas plus a handful of hero
sprites.

This is the SOURCE OF TRUTH for those assets — never hand-edit the baked PNGs.

Inputs
  assets-raw/tombstone_feature_vfx/**   Kenney CC0 families (copy of the library,
                                        see KENNEY_HAUL below for the exact dirs)
  assets-raw/scenario_western_vfx/*.png already-downloaded Scenario library art
                                        (read-only reuse; nothing is generated here)

Outputs
  static/assets/sprites/fx/tombstone_feature_vfx.png + .json   spriteSheet atlas
  static/assets/sprites/fx/fx_*.png                            hero sprites

Frame ORDER in the atlas is the binding contract for src/game/featureVfx.ts —
appending is safe, reordering is not.

Alpha hygiene: every source is edge-bled (opaque colour dilated outward under the
soft alpha) and then zeroed under fully transparent pixels, so the textures are
safe for premultiplied blending and mipmaps and can never fringe white on the
dark graveyard board.

Run:  python tools/make_tombstone_feature_vfx_atlas.py
"""

from __future__ import annotations

import json
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
KENNEY = os.path.join(APP, "assets-raw", "tombstone_feature_vfx")
SCENARIO = os.path.join(APP, "assets-raw", "scenario_western_vfx")
OUT = os.path.join(APP, "static", "assets", "sprites", "fx")

CELL = 160
COLUMNS = 8
ALPHA_FLOOR = 8
BLEED_PASSES = 6

# The Kenney library folders this haul came from (kenney skill: announce the pull).
KENNEY_HAUL = [
	"kenney_particle-pack/PNG (Transparent)  (77 -> smoke, dust, muzzle, flash,"
	" spark, slash, twirl, dirt)",
	"kenney_light-masks-1.0/Transparent      (36 -> glow, ring, cones, god-rays)",
	"kenney_splat-pack/PNG/Default (256px)   (36 -> dirt splat decals)",
	"kenney_smoke-particles/PNG/Explosion    (9  -> grave burst)",
	"kenney_smoke-particles/PNG/Black smoke  (25 -> held, superseded by particle smoke)",
	"kenney_smoke-particles/PNG/White puff   (25 -> held, superseded by particle smoke)",
	"kenney_smoke-particles/PNG/Flash        (9  -> held, superseded by muzzle_*)",
	"kenney_pattern-pack/PNG/Default         (18 -> grit grain)",
]

# ---------------------------------------------------------------------------
# Tombstone palette (mirrors src/game/tombstoneVfx.ts TOMBSTONE_FX)
# ---------------------------------------------------------------------------
# Gunsmoke has to READ against a near-black graveyard plate, so it sits well
# above the ink-grey the source frames start at.
GUNSMOKE = (152, 142, 128)
POWDER = (86, 62, 42)
SAND = (196, 168, 124)
BONE = (212, 196, 168)
EMBER = (214, 126, 52)
FLASH_AMBER = (255, 206, 132)
RUST = (168, 74, 40)
# Powder burn on a near-black card: ash, not soot. A charcoal smudge on a
# charcoal plate is an invisible mark, which defeats the point of the mark.
SOOT = (104, 84, 66)
BRASS = (222, 182, 96)
# Dusty lantern warmth, deliberately NOT a cool clinical white shaft.
GRAVELIGHT = (176, 158, 122)

# name, source (folder/file), tint RGB, contrast, mode
#   mode 'luma'  — recolour by brightness (sources that carry their own shading)
#   mode 'alpha' — recolour by coverage (flat black/white sources; a luma tint
#                  would multiply black art straight back to black)
FRAMES: list[tuple[str, str, tuple[int, int, int], float, str]] = []


def _files(prefix: str, folder: str, names: list[str], tint, contrast, mode="luma"):
	for order, name in enumerate(names):
		FRAMES.append((f"{prefix}{order}", f"{folder}/{name}", tint, contrast, mode))


def _seq(prefix: str, folder: str, stem: str, indices: list[int], tint, contrast, mode="luma"):
	_files(prefix, folder, [f"{stem}{index:02d}.png" for index in indices], tint, contrast, mode)


# The first pass of this atlas used the smoke-pack "Black smoke" / "White puff"
# sequences and the tiny particle-pack flare/ring/scorch stills. On the board
# those read exactly as the user described them: flat cream and grey stickers,
# a hairline amber outline around an empty cell, tiny dots, and orange spikes.
# The particle pack carries the same families as full, internally shaded clouds
# and proper radial lights, so everything below is sourced from those instead.

# 0..7  gunsmoke plume — the revolver's exhaust, drifting and thinning
_files(
	"gunsmoke", "particles",
	[f"smoke_{n:02d}.png" for n in (1, 2, 3, 4, 5, 6, 7, 8)], GUNSMOKE, 1.05,
)
# 8..15 grave dust — kicked dirt and the trail behind the nudge rider. Same
# family, warmer and drier, walked in a different order so a plume and a dust
# kick never show the identical silhouette back to back.
_files(
	"dust", "particles",
	[f"smoke_{n:02d}.png" for n in (9, 10, 4, 6, 2, 8, 5, 3)], SAND, 1.0,
)
# 16..19 muzzle flash — directional cone, points UP at rest, callers rotate it
_files("muzzle", "particles", [f"muzzle_{n:02d}.png" for n in (2, 3, 4, 5)], FLASH_AMBER, 1.2)
# 20..23 impact flash — omnidirectional bloom, for a hit with no barrel behind
# it. Soft radials only: the particle pack's spark_* and star_* are forked
# lightning and four-point arcade stars, and its circle_02/circle_04 are
# hairline RING outlines, which on a dark card read as exactly the "empty cell
# with a yellow circle round it" this atlas was rebuilt to get rid of.
_files(
	"flash", "particles",
	["circle_05.png", "star_05.png", "magic_05.png", "flare_01.png"], FLASH_AMBER, 1.25,
)
# 24..27 grave burst — the coffin lid letting go. The source is a fireball, but
# it is tinted to lit SAND rather than fire: a grave opening throws dust, not
# flame. It was previously tinted POWDER, which multiplied an already-dark
# board plate down to an invisible brown smudge — the coffinOpen event had no
# visible hero beat at all as a result.
_seq("burst", "explosion/Explosion", "explosion", [0, 2, 4, 6], SAND, 1.3)

FRAMES += [
	# 28..30 dirt clods. The particle pack's dirt_* stills are fine sprays of
	# pinpoint specks; shrunk to a cell they scatter as loose white dots rather
	# than reading as thrown earth, so the clods are cut from the splat pack —
	# solid, irregular, and unmistakably a lump of dirt at any size.
	("dirt0", "splat/splat07.png", POWDER, 1.0, "alpha"),
	("dirt1", "splat/splat15.png", (110, 84, 54), 1.0, "alpha"),
	("dirt2", "splat/splat23.png", (128, 98, 62), 1.0, "alpha"),
	# 31..33 powder burn left on a scored card. Soft ash smudges — the
	# particle pack's scorch_* stills are spiked splatter stars and stamped
	# themselves onto the symbol art like stickers.
	("scorch0", "particles/smoke_05.png", SOOT, 0.95, "luma"),
	("scorch1", "particles/smoke_08.png", (96, 76, 60), 0.95, "luma"),
	("scorch2", "particles/smoke_02.png", (112, 90, 70), 0.95, "luma"),
	# 34..36 spent-brass sparks — short hot streaks. The pack's spark_* files
	# are forked lightning bolts, which read as loose squiggles over a card.
	# These are the pack's THICK traces on purpose: the hairline ones (trace_01,
	# _04, _07) covered under half a percent of their tile, so once scaled down
	# to a cell they fell under a pixel and the brass simply never appeared.
	("spark0", "particles/trace_05.png", BRASS, 1.4, "luma"),
	("spark1", "particles/trace_06.png", (236, 198, 120), 1.4, "luma"),
	("spark2", "particles/trace_03.png", (204, 150, 70), 1.4, "luma"),
	# 37..39 speed streaks dragged behind a moving card. slash_* are crescent
	# arcs: laid behind the nudge rider they read as a stray amber hoop floating
	# beside the card, not as motion. trace_* are straight tapered streaks.
	("trace0", "particles/trace_02.png", BRASS, 1.4, "luma"),
	("trace1", "particles/trace_05.png", (230, 176, 96), 1.4, "luma"),
	("trace2", "particles/trace_06.png", (200, 140, 66), 1.4, "luma"),
	# 40..42 dirt splats (grave spoil thrown onto the plate)
	("splat0", "splat/splat04.png", POWDER, 1.0, "alpha"),
	("splat1", "splat/splat12.png", (98, 74, 48), 1.0, "alpha"),
	("splat2", "splat/splat20.png", (120, 92, 58), 1.0, "alpha"),
	# 43..45 swipe arcs — the crescent a shunted or riding card cuts
	("swipe0", "particles/twirl_01.png", BRASS, 1.3, "luma"),
	("swipe1", "particles/twirl_02.png", (228, 176, 96), 1.3, "luma"),
	("swipe2", "particles/twirl_03.png", (198, 140, 66), 1.3, "luma"),
	# 46 lantern glow, 47 halo ring.
	# Both come from the light-mask pack: a big soft radial falloff and a THICK
	# soft ring. The particle-pack light_02 was a dark double lobe and ring_c a
	# one-pixel circle, which is where the "empty cell with an amber outline"
	# came from.
	("glow", "lights/circle_c.png", EMBER, 1.0, "luma"),
	("ring", "lights/ring_b.png", EMBER, 1.2, "luma"),
	# 48..50 grave light (dusty lantern shaft out of an opened plot). The
	# `*_composed_c` masks in this pack are straight vertical bars, which on a
	# cell read as a grey stripe rather than light escaping a plot; the
	# `cone_composed_*` masks are real spreading cones.
	("shaft0", "lights/cone_composed_c.png", GRAVELIGHT, 1.25, "luma"),
	("shaft1", "lights/cone_composed_d.png", GRAVELIGHT, 1.25, "luma"),
	("shaft2", "lights/cone_composed_e.png", BONE, 1.25, "luma"),
]

# Hero sprites straight from the Scenario library the user already generated.
#
# Deliberately NOT baked:
#   burst_dark        a spiked black star. Recoloured it still reads as an
#                     orange spiked sticker glued over the card — the exact
#                     look that got the first pass rejected.
#   muzzle_flash_chrome  stark black-and-white ink art, off-tone next to the
#                     painted graveyard board; muzzle_flash_wood carries the
#                     same beat in the right register.
#   dust_kick_outlaw  a full-body figure. Dig-up is a cell-level event, so it
#                     now plants a spade instead (tools/make_digup_shovel.py).
#   spark_streak_gold a single long gold sparkler. It only ever read as a
#                     stray streak over the nudge rider; FX.trace does the job.
#   starburst_gold    a multi-point star. Behind a bountied card on a near-black
#                     board its points read as a fan of hard grey-white
#                     triangles laid across the symbol — the stray-spike look
#                     the first pass was rejected for. Bounty blooms instead.
HEROES: list[tuple[str, str, int]] = [
	("fx_dust_plume", "dust_plume.png", 768),
	("fx_muzzle_flash", "muzzle_flash_wood.png", 640),
]


def load_rgba(path: str) -> Image.Image:
	if not os.path.isfile(path):
		raise SystemExit(f"missing source: {path}")
	return Image.open(path).convert("RGBA")


def bleed_alpha(image: Image.Image) -> Image.Image:
	"""Dilate opaque colour into the soft/transparent margin, then zero the RGB
	under fully transparent pixels.

	Scenario exports leave white (255,255,255) under transparent pixels, which
	bleeds a bright fringe as soon as the texture is filtered or mipmapped on a
	dark background. Standard edge-padding fixes it at the source."""
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


def tint_luma(image: Image.Image, rgb: tuple[int, int, int], contrast: float) -> Image.Image:
	"""Recolour by luminance, keeping a whisper of the original chroma so soft
	particles do not go flat. Same treatment as the split VFX atlas.

	The luminance is normalised against the source's own brightest pixels first.
	Kenney's particle clouds are painted mid-grey (peak luma ~0.38), so a raw
	multiply by the tint lands them at a third of their intended value — dark
	smoke on a near-black graveyard board, i.e. invisible."""
	data = np.array(image).astype(np.float32)
	src = data[..., :3]
	alpha = data[..., 3]
	luma = (0.2126 * src[..., 0] + 0.7152 * src[..., 1] + 0.0722 * src[..., 2]) / 255.0
	opaque = alpha > 24
	if opaque.any():
		peak = float(np.percentile(luma[opaque], 99))
		if peak > 0.02:
			luma = np.clip(luma / peak, 0.0, 1.0)
	luma = np.clip((luma - 0.5) * contrast + 0.5, 0.0, 1.0)
	tint = np.array(rgb, dtype=np.float32)
	toned = np.clip(tint * luma[..., None] * 0.88 + src * 0.12, 0, 255)
	out = np.dstack([toned, alpha]).astype(np.uint8)
	out[alpha <= ALPHA_FLOOR] = (0, 0, 0, 0)
	return Image.fromarray(out, "RGBA")


def tint_silhouette(image: Image.Image, rgb: tuple[int, int, int]) -> Image.Image:
	"""Colour a flat silhouette from its own alpha so the shape survives: the
	core takes the full tint, the feathered edge darkens toward powder burn."""
	data = np.array(image).astype(np.float32)
	alpha = data[..., 3]
	strength = np.clip(alpha / 255.0, 0.0, 1.0)
	tint = np.array(rgb, dtype=np.float32)
	toned = tint[None, None, :] * (0.35 + 0.65 * strength)[..., None]
	out = np.dstack([toned, alpha]).astype(np.uint8)
	out[alpha <= ALPHA_FLOOR] = (0, 0, 0, 0)
	return Image.fromarray(out, "RGBA")


def normalise_alpha(image: Image.Image, peak: int = 240) -> Image.Image:
	"""Scale coverage so the frame's densest pixel reaches `peak`.

	Several of the light masks top out around a tenth of full alpha. Left alone
	they are invisible at any sane caller alpha, and the temptation is then to
	draw them at alpha > 1 or stack copies. Normalising here keeps the source's
	falloff and hands the callers a predictable 0..1 range."""
	data = np.array(image).astype(np.float32)
	alpha = data[..., 3]
	current = float(alpha.max())
	if current < 1.0:
		return image
	data[..., 3] = np.clip(alpha * (peak / current), 0, 255)
	return Image.fromarray(data.astype(np.uint8), "RGBA")


def resize_rgba(image: Image.Image, size: tuple[int, int]) -> Image.Image:
	"""Resize through premultiplied alpha.

	Straight RGBA resampling mixes the colour of transparent pixels into the
	visible edge. Every source here is zeroed to black under transparency, so a
	naive resize drags a soft particle's whole body toward black — which is how
	the first bake turned bright Kenney smoke into an invisible grey smear."""
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


def alpha_crop(image: Image.Image) -> Image.Image:
	mask = image.getchannel("A").point(lambda value: 255 if value > ALPHA_FLOOR else 0)
	box = mask.getbbox()
	if box is None:
		raise SystemExit("source is fully transparent")
	return image.crop(box)


def fit_square(image: Image.Image, size: int, fill: float = 0.94) -> Image.Image:
	scale = min(size / image.width, size / image.height) * fill
	nw = max(1, round(image.width * scale))
	nh = max(1, round(image.height * scale))
	resized = resize_rgba(image, (nw, nh))
	canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
	canvas.paste(resized, ((size - nw) // 2, (size - nh) // 2), resized)
	return canvas


def fit_box(image: Image.Image, longest: int) -> Image.Image:
	scale = min(1.0, longest / max(image.width, image.height))
	nw = max(1, round(image.width * scale))
	nh = max(1, round(image.height * scale))
	return resize_rgba(image, (nw, nh))


def bake_atlas() -> None:
	baked: list[tuple[str, Image.Image]] = []
	for name, rel, tint, contrast, mode in FRAMES:
		art = alpha_crop(bleed_alpha(load_rgba(os.path.join(KENNEY, rel.replace("/", os.sep)))))
		art = tint_silhouette(art, tint) if mode == "alpha" else tint_luma(art, tint, contrast)
		baked.append((name, fit_square(normalise_alpha(art), CELL)))

	rows = (len(baked) + COLUMNS - 1) // COLUMNS
	atlas = Image.new("RGBA", (CELL * COLUMNS, CELL * rows), (0, 0, 0, 0))
	meta_frames: dict[str, dict] = {}
	for index, (name, art) in enumerate(baked):
		col = index % COLUMNS
		row = index // COLUMNS
		x, y = col * CELL, row * CELL
		atlas.paste(art, (x, y), art)
		# key carries the ordinal so the loaded texture ARRAY order is obvious
		meta_frames[f"fx_{index:02d}_{name}.png"] = {
			"frame": {"x": x, "y": y, "w": CELL, "h": CELL},
			"rotated": False,
			"trimmed": False,
			"spriteSourceSize": {"x": 0, "y": 0, "w": CELL, "h": CELL},
			"sourceSize": {"w": CELL, "h": CELL},
		}

	png_path = os.path.join(OUT, "tombstone_feature_vfx.png")
	json_path = os.path.join(OUT, "tombstone_feature_vfx.json")
	atlas.save(png_path, optimize=True)
	with open(json_path, "w", encoding="utf-8") as handle:
		json.dump(
			{
				"frames": meta_frames,
				"meta": {
					"image": "tombstone_feature_vfx.png",
					"format": "RGBA8888",
					"size": {"w": atlas.width, "h": atlas.height},
					"scale": "1",
					"kenney_sources": KENNEY_HAUL,
				},
			},
			handle,
			indent=1,
		)
	print(f"[feature_vfx] atlas {len(baked)} frames -> {png_path} ({os.path.getsize(png_path):,} B)")


def bake_heroes() -> None:
	for name, source, longest in HEROES:
		art = fit_box(alpha_crop(bleed_alpha(load_rgba(os.path.join(SCENARIO, source)))), longest)
		path = os.path.join(OUT, f"{name}.png")
		art.save(path, optimize=True)
		print(f"[feature_vfx] {name} {art.width}x{art.height} <- scenario/{source}")


def main() -> None:
	os.makedirs(OUT, exist_ok=True)
	bake_atlas()
	bake_heroes()
	print("[feature_vfx] Kenney haul:")
	for line in KENNEY_HAUL:
		print(f"  - {line}")


if __name__ == "__main__":
	main()
