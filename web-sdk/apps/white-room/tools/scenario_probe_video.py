"""Probe whether the Scenario plan can still generate video (quota check).

Attempts a minimal text-to-video job. Prints the jobId if the plan allows it,
or the plan-limit / error message if not. Used to decide whether to pursue the
Scenario route for the intro video vs. the local FFmpeg build.
Run:  python tools/scenario_probe_video.py
"""

from __future__ import annotations

import sys

import scenario_api as sc

# image-to-video / text-to-video capable models per Scenario docs
CANDIDATE_MODELS = [
    "model_kling-v2-1",
    "model_kling-v2-6-t2v-pro",
    "model_open-ai-sora-2",
]

PROMPT = (
    "slow cinematic camera push forward into an ornate haunted mirror, "
    "passing through the rippling silver glass into a swirling violet void, "
    "gothic, volumetric fog, ghostly"
)


def main() -> int:
    for model in CANDIDATE_MODELS:
        print(f"\n=== trying {model} ===", flush=True)
        try:
            res = sc.request(
                "POST",
                f"/generate/custom/{model}",
                {"prompt": PROMPT, "aspectRatio": "16:9", "duration": 5},
                timeout=60,
            )
            print("RESPONSE:", str(res)[:600], flush=True)
            job = res.get("job", res)
            job_id = job.get("jobId") or job.get("id")
            if job_id:
                print(f"JOB STARTED: {job_id} (quota OK for {model})", flush=True)
                return 0
        except Exception as error:  # noqa: BLE001
            msg = str(error)
            print("ERROR:", msg[:600], flush=True)
            if "PlanLimit" in msg or "creative units" in msg or "limit" in msg.lower():
                print("=> QUOTA EXHAUSTED", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
