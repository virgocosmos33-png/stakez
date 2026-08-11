"""Bake the LINKED-CELL FIRE atlas: a REAL burning frame that rings the card and
licks over its border — the card face stays readable through the open centre.

Outputs: static/ + assets/ sprites/fx/cell_fire.png + .json  (key `cellFire`)

WHY METABALL FIRE (THE "only-css-fire" TECHNIQUE, BAKED)
--------------------------------------------------------
Every other pass was rejected as ugly: runtime additive tongues broke into blobs;
keyed stills baked into a lava slab / veiled the card; Kenney particle plumes
tiled into "gold candle teeth"; Kenney's explosion pack is cartoon puffs; and a
keyed real-fire photo only shimmered, it did not flow. The user pointed at the
classic CSS metaball fire (rising dark blobs -> blur -> contrast() snaps the
fuzzy field into sharp organic flame tongues). We replicate that in numpy: build
a sum-of-gaussians scalar field = an always-burning border ROOT outline of the
card rectangle + flame PARTICLES rising outward from it, then ISO-THRESHOLD the
field (the contrast step) to get sharp, connected, organic flames with a wispy
skirt. Particles cycle an integer number of times over the 16-phase loop, so the
flipbook loops seamlessly and animates like real licking fire. Baked to PNG, so
the engine only alpha-draws it and it renders identically headless
(tools/qa_fire_mock.py) and in-engine.

Extra bands: smoke (Kenney Black smoke, off the top), a warm glow (Kenney light
mask), and warm ember sprites (Kenney sparks). Frame order is the contract in
src/game/cellFire.ts.
"""

import json
import os

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
KENNEY = os.path.join(APP, "assets-raw", "kenney_haul_fire")
# the fx sprites live in BOTH trees: static/ is served, assets/ is what the
# bundler resolves. Write to both so the two never drift.
OUT_DIRS = [
    os.path.join(APP, "static", "assets", "sprites", "fx"),
    os.path.join(APP, "assets", "sprites", "fx"),
]

# Frame geometry (bake px). CARD keeps the portrait card aspect (0.775); DEPTH is
# how far the flames lick beyond the card edge. The ratios FRAME/CARD are the
# contract the component uses to size the sprite around the card without
# stretching (kept in src/game/cellFire.ts — update both together).
CARD_W, CARD_H = 186, 240
DEPTH = 42  # flames lick ~42px beyond the card edge and over its border
FRAME_W = CARD_W + 2 * DEPTH  # 270
FRAME_H = CARD_H + 2 * DEPTH  # 324
FRAME_PHASES = 16

# METABALL FIRE (the "only-css-fire" technique: rising blobs -> blur -> contrast
# threshold snaps the fuzzy field into sharp organic flame tongues). We build a
# sum-of-gaussians field around the card border, each blob a flame particle
# rising OUTWARD from the border with an upward bias, then iso-threshold it. The
# particles cycle an INTEGER number of times over the phase loop so the flipbook
# is seamless. This is procedural, so it animates like real licking fire.
MB_PARTICLES = 360      # flame particles seeded around the whole border
MB_ISO = 0.62           # higher iso -> leaner, separated tongues with real gaps
MB_EDGE = 0.13          # softness of the iso edge (wispy flame skirt)
MB_ISO_MAX = 1.5        # field value treated as the white-hot core
MB_ROOT_THICK = 4.5     # thin always-burning border line (not a fat band)
MB_ROOT_GAIN = 1.0      # how bright the root line burns

SMOKE = 112
SMOKE_COUNT = 16
GLOW = 200
EMBER = 40
EMBER_COUNT = 8

# keep the packed atlas comfortably under the 4096 GPU texture limit
ATLAS_MAX_W = 2048


def _smoothstep(a: float, b: float, x: np.ndarray) -> np.ndarray:
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _fxn(seed: float) -> float:
    """Deterministic 0..1 hash so every bake / replay is identical."""
    v = np.sin(seed * 12.9898 + 78.233) * 43758.5453
    return float(v - np.floor(v))


# card rectangle inside the frame (fire grows from this border outline)
_CARD_L, _CARD_T = DEPTH, DEPTH
_CARD_R, _CARD_B = DEPTH + CARD_W, DEPTH + CARD_H
_PERIM = 2.0 * (CARD_W + CARD_H)


