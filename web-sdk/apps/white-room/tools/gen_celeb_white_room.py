"""Generate THE WHITE ROOM win-celebration stills + loops via Scenario.



Each tier gets a UNIQUE clinical still (txt2img) then a UNIQUE img2video loop.

Never paste one whiteout clip across t2–t7. Old gothic Madam Mirror art is

overwritten.

Run via DramaStudioMCP regenerate_assets scope=celebration (FORCE=1 by default
when env CELEB_FORCE unset — set CELEB_FORCE=0 to keep existing unique files).
"""
from __future__ import annotations

import hashlib
import os
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

HERE = Path(__file__).resolve().parent
CELEB = HERE.parent / "static" / "assets" / "sprites" / "celeb"
IMG_MODEL = os.environ.get("CELEB_IMG_MODEL", "model_openai-gpt-image-2")
VID_MODEL = os.environ.get("CELEB_VID_MODEL", "model_kling-v3-i2v-pro")

NEG = (
    "NO purple, NO amethyst, NO Victorian parlor, NO ornate gold frame, "
    "NO green ghost mist, NO sheet ghost, NO gothic candlelight, NO Madam Mirror branding."
)
STYLE = (
    "THE WHITE ROOM slot win-celebration key art. Clinical psychological horror. "
    "Palette: pure white, silver, cold grey, fluorescent cyan-white, faint dried-blood #6b2a28 only. "
    "Padded isolation cell / psychiatric ward. Photoreal cinematic 16:9 still. " + NEG
)

# Unique tier concepts (t2…t7) — never duplicate one whiteout across all six.
TIERS = {
    2: {
        "title": "Fluorescent Strobe Intake",
        "still": (
            STYLE
            + "Fluorescent strobe intake: white padded cell under harsh flickering tubes, "
            "intake desk with metal clipboard, pale patient in thin hospital gown standing "
            "under stuttering white light, silver reflections, clinical dread."
        ),
        "motion": (
            "Harsh fluorescent tubes strobe and flicker; cold white light pulses across "
            "padded walls; patient silhouette trembles under intake lights; camera slow push-in. "
            "No purple, no green mist, no Victorian furniture."
        ),
    },
    3: {
        "title": "Patient 404 Restraint Break",
        "still": (
            STYLE
            + "Patient 404 restraint break: pale figure stamped 404 on forehead in white "
            "straitjacket, leather medical straps snapping loose, padded white walls, "
            "silver buckle glints, institutional horror."
        ),
        "motion": (
            "Leather restraint straps snap and whip; patient strains forward; fluorescent "
            "hum flicker; padded wall compresses; slow cinematic tension. No purple, no gothic."
        ),
    },
    4: {
        "title": "Observation Glass Shatter",
        "still": (
            STYLE
            + "Observation glass shatter: two-way observation window exploding into shards "
            "over a sterile white observation room, silver glass fragments frozen mid-air, "
            "frost cracks, cold clinical light."
        ),
        "motion": (
            "Observation glass cracks with frost then shatters outward; ceramic dust and "
            "silver shards fly; sterile white room beyond; slow-motion impact. No green ghosts."
        ),
    },
    5: {
        "title": "Her Side Empty Chair",
        "still": (
            STYLE
            + "Her Side empty chair / IT KNOWS YOU: lone white metal institutional chair "
            "slightly off-center in a clean padded cell, solid coherent legs, recently vacated "
            "seat dent, graffiti REMEMBER? / WHO AM I? left and IT KNOWS YOU! / NO ESCAPE / "
            "THEY WATCH + staring eye right, CCTV red LED, perfectly straight tiles, "
            "NO gurney, NO ghost limbs, NO purple overlays, no people, no logos."
        ),
        "motion": (
            "Slow cinematic drift toward empty chair; fluorescent hum flicker; cold clinical "
            "light shift; CCTV LED glow; dust motes; geometry locked stable. "
            "No ghost limbs, no purple overlays, no warped tiles, no purple gothic."
        ),
    },
    6: {
        "title": "Memory Reset Dissolve",
        "still": (
            STYLE
            + "Memory Reset dissolve: empty white institutional metal chair centered in a clean "
            "padded isolation cell, perfectly straight tufted wall panels and floor tiles, soft "
            "fluorescent overexposure bloom on the back wall like CRT memory wipe, CCTV dome, "
            "graffiti REMEMBER? / IT KNOWS YOU, NO gurney, NO bed rails, NO people, no logos."
        ),
        "motion": (
            "Slow cinematic push-in; empty chair stays solid; fluorescent hum flicker; soft white "
            "memory-wipe bloom pulses on back wall; dust motes; geometry locked stable. "
            "No gurney, no phantom rails, no warped tiles, no Victorian, no green mist."
        ),
    },
    7: {
        "title": "Padded Cell Whiteout",
        "still": (
            STYLE
            + "Padded cell WHITEOUT: entire isolation cell flooded with overexposed pure white "
            "light, padded walls barely visible as silver edges, silhouettes dissolving to ash, "
            "maximum clinical obliteration."
        ),
        "motion": (
            "Entire padded cell floods with overexposed white light; silhouettes dissolve; "
            "rising white-noise bloom; silver edges vanish into whiteout. No purple gothic."
        ),
    },
}


