"""Image-to-video ambient loops for THE WHITE ROOM backgrounds.

Seeds from mirror/bg_base.webp + bg_freespin.webp via Scenario Kling/Seedance.
Outputs:
  mirror/bg_base_anim.mp4
  mirror/bg_base_anim_portrait.mp4
  mirror/bg_freespin_anim.mp4

Run via DramaStudioMCP regenerate_assets scope=backgrounds.
"""
from __future__ import annotations

import base64
import mimetypes
import os
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

HERE = Path(__file__).resolve().parent
MIRROR = HERE.parent / "static" / "assets" / "sprites" / "mirror"
MODEL = os.environ.get("BG_ANIM_MODEL", "model_kling-v2-1")

JOBS = [
    {
        "src": "bg_base.webp",
        "out": "bg_base_anim.mp4",
        "prompt": (
            "Subtle ambient loop of a sterile white padded isolation cell. Fluorescent "
            "overhead light flickers faintly, soft dust drifts, camera completely static. "
            "No people entering, no text, no purple neon. Clinical dread."
        ),
    },
    {
        "src": "bg_base.webp",
        "out": "bg_base_anim_portrait.mp4",
        "portrait": True,
        "prompt": (
            "Portrait-framed subtle ambient loop of a sterile white padded isolation cell. "
            "Faint fluorescent flicker, static camera, no new objects, no text."
        ),
    },
    {
        "src": "bg_freespin.webp",
        "out": "bg_freespin_anim.mp4",
        "prompt": (
            "Subtle ambient loop of THE WHITE ROOM free-spin cell — harsher fluorescent "
            "strobe, deeper shadows in padded walls, static camera, clinical whiteout mood, "
            "no purple, no gothic parlor, no text."
        ),
    },
]


def upload(path: Path) -> str:
    mime = mimetypes.guess_type(str(path))[0] or "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode()
    resp = s.request("POST", "/assets", {"image": f"data:{mime};base64,{b64}", "name": path.name})
    aid = resp.get("asset", {}).get("id") or resp.get("assetId")
    if not aid:
        raise SystemExit(f"upload failed: {resp}")
    return aid


def portraitize(src: Path, dest: Path) -> None:
    img = Image.open(src).convert("RGB")
    w, h = img.size
    pw, ph = 1080, 1920
    scale = max(pw / w, ph / h)
    nw, nh = int(w * scale), int(h * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - pw) // 2
    top = (nh - ph) // 2
    img.crop((left, top, left + pw, top + ph)).save(dest, "WEBP", quality=90, method=6)


def poll_download(job_id: str, out: Path) -> bool:
    for _ in range(120):
        time.sleep(3)
        st = s.request("GET", f"/jobs/{job_id}")
        j = st.get("job", st)
        status = j.get("status")
        if status in ("success", "completed", "done"):
            url = None
            for a in j.get("assets") or []:
                if isinstance(a, dict) and a.get("url"):
                    url = a["url"]
                    break
            if not url:
                ids = (j.get("metadata") or {}).get("assetIds") or []
                for aid in ids:
                    info = s.request("GET", f"/assets/{aid}")
                    url = info.get("asset", info).get("url")
                    if url:
                        break
            if url:
                urllib.request.urlretrieve(url, out)
                print(f"[bg-anim] saved {out} ({out.stat().st_size})", flush=True)
                return True
            print(f"[bg-anim] no url for {job_id}: {j}", flush=True)
            return False
        if status in ("failure", "failed", "error"):
            print(f"[bg-anim] failed {job_id}: {j}", flush=True)
            return False
    print(f"[bg-anim] timeout {job_id}", flush=True)
    return False


def main() -> int:
    ok = True
    for job in JOBS:
        src = MIRROR / job["src"]
        if not src.is_file():
            alt = src.with_suffix(".png")
            if alt.is_file():
                src = alt
            else:
                print(f"[bg-anim] missing {job['src']}", flush=True)
                ok = False
                continue
        out = MIRROR / job["out"]
        if out.exists() and out.stat().st_size > 100_000 and os.environ.get("FORCE") != "1":
            # Force replace Madam-era files when GAME_NAME is white room unless KEEP_OLD=1
            if os.environ.get("KEEP_OLD") == "1":
                print(f"[bg-anim] keep {out.name}", flush=True)
                continue
        seed = src
        if job.get("portrait"):
            seed = MIRROR / "_bg_base_portrait_seed.webp"
            portraitize(src, seed)
        try:
            aid = upload(seed)
            # Kling img2video expects startImage (asset id), not image.
            payload = {"startImage": aid, "prompt": job["prompt"], "duration": 5}
            res = s.request("POST", f"/generate/custom/{MODEL}", payload)
            jid = (res.get("job") or res).get("jobId") or (res.get("job") or res).get("id")
            print(f"[bg-anim] {job['out']} job {jid}", flush=True)
            if not poll_download(jid, out):
                ok = False
        except Exception as exc:  # noqa: BLE001
            print(f"[bg-anim] error {job['out']}: {exc}", flush=True)
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
