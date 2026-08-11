"""Bake the nudge rider's furniture: its card frame and the multiplier plaque.

Both replace procedural Graphics stand-ins. The rider used to be a bare symbol
inside a flat amber `roundRect` stroke with a second stroked box under it for
the multiplier — which is exactly the "empty outlined cell" the event was
reported for. The plaque is shared with StretchWays so the bounty and nudge
payoff badges are one piece of art rather than two hand-rolled boxes.

Sources are Layer AI generations (workspace "Back's Workspace", session
"Tombstone Reborn - nudge UI"), generated against a pure black void so the key
unmixes exactly. Nothing here is generated in Scenario.

The frame's open centre is part of the point: it is black in the source, so it
keys to fully transparent and the symbol reads through it.

Outputs
  static/assets/sprites/fx/fx_rider_frame.png
  static/assets/sprites/fx/fx_mult_plaque.png

Run:  python tools/make_nudge_ui.py
"""

from __future__ import annotations

import os

import numpy as np
from PIL import Image

from alpha_key import alpha_crop, bleed_alpha, fit_longest, key_black, lift_exposure

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
RAW = os.path.join(APP, "assets-raw", "layer_nudge")
OUT = os.path.join(APP, "static", "assets", "sprites", "fx")

# The board is near-black and both plates are lit for a black void, so they
# need a modest lift to sit above the cards rather than merge into them. The
# key runs low, because the iron's shadow side is genuinely dark and clipping
# it eats the frame's outer edge.
JOBS = [
	dict(src="frame_c.png", out="fx_rider_frame", longest=768, low=0.03, high=0.11, gain=1.35),
	dict(src="plaque_b.png", out="fx_mult_plaque", longest=512, low=0.03, high=0.11, gain=1.45),
]


def main() -> None:
	os.makedirs(OUT, exist_ok=True)
	for job in JOBS:
		path = os.path.join(RAW, job["src"])
		if not os.path.isfile(path):
			raise SystemExit(f"missing Layer AI source: {path}")
		keyed = key_black(Image.open(path), job["low"], job["high"])
		art = fit_longest(alpha_crop(bleed_alpha(lift_exposure(keyed, job["gain"]))), job["longest"])
		art.save(os.path.join(OUT, f"{job['out']}.png"), optimize=True)
		alpha = np.array(art)[..., 3]
		print(
			f"[nudge-ui] {job['out']} {art.width}x{art.height}"
			f" coverage {alpha.mean() / 255:.2f} <- layer_nudge/{job['src']}"
		)


if __name__ == "__main__":
	main()
