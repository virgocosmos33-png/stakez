"""Bake the board frame as ONE transparent PNG, pre-shaped to the authored
diamond staircase, so the frontend just places a sprite (no runtime masking).

TOMBSTONE R.I.P. STYLE: the frame is no longer a flat wood ring — every edge of
the staircase carries a REAL painted timber plank (cut from a generated plank
sheet), laid along the edge with rough split ends OVERHANGING past each corner,
so the outline reads as rough nailed-together graveyard carpentry. The inside
is fully transparent (the scene shows through while the reels spin); iron bolt
heads pin the joints.

The shape replicates src/game geometry EXACTLY:
  - SYMBOL_SIZE solved from PORTRAIT_DESIGN_W (chassisArt.ts)
  - CELL_PITCH_X = SYMBOL_SIZE * 0.8, column left edges at (i + 0.03) * pitch
  - per-reel y offsets: centered on MAX_ROWS, EXCEPT the last reel which is
    centered on its left neighbour (utils.getReelYOffset special lane rule)
  - planks are centered on the mid-ring (outline offset by BORDER/2)

Output: assets/sprites/board/board_frame.png (+ static tree), drawn at SCALE x
resolution. The canvas is the BORDER-grown outer box grown again by MARGIN on
every side (for the plank overhangs) — BoardPlate.svelte's frameBox MUST use
the same BORDER + MARGIN. Re-run after any board-shape change.
"""

import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
GEN_DIR = os.path.normpath(
    os.path.join(
        os.path.expanduser("~"),
        ".cursor",
        "projects",
        "c-Users-Emex33-Desktop-stakez",
        "assets",
    )
)
# chunky 2-3 board assemblies with ragged split ends, nails, chains and blood
# baked in (generated over the user's approved black-frame reference)
PLANK_SHEET = os.path.join(GEN_DIR, "tr_frame_planks_v2.png")
# discrete offcut pieces on black (crossed boards, chain wraps, splinter
# shards, strap plates, paper scrap) laid over the corners/joints
SCRAP_SHEET = os.path.join(GEN_DIR, "tr_frame_scraps.png")

# --- geometry (mirror of chassisArt.ts / utils.ts) -----------------------------
GEN_NUM_REELS = 6
NUM_ROWS = [3, 4, 4, 2, 2, 1]
MAX_ROWS = max(NUM_ROWS)
COLUMN_PITCH_SCALE = 0.8
REEL_PADDING = 0.53
PORTRAIT_DESIGN_W = 960
SIDE_H_SCALE = MAX_ROWS * 1.15 * 0.78
SIDE_W_SCALE = SIDE_H_SCALE * 355 / 1505
SYMBOL_SIZE = math.floor(
    PORTRAIT_DESIGN_W / ((GEN_NUM_REELS + 1) * COLUMN_PITCH_SCALE + SIDE_W_SCALE)
)
PITCH = SYMBOL_SIZE * COLUMN_PITCH_SCALE

BORDER = 30       # nominal frame thickness (board units) — keep BoardPlate in sync
MARGIN = 60       # extra canvas on every side for overhangs + tilted planks — BoardPlate too
INNER_INSET = 2   # kept for reference (BoardPlate's old silhouette inset)
SCALE = 2         # supersample for crisp detail

PLANK_THICK = 48   # nominal plank width across the frame line (board units)
PLANK_OVERHANG = 34  # split ends run this far past each corner (board units)


def columns():
    cols = []
    for i, rows in enumerate(NUM_ROWS):
        if i == len(NUM_ROWS) - 1:
            neighbor = NUM_ROWS[i - 1]
            noff = (MAX_ROWS - neighbor) / 2 * SYMBOL_SIZE
            top = noff + (neighbor - rows) / 2 * SYMBOL_SIZE
        else:
            top = (MAX_ROWS - rows) / 2 * SYMBOL_SIZE
        left = (i + REEL_PADDING) * PITCH - PITCH / 2
        cols.append(
            {"left": left, "right": left + PITCH, "top": top, "bottom": top + rows * SYMBOL_SIZE}
        )
    return cols


