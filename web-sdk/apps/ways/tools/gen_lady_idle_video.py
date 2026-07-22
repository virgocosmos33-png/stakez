"""Generate a 5s looping IDLE video for the Lady Mirror character (base + bonus)
via Scenario image-to-video (Kling v2.1).

Pipeline per variant:
  1. composite the transparent cutout onto a solid BLUE screen (9:16), centered
     with margin so the veil can sway without clipping. Blue is chosen because
     the character has GREEN ghost-mist (green key would eat it) and a purple
     translucent veil (over blue the veil keys to partial alpha = correct see-
     through look).
  2. upload the blue frame, run Kling image-to-video with a subtle-idle prompt.
  3. download the mp4 to assets-raw/lady_video/.

Chroma-key -> alpha webm happens in a separate step (post_lady_idle_video.py).

Run: python tools/gen_lady_idle_video.py
"""
from __future__ import annotations

import sys
import base64
import mimetypes
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

APP = Path(__file__).resolve().parents[1]
SCENE = APP / "static" / "assets" / "sprites" / "scene"
OUT = APP / "assets-raw" / "lady_video"
OUT.mkdir(parents=True, exist_ok=True)

MODEL = "model_kling-v2-1"
BLUE = (0, 0, 255)
CANVAS = (720, 1280)  # 9:16
FIG_H_FRAC = 0.9  # character height as fraction of canvas height

PROMPT = (
    "Subtle idle character animation. The gothic Victorian woman breathes gently and "
    "sways almost imperceptibly as if slowly floating in place. Her long translucent "
    "lace veil and layered gown drift and billow softly, wisps of ghostly mist curl "
    "slowly around her, faint strands of hair move. She holds the hand mirror steady. "
    "Minimal, hypnotic, elegant, slow looping motion. Camera completely static. "
    "The solid blue background stays perfectly flat and unchanged, no new objects, no text."
)

VARIANTS = {
    "lady_idle_base": "lady_character.png",
    "lady_idle_bonus": "lady_bonus.png",
}


def build_bluescreen(src: Path, dest: Path) -> None:
    fig = Image.open(src).convert("RGBA")
    canvas = Image.new("RGBA", CANVAS, BLUE + (255,))
    target_h = int(CANVAS[1] * FIG_H_FRAC)
    scale = target_h / fig.height
    target_w = int(fig.width * scale)
    fig = fig.resize((target_w, target_h), Image.LANCZOS)
    x = (CANVAS[0] - target_w) // 2
    y = (CANVAS[1] - target_h) // 2
    # composite over blue so translucent regions blend toward blue (keyable)
    canvas.alpha_composite(fig, (x, y))
    canvas.convert("RGB").save(dest, "PNG")
    print(f"[blue] {dest.name} {canvas.size}", flush=True)


def upload_asset(image_path: Path) -> str:
    mime = mimetypes.guess_type(str(image_path))[0] or "image/png"
    encoded = base64.b64encode(image_path.read_bytes()).decode()
    resp = s.request(
        "POST", "/assets",
        {"image": f"data:{mime};base64,{encoded}", "name": image_path.name},
    )
    asset_id = resp.get("asset", {}).get("id") or resp.get("assetId")
    if not asset_id:
        raise SystemExit(f"upload failed: {resp}")
    return asset_id


def find_asset_url(job_payload: dict) -> str | None:
    job = job_payload.get("job", job_payload)
    ids = (job.get("metadata") or {}).get("assetIds") or []
    for aid in ids:
        info = s.request("GET", f"/assets/{aid}")
        url = info.get("asset", info).get("url")
        if url:
            return url
    return None


def main() -> None:
    # 1. build blue frames + 2. submit all jobs
    pending: dict[str, str] = {}  # job_id -> out stem
    for stem, srcname in VARIANTS.items():
        mp4 = OUT / f"{stem}.mp4"
        if mp4.exists():
            print(f"[skip] {mp4.name} already present", flush=True)
            continue
        blue = OUT / f"{stem}_blue.png"
        build_bluescreen(SCENE / srcname, blue)
        asset_id = upload_asset(blue)
        resp = s.request(
            "POST", f"/generate/custom/{MODEL}",
            {"startImage": asset_id, "prompt": PROMPT, "duration": 5},
        )
        job = resp.get("job", resp)
        job_id = job.get("jobId") or job.get("id")
        pending[job_id] = stem
        print(f"[submit] {stem} -> {job_id}", flush=True)

    # 3. poll + download
    for job_id, stem in pending.items():
        print(f"[wait] {stem} ({job_id})...", flush=True)
        job = s.wait_for_job(job_id, poll_seconds=6, timeout_seconds=900)
        status = job.get("job", job).get("status")
        if status != "success":
            print(f"[FAIL] {stem}: status={status}", flush=True)
            continue
        url = find_asset_url(job)
        if not url:
            print(f"[FAIL] {stem}: no asset url", flush=True)
            continue
        dest = OUT / f"{stem}.mp4"
        s.download(url, dest)
        print(f"[saved] {dest.name} ({dest.stat().st_size // 1024} KB)", flush=True)


if __name__ == "__main__":
    main()
