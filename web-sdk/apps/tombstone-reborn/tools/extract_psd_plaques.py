"""Extract WAYS / MULTI / WIN / FREE SPINS plaque pixels from the Desktop PSD.

Same law as tools/extract_psd_frame_chrome.py:
- Does NOT import export_western_scene2.
- Does NOT write the user's PSD.
- Native layer pixels, then 2x LANCZOS RGB + nearest alpha.
- No color-key. No MinFilter erode.

Also re-reads MAIN FRAME, beam, hanging lamps (nails only — never flatten lamps),
and hang-chain layers so seats stay honest.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image
from psd_tools import PSDImage

DESKTOP = Path(r"C:\Users\Emex33\Desktop")
APP = Path(__file__).resolve().parents[1]
RAW = APP / "assets-raw" / "scene" / "psd_plaques"
SCALE = 2
ALPHA = 12


def newest_psd() -> Path:
	cands = list(DESKTOP.glob("western_scene2*.psd"))
	repo = APP / "assets-raw" / "scene" / "western_scene2.psd"
	if repo.exists():
		cands.append(repo)
	if not cands:
		raise SystemExit("no western_scene2*.psd")
	return max(cands, key=lambda p: p.stat().st_mtime)


def walk(layers, parent=""):
	for layer in layers:
		name = layer.name
		key = " ".join(name.lower().split())
		if layer.is_group():
			yield from walk(list(layer), key)
			continue
		yield layer, key, parent


def up2(img: Image.Image) -> Image.Image:
	rgba = img.convert("RGBA")
	w, h = rgba.size
	rgb = rgba.convert("RGB").resize((w * SCALE, h * SCALE), Image.Resampling.LANCZOS)
	a = rgba.getchannel("A").resize((w * SCALE, h * SCALE), Image.Resampling.NEAREST)
	return Image.merge("RGBA", (*rgb.split(), a))


def sha1(path: Path) -> str:
	h = hashlib.sha1()
	h.update(path.read_bytes())
	return h.hexdigest()[:12]


def bbox_of(layer) -> tuple[int, int, int, int] | None:
	box = layer.bbox
	if box is None:
		return None
	l, t, r, b = (int(box[0]), int(box[1]), int(box[2]), int(box[3]))
	if r - l <= 1 or b - t <= 1:
		return None
	return (l, t, r, b)


def composite(layer) -> Image.Image | None:
	comp = layer.composite()
	if comp is None:
		return None
	return comp.convert("RGBA")


def inner_pocket(img: Image.Image, bbox1: tuple[int, int, int, int]):
	from collections import deque

	a = np.array(img.convert("RGBA"))[:, :, 3]
	h, w = a.shape
	hole = a <= ALPHA
	ext = np.zeros((h, w), dtype=np.bool_)
	q = deque()
	for x in range(w):
		if hole[0, x]:
			ext[0, x] = True
			q.append((0, x))
		if hole[h - 1, x]:
			ext[h - 1, x] = True
			q.append((h - 1, x))
	for y in range(h):
		if hole[y, 0]:
			ext[y, 0] = True
			q.append((y, 0))
		if hole[y, w - 1]:
			ext[y, w - 1] = True
			q.append((y, w - 1))
	while q:
		cy, cx = q.popleft()
		for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
			if ny < 0 or nx < 0 or ny >= h or nx >= w:
				continue
			if ext[ny, nx] or not hole[ny, nx]:
				continue
			ext[ny, nx] = True
			q.append((ny, nx))
	interior = hole & ~ext
	if interior.any():
		ys, xs = np.where(interior)
		x0, x1 = int(xs.min()), int(xs.max()) + 1
		y0, y1 = int(ys.min()), int(ys.max()) + 1
		kind = "transparent-hole"
	else:
		# U-frame: open top connects the interior to the edge, so flood-fill
		# sees no hole. Walk the center column for the floor plank, then take
		# the median inner post edges on the open rows.
		opaque = a > ALPHA
		mid = w // 2
		open_x0: list[int] = []
		open_x1: list[int] = []
		open_y: list[int] = []
		floor_y: int | None = None
		for y in range(h):
			if opaque[y, mid]:
				if open_y and floor_y is None:
					floor_y = y
				continue
			li = mid
			while li > 0 and not opaque[y, li]:
				li -= 1
			ri = mid
			while ri < w - 1 and not opaque[y, ri]:
				ri += 1
			if opaque[y, li] and opaque[y, ri] and ri - li > w * 0.2:
				open_y.append(y)
				open_x0.append(li)
				open_x1.append(ri)
		if open_y and floor_y is not None:
			pad = max(2, int(round(w * 0.02)))
			x0 = int(np.median(open_x0)) + pad
			x1 = int(np.median(open_x1)) - pad
			y0 = open_y[0]
			y1 = max(y0 + 8, floor_y - pad)
			kind = "u-channel"
		else:
			pad_x = max(1, int(round(w * 0.12)))
			pad_y = max(1, int(round(h * 0.18)))
			x0, y0, x1, y1 = pad_x, pad_y, w - pad_x, h - pad_y
			kind = "no-hole-inset"
	return {
		"kind": kind,
		"local": [x0, y0, x1, y1],
		"bbox1": [bbox1[0] + x0, bbox1[1] + y0, bbox1[0] + x1, bbox1[1] + y1],
		"opaque_frac": float((a > ALPHA).mean()),
	}


def save_pair(img: Image.Image, stem: str) -> dict:
	native = RAW / f"{stem}_native.png"
	px2 = RAW / f"{stem}_2x.png"
	img.save(native, "PNG")
	up2(img).save(px2, "PNG")
	return {"native": str(native), "px2": str(px2), "size1": list(img.size)}


def install_base(src: Path, rels: list[Path]) -> list[str]:
	out = []
	for dest in rels:
		dest.parent.mkdir(parents=True, exist_ok=True)
		shutil.copy2(src, dest)
		out.append(str(dest))
	return out


def sprite_copies(name: str) -> list[Path]:
	return [
		APP / "assets" / "sprites" / "tombstone" / name,
		APP / "static" / "assets" / "sprites" / "tombstone" / name,
		APP / "assets-src" / "sprites" / "tombstone" / name,
		APP / "assets-src" / "assets" / "sprites" / "tombstone" / name,
	]


def board_copies(name: str) -> list[Path]:
	return [
		APP / "assets" / "sprites" / "board" / name,
		APP / "static" / "assets" / "sprites" / "board" / name,
		APP / "assets-src" / "sprites" / "board" / name,
		APP / "assets-src" / "assets" / "sprites" / "board" / name,
	]


def is_chain_strip(box: tuple[int, int, int, int], name: str) -> bool:
	"""Real hang chains are thin columns. Boxes/pallets are wide."""
	key = " ".join(name.lower().split())
	if "bolt" in key:
		return False
	w = box[2] - box[0]
	return w <= 24


def assign_chain(parent: str, box: tuple[int, int, int, int], name: str) -> str | None:
	if not is_chain_strip(box, name):
		return None
	l, t, r, b = box
	cx = (l + r) / 2
	cy = (t + b) / 2
	if parent == "win frame chains":
		return "win"
	if parent == "free spins frame":
		return "spins"
	if parent == "chains upframe":
		if cx < 734:
			return "board"
		if 734 <= cx < 880:
			return "win" if cy > 500 else "multi"
		if cx >= 880:
			if cy > 500:
				return "spins"
			if cy < 400:
				return "ways"
			return "spins"
	return None


def merge_columns(items: list[dict]) -> list[dict]:
	"""Same-x chain segments become one island — do not tile-stack two sprites."""
	if not items:
		return []
	ordered = sorted(items, key=lambda i: (i["bbox"][0], i["bbox"][1]))
	groups: list[list[dict]] = []
	for item in ordered:
		l, t, r, b = item["bbox"]
		placed = False
		for group in groups:
			gl, gt, gr, gb = group[0]["bbox"]
			for g in group[1:]:
				gl = min(gl, g["bbox"][0])
				gt = min(gt, g["bbox"][1])
				gr = max(gr, g["bbox"][2])
				gb = max(gb, g["bbox"][3])
			overlap = min(r, gr) - max(l, gl)
			if overlap >= 8 and (min(b, gb) - max(t, gt) >= -4):
				group.append(item)
				placed = True
				break
		if not placed:
			groups.append([item])
	merged = []
	for group in groups:
		if len(group) == 1:
			merged.append(group[0])
			continue
		l = min(g["bbox"][0] for g in group)
		t = min(g["bbox"][1] for g in group)
		r = max(g["bbox"][2] for g in group)
		b = max(g["bbox"][3] for g in group)
		canvas = Image.new("RGBA", (r - l, b - t), (0, 0, 0, 0))
		for g in group:
			gl, gt, gr, gb = g["bbox"]
			canvas.alpha_composite(g["img"], (gl - l, gt - t))
		merged.append({
			"who": group[0]["who"],
			"name": " + ".join(g["name"] for g in group),
			"parent": group[0]["parent"],
			"bbox": (l, t, r, b),
			"img": canvas,
		})
	return merged


def ts_rect(box2: list[int]) -> str:
	return f"{{ left: {box2[0]}, top: {box2[1]}, right: {box2[2]}, bottom: {box2[3]} }}"


def main() -> None:
	src = newest_psd()
	st = src.stat()
	print(f"PSD {src} mtime={st.st_mtime} bytes={st.st_size}")
	psd = PSDImage.open(src)
	print(f"canvas {psd.width}x{psd.height}")
	RAW.mkdir(parents=True, exist_ok=True)

	layers_found = []
	groups = {
		"ways frame": [],
		"multi frame": [],
		"win frame": [],
		"free spins frame": [],
	}
	chains: list[dict] = []
	bolts: list[dict] = []
	frame_img = None
	frame_bbox = None
	beam_bbox = None
	lamp_l = None
	lamp_r = None

	for layer, key, parent in walk(list(psd)):
		box = bbox_of(layer)
		rec = {
			"name": layer.name,
			"key": key,
			"parent": parent,
			"kind": "group" if layer.is_group() else "layer",
			"visible": bool(layer.visible),
			"bbox": list(box) if box else None,
		}
		layers_found.append(rec)
		if box is None:
			continue

		if key in ("main frame", "frame"):
			img = composite(layer)
			if img is not None:
				frame_img = img
				frame_bbox = box
				print(f"FRAME {layer.name!r} {img.size} bbox={box}")

		if key == "beam":
			beam_bbox = box
			print(f"BEAM bbox={box}")

		if key == "left hanging lamp":
			lamp_l = box
			print(f"LAMP L {layer.name!r} bbox={box} (nails only, not flattened)")
		if key == "right hanging lamp":
			lamp_r = box
			print(f"LAMP R {layer.name!r} bbox={box} (nails only, not flattened)")

		if parent in groups:
			img = composite(layer)
			if img is None:
				continue
			role = "other"
			if "bolt" in key:
				role = "bolt"
			elif parent in ("ways frame", "multi frame", "win frame", "free spins frame"):
				# shorter / higher layer is the labeled pallet
				h = box[3] - box[1]
				if h <= 40:
					role = "pallet"
				elif h <= 100:
					role = "box"
				else:
					role = "chain"
			groups[parent].append({"name": layer.name, "bbox": box, "img": img, "role": role, "key": key})
			print(f"  {parent} {role} {layer.name!r} {img.size} bbox={box}")

		if parent == "win frame chains" or (
			parent in ("chains upframe", "free spins frame", "win frame") and "bolt" not in key
		):
			img = composite(layer)
			if img is None:
				continue
			who = assign_chain(parent, box, layer.name)
			if who:
				chains.append({"who": who, "name": layer.name, "parent": parent, "bbox": box, "img": img})
				print(f"CHAIN {who} {layer.name!r} parent={parent!r} {img.size} bbox={box}")

		if "bolt" in key and box is not None:
			img = composite(layer)
			if img is not None:
				bolts.append({"name": layer.name, "parent": parent, "bbox": box, "img": img})

	# Classify box vs pallet inside each plaque group by height if needed
	plaques = {}
	alias = {
		"ways frame": "ways",
		"multi frame": "multi",
		"win frame": "win",
		"free spins frame": "spins",
	}
	for gname, items in groups.items():
		slug = alias[gname]
		box_items = [i for i in items if i["role"] == "box"]
		pal_items = [i for i in items if i["role"] == "pallet"]
		if not box_items and items:
			# tallest = box, next = pallet
			ordered = sorted(items, key=lambda i: (i["bbox"][3] - i["bbox"][1]), reverse=True)
			if ordered:
				ordered[0]["role"] = "box"
				box_items = [ordered[0]]
			if len(ordered) > 1:
				ordered[1]["role"] = "pallet"
				pal_items = [ordered[1]]
		if not box_items:
			print(f"MISSING box in {gname}")
			continue
		box = max(box_items, key=lambda i: (i["bbox"][2] - i["bbox"][0]) * (i["bbox"][3] - i["bbox"][1]))
		pallet = max(pal_items, key=lambda i: (i["bbox"][2] - i["bbox"][0]) * (i["bbox"][3] - i["bbox"][1])) if pal_items else None
		pocket = inner_pocket(box["img"], box["bbox"])
		well1 = list(pocket["bbox1"])
		if pallet is not None:
			# keep numbers below the labeled pallet
			well1[1] = max(well1[1], pallet["bbox"][3] - 4)
			if well1[3] - well1[1] < 8:
				well1[1] = pallet["bbox"][3]
		plaques[slug] = {
			"group": gname,
			"box": box,
			"pallet": pallet,
			"pocket": pocket,
			"well1": well1,
		}

	installed = []
	plaque_out = {}
	for slug, rec in plaques.items():
		box = rec["box"]
		saved_box = save_pair(box["img"], f"{slug}_box")
		box_name = {
			"ways": "wood_readout_ways.png",
			"multi": "wood_readout_multi.png",
			"win": "wood_readout_win.png",
			"spins": "wood_readout_spins.png",
		}[slug]
		installed.extend(install_base(Path(saved_box["px2"]), sprite_copies(box_name)))
		old = APP / "assets" / "sprites" / "tombstone" / box_name
		print(f"INSTALL {slug} box -> {box_name} sha={sha1(old)} {box['img'].size} -> {SCALE}x")

		pallet_rec = None
		if rec["pallet"] is not None:
			saved_pal = save_pair(rec["pallet"]["img"], f"{slug}_pallet")
			pal_name = {
				"ways": "wood_pallet_ways.png",
				"multi": "wood_pallet_multi.png",
				"win": "wood_pallet_win.png",
				"spins": "wood_pallet_spins.png",
			}[slug]
			installed.extend(install_base(Path(saved_pal["px2"]), sprite_copies(pal_name)))
			pallet_rec = {
				"layer": rec["pallet"]["name"],
				"bbox1": list(rec["pallet"]["bbox"]),
				"bbox2": [c * SCALE for c in rec["pallet"]["bbox"]],
				**saved_pal,
			}

		plaque_out[slug] = {
			"box": {
				"layer": box["name"],
				"bbox1": list(box["bbox"]),
				"bbox2": [c * SCALE for c in box["bbox"]],
				**saved_box,
			},
			"pallet": pallet_rec,
			"well1": rec["well1"],
			"well2": [c * SCALE for c in rec["well1"]],
			"pocket": rec["pocket"],
			"chains": [],
		}

	# plaque + board chains (merge same-column segments first)
	chain_out = {"board": [], "ways": [], "multi": [], "win": [], "spins": []}
	by_who: dict[str, list[dict]] = {"board": [], "ways": [], "multi": [], "win": [], "spins": []}
	for ch in chains:
		by_who[ch["who"]].append(ch)
	merged_chains: list[dict] = []
	for who, rows in by_who.items():
		merged_chains.extend(merge_columns(rows))
	for i, ch in enumerate(sorted(merged_chains, key=lambda c: (c["who"], c["bbox"][0], c["bbox"][1]))):
		who = ch["who"]
		idx = len(chain_out[who])
		stem = f"chain_{who}_{idx}"
		saved = save_pair(ch["img"], stem)
		entry = {
			"id": f"{who}-{idx}",
			"layer": ch["name"],
			"parent": ch["parent"],
			"bbox1": list(ch["bbox"]),
			"bbox2": [c * SCALE for c in ch["bbox"]],
			**saved,
		}
		if who == "board":
			name = f"hang_chain_{idx}.png"
			install_base(Path(saved["px2"]), board_copies(name))
			entry["game"] = f"assets/sprites/board/{name}"
		else:
			name = f"plaque_chain_{who}_{idx}.png"
			install_base(Path(saved["px2"]), sprite_copies(name))
			entry["game"] = f"assets/sprites/tombstone/{name}"
			if who in plaque_out:
				plaque_out[who]["chains"].append(entry)
		chain_out[who].append(entry)
		print(f"INSTALL chain {entry['id']} {ch['img'].size} -> {name}")

	frame_info = None
	if frame_img is not None and frame_bbox is not None:
		saved = save_pair(frame_img, "frame")
		# only install if pixels changed
		dest = APP / "assets" / "sprites" / "board" / "board_frame.png"
		new_hash = sha1(Path(saved["px2"]))
		old_hash = sha1(dest) if dest.exists() else "missing"
		if new_hash != old_hash:
			install_base(Path(saved["px2"]), board_copies("board_frame.png"))
			print(f"FRAME pixels changed {old_hash} -> {new_hash}")
		else:
			print(f"FRAME pixels unchanged {old_hash}")
		pocket = inner_pocket(frame_img, frame_bbox)
		frame_info = {
			"layer": "MAIN FRAME",
			"bbox1": list(frame_bbox),
			"bbox2": [c * SCALE for c in frame_bbox],
			"sha1": new_hash,
			"sha1_live": old_hash,
			"pocket": pocket,
			"pocket2": [c * SCALE for c in pocket["bbox1"]],
			**saved,
		}

	def lamp_nails(box):
		l, t, r, b = box
		return {
			"hangX": round((l + r) / 2) * SCALE,
			"hangY": t * SCALE,
			"left": l * SCALE,
			"top": t * SCALE,
			"right": r * SCALE,
			"bottom": b * SCALE,
			"bbox1": list(box),
		}

	lamps = {
		"L": lamp_nails(lamp_l) if lamp_l else None,
		"R": lamp_nails(lamp_r) if lamp_r else None,
	}

	manifest = {
		"source": str(src),
		"mtime": st.st_mtime,
		"canvas": [psd.width, psd.height],
		"scale": SCALE,
		"plaques": {
			k: {
				**{kk: vv for kk, vv in v.items() if kk not in ("box", "pallet")},
				"box": {kk: vv for kk, vv in v["box"].items()},
				"pallet": v["pallet"],
			}
			for k, v in plaque_out.items()
		},
		"board_chains": chain_out["board"],
		"frame": frame_info,
		"beam": {
			"bbox1": list(beam_bbox) if beam_bbox else None,
			"bbox2": [c * SCALE for c in beam_bbox] if beam_bbox else None,
		},
		"lamps": lamps,
		"layers": [{"name": x["name"], "parent": x["parent"], "bbox": x["bbox"]} for x in layers_found if x["bbox"]],
		"installed": installed,
	}
	# plaques in manifest already include box/pallet; drop raw images
	(RAW / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")

	# generated seats
	board2 = frame_info["bbox2"] if frame_info else [614, 272, 2070, 1500]
	pocket2 = frame_info["pocket2"] if frame_info else [620, 376, 1966, 1424]
	beam2 = manifest["beam"]["bbox2"] or [36, 106, 2658, 258]
	l_lamp = lamps["L"] or {"hangX": 258, "hangY": 146, "left": 196, "top": 146, "right": 320, "bottom": 610}
	r_lamp = lamps["R"] or {"hangX": 2438, "hangY": 146, "left": 2376, "top": 146, "right": 2500, "bottom": 610}

	def plaque_ts(slug: str) -> str:
		p = plaque_out[slug]
		box = p["box"]["bbox2"]
		pal = p["pallet"]["bbox2"] if p["pallet"] else box
		well = p["well2"]
		chs = p["chains"]
		chain_lines = ",\n\t\t\t".join(
			f'{{ id: "{c["id"]}", key: "plaqueChain{slug.title()}{c["id"].split("-")[1]}", left: {c["bbox2"][0]}, top: {c["bbox2"][1]}, right: {c["bbox2"][2]}, bottom: {c["bbox2"][3]} }}'
			for c in chs
		)
		if not chain_lines:
			chain_lines = ""
		return (
			f"\t\t{slug}: {{\n"
			f"\t\t\tbox: {ts_rect(box)},\n"
			f"\t\t\tpallet: {ts_rect(pal)},\n"
			f"\t\t\twell: {ts_rect(well)},\n"
			f"\t\t\tchains: [{chain_lines}],\n"
			f"\t\t}}"
		)

	chain_ts = ",\n\t\t".join(
		f'{{ id: "hang-{i}", left: {c["bbox2"][0]}, top: {c["bbox2"][1]}, right: {c["bbox2"][2]}, bottom: {c["bbox2"][3]} }}'
		for i, c in enumerate(chain_out["board"])
	)

	seats = f'''/**
 * Scene-space seats from the PSD the user actually edited.
 * Source: {src}
 * Canvas {psd.width}×{psd.height} (1×), scaled ×{SCALE} into SCENE_ART 2684×1784.
 * Plaques = extracted layer pixels (box + pallet). Lamps stay Spine — nails only.
 */
export const FRAME_SEATS = {{
	source: {json.dumps(str(src))},
	psd: {{ width: {psd.width}, height: {psd.height} }},
	scale: {SCALE},
	board: {ts_rect(board2)},
	pocket: {ts_rect(pocket2)},
	beam: {ts_rect(beam2)},
	chains: [
		{chain_ts}
	],
	lamps: {{
		L: {{
			hangX: {l_lamp["hangX"]},
			hangY: {l_lamp["hangY"]},
			left: {l_lamp["left"]},
			top: {l_lamp["top"]},
			right: {l_lamp["right"]},
			bottom: {l_lamp["bottom"]},
		}},
		R: {{
			hangX: {r_lamp["hangX"]},
			hangY: {r_lamp["hangY"]},
			left: {r_lamp["left"]},
			top: {r_lamp["top"]},
			right: {r_lamp["right"]},
			bottom: {r_lamp["bottom"]},
		}},
	}},
	plaques: {{
{plaque_ts("ways") if "ways" in plaque_out else ""},
{plaque_ts("multi") if "multi" in plaque_out else ""},
{plaque_ts("win") if "win" in plaque_out else ""},
{plaque_ts("spins") if "spins" in plaque_out else ""},
	}},
}} as const;
'''
	seats_path = APP / "src" / "game" / "frameSeats.generated.ts"
	seats_path.write_text(seats, encoding="utf-8")
	print(f"wrote {seats_path}")

	lamps_ts = f'''/** Hang pivots in SCENE_ART pixels (top of each chain). Desktop western_scene2.psd 1× ×2. */
export const HANGING_LAMPS = {{
  "period": 2.4683,
  "L": {{
    "x": {float(l_lamp["hangX"])},
    "y": {float(l_lamp["hangY"])}
  }},
  "R": {{
    "x": {float(r_lamp["hangX"])},
    "y": {float(r_lamp["hangY"])}
  }}
}} as const;
'''
	lamps_path = APP / "src" / "game" / "hangingLamps.generated.ts"
	lamps_path.write_text(lamps_ts, encoding="utf-8")
	print(f"wrote {lamps_path}")

	print(json.dumps({
		"source": str(src),
		"canvas": [psd.width, psd.height],
		"plaques": {k: {"box": v["box"]["bbox1"], "pallet": v["pallet"]["bbox1"] if v["pallet"] else None, "chains": len(v["chains"])} for k, v in plaque_out.items()},
		"board_chains": len(chain_out["board"]),
		"lamps": lamps,
		"beam": beam_bbox,
	}, indent=2))


if __name__ == "__main__":
	main()
