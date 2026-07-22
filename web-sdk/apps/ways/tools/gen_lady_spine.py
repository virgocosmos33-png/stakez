"""Build a PROPER cut-out Spine rig for the Lady Mirror character.

NOT a single warping mesh (the old approach the art director rejected). Instead
the flat cutout is sliced into SEPARATE PARTS — head, torso, mirror-arm, upper
skirt, lower skirt/hem, and the veil — each packed as its own atlas region and
pinned to its own bone in a hierarchy:

    root -> hips -> torso -> head -> veil
                         \-> arm (+ hand mirror)
            hips -> skirtUpper -> skirtLower

The parts overlap generously and are layered back-to-front so the seams stay
hidden, and the idle animation moves the BONES (float bob, breathing, head tilt,
mirror-arm sway, skirt cloth-sway, veil billow) — real articulation, no image
warping. First key == last key so the loop is seamless.

Base + bonus share ONE atlas (lady.webp) with prefixed regions (base_* / bonus_*)
so lady.json and lady_bonus.json can both reference lady.atlas.

Output -> static/assets/spines/lady/ (lady.webp + lady.atlas + lady.json +
lady_bonus.json).  Run:  python tools/gen_lady_spine.py
"""

from __future__ import annotations

import io
import json
import math
import os
import time
from pathlib import Path

from PIL import Image


def robust_write(path: Path, data: bytes, attempts: int = 8) -> None:
    """Write via a temp file + atomic replace, retrying through OneDrive's
    intermittent Errno 22 file locks."""
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
    raise SystemExit(f"could not write {path} (OneDrive lock)")

APP = Path(__file__).resolve().parents[1]
SCENE = APP / "static" / "assets" / "sprites" / "scene"
OUT = APP / "static" / "assets" / "spines" / "lady"
OUT.mkdir(parents=True, exist_ok=True)

SPINE_VERSION = "4.1.23"
PERIOD = 5.0          # idle loop length (s)
SAMPLES = 16          # sine samples per loop (last == first)
# pack the atlas at reduced pixel res (kept < 4096 GPU limit); attachment display
# size stays full so she renders at full size, the texture is just cheaper.
ATLAS_SCALE = 0.6

# ---------------------------------------------------------------------------
# Part layout. Boxes are (x0,y0,x1,y1) as fractions of the TRIMMED figure bbox
# (origin top-left). Pivots are (px,py) fractions — the bone's rotation centre,
# placed where the part joins its parent up the chain. Draw order is the list
# order (first = furthest back).
# ---------------------------------------------------------------------------
Part = dict  # {name, box, pivot, parent, bone_extra?}

BASE_PARTS: list[Part] = [
    {"name": "veil",       "box": (0.48, 0.02, 1.00, 0.82), "pivot": (0.60, 0.12), "parent": "head"},
    {"name": "skirtLower", "box": (0.00, 0.58, 1.00, 1.00), "pivot": (0.50, 0.63), "parent": "skirtUpper"},
    {"name": "skirtUpper", "box": (0.04, 0.35, 0.96, 0.68), "pivot": (0.50, 0.40), "parent": "hips"},
    {"name": "torso",      "box": (0.22, 0.12, 0.78, 0.42), "pivot": (0.50, 0.40), "parent": "hips"},
    {"name": "arm",        "box": (0.40, 0.40, 0.82, 0.72), "pivot": (0.55, 0.44), "parent": "torso"},
    {"name": "head",       "box": (0.26, 0.00, 0.74, 0.21), "pivot": (0.49, 0.19), "parent": "torso"},
]

BONUS_PARTS: list[Part] = [
    {"name": "veil",       "box": (0.52, 0.06, 1.00, 0.88), "pivot": (0.62, 0.14), "parent": "head"},
    {"name": "skirtLower", "box": (0.00, 0.62, 1.00, 1.00), "pivot": (0.50, 0.66), "parent": "skirtUpper"},
    {"name": "skirtUpper", "box": (0.06, 0.40, 0.94, 0.72), "pivot": (0.50, 0.44), "parent": "hips"},
    {"name": "torso",      "box": (0.28, 0.16, 0.74, 0.46), "pivot": (0.50, 0.44), "parent": "hips"},
    {"name": "arm",        "box": (0.00, 0.02, 0.46, 0.40), "pivot": (0.40, 0.30), "parent": "torso"},
    {"name": "head",       "box": (0.33, 0.02, 0.70, 0.24), "pivot": (0.50, 0.22), "parent": "torso"},
]

