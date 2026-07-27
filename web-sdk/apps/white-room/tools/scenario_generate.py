"""Generate game art through the Scenario API (scenario.com).

Credentials are read from SCENARIO_KEY_CSV (default: the projectchimera.csv
key file), which has columns id,secret as exported from the Scenario
dashboard (Settings > API Keys).

Usage:
    python tools/scenario_generate.py "prompt text" out_name.png [--model MODEL] [--w 1024] [--h 1024] [--n 1]

Examples:
    python tools/scenario_generate.py "victorian seance parlor, horror" bg_test.png --w 1536 --h 1024
    python tools/scenario_generate.py "tarot card icon" card.png --model model_bfl-flux-2-dev

Outputs land in tools/scenario_out/.
"""

import argparse
import base64
import csv
import json
import os
import sys
import time
import urllib.request

API = "https://api.cloud.scenario.com/v1"
DEFAULT_MODEL = "model_bfl-flux-2-dev"
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
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.load(response)


def generate(prompt: str, out_name: str, model: str, width: int, height: int, count: int) -> list[str]:
    job = request(
        "POST",
        f"/generate/custom/{model}",
        {"prompt": prompt, "width": width, "height": height, "numOutputs": count},
    )
    job_id = job.get("job", {}).get("jobId") or job.get("jobId")
    if not job_id:
        raise SystemExit(f"no jobId in response: {json.dumps(job)[:400]}")
    print(f"job {job_id} submitted, polling...")

    while True:
        time.sleep(3)
        status = request("GET", f"/jobs/{job_id}")
        job_data = status.get("job", status)
        state = job_data.get("status")
        print(f"  status: {state}")
        if state == "success":
            break
        if state in ("failure", "canceled", "failed"):
            raise SystemExit(f"job failed: {json.dumps(job_data)[:600]}")

    asset_ids = job_data.get("metadata", {}).get("assetIds") or []
    os.makedirs(OUT_DIR, exist_ok=True)
    saved = []
    base, ext = os.path.splitext(out_name)
    for index, asset_id in enumerate(asset_ids):
        asset = request("GET", f"/assets/{asset_id}").get("asset", {})
        url = asset.get("url")
        if not url:
            print(f"asset {asset_id} has no url, skipping")
            continue
        suffix = f"_{index}" if len(asset_ids) > 1 else ""
        path = os.path.join(OUT_DIR, f"{base}{suffix}{ext or '.png'}")
        urllib.request.urlretrieve(url, path)
        saved.append(path)
        print(f"saved {path}")
    return saved


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument("out_name")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--w", type=int, default=1024)
    parser.add_argument("--h", type=int, default=1024)
    parser.add_argument("--n", type=int, default=1)
    args = parser.parse_args()

    if not generate(args.prompt, args.out_name, args.model, args.w, args.h, args.n):
        sys.exit("no assets produced")
