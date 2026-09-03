"""Generate Spine skeletons + a shared atlas for the ways symbol set.

THE WHITE ROOM: each symbol id maps to a DISTINCT clinical-horror concept
(land / win / postWin) via _white_room_concepts.py — NOT a shared Madam Mirror
punch+wobble+wisp pack with only new textures/tints.

Rig layers (draw order):
    plate (H/L only), aura, card mesh, glow, clip, streak, ring, wisp x3, shard x4

States (constants.ts):
    <id>          win concept motion
    <id>_land     land concept motion
    <id>_postwin  looping inhale (slight scale + lift, no mesh wave)
    <id>_static   rest pose (plate + face)
    hm_break      Observation Pane intact -> cracked + porcelain shards

spin / postWinStatic remain SPRITE states (baked plate+face). H/L board
static / land / win / postWin play this rig.
Explosion uses symbols3/explosion (rebuilt by gen_white_room_explosion.py).

GAME_CONFIG (from regenerate_assets) drives card_<id>_<slug>.png + White Room tints.

Run:  python tools/gen_symbol_spines.py
"""

import json
import math
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _white_room_concepts as wr  # noqa: E402


def robust_write_bytes(path, data, attempts=8):
    """Atomic write with retries for OneDrive Errno 22 locks."""
    tmp = path + ".tmp"
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


def robust_write_text(path, text, attempts=8):
    robust_write_bytes(path, text.encode("utf-8"), attempts=attempts)


def robust_save_image(img, path, **save_kwargs):
    """Save via temp file + replace so OneDrive locks don't kill the rebuild."""
    import io

    buf = io.BytesIO()
    fmt = "WEBP" if path.lower().endswith(".webp") else "PNG"
    img.save(buf, format=fmt, **save_kwargs)
    robust_write_bytes(path, buf.getvalue())
CARD_DIR = os.path.join(HERE, "symbol_art")
ATLAS_STATIC_DIR = os.path.normpath(
    os.path.join(HERE, "..", "static", "assets", "sprites", "symbolsStatic")
)
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "spines", "mm_symbols"))
PLATE_DIR = os.path.normpath(os.path.join(HERE, "..", "assets-raw", "cell_backplates"))
PLATE_FILES = {
    "plate_high": os.path.join(PLATE_DIR, "plate_high.png"),
    "plate_low": os.path.join(PLATE_DIR, "plate_low.png"),
}
PLATE_FOR_GID = {
    "h1": "plate_high",
    "h2": "plate_high",
    "h3": "plate_high",
    "h4": "plate_high",
    "h5": "plate_high",
    "l1": "plate_low",
    "l2": "plate_low",
    "l3": "plate_low",
    "l4": "plate_low",
    "l5": "plate_low",
}

CELL = 300
PADDING = 2
COLUMNS = 4
SPINE_VERSION = "4.1.23"

# the card is a deformable grid mesh (MESH_GRID x MESH_GRID cells) so the
# postWin animation can ripple the ACTUAL artwork - the symbol itself moves,
# it is not a glow/effect layered on a static card.
MESH_GRID = 4

# skeleton id -> art source: ("card", filename) reads from symbol_art;
# ("frame", framename) extracts a cell from the current symbolsStatic atlas.
_LEGACY_SYMBOLS = {
    "h1": ("card", "card_h1_lady_mirror.png"),
    "h2": ("card", "card_h2_wife.png"),
    "h3": ("card", "card_h3_man.png"),
    "h4": ("card", "card_h4_young_woman.png"),
    "h5": ("card", "card_h5_dog.png"),
    "l1": ("card", "card_l1_syringe.png"),
    "l2": ("card", "card_l2_stethoscope.png"),
    "l3": ("card", "card_l3_restraint_buckle.png"),
    "l4": ("card", "card_l4_clipboard_404.png"),
    "l5": ("card", "card_l5_pill_bottle.png"),
    "w": ("frame", "w.png"),
    "s": ("frame", "s.png"),
    "hm": ("frame", "hm_intact.png"),
}

