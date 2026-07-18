"""Generate Spine skeletons + a shared atlas for the Madam Mirror symbol set.

Every paying symbol (h1-h5, l1-l5) plus the specials (w, s, hm) becomes a real
multi-layer Spine 4.1 rig. Each skeleton carries, in draw order:

    aura      soft additive halo breathing behind the card
    card      the full-bleed 300x300 artwork
    glow      additive duplicate of the card (classic slot glow flash)
    clip      clipping polygon glued to the card bone (bounds the streak)
    streak    diagonal specular sheen that sweeps across the glass
    ring      expanding shockwave ring
    wisp x3   spectral wisps that drift out of the card
    shard x4  glass slivers that burst to the corners

and the animations driven by the game states in constants.ts:

    <id>          win   (~0.9s)  dip -> punch + wobble + glow flash + sheen
                                 sweeps + ring shockwave + shards + wisps
                                 (the green plasma border is NOT here: the
                                 PlasmaLiner draws one merged outline around
                                 the whole connected combination)
    <id>_land     land  (~0.36s) weighty squash-and-stretch, bottom-pinned
                                 (no ring pulse, no glow pop)
    hm_break      HM only: glow burst + intact -> cracked swap + shards

static, spin, postWin and postWinStatic are SPRITE states (crisp card, smear
frame, burning card, crisp card), so those animations no longer exist here.

FX layers are tinted per symbol class: violet for the portraits, seance green
for the letters, deep violet for WILD, amber for SCATTER, pale spectral for
the Haunted Mirror.

The runtime is @esotericsoftware/spine-pixi-v8 4.2.74, which loads 4.1 JSON.
Attachment names match atlas region names (the Spine naming contract). Output
lands in static/assets/spines/mm_symbols/ (mm_symbols.atlas/.webp/.png + one
JSON per symbol + index.ts for the Storybook bundle).

Run:  python tools/gen_symbol_spines.py
"""

import json
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
CARD_DIR = os.path.join(HERE, "symbol_art")
ATLAS_STATIC_DIR = os.path.normpath(
    os.path.join(HERE, "..", "static", "assets", "sprites", "symbolsStatic")
)
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "spines", "mm_symbols"))

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
SYMBOLS = {
    "h1": ("card", "card_h1_lady_mirror.png"),
    "h2": ("card", "card_h2_wife.png"),
    "h3": ("card", "card_h3_man.png"),
    "h4": ("card", "card_h4_little_girl.png"),
    "h5": ("card", "card_h5_dog.png"),
    "l1": ("card", "card_l1_ace.png"),
    "l2": ("card", "card_l2_king.png"),
    "l3": ("card", "card_l3_queen.png"),
    "l4": ("card", "card_l4_jack.png"),
    "l5": ("card", "card_l5_ten.png"),
    "w": ("frame", "w.png"),
    "s": ("frame", "s.png"),
    "hm": ("frame", "hm_intact.png"),
}

# atlas-only regions (no skeleton of their own; used by attachment swaps)
EXTRA_REGIONS = {
    "hm_cracked": ("frame", "hm_cracked.png"),
}