def base_outline(cols):
    """Exact staircase outline of the cells (clockwise, axis-aligned)."""
    pts = []
    first, last = cols[0], cols[-1]
    pts.append((first["left"], first["top"]))
    for i in range(1, len(cols)):
        pts.append((cols[i]["left"], cols[i - 1]["top"]))
        pts.append((cols[i]["left"], cols[i]["top"]))
    pts.append((last["right"], last["top"]))
    pts.append((last["right"], last["bottom"]))
    for i in range(len(cols) - 1, 0, -1):
        pts.append((cols[i]["left"], cols[i]["bottom"]))
        pts.append((cols[i]["left"], cols[i - 1]["bottom"]))
    pts.append((first["left"], first["bottom"]))
    return pts


def offset_rectilinear(pts, pad):
    """TRUE offset of a clockwise rectilinear polygon: every edge moves `pad`
    along its outward normal (so step VERTICALS gain thickness too, which the
    old y-only padding never gave them). Positive pad grows, negative insets."""
    clean = []
    for p in pts:
        if not clean or abs(p[0] - clean[-1][0]) + abs(p[1] - clean[-1][1]) > 1e-6:
            clean.append(p)
    if abs(clean[0][0] - clean[-1][0]) + abs(clean[0][1] - clean[-1][1]) < 1e-6:
        clean.pop()

    # each edge becomes an offset line: vertical -> x' , horizontal -> y'
    lines = []
    n = len(clean)
    for i in range(n):
        x1, y1 = clean[i]
        x2, y2 = clean[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        if abs(dx) >= abs(dy):  # horizontal edge, outward normal (0, -sign(dx))
            lines.append(("h", y1 - pad * (1 if dx > 0 else -1)))
        else:  # vertical edge, outward normal (sign(dy), 0)
            lines.append(("v", x1 + pad * (1 if dy > 0 else -1)))

    # merge consecutive same-orientation (collinear) edges
    merged = []
    for ln in lines:
        if merged and merged[-1][0] == ln[0] and abs(merged[-1][1] - ln[1]) < 1e-6:
            continue
        merged.append(ln)
    if len(merged) > 1 and merged[0][0] == merged[-1][0] and abs(merged[0][1] - merged[-1][1]) < 1e-6:
        merged.pop()

    # rebuild vertices at the intersection of each consecutive line pair
    out = []
    m = len(merged)
    for i in range(m):
        a, b = merged[i], merged[(i + 1) % m]
        if a[0] == b[0]:
            raise SystemExit("offset failed: consecutive edges share orientation")
        x = a[1] if a[0] == "v" else b[1]
        y = a[1] if a[0] == "h" else b[1]
        out.append((x, y))
    return out


def silhouette(cols, pad):
    return offset_rectilinear(base_outline(cols), pad)


def bounds(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def to_px(pts, ox, oy):
    return [((x - ox) * SCALE, (y - oy) * SCALE) for x, y in pts]


def mask_of(pts, size):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return m


def shift(arr, dx, dy):
    out = np.zeros_like(arr)
    h, w = arr.shape
    xs0, xs1 = max(0, dx), min(w, w + dx)
    ys0, ys1 = max(0, dy), min(h, h + dy)
    out[ys0:ys1, xs0:xs1] = arr[max(0, -dy) : h - max(0, dy), max(0, -dx) : w - max(0, dx)]
    return out


def load_plank_bands(sheet_path=None):
    """Cut the generated sheet into its individual plank strips (RGBA).

    The sheet is planks on pure black. Bands are found by row luminance; within
    a band, each COLUMN's alpha is filled between the first and last lit pixel,
    which keeps the ragged painted silhouette (split ends, chipped edges)
    without turning interior cracks into holes.
    """
    sheet = Image.open(sheet_path or PLANK_SHEET).convert("RGB")
    arr = np.array(sheet, float)
    lum = arr.mean(axis=2)

    lit_rows = lum.mean(axis=1) > 14
    bands, start = [], None
    for y, on in enumerate(list(lit_rows) + [False]):
        if on and start is None:
            start = y
        elif not on and start is not None:
            # 0.06: the v2 sheet packs six chunky assemblies, so each band is
            # only ~1/8 of the sheet — the old 0.12 gate dropped half of them
            if y - start > sheet.height * 0.06:
                bands.append((start, y))
            start = None

    planks = []
    for y0, y1 in bands:
        band = arr[y0:y1]
        blum = lum[y0:y1]
        h, w = blum.shape
        alpha = np.zeros((h, w), np.uint8)
        lit = blum > 16
        for x in range(w):
            ys = np.nonzero(lit[:, x])[0]
            if ys.size:
                alpha[ys[0] : ys[-1] + 1, x] = 255
        rgba = np.dstack([band.astype(np.uint8), alpha])
        img = Image.fromarray(rgba, "RGBA")
        bbox = img.getchannel("A").getbbox()
        planks.append(img.crop(bbox))
    if not planks:
        raise SystemExit("no plank bands found in " + (sheet_path or PLANK_SHEET))
    return planks


def load_scrap_pieces(sheet_path=None):
    """Cut the scrap sheet (loose grid of offcuts on pure black) into RGBA
    pieces by projection splitting: black row gaps separate the grid rows,
    black column gaps within a row separate the pieces. Alpha comes straight
    from luminance (morphologically closed so wood shadows don't punch holes),
    which keeps true concavities like the X-braces' notches transparent."""
    img = Image.open(sheet_path or SCRAP_SHEET).convert("RGB")
    arr = np.array(img, float)
    lum = arr.mean(axis=2)
    lit = lum > 16

    def runs(mask_1d, min_len):
        out, start = [], None
        for i, on in enumerate(list(mask_1d) + [False]):
            if on and start is None:
                start = i
            elif not on and start is not None:
                if i - start >= min_len:
                    out.append((start, i))
                start = None
        return out

    pieces = []
    for y0, y1 in runs(lit.any(axis=1), int(img.height * 0.05)):
        row = lit[y0:y1]
        for x0, x1 in runs(row.any(axis=0), int(img.width * 0.04)):
            crop = arr[y0:y1, x0:x1]
            clum = lum[y0:y1, x0:x1]
            alpha = Image.fromarray(np.where(clum > 12, 255, 0).astype(np.uint8), "L")
            alpha = alpha.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
            rgba = np.dstack([crop.astype(np.uint8), np.array(alpha)])
            piece = Image.fromarray(rgba, "RGBA")
            bbox = piece.getchannel("A").getbbox()
            if bbox:
                piece = piece.crop(bbox)
                if piece.width > 60 and piece.height > 60:
                    pieces.append(piece)
    if not pieces:
        raise SystemExit("no scrap pieces found in " + (sheet_path or SCRAP_SHEET))
    return pieces


def plank_segment(planks, rng, out_w, out_h):
    """A horizontal plank piece out_w x out_h px: random strip, random window
    cropped at the target aspect (so nails/cracks never stretch), random flip."""
    src = planks[rng.randrange(len(planks))]
    if rng.random() < 0.5:
        src = src.transpose(Image.FLIP_LEFT_RIGHT)
    aspect = out_w / out_h
    win_w = min(src.width, max(int(src.height * aspect), 24))
    x = rng.randrange(0, src.width - win_w + 1) if src.width > win_w else 0
    piece = src.crop((x, 0, x + win_w, src.height))
    return piece.resize((out_w, out_h), Image.LANCZOS)


def edges_of(pts):
    """consecutive vertex pairs of a closed rectilinear polygon"""
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        out.append((a, b))
    return out


OUT_TREES = (
    os.path.join(APP, "assets-src", "sprites", "board"),
    os.path.join(APP, "assets-src", "assets", "sprites", "board"),
    os.path.join(APP, "static", "assets", "sprites", "board"),
)


def main(plank_sheet=None, scrap_sheet=None, out_name="board_frame.png"):
    cols = columns()
    outer = silhouette(cols, BORDER)
    x0, y0, x1, y1 = bounds(outer)
    x0 -= MARGIN
    y0 -= MARGIN
    x1 += MARGIN
    y1 += MARGIN
    size = (int(round((x1 - x0) * SCALE)), int(round((y1 - y0) * SCALE)))

    out = Image.new("RGBA", size, (0, 0, 0, 0))
    shadow = Image.new("RGBA", size, (0, 0, 0, 0))

    # planks ride the MID-RING: half in, half out of the nominal frame line
    mid = silhouette(cols, BORDER / 2)
    mid_px = to_px(mid, x0, y0)
    planks = load_plank_bands(plank_sheet)
    rng = random.Random(1887)

    thick = int(PLANK_THICK * SCALE)
    over = PLANK_OVERHANG * SCALE

    def lay(piece, cx, cy):
        """paste a plank centered at (cx, cy) with its contact shadow"""
        px = int(round(cx - piece.width / 2))
        py = int(round(cy - piece.height / 2))
        sh = Image.new("RGBA", piece.size, (0, 0, 0, 0))
        sh.paste((0, 0, 0, 150), (0, 0), piece.getchannel("A"))
        shadow.alpha_composite(
            sh.filter(ImageFilter.GaussianBlur(3 * SCALE)), (px + 2 * SCALE, py + 3 * SCALE)
        )
        out.alpha_composite(piece, (px, py))

    # NOTHING here is straight: every plank gets its own thickness, a small
    # tilt, and a sideways drift off the frame line; long runs are built from
    # TWO overlapping boards instead of one clean beam, so the outline reads as
    # rough carpentry (Tombstone R.I.P.), not a ruler-drawn border.
    for a, b in edges_of(mid_px):
        horizontal = abs(b[0] - a[0]) >= abs(b[1] - a[1])
        length = int(abs(b[0] - a[0]) if horizontal else abs(b[1] - a[1]))
        if length < 4:
            continue
        n_pieces = 2 if length > 2.2 * SYMBOL_SIZE * SCALE else 1
        for k in range(n_pieces):
            seg = length / n_pieces
            seg_len = int(seg * rng.uniform(1.12, 1.3)) if n_pieces > 1 else length
            t = int(thick * rng.uniform(0.82, 1.12))
            piece = plank_segment(planks, rng, int(seg_len + 2 * over), t)
            if not horizontal:
                piece = piece.transpose(Image.ROTATE_90)
            # tilt scaled down on long boards so their far ends never lift off
            # the joint they are meant to cover
            max_tilt = min(2.4, 240.0 * SCALE / max(seg_len, 1))
            piece = piece.rotate(
                rng.uniform(-max_tilt, max_tilt), expand=True, resample=Image.BICUBIC
            )
            f = (k + 0.5) / n_pieces + rng.uniform(-0.04, 0.04)
            cx = a[0] + (b[0] - a[0]) * f
            cy = a[1] + (b[1] - a[1]) * f
            drift = rng.uniform(-3, 3) * SCALE
            if horizontal:
                cy += drift
            else:
                cx += drift
            lay(piece, cx, cy)

    # GENERATED offcut pieces nailed over the joints: crossed boards, chain
    # wraps, splinter shards, strap plates — real painted art, not drawn
    # ellipses (the boards carry their own baked nails and bolt plates now).
    # Every corner gets one, cycling through the sheet so neighbours differ.
    scraps = load_scrap_pieces(scrap_sheet)
    corner_pts, min_gap = [], 40 * SCALE
    for p in mid_px:
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > min_gap**2 for q in corner_pts):
            corner_pts.append(p)
    order = list(range(len(scraps)))
    rng.shuffle(order)
    for idx, p in enumerate(corner_pts):
        if rng.random() < 0.18:
            continue
        scrap = scraps[order[idx % len(order)]]
        if rng.random() < 0.5:
            scrap = scrap.transpose(Image.FLIP_LEFT_RIGHT)
        target_w = rng.uniform(64, 104) * SCALE
        f = target_w / scrap.width
        scrap = scrap.resize(
            (int(scrap.width * f), int(scrap.height * f)), Image.LANCZOS
        )
        scrap = scrap.rotate(
            rng.uniform(-24, 24), expand=True, resample=Image.BICUBIC
        )
        lay(
            scrap,
            p[0] + rng.uniform(-6, 6) * SCALE,
            p[1] + rng.uniform(-6, 6) * SCALE,
        )

    out = Image.alpha_composite(shadow, out)

    # guarantee the play area: whatever the pieces did, nothing keeps more
    # than a small plank lip inside the cell outline (same rule as the wire
    # tool), so no scrap ever sits over a spinning symbol
    arr = np.array(out)
    inner = Image.new("L", size, 0)
    ImageDraw.Draw(inner).polygon(to_px(silhouette(cols, -6), x0, y0), fill=255)
    arr[..., 3] = np.where(np.array(inner) > 0, 0, arr[..., 3])
    out = Image.fromarray(arr, "RGBA")

    for dst in OUT_TREES:
        os.makedirs(dst, exist_ok=True)
        path = os.path.join(dst, out_name)
        out.save(path, optimize=True)
        print("wrote", path, out.size)

    # the component anchors the sprite at this authored box (board-local units)
    print("anchor box:", {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0})
    print("SYMBOL_SIZE", SYMBOL_SIZE, "PITCH", PITCH, "| BORDER+MARGIN =", BORDER + MARGIN)


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--planks", default=PLANK_SHEET)
    p.add_argument("--scraps", default=SCRAP_SHEET)
    p.add_argument("--out", default="board_frame.png")
    args = p.parse_args()
    main(args.planks, args.scraps, args.out)
