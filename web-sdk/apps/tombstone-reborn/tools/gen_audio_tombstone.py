# Generate Tombstone Reborn themed audio via Scenario (replaces Madam Mirror leftovers).
# Prompts: tools/scenario_sfx_prompts.json
# Output: assets-raw/audio_gen/{cue}.mp3
# Next: python tools/rebuild_audio_sprite.py
# Creds: SCENARIO_CRED_TXT or scenario.txt with api key / secret key lines.

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

_cred = os.environ.get(
    "SCENARIO_CRED_TXT",
    r"C:\Users\Emex33\Documents\Stake Engine Front End Builder\scenario.txt",
)
if Path(_cred).is_file():
    import scenario_api as _sa

    _sa.LEGACY_TXT = Path(_cred)

import scenario_api as s  # noqa: E402

APP = Path(__file__).resolve().parents[1]
OUT_DIR = APP / "assets-raw" / "audio_gen"
PROMPTS = Path(__file__).parent / "scenario_sfx_prompts.json"
MANIFEST = OUT_DIR / "manifest_tombstone.json"

SFX_MODEL = "model_sonilo-v1-1-text-to-sound-effects"
MUSIC_MODEL = "model_elevenlabs-music-v2"


def find_asset_urls(job_payload: dict) -> list[str]:
    job = job_payload.get("job", job_payload)
    asset_ids = (job.get("metadata") or {}).get("assetIds") or []
    urls = []
    for asset_id in asset_ids:
        info = s.request("GET", f"/assets/{asset_id}")
        asset = info.get("asset", info)
        url = asset.get("url")
        if url:
            urls.append(url)
    return urls


def generate_one(cue: str, model: str, payload: dict) -> Path:
    dest = OUT_DIR / f"{cue}.mp3"
    print(f"[gen] {cue} via {model} ...", flush=True)
    job = s.request("POST", f"/generate/custom/{model}", payload)
    job_id = (job.get("job") or job).get("jobId") or job.get("jobId")
    if not job_id:
        raise RuntimeError(f"{cue}: no jobId: {json.dumps(job)[:400]}")
    done = s.wait_for_job(job_id, poll_seconds=3, timeout_seconds=600)
    status = (done.get("job") or done).get("status")
    if status != "success":
        raise RuntimeError(f"{cue}: job {job_id} -> {status}: {json.dumps(done)[:500]}")
    urls = find_asset_urls(done)
    if not urls:
        raise RuntimeError(f"{cue}: no asset urls for {job_id}")
    s.download(urls[0], dest)
    print(f"[ok] {cue} -> {dest} ({dest.stat().st_size} bytes)", flush=True)
    return dest


def main() -> None:
    data = json.loads(PROMPTS.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    skip = set(data.get("skip") or [])
    manifest: dict[str, dict] = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if (OUT_DIR / "bgm_main.mp3").exists():
        skip.add("bgm_main")

    force = "--force" in sys.argv
    plan: list[tuple[str, str, dict]] = []
    for cue, spec in (data.get("sfx") or {}).items():
        if cue in skip:
            continue
        if not force and (OUT_DIR / f"{cue}.mp3").exists() and cue in manifest:
            continue
        plan.append(
            (
                cue,
                SFX_MODEL,
                {
                    "prompt": spec["prompt"],
                    "duration": int(max(1, round(float(spec.get("duration", 2))))),
                    "audioFormat": "mp3",
                },
            )
        )

    for cue, spec in (data.get("music") or {}).items():
        if cue in skip:
            continue
        if not force and (OUT_DIR / f"{cue}.mp3").exists() and cue in manifest:
            continue
        plan.append(
            (
                cue,
                MUSIC_MODEL,
                {
                    "prompt": spec["prompt"],
                    "durationSeconds": int(spec.get("durationSeconds", 8)),
                    "forceInstrumental": True,
                    "outputFormat": "mp3_44100_128",
                },
            )
        )

    root_loop2 = APP.parents[2] / "loop2.mp3"
    if root_loop2.is_file() and (force or not (OUT_DIR / "bgm_freespin.mp3").exists()):
        import shutil

        shutil.copy2(root_loop2, OUT_DIR / "bgm_freespin.mp3")
        print("[copy] loop2.mp3 -> bgm_freespin.mp3", flush=True)
        plan = [p for p in plan if p[0] != "bgm_freespin"]

    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
        plan = [p for p in plan if p[0] == only]

    print(f"[plan] {len(plan)} cues to generate", flush=True)
    failures: list[str] = []
    for cue, model, payload in plan:
        try:
            generate_one(cue, model, payload)
            manifest[cue] = {"model": model, "payload": payload, "ts": time.time()}
            MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] {cue}: {exc}", flush=True)
            failures.append(cue)
            time.sleep(2)

    print(f"[done] ok={len(plan) - len(failures)} fail={len(failures)} {failures}", flush=True)
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
