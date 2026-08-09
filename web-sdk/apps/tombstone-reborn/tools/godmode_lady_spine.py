"""God Mode AI -> Spine 4.1 host idle for THE WHITE ROOM Patient.

Public GodMode API returns sprite sheets + MP4 (native Spine export is invite-only
web UI). This adapts sheets into Spine 4.1.23 sequence skeletons that the existing
pixi-spine loader plays as animation name ``idle``.

Auth (never log the full key):
  - game-builder/.godmode-settings.json  {"apiKey":"gmd_..."}
  - or env GODMODE_API_KEY / GODMODE_TOKEN

Run:
  python tools/godmode_lady_spine.py
  python tools/godmode_lady_spine.py --action sidescrolling_idle_ffg --variant base
"""

from __future__ import annotations

import argparse
import io
import json
import mimetypes
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

APP = Path(__file__).resolve().parents[1]
REPO = APP.parents[2]
BUILDER = REPO / "game-builder"
SCENE = APP / "static" / "assets" / "sprites" / "scene"
OUT = APP / "static" / "assets" / "spines" / "lady"
RAW = APP / "tools" / "scenario_out" / "godmode_lady"
SPINE_VERSION = "4.1.23"
API_BASE = "https://www.godmodeai.co/api/generation-api/v1"

DEFAULT_ACTION = "sidescrolling_idle_ffg"
DEFAULT_VIEW = "side-scrolling"
DEFAULT_PROMPT = (
    "Pale gaunt woman in white canvas straitjacket with leather straps, "
    "seated on a plain white wooden chair, long matted black hair, hollow stare, "
    "clinical asylum patient idle, shallow breathing, three-quarter view facing left, "
    "transparent background, no Victorian gown, no veil, no hand mirror"
)
DEFAULT_NEGATIVE = (
    "victorian dress, lace veil, gothic gown, floating, weapon, text, logo, UI, "
    "extra limbs, deformed hands, busy background"
)


def mask_key(k: str) -> str:
    k = str(k or "")
    return (k[:6] + "..." + k[-4:]) if len(k) > 12 else ("set" if k else "missing")


