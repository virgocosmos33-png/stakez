"""Generate the per-character wild-reel videos (with audio) via Scenario + Veo 3.1.

Matches the reference clip wr_reel_wild.mp4 (The Grin): 1080x1920, ~6s, the
character idling in the narrow padded cell with black bars left/right, native
audio on the clip itself (the game plays it once, then loops silently).

Start frames are the existing wr_reel_h*.png portraits, scaled to 1920 tall and
centered on a 1080x1920 black canvas — exactly the reference composition.

Usage:
    python tools/scenario_wild_reel_videos.py h1 h2 h4 h5
    python tools/scenario_wild_reel_videos.py h1            # single test run
"""

import sys
import time
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

APP = Path(__file__).resolve().parents[1]
PORTRAITS = APP / "assets-src" / "sprites" / "mirror"
OUT = Path(__file__).parent / "scenario_out"

MODEL = "model_veo3-1-fast"
W, H = 1080, 1920

STYLE = (
    "Keep EXACTLY the composition of the input image for the entire clip: a "
    "full-body wide shot, the character visible head to toe, standing on the "
    "floor of a narrow white padded asylum cell that fills the middle of the "
    "frame. The far left and far right of the frame are plain flat solid black "
    "margins — empty blackness, not objects, nothing drawn there. Static "
    "locked-off camera, absolutely no camera movement, no zoom, no pan, no "
    "push-in, no cut. Cinematic horror, desaturated near-monochrome whites, "
    "subtle film grain, cold fluorescent light from the ceiling panel. The "
    "character stays in place; only small, slow, unsettling idle motion. "
)

PROMPTS = {
    "h1": STYLE
    + "A gaunt pale woman with long wet black hair in a white coverall stands "
    "facing the camera. She sways almost imperceptibly, breathing slowly; her "
    "head tilts a little to one side while her sunken eyes stay locked on the "
    "camera; wet strands of hair slide across her face. "
    "Audio: low fluorescent hum, slow raspy female breathing, a faint echoing water drip.",
    "h2": STYLE
    + "A young male doctor with empty glowing pale-blue eyes, white lab coat "
    "over blue scrubs, holding a clipboard. He slowly lifts his blank gaze from "
    "the clipboard to stare into the camera, perfectly calm, then taps his pen "
    "once against the clipboard. "
    "Audio: fluorescent buzz, one soft pen tap, a slow calm male exhale, distant ward echo.",
    "h4": STYLE
    + "A pale young woman with long white-blonde hair in a dotted white gown "
    "stands in profile before a wide-open doorway that is pitch black inside. "
    "She stands almost frozen, staring into the darkness; cold air from the "
    "doorway stirs her hair and the hem of her gown; she leans slightly "
    "toward the black opening. "
    "Audio: hollow wind breathing out of the doorway, a faint distant knock, a low ambient drone.",
    "h5": STYLE
    + "A man sealed in white restraints with brown leather harness straps "
    "buckled across his chest and a metal head device labeled 404, eyes closed. "
    "His fingers twitch; he strains subtly against the straps making them "
    "creak; the head device gives a faint electronic blink; his breathing is "
    "shallow and strained. "
    "Audio: electrical buzzing, creaking leather straps, deep strained breathing, one distant monitor beep.",
}


def build_start_frame(key: str) -> Path:
    """Portrait scaled to full height, centered on black 1080x1920."""
    src = PORTRAITS / f"wr_reel_{key}.png"
    portrait = Image.open(src).convert("RGB")
    scale = H / portrait.height
    scaled = portrait.resize((round(portrait.width * scale), H), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    canvas.paste(scaled, ((W - scaled.width) // 2, 0))
    OUT.mkdir(exist_ok=True)
    dest = OUT / f"wr_reel_{key}_start.png"
    canvas.save(dest)
    print(f"[{key}] start frame {scaled.width}x{H} centered -> {dest.name}")
    return dest


def submit(key: str, start_frame: Path) -> str:
    asset_id = None
    import base64
    import mimetypes

    mime = mimetypes.guess_type(str(start_frame))[0] or "image/png"
    encoded = base64.b64encode(start_frame.read_bytes()).decode()
    response = s.request(
        "POST",
        "/assets",
        {"image": f"data:{mime};base64,{encoded}", "name": start_frame.name},
    )
    asset_id = response.get("asset", {}).get("id") or response.get("assetId")
    if not asset_id:
        raise SystemExit(f"[{key}] upload failed: {str(response)[:300]}")
    print(f"[{key}] uploaded start frame as {asset_id}")

    # Veo 3.1 params: start with the full wishlist, fall back to the minimal
    # set Kling uses if the endpoint rejects unknown parameters.
    bodies = [
        {
            "startImage": asset_id,
            "prompt": PROMPTS[key],
            "duration": 6,
            "aspectRatio": "9:16",
            "resolution": "1080p",
            "generateAudio": True,
        },
        {"startImage": asset_id, "prompt": PROMPTS[key], "duration": 6},
    ]
    last_error = None
    for body in bodies:
        try:
            job = s.request("POST", f"/generate/custom/{MODEL}", body)
            job_id = job.get("job", {}).get("jobId") or job.get("jobId")
            if job_id:
                print(f"[{key}] job {job_id} submitted with keys {sorted(body)}")
                return job_id
            last_error = str(job)[:300]
        except RuntimeError as error:
            last_error = str(error)[:300]
            print(f"[{key}] submit variant failed: {last_error}")
    raise SystemExit(f"[{key}] all submit variants failed: {last_error}")


def download(key: str, job_id: str) -> Path:
    job = s.wait_for_job(job_id, poll_seconds=10, timeout_seconds=1800)
    job_data = job.get("job", job)
    if job_data.get("status") != "success":
        raise SystemExit(f"[{key}] job failed: {str(job_data)[:600]}")
    asset_ids = job_data.get("metadata", {}).get("assetIds") or []
    if not asset_ids:
        raise SystemExit(f"[{key}] no output assets: {str(job_data)[:600]}")
    asset = s.request("GET", f"/assets/{asset_ids[0]}").get("asset", {})
    dest = OUT / f"wr_reel_{key}.mp4"
    s.download(asset["url"], dest)
    print(f"[{key}] saved {dest} ({dest.stat().st_size:,} B)")
    return dest


def main() -> None:
    keys = [k.lower() for k in sys.argv[1:]] or ["h1"]
    for key in keys:
        if key not in PROMPTS:
            raise SystemExit(f"unknown character key {key!r} (choose from {sorted(PROMPTS)})")

    jobs: list[tuple[str, str]] = []
    for key in keys:
        frame = build_start_frame(key)
        jobs.append((key, submit(key, frame)))
        time.sleep(2)

    for key, job_id in jobs:
        download(key, job_id)


if __name__ == "__main__":
    main()
