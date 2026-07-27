"""Batch image-to-video through Scenario: submit ALL jobs at once, poll together.

Edit JOBS below, run, and collect mp4s from tools/scenario_out/.
"""

import base64
import csv
import json
import mimetypes
import os
import time
import urllib.error
import urllib.request

API = "https://api.cloud.scenario.com/v1"
MODEL = "model_kling-v2-1"
KEY_CSV = os.environ.get("SCENARIO_KEY_CSV", r"c:\Users\Emex33\Downloads\projectchimera.csv")
SRC_DIR = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenario_out")

STYLE = (
    " Vintage grindhouse horror film, aged film stock, subtle constant film grain shimmer."
    " Camera completely static, slow subtle looping motion only, no new objects appear, no text."
)

JOBS = [
    ("celeb_t2.png", "celeb_t2.mp4",
     "The silhhouetted medium sways almost imperceptibly in the glowing doorway, the amber light behind her flickers and breathes, candle flames flicker, her long shadow trembles across the floor, dust motes drift." + STYLE),
    ("celeb_t3.png", "celeb_t3.mp4",
     "The ghostly green spectral hand slowly creeps closer to the terrified couple, its ectoplasm mist swirling, the couple trembles in fear, candle flames flicker wildly, green light pulses." + STYLE),
    ("celeb_t4.png", "celeb_t4.mp4",
     "The tarot cards and ouija planchette float and tumble slowly in mid-air, the ghostly white hands rising from the table writhe, candle flames streak and flicker, the seated people recoil in terror." + STYLE),
    ("celeb_t5.png", "celeb_t5.mp4",
     "The screaming woman's wild red hair drifts as if underwater, green spectral wisps swirl around her face, her cracked skin glows and pulses from within, her blank white eyes flare." + STYLE),
    ("celeb_t6.png", "celeb_t6.mp4",
     "The dark blood-red water ripples slowly around the pale floating face, her black hair drifts and spreads through the water, her glowing green eyes pulse, blood swirls from her lips into the water." + STYLE),
    ("celeb_t7.png", "celeb_t7.mp4",
     "The spectral medium queen's green ectoplasm aura swirls and billows violently, floating glass shards rotate and glint, red smoke churns behind the mirror, her burning green eyes blaze, witnesses tremble." + STYLE),
]


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
        "POST", "/assets",
        {"image": f"data:{mime};base64,{encoded}", "name": os.path.basename(image_path)},
    )
    return response.get("asset", {}).get("id") or response["assetId"]


# jobs already running from a previous invocation: job_id -> out name
SEED_PENDING: dict[str, str] = {
    "job_XwMETyppQsiEBAwxmveSNEWE": "celeb_t2.mp4",
    "job_RW9g2GS3AdHLKNLdX6497rVH": "celeb_t3.mp4",
}


def submit(src: str, prompt: str) -> str:
    asset_id = upload_asset(os.path.join(SRC_DIR, src))
    while True:
        try:
            job = request(
                "POST", f"/generate/custom/{MODEL}",
                {"startImage": asset_id, "prompt": prompt, "duration": 5},
            )
            return job.get("job", {}).get("jobId") or job["jobId"]
        except urllib.error.HTTPError as error:
            if error.code == 429:
                print("  rate limited, waiting 20s...")
                time.sleep(20)
            else:
                raise


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    queue = [(src, out, prompt) for src, out, prompt in JOBS if out not in SEED_PENDING.values()]
    pending = dict(SEED_PENDING)  # job_id -> out name
    done: dict[str, list] = {}
    MAX_ACTIVE = 2

    while pending or queue:
        # keep up to MAX_ACTIVE jobs running
        while queue and len(pending) < MAX_ACTIVE:
            src, out, prompt = queue.pop(0)
            job_id = submit(src, prompt)
            pending[job_id] = out
            print(f"submitted {out} -> {job_id}")

        time.sleep(10)
        for job_id in list(pending):
            status = request("GET", f"/jobs/{job_id}")
            job_data = status.get("job", status)
            state = job_data.get("status")
            if state == "success":
                done[pending.pop(job_id)] = job_data.get("metadata", {}).get("assetIds", [])
                print(f"done {len(done)}/{len(JOBS)}")
            elif state in ("failure", "failed", "canceled"):
                print(f"FAILED {pending.pop(job_id)}: {json.dumps(job_data)[:300]}")

    for out, asset_ids in done.items():
        if not asset_ids:
            print(f"no asset for {out}")
            continue
        asset = request("GET", f"/assets/{asset_ids[0]}").get("asset", {})
        urllib.request.urlretrieve(asset["url"], os.path.join(OUT_DIR, out))
        print(f"saved {out}")
    print("all done")


if __name__ == "__main__":
    main()