def load_api_key() -> str:
    for env in ("GODMODE_API_KEY", "GODMODE_TOKEN"):
        v = (os.environ.get(env) or "").strip()
        if v:
            return v
    settings = BUILDER / ".godmode-settings.json"
    if settings.exists():
        try:
            j = json.loads(settings.read_text(encoding="utf-8"))
            v = (j.get("apiKey") or j.get("token") or "").strip()
            if v:
                return v
        except Exception as e:
            raise SystemExit(f"could not read {settings}: {e}") from e
    legacy = REPO / "godmodeapi.txt"
    if legacy.exists():
        m = re.search(r"gmd_[a-f0-9]+", legacy.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return m.group(0)
    raise SystemExit(
        "No GodMode API key. Set game-builder/.godmode-settings.json "
        '{"apiKey":"gmd_..."} or env GODMODE_API_KEY.'
    )


def robust_write(path: Path, data: bytes, attempts: int = 8) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    for i in range(attempts):
        try:
            with open(tmp, "wb") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
            return
        except OSError:
            time.sleep(0.6 * (i + 1))
    raise SystemExit(f"could not write {path} (file lock)")


def api_json(method: str, path: str, key: str, body: dict | None = None, timeout: int = 120):
    url = API_BASE + path
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Accept", "application/json")
    if body is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return resp.status, json.loads(raw.decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", "ignore")[:800]
        raise SystemExit(f"GodMode {method} {path} -> HTTP {e.code}: {err}") from e


def upload_file(key: str, file_path: Path) -> str:
    boundary = f"----godmode{int(time.time() * 1000)}"
    filename = file_path.name
    mime = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    file_bytes = file_path.read_bytes()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file_upload"; filename="{filename}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(API_BASE + "/files/file/local", data=body, method="POST")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            j = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"upload failed HTTP {e.code}: {e.read()[:400]}") from e
    url = j.get("url")
    if not url:
        raise SystemExit(f"upload missing url: {j}")
    print(f"[upload] ok -> ...{url[-48:]}", flush=True)
    return url


def download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = resp.read()
    robust_write(dest, data)
    print(f"[dl] {dest.name} ({len(data)} bytes)", flush=True)
    return dest


def poll_request(key: str, kind: str, request_id: str, timeout_s: int = 320, interval: float = 3.0):
    deadline = time.time() + timeout_s
    status_path = f"/{kind}/requests/{request_id}/status"
    result_path = f"/{kind}/requests/{request_id}"
    while time.time() < deadline:
        _, st = api_json("GET", status_path, key, timeout=60)
        status = (st.get("status") or st.get("state") or "").upper()
        print(f"[{kind}] status={status or '?'}", flush=True)
        if status in ("COMPLETED", "COMPLETE", "SUCCESS", "DONE"):
            _, result = api_json("GET", result_path, key, timeout=60)
            return result
        if status in ("FAILED", "ERROR", "JOB_ERROR"):
            raise SystemExit(f"{kind} failed: {st}")
        if st.get("sprite_sheet_url") or st.get("clean_sprite_sheet_url") or st.get("generation_url"):
            return st
        time.sleep(interval)
    _, result = api_json("GET", result_path, key, timeout=60)
    return result


def generate_sprite(key: str, image_url: str, action_id: str, view_type: str, prompts: dict) -> dict:
    body = {
        "image_url": image_url,
        "action_id": action_id,
        "view_type": view_type,
        "auto_repose": False,
        "positive_prompt": prompts["positive"],
        "negative_prompt": prompts["negative"],
    }
    code, data = api_json("POST", "/sprite", key, body, timeout=120)
    print(f"[sprite] submit HTTP {code}", flush=True)
    if data.get("sprite_sheet_url"):
        return data
    rid = data.get("request_id")
    if not rid:
        raise SystemExit(f"sprite submit missing request_id: {data}")
    return poll_request(key, "sprite", rid)


def remove_bg(key: str, image_url: str, num_frames: int | None = None) -> dict:
    body: dict = {"image_url": image_url, "model": "BEN"}
    if num_frames:
        body["num_frames"] = int(num_frames)
    code, data = api_json("POST", "/bg-removal", key, body, timeout=120)
    print(f"[bg] submit HTTP {code}", flush=True)
    if data.get("clean_sprite_sheet_url"):
        return data
    rid = data.get("request_id")
    if not rid:
        raise SystemExit(f"bg-removal missing request_id: {data}")
    return poll_request(key, "bg-removal", rid)


def slice_grid(sheet: Image.Image, cols: int, rows: int) -> list[Image.Image]:
    W, H = sheet.size
    cw, ch = W // cols, H // rows
    frames = []
    for r in range(rows):
        for c in range(cols):
            tile = sheet.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch))
            if tile.split()[3].getbbox():
                frames.append(tile)
    return frames


def slice_by_bboxes(sheet: Image.Image, boxes: list) -> list[Image.Image]:
    frames = []
    for b in boxes:
        if isinstance(b, dict):
            if "x1" in b and "x0" in b:
                x, y = int(b["x0"]), int(b["y0"])
                w, h = int(b["x1"]) - x, int(b["y1"]) - y
            else:
                x = int(b.get("x", b.get("left", 0)))
                y = int(b.get("y", b.get("top", 0)))
                w = int(b.get("w", b.get("width", 0)))
                h = int(b.get("h", b.get("height", 0)))
        elif isinstance(b, (list, tuple)) and len(b) >= 4:
            x, y, w, h = map(int, b[:4])
        else:
            continue
        if w <= 1 or h <= 1:
            continue
        frames.append(sheet.crop((x, y, x + w, y + h)))
    return frames


