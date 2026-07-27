"""Generate the 'enter the mirror' intro via Scenario TEXT-TO-VIDEO.

Original generated footage (NO reference to the game's loading art): a first-
person camera flies THROUGH an ornate haunted mirror's rippling glass and tumbles
into a swirling, rotating mirror dimension of floating glass shards, infinite
reflections and violet fog. Downloads the raw mp4 to qa-shots/intro/.

Usage:
  python tools/scenario_intro_video.py land   # 16:9
  python tools/scenario_intro_video.py port   # 9:16
  python tools/scenario_intro_video.py fetch <jobId> <land|port>   # download an existing job
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import scenario_api as sc

HERE = Path(__file__).resolve().parent
INTRO = HERE.parents[3] / "qa-shots" / "intro"
INTRO.mkdir(parents=True, exist_ok=True)

MODEL = "model_kling-v2-6-t2v-pro"  # confirmed working text-to-video

PROMPT = (
    "Cinematic first-person camera flying forward and plunging THROUGH the surface "
    "of an ornate antique haunted mirror. The silver glass ripples like water and "
    "shatters, and the camera passes through into a swirling, slowly rotating mirror "
    "dimension: hundreds of floating spinning shards of mirror glass reflecting "
    "violet light, infinite kaleidoscopic reflections, drifting fog and glowing "
    "embers, a deep violet portal void. Dark gothic occult atmosphere, deep violet "
    "and tarnished silver palette, volumetric god rays, slow ominous motion, "
    "hyper detailed, no text, no words, no title."
)

VARIANTS = {
    "land": {"aspect": "16:9", "out": "intro_mirror_land.mp4"},
    "port": {"aspect": "9:16", "out": "intro_mirror_port.mp4"},
}


def start_job(aspect: str) -> str:
    res = sc.request(
        "POST",
        f"/generate/custom/{MODEL}",
        {"prompt": PROMPT, "aspectRatio": aspect, "duration": 5},
    )
    job = res.get("job", res)
    job_id = job.get("jobId") or job.get("id")
    cost = job.get("billing", {}).get("cuCost")
    print(f"job {job_id} started (cuCost={cost}, aspect={aspect})", flush=True)
    return job_id


def poll(job_id: str):
    started = time.time()
    while True:
        job = sc.request("GET", f"/jobs/{job_id}")
        j = job.get("job", job)
        status = j.get("status")
        prog = (j.get("progress") or 0) * 100
        print(f"  {status} {prog:.0f}%  ({time.time()-started:.0f}s)", flush=True)
        if status in ("success", "failure", "canceled", "failed"):
            return j
        if time.time() - started > 900:
            print("TIMEOUT", flush=True)
            return j
        time.sleep(8)


def download_job(j: dict, out_name: str) -> bool:
    if j.get("status") != "success":
        print("JOB not success:", str(j.get("error"))[:300], flush=True)
        return False
    asset_ids = j.get("metadata", {}).get("assetIds", [])
    print("assetIds:", asset_ids, flush=True)
    for aid in asset_ids:
        a = sc.request("GET", f"/assets/{aid}")
        url = a.get("asset", a).get("url")
        if url:
            dest = INTRO / out_name
            sc.download(url, dest)
            print(f"DOWNLOADED {dest} ({dest.stat().st_size} bytes)", flush=True)
            return True
    return False


def main() -> int:
    if sys.argv[1] == "fetch":
        job_id, which = sys.argv[2], sys.argv[3]
        j = sc.request("GET", f"/jobs/{job_id}")
        return 0 if download_job(j.get("job", j), VARIANTS[which]["out"]) else 1

    which = sys.argv[1] if len(sys.argv) > 1 else "land"
    spec = VARIANTS[which]
    job_id = start_job(spec["aspect"])
    j = poll(job_id)
    return 0 if download_job(j, spec["out"]) else 1


if __name__ == "__main__":
    sys.exit(main())
