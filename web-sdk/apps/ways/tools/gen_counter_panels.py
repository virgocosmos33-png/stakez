"""Generate on-theme creative accents for the WAYS / FREE SPINS counters.

The counter panels themselves are drawn procedurally (drawGlassPill -> tarnished
silver frame + violet scrying glass) so text always fits. Scenario supplies the
premium finishing touch: a subtle "haunted mirror" etched-glass texture that is
overlaid inside the glass, and an optional tarnished-silver filigree corner
ornament. Both are keyed to transparent PNGs by PIL so they drop onto the pill
without any hard background box.

Runs jobs SEQUENTIALLY (Scenario has a small parallel-job cap). A 400 validation
error is not billed, so the schema probe below is safe.

Usage:
  python gen_counter_panels.py texture
  python gen_counter_panels.py corner
  python gen_counter_panels.py all
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import scenario_api as sc

HERE = Path(__file__).resolve().parent
RAW = HERE.parents[3] / "qa-shots" / "creatives"
RAW.mkdir(parents=True, exist_ok=True)

MODEL = "model_imagen4-ultra"  # Scenario platform Imagen 4 Ultra (prompt + aspectRatio)

JOBS = {
    "texture": {
        "prompt": (
            "Dark amethyst haunted-mirror scrying glass texture, faint occult "
            "seance sigils and delicate baroque filigree etched into black glass, "
            "wisps of violet smoke, subtle cracked-mirror veins catching cold "
            "light, symmetrical centred motif fading into deep near-black at the "
            "edges, moody gothic Victorian, ornate, high detail, no text, no "
            "lettering, no border frame, no watermark"
        ),
        "aspectRatio": "1:1",
        "out": "counter_texture.png",
    },
    "corner": {
        "prompt": (
            "A single ornate corner ornament of tarnished antique silver filigree "
            "with cold violet patina, baroque gothic scrollwork and a small "
            "amethyst cabochon, top-left corner piece, isolated on pure solid "
            "black background, sharp studio lighting, centred, symmetrical, high "
            "detail, metallic, no text, no watermark"
        ),
        "aspectRatio": "1:1",
        "out": "counter_corner.png",
    },
}


def start_job(spec: dict) -> str:
    payload = {
        "prompt": spec["prompt"],
        "aspectRatio": spec["aspectRatio"],
    }
    res = sc.request("POST", f"/generate/custom/{MODEL}", payload)
    job = res.get("job", res)
    job_id = job.get("jobId") or job.get("id")
    cost = job.get("billing", {}).get("cuCost")
    print(f"job {job_id} started (cuCost={cost})", flush=True)
    return job_id


def run(name: str) -> int:
    spec = JOBS[name]
    job_id = start_job(spec)
    started = time.time()
    while True:
        job = sc.request("GET", f"/jobs/{job_id}")
        j = job.get("job", job)
        status = j.get("status")
        prog = (j.get("progress") or 0) * 100
        print(f"  {status} {prog:.0f}%  ({time.time()-started:.0f}s)", flush=True)
        if status in ("success", "failure", "canceled", "failed"):
            break
        if time.time() - started > 600:
            print("TIMEOUT", flush=True)
            return 1
        time.sleep(6)
    if status != "success":
        print("JOB FAILED:", str(j.get("error"))[:400], flush=True)
        return 1
    asset_ids = j.get("metadata", {}).get("assetIds", [])
    print("assetIds:", asset_ids, flush=True)
    for aid in asset_ids:
        a = sc.request("GET", f"/assets/{aid}")
        url = a.get("asset", a).get("url")
        if url:
            dest = RAW / spec["out"]
            sc.download(url, dest)
            print("DOWNLOADED", dest, dest.stat().st_size, "bytes", flush=True)
    return 0


def main() -> int:
    which = sys.argv[1] if len(sys.argv) > 1 else "texture"
    names = list(JOBS) if which == "all" else [which]
    for n in names:
        print(f"=== {n} ===", flush=True)
        rc = run(n)
        if rc != 0:
            return rc
    return 0


if __name__ == "__main__":
    sys.exit(main())
