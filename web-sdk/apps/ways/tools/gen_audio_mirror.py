"""Generate Madam Mirror themed audio cues via Scenario (ElevenLabs models).

Replaces the remaining Mining-Mayhem template cues with s\u00e9ance/haunted-mirror
sound design. Downloads mp3s into assets-raw/audio_gen/ and writes a manifest
that rebuild_audio_sprite.py consumes.

Run:  python tools/gen_audio_mirror.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

APP = Path(__file__).resolve().parents[1]
OUT_DIR = APP / "assets-raw" / "audio_gen"
MANIFEST = OUT_DIR / "manifest.json"

MUSIC = "model_elevenlabs-music-v2"
SFX = "model_elevenlabs-sound-effects-v2"

# cue -> (model, payload)  — durations sized close to the template slots so
# game pacing stays familiar after the sprite rebuild
PLAN: dict[str, tuple[str, dict]] = {
    "bgm_freespin": (
        MUSIC,
        {
            "prompt": (
                "Dark Victorian seance ritual music loop for a haunted mirror casino game bonus round. "
                "Slow hypnotic waltz pulse, bowed double bass drone, glass armonica shimmer, "
                "music box melody in a minor key, distant ghostly female humming, candle-lit parlor "
                "atmosphere, ticking grandfather clock, tense and occult but elegant. "
                "Seamless loop, consistent energy, no big climax, instrumental only."
            ),
            "durationSeconds": 72,
            "forceInstrumental": True,
        },
    ),
    "bgm_winlevel_big": (
        SFX,
        {
            "text": "Dark elegant orchestral win celebration loop, gothic waltz strings and harpsichord, ghostly choir pad, uptempo, seamless loop",
            "durationSeconds": 8,
            "loop": True,
        },
    ),
    "bgm_winlevel_superwin": (
        SFX,
        {
            "text": "Bigger dark orchestral celebration loop, driving gothic strings, bells and ghost choir swelling, triumphant occult energy, seamless loop",
            "durationSeconds": 8,
            "loop": True,
        },
    ),
    "bgm_winlevel_mega": (
        SFX,
        {
            "text": "Huge dark celebration loop, pounding orchestral gothic waltz, church bells, soaring spectral choir, intense, seamless loop",
            "durationSeconds": 8,
            "loop": True,
        },
    ),
    "bgm_winlevel_epic": (
        SFX,
        {
            "text": "Epic occult orchestral celebration loop, massive drums, full gothic choir, cathedral organ stabs, frantic ecstatic energy, seamless loop",
            "durationSeconds": 8,
            "loop": True,
        },
    ),
    "bgm_winlevel_max": (
        SFX,
        {
            "text": "Maximum win apocalyptic gothic celebration loop, colossal orchestra, choir fortissimo, tolling great bell, shattering glass accents, overwhelming, seamless loop",
            "durationSeconds": 8,
            "loop": True,
        },
    ),
    "sfx_anticipation": (
        SFX,
        {
            "text": "Tense ghostly anticipation loop, string tremolo rising, whispering spirits, glass resonance shimmer building suspense, haunted seance, seamless loop",
            "durationSeconds": 7.5,
            "loop": True,
        },
    ),
    "sfx_anticipation_start": (
        SFX,
        {"text": "Quick ghostly reverse whoosh riser ending in a crystalline glass ping", "durationSeconds": 1},
    ),
    "jng_intro_fs": (
        SFX,
        {"text": "Haunted music box jingle sting, ascending eerie glissando with ghostly bell flourish, elegant victorian", "durationSeconds": 2},
    ),
    "sfx_youwon_panel": (
        SFX,
        {"text": "Dark triumphant chime fanfare, antique bells arpeggio with ghostly choir tail, celebratory occult", "durationSeconds": 3},
    ),
    "sfx_bigwin_coinloop": (
        SFX,
        {
            "text": "Continuous cascade of shimmering glass chimes and spectral sparkles, magical shimmering treasure loop, seamless loop",
            "durationSeconds": 15,
            "loop": True,
        },
    ),
    "sfx_scatter_stop_1": (SFX, {"text": "Single ghostly glass bell note, low pitch, ouija planchette knock accent, haunted", "durationSeconds": 1}),
    "sfx_scatter_stop_2": (SFX, {"text": "Single ghostly glass bell note, slightly higher pitch than before, ouija knock accent, rising tension", "durationSeconds": 1}),
    "sfx_scatter_stop_3": (SFX, {"text": "Single ghostly glass bell note, medium-high pitch, ouija knock accent, more urgent", "durationSeconds": 1}),
    "sfx_scatter_stop_4": (SFX, {"text": "Single ghostly glass bell note, high pitch with whisper swirl, urgent haunted", "durationSeconds": 1}),
    "sfx_scatter_stop_5": (SFX, {"text": "Single ghostly glass bell note, highest pitch with spectral choir gasp, climactic", "durationSeconds": 1}),
    "sfx_scatter_reveal": (SFX, {"text": "Ghostly bell reveal shimmer, glass resonance bloom, mysterious", "durationSeconds": 1.5}),
    "sfx_scatter_win_v2": (SFX, {"text": "Spectral choir swell with deep resonant bell toll, seance triumph, dark magical", "durationSeconds": 3.5}),
    "sfx_multiplier_landing": (SFX, {"text": "Haunted mirror glass tick, crystalline knock with short eerie ring", "durationSeconds": 1}),
    "sfx_multiplier_combine_a": (SFX, {"text": "Glass energy charge-up swirl, rising ethereal whirl into soft chime", "durationSeconds": 1.2}),
    "sfx_multiplier_up": (SFX, {"text": "Mirror crack energy zap with reverse glass shimmer, spectral surge", "durationSeconds": 1.5}),
    "sfx_multiplier_win": (SFX, {"text": "Cascading glass arpeggio celebration, haunted chimes rising, sparkling occult win", "durationSeconds": 3.8}),
    "sfx_btn_spin": (SFX, {"text": "Elegant dark whoosh with soft antique click, quick UI spin action", "durationSeconds": 1}),
    "sfx_btn_general": (SFX, {"text": "Soft antique wooden click, subtle UI tick", "durationSeconds": 0.5}),
    "sfx_fs_respins": (SFX, {"text": "Haunting retrigger swell, ghostly choir rise ending in bright bell hit", "durationSeconds": 4}),
}


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


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, dict] = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text())

    todo = {cue: spec for cue, spec in PLAN.items() if not (OUT_DIR / f"{cue}.mp3").exists()}
    print(f"[gen] {len(todo)} cues to generate ({len(PLAN) - len(todo)} already present)", flush=True)

    # the plan allows only 2 parallel custom jobs — run strictly one at a
    # time and retry 429s with a backoff
    for cue, (model, payload) in todo.items():
        job_id = None
        for attempt in range(8):
            try:
                response = s.request("POST", f"/generate/custom/{model}", payload)
                job = response.get("job", response)
                job_id = job.get("jobId") or job.get("id")
                break
            except Exception as error:  # noqa: BLE001
                if "429" in str(error):
                    print(f"[gen] {cue}: rate-limited, retry {attempt + 1}", flush=True)
                    time.sleep(20)
                else:
                    print(f"[gen] LAUNCH FAILED {cue}: {error}", flush=True)
                    break
        if not job_id:
            continue
        try:
            job = s.wait_for_job(job_id, poll_seconds=5, timeout_seconds=900)
            status = job.get("job", job).get("status")
            if status != "success":
                print(f"[gen] FAILED {cue}: status={status}", flush=True)
                continue
            urls = find_asset_urls(job)
            if not urls:
                print(f"[gen] FAILED {cue}: no assets in job", flush=True)
                continue
            dest = OUT_DIR / f"{cue}.mp3"
            s.download(urls[0], dest)
            manifest[cue] = {"jobId": job_id, "file": dest.name, "model": model}
            MANIFEST.write_text(json.dumps(manifest, indent=1))
            print(f"[gen] saved {cue} ({dest.stat().st_size // 1024} KB)", flush=True)
        except Exception as error:  # noqa: BLE001
            print(f"[gen] FAILED {cue}: {error}", flush=True)

    print(f"[gen] done: {len(manifest)}/{len(PLAN)} cues in manifest", flush=True)


if __name__ == "__main__":
    main()
