"""Download the Layer AI board-frame source art into assets-raw/layer_board_frame/.

Source of truth for the weathered reel-frame TIMBER that BoardPlate.svelte is
skinned with. All media generated on Layer AI (workspace back-s-workspace, model
FLUX.1 [dev]); nothing here comes from Scenario. Re-run after regenerating to
refresh the raw plate, then run tools/make_board_frame_art.py to bake shipping
assets.

Two prompts were generated (batch of 4 each):
  - a top-down weathered dark western timber plank surface with iron banding and
    bolts (the plank FIELD used for the board backing)
  - a single recessed timber+iron reel-window socket on black (kept as a look
    reference; the shipping socket is composited in the bake for pixel-exact
    alignment to the cell grid)

`board_timber.png` is the chosen plank field; `window_ref.png` is the chosen
window reference. Both were picked by eye from the candidates/ folder.

Usage:  python tools/fetch_layer_board_frame.py [--force]
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
OUT = APP / "assets-raw" / "layer_board_frame"
CANDID = OUT / "candidates"
MEDIA = "https://media.app.layer.ai/workspaces/f0851046-512c-4983-8219-f34e22d47340/files"

# name -> (file_id, generated filename slug)
TIMBER_SLUG = "topdown_flat_lay_of_a_weathered_dark_western_timber_plank_surface_aged-2026-08-11-003000"
WINDOW_SLUG = "a_single_empty_recessed_rectangular_reel_window_socket_thick_frame_of-2026-08-11-003001"

CANDIDATES: dict[str, tuple[str, str]] = {
	"timber_0": ("37a58abf-a2f5-43c1-a2dd-afba5bc1a2a3", TIMBER_SLUG),
	"timber_1": ("d8a26a18-4257-4f36-a3d9-a63ce1a30a2f", TIMBER_SLUG),
	"timber_2": ("4c13a842-3fcb-4950-a0e8-347314eb4465", TIMBER_SLUG),
	"timber_3": ("e7d14827-ce33-4723-8657-1dcd914e4fc5", TIMBER_SLUG),
	"window_0": ("b1c985a0-9be5-466f-b945-3429580041ba", WINDOW_SLUG),
	"window_1": ("9f8b766c-d3ac-4733-bd8f-cfa35f463af6", WINDOW_SLUG),
	"window_2": ("400b97d4-47af-4e57-ace0-bb52363ba8ea", WINDOW_SLUG),
	"window_3": ("45a9294f-72b1-49de-a83a-34b15644766e", WINDOW_SLUG),
}

# the picks copied to stable names the bake reads
PICKS = {"board_timber.png": "timber_3", "window_ref.png": "window_1"}


def main() -> None:
	force = "--force" in sys.argv
	CANDID.mkdir(parents=True, exist_ok=True)
	manifest: dict[str, str] = {}
	for name, (file_id, slug) in CANDIDATES.items():
		dest = CANDID / f"{name}.png"
		manifest[dest.name] = file_id
		if dest.exists() and not force:
			print(f"[skip] {dest.name}")
			continue
		url = f"{MEDIA}/{file_id}/{slug}.png"
		with urllib.request.urlopen(url, timeout=300) as response:
			dest.write_bytes(response.read())
		print(f"[ok] {dest.name} ({dest.stat().st_size:,} B)")

	for stable, cand in PICKS.items():
		src = CANDID / f"{cand}.png"
		(OUT / stable).write_bytes(src.read_bytes())
		print(f"[pick] {stable} <- candidates/{cand}.png")

	(OUT / "manifest_layer.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")


if __name__ == "__main__":
	main()
