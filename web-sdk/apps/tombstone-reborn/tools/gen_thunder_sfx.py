"""Generate the mega-win THUNDER cue via Scenario (ElevenLabs SFX v2).

Downloads assets-raw/audio_gen/sfx_thunder.mp3 which rebuild_audio_sprite.py
then packs into the Howler sprite. Run: python tools/gen_thunder_sfx.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

APP = Path(__file__).resolve().parents[1]
OUT = APP / "assets-raw" / "audio_gen" / "sfx_thunder.mp3"

SFX = "model_elevenlabs-sound-effects-v2"
PAYLOAD = {
    "text": (
        "Massive cinematic thunder clap for a haunted mirror slot big win. "
        "Sharp close lightning strike crack up front, then a deep powerful "
        "rolling thunder rumble with dark stormy reverb tail. Dramatic, "
        "ominous, impactful, gothic occult atmosphere. No music."
    ),
    "durationSeconds": 4,
}


def find_asset_urls(job_payload: dict) -> list[str]:
    job = job_payload.get("job", job_payload)
    asset_ids = (job.get("metadata") or {}).get("assetIds") or []
    urls = []
    for asset_id in asset_ids:
        info = s.request("GET", f"/assets/{asset_id}")
        asset = info.get("asset", info)
        if asset.get("url"):
            urls.append(asset["url"])
    return urls


def main() -> None:
    if OUT.exists():
        print(f"[thunder] already present: {OUT}", flush=True)
        return
    print("[thunder] launching Scenario SFX job...", flush=True)
    response = s.request("POST", f"/generate/custom/{SFX}", PAYLOAD)
    job = response.get("job", response)
    job_id = job.get("jobId") or job.get("id")
    if not job_id:
        raise SystemExit(f"no jobId in response: {response}")
    print(f"[thunder] job {job_id} running...", flush=True)
    job = s.wait_for_job(job_id, poll_seconds=5, timeout_seconds=900)
    status = job.get("job", job).get("status")
    if status != "success":
        raise SystemExit(f"[thunder] job failed: status={status}")
    urls = find_asset_urls(job)
    if not urls:
        raise SystemExit("[thunder] no asset urls in job")
    s.download(urls[0], OUT)
    print(f"[thunder] saved {OUT} ({OUT.stat().st_size // 1024} KB)", flush=True)


if __name__ == "__main__":
    main()