# per-class fx tint (r, g, b) 0..1
TINTS = {
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
    """Soft wisp: stacked offset gaussians with a trailing tail."""
    size = WISP_SIZE
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    cx = size / 2
    a = np.zeros((size, size), dtype=np.float32)
    for (oy, sx, sy, w) in ((-8, 11, 13, 1.0), (6, 8, 15, 0.7), (18, 5, 12, 0.45)):
        a += w * np.exp(
            -(((xx - cx) / sx) ** 2 + ((yy - (size / 2 + oy)) / sy) ** 2)
        )
    a = np.clip(a / a.max(), 0, 1) ** 1.15
    img = np.zeros((size, size, 4), dtype=np.uint8)
    img[..., :3] = 255
    img[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(img, "RGBA")


def make_ring():
    """Thin annulus with gaussian profile + faint inner fill."""
    size = RING_SIZE
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    c = size / 2
    r = np.sqrt((xx - c) ** 2 + (yy - c) ** 2)
    ring = np.exp(-(((r - size * 0.40) / (size * 0.045)) ** 2))
    inner = np.clip(1 - r / (size * 0.40), 0, 1) * 0.10
    a = np.clip(ring + inner, 0, 1)
    img = np.zeros((size, size, 4), dtype=np.uint8)
    img[..., :3] = 255
    img[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(img, "RGBA")


def make_shard(variant):
    """Sharp glass sliver with an alpha gradient along its length."""
    ss = 4
    size = SHARD_SIZE * ss
    img = Image.new("L", (size, size), 0)
    from PIL import ImageDraw

    d = ImageDraw.Draw(img)
    c = size / 2
    shapes = {
        0: [(0.0, -0.46), (0.20, -0.05), (0.07, 0.46), (-0.16, 0.05)],
        1: [(0.0, -0.42), (0.26, 0.10), (0.0, 0.42), (-0.12, 0.02)],
        2: [(-0.05, -0.48), (0.16, -0.12), (0.10, 0.44), (-0.20, 0.10)],
    }[variant]
    d.polygon([(c + px * size, c + py * size) for px, py in shapes], fill=255)
    a = np.asarray(img, dtype=np.float32) / 255.0
    yy = np.mgrid[0:size, 0:size][0].astype(np.float32)
    grad = 0.55 + 0.45 * (1 - yy / size)  # brighter tip, softer tail
    a = np.clip(a * grad, 0, 1)
    small = Image.fromarray((a * 255).astype(np.uint8), "L").resize(
        (SHARD_SIZE, SHARD_SIZE), Image.LANCZOS
    )
    out = Image.new("RGBA", (SHARD_SIZE, SHARD_SIZE), (255, 255, 255, 0))
    out.putalpha(small)
    return out


# ------------------------------------------------------------- rig building


def rig_slots(gid):
    """Slot list in draw order (first = drawn behind)."""
    return [
        {"name": f"{gid}_aura", "bone": "card", "color": hex_rgba(TINTS[gid], 0),
         "attachment": "fx_wisp", "blend": "additive"},
        {"name": gid, "bone": "card", "attachment": gid},
        {"name": f"{gid}_glow", "bone": "card", "color": "ffffff00",
         "attachment": gid, "blend": "additive"},
        {"name": f"{gid}_clip", "bone": "card", "attachment": "clip"},
        {"name": f"{gid}_streak", "bone": "streak", "color": white_rgba(0),
         "attachment": "fx_streak", "blend": "additive"},
        {"name": f"{gid}_ring", "bone": "ring", "color": hex_rgba(TINTS[gid], 0),
         "attachment": "fx_ring", "blend": "additive"},
        *[
            {"name": f"{gid}_wisp{i}", "bone": f"wisp{i}",
             "color": hex_rgba(TINTS[gid], 0), "attachment": "fx_wisp",
             "blend": "additive"}
            for i in (1, 2, 3)
        ],
        *[
            {"name": f"{gid}_shard{j}", "bone": f"shard{j}",
             "color": hex_rgba(TINTS[gid], 0.95)}
            for j in (1, 2, 3, 4)
        ],
    ]


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


def win_animation(gid):
    """Anticipation dip -> punch + wobble, double glow flash, sheen sweep,
    ring shockwave, corner shards, wisps. ~0.9s. The green plasma border is
    NOT part of the skeleton: PlasmaLiner draws one merged flame outline
    around the whole connected combination on top of the board."""
    tint = TINTS[gid]
    slots = {
        f"{gid}_glow": {
            "rgba": [
                {"color": "ffffff00"},
                {"time": 0.12, "color": "ffffffbf"},
                {"time": 0.28, "color": "ffffff33"},
                {"time": 0.42, "color": "ffffff80"},
                {"time": 0.62, "color": "ffffff1a"},
                {"time": 0.85, "color": "ffffff00"},
            ]
        },
        f"{gid}_aura": {
            "rgba": [
                {"color": hex_rgba(tint, 0.0)},
                {"time": 0.16, "color": hex_rgba(tint, 0.40)},
                {"time": 0.55, "color": hex_rgba(tint, 0.18)},
                {"time": 0.85, "color": hex_rgba(tint, 0.0)},
            ]
        },
        f"{gid}_streak": {
            "rgba": [
                {"color": white_rgba(0)},
                {"time": 0.08, "color": white_rgba(0.85)},
                {"time": 0.30, "color": white_rgba(0.85)},
                {"time": 0.34, "color": white_rgba(0)},
                {"time": 0.42, "color": white_rgba(0.55)},
                {"time": 0.62, "color": white_rgba(0.55)},
                {"time": 0.66, "color": white_rgba(0)},
            ]
        },
        f"{gid}_ring": {
            "rgba": [
                {"color": hex_rgba(tint, 0)},
                {"time": 0.10, "color": hex_rgba(tint, 0)},
                {"time": 0.16, "color": hex_rgba(tint, 0.75)},
                {"time": 0.55, "color": hex_rgba(tint, 0)},
            ]
        },
    }
    bones = {
        "card": {
            "scale": [
                {},
                {"time": 0.06, "x": 0.94, "y": 0.94},
                {"time": 0.16, "x": 1.18, "y": 1.18},
                {"time": 0.30, "x": 0.965, "y": 0.965},
                {"time": 0.44, "x": 1.09, "y": 1.09},
                {"time": 0.60, "x": 1.0, "y": 1.0},
            ],
            "rotate": [
                {},
                {"time": 0.10, "value": -3},
                {"time": 0.22, "value": 4.2},
                {"time": 0.36, "value": -3.2},
                {"time": 0.50, "value": 1.8},
                {"time": 0.64, "value": 0},
            ],
            "shear": [
                {},
                {"time": 0.14, "x": 2.5},
                {"time": 0.30, "x": -2.0},
                {"time": 0.46, "x": 1.2},
                {"time": 0.60, "x": 0},
            ],
        },
        "streak": {
            "translate": [
                {"x": -300},
                {"time": 0.32, "x": 300, "curve": "stepped"},
                {"time": 0.40, "x": -300},
                {"time": 0.66, "x": 300},
            ]
        },
        "ring": {
            "scale": [
                {"x": 0.5, "y": 0.5},
                {"time": 0.10, "x": 0.5, "y": 0.5},
                {"time": 0.55, "x": 1.7, "y": 1.7},
            ]
        },
    }
    # wisps fan out: up-left, up, up-right
    for i, angle in zip((1, 2, 3), (-135, -90, -45)):
        rad = math.radians(angle)
        dx, dy = math.cos(rad) * 78, math.sin(rad) * 78
        slots[f"{gid}_wisp{i}"] = {
            "rgba": [
                {"color": hex_rgba(tint, 0)},
                {"time": 0.10, "color": hex_rgba(tint, 0)},
                {"time": 0.24, "color": hex_rgba(tint, 0.65)},
                {"time": 0.70, "color": hex_rgba(tint, 0)},
            ]
        }
        bones[f"wisp{i}"] = {
            "translate": [
                {"x": dx * 0.15, "y": dy * 0.15},
                {"time": 0.10, "x": dx * 0.15, "y": dy * 0.15},
                {"time": 0.70, "x": dx, "y": dy - 26},
            ],
            "scale": [
                {"x": 0.7, "y": 0.7},
                {"time": 0.70, "x": 1.2, "y": 1.2},
            ],
        }
    # shards burst to the four corners
    for j, (sx, sy) in zip((1, 2, 3, 4), ((-1, -1), (1, -1), (1, 1), (-1, 1))):
        slots[f"{gid}_shard{j}"] = {
            "attachment": [
                {"name": None},
                {"time": 0.10, "name": f"fx_shard_{['a','b','c','a'][j-1]}"},
                {"time": 0.62, "name": None},
            ],
            "rgba": [
                {"color": hex_rgba(tint, 0)},
                {"time": 0.10, "color": hex_rgba(tint, 0.95)},
                {"time": 0.60, "color": hex_rgba(tint, 0)},
            ],
        }
        bones[f"shard{j}"] = {
            "translate": [
                {"time": 0.10, "x": sx * 24, "y": sy * 24},
                {"time": 0.60, "x": sx * 118, "y": sy * 118 - 18},
            ],
            "rotate": [
                {"time": 0.10, "value": 0},
                {"time": 0.60, "value": (160 + 40 * j) * (1 if sx > 0 else -1)},
            ],
            "scale": [
                {"time": 0.10, "x": 1.0, "y": 1.0},
                {"time": 0.60, "x": 0.65, "y": 0.65},
            ],
        }
    return {"slots": slots, "bones": bones}


def land_animation(gid):
    """Weighty squash-and-stretch settle, bottom-pinned so the card visibly
    slams into the row and absorbs its own momentum. No ring pulse, no glow
    pop, no dust - pure mass. (+y is down in the rendered rig.)"""
    return {
        "bones": {
            "card": {
                # squash keeps the bottom edge pinned: translate compensates
                # scale so the card crushes INTO the row, then rebounds
                "scale": [
                    {"x": 1.17, "y": 0.78},
                    {"time": 0.11, "x": 0.93, "y": 1.08},
                    {"time": 0.21, "x": 1.035, "y": 0.965},
                    {"time": 0.29, "x": 0.99, "y": 1.006},
                    {"time": 0.36, "x": 1.0, "y": 1.0},
                ],
                "translate": [
                    {"y": 33},
                    {"time": 0.11, "y": -12},
                    {"time": 0.21, "y": 5},
                    {"time": 0.29, "y": -1},
                    {"time": 0.36, "y": 0},
                ],
            },
        },
    }


def postwin_animation(gid):
    """Looping ~2.6s deform that ripples the card MESH: the winning symbol's
    own artwork gently undulates like a haunted, living photograph (a real
    animation of the image, not a glow/effect layered on top).

    A sin^2 envelope (0 at both ends, peak mid-loop) makes the ripple ease up
    from FLAT and return to flat, so the loop is C1-seamless AND matches the
    win animation's undisplaced end pose (no pop at the win->postWin handoff).
    A traveling phase keeps the pixels flowing while the envelope swells. Edge
    vertices are damped so the card never leaves its cell."""
    n = MESH_GRID
    cols = n + 1
    period = 2.6
    steps = 12
    amp_y = 18.0  # vertical ripple (skeleton px; ~9px on the 145px cell)
    amp_x = 12.0  # horizontal sway
    keys = []
    for step in range(steps + 1):
        p = step / steps
        travel = 2 * math.pi * p  # one traversal per loop -> pixels flow
        env = 0.5 - 0.5 * math.cos(2 * math.pi * p)  # sin^2: 0 -> 1 -> 0, C1 seam
        deltas = []
        for row in range(cols):
            for col in range(cols):
                nx = (col / n) * 2 - 1  # -1 left .. +1 right
                ny = 1 - (row / n) * 2  # +1 top .. -1 bottom
                damp = 0.6 + 0.4 * (1 - max(abs(nx), abs(ny)))
                dx = amp_x * env * math.sin(travel + math.pi * 0.9 * nx + 0.6 * ny) * damp
                dy = amp_y * env * math.sin(travel + math.pi * 1.1 * ny) * damp
                deltas += [round(dx, 2), round(dy, 2)]
        key = {"offset": 0, "vertices": deltas}
        if step > 0:
            key["time"] = round(p * period, 4)
        keys.append(key)
    # 4.2 nests mesh deform under attachments -> skin -> slot -> attachment ->
    # "deform" (the old top-level 4.1 "deform" key is ignored by this runtime).
    return {"attachments": {"default": {gid: {gid: {"deform": keys}}}}}


# static, postWinStatic are SPRITE states (pure static card, crisp card for the
# apparition pane slicing). postWin is now the <id>_postwin looping mesh deform.


def hm_break_animation():
    """Haunted Mirror burst: hard flash, intact -> cracked swap, ring
    shockwave and glass shards (~0.6s)."""
    tint = TINTS["hm"]
    slots = {
        "hm": {"attachment": [{"name": "hm"}, {"time": 0.18, "name": "hm_cracked"}]},
        "hm_glow": {
            "rgba": [
                {"color": "ffffff00"},
                {"time": 0.12, "color": "ffffffcc"},
                {"time": 0.22, "color": "ffffff40"},
                {"time": 0.60, "color": "ffffff00"},
            ]
        },
        "hm_ring": {
            "rgba": [
                {"color": hex_rgba(tint, 0)},
                {"time": 0.14, "color": hex_rgba(tint, 0)},
                {"time": 0.20, "color": hex_rgba(tint, 0.85)},
                {"time": 0.60, "color": hex_rgba(tint, 0)},
            ]
        },
    }
    bones = {
        "card": {
            "scale": [
                {},
                {"time": 0.12, "x": 1.14, "y": 1.14},
                {"time": 0.30, "x": 0.96, "y": 0.96},
                {"time": 0.45, "x": 1.0, "y": 1.0},
            ]
        },
        "ring": {
            "scale": [
                {"x": 0.4, "y": 0.4},
                {"time": 0.14, "x": 0.4, "y": 0.4},
                {"time": 0.60, "x": 1.8, "y": 1.8},
            ]
        },
    }
    for j, (sx, sy) in zip((1, 2, 3, 4), ((-1, -1), (1, -1), (1, 1), (-1, 1))):
        slots[f"hm_shard{j}"] = {
            "attachment": [
                {"name": None},
                {"time": 0.18, "name": f"fx_shard_{['a','b','c','a'][j-1]}"},
                {"time": 0.60, "name": None},
            ],
            "rgba": [
                {"color": hex_rgba(tint, 0)},
                {"time": 0.18, "color": hex_rgba(tint, 0.95)},
                {"time": 0.58, "color": hex_rgba(tint, 0)},
            ],
        }
        bones[f"shard{j}"] = {
            "translate": [
                {"time": 0.18, "x": sx * 20, "y": sy * 20},
                {"time": 0.58, "x": sx * 125, "y": sy * 125 - 20},
            ],
            "rotate": [
                {"time": 0.18, "value": 0},
                {"time": 0.58, "value": (180 + 30 * j) * (1 if sx > 0 else -1)},
            ],
        }
    return {"slots": slots, "bones": bones}


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
        },
    }
    if gid == "hm":
        data["animations"]["hm_break"] = hm_break_animation()
    else:
        # every paying/special card gets a looping postWin mesh ripple
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

    page.save(os.path.join(OUT_DIR, "mm_symbols.png"))
    page.save(os.path.join(OUT_DIR, "mm_symbols.webp"), lossless=True)
    with open(os.path.join(OUT_DIR, "mm_symbols.atlas"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(atlas_lines) + "\n")
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
        with open(os.path.join(OUT_DIR, f"{gid}.json"), "w", encoding="utf-8") as f:
            json.dump(skeleton_json(gid), f)
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
    with open(os.path.join(OUT_DIR, "index.ts"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(index_lines))
    print("wrote index.ts")
    print(f"\ndone -> {OUT_DIR}")
