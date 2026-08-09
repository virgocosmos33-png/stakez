"""Animate the flat-vector celebration scenes with Seedance 2.0 (fast).

First-frame (image-to-video) mode off the approved vec_t*.png keyframes so the
motion keeps the EXACT simple flat-vector cartoon look. Minimal character motion
+ a cinematic push-in; Seedance renders synchronized audio natively.

Finals download to tools/scenario_out/ as seed_vec_t*.mp4.

Run:  python tools/seedance_vec_batch.py
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
    " Simple flat 2D vector cartoon animation, limited animation style, flat solid colors,"
    " clean bold outlines, NO 3D, NO realistic rendering, NO film grain, NO texture."
    " Preserve the exact flat vector art style of the first frame. Characters stay nearly"
    " still with only minimal simple motion; decisive cinematic camera push-in / zoom-in;"
    " only the flat green glow and flat flames move. No new objects, no morphing, no text."
)

# (start image, out name, motion prompt incl. native audio)
SCENES = [
    ("vec_t2_dog.png", "seed_vec_t2.mp4",
     "The flat-vector black hound holds its bark nearly frozen at the cloth-draped ornate mirror; the"
     " green glow beneath the cloth pulses; slow-then-fast camera push-in on the glowing mirror."
     " Audio: a dog barking and growling, eerie horror ambience, faint ghostly whispers." + STYLE),
    ("vec_t3_wife.png", "seed_vec_t3.mp4",
     "The flat green spectral arm stays locked gripping the wife's throat; she is almost motionless,"
     " head tipped back, blank white eyes; the green glow pulses; fast cinematic zoom-in on the grip."
     " Audio: a woman gasping and choking, a supernatural shriek, frantic whispers." + STYLE),
    ("vec_t4_madam.png", "seed_vec_t4.mp4",
     "The veiled Madam Mirror stands nearly still just after stepping from the glowing mirror, veil"
     " barely trailing, green eyes glowing; hallway candles flicker; slow dolly then quick zoom to her face."
     " Audio: slow footsteps, dragging fabric, swelling ghostly whispers, low dread drone." + STYLE),
    ("vec_t5_husband.png", "seed_vec_t5.mp4",
     "The husband holds his impossible twisted pose frozen facing camera; the oil-lamp flame flickers;"
     " the Madam's green eyes glow in the doorway; fast dramatic zoom-in on the husband's face."
     " Audio: a low string sting, a single sharp bone crack, a stifled gasp, whispers." + STYLE),
    ("vec_t6_girl.png", "seed_vec_t6.mp4",
     "The little girl sits frozen and terrified clutching her hair; the towering veiled Madam looms"
     " almost motionless, green eyes glowing, her flat green shadow-claw creeping slightly on the wall;"
     " slow-then-fast push-in toward the shadow hand."
     " Audio: a child whimpering softly, close breathy whispers, eerie ambience." + STYLE),
    ("vec_t7_family.png", "seed_vec_t7.mp4",
     "The veiled Madam Mirror's face glows nearly still inside the green mirror; the husband leans his"
     " forehead on the glass and pounds it faintly; the mother stands frozen with hands to her head; the"
     " little girl cries and trembles slightly; the black dog barks; green glow pulses; fast push-in on the Madam."
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
