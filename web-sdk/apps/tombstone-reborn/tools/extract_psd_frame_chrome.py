"""Extract FRAME + hang-chain pixels from the user's Desktop PSD.

Does NOT import export_western_scene2. Does NOT write the PSD.
Reads C:\\Users\\Emex33\\Desktop\\western_scene2.psd (or a newer Desktop copy).
Native layer pixels, then 2x LANCZOS RGB + nearest alpha. No color-key.
No MinFilter erode.
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
RAW = APP / "assets-raw" / "scene" / "psd_frame"
SCALE = 2
ALPHA_ISLAND = 12
MIN_ISLAND = 80


def newest_psd() -> Path:
	cands = list(DESKTOP.glob("western_scene2*.psd"))
	if not cands:
		raise SystemExit("no western_scene2*.psd on Desktop")
	return max(cands, key=lambda p: p.stat().st_mtime)


def walk(layers, parent=""):
	for layer in layers:
		name = layer.name
		key = " ".join(name.lower().split())
		if layer.is_group():
			yield from walk(list(layer), key or name)
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


def islands(img: Image.Image, origin: tuple[int, int]):
	arr = np.array(img.convert("RGBA"))
	mask = arr[:, :, 3] > ALPHA_ISLAND
	h, w = mask.shape
	seen = np.zeros((h, w), dtype=np.bool_)
	found = []
	for y in range(h):
		row = mask[y]
		if not row.any():
			continue
		for x in np.flatnonzero(row):
			if seen[y, x]:
				continue
			stack = [(int(y), int(x))]
			seen[y, x] = True
			ys, xs = [int(y)], [int(x)]
			while stack:
				cy, cx = stack.pop()
				for ny in (cy - 1, cy, cy + 1):
					for nx in (cx - 1, cx, cx + 1):
						if ny < 0 or nx < 0 or ny >= h or nx >= w:
							continue
						if seen[ny, nx] or not mask[ny, nx]:
							continue
						seen[ny, nx] = True
						stack.append((ny, nx))
						ys.append(ny)
						xs.append(nx)
			area = len(xs)
			if area < MIN_ISLAND:
				continue
			x0, x1 = min(xs), max(xs) + 1
			y0, y1 = min(ys), max(ys) + 1
			crop = Image.fromarray(arr[y0:y1, x0:x1], "RGBA")
			found.append(
				{
					"bbox1": [
						origin[0] + x0,
						origin[1] + y0,
						origin[0] + x1,
						origin[1] + y1,
					],
					"area": area,
					"img": crop,
				}
			)
	found.sort(key=lambda i: i["bbox1"][0])
	return found


def inner_pocket(img: Image.Image, bbox1: tuple[int, int, int, int]):
	"""Largest fully-transparent hole, or the inner bbox of opaque ring."""
	a = np.array(img.convert("RGBA"))[:, :, 3]
	h, w = a.shape
	hole = a <= ALPHA_ISLAND
	# flood from edges = exterior; remaining hole = interior pocket
	from collections import deque

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
		# solid plate: inner 8% inset as a last-ditch measure (reported, not invented seats)
		pad_x = max(1, int(round(w * 0.08)))
		pad_y = max(1, int(round(h * 0.08)))
		x0, y0, x1, y1 = pad_x, pad_y, w - pad_x, h - pad_y
		kind = "no-hole-inset"
	return {
		"kind": kind,
		"local": [x0, y0, x1, y1],
		"bbox1": [bbox1[0] + x0, bbox1[1] + y0, bbox1[0] + x1, bbox1[1] + y1],
		"opaque_frac": float((a > ALPHA_ISLAND).mean()),
	}


def main() -> None:
	src = newest_psd()
	st = src.stat()
	print(f"PSD {src} mtime={st.st_mtime} bytes={st.st_size}")
	psd = PSDImage.open(src)
	print(f"canvas {psd.width}x{psd.height}")

	RAW.mkdir(parents=True, exist_ok=True)
	frame_img = None
	frame_bbox = None
	chain_img = None
	chain_bbox = None
	ways = []

	for layer, key, parent in walk(list(psd)):
		bbox = layer.bbox
		if bbox is None:
			continue
		l, t, r, b = bbox
		if r - l <= 1 or b - t <= 1:
			continue
		if any(tok in key for tok in ("ways", "multi", "win")) and "window" not in key:
			ways.append({"name": layer.name, "key": key, "parent": parent, "bbox": list(bbox)})
		if key == "frame":
			comp = layer.composite()
			if comp is None:
				continue
			frame_img = comp.convert("RGBA")
			frame_bbox = (int(l), int(t), int(r), int(b))
			print(f"FRAME {frame_img.size} bbox={frame_bbox} visible={layer.visible}")
		if key in ("layer 3", "hanging chains") or (parent == "hanging chains" and key.startswith("layer")):
			comp = layer.composite()
			if comp is None:
				continue
			chain_img = comp.convert("RGBA")
			chain_bbox = (int(l), int(t), int(r), int(b))
			print(f"CHAINS {layer.name!r} parent={parent!r} {chain_img.size} bbox={chain_bbox}")

	if frame_img is None or frame_bbox is None:
		raise SystemExit("FRAME layer not found")

	native_frame = RAW / "frame_native.png"
	frame_img.save(native_frame, "PNG")
	frame2 = up2(frame_img)
	frame2_path = RAW / "frame_2x.png"
	frame2.save(frame2_path, "PNG")
	pocket = inner_pocket(frame_img, frame_bbox)
	print(f"pocket {pocket}")

	chain_rows = []
	if chain_img is not None and chain_bbox is not None:
		native_chain = RAW / "hanging_chains_native.png"
		chain_img.save(native_chain, "PNG")
		up2(chain_img).save(RAW / "hanging_chains_2x.png", "PNG")
		found = islands(chain_img, (chain_bbox[0], chain_bbox[1]))
		print(f"chain islands {len(found)}")
		for i, item in enumerate(found):
			p = RAW / f"hang_chain_{i}_native.png"
			item["img"].save(p, "PNG")
			p2 = RAW / f"hang_chain_{i}_2x.png"
			up2(item["img"]).save(p2, "PNG")
			b1 = item["bbox1"]
			chain_rows.append(
				{
					"id": f"hang-{i}",
					"bbox1": b1,
					"bbox2": [c * SCALE for c in b1],
					"native": str(p),
					"px2": str(p2),
					"size1": list(item["img"].size),
					"area": item["area"],
				}
			)
			print(f"  hang-{i} {item['img'].size} bbox1={b1}")

	# install BASE timber (not small/super)
	targets = [
		APP / "assets" / "sprites" / "board" / "board_frame.png",
		APP / "static" / "assets" / "sprites" / "board" / "board_frame.png",
		APP / "assets-src" / "sprites" / "board" / "board_frame.png",
		APP / "assets-src" / "assets" / "sprites" / "board" / "board_frame.png",
	]
	old_hash = sha1(targets[0]) if targets[0].exists() else "missing"
	for dest in targets:
		dest.parent.mkdir(parents=True, exist_ok=True)
		shutil.copy2(frame2_path, dest)
		print(f"install FRAME -> {dest} {dest.stat().st_size} sha={sha1(dest)}")

	# install chain islands
	chain_dest_dir = APP / "assets" / "sprites" / "board"
	static_chain = APP / "static" / "assets" / "sprites" / "board"
	src_chain = APP / "assets-src" / "sprites" / "board"
	src_chain2 = APP / "assets-src" / "assets" / "sprites" / "board"
	for row in chain_rows:
		name = f"hang_chain_{row['id'].split('-')[1]}.png"
		srcp = Path(row["px2"])
		for d in (chain_dest_dir, static_chain, src_chain, src_chain2):
			d.mkdir(parents=True, exist_ok=True)
			shutil.copy2(srcp, d / name)
		row["game"] = f"assets/sprites/board/{name}"

	manifest = {
		"source": str(src),
		"mtime": st.st_mtime,
		"canvas": [psd.width, psd.height],
		"scale": SCALE,
		"frame": {
			"bbox1": list(frame_bbox),
			"bbox2": [c * SCALE for c in frame_bbox],
			"size1": list(frame_img.size),
			"size2": list(frame2.size),
			"native": str(native_frame),
			"px2": str(frame2_path),
			"sha1_old_board_frame": old_hash,
			"sha1_new": sha1(frame2_path),
			"pocket": pocket,
			"pocket2": [c * SCALE for c in pocket["bbox1"]],
		},
		"chains": chain_rows,
		"ways_multi_win_layers": ways,
	}
	(RAW / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
	print(json.dumps({k: manifest[k] for k in ("source", "canvas", "frame", "ways_multi_win_layers")}, indent=2, default=str))
	print(f"chains {len(chain_rows)} old_frame_sha={old_hash} new={manifest['frame']['sha1_new']}")


if __name__ == "__main__":
	main()
