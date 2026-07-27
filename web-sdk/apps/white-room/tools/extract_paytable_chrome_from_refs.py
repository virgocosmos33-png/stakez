"""Extract blank paytable chrome plates from user reference screenshots.

Rules:
  - Blank PNGs (no baked text/icons) → HTML overlays at runtime
  - Distressed torn / paint-stroke edges (exact ref silhouettes)
  - Key solid black backgrounds to alpha
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ASSETS = Path(
	r"C:\Users\xheih\.cursor\projects\c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios\assets"
)
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

REFS = {
	"pay_table_banner": "5a4c0149-61a3-4491-9b12-bef5c9d80790",
	"special_symbols": "5bac5ec3-a706-4d55-9c02-634d0b1dc46d",
	"pay_table_payout_stack": "df235ad9-bcae-4821-8d0b-a55033bbb3d8",
	"close_x": "8c4e6012-9289-44e8-8a7d-f1460eac1b04",
	"info_speaker": "8ca28881-2a3b-46fa-af4b-6c40af5c3f72",
	"close_notched": "6290824a-51fd-4872-87d6-1c21ac5c7b3c",
}


def find_ref(uid: str) -> Path:
	hits = list(ASSETS.glob(f"*{uid}*"))
	if not hits:
		raise FileNotFoundError(uid)
	return hits[0]


def to_rgba(im: Image.Image) -> np.ndarray:
	return np.asarray(im.convert("RGBA")).astype(np.float32)


def key_black(arr: np.ndarray, thresh: float = 22.0, soft: float = 14.0) -> np.ndarray:
	out = arr.copy()
	rgb = out[..., :3]
	lum = rgb.mean(axis=2)
	mx = rgb.max(axis=2)
	a = np.clip((lum - thresh) / max(soft, 1e-3), 0, 1) * 255.0
	a = np.where(mx < thresh, 0.0, a)
	# keep saturated magenta/pink even if darkish
	r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
	mag = (r > 90) & (r > g * 1.25) & (r > b * 1.1) & ((r - g) > 25)
	a = np.where(mag, np.maximum(a, 220.0), a)
	out[..., 3] = a
	return out


def inpaint_dark_glyphs(
	arr: np.ndarray,
	*,
	lum_max: float = 55.0,
	sat_min: float = 18.0,
	passes: int = 18,
) -> np.ndarray:
	"""Fill near-black baked glyphs with surrounding plate color."""
	out = arr.copy()
	rgb = out[..., :3]
	a = out[..., 3]
	lum = rgb.mean(axis=2)
	# saturation proxy — glyphs are flat black; plate has texture/chroma
	chroma = rgb.max(axis=2) - rgb.min(axis=2)
	opaque = a > 40
	glyph = opaque & (lum < lum_max) & (chroma < sat_min)
	if not glyph.any():
		return out

	# seed fill from non-glyph opaque neighbors (box blur style)
	mask = glyph.astype(np.float32)
	work = rgb.copy()
	for _ in range(passes):
		# average 3x3 of non-glyph pixels
		pad = np.pad(work, ((1, 1), (1, 1), (0, 0)), mode="edge")
		pad_m = np.pad((~glyph) & opaque, ((1, 1), (1, 1)), mode="constant", constant_values=False)
		acc = np.zeros_like(work)
		wsum = np.zeros(work.shape[:2], dtype=np.float32)
		for dy in (-1, 0, 1):
			for dx in (-1, 0, 1):
				if dy == 0 and dx == 0:
					continue
				ys = 1 + dy
				xs = 1 + dx
				sl = pad[ys : ys + work.shape[0], xs : xs + work.shape[1]]
				m = pad_m[ys : ys + work.shape[0], xs : xs + work.shape[1]].astype(np.float32)
				acc += sl * m[..., None]
				wsum += m
		ok = (wsum > 0) & glyph
		work[ok] = acc[ok] / wsum[ok, None]
		# shrink glyph where filled
		glyph = glyph & (wsum == 0)
		if not glyph.any():
			break

	# residual: sample global plate median
	plate = opaque & ~mask.astype(bool)
	if plate.any() and glyph.any():
		med = np.median(work[plate], axis=0)
		work[glyph] = med

	out[..., :3] = work
	# soften glyph seams
	return out


def crop_alpha(arr: np.ndarray, pad: int = 2) -> np.ndarray:
	a = arr[..., 3]
	ys, xs = np.where(a > 8)
	if len(xs) == 0:
		return arr
	y0, y1 = max(0, ys.min() - pad), min(arr.shape[0], ys.max() + 1 + pad)
	x0, x1 = max(0, xs.min() - pad), min(arr.shape[1], xs.max() + 1 + pad)
	return arr[y0:y1, x0:x1]


def save(arr: np.ndarray, name: str, max_w: int = 1200, scale: float = 2.5) -> Path:
	arr = crop_alpha(arr)
	im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
	# mild denoise on alpha edge
	im = im.filter(ImageFilter.UnsharpMask(radius=0.6, percent=40, threshold=2))
	w, h = im.size
	nw = min(max_w, int(w * scale))
	nh = max(1, int(h * (nw / w)))
	im = im.resize((nw, nh), Image.Resampling.LANCZOS)

	RAW.mkdir(parents=True, exist_ok=True)
	OUT.mkdir(parents=True, exist_ok=True)
	STATIC_UI.mkdir(parents=True, exist_ok=True)
	raw_path = RAW / name.replace(".png", "_from_ref.png")
	im.save(raw_path, optimize=True)
	im.save(OUT / name, optimize=True)
	im.save(STATIC_UI / name, optimize=True)
	print(f"wrote {name} {im.size}")
	return OUT / name


def split_horizontal_bands(arr: np.ndarray, n: int = 2) -> list[np.ndarray]:
	"""Split stacked chrome into n vertical bands by alpha mass."""
	a = arr[..., 3]
	row = a.mean(axis=1)
	# find gaps (low alpha rows) between bands
	active = row > 8
	segments: list[tuple[int, int]] = []
	start = None
	for i, on in enumerate(active):
		if on and start is None:
			start = i
		elif not on and start is not None:
			segments.append((start, i))
			start = None
	if start is not None:
		segments.append((start, len(active)))
	# merge tiny noise
	segments = [(s, e) for s, e in segments if (e - s) >= 8]
	if len(segments) < n:
		# fallback equal split of bbox
		ys = np.where(active)[0]
		if len(ys) == 0:
			return [arr]
		y0, y1 = ys[0], ys[-1] + 1
		h = y1 - y0
		step = h // n
		return [arr[y0 + i * step : (y0 + (i + 1) * step if i < n - 1 else y1)] for i in range(n)]
	# take largest n
	segments = sorted(segments, key=lambda se: se[1] - se[0], reverse=True)[:n]
	segments = sorted(segments, key=lambda se: se[0])
	return [arr[s:e] for s, e in segments]


def process_pay_table_banner() -> None:
	im = Image.open(find_ref(REFS["pay_table_banner"]))
	arr = key_black(to_rgba(im), thresh=18, soft=12)
	# remove black PAY TABLE text on cream
	arr = inpaint_dark_glyphs(arr, lum_max=70, sat_min=35, passes=22)
	save(arr, "title_plate_blank.png", max_w=1100, scale=2.8)


def process_special_symbols() -> None:
	im = Image.open(find_ref(REFS["special_symbols"]))
	arr = key_black(to_rgba(im), thresh=16, soft=12)
	# keep magenta stroke; drop dark metal backing strip if present (low sat dark)
	rgb = arr[..., :3]
	a = arr[..., 3]
	r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
	mag = (r > 100) & (r > g * 1.2) & ((r - g) > 30)
	# dilate magenta mask 2px so soft paint edges survive
	m = mag.astype(np.uint8)
	pad = np.pad(m, 2, mode="constant")
	dil = np.zeros_like(m)
	for dy in range(5):
		for dx in range(5):
			dil = np.maximum(dil, pad[dy : dy + m.shape[0], dx : dx + m.shape[1]])
	arr[..., 3] = np.where(dil > 0, a, 0)
	arr = inpaint_dark_glyphs(arr, lum_max=60, sat_min=40, passes=20)
	save(arr, "section_magenta_wide.png", max_w=1100, scale=3.0)


def process_stack() -> None:
	im = Image.open(find_ref(REFS["pay_table_payout_stack"]))
	arr = key_black(to_rgba(im), thresh=16, soft=12)
	bands = split_horizontal_bands(arr, 2)
	# top = PAY TABLE torn white, bottom = PAYOUT magenta
	top = inpaint_dark_glyphs(bands[0], lum_max=70, sat_min=35, passes=22)
	# strip residual dark metal behind paper if any
	save(top, "title_plate_torn.png", max_w=1000, scale=3.0)

	bot = bands[1] if len(bands) > 1 else bands[0]
	rgb = bot[..., :3]
	r, g = rgb[..., 0], rgb[..., 1]
	mag = (r > 90) & (r > g * 1.15) & ((r - g) > 25)
	bot = bot.copy()
	bot[..., 3] = np.where(mag, bot[..., 3], 0)
	bot = inpaint_dark_glyphs(bot, lum_max=60, sat_min=40, passes=20)
	save(bot, "section_magenta.png", max_w=900, scale=3.2)


def process_close_x() -> None:
	im = Image.open(find_ref(REFS["close_x"]))
	arr = key_black(to_rgba(im), thresh=14, soft=10)
	# blank magenta square — remove black X
	arr = inpaint_dark_glyphs(arr, lum_max=80, sat_min=50, passes=24)
	save(arr, "btn_close_magenta.png", max_w=256, scale=3.5)


def process_info_speaker() -> None:
	im = Image.open(find_ref(REFS["info_speaker"]))
	arr = key_black(to_rgba(im), thresh=14, soft=10)
	bands = split_horizontal_bands(arr, 2)
	# top magenta i
	top = inpaint_dark_glyphs(bands[0], lum_max=80, sat_min=45, passes=24)
	save(top, "btn_info_magenta.png", max_w=256, scale=3.5)
	# bottom white speaker frame — remove white speaker icon fill inside, keep frame
	bot = bands[1] if len(bands) > 1 else bands[0]
	bot = bot.copy()
	rgb = bot[..., :3]
	a = bot[..., 3]
	lum = rgb.mean(axis=2)
	# keep bright frame pixels; punch interior icon (bright but more centered)
	h, w = a.shape
	yy, xx = np.mgrid[0:h, 0:w]
	cx, cy = w / 2, h / 2
	# frame = bright ring near edges of alpha bbox
	opaque = a > 40
	ys, xs = np.where(opaque)
	if len(xs):
		x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
		# distance from outer edge of bbox
		dist_in = np.minimum.reduce(
			[
				xx - x0,
				x1 - xx,
				yy - y0,
				y1 - yy,
			]
		).astype(np.float32)
		# keep outer ~18% as frame; clear interior bright icon
		frame_band = dist_in < max(4, 0.18 * min(x1 - x0, y1 - y0))
		bright = lum > 140
		# clear non-frame bright (speaker glyph)
		clear = opaque & bright & ~frame_band
		bot[..., 3] = np.where(clear, 0, a)
		# also clear dim interior
		interior = opaque & ~frame_band & (dist_in > max(5, 0.22 * min(x1 - x0, y1 - y0)))
		bot[..., 3] = np.where(interior, 0, bot[..., 3])
	save(bot, "btn_speaker_frame.png", max_w=256, scale=3.5)


def process_close_notched() -> None:
	im = Image.open(find_ref(REFS["close_notched"]))
	arr = key_black(to_rgba(im), thresh=14, soft=10)
	# keep only the notched square (upper band); drop CLOSE text under it
	bands = split_horizontal_bands(arr, 2)
	sq = bands[0]
	# remove white X inside — keep notched frame ring
	sq = sq.copy()
	rgb = sq[..., :3]
	a = sq[..., 3]
	lum = rgb.mean(axis=2)
	opaque = a > 40
	ys, xs = np.where(opaque)
	if len(xs):
		x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
		yy, xx = np.mgrid[0 : a.shape[0], 0 : a.shape[1]]
		dist_in = np.minimum.reduce([xx - x0, x1 - xx, yy - y0, y1 - yy]).astype(np.float32)
		band = max(3, 0.14 * min(x1 - x0, y1 - y0))
		frame = dist_in < band
		# keep frame bright pixels; clear interior X
		sq[..., 3] = np.where(opaque & frame, a, 0)
		# restore slight corner notches already in frame
	save(sq, "btn_close_notched.png", max_w=256, scale=3.5)


def main() -> None:
	process_pay_table_banner()
	process_stack()
	process_special_symbols()
	process_close_x()
	process_info_speaker()
	process_close_notched()
	# canonical aliases used by ModalPayTable
	# prefer riveted metal+paper banner for main title
	for src, dst in [
		("title_plate_blank.png", "title_plate_blank.png"),
		("section_magenta.png", "section_magenta.png"),
		("section_magenta_wide.png", "section_magenta_wide.png"),
	]:
		assert (OUT / src).exists(), src
	print("done ->", OUT)


if __name__ == "__main__":
	main()
