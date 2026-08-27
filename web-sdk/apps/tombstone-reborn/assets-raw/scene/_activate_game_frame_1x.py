"""Open/activate Desktop western_scene2.1x.psd and copy GAME FRAME into the old 1x tab.

Never saves. Never touches Crystal 2684 western_scene2.psd on disk.
"""
from __future__ import annotations

import sys

import win32com.client

SRC_1X = r"C:\Users\Emex33\Desktop\western_scene2.1x.psd"
CRYSTAL = r"C:\Users\Emex33\Desktop\western_scene2.psd"


def path_of(doc) -> str:
	try:
		return str(doc.FullName)
	except Exception:
		return ""


def top_layer_name(doc) -> str:
	try:
		return str(doc.Layers[0].Name)
	except Exception:
		try:
			return str(doc.ArtLayers[0].Name)
		except Exception:
			return "(none)"


def find_set(doc, name: str):
	for i in range(1, int(doc.LayerSets.Count) + 1):
		g = doc.LayerSets[i]
		if str(g.Name).replace("\x00", "").strip() == name:
			return g
	return None


def main() -> int:
	ps = win32com.client.Dispatch("Photoshop.Application")
	try:
		ps.BringToFront()
	except Exception as exc:
		print(f"BringToFront: {exc}")
	ps.DisplayDialogs = 3  # psDisplayNoDialogs
	print(f"ps version={ps.Version} docs={ps.Documents.Count}")

	docs = []
	for i in range(1, int(ps.Documents.Count) + 1):
		d = ps.Documents[i]
		docs.append(d)
		print(f"TAB {i}: name={d.Name} size={d.Width}x{d.Height} path={path_of(d)!r} top={top_layer_name(d)!r}")

	# Open/activate the Desktop 1x that already has GAME FRAME
	src = None
	for d in docs:
		p = path_of(d).replace("/", "\\").lower()
		if p == SRC_1X.lower() or str(d.Name).lower() == "western_scene2.1x.psd":
			src = d
			break
	if src is None:
		print(f"OPEN {SRC_1X}")
		src = ps.Open(SRC_1X)
	ps.ActiveDocument = src
	print(f"ACTIVE src name={src.Name} size={src.Width}x{src.Height} path={path_of(src)!r} top={top_layer_name(src)!r}")

	gf = find_set(src, "GAME FRAME")
	if gf is None:
		print("ERROR GAME FRAME missing on 1x source")
		return 2
	print("src has GAME FRAME visible=" + str(gf.Visible))

	# Prefer: also put GAME FRAME on the old 1x tab named western_scene2.psd (not Crystal 2684)
	dst = None
	for i in range(1, int(ps.Documents.Count) + 1):
		d = ps.Documents[i]
		if d == src:
			continue
		w = float(d.Width)
		h = float(d.Height)
		p = path_of(d).replace("/", "\\").lower()
		name = str(d.Name).lower()
		is_crystal = abs(w - 2684) < 2 or p == CRYSTAL.lower()
		is_old_1x = name == "western_scene2.psd" and w < 2000
		print(f"CANDIDATE name={d.Name} {w}x{h} crystal={is_crystal} old1x={is_old_1x} path={path_of(d)!r}")
		if is_old_1x and not is_crystal:
			dst = d

	copied = False
	if dst is not None:
		existing = find_set(dst, "GAME FRAME")
		if existing is not None:
			print("dst already has GAME FRAME")
			copied = True
		else:
			print(f"DUPLICATE GAME FRAME into {dst.Name} {dst.Width}x{dst.Height} (no save)")
			gf.Duplicate(dst)
			# Move to top of dest
			ps.ActiveDocument = dst
			g2 = find_set(dst, "GAME FRAME")
			if g2 is not None:
				g2.Visible = True
				g2.AllLocked = False
				try:
					g2.Move(dst.Layers[0], 2)  # 2 = psPlaceBefore
				except Exception as exc:
					print(f"move-top warn: {exc}")
			copied = True
			print(f"dst top now={top_layer_name(dst)!r}")

	# Leave the 1x-with-frame tab active so the user sees it
	ps.ActiveDocument = src
	try:
		ps.BringToFront()
	except Exception:
		pass
	print(
		f"DONE active={src.Name} path={path_of(src)!r} top={top_layer_name(src)!r} copied_to_old={copied}"
	)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