def _perimeter_point(s: float) -> tuple[float, float, float, float]:
    """Map s in [0,1) to a point on the card-border outline and its OUTWARD
    normal, so a particle seeded there licks away from the card."""
    d = (s % 1.0) * _PERIM
    if d < CARD_W:  # top edge, normal up
        return _CARD_L + d, _CARD_T, 0.0, -1.0
    d -= CARD_W
    if d < CARD_H:  # right edge, normal right
        return _CARD_R, _CARD_T + d, 1.0, 0.0
    d -= CARD_H
    if d < CARD_W:  # bottom edge, normal down
        return _CARD_R - d, _CARD_B, 0.0, 1.0
    d -= CARD_W
    return _CARD_L, _CARD_B - d, -1.0, 0.0  # left edge, normal left


def _add_blob(field, cx, cy, r, inten, vx=0.0, vy=-1.0, elong=1.8):
    """Add one ANISOTROPIC gaussian flame particle: stretched along its travel
    direction (vx,vy) so it reads as a licking tongue, not a round dot. Windowed
    for speed."""
    r = max(r, 2.0)
    reach = 3 * r * elong
    x0 = max(int(cx - reach), 0)
    x1 = min(int(cx + reach) + 1, field.shape[1])
    y0 = max(int(cy - reach), 0)
    y1 = min(int(cy + reach) + 1, field.shape[0])
    if x0 >= x1 or y0 >= y1:
        return
    n = max((vx * vx + vy * vy) ** 0.5, 1e-4)
    ux, uy = vx / n, vy / n  # travel direction (tongue long axis)
    dx = np.arange(x0, x1, dtype=np.float32)[None, :] - cx
    dy = np.arange(y0, y1, dtype=np.float32)[:, None] - cy
    par = dx * ux + dy * uy          # along the tongue
    perp = -dx * uy + dy * ux        # across the tongue
    s_par = r * elong
    s_perp = r * 0.62
    field[y0:y1, x0:x1] += inten * np.exp(
        -(par * par / (2.0 * s_par * s_par) + perp * perp / (2.0 * s_perp * s_perp))
    )


def _root_field() -> np.ndarray:
    """Always-burning border: a glowing outline of the card rectangle that the
    flame particles grow out of, so the border never breaks even between licks."""
    yy, xx = np.mgrid[0:FRAME_H, 0:FRAME_W].astype(np.float32)
    dx = np.maximum(np.maximum(_CARD_L - xx, xx - _CARD_R), 0.0)
    dy = np.maximum(np.maximum(_CARD_T - yy, yy - _CARD_B), 0.0)
    out = np.sqrt(dx * dx + dy * dy)
    inx = np.minimum(xx - _CARD_L, _CARD_R - xx)
    iny = np.minimum(yy - _CARD_T, _CARD_B - yy)
    inside = np.minimum(inx, iny)
    is_in = (xx >= _CARD_L) & (xx <= _CARD_R) & (yy >= _CARD_T) & (yy <= _CARD_B)
    perim = np.where(is_in, np.maximum(inside, 0.0), out)
    return np.exp(-((perim / MB_ROOT_THICK) ** 2)) * MB_ROOT_GAIN