VARIANTS = {
    "base":  {"src": "lady_character.png", "parts": BASE_PARTS, "json": "lady.json"},
    "bonus": {"src": "lady_bonus.png",     "parts": BONUS_PARTS, "json": "lady_bonus.json"},
}

# idle bone motion — amplitude (deg unless noted), phase (fraction of loop)
MOTION = {
    "hips":       {"rotate": (0.5, 0.00)},
    "torso":      {"rotate": (0.6, 0.05), "scaleY": (0.012, 0.05)},
    "head":       {"rotate": (1.4, 0.12)},
    "arm":        {"rotate": (1.7, 0.08)},
    "skirtUpper": {"rotate": (0.9, 0.10)},
    "skirtLower": {"rotate": (1.7, 0.16)},
    "veil":       {"rotate": (2.3, 0.20)},
}
ARM_AMP_BONUS = 1.0  # raised mirror sways less


def trim_bbox(im: Image.Image) -> tuple[int, int, int, int]:
    bbox = im.split()[3].getbbox()
    if bbox is None:
        raise SystemExit("empty image")
    return bbox


def extract_parts(src: Image.Image, parts: list[Part]):
    """Crop each part box, trim to its own content, return records with the
    trimmed sub-image + geometry (all in TRIMMED-figure pixel space)."""
    fx0, fy0, fx1, fy1 = trim_bbox(src)
    fig = src.crop((fx0, fy0, fx1, fy1))
    Wt, Ht = fig.size
    records = []
    for p in parts:
        bx0, by0, bx1, by1 = p["box"]
        box = (int(bx0 * Wt), int(by0 * Ht), int(bx1 * Wt), int(by1 * Ht))
        tile = fig.crop(box)
        sub = tile.split()[3].getbbox()
        if sub is None:
            continue
        tile = tile.crop(sub)
        cw, ch = tile.size  # full-res content size -> attachment display size
        # content bbox centre in figure px
        ccx = box[0] + sub[0] + cw / 2
        ccy = box[1] + sub[1] + ch / 2
        pivx = p["pivot"][0] * Wt
        pivy = p["pivot"][1] * Ht
        # downscale the packed pixels only (display size stays cw x ch)
        aw = max(1, round(cw * ATLAS_SCALE))
        ah = max(1, round(ch * ATLAS_SCALE))
        packed = tile.resize((aw, ah), Image.LANCZOS)
        records.append({
            "name": p["name"], "parent": p["parent"], "img": packed,
            "cw": cw, "ch": ch, "ccx": ccx, "ccy": ccy, "pivx": pivx, "pivy": pivy,
        })
    return records, Wt, Ht


def pack(regions: list[dict], pad: int = 2, max_w: int = 2048):
    """Simple shelf packer. regions get 'ax','ay' assigned. Returns (W,H)."""
    x = pad
    y = pad
    row_h = 0
    W = 0
    for r in regions:
        w, h = r["img"].size
        if x + w + pad > max_w:
            x = pad
            y += row_h + pad
            row_h = 0
        r["ax"] = x
        r["ay"] = y
        x += w + pad
        row_h = max(row_h, h)
        W = max(W, x)
    H = y + row_h + pad
    return W, H


def sine_keys(amp: float, phase: float, base: float = 0.0):
    keys = []
    for i in range(SAMPLES + 1):
        t = PERIOD * i / SAMPLES
        val = base + amp * math.sin(2 * math.pi * (i / SAMPLES) + phase * 2 * math.pi)
        keys.append((round(t, 4), round(val, 4)))
    return keys


