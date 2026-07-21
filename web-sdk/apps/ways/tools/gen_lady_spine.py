"""Build a professional articulated Spine rig for the Lady Mirror scene char.

She is rigged from her EXISTING cutouts (no regen — her face/outfit stay exactly
the same) as a single full-figure WEIGHTED MESH driven by a real bone hierarchy:

    root -> hips -> spine -> chest -> neck -> head
    hips -> gown            (skirt/hem sway)
    head -> veil            (veil billow)
    chest -> armR           (the hand-mirror arm: subtle raise)
    (+ aura bone for the ghost glow)

Every mesh vertex is bone-weighted by region (head/neck/chest/spine/hips/gown
chain + veil + arm overrides), so the veil, gown and hair BEND like cloth and
the head/arm articulate — WITHOUT cutting the art into separate textures (which
on a single AI illustration would leave holes/seams). One skinned mesh = no
holes, no seams, no ghosting.

Animations:
    idle       looping ~4.6s: floating bob (root), breathing (spine scale),
               head tilt, mirror-arm raise, gown sway, veil billow, hair drift,
               pulsing violet ghost aura. First==last key -> seamless loop.
    idle_flat  committed FALLBACK: the earlier whole-figure mesh-deform ripple
               (gentle undulation) + aura, bones at rest.

Two variants (base + bonus) share one atlas (lady.webp) with regions
lady_base / lady_bonus. Runtime @esotericsoftware/spine-pixi-v8 4.2.74 (4.1
JSON, mesh deform nested under animation "attachments").

Output -> static/assets/spines/lady/ (lady.atlas/.webp/.png + lady.json +
lady_bonus.json).  Run:  python tools/gen_lady_spine.py
"""

from __future__ import annotations

import json
import math
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SCENE_DIR = os.path.normpath(
    os.path.join(HERE, "..", "static", "assets", "sprites", "scene")
)
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "spines", "lady"))

SPINE_VERSION = "4.1.23"
PAD = 2
TARGET_H = 1000  # native atlas height per figure (scaled down at runtime)

GX, GY = 7, 13  # mesh grid cells (8 x 14 vertices) — tall for smooth cloth
PERIOD = 4.6
STEPS = 12
AURA_HEX = "9a6cff"

# bone chain order (index in this list == Spine bone index used by weights)
BONE_ORDER = ["root", "hips", "spine", "chest", "neck", "head", "gown", "veil", "armR", "aura"]
BONE_PARENT = {
    "hips": "root", "spine": "hips", "chest": "spine", "neck": "chest",
    "head": "neck", "gown": "hips", "veil": "head", "armR": "chest", "aura": "root",
}

# Per-variant config: source file, bone pivots (fractional x,y from TOP-LEFT of
# the trimmed image), and the arm/veil weight regions. Base holds the mirror
# low-center; bonus raises the glowing mirror to the upper-left.
VARIANTS = {
    "lady_base": {
        "file": "lady_character.png",
        "skeleton": "lady.json",
        "pivots": {
            "hips": (0.44, 0.55), "spine": (0.44, 0.38), "chest": (0.45, 0.27),
            "neck": (0.43, 0.18), "head": (0.41, 0.12), "gown": (0.44, 0.46),
            "veil": (0.60, 0.12), "armR": (0.52, 0.26),
        },
        # arm region (shoulder -> hand+mirror), peak toward the hand (bottom)
        "arm_box": (0.47, 0.30, 0.72, 0.76), "arm_peak": "down",
        # veil billows down the right side
        "veil_box": (0.62, 0.10, 1.00, 0.95),
    },
    "lady_bonus": {
        "file": "lady_bonus.png",
        "skeleton": "lady_bonus.json",
        "pivots": {
            "hips": (0.48, 0.52), "spine": (0.48, 0.35), "chest": (0.49, 0.25),
            "neck": (0.50, 0.19), "head": (0.50, 0.12), "gown": (0.48, 0.45),
            "veil": (0.64, 0.16), "armR": (0.40, 0.22),
        },
        # raised arm+mirror to the upper-left, peak toward the mirror (up-left)
        "arm_box": (0.00, 0.00, 0.42, 0.42), "arm_peak": "upleft",
        "veil_box": (0.60, 0.14, 1.00, 0.95),
    },
}


