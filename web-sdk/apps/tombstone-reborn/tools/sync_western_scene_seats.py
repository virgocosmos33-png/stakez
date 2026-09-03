"""Seat the live room from assets/spines/western_scene.

The user moves props in that Spine folder. Overlays (lamps, plaques, board,
barrel glow, clouds) must follow those bones — not the old PSD placement.json.
Does not re-pack from backgroundSPINE. Does not invent seats.

Run: python tools/sync_western_scene_seats.py
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
SRC = APP / "assets" / "spines" / "western_scene"
SRC_JSON = SRC / "western_scene.json"
STATIC = APP / "static" / "assets" / "spines" / "western_scene"
SCALE = 2

# Overlay copies of Spine slots (hidden on the skeleton). Unions = one PSD island.
BOARD_CHAINS = (
	("hang-0", ("Layer_8_copy_11", "Layer_8")),
	("hang-1", ("Layer_8_copy",)),
	("hang-2", ("Layer_8_copy_2",)),
)
PLAQUES = {
	"ways": {
		"box": "Layer_4",
		"pallet": "Layer_5",
		"chains": (
			("ways-0", "plaqueChainWays0", ("Layer_8_copy_5",)),
			("ways-1", "plaqueChainWays1", ("Layer_8_copy_5_02",)),
			("ways-2", "plaqueChainWays2", ("Layer_8_copy_9", "Layer_8_copy_10")),
			("ways-3", "plaqueChainWays3", ("Layer_8_copy_6",)),
		),
	},
	"multi": {
		"box": "Layer_4_copy",
		"pallet": "Layer_6",
		"chains": (
			("multi-0", "plaqueChainMulti0", ("Layer_8_copy_3",)),
			("multi-1", "plaqueChainMulti1", ("Layer_8_copy_4",)),
		),
	},
	"win": {
		"box": "Layer_4_copy_2",
		"pallet": "Layer_7",
		"chains": (
			("win-0", "plaqueChainWin0", ("Layer_8_copy_7",)),
			("win-1", "plaqueChainWin1", ("Layer_8_copy_8",)),
		),
	},
	"spins": {
		"box": "Layer_4_copy_2_02",
		"pallet": "Layer_9",
		"chains": (
			("spins-0", "plaqueChainSpins0", ("Layer_8_copy_7_02",)),
			("spins-1", "plaqueChainSpins1", ("Layer_8_copy_8_02", "Layer_8_copy_12")),
		),
	},
}


def bone_world(bones: dict, name: str) -> tuple[float, float]:
	x = y = 0.0
	cur = name
	guard = 0
	while cur and guard < 64:
		b = bones[cur]
		x += float(b.get("x", 0))
		y += float(b.get("y", 0))
		cur = b.get("parent")
		guard += 1
	return x, y


def box_for(bones: dict, slots: list, skins: dict, slot_name: str) -> dict:
	slot = next(s for s in slots if s["name"] == slot_name)
	bone = bones[slot["bone"]]
	wx, wy = bone_world(bones, bone["name"])
	att_name = slot.get("attachment") or slot_name
	att = ((skins.get(slot_name) or {}).get(att_name)) or {}
	return _box(wx, wy, att)


def _box(wx: float, wy: float, att: dict) -> dict:
	ax = float(att.get("x", 0))
	ay = float(att.get("y", 0))
	w = float(att.get("width", 0))
	h = float(att.get("height", 0))
	cx = wx + ax
	cy = wy + ay
	return {
		"cx": cx,
		"cy": cy,
		"w": w,
		"h": h,
		"left": cx - w / 2,
		"right": cx + w / 2,
		"bottom": cy - h / 2,
		"top": cy + h / 2,
	}


def to_scene(box: dict, canvas_h: float) -> dict:
	left = box["left"] * SCALE
	right = box["right"] * SCALE
	top = (canvas_h - box["top"]) * SCALE
	bottom = (canvas_h - box["bottom"]) * SCALE
	return {
		"left": round(left, 1),
		"top": round(top, 1),
		"right": round(right, 1),
		"bottom": round(bottom, 1),
	}


def union_scene(boxes: list[dict]) -> dict:
	return {
		"left": min(b["left"] for b in boxes),
		"top": min(b["top"] for b in boxes),
		"right": max(b["right"] for b in boxes),
		"bottom": max(b["bottom"] for b in boxes),
	}


def ts_num(v: float) -> str:
	n = round(float(v), 1)
	return str(int(n)) if abs(n - int(n)) < 0.05 else str(n)


def ts_rect(r: dict) -> str:
	return (
		"{ "
		f"left: {ts_num(r['left'])}, top: {ts_num(r['top'])}, "
		f"right: {ts_num(r['right'])}, bottom: {ts_num(r['bottom'])}"
		" }"
	)


def well_from(box: dict, pallet: dict) -> dict:
	"""Inner U under the pallet — same fractions as hudPlaqueSeats BASE_POCKET."""
	bw = box["right"] - box["left"]
	bh = box["bottom"] - box["top"]
	left = box["left"] + bw * 0.255
	right = box["left"] + bw * 0.708
	bottom = box["top"] + bh * 0.6
	top = min(bottom - 8, max(pallet["bottom"] + 2, box["top"]))
	return {
		"left": round(left, 1),
		"top": round(top, 1),
		"right": round(right, 1),
		"bottom": round(bottom, 1),
	}


SNAP_PX = 4.0


def close_rect(a: dict, b: dict) -> bool:
	return max(abs(a[k] - b[k]) for k in ("left", "top", "right", "bottom")) <= SNAP_PX


def prefer(old: dict | None, new: dict) -> dict:
	"""Keep the cut-sprite seat when Spine is only rounding-off the PSD island."""
	if old and close_rect(old, new):
		return old
	return new


def shift_rect(r: dict, dx: float, dy: float) -> dict:
	return {
		"left": round(r["left"] + dx, 1),
		"top": round(r["top"] + dy, 1),
		"right": round(r["right"] + dx, 1),
		"bottom": round(r["bottom"] + dy, 1),
	}


def load_old_seats() -> dict | None:
	path = APP / "src" / "game" / "frameSeats.generated.ts"
	text = path.read_text(encoding="utf-8")
	# Pull the previous board/pocket so a still frame keeps the authored hole.
	import re

	def grab(name: str) -> dict | None:
		m = re.search(
			rf"{name}: \{{ left: ([-\d.]+), top: ([-\d.]+), right: ([-\d.]+), bottom: ([-\d.]+) \}}",
			text,
		)
		if not m:
			return None
		return {
			"left": float(m.group(1)),
			"top": float(m.group(2)),
			"right": float(m.group(3)),
			"bottom": float(m.group(4)),
		}

	holes = re.findall(
		r"\{ id: '([^']+)', rows: (\d+), left: ([-\d.]+), top: ([-\d.]+), "
		r"right: ([-\d.]+), bottom: ([-\d.]+) \}",
		text,
	)
	# Named chain / hang rects, plus plaque box/pallet/well in slug order.
	named = {}
	for m in re.finditer(
		r'id: "([^"]+)", (?:key: "[^"]+", )?left: ([-\d.]+), top: ([-\d.]+), '
		r"right: ([-\d.]+), bottom: ([-\d.]+)",
		text,
	):
		named[m.group(1)] = {
			"left": float(m.group(2)),
			"top": float(m.group(3)),
			"right": float(m.group(4)),
			"bottom": float(m.group(5)),
		}
	kind_rects = []
	for m in re.finditer(
		r"(box|pallet|well): \{ left: ([-\d.]+), top: ([-\d.]+), "
		r"right: ([-\d.]+), bottom: ([-\d.]+) \}",
		text,
	):
		kind_rects.append(
			(
				m.group(1),
				{
					"left": float(m.group(2)),
					"top": float(m.group(3)),
					"right": float(m.group(4)),
					"bottom": float(m.group(5)),
				},
			)
		)
	old_plaques = {}
	order = ("ways", "multi", "win", "spins")
	idx = 0
	for slug in order:
		chunk = {}
		while idx < len(kind_rects) and kind_rects[idx][0] in chunk:
			idx += 1
		for _ in range(3):
			if idx >= len(kind_rects):
				break
			kind, rect = kind_rects[idx]
			chunk[kind] = rect
			idx += 1
		if chunk:
			old_plaques[slug] = chunk
	return {
		"board": grab("board"),
		"pocket": grab("pocket"),
		"named": named,
		"plaques": old_plaques,
		"holes": [
			{
				"id": hid,
				"rows": int(rows),
				"left": float(l),
				"top": float(t),
				"right": float(r),
				"bottom": float(b),
			}
			for hid, rows, l, t, r, b in holes
		],
	}


def main() -> None:
	if not SRC_JSON.exists():
		raise SystemExit(f"missing {SRC_JSON}")
	data = json.loads(SRC_JSON.read_text(encoding="utf-8"))
	skel = data["skeleton"]
	canvas_w = float(skel["width"])
	canvas_h = float(skel["height"])
	bones = {b["name"]: b for b in data["bones"]}
	slots = data["slots"]
	skins = next(s["attachments"] for s in data["skins"] if s.get("name") == "default")

	def scene_slot(name: str) -> dict:
		return to_scene(box_for(bones, slots, skins, name), canvas_h)

	board = scene_slot("MAIN_FRAME")
	beam = scene_slot("beam")
	old = load_old_seats()
	dx = dy = 0.0
	if old and old["board"]:
		dx = board["left"] - old["board"]["left"]
		dy = board["top"] - old["board"]["top"]
	if old and old["pocket"] and (abs(dx) > 0.05 or abs(dy) > 0.05):
		pocket = shift_rect(old["pocket"], dx, dy)
		holes = [
			{**h, **shift_rect(h, dx, dy), "id": h["id"], "rows": h["rows"]}
			for h in old["holes"]
		]
	elif old and old["pocket"]:
		pocket = old["pocket"]
		holes = old["holes"]
	else:
		# Fallback inset if seats were never generated.
		pocket = {
			"left": board["left"] + 130,
			"top": board["top"] + 102,
			"right": board["right"] - 104,
			"bottom": board["bottom"] - 104,
		}
		holes = []

	lamp_l_bone = bone_world(bones, "left_hanging_lamp")
	lamp_r_bone = bone_world(bones, "right_hanging_lamp")
	lamp_l_box = scene_slot("left_hanging_lamp")
	lamp_r_box = scene_slot("right_hanging_lamp")
	hang_l = {
		"x": round(lamp_l_bone[0] * SCALE, 1),
		"y": round((canvas_h - lamp_l_bone[1]) * SCALE, 1),
	}
	hang_r = {
		"x": round(lamp_r_bone[0] * SCALE, 1),
		"y": round((canvas_h - lamp_r_bone[1]) * SCALE, 1),
	}

	glow = box_for(bones, slots, skins, "lantern_dim_light")
	barrel_glow = {
		"x": round(glow["cx"] * SCALE, 2),
		"y": round((canvas_h - glow["cy"]) * SCALE, 2),
		"w": round(glow["w"] * SCALE, 2),
		"h": round(glow["h"] * SCALE, 2),
	}
	cloud_att = ((skins.get("background_clouds") or {}).get("background_clouds")) or {}
	cloud_home = float(cloud_att.get("x", 592.5))

	old_named = (old or {}).get("named") or {}
	old_plaques = (old or {}).get("plaques") or {}

	chains = []
	for hid, names in BOARD_CHAINS:
		boxes = [scene_slot(n) for n in names]
		u = prefer(old_named.get(hid), union_scene(boxes))
		chains.append({"id": hid, **u})

	plaque_blocks = []
	for slug, spec in PLAQUES.items():
		prev = old_plaques.get(slug) or {}
		box = prefer(prev.get("box"), scene_slot(spec["box"]))
		pallet = prefer(prev.get("pallet"), scene_slot(spec["pallet"]))
		well = prev.get("well") or well_from(box, pallet)
		chain_lines = []
		for cid, key, names in spec["chains"]:
			u = prefer(old_named.get(cid), union_scene([scene_slot(n) for n in names]))
			chain_lines.append(
				f'{{ id: "{cid}", key: "{key}", '
				f"left: {ts_num(u['left'])}, top: {ts_num(u['top'])}, "
				f"right: {ts_num(u['right'])}, bottom: {ts_num(u['bottom'])} }}"
			)
		plaque_blocks.append(
			f"\t\t{slug}: {{\n"
			f"\t\t\tbox: {ts_rect(box)},\n"
			f"\t\t\tpallet: {ts_rect(pallet)},\n"
			f"\t\t\twell: {ts_rect(well)},\n"
			f"\t\t\tchains: [\n\t\t\t\t"
			+ ",\n\t\t\t\t".join(chain_lines)
			+ ",\n\t\t\t],\n"
			f"\t\t}},"
		)

	hole_ts = ",\n\t\t".join(
		f"{{ id: '{h['id']}', rows: {h['rows']}, "
		f"left: {h['left']}, top: {h['top']}, right: {h['right']}, bottom: {h['bottom']} }}"
		for h in holes
	)
	chain_ts = ",\n\t\t".join(
		f'{{ id: "{c["id"]}", left: {c["left"]}, top: {c["top"]}, '
		f'right: {c["right"]}, bottom: {c["bottom"]} }}'
		for c in chains
	)

	seats = f'''/**
 * Scene-space seats from assets/spines/western_scene (Spine setup pose).
 * Canvas {int(canvas_w)}×{int(canvas_h)} (1×), scaled ×{SCALE} into SCENE_ART.
 * Plaques / lamps / board follow the skeleton the user edited. Do not use placement.json.
 */
export const FRAME_SEATS = {{
	source: {json.dumps(str(SRC))},
	psd: {{ width: {int(canvas_w)}, height: {int(canvas_h)} }},
	scale: {SCALE},
	board: {ts_rect(board)},
	/** Interior hole of MAIN_FRAME at 2×. Tracks the board if that bone moved. */
	pocket: {ts_rect(pocket)},
	/** Stepped hole bands in SCENE_ART (one connected island, not 6 separate windows). */
	holeColumns: [
		{hole_ts}
	],
	beam: {ts_rect(beam)},
	chains: [
		{chain_ts}
	],
	lamps: {{
		L: {{
			hangX: {hang_l["x"]},
			hangY: {hang_l["y"]},
			left: {lamp_l_box["left"]},
			top: {lamp_l_box["top"]},
			right: {lamp_l_box["right"]},
			bottom: {lamp_l_box["bottom"]},
		}},
		R: {{
			hangX: {hang_r["x"]},
			hangY: {hang_r["y"]},
			left: {lamp_r_box["left"]},
			top: {lamp_r_box["top"]},
			right: {lamp_r_box["right"]},
			bottom: {lamp_r_box["bottom"]},
		}},
	}},
	plaques: {{
{chr(10).join(plaque_blocks)}
	}},
}} as const;
'''
	seats_path = APP / "src" / "game" / "frameSeats.generated.ts"
	seats_path.write_text(seats.replace("\t", "\t"), encoding="utf-8")

	lamps_ts = f'''/** Hang pivots in SCENE_ART pixels (top of each chain). From western_scene bones. */
export const HANGING_LAMPS = {{
  "period": 2.4683,
  "L": {{
    "x": {hang_l["x"]},
    "y": {hang_l["y"]}
  }},
  "R": {{
    "x": {hang_r["x"]},
    "y": {hang_r["y"]}
  }}
}} as const;
'''
	lamps_path = APP / "src" / "game" / "hangingLamps.generated.ts"
	lamps_path.write_text(lamps_ts, encoding="utf-8")

	scene_seats = f'''/** Live overlay seats from assets/spines/western_scene. Regenerated by tools/sync_western_scene_seats.py. */
export const WESTERN_SCENE_SEATS = {{
	cloudHomeX: {cloud_home},
	barrelGlow: {{
		x: {barrel_glow["x"]},
		y: {barrel_glow["y"]},
		w: {barrel_glow["w"]},
		h: {barrel_glow["h"]},
	}},
}} as const;
'''
	scene_path = APP / "src" / "game" / "westernSceneSeats.generated.ts"
	scene_path.write_text(scene_seats, encoding="utf-8")

	STATIC.mkdir(parents=True, exist_ok=True)
	copied = 0
	for src in SRC.rglob("*"):
		if not src.is_file():
			continue
		rel = src.relative_to(SRC)
		dest = STATIC / rel
		dest.parent.mkdir(parents=True, exist_ok=True)
		if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime and dest.stat().st_size == src.stat().st_size:
			continue
		shutil.copy2(src, dest)
		copied += 1

	moved = []
	if old and old["board"]:
		if abs(dx) > 0.05 or abs(dy) > 0.05:
			moved.append(f"MAIN_FRAME {dx:+.1f},{dy:+.1f}")
	props = ("barrel", "skull", "post_L", "post_R", "grass_02", "rocks_02", "lantern_dim")
	prop_report = []
	for name in props:
		if name not in bones:
			continue
		wx, wy = bone_world(bones, name)
		box = scene_slot(name)
		prop_report.append(
			f"  {name:12} bone=({wx:.1f},{wy:.1f}) scene=({box['left']:.0f},{box['top']:.0f})-({box['right']:.0f},{box['bottom']:.0f})"
		)

	print(f"ok seats from {SRC}")
	print(f"  board {board}")
	print(f"  pocket {pocket}")
	print(f"  lamps L hang {hang_l}  R hang {hang_r}")
	print(f"  barrel glow {barrel_glow}")
	print(f"  cloud homeX {cloud_home}")
	print(f"  static copied {copied} files")
	if moved:
		print("  moved:", ", ".join(moved))
	print("  props:")
	print("\n".join(prop_report))


if __name__ == "__main__":
	main()
