"""Download the Layer AI win-celebration source art into assets-raw/layer_win/.

Source of truth for the win ladder hero plates + the coin/cartridge scatter sheet.
All media generated on Layer AI (workspace back-s-workspace, model FLUX.1 [dev]);
nothing here comes from Scenario. Re-run after regenerating a tier to refresh the
raw plate, then run tools/make_win_celebration_art.py to bake shipping assets.

Usage:  python tools/fetch_layer_win_tiers.py [--force]
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
OUT = APP / "assets-raw" / "layer_win"
MEDIA = "https://media.app.layer.ai/workspaces/f0851046-512c-4983-8219-f34e22d47340/files"

# tier slug -> (file_id, slug of the generated filename) per candidate variant
SOURCES: dict[str, list[tuple[str, str]]] = {
    "bounty": [
        ("d290c7ff-4dfb-48dd-b194-feb0b12d78f7", "a_tarnished_tin_bounty_star_badge_and_stacked_gold_coins_scattered_on-2026-08-10-210032"),
        ("cbc40853-e379-4d6c-badc-dc0ffcb59224", "a_tarnished_tin_bounty_star_badge_and_stacked_gold_coins_scattered_on-2026-08-10-210032"),
    ],
    "showdown": [
        ("21bb0618-dbd1-48f7-9dd9-1cb280efdbeb", "two_black_gunslinger_silhouettes_in_long_coats_and_widebrim_hats-2026-08-10-210035"),
        ("34ea6701-23e6-450f-b0ef-50d510038fdf", "two_black_gunslinger_silhouettes_in_long_coats_and_widebrim_hats-2026-08-10-210035"),
    ],
    "highnoon": [
        ("3d2801d7-1a6d-4a20-8914-9fdaf952d6aa", "dramatic_close_side_view_of_a_revolver_firing_enormous_whitehot-2026-08-10-210040"),
        ("381f7f38-3cb5-4d7c-b4ee-8c2033551f86", "dramatic_close_side_view_of_a_revolver_firing_enormous_whitehot-2026-08-10-210040"),
    ],
    "laststand": [
        ("37eb1e97-549a-41a7-9349-675112aff53f", "lone_outlaw_silhouette_in_a_long_duster_coat_standing_on_a_rocky_desert-2026-08-10-210044"),
        ("a38d5090-398a-4dc7-9192-a797cffdbdda", "lone_outlaw_silhouette_in_a_long_duster_coat_standing_on_a_rocky_desert-2026-08-10-210044"),
    ],
    "bloodmoney": [
        ("db4df51a-0492-4056-a5cc-f5124f5a1324", "a_torn_burlap_money_sack_spilling_a_cascade_of_gold_coins_and_brass-2026-08-10-210047"),
        ("e5b8a393-ae76-4ff8-b53e-1d244176c079", "a_torn_burlap_money_sack_spilling_a_cascade_of_gold_coins_and_brass-2026-08-10-210047"),
    ],
    "boothill": [
        ("6db62355-a8e1-4c06-a497-166b832beb70", "vast_desert_boothill_graveyard_of_crooked_wooden_crosses_and_leaning-2026-08-10-210051"),
        ("167e2b49-d972-410d-9845-003b544b3953", "vast_desert_boothill_graveyard_of_crooked_wooden_crosses_and_leaning-2026-08-10-210051"),
    ],
    "scatter": [
        ("0b0e2862-d033-4ba8-b063-ac34afc4de56", "game_asset_sprite_sheet_on_a_pure_solid_black_background_a_neat_grid_of-2026-08-10-210216"),
        ("a4d73a9c-78e7-4d04-b757-e17cb6943932", "game_asset_sprite_sheet_on_a_pure_solid_black_background_a_neat_grid_of-2026-08-10-210216"),
    ],
}


def main() -> None:
    force = "--force" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, str] = {}
    for tier, variants in SOURCES.items():
        for index, (file_id, slug) in enumerate(variants):
            dest = OUT / f"{tier}_{index}.png"
            manifest[dest.name] = file_id
            if dest.exists() and not force:
                print(f"[skip] {dest.name}")
                continue
            url = f"{MEDIA}/{file_id}/{slug}.png"
            with urllib.request.urlopen(url, timeout=180) as response:
                dest.write_bytes(response.read())
            print(f"[ok] {dest.name} ({dest.stat().st_size:,} B)")
    (OUT / "manifest_layer.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
