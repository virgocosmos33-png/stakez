"""Install the ready western Spine scene.

Source of truth:
  C:\\Users\\Emex33\\Documents\\fire frame vfx\\backgroundSPINE\\spine-scene

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
SRC = Path(r"C:\Users\Emex33\Documents\fire frame vfx\backgroundSPINE\spine-scene")
SRC_JSON = SRC / "skeleton.json"
SRC_IMAGES = SRC / "images"
SRC_FX = SRC / "fx" if (SRC / "fx").exists() else SRC.parent / "fx"
NAME = "western_scene"
SPINE_VERSION = "4.1.23"
PAD = 2
CANVAS_W = 1342
CANVAS_H = 892
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
BOARD_FRAME_OUT = (
	APP / "assets" / "sprites" / "board" / "board_frame.png",
	APP / "static" / "assets" / "sprites" / "board" / "board_frame.png",
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

	widest = max((w for _n, w, _h, _img in rects), default=1)
	page_w = 2048
	while page_w < widest + PAD * 2:
		page_w *= 2
	placed, page_h = layout(page_w)
	while page_h > 8192 and page_w < 8192:
		page_w *= 2
		placed, page_h = layout(page_w)
	if page_h > 8192:
		raise SystemExit(f"atlas too tall {page_w}x{page_h}")

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


def _composite_at(dst: Image.Image, src: Image.Image, x: int, y: int) -> None:
	dx, dy = x, y
	sx = sy = 0
	sw, sh = src.size
	if dx < 0:
		sx = -dx
		sw -= sx
		dx = 0
	if dy < 0:
		sy = -dy
		sh -= sy
		dy = 0
	if dx + sw > dst.width:
		sw = dst.width - dx
	if dy + sh > dst.height:
		sh = dst.height - dy
	if sw <= 0 or sh <= 0:
		return
	piece = src.crop((sx, sy, sx + sw, sy + sh))
	dst.alpha_composite(piece, (dx, dy))


def compose_plate(src: dict) -> Image.Image | None:
	"""Street only. No red_filter. Same draw order as the ready skeleton."""
	skins = src["skins"]
	default = skins["default"] if isinstance(skins, dict) else next(
		skin["attachments"] for skin in skins if skin.get("name") == "default"
	)
	bones = {bone["name"]: bone for bone in src["bones"]}
	out = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
	painted = 0
	for slot in src["slots"]:
		name = slot["name"]
		if name == "red_filter" or not name.startswith("background"):
			continue
		att_name = slot.get("attachment") or name
		att = (default.get(name) or {}).get(att_name)
		path = SRC_IMAGES / f"{att_name}.png"
		if not att or not path.exists():
			continue
		bone = bones[slot["bone"]]
		cx = float(bone.get("x", 0)) + float(att.get("x", 0))
		cy = float(bone.get("y", 0)) + float(att.get("y", 0))
		img = Image.open(path).convert("RGBA")
		w, h = img.size
		left = cx - w / 2
		bottom = cy - h / 2
		_composite_at(out, img, int(round(left)), int(round(CANVAS_H - bottom - h)))
		painted += 1
	legacy = SRC_IMAGES / "background.png"
	if painted == 0 and legacy.exists():
		return Image.open(legacy).convert("RGBA")
	return out if painted else None


def write_board_frame() -> None:
	"""BoardPlate ring = ready MAIN_FRAME, 2x. Spine slot stays hidden."""
	src = SRC_IMAGES / "MAIN_FRAME.png"
	if not src.exists():
		return
	im = Image.open(src).convert("RGBA")
	w, h = im.size
	rgb = im.convert("RGB").resize((w * 2, h * 2), Image.Resampling.LANCZOS)
	alpha = im.getchannel("A").resize((w * 2, h * 2), Image.Resampling.NEAREST)
	out = Image.merge("RGBA", (*rgb.split(), alpha))
	for dest in BOARD_FRAME_OUT:
		dest.parent.mkdir(parents=True, exist_ok=True)
		out.save(dest, "PNG")


def write_out(data: dict, atlas: Image.Image, text: str, plate: Image.Image | None) -> None:
	payload = json.dumps(data, separators=(",", ":"))
	for dest in OUT_DIRS:
		if dest.exists():
			shutil.rmtree(dest, ignore_errors=True)
		dest.mkdir(parents=True, exist_ok=True)
		(dest / f"{NAME}.json").write_text(payload, encoding="utf-8")
		(dest / f"{NAME}.atlas").write_text(text, encoding="utf-8")
		atlas.save(dest / f"{NAME}.png", "PNG")
		images_dir = dest / "images"
		images_dir.mkdir(exist_ok=True)
		keep = {src.name for src in SRC_IMAGES.glob("*.png")}
		for src in SRC_IMAGES.glob("*.png"):
			shutil.copy2(src, images_dir / src.name)
		for leftover in images_dir.glob("*.png"):
			if leftover.name not in keep:
				leftover.unlink()
		if SRC_FX.exists():
			fx_dir = dest / "fx"
			fx_dir.mkdir(exist_ok=True)
			for src in SRC_FX.glob("*.png"):
				shutil.copy2(src, fx_dir / src.name)
		for extra in ("lamp_state.json", "placement.json", "sign_state.json", "red_filter.json"):
			src = SRC.parent / extra
			if not src.exists():
				src = SRC / extra
			if src.exists():
				shutil.copy2(src, dest / extra)
	write_board_frame()
	if plate is not None:
		for dest in BG_OUT:
			dest.parent.mkdir(parents=True, exist_ok=True)
			plate.save(dest, "PNG")
	if SRC_FX.exists():
		for dest in FX_OUT:
			if dest.exists():
				shutil.rmtree(dest)
			dest.mkdir(parents=True, exist_ok=True)
			for src in SRC_FX.glob("*.png"):
				shutil.copy2(src, dest / src.name)
	red = SRC_IMAGES / "red_filter.png"
	if red.exists():
		for dest in FX_OUT:
			dest.mkdir(parents=True, exist_ok=True)
			shutil.copy2(red, dest / "red_filter.png")
		red_json = SRC.parent / "red_filter.json"
		if not red_json.exists():
			red_json = SRC / "red_filter.json"
		if red_json.exists():
			for dest in FX_OUT:
				shutil.copy2(red_json, dest / "red_filter.json")


def main() -> None:
	if not SRC_JSON.exists():
		raise SystemExit(f"missing ready scene {SRC_JSON}")
	src = json.loads(SRC_JSON.read_text(encoding="utf-8"))
	plate = compose_plate(src)
	data = convert(src)
	names = attachment_names(data)
	atlas, placed = pack(names)
	if set(placed) != set(names):
		raise SystemExit(f"pack missed {sorted(set(names) - set(placed))}")
	text = atlas_text(atlas.width, atlas.height, placed)
	write_out(data, atlas, text, plate)
	print(f"ok {NAME} from {SRC}")
	print(f"  atlas {atlas.size} attachments={len(names)}")
	print(f"  clips: {', '.join(data['animations'])}")
	print(f"  slots: {len(data['slots'])}  bones: {len(data['bones'])}")
	for dest in OUT_DIRS:
		print(f"  {dest}")


if __name__ == "__main__":
	main()