def guess_grid(sheet: Image.Image) -> tuple[int, int]:
    """Pick a cols×rows grid that maximizes non-empty cells (GodMode often uses 3×7 / 4×N)."""
    W, H = sheet.size
    alpha = sheet.split()[3]
    best = (4, max(1, H // max(1, W // 4)))
    best_score = -1
    for cols in (3, 4, 5, 6, 8, 2):
        if W % cols != 0:
            continue
        for rows in (7, 6, 8, 5, 4, 3, 2, 1, 9, 12):
            if H % rows != 0:
                continue
            cw, ch = W // cols, H // rows
            if cw < 32 or ch < 32:
                continue
            nonempty = 0
            for r in range(rows):
                for c in range(cols):
                    tile = alpha.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch))
                    # mean alpha proxy via histogram
                    hist = tile.histogram()
                    if sum(hist[16:]) > (cw * ch * 0.02):
                        nonempty += 1
            score = nonempty * 1000 - abs(nonempty - 21)  # prefer ~21-frame sheets
            if nonempty >= 4 and score > best_score:
                best_score = score
                best = (cols, rows)
    return best


def trim_frame(im: Image.Image, pad: int = 2) -> Image.Image:
    bb = im.split()[3].getbbox()
    if not bb:
        return im
    x0, y0, x1, y1 = bb
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(im.width, x1 + pad)
    y1 = min(im.height, y1 + pad)
    return im.crop((x0, y0, x1, y1))


def extract_frames_from_sheet(sheet_path: Path, bg_meta: dict | None) -> list[Image.Image]:
    sheet = Image.open(sheet_path).convert("RGBA")
    boxes = None
    if bg_meta:
        boxes = bg_meta.get("bounding_boxes") or bg_meta.get("bboxes") or bg_meta.get("frames")
    if boxes:
        frames = [f for f in slice_by_bboxes(sheet, boxes) if f.width >= 64 and f.height >= 96]
        if frames:
            print(f"[slice] {len(frames)} frames via bounding_boxes", flush=True)
            return frames
    cols, rows = guess_grid(sheet)
    frames = slice_grid(sheet, cols, rows)
    print(f"[slice] grid {cols}x{rows} -> {len(frames)} frames (sheet {sheet.size})", flush=True)
    frames = [f for f in frames if f.width >= 64 and f.height >= 96]
    return frames if len(frames) >= 2 else [sheet]


def normalize_frames(frames: list[Image.Image], target_h: int) -> tuple[list[Image.Image], int, int]:
    norm: list[Image.Image] = []
    dw = dh = 0
    for fr in frames:
        fr = trim_frame(fr.convert("RGBA"))
        if fr.height < 8:
            continue
        scale = target_h / fr.height
        nw = max(1, round(fr.width * scale))
        nh = max(1, round(fr.height * scale))
        pw = max(1, round(nw * 0.55))
        ph = max(1, round(nh * 0.55))
        packed = fr.resize((pw, ph), Image.LANCZOS)
        packed.info["display"] = (nw, nh)
        norm.append(packed)
        dw, dh = nw, nh
    if not norm:
        raise SystemExit("no usable frames after normalize")
    return norm, dw, dh


def build_sequence_skel(prefix: str, count: int, display_w: int, display_h: int, fps: float = 12.0):
    delay = round(1.0 / fps, 4)
    duration = round(count * delay, 4)
    attach_name = f"{prefix}/"
    slot_name = f"{prefix}/00"
    return {
        "skeleton": {
            "hash": f"godmode-{prefix}",
            "spine": SPINE_VERSION,
            "x": round(-display_w / 2, 2),
            "y": round(-display_h / 2, 2),
            "width": float(display_w),
            "height": float(display_h),
            "images": "",
            "audio": "",
        },
        "bones": [{"name": "root"}],
        "slots": [{"name": slot_name, "bone": "root", "attachment": attach_name}],
        "skins": [
            {
                "name": "default",
                "attachments": {
                    slot_name: {
                        attach_name: {
                            "width": display_w,
                            "height": display_h,
                            "sequence": {"count": count, "start": 0, "digits": 2},
                        }
                    }
                },
            }
        ],
        "animations": {
            "idle": {
                "attachments": {
                    "default": {
                        slot_name: {
                            attach_name: {
                                "sequence": [
                                    {"mode": "loop", "delay": delay},
                                    {"time": duration, "mode": "loop"},
                                ]
                            }
                        }
                    }
                }
            }
        },
    }


