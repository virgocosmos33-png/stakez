"""Install the full TR2 Spine Background scene (every attachment).

Source: https://github.com/brandnitions-dev/TR2-Spine-Background-scene
Local clone: <repo>/_tr2_spine_scene/spine-scene  (or fire-frame fallback)

Spine 3.8.75 -> 4.1.23. Idle stays idle. Barrel glow is `barrel_on`
so base can leave the lantern dark.

Run: python tools/install_western_scene.py
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image

APP = Path(__file__).resolve().parents[1]
REPO = APP.parents[2]
CLONE = REPO / "_tr2_spine_scene" / "spine-scene"
FALLBACK = Path(r"C:\Users\Emex33\Documents\fire frame vfx\backgroundSPINE\spine-scene")
SRC = CLONE if (CLONE / "skeleton.json").exists() else FALLBACK
SRC_JSON = SRC / "skeleton.json"
SRC_IMAGES = SRC / "images"
SRC_FX = SRC.parent / "fx"
NAME = "western_scene"
SPINE_VERSION = "4.1.23"
PAD = 2
OUT_DIRS = (
	APP / "assets" / "spines" / NAME,
	APP / "static" / "assets" / "spines" / NAME,
)
BG_OUT = (
	APP / "assets" / "sprites" / "scene" / "western_scene_ready_bg.png",
	APP / "static" / "assets" / "sprites" / "scene" / "western_scene_ready_bg.png",
)
FX_OUT = (
	APP / "assets" / "sprites" / "scene" / "western_scene_fx",
	APP / "static" / "assets" / "sprites" / "scene" / "western_scene_fx",
)


def convert_keys(node) -> None:
	if isinstance(node, list):
		for item in node:
			convert_keys(item)
		return
	if not isinstance(node, dict):
		return
	if "angle" in node and "value" not in node:
		node["value"] = node.pop("angle")
	for value in node.values():
		convert_keys(value)


def convert(src: dict) -> dict:
	data = json.loads(json.dumps(src))
	skel = data["skeleton"]
	skel["spine"] = SPINE_VERSION
	skel["images"] = "./"
	skel["hash"] = "western-scene-full"

	default = data["skins"]["default"]
	data["skins"] = [{"name": "default", "attachments": default}]

	convert_keys(data["animations"])
	idle = data["animations"].setdefault("idle", {})
	slot_anims = idle.setdefault("slots", {})
	barrel = slot_anims.pop("lantern_dim_light", None)
	data["animations"]["barrel_on"] = (
		{"slots": {"lantern_dim_light": barrel}} if barrel else {"slots": {}}
	)

	for slot in data["slots"]:
		if slot["name"] == "lantern_dim_light":
			slot["color"] = "00000000"

	return data


def pack(names: list[str]) -> tuple[Image.Image, dict[str, tuple[int, int, int, int]]]:
	rects: list[tuple[str, int, int, Image.Image]] = []
	missing: list[str] = []
	for name in names:
		path = SRC_IMAGES / f"{name}.png"
		if not path.exists():
			missing.append(name)
			continue
		img = Image.open(path).convert("RGBA")
		rects.append((name, img.width, img.height, img))
	if missing:
		raise SystemExit(f"missing images: {', '.join(missing)}")
	rects.sort(key=lambda item: (-item[2], -item[1]))

	def layout(page_w: int) -> tuple[dict[str, tuple[int, int, int, int]], int]:
		x = PAD
		y = PAD
		row_h = 0
		placed: dict[str, tuple[int, int, int, int]] = {}
		for name, w, h, _img in rects:
			if x + w + PAD > page_w:
				x = PAD
				y += row_h + PAD
				row_h = 0
			placed[name] = (x, y, w, h)
			x += w + PAD
			row_h = max(row_h, h)
		return placed, y + row_h + PAD

	page_w = 2048
	placed, page_h = layout(page_w)
	if page_h > 4096:
		page_w = 4096
		placed, page_h = layout(page_w)

	atlas = Image.new("RGBA", (page_w, page_h), (0, 0, 0, 0))
	by_name = {name: img for name, _w, _h, img in rects}
	for name, (px, py, w, h) in placed.items():
		atlas.paste(by_name[name], (px, py))
	return atlas, placed


def atlas_text(page_w: int, page_h: int, placed: dict[str, tuple[int, int, int, int]]) -> str:
	lines = [
		f"{NAME}.png",
		f"size:{page_w},{page_h}",
		"filter:Linear,Linear",
		"scale:1",
	]
	for name in sorted(placed):
		x, y, w, h = placed[name]
		lines.append(name)
		lines.append(f"bounds:{x},{y},{w},{h}")
	return "\n".join(lines) + "\n"


def attachment_names(data: dict) -> list[str]:
	names: set[str] = set()
	for skin in data["skins"]:
		for slot_atts in skin["attachments"].values():
			names.update(slot_atts.keys())
	return sorted(names)


def write_out(data: dict, atlas: Image.Image, text: str) -> None:
	payload = json.dumps(data, separators=(",", ":"))
	bg = SRC_IMAGES / "background.png"
	for dest in OUT_DIRS:
		if dest.exists():
			shutil.rmtree(dest)
		dest.mkdir(parents=True, exist_ok=True)
		(dest / f"{NAME}.json").write_text(payload, encoding="utf-8")
		(dest / f"{NAME}.atlas").write_text(text, encoding="utf-8")
		atlas.save(dest / f"{NAME}.png", "PNG")
		images_dir = dest / "images"
		images_dir.mkdir(exist_ok=True)
		for src in SRC_IMAGES.glob("*.png"):
			shutil.copy2(src, images_dir / src.name)
		if SRC_FX.exists():
			fx_dir = dest / "fx"
			fx_dir.mkdir(exist_ok=True)
			for src in SRC_FX.glob("*.png"):
				shutil.copy2(src, fx_dir / src.name)
		for extra in ("lamp_state.json", "placement.json", "sign_state.json"):
			src = SRC.parent / extra
			if src.exists():
				shutil.copy2(src, dest / extra)
	if bg.exists():
		for dest in BG_OUT:
			dest.parent.mkdir(parents=True, exist_ok=True)
			shutil.copy2(bg, dest)
	if SRC_FX.exists():
		for dest in FX_OUT:
			if dest.exists():
				shutil.rmtree(dest)
			dest.mkdir(parents=True, exist_ok=True)
			for src in SRC_FX.glob("*.png"):
				shutil.copy2(src, dest / src.name)


def main() -> None:
	if not SRC_JSON.exists():
		raise SystemExit(f"missing ready scene {SRC_JSON}")
	src = json.loads(SRC_JSON.read_text(encoding="utf-8"))
	data = convert(src)
	names = attachment_names(data)
	atlas, placed = pack(names)
	if set(placed) != set(names):
		raise SystemExit(f"pack missed {sorted(set(names) - set(placed))}")
	text = atlas_text(atlas.width, atlas.height, placed)
	write_out(data, atlas, text)
	print(f"ok {NAME} from {SRC}")
	print(f"  atlas {atlas.size} attachments={len(names)}")
	print(f"  clips: {', '.join(data['animations'])}")
	print(f"  slots: {len(data['slots'])}  bones: {len(data['bones'])}")
	for dest in OUT_DIRS:
		print(f"  {dest}")


if __name__ == "__main__":
	main()