def rgba_hex(hex6: str, alpha: float) -> str:
    return f"{hex6}{int(max(0.0, min(1.0, alpha)) * 255):02x}"


def load_trimmed(name: str) -> Image.Image:
    img = Image.open(os.path.join(SCENE_DIR, name)).convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    w, h = img.size
    return img.resize((max(1, round(w * TARGET_H / h)), TARGET_H), Image.LANCZOS)


def smoothstep(a: float, b: float, x: float) -> float:
    if a == b:
        return 0.0 if x < a else 1.0
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def box_mask(fx: float, fy: float, box, feather=0.08) -> float:
    x0, y0, x1, y1 = box
    hx = smoothstep(x0 - feather, x0 + feather, fx) * (1 - smoothstep(x1 - feather, x1 + feather, fx))
    hy = smoothstep(y0 - feather, y0 + feather, fy) * (1 - smoothstep(y1 - feather, y1 + feather, fy))
    return hx * hy


def chain_weight(fy: float, anchors) -> dict:
    """Blend along the vertical spine chain by fy (2-bone linear blend)."""
    if fy <= anchors[0][0]:
        return {anchors[0][1]: 1.0}
    if fy >= anchors[-1][0]:
        return {anchors[-1][1]: 1.0}
    for i in range(len(anchors) - 1):
        y0, n0 = anchors[i]
        y1, n1 = anchors[i + 1]
        if y0 <= fy <= y1:
            t = (fy - y0) / (y1 - y0)
            return {n0: 1 - t, n1: t}
    return {anchors[-1][1]: 1.0}


def vertex_weights(fx: float, fy: float, cfg: dict, anchors) -> dict:
    w = chain_weight(fy, anchors)

    # arm/mirror override: bias toward the hand end so the mirror leads
    arm = box_mask(fx, fy, cfg["arm_box"], 0.06)
    if cfg["arm_peak"] == "down":
        arm *= smoothstep(cfg["arm_box"][1], cfg["arm_box"][3], fy)
    else:  # upleft
        arm *= smoothstep(cfg["arm_box"][2], cfg["arm_box"][0], fx) * smoothstep(
            cfg["arm_box"][3], cfg["arm_box"][1], fy
        )
    arm_w = arm * 0.8
    # veil override: strongest at the outer/lower edge of the veil
    veil = box_mask(fx, fy, cfg["veil_box"], 0.07)
    veil *= smoothstep(cfg["veil_box"][0], cfg["veil_box"][2], fx)
    veil_w = veil * 0.55

    override = min(0.92, arm_w + veil_w)
    if override > 0.001:
        for k in list(w.keys()):
            w[k] *= 1 - override
        if arm_w >= veil_w:
            w["armR"] = w.get("armR", 0) + arm_w
            if veil_w > 0.02:
                w["veil"] = w.get("veil", 0) + veil_w
        else:
            w["veil"] = w.get("veil", 0) + veil_w
            if arm_w > 0.02:
                w["armR"] = w.get("armR", 0) + arm_w

    # keep the 3 strongest, renormalise
    top = dict(sorted(w.items(), key=lambda kv: kv[1], reverse=True)[:3])
    total = sum(top.values()) or 1.0
    return {k: v / total for k, v in top.items()}


def bone_abs(cfg: dict, W: float, H: float) -> dict:
    """Absolute skeleton coords (y-up, figure centered) for every bone."""
    def m(frac):
        fx, fy = frac
        return (-W / 2 + fx * W, H / 2 - fy * H)

    abs_pos = {"root": (0.0, 0.0), "aura": (0.0, 0.0)}
    for name, frac in cfg["pivots"].items():
        abs_pos[name] = m(frac)
    return abs_pos


def build_bones(abs_pos: dict) -> list:
    bones = []
    for name in BONE_ORDER:
        entry = {"name": name}
        parent = BONE_PARENT.get(name)
        if parent:
            entry["parent"] = parent
            entry["x"] = round(abs_pos[name][0] - abs_pos[parent][0], 2)
            entry["y"] = round(abs_pos[name][1] - abs_pos[parent][1], 2)
        bones.append(entry)
    return bones