def write_atlas_and_skel(built: dict[str, tuple], fps: float) -> None:
    """built[prefix] = (packed_frames, display_w, display_h, json_name)"""
    all_regions: list[dict] = []
    for prefix, (frames, _dw, _dh, _jn) in built.items():
        for i, fr in enumerate(frames):
            all_regions.append({"name": f"{prefix}/{i:02d}", "img": fr, "prefix": prefix})

    pad = 2
    x = pad
    y = pad
    row_h = 0
    W = 0
    max_w = 4096
    for r in all_regions:
        w, h = r["img"].size
        if x + w + pad > max_w:
            x = pad
            y += row_h + pad
            row_h = 0
        r["ax"], r["ay"] = x, y
        x += w + pad
        row_h = max(row_h, h)
        W = max(W, x)
    H = y + row_h + pad
    page = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for r in all_regions:
        page.alpha_composite(r["img"], (r["ax"], r["ay"]))

    OUT.mkdir(parents=True, exist_ok=True)
    for name in ("lady.json", "lady_bonus.json", "lady.atlas", "lady.webp"):
        p = OUT / name
        if p.exists():
            bak = OUT / f"{name}.pre_godmode.bak"
            if not bak.exists():
                try:
                    bak.write_bytes(p.read_bytes())
                except OSError:
                    pass

    buf = io.BytesIO()
    page.save(buf, "WEBP", lossless=True, quality=100)
    robust_write(OUT / "lady.webp", buf.getvalue())

    lines = ["lady.webp", f"size:{W},{H}", "filter:Linear,Linear", "scale:1"]
    for r in all_regions:
        w, h = r["img"].size
        lines.append(r["name"])
        lines.append(f"bounds:{r['ax']},{r['ay']},{w},{h}")
    robust_write(OUT / "lady.atlas", ("\n".join(lines) + "\n").encode("utf-8"))
    print(f"[atlas] lady.webp {W}x{H} regions={len(all_regions)}", flush=True)

    for prefix, (frames, dw, dh, json_name) in built.items():
        skel = build_sequence_skel(prefix, len(frames), dw, dh, fps=fps)
        robust_write(OUT / json_name, json.dumps(skel).encode("utf-8"))
        print(f"[skel] {json_name} frames={len(frames)} display={dw}x{dh}", flush=True)


def run_variant(key: str, src: Path, action: str, view: str, prompts: dict, skip_bg: bool) -> list[Image.Image]:
    print(f"[variant] src={src.name} action={action} view={view}", flush=True)
    image_url = upload_file(key, src)
    result = generate_sprite(key, image_url, action, view, prompts)
    sheet_url = result.get("sprite_sheet_url") or result.get("spritesheet_url")
    video_url = result.get("generation_url") or result.get("video_url")
    if video_url:
        try:
            download(video_url, RAW / f"{src.stem}_preview.mp4")
        except Exception as e:
            print(f"[dl] preview skipped: {e}", flush=True)
    if not sheet_url:
        raise SystemExit(f"no sprite_sheet_url in result keys={list(result.keys())}")
    sheet_path = download(sheet_url, RAW / f"{src.stem}_sheet.png")
    bg_meta = None
    if not skip_bg:
        try:
            bg_meta = remove_bg(key, sheet_url)
            robust_write(
                RAW / f"{src.stem}_bg_meta.json",
                json.dumps(bg_meta).encode("utf-8"),
            )
            clean = bg_meta.get("clean_sprite_sheet_url")
            if clean:
                sheet_path = download(clean, RAW / f"{src.stem}_sheet_clean.png")
        except SystemExit as e:
            print(f"[bg] skipped ({e})", flush=True)
            bg_meta = None
            # Resume from a prior meta if present (credits / 413 failures).
            meta_path = RAW / f"{src.stem}_bg_meta.json"
            if meta_path.exists():
                try:
                    bg_meta = json.loads(meta_path.read_text(encoding="utf-8"))
                    print(f"[bg] loaded cached meta ({len(bg_meta.get('bounding_boxes') or [])} boxes)", flush=True)
                except Exception:
                    bg_meta = None
    return extract_frames_from_sheet(sheet_path, bg_meta)