def build_frame_flipbook() -> list[Image.Image]:
    """FRAME_PHASES of METABALL fire tracing the card border (the only-css-fire
    technique baked to PNG). A sum-of-gaussians field = a burning border root +
    flame particles rising outward from it; iso-thresholding that field is the
    "contrast" step that turns the fuzzy blobs into sharp organic flame tongues.
    Particles cycle an integer number of times over the loop so it is seamless,
    and the field only lives around the border so the card centre stays clear."""
    root = _root_field()
    reach = DEPTH * 1.85
    frames: list[Image.Image] = []
    for phase in range(FRAME_PHASES):
        field = root.copy()
        for i in range(MB_PARTICLES):
            px, py, nx, ny = _perimeter_point(_fxn(i * 1.73 + 0.5))
            cycles = 1 + int(_fxn(i * 2.31 + 3.0) * 3)      # 1..3 rises per loop
            off = _fxn(i * 3.97 + 7.0)
            life = ((phase / FRAME_PHASES) * cycles + off) % 1.0
            # tangent along the edge for a side-to-side wiggle
            tx, ty = -ny, nx
            wig = np.sin(life * 6.2832 * cycles + i) * 6.0
            drift = life * reach
            up = life * DEPTH * 0.5                          # fire leans upward
            cx = px + nx * drift + tx * wig
            cy = py + ny * drift + ty * wig - up
            # travel direction = outward normal biased upward -> tongue long axis
            vx, vy = nx, ny - 0.7
            size = 3.6 + 4.0 * _fxn(i * 5.11 + 2.0) + life * 3.0  # leaner tongues
            inten = (1.0 - life) ** 1.15 * (0.7 + 0.6 * _fxn(i * 6.73 + 9.0))
            _add_blob(field, cx, cy, size, inten, vx, vy, elong=2.1)

        # metaball iso-threshold = the CSS contrast() step
        alpha = _smoothstep(MB_ISO - MB_EDGE, MB_ISO + MB_EDGE, field)
        core = np.clip((field - MB_ISO) / (MB_ISO_MAX - MB_ISO), 0.0, 1.0)
        # fire ramp: red-orange skirt -> orange body -> gold-hot core
        tip = np.array([0.90, 0.15, 0.02], np.float32)
        mid = np.array([1.00, 0.45, 0.07], np.float32)
        hot = np.array([1.00, 0.82, 0.36], np.float32)
        c = core[..., None]
        col = tip + (mid - tip) * np.clip(c / 0.5, 0.0, 1.0)
        col = col + (hot - mid) * np.clip((c - 0.5) / 0.5, 0.0, 1.0)
        col = np.clip(col * 1.08, 0.0, 1.0)
        out = np.dstack([col, np.clip(alpha, 0.0, 1.0)])
        img = Image.fromarray((out * 255).astype(np.uint8), "RGBA")
        img = img.filter(ImageFilter.GaussianBlur(0.5))  # soften the iso edge
        frames.append(clear_rgb_under_alpha(img))
    print(f"[fire] {len(frames)} metaball-fire phases @ {FRAME_W}x{FRAME_H} (only-css-fire)")
    return frames


def alpha_crop(img: Image.Image, pad: int = 2) -> Image.Image:
    box = img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if not box:
        return img
    l = max(box[0] - pad, 0)
    t = max(box[1] - pad, 0)
    r = min(box[2] + pad, img.width)
    b = min(box[3] + pad, img.height)
    return img.crop((l, t, r, b))


def clear_rgb_under_alpha(img: Image.Image) -> Image.Image:
    arr = np.asarray(img).copy()
    arr[arr[..., 3] == 0, :3] = 0
    return Image.fromarray(arr, "RGBA")


