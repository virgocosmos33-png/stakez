"""Rebuild the celebration cutscenes with Seedance 2.0, consistent characters.

Uses Scenario's Seedance 2.0 (model_bytedance-seedance-2-0) in multimodal
REFERENCE mode: the 5 canonical character portraits (prem_*.png) are uploaded
once and passed as referenceImages, cited in each prompt as @image1/@image2/...
so every scene renders the SAME madam / mother / father / girl / dog. Seedance
generates synchronized audio natively (generateAudio=true), so no separate
audio pass is needed.

Finals download to tools/scenario_out/ as seed_scene*.mp4.

Run:  python tools/scenario_seedance_scenes.py
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
MODEL = "model_bytedance-seedance-2-0"
KEY_CSV = os.environ.get("SCENARIO_KEY_CSV", r"c:\Users\Emex33\Downloads\projectchimera.csv")
SRC_DIR = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenario_out")

# canonical character reference portraits (the symbol art = the ground truth look)
CHARS = {
    "madam": "prem_madam.png",
    "mom": "prem_mom.png",
    "dad": "prem_dad.png",
    "girl": "prem_girl.png",
    "dog": "prem_dog.png",
}

STYLE = (
    " Vintage grindhouse Victorian gothic horror film, aged film stock, heavy film grain, "
    "desaturated sepia and charcoal with sickly absinthe-green light, dramatic chiaroscuro, cinematic, no text."
)

# (out name, [character keys in @image order], prompt). @imageN maps to the
# Nth entry of referenceImages, which we build from the char list per scene.
SCENES = [
    ("seed_scene_dog.mp4", ["dog"],
     "The gaunt spectral black dog @image1 stands in a dark dusty Victorian parlor, barking and snarling "
     "at a tall ornate standing mirror draped with a pale dust cloth; a thin sliver of eerie green light "
     "glows from beneath the cloth and pulses; dust drifts in shafts of moonlight. "
     "Audio: a dog barking, growling and snarling aggressively, eerie horror ambience, faint ghostly whispers." + STYLE),
    ("seed_scene_wife_throat.mp4", ["mom"],
     "The pale Victorian mourning woman @image1 stands before an ornate mirror and pulls a dust cloth off it; "
     "a pale gaunt spectral hand bursts from the glowing green mirror and seizes her by the throat; she recoils "
     "in terror as green light floods the room. "
     "Audio: a woman gasping and choking, a sharp supernatural shriek, cracking glass, frantic whispers." + STYLE),
    ("seed_scene_madam_walk.mp4", ["madam"],
     "The veiled Madam Mirror @image1, a fraudulent medium in a black lace mourning veil with glowing green eyes, "
     "steps slowly out of a glowing green ornate mirror and walks forward down a dark Victorian hallway, her long "
     "veil trailing, candlelight flickering. "
     "Audio: slow deliberate footsteps, dragging fabric, a swelling choir of ghostly whispers, low dread drone." + STYLE),
    ("seed_scene_father_neck.mp4", ["madam", "dad"],
     "In a dark Victorian study, the veiled Madam Mirror @image1 stands behind the seated gentleman father @image2 "
     "and slowly turns his head at an unnatural twisted angle; his top hat has fallen; green oil-lamp light flickers. "
     "Stylized horror, not gory. "
     "Audio: a tense low string sting, a single sharp bone crack, a man's stifled gasp, whispers." + STYLE),
    ("seed_scene_girl_hair.mp4", ["madam", "girl"],
     "In a dim Victorian child's bedroom, the veiled Madam Mirror @image1 looms over the frightened little girl "
     "@image2 sitting on a bed and slowly cuts the girl's long hair with antique iron shears; locks of hair drift "
     "down; sickly green window light. Stylized and atmospheric. "
     "Audio: metal shears snipping, a child whimpering softly, close breathy whispers." + STYLE),
    ("seed_scene_family_trapped.mp4", ["madam", "mom", "dad", "girl", "dog"],
     "In an ornate Victorian bedroom, the veiled Madam Mirror @image1 stands triumphant before a huge ornate mirror; "
     "trapped inside the glowing green glass are the mourning mother @image2, the gentleman father @image3, the little "
     "girl @image4 and the gaunt black dog @image5, all clawing and pressing against the inside of the glass trying to "
     "escape; green light radiating and pulsing. "
     "Audio: muffled screams and desperate pounding on glass, a chorus of tormented whispers." + STYLE),
]

# Pro plan handles many concurrent jobs (priority queue); basic choked at 2.
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
                body_txt = error.read().decode(errors="ignore")[:300]
                print(f"  HTTP {error.code}: {body_txt}", flush=True)
                raise


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    # upload the character portraits once
    char_assets = {}
    for key, fname in CHARS.items():
        char_assets[key] = upload_image(os.path.join(SRC_DIR, fname))
        print(f"uploaded {key} -> {char_assets[key]}", flush=True)

    queue = list(SCENES)
    pending: dict[str, str] = {}   # job_id -> out
    done: dict[str, list] = {}

    while pending or queue:
        while queue and len(pending) < MAX_ACTIVE:
            out, char_keys, prompt = queue.pop(0)
            ref_ids = [char_assets[k] for k in char_keys]
            body = {
                "prompt": prompt,
                "referenceImages": ref_ids,
                "duration": 5,
                "resolution": "1080p",
                "aspectRatio": "16:9",
                "generateAudio": True,
            }
            job_id = submit(body)
            pending[job_id] = out
            print(f"submitted {out} ({len(char_keys)} refs) -> {job_id}", flush=True)

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