def build_weighted_mesh(W: float, H: float, abs_pos: dict, cfg: dict) -> dict:
    cols, rows = GX + 1, GY + 1
    idx = {name: i for i, name in enumerate(BONE_ORDER)}
    anchors = sorted(
        [(cfg["pivots"][n][1], n) for n in ("head", "neck", "chest", "spine", "hips", "gown")]
    )
    uvs, verts = [], []
    for row in range(rows):
        for col in range(cols):
            u, v = col / GX, row / GY
            uvs += [u, v]
            vx = -W / 2 + u * W
            vy = H / 2 - v * H
            weights = vertex_weights(u, v, cfg, anchors)
            entry = [len(weights)]
            for name, wt in weights.items():
                bx, by = abs_pos[name]
                entry += [idx[name], round(vx - bx, 2), round(vy - by, 2), round(wt, 4)]
            verts += entry
    triangles = []
    for row in range(GY):
        for col in range(GX):
            i0 = row * cols + col
            i1 = i0 + 1
            i2 = i0 + cols
            i3 = i2 + 1
            triangles += [i0, i2, i1, i1, i2, i3]
    return {
        "type": "mesh",
        "uvs": uvs,
        "triangles": triangles,
        "vertices": verts,
        "hull": 2 * cols + 2 * (rows - 2),
        "width": W,
        "height": H,
    }


def sine_keys(amp, phase=0.0, base=0.0, cycles=1):
    return [(i, base + amp * math.sin(2 * math.pi * cycles * (i / STEPS) + phase)) for i in range(STEPS + 1)]


def timed(keys, make):
    out = []
    for i, value in keys:
        key = make(value)
        if i > 0:
            key["time"] = round(i * PERIOD / STEPS, 4)
        out.append(key)
    return out


def idle_animation(region: str, W: float, H: float) -> dict:
    bones = {
        "root": {"translate": timed(sine_keys(H * 0.018, 0.0), lambda v: {"x": 0, "y": round(v, 2)})},
        "hips": {"rotate": timed(sine_keys(0.6, math.pi / 5), lambda v: {"value": round(v, 3)})},
        "spine": {
            "rotate": timed(sine_keys(0.5, math.pi / 3), lambda v: {"value": round(v, 3)}),
            "scale": [],
        },
        "chest": {"rotate": timed(sine_keys(0.8, math.pi / 2), lambda v: {"value": round(v, 3)})},
        "neck": {"rotate": timed(sine_keys(0.7, math.pi / 2.5), lambda v: {"value": round(v, 3)})},
        "head": {"rotate": timed(sine_keys(1.6, math.pi / 2), lambda v: {"value": round(v, 3)})},
        "gown": {"rotate": timed(sine_keys(1.4, 0.0), lambda v: {"value": round(v, 3)})},
        "veil": {"rotate": timed(sine_keys(1.2, math.pi / 4), lambda v: {"value": round(v, 3)})},
        "armR": {"rotate": timed(sine_keys(2.2, math.pi / 6), lambda v: {"value": round(v, 3)})},
        "aura": {"scale": timed(sine_keys(0.02, math.pi / 2, 1.03), lambda v: {"x": round(v, 4), "y": round(v, 4)})},
    }
    # breathing on spine (y swell, slight x pinch)
    for i, v in sine_keys(0.014, 0.0):
        key = {"x": round(1 - v * 0.6, 4), "y": round(1 + v, 4)}
        if i > 0:
            key["time"] = round(i * PERIOD / STEPS, 4)
        bones["spine"]["scale"].append(key)

    # light cloth shimmer deform on top of the bone motion (small; seamless)
    cols, rows = GX + 1, GY + 1
    sway = W * 0.012
    deform_keys = []
    for i in range(STEPS + 1):
        phase = 2 * math.pi * (i / STEPS)
        deltas = []
        for row in range(rows):
            for col in range(cols):
                ny = row / GY
                dx = sway * (ny ** 1.4) * math.sin(phase + ny * 2.4)
                deltas += [round(dx, 2), 0.0]
        key = {"offset": 0, "vertices": deltas}
        if i > 0:
            key["time"] = round(i * PERIOD / STEPS, 4)
        deform_keys.append(key)

    aura_rgba = timed(
        sine_keys(0.5, -math.pi / 2, 0.5),
        lambda v: {"color": rgba_hex(AURA_HEX, 0.05 + 0.12 * max(0.0, min(1.0, v)))},
    )
    return {
        "slots": {"lady_aura": {"rgba": aura_rgba}},
        "bones": bones,
        "attachments": {"default": {"lady_body": {region: {"deform": deform_keys}}}},
    }