# atlas-only regions (no skeleton of their own; used by attachment swaps).
# Prefer White Room card master when present (ALWAYS_KEEP in repack used to
# leave a Madam Mirror purple hm_cracked in symbolsStatic).
def _resolve_extra_regions():
    card = "card_hm_cracked.png"
    if os.path.isfile(os.path.join(CARD_DIR, card)):
        return {"hm_cracked": ("card", card)}
    return {"hm_cracked": ("frame", "hm_cracked.png")}


EXTRA_REGIONS = _resolve_extra_regions()

# Legacy Madam Mirror FX tints (r, g, b) 0..1
_LEGACY_TINTS = {
    "h1": (0.80, 0.64, 1.00),
    "h2": (0.80, 0.64, 1.00),
    "h3": (0.80, 0.64, 1.00),
    "h4": (0.80, 0.64, 1.00),
    "h5": (0.80, 0.64, 1.00),
    "l1": (0.86, 0.88, 1.00),
    "l2": (0.86, 0.88, 1.00),
    "l3": (0.86, 0.88, 1.00),
    "l4": (0.86, 0.88, 1.00),
    "l5": (0.86, 0.88, 1.00),
    "w": (0.72, 0.53, 1.00),
    "s": (1.00, 0.81, 0.45),
    "hm": (0.90, 0.83, 1.00),
}

# THE WHITE ROOM — clinical silver / charcoal / faint dried-blood (no purple)
_WHITE_ROOM_TINTS = {
    "h1": (0.91, 0.90, 0.88),
    "h2": (0.86, 0.85, 0.82),
    "h3": (0.78, 0.76, 0.72),
    "h4": (0.88, 0.87, 0.84),
    "h5": (0.72, 0.70, 0.66),
    "l1": (0.70, 0.68, 0.64),
    "l2": (0.70, 0.68, 0.64),
    "l3": (0.66, 0.64, 0.60),
    "l4": (0.66, 0.64, 0.60),
    "l5": (0.62, 0.60, 0.56),
    "w": (0.92, 0.90, 0.88),
    "s": (0.90, 0.88, 0.84),
    "hm": (0.82, 0.70, 0.68),  # silver + faint blood
}

_FRAME_SPECIALS = {
    "w": ("frame", "w.png"),
    "s": ("frame", "s.png"),
    "hm": ("frame", "hm_intact.png"),
}


def _slug(name: str) -> str:
    s_ = re.sub(r"[^a-z0-9]+", "_", (name or "symbol").lower()).strip("_")
    return s_ or "symbol"


def _hex_to_rgb01(hex_color: str):
    h = (hex_color or "").strip().lstrip("#")
    if len(h) != 6:
        return None
    return (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)


