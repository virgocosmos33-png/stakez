"""Convert Scenario glass renders (on pure black) into translucent overlays.

Luminance becomes alpha. Prefers portable assets-raw paths under this app;
falls back only if SRC_DIR env is set.

Outputs single-cell observation panes (NOT full-board Madam Mirror sheets):
  glass_intact.png / glass_broken.png
  observation_pane_intact.png / observation_pane_cracked.png

Prefer: python tools/make_observation_panes.py (procedural + optional Scenario src).
"""

import os
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
APP = HERE.parent
OUT_DIR = APP / "static" / "assets" / "sprites" / "mirror"
SRC_DIR = Path(os.environ.get("GLASS_SRC_DIR", APP / "assets-raw" / "observation_panes"))

JOBS = {
	"intact_src.png": ("glass_intact.png", 1.35, 0.10),
	"cracked_src.png": ("glass_broken.png", 1.5, 0.06),
	# legacy names from older pipelines
	"glass_intact_src.png": ("glass_intact.png", 1.35, 0.10),
	"glass_broken_src.png": ("glass_broken.png", 1.5, 0.06),
}

SIZE = 512
OUT_DIR.mkdir(parents=True, exist_ok=True)

wrote = 0
for src_name, (out_name, alpha_gain, base_alpha) in JOBS.items():
	src_path = SRC_DIR / src_name
	if not src_path.is_file():
		continue
	im = Image.open(src_path).convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
	out = Image.new("RGBA", (SIZE, SIZE))
	src_px = im.load()
	out_px = out.load()
	for y in range(SIZE):
		for x in range(SIZE):
			r, g, b = src_px[x, y]
			lum = max(r, g, b)
			alpha = min(255, int(lum * alpha_gain + 255 * base_alpha))
			out_px[x, y] = (r, g, b, alpha)
	out.save(OUT_DIR / out_name)
	# also write observation_pane_* aliases
	alias = (
		"observation_pane_intact.png"
		if "intact" in out_name
		else "observation_pane_cracked.png"
	)
	out.save(OUT_DIR / alias)
	print(f"{src_name} -> {out_name} + {alias}")
	wrote += 1

if wrote == 0:
	print(f"No Scenario sources in {SRC_DIR}; run make_observation_panes.py instead.")
