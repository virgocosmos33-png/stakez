"""Generate THE WHITE ROOM win-celebration stills + loops via Scenario.

Concept: THE PATIENT arc (top symbol — black hair, force vest).
  t2 INTAKE    — brought in, vested, crying
  t3 RESTRAINT — tests the straps, disbelief
  t4 STRUGGLE  — fighting the vest
  t5 BREAKOUT  — vest breaks free
  t6 SCRATCH   — clawing the padded walls
  t7 WHITEOUT  — room obliterates to white

Each tier: txt2img still (character-referenced) → Kling img2video loop.
Run:
  CELEB_LIVE=1 CELEB_FORCE=1 python tools/gen_celeb_white_room.py
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
# Locked Patient look (force vest / black hair) — chroma still used as face+costume ref
CHAR_REF = HERE.parent / "assets-raw" / "lady_video" / "kling_credit_base_f0.png"
IMG_MODEL = os.environ.get("CELEB_IMG_MODEL", "model_openai-gpt-image-2")
VID_MODEL = os.environ.get("CELEB_VID_MODEL", "model_kling-v3-i2v-pro")

NEG = (
    "NO purple, NO amethyst, NO Victorian parlor, NO ornate gold frame, "
    "NO green ghost mist, NO sheet ghost, NO gothic candlelight, NO Madam Mirror branding, "
    "NO text, NO letters, NO logos, NO watermark, NO title card."
)
CHAR = (
    "Same young woman every shot: pale gaunt skin, sunken dark eyes, long messy stringy black hair, "
    "barefoot. White institutional force-vest / straitjacket gown with thick tan leather straps and "
    "metal buckles pinning her arms (unless the beat says the vest is off). "
)
ROOM = (
    "Setting: narrow padded isolation cell, white tufted pad walls and ceiling, "
    "single square cold fluorescent ceiling light, clinical psychological horror, "
    "photoreal cinematic 16:9. Palette pure white / silver / cold grey / faint dried blood only. "
)
STYLE = "THE WHITE ROOM slot win-celebration key art. " + CHAR + ROOM + NEG

# Unique tier concepts (t2…t7)
TIERS = {
    2: {
        "title": "INTAKE",
        "still": (
            STYLE
            + "INTAKE: she has just been brought into the padded cell. Force vest ON, straps tight. "
            "She sits or stands near a plain white institutional chair, crying, head bowed, "
            "tears on pale cheeks, hair in her face. Metal door frame barely visible at the edge. "
            "Cold fluorescent hum. Helpless, newly admitted. No gore."
        ),
        "motion": (
            "She cries softly, shoulders tremble, a tear falls, hair shifts slightly, "
            "fluorescent tube flickers once, slow almost-static camera. Force vest stays on. "
            "No text, no purple, no green mist."
        ),
    },
    3: {
        "title": "RESTRAINT",
        "still": (
            STYLE
            + "RESTRAINT: force vest still ON. She tests the leather straps — disbelief, not rage. "
            "Looks toward the observation glass / camera with wet eyes. Breath fog on glass optional. "
            "Straps taut across her torso, knuckles white. Quiet dread. No gore."
        ),
        "motion": (
            "She pulls once against the straps, straps creak, she looks up at the glass, "
            "shallow breathing, fluorescent flicker, slow push-in. Vest stays on. "
            "No text, no purple, no green mist."
        ),
    },
    4: {
        "title": "STRUGGLE",
        "still": (
            STYLE
            + "STRUGGLE: force vest ON, full fight. She thrashes against the straps, chair scrapes, "
            "jaw clenched, tears and anger, hair wild. Leather straps strain, buckle glints. "
            "Padded walls close in. Violent effort, still trapped. No gore, no broken bones."
        ),
        "motion": (
            "She violently struggles in the force vest, shoulders wrench, chair scrapes the floor, "
            "hair flies, straps pull taut, fluorescent strobe flicker, tense cinematic motion. "
            "Vest stays on. No text, no purple."
        ),
    },
    5: {
        "title": "BREAKOUT",
        "still": (
            STYLE
            + "BREAKOUT: the force vest is coming OFF — one leather strap snapped loose, buckle open, "
            "vest half-peeled from her shoulders. She is mid-escape, face fierce, overexposed white "
            "light spike behind her. Vest falling. Freedom hitting. No gore."
        ),
        "motion": (
            "A strap snaps free, the force vest peels off her shoulders and drops toward the floor, "
            "harsh white light blooms, she gasps free, slow-motion cinematic beat. "
            "No text, no purple, no green mist."
        ),
    },
    6: {
        "title": "SCRATCH",
        "still": (
            STYLE
            + "SCRATCH: force vest GONE — torn white gown only, arms free. She presses both palms "
            "flat into the tufted padded wall, leaning her forehead against it, exhausted and numb. "
            "Long faint dark score-lines already mark the pad behind her hands (old wall wear, not injury). "
            "Quiet aftermath. Soft clinical light. No violence, no blood, no wounds."
        ),
        "motion": (
            "She slowly drags her fingertips down the padded wall leaving faint dark score lines in the foam, "
            "head bowed, breathing heavy, camera slow push-in on the wall marks, fluorescent flicker. "
            "No vest. No blood. No text, no purple."
        ),
    },
    7: {
        "title": "WHITEOUT",
        "still": (
            STYLE
            + "WHITEOUT: padded cell flooded with overexposed pure white light. Her silhouette "
            "fades into the white bloom, pad seams barely visible as silver edges, "
            "maximum clinical overexposure. Almost nothing left but white. No text in frame. "
            "No violence, no blood."
        ),
        "motion": (
            "Entire padded cell floods with overexposed white light; her silhouette fades into the bloom; "
            "rising soft white wash; silver pad edges vanish into whiteout. No purple gothic."
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
        try:
            tr = s.request("GET", f"/assets/{asset_id}/download")
            url = (tr.get("url") or tr.get("downloadUrl") or "").strip()
        except Exception:  # noqa: BLE001
            url = ""
    if not url:
        raise RuntimeError(f"no url for {asset_id}: {meta}")
    urllib.request.urlretrieve(url, dest)
    print(f"[celeb-wr] downloaded {dest} ({dest.stat().st_size})", flush=True)


def gen_still(n: int, prompt: str, out_png: Path, ref_id: str | None) -> Path:
    if out_png.exists() and out_png.stat().st_size > 50_000 and not _force():
        print(f"[celeb-wr] keep still {out_png}", flush=True)
        return out_png
    body: dict = {
        "prompt": prompt,
        "numOutputs": 1,
        "width": 1280,
        "height": 720,
        "quality": "medium",
        "background": "opaque",
    }
    if ref_id:
        body["referenceImages"] = [ref_id]
    job = s.request("POST", f"/generate/custom/{IMG_MODEL}", body)
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
                "logos, watermarks, text, purple, green mist, victorian gothic"
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

    if os.environ.get("CELEB_LIVE") != "1":
        print("[celeb-wr] CELEB_LIVE!=1 — skip live Scenario (assemble/wire handle wiring)", flush=True)
        return 0

    ref_id = None
    if CHAR_REF.is_file():
        ref_id = upload(CHAR_REF)
        print(f"[celeb-wr] character ref {CHAR_REF.name} -> {ref_id}", flush=True)
    else:
        print(f"[celeb-wr] WARN: missing character ref {CHAR_REF}", flush=True)

    only = {
        int(x.strip())
        for x in (os.environ.get("CELEB_ONLY") or "").split(",")
        if x.strip().isdigit()
    }
    for n, spec in TIERS.items():
        if only and n not in only:
            print(f"[celeb-wr] skip t{n} (CELEB_ONLY)", flush=True)
            continue
        out_dir = CELEB / f"celeb_t{n}"
        out_dir.mkdir(parents=True, exist_ok=True)
        still_png = out_dir / f"celeb_t{n}_still.png"
        out_mp4 = out_dir / f"celeb_t{n}.mp4"
        webp = CELEB / f"celeb_t{n}.webp"

        print(f"[celeb-wr] === t{n} {spec['title']} ===", flush=True)
        try:
            gen_still(n, spec["still"], still_png, ref_id)
            from PIL import Image

            Image.open(still_png).convert("RGB").save(webp, "WEBP", quality=90, method=6)
            # also mirror into assets/ source tree
            src_webp = HERE.parent / "assets" / "sprites" / "celeb" / f"celeb_t{n}.webp"
            src_webp.parent.mkdir(parents=True, exist_ok=True)
            Image.open(still_png).convert("RGB").save(src_webp, "WEBP", quality=90, method=6)
            print(f"[celeb-wr] poster {webp.name}", flush=True)

            image_id = upload(still_png)
            gen_video(n, image_id, spec["motion"], out_mp4)
            src_mp4_dir = HERE.parent / "assets" / "sprites" / "celeb" / f"celeb_t{n}"
            src_mp4_dir.mkdir(parents=True, exist_ok=True)
            src_mp4 = src_mp4_dir / f"celeb_t{n}.mp4"
            src_mp4.write_bytes(out_mp4.read_bytes())
            if _is_duplicate_of_whiteout(out_mp4):
                raise RuntimeError(f"t{n} video is still duplicate of celeb_whiteout — abort")
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            if "429" in msg or "RateLimit" in msg or "Too Many Requests" in msg:
                print(f"[celeb-wr] rate-limited on t{n}: {exc}", flush=True)
                return 1
            print(f"[celeb-wr] t{n} ERROR: {exc}", flush=True)
            return 1

    print("[celeb-wr] all tiers generated", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
