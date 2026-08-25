"""Extract visible western_scene2.psd layers as isolated PNGs for Crystal Rescale."""
from __future__ import annotations

import json
from pathlib import Path

from psd_tools import PSDImage

from export_western_scene2 import PSD_NAME, RAW, sync_from_desktop

OUT = RAW / "crystal_src"
SKIP = {
    "layer 1",
    "board",
    "layer 2",
    "layer 2 copy",
    "chain_02",
    "chain_02 copy",
    "postsign",
    "tellnotales",
    "deadman",
    "beware1",
    "beware2",
}


def norm(name: str) -> str:
	return " ".join(name.lower().split())


def main() -> None:
	src = sync_from_desktop(RAW / PSD_NAME)
	psd = PSDImage.open(src)
	OUT.mkdir(parents=True, exist_ok=True)
	manifest = []
	used: dict[str, int] = {}

	def walk(layers, parent=""):
		for layer in layers:
			key = norm(layer.name)
			if layer.is_group():
				if key in SKIP or not layer.visible:
					continue
				walk(list(layer), key)
				continue
			if key in SKIP or not layer.visible:
				continue
			if layer.bbox is None or layer.width <= 1 or layer.height <= 1:
				continue
			img = layer.composite()
			if img is None:
				continue
			img = img.convert("RGBA")
			n = used.get(key, 0) + 1
			used[key] = n
			slug = key.replace(" ", "_")
			if n > 1:
				slug = f"{slug}_{n}"
			path = OUT / f"{slug}.png"
			img.save(path, "PNG")
			manifest.append(
				{
					"name": layer.name,
					"slug": slug,
					"path": str(path),
					"bbox": list(layer.bbox),
					"size": [img.width, img.height],
					"parent": parent,
				}
			)
			print(f"{slug:28s} {img.width:4d}x{img.height:<4d} bbox={layer.bbox}")

	walk(list(psd))
	(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
	print(f"extracted {len(manifest)} layers -> {OUT}")


if __name__ == "__main__":
	main()
