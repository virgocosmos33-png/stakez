"""Animate a still image into a looping ambient video via the Scenario API.

Uploads the image as an asset, runs an image-to-video model with it as the
first frame, polls the job, and downloads the resulting mp4.

Usage:
    python tools/scenario_video.py <image_path> "<motion prompt>" <out.mp4> [--model model_kling-v2-1] [--duration 5]
"""

import argparse
import base64
import csv
import json
import mimetypes
import os
import time
import urllib.request

API = "https://api.cloud.scenario.com/v1"
KEY_CSV = os.environ.get("SCENARIO_KEY_CSV", r"c:\Users\Emex33\Downloads\projectchimera.csv")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenario_out")


def auth_header() -> str:
    with open(KEY_CSV, encoding="utf-8") as f:
        row = next(csv.DictReader(f))
    token = base64.b64encode(f"{row['id']}:{row['secret']}".encode()).decode()
    return f"Basic {token}"


def request(method: str, path: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(
        f"{API}{path}",
        method=method,
        headers={"Authorization": auth_header(), "Content-Type": "application/json"},
        data=json.dumps(body).encode() if body is not None else None,
    )
    with urllib.request.urlopen(req, timeout=180) as response:
        return json.load(response)


def upload_asset(image_path: str) -> str:
    mime = mimetypes.guess_type(image_path)[0] or "image/png"
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    response = request(
        "POST",
        "/assets",
        {"image": f"data:{mime};base64,{encoded}", "name": os.path.basename(image_path)},
    )
    asset_id = response.get("asset", {}).get("id") or response.get("assetId")
    if not asset_id:
        raise SystemExit(f"upload failed: {json.dumps(response)[:400]}")
    print(f"uploaded asset {asset_id}")
    return asset_id


def wait_for_job(job_id: str) -> dict:
    while True:
        time.sleep(5)
        status = request("GET", f"/jobs/{job_id}")
        job_data = status.get("job", status)
        state = job_data.get("status")
        progress = job_data.get("progress")
        print(f"  status: {state}" + (f" ({progress * 100:.0f}%)" if progress else ""))
        if state == "success":
            return job_data
        if state in ("failure", "failed", "canceled"):
            raise SystemExit(f"job failed: {json.dumps(job_data)[:600]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("prompt")
    parser.add_argument("out")
    parser.add_argument("--model", default="model_kling-v2-1")
    parser.add_argument("--duration", type=int, default=5)
    args = parser.parse_args()

    asset_id = upload_asset(args.image)

    job = request(
        "POST",
        f"/generate/custom/{args.model}",
        {"startImage": asset_id, "prompt": args.prompt, "duration": args.duration},
    )
    job_id = job.get("job", {}).get("jobId") or job.get("jobId")
    if not job_id:
        raise SystemExit(f"no jobId: {json.dumps(job)[:400]}")
    print(f"video job {job_id} submitted, polling (video can take a few minutes)...")

    job_data = wait_for_job(job_id)
    asset_ids = job_data.get("metadata", {}).get("assetIds") or []
    if not asset_ids:
        raise SystemExit(f"no assets: {json.dumps(job_data)[:600]}")

    os.makedirs(OUT_DIR, exist_ok=True)
    asset = request("GET", f"/assets/{asset_ids[0]}").get("asset", {})
    url = asset.get("url")
    out_path = os.path.join(OUT_DIR, args.out)
    urllib.request.urlretrieve(url, out_path)
    print(f"saved {out_path}")


if __name__ == "__main__":
    main()
