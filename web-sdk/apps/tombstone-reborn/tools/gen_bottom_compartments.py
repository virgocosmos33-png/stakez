"""Generate THE WHITE ROOM bottom counter rail via Scenario (Flux Kontext edit).

Restyles the existing three-well layout (WAYS | FREE SPINS | WIN) from gold
gothic Madam Mirror chrome into white/silver clinical ornate matching the
padded-cell reel frame. Writes:

  COUNTER_FRAME_SRC/frame_bottom_compartments_gen.png

which process_bottom_compartments.py installs into static assets.

Env:
  GAME_CONFIG — optional; used only for log identity
  SCENARIO_REF_ASSET — optional Scenario asset_id of the gold layout reference
  COUNTER_FRAME_SRC — output directory for the gen master
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

MODEL = "model_flux-kontext-editing"
HERE = Path(__file__).resolve().parent
OUT_DIR = Path(
    os.environ.get(
        "COUNTER_FRAME_SRC",
        Path.home()
        / ".cursor"
        / "projects"
        / "c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios"
        / "assets",
    )
)
OUT_NAME = "frame_bottom_compartments_gen.png"
REF_PATH = (
    HERE.parent / "static" / "assets" / "sprites" / "mirror" / "frame_bottom_compartments.png"
)
# Prefer GOLD bak if present so re-runs don't restyle an already-white frame.
REF_BAK = (
    HERE.parent
    / "static"
    / "assets"
    / "sprites"
    / "mirror"
    / "frame_bottom_compartments_GOLD_BAK.png"
)

PROMPT = (
    "COMPLETE MATERIAL REDESIGN of this exact UI chrome — keep IDENTICAL geometry: "
    "three empty dark recessed rectangular wells in a horizontal row, four vertical "
    "pillars separating them, same proportions, same silhouette, same well positions. "
    "DELETE all gothic gold filigree, skulls, baroque scrolls, Victorian ornament. "
    "REPLACE materials with THE WHITE ROOM clinical asylum HUD: dirty white "
    "padded-cell fabric panels with tufted seams, brushed clinical steel / fluorescent "
    "tube housings as the outer bezel, leather restraint straps with metal buckles as "
    "the four pillar centers (no skulls), riveted observation-window corners, faint "
    "dried-blood grit only at seams. Dark charcoal empty wells (no text). Pure black "
    "background outside the rail. Face-on orthographic game UI asset, high detail, "
    "NOT a recolor of gold gothic — a NEW clinical padded-cell construction."
)


def _game_name() -> str:
    path = (os.environ.get("GAME_CONFIG") or "").strip()
    if path and Path(path).is_file():
        cfg = json.loads(Path(path).read_text(encoding="utf-8"))
        return str((cfg.get("identity") or {}).get("workingName") or "THE WHITE ROOM")
    return "THE WHITE ROOM"


def _ensure_ref_asset() -> str:
    env_id = (os.environ.get("SCENARIO_REF_ASSET") or "").strip()
    if env_id:
        return env_id
    ref = REF_BAK if REF_BAK.is_file() else REF_PATH
    if not ref.is_file():
        raise SystemExit(f"missing reference frame: {ref}")
    # Upload via Scenario REST (multipart not needed for tools path — use asset create from URL/local)
    # scenario_api helpers: put local file through temporary hosting is not available;
    # instead POST /assets/upload style via generate with image — use custom upload endpoint.
    # Prefer env SCENARIO_REF_ASSET when MCP already uploaded.
    raise SystemExit(
        "Set SCENARIO_REF_ASSET to a Scenario asset_id of the gold layout reference "
        f"(local file at {ref}). Prefer MCP upload_asset → model_run path."
    )


def main() -> None:
    print(f"gen_bottom_compartments: game={_game_name()} model={MODEL}", flush=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dest = OUT_DIR / OUT_NAME
    # MCP path: Scenario model_run downloads the master first; process installs it.
    if dest.is_file() and not (os.environ.get("FORCE_REGEN") or "").strip():
        print(f"skip gen — master already present: {dest} ({dest.stat().st_size} bytes)", flush=True)
        return

    ref_id = _ensure_ref_asset()

    # CRITICAL: bak geometry is ~3.30:1 (1524x462). Never force 21:9 (~2.33:1) —
    # that stretches wells/pillars and breaks FrameMorphHud WELL fractions.
    # Even aspectRatio=auto may still emit ~21:9 from Flux; process_bottom_compartments
    # must bak-lock resize to GOLD_BAK pixel size before install.
    job = s.request(
        "POST",
        f"/generate/custom/{MODEL}",
        {
            "prompt": PROMPT,
            "referenceImages": [ref_id],
            "numOutputs": 1,
            "aspectRatio": "auto",
            "quality": "high",
            "guidanceScale": 5.5,
        },
    )
    job_id = job.get("job", {}).get("jobId") or job.get("jobId")
    if not job_id:
        raise SystemExit(f"no jobId: {job}")
    print(f"job {job_id} submitted", flush=True)
    result = s.wait_for_job(job_id)
    job_data = result.get("job", result)
    if job_data.get("status") != "success":
        raise SystemExit(f"job failed: {job_data.get('status')}: {job_data}")
    asset_ids = job_data.get("metadata", {}).get("assetIds") or []
    if not asset_ids:
        raise SystemExit(f"no assetIds: {job_data}")
    asset = s.request("GET", f"/assets/{asset_ids[0]}").get("asset", {})
    url = asset.get("url")
    if not url:
        raise SystemExit(f"asset {asset_ids[0]} has no url")
    s.download(url, dest)
    print(f"saved {dest} ({dest.stat().st_size} bytes) from {asset_ids[0]}", flush=True)
    time.sleep(0.2)


if __name__ == "__main__":
    main()
