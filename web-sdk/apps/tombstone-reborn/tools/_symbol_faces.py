"""Shared face isolation for paying-card plates.

The desktop kit idles are painted on an opaque studio-black field. The wood /
blood plates can only read if that field is knocked out. Flood from the border
through near-black low-chroma pixels so dark coats and hats stay.
"""

from __future__ import annotations

import numpy as np
from PIL import Image

CELL = 300
CARD_H = 292
CARD_W = round(CARD_H * 0.775)


def alpha_crop(im: Image.Image) -> Image.Image:
    bbox = im.getchannel("A").getbbox()
    return im.crop(bbox) if bbox else im


def knockout_studio_black(im: Image.Image, lum_max: float = 14.0, chroma_max: float = 8.0, band: int = 16) -> Image.Image:
    """Open only the studio field that touches the border. Never punch
    interiors (letter counters, coat folds) and never blur the cut."""
    rgba = np.asarray(im.convert("RGBA"))
    rgb = rgba[..., :3].astype(np.float32)
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    walk = (lum <= lum_max) & (chroma <= chroma_max)
    h, w = lum.shape
    seen = np.zeros((h, w), dtype=bool)
    edge = min(band, h // 6, w // 6)
    seen[:edge] |= walk[:edge]
    seen[-edge:] |= walk[-edge:]
    seen[:, :edge] |= walk[:, :edge]
    seen[:, -edge:] |= walk[:, -edge:]
    for _ in range(max(h, w)):
        dil = seen.copy()
        dil[1:] |= seen[:-1]
        dil[:-1] |= seen[1:]
        dil[:, 1:] |= seen[:, :-1]
        dil[:, :-1] |= seen[:, 1:]
        new = dil & walk
        if np.array_equal(new, seen):
            break
        seen = new
    out = rgba.copy()
    out[..., 3][seen] = 0
    return Image.fromarray(out, "RGBA")


def fit_in_cell(src: Image.Image, box_w: int, box_h: int, cell: int = CELL) -> Image.Image:
    src = alpha_crop(src.convert("RGBA"))
    scale = min(box_w / src.width, box_h / src.height)
    nw = max(1, round(src.width * scale))
    nh = max(1, round(src.height * scale))
    fitted = src.resize((nw, nh), Image.LANCZOS)
    cell_im = Image.new("RGBA", (cell, cell), (0, 0, 0, 0))
    cell_im.paste(fitted, ((cell - nw) // 2, (cell - nh) // 2), fitted)
    return cell_im


def face_cell(src: Image.Image) -> Image.Image:
    return fit_in_cell(knockout_studio_black(src), CARD_W - 12, CARD_H - 12)


def card_cell(src: Image.Image) -> Image.Image:
    """Rank letters as authored. Do not punch the black field — that
    ate the A counter and left gold specks."""
    return fit_in_cell(src.convert("RGBA"), CARD_W, CARD_H - 24)


def scatter_cell(src: Image.Image) -> Image.Image:
    """Scatter moon/tombstone is authored flush to the top of the square.
    Shrink and sit it a little low so the timber beam does not shear the arc."""
    src = alpha_crop(src.convert("RGBA"))
    box_w = max(1, CARD_W - 16)
    box_h = max(1, CARD_H - 40)
    scale = min(box_w / src.width, box_h / src.height)
    nw = max(1, round(src.width * scale))
    nh = max(1, round(src.height * scale))
    fitted = src.resize((nw, nh), Image.LANCZOS)
    cell_im = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    x = (CELL - nw) // 2
    y = (CELL - nh) // 2 + 14
    if y + nh > CELL:
        y = CELL - nh
    cell_im.paste(fitted, (x, max(0, y)), fitted)
    return cell_im


# Preacher-ref pocket: brim to the sides, hat a sliver under the rail,
# chest / guns / cross still in. Cover the whole island. Never 0.50
# (face-only). Never contain-fit of the 1024 square (too small).
HIGH_ROOF = 20


def high_cell(src: Image.Image) -> Image.Image:
    """Desktop high-pay PNG as authored. Cover-fill the cell. No punch."""
    src = src.convert("RGBA")
    box_w, box_h = CARD_W, CARD_H - HIGH_ROOF
    scale = max(box_w / max(1, src.width), box_h / max(1, src.height))
    nw = max(1, round(src.width * scale))
    nh = max(1, round(src.height * scale))
    fitted = src.resize((nw, nh), Image.LANCZOS)
    src_x = max(0, (nw - box_w) // 2)
    src_y = 0
    crop = fitted.crop((src_x, src_y, src_x + box_w, src_y + box_h))
    if crop.size != (box_w, box_h):
        padded = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
        padded.paste(crop, (0, 0), crop)
        crop = padded
    cell_im = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    cell_im.paste(crop, ((CELL - box_w) // 2, (CELL - box_h) // 2), crop)
    return cell_im
