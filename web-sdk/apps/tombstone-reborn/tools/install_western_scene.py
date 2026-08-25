"""Install the ready-made backgroundSPINE western scene as a Spine 4.1.23 pack.

Source: C:/Users/Emex33/Documents/fire frame vfx/backgroundSPINE/spine-scene
Runtime: spine-pixi-v8 (4.1). A 3.8 skeleton loads as a still pose.

Game chrome (MAIN_FRAME / plaques / hang chains) is stripped — BoardPlate
already draws those. Barrel glow is split onto `barrel_on` so base can
leave the lantern dark.

Run: python tools/install_western_scene.py
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image

APP = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Users\Emex33\Documents\fire frame vfx\backgroundSPINE\spine-scene")
SRC_JSON = SRC / "skeleton.json"
SRC_IMAGES = SRC / "images"
NAME = "western_scene"
SPINE_VERSION = "4.1.23"
PAD = 2
OUT_DIRS = (
	APP / "assets" / "spines" / NAME,
	APP / "static" / "assets" / "spines" / NAME,
)


def is_chrome(name: str) -> bool:
	return name == "MAIN_FRAME" or name.startswith("Layer_") or name.startswith("chain_bolt")


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


def kept_bones(data: dict, slot_bones: set[str]) -> list[dict]:
	by_name = {bone["name"]: bone for bone in data["bones"]}
	keep: set[str] = set(slot_bones)
	keep.add("root")
	changed = True
	while changed:
		changed = False
		for name in list(keep):
			parent = by_name.get(name, {}).get("parent")
			if parent and parent not in keep:
				keep.add(parent)
				changed = True
	return [bone for bone in data["bones"] if bone["name"] in keep]


def convert(src: dict) -> dict:
	data = json.loads(json.dumps(src))
	skel = data["skeleton"]
	skel["spine"] = SPINE_VERSION
	skel["images"] = "./"
	skel["hash"] = "western-scene"

	slots = [slot for slot in data["slots"] if not is_chrome(slot["name"])]
	data["slots"] = slots
	slot_bones = {slot["bone"] for slot in slots}
	data["bones"] = kept_bones(data, slot_bones)

	default = data["skins"]["default"]
	attachments = {name: att for name, att in default.items() if not is_chrome(name)}
	data["skins"] = [{"name": "default", "attachments": attachments}]

	convert_keys(data["animations"])
	idle = data["animations"].setdefault("idle", {})
	slot_anims = idle.get("slots") or {}
	barrel = slot_anims.pop("lantern_dim_light", None)
	idle["slots"] = {name: track for name, track in slot_anims.items() if not is_chrome(name)}
	idle["bones"] = {
		name: track for name, track in (idle.get("bones") or {}).items() if not is_chrome(name)
	}
	data["animations"]["barrel_on"] = {"slots": {"lantern_dim_light": barrel}} if barrel else {"slots": {}}

	for slot in data["slots"]:
		if slot["name"] == "lantern_dim_light":
			slot["color"] = "00000000"

	return data


def pack(names: list[str]) -> tuple[Image.Image, dict[str, tuple[int, int, int, int]]]:
	rects: list[tuple[str, int, int, Image.Image]] = []
	for name in names:
		path = SRC_IMAGES / f"{name}.png"
		if not path.exists():
			raise SystemExit(f"missing {path}")
		img = Image.open(path).convert("RGBA")
		rects.append((name, img.width, img.height, img))
	rects.sort(key=lambda item: (-item[2], -item[1]))

	page_w = 2048
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
	page_h = y + row_h + PAD
	if page_h > 4096:
		page_w = 4096
		x = PAD
		y = PAD
		row_h = 0
		placed = {}
		for name, w, h, _img in rects:
			if x + w + PAD > page_w:
				x = PAD
				y += row_h + PAD
				row_h = 0
			placed[name] = (x, y, w, h)
			x += w + PAD
			row_h = max(row_h, h)
		page_h = y + row_h + PAD

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
	for dest in OUT_DIRS:
		if dest.exists():
			shutil.rmtree(dest)
		dest.mkdir(parents=True, exist_ok=True)
		(dest / f"{NAME}.json").write_text(payload, encoding="utf-8")
		(dest / f"{NAME}.atlas").write_text(text, encoding="utf-8")
		atlas.save(dest / f"{NAME}.png", "PNG")


def main() -> None:
	if not SRC_JSON.exists():
		raise SystemExit(f"missing ready scene {SRC_JSON}")
	src = json.loads(SRC_JSON.read_text(encoding="utf-8"))
	data = convert(src)
	names = attachment_names(data)
	atlas, placed = pack(names)
	text = atlas_text(atlas.width, atlas.height, placed)
	write_out(data, atlas, text)
	print(f"ok {NAME} {atlas.size} attachments={len(names)}")
	print(f"  clips: {', '.join(data['animations'])}")
	print(f"  slots: {len(data['slots'])}  bones: {len(data['bones'])}")
	for dest in OUT_DIRS:
		print(f"  {dest}")


if __name__ == "__main__":
	main()
