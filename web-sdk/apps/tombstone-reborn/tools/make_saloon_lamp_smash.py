"""Unlit copy of saloon_lamp_l.png. Same lantern, no flame, no halo, no crack.

Runtime only swaps this file in when the lamp is shot.

Run:  python tools/make_saloon_lamp_smash.py
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image

APP = Path(__file__).resolve().parents[1]
SRC = APP / "static" / "assets" / "sprites" / "scene" / "saloon_lamp_l.png"
DEST = APP / "static" / "assets" / "sprites" / "scene" / "saloon_lamp_l_smashed.png"

CX, CY = 469.0, 240.0
RX, RY = 50.0, 60.0


def ellipse_d(x: float, y: float) -> float:
	return math.hypot((x - CX) / RX, (y - CY) / RY)


def smooth(a: float, b: float, x: float) -> float:
	t = max(0.0, min(1.0, (x - a) / (b - a)))
	return t * t * (3.0 - 2.0 * t)


def main() -> None:
	img = Image.open(SRC).convert("RGBA")
	w, h = img.size
	px = img.load()
	out = Image.new("RGBA", (w, h))
	op = out.load()

	for y in range(h):
		for x in range(w):
			r, g, b, a = px[x, y]
			if a < 80:
				# baked cream wash — delete, do not dim
				continue
			d = ellipse_d(x, y)
			lum = (r + g + b) / 3.0
			if d <= 1.05 and lum > 40:
				kill = smooth(55, 160, lum)
				grey = int(lum * 0.22)
				t = kill
				r = int(r * (1.0 - t) + grey * t)
				g = int(g * (1.0 - t) + grey * t)
				b = int(b * (1.0 - t) + grey * t)
				r = int(r * (1.0 - 0.45 * kill))
				g = int(g * (1.0 - 0.48 * kill))
				b = int(b * (1.0 - 0.35 * kill))
			op[x, y] = (r, g, b, a)

	out.save(DEST)
	print(f"wrote {DEST}")


if __name__ == "__main__":
	main()
