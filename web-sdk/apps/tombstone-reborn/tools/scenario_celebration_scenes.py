"""Animate + score the 5-scene celebration cutscene sequence through Scenario.

Two stages per scene, all server-side:
  1. Kling image-to-video (model_kling-v2-1) animates the still frame (silent).
     The job returns a Scenario video assetId.
  2. MM Audio 2 (model_mm-audio-2) takes that video assetId and generates
     synchronized horror audio from an audio prompt (ambience + whispers +
     scene sounds), returning the final video-with-audio asset.

Motion + audio prompts are ominous-but-restrained so Kling/MMAudio moderation
does not reject the darker beats. Finals download to tools/scenario_out/.

Run:  python tools/scenario_celebration_scenes.py
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
VIDEO_MODEL = "model_kling-v2-1"
AUDIO_MODEL = "model_mm-audio-2"
KEY_CSV = os.environ.get("SCENARIO_KEY_CSV", r"c:\Users\Emex33\Downloads\projectchimera.csv")
SRC_DIR = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenario_out")

STYLE = (
    " Vintage grindhouse horror film, aged film stock, subtle constant film grain shimmer."
    " Slow ominous cinematic motion, camera almost static, no new objects appear, no text."
)

# common horror bed layered under every scene's specific audio
AMB = (
    "Eerie horror atmosphere, low ominous drone, faint ghostly whispering voices, distant cold wind, "
    "creaking floorboards, a detuned music box far away, dread. "
)

# (start image, out name, motion prompt, audio prompt)
JOBS = [
    ("scene1_dog.png", "scene1_dog.mp4",
     "The gaunt black dog barks and snarls at the cloth-covered mirror, its body tensing and recoiling, "
     "the sliver of green light beneath the cloth pulses and flickers, dust drifts, the cloth sways faintly." + STYLE,
     AMB + "A large dog barking, snarling and growling aggressively, echoing in an empty parlor."),
    ("scene2a_wife_enter.png", "scene2a_wife_enter.mp4",
     "The Victorian wife steps slowly toward the shrouded mirror, the green light behind the cloth swells "
     "and brightens, long shadows stretch across the room, dust motes drift through the beams." + STYLE,
     AMB + "Slow hesitant footsteps on wood, a rising unnatural hum, breathy whispers growing louder."),
    ("scene2b_wife_throat.png", "scene2b_wife_throat.mp4",
     "The pale spectral hand tightens its grip on the woman's throat as she recoils, the cracked mirror's "
     "green light pulses violently, her veil and hair drift, the falling cloth slides down." + STYLE,
     AMB + "A woman gasping and choking, a sharp supernatural shriek, cracking glass, frantic whispers."),
    ("scene3a_madam_walk.png", "scene3a_madam_walk.mp4",
     "The veiled Madam Mirror walks slowly forward out of the glowing mirror, her long veil and dress "
     "trailing and swaying, candle flames flicker, the green portal light churns behind her." + STYLE,
     AMB + "Slow deliberate footsteps, trailing fabric dragging, a swelling choir of whispers, low dread tones."),
    ("scene3b_father_neck.png", "scene3b_father_neck.mp4",
     "The veiled figure slowly turns the seated man's head at an unnatural angle, his frozen expression, "
     "the green oil-lamp light flickers, her veil drifts, dread-filled slow motion." + STYLE,
     AMB + "A tense low string sting, a single sharp bone crack, a man's stifled gasp, whispers."),
    ("scene4_girl_hair.png", "scene4_girl_hair.mp4",
     "The veiled figure slowly closes the shears as locks of the girl's long hair drift down through the air, "
     "the frightened girl trembles, the green window light flickers, the tattered veil sways." + STYLE,
     AMB + "Metal shears slowly snipping, a child whimpering softly, close breathy whispers."),
    ("scene5_family_trapped.png", "scene5_family_trapped.mp4",
     "The trapped family press and claw against the inside of the glowing green mirror, their hands sliding "
     "on the glass, the green light radiates and pulses, the veiled Madam stands still and triumphant, veil drifting." + STYLE,
     AMB + "Muffled screams and desperate pounding on glass from behind a barrier, a chorus of tormented whispers."),
]

MAX_ACTIVE = 2


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


def submit(model: str, body: dict) -> str:
    while True:
        try:
            job = request("POST", f"/generate/custom/{model}", body)
            return job.get("job", {}).get("jobId") or job["jobId"]
        except urllib.error.HTTPError as error:
            if error.code == 429:
                print("  rate limited, waiting 20s...", flush=True)
                time.sleep(20)
            else:
                raise


def run_stage(tasks: list[tuple], make_body, label: str) -> dict:
    """tasks: list of (key, body_input). Returns {key: [assetIds]} for successes."""
    queue = list(tasks)
    pending: dict[str, str] = {}   # job_id -> key
    results: dict[str, list] = {}
    while pending or queue:
        while queue and len(pending) < MAX_ACTIVE:
            key, body_input = queue.pop(0)
            job_id = submit(*make_body(body_input))
            pending[job_id] = key
            print(f"[{label}] submitted {key} -> {job_id}", flush=True)
        time.sleep(10)
        for job_id in list(pending):
            status = request("GET", f"/jobs/{job_id}")
            job_data = status.get("job", status)
            state = job_data.get("status")
            if state == "success":
                key = pending.pop(job_id)
                results[key] = job_data.get("metadata", {}).get("assetIds", [])
                print(f"[{label}] done {key} ({len(results)}/{len(tasks)})", flush=True)
            elif state in ("failure", "failed", "canceled"):
                key = pending.pop(job_id)
                print(f"[{label}] FAILED {key}: {json.dumps(job_data)[:300]}", flush=True)
    return results


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    # stage 1: Kling image-to-video (silent)
    video_tasks = []
    for src, out, motion, _audio in JOBS:
        asset_id = upload_image(os.path.join(SRC_DIR, src))
        video_tasks.append((out, (asset_id, motion)))
    videos = run_stage(
        video_tasks,
        lambda inp: (VIDEO_MODEL, {"startImage": inp[0], "prompt": inp[1], "duration": 5}),
        "video",
    )

    # stage 2: MM Audio 2 video-to-audio, fed the Kling video asset directly
    audio_prompts = {out: audio for _s, out, _m, audio in JOBS}
    audio_tasks = []
    for out, asset_ids in videos.items():
        if asset_ids:
            audio_tasks.append((out, (asset_ids[0], audio_prompts[out])))
        else:
            print(f"no video asset for {out}, skipping audio", flush=True)
    finals = run_stage(
        audio_tasks,
        lambda inp: (AUDIO_MODEL, {"video": inp[0], "prompt": inp[1], "duration": 5}),
        "audio",
    )

    # download finals (fall back to the silent video if audio stage failed)
    for _src, out, _m, _a in JOBS:
        asset_ids = finals.get(out) or videos.get(out)
        if not asset_ids:
            print(f"no asset for {out}", flush=True)
            continue
        asset = request("GET", f"/assets/{asset_ids[0]}").get("asset", {})
        urllib.request.urlretrieve(asset["url"], os.path.join(OUT_DIR, out))
        tag = "with audio" if out in finals else "SILENT (audio failed)"
        print(f"saved {out} [{tag}]", flush=True)
    print("all done", flush=True)


if __name__ == "__main__":
    main()
