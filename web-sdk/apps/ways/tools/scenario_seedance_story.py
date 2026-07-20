"""Animate the 6-beat celebration story with Seedance 2.0 Fast (first-frame mode).

Feeds the existing/new key-frames we already have as first frames, adds per-beat
motion + native audio. Fast tier @ 720p for speed. All 6 run concurrently (Pro).
Downloads to tools/scenario_out/story_t{2..7}.mp4.

Run:  python tools/scenario_seedance_story.py
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
MODEL = "model_bytedance-seedance-2-0-fast"
RESOLUTION = "720p"
KEY_CSV = os.environ.get("SCENARIO_KEY_CSV", r"c:\Users\Emex33\Downloads\projectchimera.csv")
SRC_DIR = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenario_out")

STYLE = (
    " Painterly grainy 2D-animation horror, not photorealistic, hand-painted animated film look, heavy film "
    "grain, sickly absinthe-green light, chiaroscuro. Subtle sakuga motion, smear frames on fast moves."
)

# (first-frame still, out name, motion+audio prompt)
JOBS = [
    ("scene1_dog.png", "story_t2.mp4",
     "The gaunt black dog barks aggressively at the cloth-draped mirror; the mirror glows a faint pulsing green; "
     "dust drifts. Audio: a dog barking and growling, eerie ambience, faint ghostly whispers." + STYLE),
    ("scene2b_wife_throat.png", "story_t3.mp4",
     "The woman pulls the cloth off the ornate mirror; a pale spectral arm shoots out of the glowing green mirror, "
     "grabs her by the throat and squeezes; she chokes, her eyes roll back to white and she goes limp. "
     "Audio: a woman choking and gasping, a supernatural shriek, cracking glass, whispers." + STYLE),
    ("scene3a_madam_walk.png", "story_t4.mp4",
     "The veiled Madam Mirror steps fully out of the glowing green mirror and walks forward down the dark hallway "
     "toward a bedroom, her veil trailing, candlelight flickering. "
     "Audio: slow deliberate footsteps, dragging fabric, swelling ghostly whispers, low dread drone." + STYLE),
    ("man_twisted.png", "story_t5.mp4",
     "Slow eerie push-in: the Victorian man faces the camera while his body is twisted 180 degrees the wrong way, "
     "swaying unnaturally; the veiled Madam silhouette watches from the doorway; green light flickers. Stylized, not gory. "
     "Audio: a sickening bone crack, a stifled gasp, a low dread tone, whispers." + STYLE),
    ("girl_blood.png", "story_t6.mp4",
     "The veiled Madam cuts and tears the crying girl's hair with iron shears and smears dark red across the girl's "
     "face; the terrified girl sobs; the Madam tilts her head and laughs softly. Stylized horror. "
     "Audio: a young girl crying and whimpering in fear, iron shears snipping, a soft cruel womanly laugh, whispers." + STYLE),
    ("scene5_family_trapped.png", "story_t7.mp4",
     "The veiled Madam stands still, angry but fulfilled, while behind her the whole family trapped inside the "
     "glowing green mirror claw, pound and scream, pressing against the glass trying to escape. "
     "Audio: muffled screams and desperate pounding on glass, distorted voices crying help, a chorus of tormented whispers." + STYLE),
]

MAX_ACTIVE = 6


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


def submit(body: dict) -> str:
    while True:
        try:
            job = request("POST", f"/generate/custom/{MODEL}", body)
            return job.get("job", {}).get("jobId") or job["jobId"]
        except urllib.error.HTTPError as error:
            if error.code == 429:
                print("  rate limited, waiting 20s...", flush=True)
                time.sleep(20)
            else:
                print(f"  HTTP {error.code}: {error.read().decode(errors='ignore')[:300]}", flush=True)
                raise


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    queue = []
    for still, out, prompt in JOBS:
        asset_id = upload_image(os.path.join(SRC_DIR, still))
        queue.append((out, asset_id, prompt))
        print(f"uploaded {still} -> {asset_id}", flush=True)

    pending: dict[str, str] = {}
    done: dict[str, list] = {}
    while pending or queue:
        while queue and len(pending) < MAX_ACTIVE:
            out, asset_id, prompt = queue.pop(0)
            body = {
                "prompt": prompt,
                "image": asset_id,
                "duration": 5,
                "resolution": RESOLUTION,
                "aspectRatio": "16:9",
                "generateAudio": True,
            }
            job_id = submit(body)
            pending[job_id] = out
            print(f"submitted {out} -> {job_id}", flush=True)
        time.sleep(10)
        for job_id in list(pending):
            status = request("GET", f"/jobs/{job_id}")
            job_data = status.get("job", status)
            state = job_data.get("status")
            if state == "success":
                done[pending.pop(job_id)] = job_data.get("metadata", {}).get("assetIds", [])
                print(f"done {len(done)}/{len(JOBS)}", flush=True)
            elif state in ("failure", "failed", "canceled"):
                out = pending.pop(job_id)
                print(f"FAILED {out}: {json.dumps(job_data)[:400]}", flush=True)

    for out, asset_ids in done.items():
        if not asset_ids:
            print(f"no asset for {out}", flush=True)
            continue
        asset = request("GET", f"/assets/{asset_ids[0]}").get("asset", {})
        urllib.request.urlretrieve(asset["url"], os.path.join(OUT_DIR, out))
        print(f"saved {out}", flush=True)
    print("all done", flush=True)


if __name__ == "__main__":
    main()
