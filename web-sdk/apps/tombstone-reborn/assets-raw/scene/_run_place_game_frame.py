"""Run GAME FRAME JSX against the live Photoshop document via COM."""
from __future__ import annotations

import sys
from pathlib import Path

import win32com.client

JSX = Path(__file__).with_name("_place_game_frame_active.jsx")
LOG = Path(__file__).with_name("_game_frame_place_log.txt")


def main() -> int:
	if not JSX.is_file():
		print(f"missing {JSX}", file=sys.stderr)
		return 2
	ps = win32com.client.Dispatch("Photoshop.Application")
	try:
		ps.BringToFront()
	except Exception as exc:
		print(f"BringToFront: {exc}")
	# 3 = psDisplayNoDialogs
	ps.DisplayDialogs = 3
	print(f"ps version={ps.Version} docs={ps.Documents.Count}")
	if ps.Documents.Count < 1:
		print("ERROR no open document", file=sys.stderr)
		return 3
	doc = ps.ActiveDocument
	print(f"active name={doc.Name}")
	try:
		print(f"active path={doc.FullName}")
	except Exception:
		print("active path=(unsaved)")
	print(f"active size={doc.Width}x{doc.Height}")
	jsx_text = JSX.read_text(encoding="utf-8")
	result = ps.DoJavaScript(jsx_text)
	print(f"jsx result={result}")
	if LOG.is_file():
		print("--- log ---")
		print(LOG.read_text(encoding="utf-8", errors="replace"))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