def _resolve_from_game_config():
    """Return (symbols_dict, tints_dict) or None when GAME_CONFIG is unset/unusable."""
    path = (os.environ.get("GAME_CONFIG") or "").strip()
    if not path or not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    identity = cfg.get("identity") or {}
    game_name = (identity.get("workingName") or identity.get("gameName") or "").lower()
    is_white_room = "white_room" in game_name.replace(" ", "_") or game_name == "the white room"

    symbols = dict(_LEGACY_SYMBOLS)
    for sym in cfg.get("symbols") or []:
        sid = str(sym.get("id") or "").lower()
        if not sid or sid == "me":
            # ME has no dedicated mm_symbols skeleton in this pack
            continue
        name = sym.get("name") or sid.upper()
        card_name = f"card_{sid}_{_slug(name)}.png"
        card_path = os.path.join(CARD_DIR, card_name)
        if os.path.isfile(card_path):
            symbols[sid] = ("card", card_name)
        elif sid in _FRAME_SPECIALS:
            # Prefer White Room card master when symbols agent has landed it;
            # otherwise keep symbolsStatic frame until repack.
            symbols[sid] = _FRAME_SPECIALS[sid]
        # else keep legacy card path so atlas rebuild still has pixels

    if is_white_room:
        tints = dict(_WHITE_ROOM_TINTS)
        # Optional: nudge highs toward palette mid greys if present
        palette = (cfg.get("promptContext") or {}).get("palette") or []
        if len(palette) >= 3:
            mid = _hex_to_rgb01(palette[2])  # #8a8680
            light = _hex_to_rgb01(palette[0])  # #f4f1ec
            blood = _hex_to_rgb01(palette[5]) if len(palette) > 5 else None
            if light:
                for k in ("h1", "h2", "h4", "w", "s"):
                    tints[k] = light
            if mid:
                for k in ("h3", "h5", "l1", "l2", "l3", "l4", "l5"):
                    tints[k] = mid
            if blood:
                tints["hm"] = tuple(0.55 * a + 0.45 * b for a, b in zip(mid or light, blood))
    else:
        tints = dict(_LEGACY_TINTS)

    print(f"gen_symbol_spines: GAME_CONFIG={path} white_room={is_white_room}")
    for gid, (kind, ref) in symbols.items():
        exists = os.path.isfile(os.path.join(CARD_DIR, ref)) if kind == "card" else "atlas-frame"
        print(f"  {gid}: {kind}:{ref} ({exists})")
    return symbols, tints


