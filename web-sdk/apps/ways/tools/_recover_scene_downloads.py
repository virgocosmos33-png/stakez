"""One-off: re-download the already-generated celebration scene assets by job id.

The main batch generated all 7 video+audio jobs successfully but a download-loop
bug skipped saving them. The jobs still hold their asset ids, so fetch and save.
"""

import base64
import csv
import json
import os
import urllib.request

API = "https://api.cloud.scenario.com/v1"
KEY_CSV = os.environ.get("SCENARIO_KEY_CSV", r"c:\Users\Emex33\Downloads\projectchimera.csv")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenario_out")

# audio (final, with-sound) job ids from the batch log -> output filename
JOB_TO_OUT = {
    "job_2ZsqBokthNiRven5XzrcBvZB": "scene2a_wife_enter.mp4",
    "job_mRvgkxPKG3Bv3371NaG5VuUg": "scene1_dog.mp4",
    "job_s33f9YZcwdYfWjJKQVE4Q9Mi": "scene2b_wife_throat.mp4",
    "job_NfESqtXehPM2ZLnKMMmnQ5c7": "scene3a_madam_walk.mp4",
    "job_VZZdVUJDx2RKMto5ZQyHKWcz": "scene3b_father_neck.mp4",
    "job_DraQExvHxgiYNyZ3hR8EYfUT": "scene4_girl_hair.mp4",
    "job_Mb6AJFbWQQtHKTYa68VAHumm": "scene5_family_trapped.mp4",
}


def auth_header() -> str:
    with open(KEY_CSV, encoding="utf-8") as f:
        row = next(csv.DictReader(f))
    token = base64.b64encode(f"{row['id']}:{row['secret']}".encode()).decode()
    return f"Basic {token}"


def get(path: str) -> dict:
    req = urllib.request.Request(f"{API}{path}", headers={"Authorization": auth_header()})
    with urllib.request.urlopen(req, timeout=180) as response:
        return json.load(response)


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    for job_id, out in JOB_TO_OUT.items():
        job = get(f"/jobs/{job_id}").get("job", {})
        asset_ids = job.get("metadata", {}).get("assetIds", [])
        if not asset_ids:
            print(f"NO ASSET {out} (status={job.get('status')})", flush=True)
            continue
        asset = get(f"/assets/{asset_ids[0]}").get("asset", {})
        urllib.request.urlretrieve(asset["url"], os.path.join(OUT_DIR, out))
        print(f"saved {out}", flush=True)
    print("recovery done", flush=True)


if __name__ == "__main__":
    main()
