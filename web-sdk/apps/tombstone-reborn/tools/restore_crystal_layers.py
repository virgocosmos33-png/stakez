"""Fit Crystal RGB to exact 2x and restore the original LANCZOS alpha."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image

from export_western_scene2 import RAW

SRC = RAW / "crystal_src"
CRYSTAL = RAW / "crystal_out"
READY = RAW / "crystal_ready"
SCALE = 2


def restore(orig: Image.Image, crystal: Image.Image, tw: int, th: int) -> Image.Image:
	rgb = crystal.convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
	alpha = orig.convert("RGBA").split()[-1].resize((tw, th), Image.Resampling.LANCZOS)
	arr = np.dstack([np.asarray(rgb), np.asarray(alpha)])
	arr[arr[:, :, 3] == 0, :3] = 0
	return Image.fromarray(arr, "RGBA")


def main() -> None:
	manifest = json.loads((SRC / "manifest.json").read_text(encoding="utf-8"))
	READY.mkdir(parents=True, exist_ok=True)
	done = 0
	missing = []
	for item in manifest:
		slug = item["slug"]
		src_path = SRC / f"{slug}.png"
		cry_path = CRYSTAL / f"{slug}.png"
		if slug in ("left_hanging_lamp", "right_hanging_lamp") and not cry_path.is_file():
			shared = CRYSTAL / "hanging_lamp.png"
			if shared.is_file():
				cry_path = shared
		ow, oh = item["size"]
		tw, th = ow * SCALE, oh * SCALE
		if not cry_path.is_file():
			missing.append(slug)
			src_im = Image.open(src_path)
			out = restore(src_im, src_im, tw, th)
			print(f"{slug:24s} LANCZOS fallback {ow}x{oh} -> {tw}x{th}")
		else:
			out = restore(Image.open(src_path), Image.open(cry_path), tw, th)
			print(f"{slug:24s} {ow}x{oh} -> {tw}x{th}  from {tuple(Image.open(cry_path).size)}")
		dest = READY / f"{slug}.png"
		out.save(dest, "PNG")
		done += 1
	print(f"ready {done}  missing {missing}")


if __name__ == "__main__":
	main()
