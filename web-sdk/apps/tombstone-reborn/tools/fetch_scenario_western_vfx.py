"""Pull the western feature-VFX generations out of the Scenario team library.

Run:
    $env:SCENARIO_CRED_TXT = '<path to scenario.txt>'
    python tools/fetch_scenario_western_vfx.py

Outputs: assets-raw/scenario_western_vfx/<role>.png (+ SOURCES.txt)

These are the hero plates for the SPLIT strike and the target lock: revolver
muzzle flashes, dust plumes, the gold starburst / sparkler, and the real
splintered bullet holes. Kenney supplies the supporting smoke, light masks and
divider chrome; see tools/make_tombstone_split_vfx_atlas.py for the bake.

Team    team_SDcGAc7TMcpPtTw2DUYM9WqB
Project proj_va6b2WpUFBeUgJKVMo1VfaLZ
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import scenario_api  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "assets-raw" / "scenario_western_vfx"

# role -> (asset id, what the generation actually is)
ASSETS: dict[str, tuple[str, str]] = {
	"muzzle_flash_wood": (
		"asset_nPHwqvN6UsNJxFegtopJEKmE",
		"vintage revolver, wooden grips, firing — warm yellow flash + smoke",
	),
	"muzzle_flash_chrome": (
		"asset_YyiMgUJPKi49qraUsZCQyp7A",
		"black revolver firing — orange/yellow muzzle flash",
	),
	"dust_plume": (
		"asset_3TDgQKHtCspBGWUBg2dFQKwQ",
		"brown dust devil rising off dirt, tapering to a wispy cloud",
	),
	"dust_kick_outlaw": (
		"asset_VwrAF1in5MSrSAzWrTCLk5He",
		"skeletal cowboy scattering dirt and dust from the ground",
	),
	"starburst_gold": (
		"asset_d645nhJnf86yxFUutPBd3Zg3",
		"gold multi-point starburst",
	),
	"spark_streak_gold": (
		"asset_zEAWCU1s7FLJA76FPK2MJ8x8",
		"gold sparkler streak with a bright flare head",
	),
	"star_spiked_iron": (
		"asset_oq3aDcwji5zCuk8op67zfURo",
		"metallic spiked star with amber inlays — lock emblem",
	),
	"burst_dark": (
		"asset_81FSNPfKo3vTe5JDLtU19FJV",
		"dark jagged starburst with a hot core",
	),
	# The real splintered-wood bullet holes. The atlas used to be baked from the
	# 02:18 starburst generations by mistake, which is why every hit stamped a
	# pale radial sparkle onto the card instead of a hole.
	"holes_sheet_a": (
		"asset_9To3efFkAjWKGQsiTx1zk6WP",
		"four bullet holes splintered in wood (2x2 sheet)",
	),
	"holes_sheet_b": (
		"asset_uuJceMUv11jWQWgXJFGjocBz",
		"three radial splinter holes + one clean hole in a post (2x2 sheet)",
	),
	"holes_sheet_c": (
		"asset_p9SKDPb2A153w92wFjGKmtA9",
		"circular splintered holes with cracks (2x2 sheet)",
	),
	# Vertical weathered plank + riveted iron band — the split seam chrome.
	"plank_iron_a": (
		"asset_hxDbGe5HXL4Wn855hdj2akSD",
		"tall dark wooden plank sign in a riveted iron frame",
	),
	"plank_iron_b": (
		"asset_148CBZCoCgzNPx7wSYJ15KCQ",
		"vertical wood panel, dark metal border with rivets",
	),
}


def resolve_url(asset_id: str) -> str:
	payload = scenario_api.request("GET", f"/assets/{asset_id}")
	record = payload.get("asset", payload)
	url = record.get("url")
	if not url:
		raise SystemExit(f"no download url for {asset_id}")
	return url


def main() -> None:
	OUT.mkdir(parents=True, exist_ok=True)
	lines = [
		"Scenario team library pulls (team_SDcGAc7TMcpPtTw2DUYM9WqB /",
		"proj_va6b2WpUFBeUgJKVMo1VfaLZ), fetched by tools/fetch_scenario_western_vfx.py",
		"",
	]
	for role, (asset_id, note) in ASSETS.items():
		dest = OUT / f"{role}.png"
		scenario_api.download(resolve_url(asset_id), dest)
		size = dest.stat().st_size
		print(f"[scenario] {role:20s} {asset_id}  {size:,} B", flush=True)
		lines.append(f"{role}.png  <-  {asset_id}  # {note}")
	(OUT / "SOURCES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
	print(f"[scenario] {len(ASSETS)} assets -> {OUT}")


if __name__ == "__main__":
	main()
