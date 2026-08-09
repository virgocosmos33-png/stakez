"""Generate Cell Seal FULL-BODY vertical stills (H1–H5) via Scenario API.

Respects rate-limit cooldowns (sleeps remainingSeconds). Downloads to:
  assets-raw/cellSeal/{id}_full.png
  tools/scenario_out/cellSeal/{id}_meta.json

Optional expand i2v → assets-raw/cellSeal/{id}_expand.mp4

Credentials: game-builder/.scenario-settings.json (never commit).

  python tools/scenario_cell_seal_batch.py --ids H2,H3,H4,H5 --wait-rate-limit
  python tools/scenario_cell_seal_batch.py --skip-video
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

import scenario_api as sc

APP = Path(__file__).resolve().parents[1]
RAW = APP / "assets-raw" / "cellSeal"
ARCHIVE = APP / "tools" / "scenario_out" / "cellSeal"
SYMBOLS = ["H1", "H2", "H3", "H4", "H5"]

# H1 shipped via Flux img-edit (OAuth). API-key path may hit PlanLimitReached;
# prefer Flux + portrait refs (same as asset_R3AvZAjSkWt8CFCJTY6xvoBF).
IMAGE_MODEL = os.environ.get("CELL_SEAL_IMAGE_MODEL", "model_bfl-flux-2-dev")
VIDEO_MODEL = os.environ.get("CELL_SEAL_VIDEO_MODEL", "model_xai-grok-imagine-video-1-5")
STYLE_REF = os.environ.get("CELL_SEAL_STYLE_REF", "asset_R3AvZAjSkWt8CFCJTY6xvoBF")

# Uploaded medallion portraits used as Flux referenceImages (H1 pipeline).
PORTRAIT_REFS = {
    "H1": "asset_HnWSw86T5fK8CrUr7LkcR5zx",
    "H2": "asset_XqbMtfY4AHTT1fdK6qGFjj7j",
    "H3": "asset_sejjrxmW9VG4VJoaok3jjx7Y",
    "H4": "asset_5ppdQ89hQX9jLMhfgQhdGDig",
    "H5": "asset_SULNDBWjNgYoAEMdcH2Eiujo",
}

PROMPTS = {
    "H1": (
        "FULL-BODY vertical slot-reel game asset, tall narrow portrait 512x1680. "
        "Transform this character into a complete head-to-toe standing figure "
        "filling the vertical frame. THE PATIENT — pale gaunt woman, white canvas "
        "straitjacket with leather straps, long stringy black hair, hollow haunted "
        "stare, standing centered in a narrow white quilted padded cell, overhead "
        "fluorescent ceiling light, faint dried-blood flecks, dark grey floor. "
        "Photoreal clinical horror. NOT circular medallion, NOT bust crop, NO text, "
        "NO UI, NO purple neon. Clinical whites greys silvers only."
    ),
    "H2": (
        "FULL-BODY vertical slot-reel game asset, tall narrow portrait 512x1680. "
        "Transform this character into a complete head-to-toe standing figure "
        "filling the vertical frame. THE DOCTOR — young pale man with dark wavy "
        "hair, white lab coat over light blue scrubs, cold eyes, clipboard at side, "
        "standing centered in a narrow white quilted padded cell, overhead "
        "fluorescent ceiling light, faint dried-blood flecks, dark grey floor. "
        "Photoreal clinical horror. NOT circular medallion, NOT bust crop, NO text, "
        "NO UI, NO purple. Clinical whites greys silvers only."
    ),
    "H3": (
        "FULL-BODY vertical slot-reel game asset, tall narrow portrait 512x1680. "
        "Transform this character into a complete head-to-toe standing figure "
        "filling the vertical frame. THE GRIN — terrifying bald pale figure with "
        "stretched unnatural smile, huge dark sunken eyes, grey flesh, thin "
        "hospital garb, standing centered in a narrow white quilted padded cell, "
        "overhead fluorescent ceiling light, faint dried-blood flecks, dark grey "
        "floor. Photoreal clinical horror. NOT circular medallion, NOT bust crop, "
        "NO text, NO UI, NO purple."
    ),
    "H4": (
        "FULL-BODY vertical slot-reel game asset, tall narrow portrait 512x1680. "
        "Transform this character into a complete head-to-toe standing figure "
        "filling the vertical frame. THE DOORWAY — young girl with pale blonde "
        "hair in a thin hospital gown, three-quarter view toward a dark "
        "institutional doorway into blackness, padded white asylum corridor, "
        "overhead fluorescent light, faint dried-blood flecks. Photoreal clinical "
        "horror. NOT circular medallion, NOT bust crop, NO text, NO UI."
    ),
    "H5": (
        "FULL-BODY vertical slot-reel game asset, tall narrow portrait 512x1680. "
        "Transform this character into a complete head-to-toe standing figure "
        "filling the vertical frame. FILE 404 — restrained patient, medical "
        "leather straps wrapping skull and torso, blank stare, forehead stamped "
        "404 in clinical ink (only allowed text), padded white asylum cell, "
        "overhead fluorescent light, faint dried blood. Photoreal clinical "
        "horror. NOT circular medallion, NOT bust crop, NO UI chrome, NO purple."
    ),
}

IDLE_MOTION = (
    "Subtle looping idle for a slot full-reel character: shallow breathing, tiny "
    "weight shift, clinical fluorescent flicker, keep identity locked, no camera "
    "move, no zoom, no morphing, silent."
)


def _parse_rate_limit(err: Exception) -> int | None:
    text = str(err)
    m = re.search(r'"remainingSeconds"\s*:\s*"?(\d+)"?', text)
    if m:
        return int(m.group(1))
    m = re.search(r"wait\s+(\d+)\s+seconds", text, re.I)
    if m:
        return int(m.group(1))
    if "429" in text or "RateLimit" in text or "Too Many Requests" in text:
        return 60
    return None


def _post_generate(model: str, payload: dict) -> dict:
    while True:
        try:
            return sc.request("POST", f"/generate/custom/{model}", payload, timeout=180)
        except RuntimeError as e:
            rem = _parse_rate_limit(e)
            if rem is None:
                raise
            sleep_s = rem + 20
            print(f"[rate-limit] sleeping {sleep_s}s …", flush=True)
            time.sleep(sleep_s)


def _asset_ids(job_payload: dict) -> list[str]:
    job = job_payload.get("job", job_payload)
    meta = job.get("metadata") or {}
    ids = meta.get("assetIds") or job.get("assetIds") or []
    return [i for i in ids if isinstance(i, str)]


def _download_asset(asset_id: str, dest: Path) -> Path:
    asset = sc.request("GET", f"/assets/{asset_id}").get("asset", {})
    url = asset.get("url") or asset.get("downloadUrl")
    if not url:
        raise RuntimeError(f"no url for {asset_id}")
    sc.download(url, dest)
    print(f"[dl] {dest.name} ({dest.stat().st_size} bytes) ← {asset_id}", flush=True)
    return dest


def gen_still(sym: str) -> dict:
    print(f"[still] {sym} model={IMAGE_MODEL}", flush=True)
    refs = [PORTRAIT_REFS[sym]]
    if STYLE_REF and STYLE_REF != PORTRAIT_REFS[sym]:
        refs.append(STYLE_REF)
    payload: dict = {
        "prompt": PROMPTS[sym],
        "width": 512,
        "height": 1680,
        "numOutputs": 1,
        "guidance": 4.5,
        "numInferenceSteps": 28,
        "referenceImages": refs,
    }
    # GPT Image 2 accepts quality/background; Flux ignores unknowns or rejects —
    # only attach when using openai model.
    if "gpt-image" in IMAGE_MODEL:
        payload["quality"] = "high"
        payload["background"] = "auto"
        payload.pop("guidance", None)
        payload.pop("numInferenceSteps", None)
        payload.pop("referenceImages", None)
    job = _post_generate(IMAGE_MODEL, payload)
    job_id = job.get("job", {}).get("jobId") or job.get("jobId")
    if not job_id:
        raise RuntimeError(f"{sym}: no jobId: {job}")
    print(f"[still] job={job_id}", flush=True)
    result = sc.wait_for_job(job_id, timeout_seconds=600)
    job_data = result.get("job", result)
    if job_data.get("status") != "success":
        raise RuntimeError(f"{sym}: {job_data.get('status')}: {job_data}")
    aids = _asset_ids(result)
    if not aids:
        raise RuntimeError(f"{sym}: no assetIds")
    asset_id = aids[0]
    raw = RAW / f"{sym}_full.png"
    arch = ARCHIVE / f"{sym}_full.png"
    _download_asset(asset_id, raw)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    arch.write_bytes(raw.read_bytes())
    meta = {
        "symbol": sym,
        "stillAssetId": asset_id,
        "model": IMAGE_MODEL,
        "refPortrait": PORTRAIT_REFS.get(sym),
        "styleRef": STYLE_REF,
        "note": f"full-body 512x1680 {sym}",
    }
    (ARCHIVE / f"{sym}_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def gen_video(sym: str, image_asset_id: str) -> dict:
    print(f"[video] {sym} model={VIDEO_MODEL}", flush=True)
    # Schema varies by model; image + prompt is the common pair.
    job = _post_generate(
        VIDEO_MODEL,
        {
            "prompt": IDLE_MOTION,
            "image": image_asset_id,
        },
    )
    job_id = job.get("job", {}).get("jobId") or job.get("jobId")
    if not job_id:
        raise RuntimeError(f"{sym} video: no jobId: {job}")
    result = sc.wait_for_job(job_id, timeout_seconds=700)
    job_data = result.get("job", result)
    if job_data.get("status") != "success":
        raise RuntimeError(f"{sym} video: {job_data.get('status')}")
    aids = _asset_ids(result)
    if not aids:
        raise RuntimeError(f"{sym} video: no assetIds")
    dest = RAW / f"{sym}_expand.mp4"
    _download_asset(aids[0], dest)
    mpath = ARCHIVE / f"{sym}_meta.json"
    meta = json.loads(mpath.read_text(encoding="utf-8")) if mpath.exists() else {"symbol": sym}
    meta["videoAssetId"] = aids[0]
    meta["videoModel"] = VIDEO_MODEL
    mpath.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", default=os.environ.get("CELL_SEAL_IDS", "H2,H3,H4,H5"))
    ap.add_argument("--skip-video", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--wait-rate-limit", action="store_true",
                    help="On 429, sleep remainingSeconds and continue (default for batch)")
    args = ap.parse_args()
    # always honor rate limits in this batch tool
    _ = args.wait_rate_limit

    ids = [s.strip().upper() for s in args.ids.split(",") if s.strip() in set(SYMBOLS)]
    RAW.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)

    results = []
    for sym in ids:
        existing = RAW / f"{sym}_full.png"
        if existing.exists() and existing.stat().st_size > 700_000 and not args.force:
            print(f"[skip-still] {sym} already large ({existing.stat().st_size})", flush=True)
            meta_path = ARCHIVE / f"{sym}_meta.json"
            meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {
                "symbol": sym, "stillAssetId": None, "skipped": True
            }
        else:
            meta = gen_still(sym)
        if not args.skip_video and meta.get("stillAssetId"):
            try:
                meta = gen_video(sym, meta["stillAssetId"])
            except Exception as e:
                print(f"[video-fail] {sym}: {e}", flush=True)
        results.append(meta)
        time.sleep(2)

    print(json.dumps({"ok": True, "results": results}, indent=2))


if __name__ == "__main__":
    main()