def fit(img: Image.Image, w: int, h: int) -> Image.Image:
    scale = min(w / img.width, h / img.height)
    size = (max(int(img.width * scale), 1), max(int(img.height * scale), 1))
    small = img.resize(size, Image.LANCZOS)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(small, ((w - size[0]) // 2, h - size[1]), small)
    return canvas


def build_smoke() -> list[Image.Image]:
    src = os.path.join(KENNEY, "smokeseq_black")
    names = sorted(n for n in os.listdir(src) if n.endswith(".png"))
    if not names:
        raise SystemExit(f"missing Kenney smoke haul: {src}")
    step = max(len(names) // SMOKE_COUNT, 1)
    out = []
    for name in names[::step][:SMOKE_COUNT]:
        img = Image.open(os.path.join(src, name)).convert("RGBA")
        arr = np.asarray(img).astype(np.float32)
        lift = np.array([120.0, 104.0, 92.0], np.float32)
        arr[..., :3] = lift * (0.5 + 0.5 * (arr[..., :3] / 255.0))
        img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
        puff = fit(alpha_crop(img), SMOKE, SMOKE).filter(ImageFilter.GaussianBlur(2.6))
        out.append(clear_rgb_under_alpha(puff))
    print(f"[fire] {len(out)} smoke frames @ {SMOKE}px from Kenney Black smoke")
    return out


def build_embers() -> list[Image.Image]:
    src = os.path.join(KENNEY, "spark")
    names = sorted(n for n in os.listdir(src) if n.endswith(".png"))
    if not names:
        raise SystemExit(f"missing Kenney spark haul: {src}")
    out = []
    for name in (names * EMBER_COUNT)[:EMBER_COUNT]:
        img = Image.open(os.path.join(src, name)).convert("RGBA")
        arr = np.asarray(img).astype(np.float32)
        a = arr[..., 3:4] / 255.0
        tint = np.array([255.0, 150.0, 40.0], np.float32) + np.array([0.0, 90.0, 150.0], np.float32) * a
        arr[..., :3] = np.clip(tint, 0, 255)
        img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
        out.append(clear_rgb_under_alpha(fit(alpha_crop(img), EMBER, EMBER)))
    print(f"[fire] {len(out)} embers @ {EMBER}px from Kenney sparks")
    return out


def build_glow() -> Image.Image:
    src = os.path.join(KENNEY, "lightmasks")
    names = sorted(n for n in os.listdir(src) if n.endswith(".png"))
    pick = next((n for n in names if "circle" in n.lower()), names[0] if names else None)
    if pick is None:
        raise SystemExit(f"missing Kenney light masks: {src}")
    img = Image.open(os.path.join(src, pick)).convert("RGBA")
    img = fit(alpha_crop(img), GLOW, GLOW).filter(ImageFilter.GaussianBlur(1.2))
    print(f"[fire] glow from {pick}")
    return clear_rgb_under_alpha(img)


def main() -> None:
    for out_dir in OUT_DIRS:
        os.makedirs(out_dir, exist_ok=True)

    frame = build_frame_flipbook()
    smoke = build_smoke()
    glow = build_glow()
    embers = build_embers()

    # Insertion order IS the contract (src/game/cellFire.ts indexes the flat
    # texture list the loader returns). Grid-pack each band into rows capped at
    # ATLAS_MAX_W so the big frame tiles never blow past the GPU texture limit.
    bands = [
        ("frame", frame, FRAME_W, FRAME_H),
        ("smoke", smoke, SMOKE, SMOKE),
        ("glow", [glow], GLOW, GLOW),
        ("ember", embers, EMBER, EMBER),
    ]

    # first pass: assign every tile a row/col to compute the atlas size
    placements = []  # (band_name, index, tile_w, tile_h, x, y)
    x = y = row_h = 0
    atlas_w = 0
    for name, items, tw, th in bands:
        if x != 0:  # start each band on a fresh row for tidy, stable layout
            y += row_h
            x = row_h = 0
        per_row = max(ATLAS_MAX_W // tw, 1)
        for index, _img in enumerate(items):
            if index and index % per_row == 0:
                y += th
                x = 0
            placements.append((name, index, tw, th, x, y))
            x += tw
            row_h = max(row_h, th)
            atlas_w = max(atlas_w, x)
        y += row_h
        x = row_h = 0
    atlas_h = y

    atlas = Image.new("RGBA", (atlas_w, atlas_h), (0, 0, 0, 0))
    lookup = {(n, i): (bx, by) for (n, i, _tw, _th, bx, by) in placements}
    meta_frames = {}
    band_no = {name: k for k, (name, *_r) in enumerate(bands)}
    for name, items, tw, th in bands:
        for index, img in enumerate(items):
            bx, by = lookup[(name, index)]
            atlas.paste(img, (bx + (tw - img.width) // 2, by + (th - img.height) // 2), img)
            meta_frames[f"{band_no[name]}_{name}_{index:02d}.png"] = {
                "frame": {"x": bx, "y": by, "w": tw, "h": th},
                "rotated": False,
                "trimmed": False,
                "spriteSourceSize": {"x": 0, "y": 0, "w": tw, "h": th},
                "sourceSize": {"w": tw, "h": th},
            }

    meta = {
        "frames": meta_frames,
        "meta": {
            "image": "cell_fire.png",
            "format": "RGBA8888",
            "size": {"w": atlas.width, "h": atlas.height},
            "scale": "1",
            "sources": {
                "frame": "Metaball fire (only-css-fire technique): sum-of-gaussians border field iso-thresholded into organic flame tongues, animated per phase",
                "smoke": "Kenney smoke-particles / Black smoke (CC0)",
                "glow": "Kenney light-masks-1.0 / Transparent (CC0)",
                "ember": "Kenney particle-pack / spark (CC0), warm-tinted",
            },
            "geometry": {
                "cardW": CARD_W, "cardH": CARD_H, "frameW": FRAME_W, "frameH": FRAME_H,
            },
            "counts": {"frame": len(frame), "smoke": len(smoke), "glow": 1, "ember": len(embers)},
        },
    }
    for out_dir in OUT_DIRS:
        png_path = os.path.join(out_dir, "cell_fire.png")
        json_path = os.path.join(out_dir, "cell_fire.json")
        atlas.save(png_path, optimize=True)
        with open(json_path, "w", encoding="utf-8") as handle:
            json.dump(meta, handle, indent=1)
        print(f"[fire] wrote {png_path} ({os.path.getsize(png_path):,} B) {atlas.width}x{atlas.height}")


if __name__ == "__main__":
    main()
