"""Download the Layer AI BONUS-ENTRY BANNER hero art into assets-raw/layer_bonus/.

Two tiers, matching the two real buy modes in src/game/betModeMeta.ts:

  bonus_small (80x)   DEAD MAN'S HAND   the six-card special bar is fully awake
  bonus_super (1000x) OPEN GRAVE        the bar plus the sealed last-reel lane

Both were generated on Layer AI with the same model as the win-celebration hero
plates (FLUX.1 [dev], model 50d5467d-5576-4a35-af38-7e8e4799683d, workspace
back-s-workspace) so the banner plates and the win-ladder plates read as one
render pass. Nothing here comes from Scenario.

Re-run after regenerating a tier to refresh the raw plate, then run
tools/make_bonus_entry_art.py to bake the shipping assets.

Usage:  python tools/fetch_layer_bonus_entry.py [--force]
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
OUT = APP / "assets-raw" / "layer_bonus"
MEDIA = "https://media.app.layer.ai/workspaces/f0851046-512c-4983-8219-f34e22d47340/files"

# tier slug -> candidate variants, as (file_id, generated filename slug)
SOURCES: dict[str, list[tuple[str, str]]] = {
    "small": [
        ("dc266daa-ccf6-428b-8c83-eb6598608d52", "cinematic_dark_western_concept_art_wide_169_hero_plate_a_dead_mans_hand-2026-08-10-224319"),
        ("70d421ce-40ef-4143-8a55-fb385bb40715", "cinematic_dark_western_concept_art_wide_169_hero_plate_a_dead_mans_hand-2026-08-10-224319"),
        ("b366fa13-08d7-42c5-849a-3facffa76a48", "cinematic_dark_western_concept_art_wide_169_hero_plate_a_dead_mans_hand-2026-08-10-224319"),
    ],
    "super": [
        ("89c5128c-709b-4f1a-9c2b-ce04a88782b9", "cinematic_dark_western_concept_art_wide_169_hero_plate_a_grave_torn-2026-08-10-224324"),
        ("1cef32f6-d68a-4640-8271-96c3d476c555", "cinematic_dark_western_concept_art_wide_169_hero_plate_a_grave_torn-2026-08-10-224324"),
        ("435ffd00-dc9f-466b-8e24-3aef83afac2b", "cinematic_dark_western_concept_art_wide_169_hero_plate_a_grave_torn-2026-08-10-224324"),
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