def main() -> None:
    ap = argparse.ArgumentParser(description="GodMode AI idle -> Spine 4.1 lady host")
    ap.add_argument("--action", default=os.environ.get("GODMODE_ACTION", DEFAULT_ACTION))
    ap.add_argument("--view", default=os.environ.get("GODMODE_VIEW", DEFAULT_VIEW))
    ap.add_argument("--variant", choices=("base", "bonus", "both"), default="both")
    ap.add_argument("--skip-bg", action="store_true")
    ap.add_argument("--fps", type=float, default=12.0)
    ap.add_argument("--target-h", type=int, default=1300)
    args = ap.parse_args()

    # Hard stop: broken GodMode sidescroll idle destroyed the White Room Patient.
    # Restore path is *.pre_godmode.bak — do not overwrite until clean masters exist.
    guard = RAW / "DO_NOT_REGENERATE.txt"
    if guard.is_file() and os.environ.get("FORCE_GODMODE_LADY", "").strip().lower() not in {
        "1",
        "true",
        "yes",
    }:
        raise SystemExit(
            f"REFUSING godmode_lady_spine: {guard} present. "
            "Set FORCE_GODMODE_LADY=1 only after clean assets-raw/lady_masters/ exist."
        )

    key = load_api_key()
    print(f"[auth] key={mask_key(key)} base={API_BASE}", flush=True)
    RAW.mkdir(parents=True, exist_ok=True)

    prompts = {"positive": DEFAULT_PROMPT, "negative": DEFAULT_NEGATIVE}
    jobs: list[tuple[str, Path, str]] = []
    if args.variant in ("base", "both"):
        jobs.append(("base_idle", SCENE / "lady_character.png", "lady.json"))
    if args.variant in ("bonus", "both"):
        bonus = SCENE / "lady_bonus.png"
        if bonus.exists():
            jobs.append(("bonus_idle", bonus, "lady_bonus.json"))
        elif args.variant == "bonus":
            raise SystemExit(f"missing {bonus}")

    built: dict[str, tuple] = {}
    for prefix, src, json_name in jobs:
        if not src.exists():
            raise SystemExit(f"missing character sprite: {src}")
        frames = run_variant(key, src, args.action, args.view, prompts, skip_bg=args.skip_bg)
        packed, dw, dh = normalize_frames(frames, args.target_h)
        built[prefix] = (packed, dw, dh, json_name)

    # Bonus without a separate gen: same atlas regions as base (no duplicate pack).
    reuse_bonus_from_base = False
    if "bonus_idle" not in built and "base_idle" in built:
        reuse_bonus_from_base = True
        print("[bonus] lady_bonus.json will reference base_idle frames", flush=True)

    write_atlas_and_skel(built, fps=args.fps)

    if reuse_bonus_from_base:
        frames, dw, dh, _ = built["base_idle"]
        skel = build_sequence_skel("base_idle", len(frames), dw, dh, fps=args.fps)
        skel["skeleton"]["hash"] = "godmode-bonus-via-base"
        robust_write(OUT / "lady_bonus.json", json.dumps(skel).encode("utf-8"))
        print(f"[skel] lady_bonus.json (shared base_idle) frames={len(frames)}", flush=True)

    print("[done] installed ->", OUT, flush=True)


if __name__ == "__main__":
    main()
