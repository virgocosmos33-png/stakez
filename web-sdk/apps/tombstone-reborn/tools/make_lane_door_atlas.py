"""Bake the last-reel lane door flipbook from the saloon-door-swing pack.

Outputs (written to BOTH asset trees so neither drifts):
    assets/sprites/fx/lane_door.png + .json          (key `laneDoor`)
    static/assets/sprites/fx/lane_door.png + .json

Source
------
VFXPACKSHEETS/saloon-door-swing/parts/frame_01..16.png — the door.png swing,
hinge on the right. Each island is padded onto one shared canvas so the post
stays put as the leaf swings edge-on.
"""

from __future__ import annotations

import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(APP)))
SRC_DIR = os.path.join(REPO, "VFXPACKSHEETS", "saloon-door-swing", "parts")

OUT_DIRS = (
	os.path.join(APP, "assets", "sprites", "fx"),
	os.path.join(APP, "static", "assets", "sprites", "fx"),
	os.path.join(APP, "assets-src", "assets", "sprites", "fx"),
)

FRAME_COUNT = 16
COLS = 4
ALPHA_FLOOR = 8


def clear_transparent_rgb(image: Image.Image) -> Image.Image:
	pixels = image.load()
	for y in range(image.height):
		for x in range(image.width):
			if pixels[x, y][3] == 0:
				pixels[x, y] = (0, 0, 0, 0)
	return image


def load_frame(index: int) -> Image.Image:
	path = os.path.join(SRC_DIR, f"frame_{index:02d}.png")
	if not os.path.isfile(path):
		raise SystemExit(f"missing door frame: {path}")
	return Image.open(path).convert("RGBA")


def pad_hinge(frames: list[Image.Image]) -> list[Image.Image]:
	"""Align every crop to the bottom-right so the hinge post does not drift."""
	max_w = max(frame.width for frame in frames)
	max_h = max(frame.height for frame in frames)
	aligned = []
	for frame in frames:
		canvas = Image.new("RGBA", (max_w, max_h), (0, 0, 0, 0))
		x = max_w - frame.width
		y = max_h - frame.height
		canvas.paste(frame, (x, y), frame)
		aligned.append(clear_transparent_rgb(canvas))
	return aligned


def main() -> None:
	raw = [load_frame(i) for i in range(1, FRAME_COUNT + 1)]
	frames = pad_hinge(raw)
	tile_w, tile_h = frames[0].size
	rows = (FRAME_COUNT + COLS - 1) // COLS
	atlas = Image.new("RGBA", (tile_w * COLS, tile_h * rows), (0, 0, 0, 0))
	meta_frames = {}
	for index, frame in enumerate(frames):
		col = index % COLS
		row = index // COLS
		x = col * tile_w
		y = row * tile_h
		atlas.paste(frame, (x, y), frame)
		meta_frames[f"door_{index:02d}.png"] = {
			"frame": {"x": x, "y": y, "w": tile_w, "h": tile_h},
			"rotated": False,
			"trimmed": False,
			"spriteSourceSize": {"x": 0, "y": 0, "w": tile_w, "h": tile_h},
			"sourceSize": {"w": tile_w, "h": tile_h},
		}
		print(f"[lane-door] frame_{index + 1:02d} -> {tile_w}x{tile_h} @ {col},{row}")

	meta = {
		"frames": meta_frames,
		"meta": {
			"image": "lane_door.png",
			"format": "RGBA8888",
			"size": {"w": atlas.width, "h": atlas.height},
			"scale": "1",
			"source": "VFXPACKSHEETS/saloon-door-swing (door.png swing)",
		},
	}

	for out_dir in OUT_DIRS:
		os.makedirs(out_dir, exist_ok=True)
		png_path = os.path.join(out_dir, "lane_door.png")
		json_path = os.path.join(out_dir, "lane_door.json")
		atlas.save(png_path, optimize=True)
		with open(json_path, "w", encoding="utf-8") as handle:
			json.dump(meta, handle, indent=1)
		print(f"[lane-door] wrote {png_path} ({os.path.getsize(png_path):,} B)")


if __name__ == "__main__":
	main()