def _resolve_cards_on_disk():
    """When GAME_CONFIG is unset, prefer newest card_<id>_*.png over legacy
    Madam Mirror filenames so a bare `python tools/gen_symbol_spines.py` cannot
    repack old gothic portraits into mm_symbols while symbolsStatic is White Room.
    """
    symbols = dict(_LEGACY_SYMBOLS)
    # Legacy basenames that must lose to any newer White Room card_* master.
    legacy_names = {v[1] for v in _LEGACY_SYMBOLS.values() if v[0] == "card"}
    for sid in list(symbols.keys()):
        kind, _ref = symbols[sid]
        if kind != "card":
            continue
        matches = sorted(
            (
                p
                for p in Path(CARD_DIR).glob(f"card_{sid}_*.png")
                if p.is_file() and "_OLD_" not in p.parts
            ),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not matches:
            continue
        # Prefer a non-legacy master when present; otherwise newest file.
        preferred = next((p for p in matches if p.name not in legacy_names), matches[0])
        symbols[sid] = ("card", preferred.name)
    # Prefer White Room specials from symbolsStatic frames (already repacked).
    for sid, frame in _FRAME_SPECIALS.items():
        symbols[sid] = frame
    # Detect White Room by presence of known WR high cards.
    wr_markers = (
        "card_h1_the_patient.png",
        "card_h2_the_doctor.png",
        "card_h3_the_grin.png",
    )
    is_wr = any(os.path.isfile(os.path.join(CARD_DIR, n)) for n in wr_markers)
    tints = dict(_WHITE_ROOM_TINTS) if is_wr else dict(_LEGACY_TINTS)
    print(f"gen_symbol_spines: no GAME_CONFIG; disk-resolve white_room={is_wr}")
    for gid, (kind, ref) in symbols.items():
        exists = os.path.isfile(os.path.join(CARD_DIR, ref)) if kind == "card" else "atlas-frame"
        print(f"  {gid}: {kind}:{ref} ({exists})")
    return symbols, tints


_resolved = _resolve_from_game_config()
if _resolved:
    SYMBOLS, TINTS = _resolved
else:
    SYMBOLS, TINTS = _resolve_cards_on_disk()

STREAK_W, STREAK_H = 140, 460
WISP_SIZE = 96
RING_SIZE = 176
SHARD_SIZE = 64


def hex_rgba(tint, alpha):
    r, g, b = tint
    return f"{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}{int(max(0, min(1, alpha)) * 255):02x}"


def white_rgba(alpha):
    return hex_rgba((1, 1, 1), alpha)


# ---------------------------------------------------------------- fx artwork


def make_streak():
    """Vertical soft white bar: gaussian across width, feathered ends."""
    xs = np.arange(STREAK_W, dtype=np.float32)
    ys = np.arange(STREAK_H, dtype=np.float32)
    ax = np.exp(-(((xs - STREAK_W / 2) / (STREAK_W / 4.2)) ** 2))
    edge = STREAK_H * 0.12
    ay = np.minimum(np.minimum(ys / edge, (STREAK_H - 1 - ys) / edge), 1.0)
    alpha = np.clip(ax[None, :] * ay[:, None], 0, 1)
    # brighter hot line in the middle
    hot = np.exp(-(((xs - STREAK_W / 2) / (STREAK_W / 14)) ** 2))
    alpha = np.clip(alpha + hot[None, :] * ay[:, None] * 0.5, 0, 1)
    img = np.zeros((STREAK_H, STREAK_W, 4), dtype=np.uint8)
    img[..., :3] = 255
    img[..., 3] = (alpha * 255).astype(np.uint8)
    return Image.fromarray(img, "RGBA")


def make_wisp():
    """Clinical dust / ash mote (not gothic spectral wisp)."""
    size = WISP_SIZE
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    cx, cy = size / 2, size / 2
    a = np.zeros((size, size), dtype=np.float32)
    # soft particulate cloud — flatter, less "ghost trail"
    for (ox, oy, sx, sy, w) in (
        (0, 0, 16, 14, 1.0),
        (-10, 6, 9, 8, 0.55),
        (12, -4, 8, 10, 0.45),
        (4, 14, 6, 6, 0.35),
    ):
        a += w * np.exp(-(((xx - cx - ox) / sx) ** 2 + ((yy - cy - oy) / sy) ** 2))
    a = np.clip(a / a.max(), 0, 1) ** 1.35
    img = np.zeros((size, size, 4), dtype=np.uint8)
    # cool grey-white dust (tinted at runtime)
    img[..., 0] = 235
    img[..., 1] = 232
    img[..., 2] = 226
    img[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(img, "RGBA")


def make_ring():
    """Thin clinical shock ring — silver annulus, no soft gothic fill."""
    size = RING_SIZE
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    c = size / 2
    r = np.sqrt((xx - c) ** 2 + (yy - c) ** 2)
    ring = np.exp(-(((r - size * 0.38) / (size * 0.028)) ** 2))
    a = np.clip(ring, 0, 1)
    img = np.zeros((size, size, 4), dtype=np.uint8)
    img[..., 0] = 244
    img[..., 1] = 241
    img[..., 2] = 236
    img[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(img, "RGBA")


def make_shard(variant):
    """Porcelain / observation-glass chip (angular ceramic, not gem shard)."""
    ss = 4
    size = SHARD_SIZE * ss
    img = Image.new("L", (size, size), 0)
    from PIL import ImageDraw

    d = ImageDraw.Draw(img)
    c = size / 2
    # more faceted ceramic chip silhouettes
    shapes = {
        0: [(0.0, -0.42), (0.28, -0.08), (0.18, 0.38), (-0.22, 0.20), (-0.24, -0.10)],
        1: [(-0.10, -0.40), (0.30, -0.18), (0.22, 0.30), (-0.05, 0.42), (-0.28, 0.05)],
        2: [(0.05, -0.46), (0.20, 0.05), (0.02, 0.44), (-0.26, 0.12), (-0.12, -0.22)],
    }[variant]
    d.polygon([(c + px * size, c + py * size) for px, py in shapes], fill=255)
    a = np.asarray(img, dtype=np.float32) / 255.0
    yy = np.mgrid[0:size, 0:size][0].astype(np.float32)
    grad = 0.50 + 0.50 * (1 - yy / size)
    a = np.clip(a * grad, 0, 1)
    small = Image.fromarray((a * 255).astype(np.uint8), "L").resize(
        (SHARD_SIZE, SHARD_SIZE), Image.LANCZOS
    )
    out = Image.new("RGBA", (SHARD_SIZE, SHARD_SIZE), (232, 228, 220, 0))
    out.putalpha(small)
    return out


# ------------------------------------------------------------- rig building


def rig_slots(gid):
    """Slot list in draw order (first = drawn behind). No cell backboard."""
    slots = [
        {"name": f"{gid}_aura", "bone": "card", "color": hex_rgba(TINTS[gid], 0)},
        {"name": gid, "bone": "card", "attachment": gid},
        {"name": f"{gid}_glow", "bone": "card", "color": "ffffff00"},
        {"name": f"{gid}_clip", "bone": "card"},
        {"name": f"{gid}_streak", "bone": "streak", "color": white_rgba(0)},
        {"name": f"{gid}_ring", "bone": "ring", "color": hex_rgba(TINTS[gid], 0)},
        *[
            {"name": f"{gid}_wisp{i}", "bone": f"wisp{i}",
             "color": hex_rgba(TINTS[gid], 0)}
            for i in (1, 2, 3)
        ],
        *[
            {"name": f"{gid}_shard{j}", "bone": f"shard{j}",
             "color": hex_rgba(TINTS[gid], 0.95)}
            for j in (1, 2, 3, 4)
        ],
    ]
    return slots


def rig_bones():
    return [
        {"name": "root"},
        {"name": "card", "parent": "root"},
        {"name": "streak", "parent": "card"},
        {"name": "ring", "parent": "root"},
        *[{"name": f"wisp{i}", "parent": "root"} for i in (1, 2, 3)],
        *[{"name": f"shard{j}", "parent": "root"} for j in (1, 2, 3, 4)],
    ]


def card_mesh():
    """A centered CELL x CELL grid mesh (MESH_GRID cells per axis) mapped 1:1
    onto the card region. Renders identically to the region at rest; the
    postWin deform timeline warps its vertices so the artwork itself ripples.
    Bone (y-up), top row -> v=0 so the image stays upright."""
    n = MESH_GRID
    cols = n + 1
    vertices = []
    uvs = []
    for row in range(cols):
        for col in range(cols):
            u = col / n
            v = row / n
            vertices += [-CELL / 2 + u * CELL, CELL / 2 - v * CELL]
            uvs += [u, v]
    triangles = []
    for row in range(n):
        for col in range(n):
            i0 = row * cols + col
            i1 = i0 + 1
            i2 = i0 + cols
            i3 = i2 + 1
            triangles += [i0, i2, i1, i1, i2, i3]
    return {
        "type": "mesh",
        "uvs": uvs,
        "triangles": triangles,
        "vertices": vertices,
        "hull": 2 * cols + 2 * (cols - 2),
        "width": CELL,
        "height": CELL,
    }


def rig_attachments(gid):
    rect = {"x": 0, "y": 0, "width": CELL, "height": CELL}
    # the card slot is a deformable mesh (hm stays a plain region: it does an
    # intact->cracked attachment swap and never rests in postWin)
    card_att = dict(rect) if gid == "hm" else {gid: card_mesh()}[gid]
    att = {
        f"{gid}_aura": {"fx_wisp": {"x": 0, "y": 0, "width": 384, "height": 384}},
        gid: {gid: card_att},
        f"{gid}_glow": {gid: dict(rect)},
        f"{gid}_clip": {
            "clip": {
                "type": "clipping",
                "end": f"{gid}_streak",
                "vertexCount": 4,
                "vertices": [-150, -150, 150, -150, 150, 150, -150, 150],
            }
        },
        f"{gid}_streak": {
            "fx_streak": {"x": 0, "y": 0, "rotation": -24,
                          "width": STREAK_W, "height": STREAK_H}
        },
        f"{gid}_ring": {"fx_ring": {"x": 0, "y": 0, "width": 220, "height": 220}},
    }
    for i in (1, 2, 3):
        att[f"{gid}_wisp{i}"] = {"fx_wisp": {"x": 0, "y": 0, "width": 96, "height": 96}}
    for j, variant in zip((1, 2, 3, 4), ("a", "b", "c", "a")):
        att[f"{gid}_shard{j}"] = {
            f"fx_shard_{variant}": {"x": 0, "y": 0, "width": 56, "height": 56}
        }
    if gid == "hm":
        att["hm"]["hm_cracked"] = dict(rect)
    return att


# ---------------------------------------------------------------- animations
# THE WHITE ROOM: per-symbol concepts (restraint / glare / glitch / shatter…).
# Madam Mirror shared punch+wobble+wisp pack is intentionally gone.


def win_animation(gid):
    return wr.win_animation(gid, TINTS[gid])


def land_animation(gid):
    return wr.land_animation(gid, TINTS[gid])


def postwin_animation(gid):
    return wr.postwin_animation(gid, mesh_grid=MESH_GRID)


def hm_break_animation():
    return wr.hm_break_animation(TINTS['hm'])


def skeleton_json(gid):
    data = {
        "skeleton": {
            "hash": f"mm-{gid}",
            "spine": SPINE_VERSION,
            "x": -CELL / 2,
            "y": -CELL / 2,
            "width": CELL,
            "height": CELL,
            "images": "./images/",
            "audio": "",
        },
        "bones": rig_bones(),
        "slots": rig_slots(gid),
        "skins": [{"name": "default", "attachments": rig_attachments(gid)}],
        "animations": {
            gid: win_animation(gid),
            f"{gid}_land": land_animation(gid),
            f"{gid}_static": {"bones": {"card": {"scale": [{"x": 1.0, "y": 1.0}]}}},
        },
    }
    if gid == "hm":
        data["animations"]["hm_break"] = hm_break_animation()
    else:
        # every paying/special card gets a looping postWin inhale
        data["animations"][f"{gid}_postwin"] = postwin_animation(gid)
    return data


# --------------------------------------------------------------------- main


def load_static_frame(atlas_img, atlas_json, frame_name):
    f = atlas_json["frames"][frame_name]["frame"]
    region = atlas_img.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]))
    return region.resize((CELL, CELL), Image.LANCZOS)


