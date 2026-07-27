"""Generate THE WHITE ROOM host character masters via Scenario (Flux).

Outputs (assets-raw/lady_masters/):
  white_room_character_base.png   — seated Patient, straitjacket, magenta BG
  white_room_character_bonus.png  — unleashed bonus pose, same identity

Reads GAME_CONFIG for identity / promptContext. Skips existing files unless
FORCE_LADY_CHAR=1. Magenta #FF00FF BG is intentional for alpha_crop_lady.py.

Run:  python tools/gen_lady_character.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

APP = Path(__file__).resolve().parents[1]
OUT = APP / "assets-raw" / "lady_masters"
MODEL = "model_bfl-flux-2-dev"
WIDTH, HEIGHT = 1024, 1536


def _load_cfg() -> dict:
    path = (os.environ.get("GAME_CONFIG") or "").strip()
    if path and Path(path).is_file():
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return {}


def _force() -> bool:
    return os.environ.get("FORCE_LADY_CHAR", "").strip().lower() in {"1", "true", "yes"}


def _prompts(cfg: dict) -> dict[str, str]:
    pc = cfg.get("promptContext") or {}
    ident = cfg.get("identity") or {}
    game = ident.get("workingName") or ident.get("gameName") or "THE WHITE ROOM"
    palette = ", ".join(pc.get("palette") or ["#f4f1ec", "#c8c4bc", "#8a8680", "#3a3632", "#6b2a28"])
    mood = pc.get("mood") or "sterile, haunted, clinical dread"
    style = pc.get("style") or "psychological-horror asylum isolation cell"
    shared = (
        f"Full-body character sprite for \"{game}\" slot host. Theme: {style}. "
        f"Mood: {mood}. Palette: {palette}. "
        "Pale gaunt young woman PATIENT in white canvas asylum STRAITJACKET with "
        "brown leather restraint straps and metal buckles, arms bound crossed in "
        "front by long sleeves, long matted black hair, hollow haunted eyes, "
        "sitting on a plain white wooden spindle-back chair, long white institutional "
        "gown skirt with frayed hem, bare pale feet. Three-quarter view facing LEFT "
        "(toward the reels). Clinical psychological horror. "
        "SOLID flat MAGENTA #FF00FF background for chroma key — no room, no wall, "
        "no graffiti, no medical cart, no text, no watermark. "
        "NO veil, NO lace, NO gothic gown, NO hand mirror, NO purple, NO Victorian. "
        "Full figure nothing cropped, feet near bottom, head near top, painterly "
        "illustration, clear silhouette, key light top-left."
    )
    return {
        "white_room_character_base.png": (
            shared + " BASE pose: composed, slumped watchful idle, shallow breathe, straps tight."
        ),
        "white_room_character_bonus.png": (
            shared
            + " BONUS pose: SAME woman unleashed — lean forward, wilder hair, strained straps, "
            "menacing intense stare, stronger silhouette, still seated and still bound."
        ),
    }


def generate_one(filename: str, prompt: str) -> Path:
    job = s.request(
        "POST",
        f"/generate/custom/{MODEL}",
        {
            "prompt": prompt,
            "width": WIDTH,
            "height": HEIGHT,
            "numOutputs": 1,
            "guidance": 5,
            "numInferenceSteps": 28,
        },
    )
    job_id = job.get("job", {}).get("jobId") or job.get("jobId")
    if not job_id:
        raise RuntimeError(f"{filename}: no jobId: {job}")
    print(f"[gen] {filename} job={job_id}", flush=True)
    result = s.wait_for_job(job_id, timeout_seconds=600)
    job_data = result.get("job", result)
    if job_data.get("status") != "success":
        raise RuntimeError(f"{filename}: {job_data.get('status')}: {job_data}")
    asset_ids = job_data.get("metadata", {}).get("assetIds") or []
    if not asset_ids:
        raise RuntimeError(f"{filename}: no assetIds")
    asset = s.request("GET", f"/assets/{asset_ids[0]}").get("asset", {})
    url = asset.get("url")
    if not url:
        raise RuntimeError(f"{filename}: asset has no url")
    dest = OUT / filename
    s.download(url, dest)
    print(f"[gen] saved {dest}", flush=True)
    return dest


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = _load_cfg()
    prompts = _prompts(cfg)
    force = _force()
    scene = APP / "static" / "assets" / "sprites" / "scene"
    fallback_ok = (scene / "lady_character.png").is_file() and (scene / "lady_bonus.png").is_file()
    failed = 0
    for filename, prompt in prompts.items():
        dest = OUT / filename
        if dest.is_file() and not force:
            print(f"[keep] {dest.name} (FORCE_LADY_CHAR=1 to regen)", flush=True)
            continue
        ok = False
        for attempt in range(1, 4):
            try:
                generate_one(filename, prompt)
                ok = True
                break
            except Exception as err:  # noqa: BLE001
                msg = str(err)
                print(f"[err] {filename} attempt {attempt}: {msg}", flush=True)
                # Rate-limit / CU cap: do not burn retries forever
                if "429" in msg or "RateLimit" in msg or "Too Many Requests" in msg:
                    break
                if attempt < 3:
                    time.sleep(15 * attempt)
        if not ok:
            failed += 1
        time.sleep(2)
    if failed:
        if fallback_ok:
            print(
                f"[warn] {failed} master(s) not generated — continuing with existing "
                "scene cutouts for alpha_crop / spine (retry when Scenario CU allows).",
                flush=True,
            )
            return 0
        print("[fail] no masters and no scene cutouts", flush=True)
        return 1
    print("done", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
