"""Generate base+bonus Patient idle mp4s from bluescreens via Scenario API keys."""
from __future__ import annotations

import base64
import mimetypes
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

APP = Path(__file__).resolve().parents[1]
VIDEO = APP / "assets-raw" / "lady_video"
MODEL = os.environ.get("LADY_IDLE_MODEL", "model_bytedance-seedance-2-0-fast")

BASE_PROMPT = (
    "Subtle professional looping idle of the exact same pale seated woman from "
    "the first frame. She sits still on the white wooden chair, head slightly "
    "bowed, hands in lap, leather restraint straps around torso. Very subtle "
    "shallow breathing — chest and shoulders rise and fall a few millimeters. "
    "Soft strands of long dark hair drift almost imperceptibly. Cloth folds of "
    "the white gown shift with tiny natural motion. Camera completely locked "
    "static. Solid flat blue background must stay perfectly unchanged, no new "
    "objects, no room geometry, no double chairs, no morphing, no warping, no "
    "glitch. Clinical eerie psychological horror, calm, high quality, seamless "
    "micro-motion only."
)

BONUS_PROMPT = (
    "Same exact pale seated woman from the first frame, but EXTRA horror "
    "intensity for a bonus free-spins idle. Fluorescent flicker lighting strobes "
    "faintly across her white gown and face. Occasional brief red camera-"
    "recording blink reflection in the eye. Subtle involuntary head twitch, "
    "then return to bowed pose. Restraint straps tighten with micro tension. "
    "Darker colder clinical grade, it-knows-you atmosphere. Hair strands twitch. "
    "Still one single chair, one single body, no doubles. Camera locked static. "
    "Solid flat blue background stays perfectly flat and unchanged — no new "
    "objects, no morphing, no glitch strips. Professional psychological horror "
    "loop, controlled intensity."
)

VARIANTS = {
    "lady_idle_base": (VIDEO / "lady_idle_base_blue.png", BASE_PROMPT),
    "lady_idle_bonus": (VIDEO / "lady_idle_bonus_blue.png", BONUS_PROMPT),
}


def upload_asset(image_path: Path) -> str:
    mime = mimetypes.guess_type(str(image_path))[0] or "image/png"
    encoded = base64.b64encode(image_path.read_bytes()).decode()
    resp = s.request(
        "POST",
        "/assets",
        {"image": f"data:{mime};base64,{encoded}", "name": image_path.name},
    )
    asset_id = resp.get("asset", {}).get("id") or resp.get("assetId")
    if not asset_id:
        raise SystemExit(f"upload failed: {resp}")
    print(f"[upload] {image_path.name} -> {asset_id}", flush=True)
    return asset_id


def find_asset_url(job_payload: dict) -> tuple[str | None, str | None]:
    job = job_payload.get("job", job_payload)
    ids = (job.get("metadata") or {}).get("assetIds") or []
    for aid in ids:
        info = s.request("GET", f"/assets/{aid}")
        url = info.get("asset", info).get("url")
        if url:
            return aid, url
    return None, None


def payload_for(model: str, asset_id: str, prompt: str) -> dict:
    if "seedance" in model:
        return {
            "image": asset_id,
            "lastFrameImage": asset_id,
            "prompt": prompt,
            "duration": 5,
            "resolution": "720p",
            "aspectRatio": "9:16",
            "generateAudio": False,
        }
    if "kling-v3" in model:
        return {
            "startImage": asset_id,
            "endImage": asset_id,
            "prompt": prompt,
            "duration": "5",
            "aspectRatio": "9:16",
            "generateAudio": False,
            "cfgScale": 0.55,
            "negativePrompt": (
                "double chair, duplicate body, glitch, morph, warp, text, "
                "new objects, camera move, zoom, pan"
            ),
        }
    # Kling 2.1 style
    return {
        "startImage": asset_id,
        "prompt": prompt,
        "duration": 5,
    }


def main() -> None:
    models = [MODEL]
    # fallbacks if rate-limited / unavailable
    for m in (
        "model_bytedance-seedance-2-0-fast",
        "model_kling-v3-i2v-pro",
        "model_kling-v2-1",
    ):
        if m not in models:
            models.append(m)

    pending: dict[str, str] = {}
    meta: dict[str, dict] = {}

    for stem, (blue, prompt) in VARIANTS.items():
        if not blue.is_file():
            raise SystemExit(f"missing bluescreen: {blue}")
        asset_id = upload_asset(blue)
        last_err = None
        for model in models:
            body = payload_for(model, asset_id, prompt)
            try:
                resp = s.request("POST", f"/generate/custom/{model}", body)
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                print(f"[retry] {stem} {model}: {exc}", flush=True)
                continue
            job = resp.get("job", resp)
            job_id = job.get("jobId") or job.get("id")
            if not job_id:
                last_err = RuntimeError(f"no job id: {resp}")
                continue
            pending[job_id] = stem
            meta[stem] = {"model": model, "sourceAssetId": asset_id, "jobId": job_id}
            print(f"[submit] {stem} model={model} job={job_id}", flush=True)
            break
        else:
            raise SystemExit(f"all models failed for {stem}: {last_err}")

    results = {}
    for job_id, stem in pending.items():
        print(f"[wait] {stem} ({job_id})...", flush=True)
        job = s.wait_for_job(job_id, poll_seconds=6, timeout_seconds=900)
        status = job.get("job", job).get("status")
        if status != "success":
            print(f"[FAIL] {stem}: status={status}", flush=True)
            continue
        aid, url = find_asset_url(job)
        if not url:
            print(f"[FAIL] {stem}: no asset url", flush=True)
            continue
        dest = VIDEO / f"{stem}.mp4"
        s.download(url, dest)
        meta[stem]["outputAssetId"] = aid
        meta[stem]["mp4"] = str(dest)
        results[stem] = dest
        print(f"[saved] {dest.name} ({dest.stat().st_size // 1024} KB) asset={aid}", flush=True)

    out_meta = VIDEO / "whiteroom_idle_jobs.json"
    import json

    out_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"[meta] {out_meta}", flush=True)
    if len(results) != len(VARIANTS):
        raise SystemExit(f"incomplete: {list(results)}")


if __name__ == "__main__":
    main()