def idle_flat_animation(region: str, W: float, H: float) -> dict:
    """Committed fallback: the whole-figure mesh-deform ripple + aura, bones
    at rest (the earlier single-texture 'living photo' idle)."""
    cols, rows = GX + 1, GY + 1
    amp = W * 0.03
    keys = []
    for i in range(STEPS + 1):
        p = i / STEPS
        travel = 2 * math.pi * p
        env = 0.5 - 0.5 * math.cos(2 * math.pi * p)  # sin^2 seam
        deltas = []
        for row in range(rows):
            for col in range(cols):
                nx = (col / GX) * 2 - 1
                ny = 1 - (row / GY) * 2
                damp = 0.6 + 0.4 * (1 - max(abs(nx), abs(ny)))
                dx = amp * env * math.sin(travel + math.pi * 0.9 * nx + 0.6 * ny) * damp
                dy = amp * 0.7 * env * math.sin(travel + math.pi * 1.1 * ny) * damp
                deltas += [round(dx, 2), round(dy, 2)]
        key = {"offset": 0, "vertices": deltas}
        if i > 0:
            key["time"] = round(p * PERIOD, 4)
        keys.append(key)
    aura_rgba = timed(
        sine_keys(0.5, -math.pi / 2, 0.5),
        lambda v: {"color": rgba_hex(AURA_HEX, 0.05 + 0.1 * max(0.0, min(1.0, v)))},
    )
    return {
        "slots": {"lady_aura": {"rgba": aura_rgba}},
        "bones": {"root": {"translate": timed(sine_keys(H * 0.014, 0.0), lambda v: {"x": 0, "y": round(v, 2)})}},
        "attachments": {"default": {"lady_body": {region: {"deform": keys}}}},
    }


def skeleton_json(region: str, W: float, H: float, cfg: dict) -> dict:
    abs_pos = bone_abs(cfg, W, H)
    return {
        "skeleton": {
            "hash": f"mm-{region}", "spine": SPINE_VERSION,
            "x": -W / 2, "y": -H / 2, "width": W, "height": H,
            "images": "./images/", "audio": "",
        },
        "bones": build_bones(abs_pos),
        "slots": [
            {"name": "lady_aura", "bone": "aura", "attachment": region,
             "color": rgba_hex(AURA_HEX, 0.1), "blend": "additive"},
            {"name": "lady_body", "bone": "root", "attachment": region},
        ],
        "skins": [{
            "name": "default",
            "attachments": {
                "lady_aura": {region: {"width": W, "height": H}},
                "lady_body": {region: build_weighted_mesh(W, H, abs_pos, cfg)},
            },
        }],
        "animations": {
            "idle": idle_animation(region, W, H),
            "idle_flat": idle_flat_animation(region, W, H),
        },
    }


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    imgs = {region: load_trimmed(cfg["file"]) for region, cfg in VARIANTS.items()}

    base, bonus = imgs["lady_base"], imgs["lady_bonus"]
    page_w = PAD * 3 + base.width + bonus.width
    page_h = PAD * 2 + max(base.height, bonus.height)
    page = Image.new("RGBA", (page_w, page_h), (0, 0, 0, 0))
    placements = {"lady_base": (PAD, PAD), "lady_bonus": (PAD * 2 + base.width, PAD)}
    atlas_lines = ["lady.webp", f"size:{page_w},{page_h}", "filter:Linear,Linear", "scale:1"]
    for region, (x, y) in placements.items():
        img = imgs[region]
        page.paste(img, (x, y))
        atlas_lines += [region, f"bounds:{x},{y},{img.width},{img.height}"]

    page.save(os.path.join(OUT_DIR, "lady.png"))
    page.save(os.path.join(OUT_DIR, "lady.webp"), lossless=True)
    with open(os.path.join(OUT_DIR, "lady.atlas"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(atlas_lines) + "\n")

    for region, cfg in VARIANTS.items():
        img = imgs[region]
        data = skeleton_json(region, float(img.width), float(img.height), cfg)
        with open(os.path.join(OUT_DIR, cfg["skeleton"]), "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f)
        print(f"  {region}: {img.width}x{img.height} -> {cfg['skeleton']}")

    print(f"wrote atlas {page_w}x{page_h} + {len(imgs)} weighted-mesh skeletons to {OUT_DIR}")


if __name__ == "__main__":
    main()