def build_cell(kind, ref, atlas_img, atlas_json):
    if kind == "card":
        return Image.open(os.path.join(CARD_DIR, ref)).convert("RGBA").resize((CELL, CELL), Image.LANCZOS)
    return load_static_frame(atlas_img, atlas_json, ref).convert("RGBA")


def rebuild_atlas():
    """Recompose the shared mm_symbols atlas from source art. Needs the card
    PNGs in symbol_art/ (h/l) plus the symbolsStatic atlas (w/s/hm)."""
    static_img = Image.open(os.path.join(ATLAS_STATIC_DIR, "symbolsStatic.webp")).convert("RGBA")
    with open(os.path.join(ATLAS_STATIC_DIR, "symbolsStatic.json"), encoding="utf-8") as f:
        static_json = json.load(f)

    all_regions = {**SYMBOLS, **EXTRA_REGIONS}
    cells = {
        region: build_cell(kind, ref, static_img, static_json)
        for region, (kind, ref) in all_regions.items()
    }
    for region, path in PLATE_FILES.items():
        if os.path.isfile(path):
            cells[region] = Image.open(path).convert("RGBA").resize((CELL, CELL), Image.LANCZOS)
            all_regions[region] = ("plate", path)

    # fx artwork (white, tinted at runtime by slot colors)
    fx = {
        "fx_streak": make_streak(),
        "fx_wisp": make_wisp(),
        "fx_ring": make_ring(),
        "fx_shard_a": make_shard(0),
        "fx_shard_b": make_shard(1),
        "fx_shard_c": make_shard(2),
    }

    # compose the shared atlas page: 4 columns of cards + an fx strip below
    regions = list(all_regions.keys())
    rows = (len(regions) + COLUMNS - 1) // COLUMNS
    page_w = COLUMNS * (CELL + PADDING) + PADDING
    cards_h = rows * (CELL + PADDING) + PADDING
    fx_h = STREAK_H + 2 * PADDING
    page_h = cards_h + fx_h
    page = Image.new("RGBA", (page_w, page_h), (0, 0, 0, 0))

    atlas_lines = ["mm_symbols.webp", f"size:{page_w},{page_h}", "filter:Linear,Linear", "scale:1"]
    for i, region in enumerate(regions):
        col, row = i % COLUMNS, i // COLUMNS
        x = PADDING + col * (CELL + PADDING)
        y = PADDING + row * (CELL + PADDING)
        page.paste(cells[region], (x, y))
        atlas_lines += [region, f"bounds:{x},{y},{CELL},{CELL}"]

    fx_x = PADDING
    for name, img in fx.items():
        page.paste(img, (fx_x, cards_h + PADDING))
        atlas_lines += [name, f"bounds:{fx_x},{cards_h + PADDING},{img.width},{img.height}"]
        fx_x += img.width + PADDING

    robust_save_image(page, os.path.join(OUT_DIR, "mm_symbols.png"))
    robust_save_image(page, os.path.join(OUT_DIR, "mm_symbols.webp"), lossless=True)
    robust_write_text(os.path.join(OUT_DIR, "mm_symbols.atlas"), "\n".join(atlas_lines) + "\n")
    print(f"wrote atlas {page_w}x{page_h} with {len(regions) + len(fx)} regions")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)

    # The card pixels already live in the committed mm_symbols atlas, so the
    # skeletons (mesh + postWin ripple) can be regenerated without the source
    # art. Rebuild the atlas image only when the sources are present and the
    # caller didn't ask for skeletons-only.
    have_sources = os.path.isdir(CARD_DIR) and any(
        os.path.exists(os.path.join(CARD_DIR, ref))
        for kind, ref in SYMBOLS.values()
        if kind == "card"
    )
    skeletons_only = "--skeletons-only" in sys.argv or not have_sources
    if skeletons_only:
        print("skeletons-only: reusing the existing mm_symbols atlas (no image rebuild)")
    else:
        rebuild_atlas()

    for gid in SYMBOLS:
        robust_write_text(os.path.join(OUT_DIR, f"{gid}.json"), json.dumps(skeleton_json(gid)))
        print(f"wrote {gid}.json")

    # Storybook / chromatic bundle helper (mirrors the other spine folders)
    keymap = {
        "h1": "H1", "h2": "H2", "h3": "H3", "h4": "H4", "h5": "H5",
        "l1": "L1", "l2": "L2", "l3": "L3", "l4": "L4", "l5": "L5",
        "w": "W", "s": "S", "hm": "HM",
    }
    index_lines = [
        "import { createAsset } from 'pixi-svelte';",
        "",
        "import img from './mm_symbols.webp';",
        "import rawAtlas from './mm_symbols.atlas?raw';",
    ]
    for region, key in keymap.items():
        index_lines.append(f"import {key} from './{region}.json';")
    index_lines += ["", "export default createAsset({", "\timg,", "\trawAtlas,", "\tspines: {"]
    index_lines += [f"\t\t{key}," for key in keymap.values()]
    index_lines += ["\t},", "});", ""]
    robust_write_text(os.path.join(OUT_DIR, "index.ts"), "\n".join(index_lines) + "\n")
    print("wrote index.ts")
    print(f"\ndone -> {OUT_DIR}")
