"""Bake WAYS / MULTI / WIN boxes from the SAME plank sheet as the reel frame.

tools/make_board_frame_image.py lays tr_frame_planks_v2.png + tr_frame_scraps.png
around the staircase. This cuts those same boards into a small carpentry frame
with a dark well for gold text — three of these sit in the sky pocket above the
short right reels.

Run:  python tools/make_wood_readout_box.py
"""

from __future__ import annotations

import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from make_board_frame_image import load_plank_bands, load_scrap_pieces, plank_segment

REL = os.path.join("sprites", "tombstone", "wood_readout_box.png")

# sprite canvas — extra margin so split ends hang off the well, like the frame
W, H = 640, 400
WELL = (110, 90, 530, 310)  # l, t, r, b of the dark inset
THICK = 58
OVER = 36
SEED = 1887


def lay(dst: Image.Image, shadow: Image.Image, piece: Image.Image, cx: float, cy: float) -> None:
	px = int(round(cx - piece.width / 2))
	py = int(round(cy - piece.height / 2))
	sh = Image.new("RGBA", piece.size, (0, 0, 0, 0))
	sh.paste((0, 0, 0, 150), (0, 0), piece.getchannel("A"))
	shadow.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)), (px + 3, py + 4))
	dst.alpha_composite(piece, (px, py))


def main() -> None:
	planks = load_plank_bands()
	scraps = load_scrap_pieces()
	rng = random.Random(SEED)

	out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
	shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))

	l, t, r, b = WELL
	cx, cy = (l + r) / 2, (t + b) / 2
	well_w, well_h = r - l, b - t

	# four boards around the well, overlapping at the corners (same carpentry
	# as the reel frame — two overlapping pieces on the long sides)
	top = plank_segment(planks, rng, well_w + 2 * OVER, int(THICK * rng.uniform(0.9, 1.1)))
	bot = plank_segment(planks, rng, well_w + 2 * OVER, int(THICK * rng.uniform(0.9, 1.1)))
	left = plank_segment(planks, rng, well_h + 2 * OVER, int(THICK * rng.uniform(0.9, 1.1)))
	right = plank_segment(planks, rng, well_h + 2 * OVER, int(THICK * rng.uniform(0.9, 1.1)))
	left = left.transpose(Image.ROTATE_90)
	right = right.transpose(Image.ROTATE_90)

	lay(out, shadow, top, cx, t)
	lay(out, shadow, bot, cx, b)
	lay(out, shadow, left, l, cy)
	lay(out, shadow, right, r, cy)

	# corner scraps / crossed boards, same sheet the frame uses
	order = list(range(len(scraps)))
	rng.shuffle(order)
	for i, (px, py) in enumerate(((l, t), (r, t), (l, b), (r, b))):
		scrap = scraps[order[i % len(order)]]
		if rng.random() < 0.5:
			scrap = scrap.transpose(Image.FLIP_LEFT_RIGHT)
		f = rng.uniform(72, 96) / scrap.width
		scrap = scrap.resize((int(scrap.width * f), int(scrap.height * f)), Image.LANCZOS)
		scrap = scrap.rotate(rng.uniform(-18, 18), expand=True, resample=Image.BICUBIC)
		lay(out, shadow, scrap, px + rng.uniform(-4, 4), py + rng.uniform(-4, 4))

	framed = Image.alpha_composite(shadow, out)

	# dark well so gold text doesn't sit on the sky. Punch it into the open
	# centre AFTER the boards, so planks still overlap the well lip.
	well = Image.new("RGBA", (W, H), (0, 0, 0, 0))
	wd = ImageDraw.Draw(well)
	pad = 10
	wd.rounded_rectangle(
		[l + pad, t + pad, r - pad, b - pad],
		radius=8,
		fill=(12, 10, 8, 255),
	)
	wd.rounded_rectangle(
		[l + pad + 2, t + pad + 2, r - pad - 2, b - pad - 2],
		radius=6,
		outline=(0, 0, 0, 200),
		width=2,
	)
	framed = Image.alpha_composite(framed, well)

	opening = {
		"x0": round((l + pad) / W, 4),
		"x1": round((r - pad) / W, 4),
		"y0": round((t + pad) / H, 4),
		"y1": round((b - pad) / H, 4),
	}

	for base in ("assets-src", os.path.join("static", "assets")):
		path = os.path.join(APP, base, REL)
		os.makedirs(os.path.dirname(path), exist_ok=True)
		framed.save(path, optimize=True)
		print(f"wrote {path} {framed.size} opening={opening} aspect={W / H:.3f}")


if __name__ == "__main__":
	main()