def build_skeleton(records: list[dict], Wt: int, Ht: int, prefix: str, is_bonus: bool):
    def sx(ix):  # image px -> spine world x (root at figure centre)
        return round(ix - Wt / 2, 2)

    def sy(iy):
        return round(Ht / 2 - iy, 2)

    by_name = {r["name"]: r for r in records}
    # bone world positions (spine coords) from each part's pivot
    world = {"root": (0.0, 0.0), "hips": (sx(Wt / 2), sy(Ht * 0.42))}
    for r in records:
        world[r["name"]] = (sx(r["pivx"]), sy(r["pivy"]))

    parents = {"hips": "root"}
    for r in records:
        parents[r["name"]] = r["parent"]

    def local(name):
        wx, wy = world[name]
        px, py = world[parents[name]]
        return round(wx - px, 2), round(wy - py, 2)

    # bone order: parents before children
    order = ["root", "hips", "torso", "head", "veil", "arm", "skirtUpper", "skirtLower"]
    bones = [{"name": "root"}]
    for name in order[1:]:
        if name != "hips" and name not in by_name:
            continue
        lx, ly = local(name)
        bones.append({"name": name, "parent": parents[name], "x": lx, "y": ly})

    # slots in draw order == records order (already back->front)
    slots = []
    skin_attach = {}
    for r in records:
        region = f"{prefix}_{r['name']}"
        slot = f"sl_{r['name']}"
        slots.append({"name": slot, "bone": r["name"], "attachment": region})
        bwx, bwy = world[r["name"]]
        ax = round((sx(r["ccx"])) - bwx, 2)
        ay = round((sy(r["ccy"])) - bwy, 2)
        skin_attach[slot] = {region: {"x": ax, "y": ay, "width": r["cw"], "height": r["ch"]}}

    # ---- idle animation (bone transforms only) ----
    anim_bones = {}
    # float bob on root
    root_keys = sine_keys(14.0, 0.0)
    anim_bones["root"] = {"translate": [{"time": t, "x": 0, "y": v} for t, v in root_keys]}
    for name, m in MOTION.items():
        if name not in by_name and name not in ("hips",):
            continue
        entry = {}
        if "rotate" in m:
            amp, ph = m["rotate"]
            if name == "arm" and is_bonus:
                amp = ARM_AMP_BONUS
            entry["rotate"] = [{"time": t, "value": v} for t, v in sine_keys(amp, ph)]
        if "scaleY" in m:
            amp, ph = m["scaleY"]
            entry["scale"] = [{"time": t, "x": 1.0, "y": round(v, 4)}
                              for t, v in sine_keys(amp, ph, base=1.0)]
        anim_bones[name] = entry

    return {
        "skeleton": {
            "hash": f"lady-{prefix}", "spine": SPINE_VERSION,
            "x": round(-Wt / 2, 1), "y": round(-Ht / 2, 1),
            "width": float(Wt), "height": float(Ht), "images": "", "audio": "",
        },
        "bones": bones,
        "slots": slots,
        "skins": [{"name": "default", "attachments": skin_attach}],
        "animations": {"idle": {"bones": anim_bones}},
    }


def main() -> None:
    all_regions: list[dict] = []
    variant_records = {}
    for key, cfg in VARIANTS.items():
        src = Image.open(SCENE / cfg["src"]).convert("RGBA")
        recs, Wt, Ht = extract_parts(src, cfg["parts"])
        prefix = key
        for r in recs:
            r["region"] = f"{prefix}_{r['name']}"
            all_regions.append(r)
        variant_records[key] = (recs, Wt, Ht, prefix)
        print(f"[{key}] {len(recs)} parts, figure {Wt}x{Ht}", flush=True)

    # pack every region of both variants into one atlas page
    W, H = pack(all_regions)
    page = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for r in all_regions:
        page.alpha_composite(r["img"], (r["ax"], r["ay"]))
    buf = io.BytesIO()
    page.save(buf, "WEBP", lossless=True, quality=100)
    robust_write(OUT / "lady.webp", buf.getvalue())

    # atlas
    lines = ["lady.webp", f"size:{W},{H}", "filter:Linear,Linear", "scale:1"]
    for r in all_regions:
        w, h = r["img"].size
        lines.append(r["region"])
        lines.append(f"bounds:{r['ax']},{r['ay']},{w},{h}")
    robust_write(OUT / "lady.atlas", ("\n".join(lines) + "\n").encode("utf-8"))
    print(f"[atlas] lady.webp {W}x{H}, {len(all_regions)} regions", flush=True)

    # skeletons
    for key, (recs, Wt, Ht, prefix) in variant_records.items():
        skel = build_skeleton(recs, Wt, Ht, prefix, is_bonus=(key == "bonus"))
        robust_write(OUT / VARIANTS[key]["json"], json.dumps(skel).encode("utf-8"))
        print(f"[skel] {VARIANTS[key]['json']} ({len(skel['bones'])} bones, "
              f"{len(skel['slots'])} slots)", flush=True)


if __name__ == "__main__":
    main()
