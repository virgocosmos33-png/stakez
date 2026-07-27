"""Extract blank magenta chevron plate from intro-carousel arrow ref.

Scrubs baked black chevron so runtime can overlay Impact < / >.
Also syncs btn_close_magenta + accent_stain into ways buy_ui for Pixi.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

REF = Path(
	r"C:\Users\xheih\.cursor\projects\c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios"
	r"\assets\c__Users_xheih_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_"
	r"image-80a57f30-a5dd-4679-9e71-fad653c94ca3.png"
)
WAYS = Path(__file__).resolve().parent.parent
PKG = WAYS.parents[1] / "packages" / "components-ui-html" / "src" / "assets" / "paytable"
BUY_UI = [
	WAYS / "assets" / "sprites" / "mirror" / "buy_ui",
	WAYS / "static" / "assets" / "sprites" / "mirror" / "buy_ui",
]
OUTS = [
	*(root / "chevron_plate.png" for root in BUY_UI),
	PKG / "chevron_plate.png",
	WAYS / "static" / "assets" / "paytable_ui" / "chevron_plate.png",
]


def main() -> None:
	close_src = PKG / "btn_close_magenta.png"
	stain_src = PKG / "accent_stain.png"
	for name, src in (("btn_close_magenta.png", close_src), ("accent_stain.png", stain_src)):
		for dest_root in BUY_UI:
			dest = dest_root / name
			dest.write_bytes(src.read_bytes())
			print("copied", dest)

	arr = np.asarray(Image.open(REF).convert("RGBA")).astype(np.float32)
	rgb = arr[..., :3]
	r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
	mx = rgb.max(axis=2)
	mag = (r > 55) & (r > g * 1.1) & (r > b * 1.0) & ((r - np.minimum(g, b)) > 15)
	alpha = np.where(mag, 255.0, np.clip((mx - 20) / 20, 0, 1) * 255)
	alpha = np.where((~mag) & (mx < 40), 0.0, alpha)
	arr[..., 3] = alpha

	ys, xs = np.where(mag)
	y0, y1 = int(ys.min()), int(ys.max())
	x0, x1 = int(xs.min()), int(xs.max())
	cy, cx = (y0 + y1) / 2, (x0 + x1) / 2
	edge = []
	for y, x in zip(ys, xs):
		if abs(y - cy) > (y1 - y0) * 0.28 or abs(x - cx) > (x1 - x0) * 0.28:
			edge.append(rgb[y, x])
	med = np.median(np.array(edge), axis=0) if edge else np.array([180.0, 20.0, 70.0])
	print("median plate", med, "bbox", x0, y0, x1, y1)

	lum = rgb.mean(axis=2)
	chroma = rgb.max(axis=2) - rgb.min(axis=2)
	yy, xx = np.mgrid[0 : arr.shape[0], 0 : arr.shape[1]]
	dist = np.sqrt(((yy - cy) / (y1 - y0 + 1e-3)) ** 2 + ((xx - cx) / (x1 - x0 + 1e-3)) ** 2)
	in_plate = mag | ((yy >= y0) & (yy <= y1) & (xx >= x0) & (xx <= x1) & (alpha > 40))
	glyph = in_plate & (lum < 85) & (chroma < 55) & (dist < 0.42)
	glyph |= (
		(yy >= y0)
		& (yy <= y1)
		& (xx >= x0)
		& (xx <= x1)
		& (lum < 70)
		& (chroma < 45)
		& (dist < 0.45)
	)
	print("glyph px", int(glyph.sum()))

	rng = np.random.default_rng(0)
	noise = rng.normal(0, 8, size=(*glyph.shape, 3))
	fill = np.clip(med + noise, 0, 255)
	for c in range(3):
		channel = arr[..., c]
		channel[glyph] = fill[..., c][glyph]
		arr[..., c] = channel
	arr[..., 3][glyph] = 255

	ys, xs = np.where(arr[..., 3] > 20)
	crop = arr[max(0, ys.min() - 2) : ys.max() + 3, max(0, xs.min() - 2) : xs.max() + 3].astype(
		np.uint8
	)
	im = Image.fromarray(crop, "RGBA").resize(
		(crop.shape[1] * 2, crop.shape[0] * 2), Image.Resampling.NEAREST
	)
	for p in OUTS:
		p.parent.mkdir(parents=True, exist_ok=True)
		im.save(p)
		print("wrote", p, im.size)

	chk = np.asarray(im).astype(np.float32)
	rgb = chk[..., :3]
	a = chk[..., 3]
	lum = rgb.mean(2)
	chroma = rgb.max(2) - rgb.min(2)
	r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
	mag = (r > 55) & (r > g * 1.1) & (r > b * 1.0)
	h, w = chk.shape[:2]
	dark = (a > 80) & (lum < 70) & (chroma < 40) & ~mag
	print(
		"center dark",
		int(dark[int(h * 0.25) : int(h * 0.75), int(w * 0.25) : int(w * 0.75)].sum()),
		"total dark",
		int(dark.sum()),
	)


if __name__ == "__main__":
	main()
