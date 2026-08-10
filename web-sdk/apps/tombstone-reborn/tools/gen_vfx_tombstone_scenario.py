# Generate Tombstone split-VFX source frames via Scenario (Ideogram transparent).
# Writes assets-raw/tombstone_vfx/ then run: python tools/make_tombstone_split_vfx_atlas.py

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
OUT_DIR = APP / "assets-raw" / "tombstone_vfx"
PROMPTS = Path(__file__).parent / "scenario_sfx_prompts.json"
MODEL = "model_ideogram-v3-generate-transparent"
MANIFEST = OUT_DIR / "manifest_scenario_vfx.json"


def find_asset_ids(job_payload: dict) -> list[str]:
    job = job_payload.get("job", job_payload)
    return list((job.get("metadata") or {}).get("assetIds") or [])


def main() -> None:
    data = json.loads(PROMPTS.read_text(encoding="utf-8"))
    vfx = data.get("vfx") or {}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    force = "--force" in sys.argv

    todo = {
        name: prompt
        for name, prompt in vfx.items()
        if force or name not in manifest or not (OUT_DIR / name).exists()
    }
    print(f"[vfx] {len(todo)} frames to generate", flush=True)

    failures = []
    for name, prompt in todo.items():
        try:
            print(f"[vfx] {name} ...", flush=True)
            response = s.request(
                "POST",
                f"/generate/custom/{MODEL}",
                {
                    "prompt": prompt,
                    "negativePrompt": "text, watermark, logo, background scene, photo of person, opaque square backdrop",
                    "aspectRatio": "1:1",
                    "renderingSpeed": "BALANCED",
                    "expandPrompt": False,
                    "numOutputs": 1,
                },
            )
            job_id = (response.get("job") or response).get("jobId") or response.get("jobId")
            done = s.wait_for_job(job_id, poll_seconds=4, timeout_seconds=600)
            if (done.get("job") or done).get("status") != "success":
                raise RuntimeError(json.dumps(done)[:400])
            asset_ids = find_asset_ids(done)
            if not asset_ids:
                raise RuntimeError("no assets")
            info = s.request("GET", f"/assets/{asset_ids[0]}")
            url = (info.get("asset") or info).get("url")
            if not url:
                raise RuntimeError("no url")
            dest = OUT_DIR / name
            s.download(url, dest)
            manifest[name] = {"jobId": job_id, "assetId": asset_ids[0], "ts": time.time()}
            MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
            print(f"[ok] {name} ({dest.stat().st_size} bytes)", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] {name}: {exc}", flush=True)
            failures.append(name)
            time.sleep(2)

    print(f"[vfx done] fail={failures}", flush=True)
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
