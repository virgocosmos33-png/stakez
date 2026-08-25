"""Write a 2684x1784 layered PSD from crystal_ready PNGs."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image
from pytoshop import enums
from pytoshop.user.nested_layers import Image as PsdLayer
from pytoshop.user.nested_layers import nested_layers_to_psd

from export_western_scene2 import PSD_NAME, RAW
from restore_crystal_layers import READY, SCALE, SRC

CANVAS = (1342 * SCALE, 892 * SCALE)
DESK = Path.home() / "Desktop" / PSD_NAME


def channels_rgba(im: Image.Image) -> dict[int, np.ndarray]:
	arr = np.asarray(im.convert("RGBA"))
	return {0: arr[:, :, 0], 1: arr[:, :, 1], 2: arr[:, :, 2], -1: arr[:, :, 3]}


def main() -> None:
	manifest = json.loads((SRC / "manifest.json").read_text(encoding="utf-8"))
	layers = []
	for item in manifest:
		path = READY / f"{item['slug']}.png"
		if not path.is_file():
			print(f"skip {item['slug']}")
			continue
		im = Image.open(path)
		x0, y0, _, _ = item["bbox"]
		left = int(round(x0 * SCALE))
		top = int(round(y0 * SCALE))
		layers.append(
			PsdLayer(
				name=item["name"],
				visible=True,
				left=left,
				top=top,
				channels=channels_rgba(im),
			)
		)
		print(f"{item['slug']:24s} {left},{top}")
	psd = nested_layers_to_psd(
		layers,
		color_mode=enums.ColorMode.rgb,
		compression=enums.Compression.raw,
		size=(CANVAS[0], CANVAS[1]),
	)
	raw_psd = RAW / PSD_NAME
	with raw_psd.open("wb") as fh:
		psd.write(fh)
	if DESK.parent.is_dir():
		with DESK.open("wb") as fh:
			psd.write(fh)
	print(f"wrote {len(layers)} layers {CANVAS[0]}x{CANVAS[1]} -> {raw_psd}")


if __name__ == "__main__":
	main()
