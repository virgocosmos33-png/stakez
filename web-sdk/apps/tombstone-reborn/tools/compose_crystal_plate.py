"""Composite crystal_ready layers into the live 2x night plate."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from export_western_scene2 import HIDE_FOR_PLATE, RAW, STATIC, VITE

from restore_crystal_layers import READY, SCALE, SRC

CANVAS = (1342 * SCALE, 892 * SCALE)


def norm(name: str) -> str:
	return " ".join(name.lower().split())


def main() -> None:
	manifest = json.loads((SRC / "manifest.json").read_text(encoding="utf-8"))
	hide = {norm(n) for n in HIDE_FOR_PLATE}
	plate = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
	used = 0
	for item in manifest:
		if norm(item["name"]) in hide:
			continue
		path = READY / f"{item['slug']}.png"
		if not path.is_file():
			print(f"skip {item['slug']} (no ready png)")
			continue
		layer = Image.open(path).convert("RGBA")
		x0, y0, _, _ = item["bbox"]
		plate.alpha_composite(layer, (int(round(x0 * SCALE)), int(round(y0 * SCALE))))
		used += 1
	rgb = plate.convert("RGB")
	raw_png = RAW / "western_scene2.png"
	rgb.save(raw_png, "PNG")
	for dest in (VITE, STATIC):
		dest.mkdir(parents=True, exist_ok=True)
		rgb.save(dest / "western_scene2.webp", "WEBP", quality=92, method=6)
		rgb.save(dest / "western_scene2.png", "PNG")
	print(f"composited {used} layers -> {CANVAS[0]}x{CANVAS[1]}")


if __name__ == "__main__":
	main()
