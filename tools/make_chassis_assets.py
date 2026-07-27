"""Key the cell-block chassis art off its magenta plate and locate its openings.

The chassis is three heavy iron blocks (left column, right column, bottom beam),
each generated on a flat FF00FF plate with its three cell openings punched
straight through as more flat magenta. Keying turns the plate AND the openings
into alpha in one pass, which is exactly what we want: the openings become real
holes the game can drop a symbol through.

The point of this tool is the MEASUREMENT. Rather than authoring the art to match
hardcoded cell coordinates - which never survives a regenerated asset - we detect
where the openings actually landed and let the game read those positions back.
An opening is an alpha hole that does NOT touch the border (the surrounding plate
does), so flood-filling transparency in from the edge separates "outside" from
"opening", and labelling what's left gives one component per opening.

Openings are reported as fractions of the cropped tile, so they survive any
rescale: the game scales a block until its openings are the size it wants, then
positions the block from those same fractions.

Usage: python tools/make_chassis_assets.py
Writes web-sdk/apps/white-room/assets/sprites/mirror/chassis_*.png plus the
background plate, and prints the metrics block for cellChassis.ts.
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

SRC_DIR = Path.home() / ".cursor/projects/c-Users-Emex33-Desktop-stakez/assets"
OUT_DIR = Path("web-sdk/apps/white-room/assets/sprites/mirror")
SCENE_DIR = Path("web-sdk/apps/white-room/assets/sprites/scene")

KEY_LO, KEY_HI = 40.0, 110.0
HOLE = 0.5  # alpha below this counts as a hole when tracing openings
MIN_AREA = 0.004  # ignore specks: an opening is >=0.4% of the tile


def key_magenta(path: Path) -> np.ndarray:
    """RGBA float array with the magenta plate (and the punched openings) keyed."""
    arr = np.asarray(Image.open(path).convert("RGBA")).astype(np.float32)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    excess = np.minimum(r, b) - g  # "magenta-ness"
    alpha = 1.0 - np.clip((excess - KEY_LO) / (KEY_HI - KEY_LO), 0.0, 1.0)
    keep = alpha > 0.0
    for ch in (r, b):  # spill suppression, so no magenta rim survives
        bleed = keep & (ch > g)
        ch[bleed] = g[bleed]
    return np.dstack([r, g, b, alpha * 255.0])


def crop_to_content(rgba: np.ndarray) -> np.ndarray:
    a = rgba[..., 3]
    rows = np.where(a.max(axis=1) > 8)[0]
    cols = np.where(a.max(axis=0) > 8)[0]
    return np.ascontiguousarray(rgba[rows[0] : rows[-1] + 1, cols[0] : cols[-1] + 1, :])


def openings(rgba: np.ndarray) -> list[dict]:
    """Interior alpha holes, as centre/size fractions of the tile, reading order."""
    h, w = rgba.shape[:2]
    transparent = rgba[..., 3] < HOLE * 255

    # Flood transparency in from the border: whatever it reaches is the outside
    # of the block, so the transparency it CANNOT reach is a punched opening.
    labels, n = ndimage.label(transparent)
    border = set(labels[0, :]) | set(labels[-1, :]) | set(labels[:, 0]) | set(labels[:, -1])
    border.discard(0)

    found = []
    for i in range(1, n + 1):
        if i in border:
            continue
        ys, xs = np.where(labels == i)
        if len(ys) < MIN_AREA * h * w:
            continue
        found.append(
            {
                "cx": round(float(xs.mean()) / w, 5),
                "cy": round(float(ys.mean()) / h, 5),
                "w": round(float(xs.max() - xs.min() + 1) / w, 5),
                "h": round(float(ys.max() - ys.min() + 1) / h, 5),
            }
        )
    # reading order: top-to-bottom, then left-to-right, so a column comes out
    # 0,1,2 downward and the bottom beam comes out 0,1,2 rightward
    found.sort(key=lambda o: (round(o["cy"], 2), o["cx"]))
    return found


# --- moving parts -------------------------------------------------------------
# The cogs, the hanging counterweights and the beam's chain swags have to leave
# the block art to be animated at all: a sprite can only turn or travel as a
# whole. So they are cut out here into their own sprites and the block keeps
# everything that never moves. CellChassis draws them back in the same places
# (chassisArt.ts carries the geometry) and drives them when a cell opens.
#
# Measured on the keyed side block (605x1505) and beam (1510x603). They are
# stored as fractions so they survive the rescale the game does, and they are
# re-measured by eye only if the art is regenerated.
SIDE_COGS = [(306, 103, 92), (305, 1394, 96)]  # cx, cy, tooth-tip radius
SIDE_CHAIN_X = 60  # left of this is free-hanging chain + counterweights only;
# the run of chain further right is drawn over solid plate and stays baked.
BEAM_SWAG_Y = 543  # below the bottom rail: the draped chain swags

COG_PAD = 3  # keeps the tooth tips off the sprite edge when it turns
# The gear casts a tooth-shaped shadow on the plate well outside its own tips.
# The socket has to swallow that too, or the shadow stays put while the gear
# turns and every tooth reads double.
COG_SOCKET = 20


def sample_ring(rgba: np.ndarray, cx: int, cy: int, r: int) -> np.ndarray:
    """Median colour of the plate just outside a disc, to blend a patch into it."""
    h, w = rgba.shape[:2]
    ys, xs = np.ogrid[:h, :w]
    d = np.hypot(xs - cx, ys - cy)
    ring = (d > r + 2) & (d < r + 14) & (rgba[..., 3] > 200)
    return np.median(rgba[ring][:, :3], axis=0) if ring.any() else np.array([60.0, 60.0, 60.0])


def cut_disc(rgba: np.ndarray, cx: int, cy: int, r: int) -> np.ndarray:
    """Lift a disc out as its own sprite and leave a machined socket behind.

    The socket matters: the gear is drawn back on top, so what shows through the
    gaps between its teeth is this recess rather than a hole in the block.
    """
    rr = r + COG_PAD
    patch = np.zeros((rr * 2, rr * 2, 4), np.float32)
    y0, y1, x0, x1 = cy - rr, cy + rr, cx - rr, cx + rr
    src = rgba[max(y0, 0) : y1, max(x0, 0) : x1, :]
    patch[max(0, -y0) : max(0, -y0) + src.shape[0], max(0, -x0) : max(0, -x0) + src.shape[1]] = src

    ys, xs = np.ogrid[: rr * 2, : rr * 2]
    d = np.hypot(xs - rr, ys - rr)
    patch[..., 3] *= np.clip(r + 1 - d, 0.0, 1.0)  # feathered disc edge

    # socket: a dark recess that lightens toward the rim, plus a lit lip
    socket = r + COG_SOCKET
    h, w = rgba.shape[:2]
    gys, gxs = np.ogrid[:h, :w]
    gd = np.hypot(gxs - cx, gys - cy)
    plate = sample_ring(rgba, cx, cy, socket)
    inside = gd <= socket + 1
    t = np.clip(gd / max(socket, 1), 0.0, 1.0)[inside][:, None]
    recess = plate[None, :] * (0.22 + 0.5 * t**2)
    lip = np.clip((t - 0.9) / 0.1, 0.0, 1.0)
    recess = recess * (1 - lip) + plate[None, :] * 1.15 * lip
    rgba[inside, :3] = np.clip(recess, 0, 255)
    rgba[inside, 3] = 255
    return patch


def cut_region(rgba: np.ndarray, box: tuple[int, int, int, int]) -> np.ndarray:
    """Lift a rectangle out as its own sprite, clearing it from the block."""
    x0, y0, x1, y1 = box
    patch = np.ascontiguousarray(rgba[y0:y1, x0:x1, :].copy())
    rgba[y0:y1, x0:x1, 3] = 0.0
    return patch


def save(rgba: np.ndarray, name: str) -> None:
    Image.fromarray(rgba.astype(np.uint8), "RGBA").save(OUT_DIR / f"{name}.png")


metrics: dict[str, dict] = {}
OUT_DIR.mkdir(parents=True, exist_ok=True)


def emit(rgba: np.ndarray, name: str) -> None:
    holes = openings(rgba)
    h, w = rgba.shape[:2]
    Image.fromarray(rgba.astype(np.uint8), "RGBA").save(OUT_DIR / f"chassis_{name}.png")
    metrics[name] = {"w": w, "h": h, "cells": holes}
    if len(holes) != 3:
        print(f"!! {name}: found {len(holes)} openings, expected 3")


# ONE side block, mirrored for the right column. Both sides have to hold their
# openings on the board's row pitch, and solving for that pitch with two
# differently-proportioned arts gave openings ~20% apart in size. Mirroring a
# single master keeps the two columns identical and the frame symmetrical. It is
# also why the plates are blank: mirrored baked numbers would read backwards, so
# LockedSlots draws the cell numbers as runtime Text instead.
side = crop_to_content(key_magenta(SRC_DIR / "raw_chassis_side.png"))
beam = crop_to_content(key_magenta(SRC_DIR / "raw_chassis_beam.png"))

# Cut the movers out BEFORE the side block is mirrored, so both columns lose the
# same pixels and the right column's parts are simply the left's mirrored — the
# two sides stay identical, which is the whole reason there is one master art.
# Both cogs are the same gear at slightly different sizes, so only the first is
# kept as a sprite and the game scales it to each socket.
cog = cut_disc(side, *SIDE_COGS[0])
cut_disc(side, *SIDE_COGS[1])
chain = cut_region(side, (0, 0, SIDE_CHAIN_X, side.shape[0]))
swag = cut_region(beam, (0, BEAM_SWAG_Y, beam.shape[1], beam.shape[0]))

save(cog, "chassis_cog")
save(chain, "chassis_chain_l")
save(np.ascontiguousarray(chain[:, ::-1, :]), "chassis_chain_r")
save(swag, "chassis_swag")

emit(side, "side_l")
emit(np.ascontiguousarray(side[:, ::-1, :]), "side_r")
emit(beam, "beam")

side_h, side_w = side.shape[:2]
beam_h, beam_w = beam.shape[:2]
metrics["movers"] = {
    # r is the SPRITE half-size (tips + pad), i.e. what the game scales the cog
    # sprite to, not the tooth-tip radius.
    "cogs": [
        {
            "cx": round(cx / side_w, 5),
            "cy": round(cy / side_h, 5),
            "r": round((r + COG_PAD) / side_h, 5),
        }
        for cx, cy, r in SIDE_COGS
    ],
    "chainW": round(SIDE_CHAIN_X / side_w, 5),
    "swagY": round(BEAM_SWAG_Y / beam_h, 5),
}

# background plate: no keying, just a graded copy at the size Background.svelte
# cover-fits from (SCENE_ART)
SCENE_DIR.mkdir(parents=True, exist_ok=True)
bg = Image.open(SRC_DIR / "raw_scene_cellblock_bg.png").convert("RGB")
bg = bg.resize((1536, 1024), Image.LANCZOS)
bg.save(SCENE_DIR / "scene_bg_cellblock.webp", quality=92, method=6)
metrics["background"] = {"w": 1536, "h": 1024}

print(json.dumps(metrics, indent=2))