def _md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _force() -> bool:
    v = os.environ.get("CELEB_FORCE", os.environ.get("FORCE", "1")).strip().lower()
    return v not in ("0", "false", "no")


def _is_duplicate_of_whiteout(mp4: Path) -> bool:
    wo = CELEB / "celeb_whiteout.mp4"
    if not mp4.is_file() or not wo.is_file():
        return False
    if mp4.stat().st_size != wo.stat().st_size:
        return False
    return _md5(mp4) == _md5(wo)


def upload(path: Path) -> str:
    import base64
    import mimetypes

    mime = mimetypes.guess_type(str(path))[0] or "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode()
    resp = s.request("POST", "/assets", {"image": f"data:{mime};base64,{b64}", "name": path.name})
    aid = resp.get("asset", {}).get("id") or resp.get("assetId")
    if not aid:
        raise SystemExit(f"upload failed: {resp}")
    return aid


def poll_job(jid: str, label: str, max_wait: int = 240) -> list[str]:
    for _ in range(max_wait // 2):
        time.sleep(2)
        st = s.request("GET", f"/jobs/{jid}")
        j = st.get("job", st)
        status = j.get("status")
        if status in ("success", "completed", "done"):
            ids = list((j.get("metadata") or {}).get("assetIds") or [])
            if not ids:
                for a in j.get("assets") or []:
                    if isinstance(a, dict) and a.get("id"):
                        ids.append(a["id"])
                    elif isinstance(a, str):
                        ids.append(a)
            return ids
        if status in ("failure", "failed", "error", "canceled"):
            raise RuntimeError(f"{label} failed: {j}")
    raise TimeoutError(f"{label} timed out job={jid}")


def download_asset(asset_id: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    meta = s.request("GET", f"/assets/{asset_id}")
    asset = meta.get("asset", meta)
    url = asset.get("url") or asset.get("downloadUrl")
    if not url:
        # transform endpoint sometimes needed
        try:
            tr = s.request("GET", f"/assets/{asset_id}/download")
            url = (tr.get("url") or tr.get("downloadUrl") or "").strip()
        except Exception:  # noqa: BLE001
            url = ""
    if not url:
        raise RuntimeError(f"no url for {asset_id}: {meta}")
    urllib.request.urlretrieve(url, dest)
    print(f"[celeb-wr] downloaded {dest} ({dest.stat().st_size})", flush=True)


def gen_still(n: int, prompt: str, out_png: Path) -> Path:
    if out_png.exists() and out_png.stat().st_size > 50_000 and not _force():
        print(f"[celeb-wr] keep still {out_png}", flush=True)
        return out_png
    job = s.request(
        "POST",
        f"/generate/custom/{IMG_MODEL}",
        {
            "prompt": prompt,
            "numOutputs": 1,
            "width": 1280,
            "height": 720,
            "quality": "medium",
            "background": "opaque",
        },
    )
    jid = (job.get("job") or job).get("jobId") or (job.get("job") or job).get("id")
    print(f"[celeb-wr] still t{n} job {jid}", flush=True)
    ids = poll_job(jid, f"still-t{n}")
    if not ids:
        raise RuntimeError(f"still t{n}: no asset ids")
    download_asset(ids[0], out_png)
    return out_png


def gen_video(n: int, image_id: str, motion: str, out_mp4: Path) -> Path:
    if (
        out_mp4.exists()
        and out_mp4.stat().st_size > 100_000
        and not _force()
        and not _is_duplicate_of_whiteout(out_mp4)
    ):
        print(f"[celeb-wr] keep video {out_mp4}", flush=True)
        return out_mp4
    # Kling expects startImage; Seedance / older i2v use image.
    if "kling" in VID_MODEL.lower():
        body = {
            "startImage": image_id,
            "prompt": motion,
            "duration": "5",
            "aspectRatio": "16:9",
            "cfgScale": 0.65,
            "generateAudio": False,
            "negativePrompt": (
                "warped tiles, phantom rails, hospital gurney, floating limbs, "
                "logos, watermarks, purple, green mist, victorian gothic"
            ),
        }
    else:
        body = {
            "image": image_id,
            "prompt": motion,
            "resolution": "720p",
            "duration": 5,
        }
    job = s.request("POST", f"/generate/custom/{VID_MODEL}", body)
    jid = (job.get("job") or job).get("jobId") or (job.get("job") or job).get("id")
    print(f"[celeb-wr] video t{n} job {jid}", flush=True)
    ids = poll_job(jid, f"video-t{n}", max_wait=400)
    if not ids:
        raise RuntimeError(f"video t{n}: no asset ids")
    download_asset(ids[0], out_mp4)
    return out_mp4


def main() -> int:
    if os.environ.get("SKIP_GEN") == "1":
        print("[celeb-wr] SKIP_GEN=1 — wire only", flush=True)
        return 0

    CELEB.mkdir(parents=True, exist_ok=True)
    print(f"[celeb-wr] FORCE={_force()} img={IMG_MODEL} vid={VID_MODEL}", flush=True)

    # Live Scenario gen is opt-in (CELEB_LIVE=1). Default path uses assemble + wire
    # so regenerate_assets still works through rate limits with unique clinical masters.
    if os.environ.get("CELEB_LIVE") != "1":
        print("[celeb-wr] CELEB_LIVE!=1 — skip live Scenario (assemble/wire handle wiring)", flush=True)
        return 0

    for n, spec in TIERS.items():
        out_dir = CELEB / f"celeb_t{n}"
        out_dir.mkdir(parents=True, exist_ok=True)
        still_png = out_dir / f"celeb_t{n}_still.png"
        out_mp4 = out_dir / f"celeb_t{n}.mp4"
        webp = CELEB / f"celeb_t{n}.webp"

        print(f"[celeb-wr] === t{n} {spec['title']} ===", flush=True)
        try:
            gen_still(n, spec["still"], still_png)
            from PIL import Image

            Image.open(still_png).convert("RGB").save(webp, "WEBP", quality=90, method=6)
            print(f"[celeb-wr] poster {webp.name}", flush=True)

            image_id = upload(still_png)
            gen_video(n, image_id, spec["motion"], out_mp4)
            if _is_duplicate_of_whiteout(out_mp4):
                raise RuntimeError(f"t{n} video is still duplicate of celeb_whiteout — abort")
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            if "429" in msg or "RateLimit" in msg or "Too Many Requests" in msg:
                print(f"[celeb-wr] rate-limited — relying on assemble_celeb_white_room.py ({exc})", flush=True)
                return 0
            print(f"[celeb-wr] t{n} ERROR: {exc}", flush=True)
            return 1

    print("[celeb-wr] all tiers generated", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
