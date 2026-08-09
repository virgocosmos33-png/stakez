"""Re-animate ONLY the dog scene with Seedance 2.0, sakuga action style.

First-frame mode off the painterly dog_sakuga.png key-frame, with a 2D hand-drawn
sakuga motion prompt (smear frames, speed lines, hit-stop) + native audio.
Downloads to tools/scenario_out/seed_dog_sakuga.mp4.
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
# Fast variant + 720p = much quicker/cheaper than the 1080p regular model
MODEL = "model_bytedance-seedance-2-0-fast"
RESOLUTION = "720p"
KEY_CSV = os.environ.get("SCENARIO_KEY_CSV", r"c:\Users\Emex33\Downloads\projectchimera.csv")
SRC_DIR = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenario_out")

# animate the EXISTING dog still we already have (not a freshly generated one)
SRC_IMAGE = "scene1_dog.png"
OUT_NAME = "seed_dog_sakuga.mp4"

PROMPT = (
    "2D hand-drawn sakuga action animation, painterly and grainy, NOT photorealistic, animated horror film look. "
    "The gaunt spectral black dog barks and lunges violently at the cloth-draped mirror with explosive kinetic "
    "energy: bold dramatic smear frames on the fast motion, sharp speed lines trailing the lunge, a sudden hit-stop "
    "time-freeze on the peak of the snarling bark then snapping back into motion, kinetic framing. The eerie green "
    "light beneath the cloth pulses and flares; dust and debris streak through the air. Heavy film grain, aged "
    "oil-painting texture, sickly absinthe-green light, chiaroscuro. "
    "Audio: a ferocious dog barking, snarling and growling, eerie horror ambience, faint ghostly whispers."
)


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


def upload_image(image_path: str) -> str:
    mime = mimetypes.guess_type(image_path)[0] or "image/png"
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    response = request(
        "POST", "/assets",
        {"image": f"data:{mime};base64,{encoded}", "name": os.path.basename(image_path)},
    )
    return response.get("asset", {}).get("id") or response["assetId"]


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    asset_id = upload_image(os.path.join(SRC_DIR, SRC_IMAGE))
    print(f"uploaded {SRC_IMAGE} -> {asset_id}", flush=True)

    body = {
        "prompt": PROMPT,
        "image": asset_id,
        "duration": 5,
        "resolution": RESOLUTION,
        "aspectRatio": "16:9",
        "generateAudio": True,
    }
    while True:
        try:
            job = request("POST", f"/generate/custom/{MODEL}", body)
            job_id = job.get("job", {}).get("jobId") or job["jobId"]
            break
        except urllib.error.HTTPError as error:
            if error.code == 429:
                print("  rate limited, waiting 20s...", flush=True)
                time.sleep(20)
            else:
                print(f"  HTTP {error.code}: {error.read().decode(errors='ignore')[:300]}", flush=True)
                raise
    print(f"submitted -> {job_id}", flush=True)

    while True:
        time.sleep(10)
        status = request("GET", f"/jobs/{job_id}")
        job_data = status.get("job", status)
        state = job_data.get("status")
        if state == "success":
            asset_ids = job_data.get("metadata", {}).get("assetIds", [])
            asset = request("GET", f"/assets/{asset_ids[0]}").get("asset", {})
            urllib.request.urlretrieve(asset["url"], os.path.join(OUT_DIR, OUT_NAME))
            print(f"saved {OUT_NAME}", flush=True)
            return
        if state in ("failure", "failed", "canceled"):
            print(f"FAILED: {json.dumps(job_data)[:400]}", flush=True)
            return
        print(f"  {state}...", flush=True)


if __name__ == "__main__":
    main()
