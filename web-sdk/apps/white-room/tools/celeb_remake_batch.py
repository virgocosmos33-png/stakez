"""Remake ALL 6 win-celebration videos in one consistent painterly-gothic style.

Image-to-video (Seedance 2.0 fast, native audio) off the celeb_new_t*.png
keyframes. New storyline: the little girl is gone; tier 6 is the blonde maid
having her golden hair shorn by the Madam, and tier 7 (MAX) is the whole
household trapped inside the mirror. The prompt preserves the exact painterly
first-frame look (NOT the flat vector cartoon).

Pro plan: all 6 submitted at once (MAX_ACTIVE=6).

Finals download to tools/scenario_out/ as celeb_remake_t*.mp4.

Run:  python tools/celeb_remake_batch.py
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
    " Preserve the EXACT painterly Victorian gothic-horror illustration style of the"
    " first frame: rich digital painting, thick inking, painterly texture, dramatic"
    " candle-lit chiaroscuro, desaturated sepia and charcoal palette with cold"
    " absinthe-green glow, aged grindhouse film grain. Camera almost static with a slow"
    " subtle cinematic push-in; characters hold their pose with only minimal motion;"
    " only the green glow, flames, smoke and fabric drift. No new objects, no morphing, no text."
)

# (start image, out name, motion + native-audio prompt)
SCENES = [
    ("celeb_new_t2.png", "celeb_remake_t2.mp4",
     "The gaunt black hound snarls and barks, hackles trembling, at the white-draped ornate"
     " mirror; the absinthe-green glow beneath the cloth pulses and breathes; the chandelier"
     " candles flicker; slow push-in on the glowing mirror."
     " Audio: a dog growling and barking, eerie horror ambience, faint ghostly whispers." + STYLE),
    ("celeb_new_t3.png", "celeb_remake_t3.mp4",
     "The glowing green spectral arm tightens its grip on the veiled wife's throat; green"
     " ectoplasm mist swirls; she trembles, head tipped back, blank white eyes; the green"
     " glow pulses; slow zoom-in on the grip."
     " Audio: a woman gasping and choking, a supernatural shriek, frantic whispers." + STYLE),
    ("celeb_new_t4.png", "celeb_remake_t4.mp4",
     "The veiled Madam Mirror steps slowly forward out of the glowing mirror into the dark"
     " hallway, her long veil and skirts trailing, green eyes glowing; wall-sconce candles"
     " flicker; slow dolly toward her face."
     " Audio: slow footsteps, dragging fabric, swelling ghostly whispers, low dread drone." + STYLE),
    ("celeb_new_t5.png", "celeb_remake_t5.mp4",
     "The mustached husband breathes in dread, eyes wide; the oil-lamp flame flickers; the"
     " veiled Madam's green eyes glow brighter in the doorway behind him; slow push-in on his face."
     " Audio: a low string sting, a faint bone creak, a stifled breath, whispers." + STYLE),
    ("celeb_new_t6.png", "celeb_remake_t6.mp4",
     "The veiled Madam closes her spectral iron shears; a long lock of golden blonde hair is"
     " severed and drifts down through the air; the kneeling blonde woman trembles and weeps;"
     " the green glow pulses; slow push-in."
     " Audio: the metallic snip of shears, a woman sobbing, cold breathy whispers, eerie ambience." + STYLE),
    ("celeb_new_t7.png", "celeb_remake_t7.mp4",
     "Inside the glowing green mirror the trapped wife, husband, blonde maid and hound writhe"
     " and pound their hands against the glass from within; the cracks in the glass pulse with"
     " green light; the veiled Madam raises her arms in triumph; green energy billows; slow push-in."
     " Audio: muffled screams and desperate pounding on glass, a chorus of tormented whispers." + STYLE),
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

    queue = list(SCENES)
    pending: dict[str, str] = {}   # job_id -> out
    done: dict[str, list] = {}

    while pending or queue:
        while queue and len(pending) < MAX_ACTIVE:
            src, out, prompt = queue.pop(0)
            asset_id = upload_image(os.path.join(SRC_DIR, src))
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
                print(f"done {len(done)}/{len(SCENES)}", flush=True)
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
