"""Flatten western_scene2.psd to the live night plate.

Source of truth: Desktop/western_scene2.psd (copied into assets-raw/scene/).
Honors Photoshop visibility, and keeps the woody sign boards off
(signpost + word overlays), matching the layers turned off in the PSD.

Ships western_scene2.webp + .png into assets/ and static/.

Run: python tools/export_western_scene2.py
"""
from __future__ import annotations

import shutil
from pathlib import Path

from psd_tools import PSDImage

APP = Path(__file__).resolve().parents[1]
RAW = APP / "assets-raw" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
STATIC = APP / "static" / "assets" / "sprites" / "scene"
PSD_NAME = "western_scene2.psd"
# The four planks live on `signpost`. Word layers are already off in the PSD.
# Hanging lamps are Spine (tools/build_hanging_lamps.py) — keep them off the still.
HIDE_BOARDS = ("signpost", "postsign", "beware1", "beware2", "deadman", "tellnotales")
HIDE_LAMPS = ("left hanging lamp", "right hanging lamp", "right  hanging lamp")
HIDE_FOR_PLATE = HIDE_BOARDS + HIDE_LAMPS


def sync_from_desktop(dest: Path) -> Path:
	desk = Path.home() / "Desktop" / PSD_NAME
	if desk.is_file() and (not dest.is_file() or desk.stat().st_mtime > dest.stat().st_mtime):
		RAW.mkdir(parents=True, exist_ok=True)
		shutil.copy2(desk, dest)
		print(f"copied newer Desktop PSD -> {dest}")
	if not dest.is_file():
		raise SystemExit(f"missing {dest} and {desk}")
	return dest


def hide_boards(layers) -> None:
	want = {" ".join(n.lower().split()) for n in HIDE_FOR_PLATE}
	for layer in layers:
		if layer.name in HIDE_FOR_PLATE or " ".join(layer.name.lower().split()) in want:
			layer.visible = False
		if layer.is_group():
			hide_boards(list(layer))


def main() -> None:
	src = sync_from_desktop(RAW / PSD_NAME)
	psd = PSDImage.open(src)
	hide_boards(list(psd))
	img = psd.composite(force=False).convert("RGB")
	img.save(RAW / "western_scene2.png", "PNG")
	for dest in (VITE, STATIC):
		dest.mkdir(parents=True, exist_ok=True)
		img.save(dest / "western_scene2.webp", "WEBP", quality=90, method=6)
		img.save(dest / "western_scene2.png", "PNG")
	print(f"exported {img.size[0]}x{img.size[1]} from {src}")


if __name__ == "__main__":
	main()
