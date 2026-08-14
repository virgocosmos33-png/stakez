"""Re-skin the mm_symbols SPINE atlas with the live TOMBSTONE REBORN faces.

The mm_symbols spine skeletons (win / land / postwin per symbol) were authored
over the OLD White Room card art, so the shared atlas image (mm_symbols.webp)
still carried clinical-horror faces (syringe, stethoscope, "404" clipboard,
straitjacket ...). Routing win/land/postWin through those spines flashed the
wrong game. This tool repaints ONLY the atlas IMAGE: every 300x300 card slot is
stamped with the matching Tombstone face cropped from the live static atlas
(symbolsStatic.v13), while the skeleton .json meshes / animations / UVs are left
completely untouched (the slot geometry is identical, so the rig just deforms
the correct art now). The generic fx_* glow slots are warmed to an ember/amber
palette so the win burst reads western instead of clinical.

Run:  python tools/reskin_symbol_spines.py
"""

import io
import json
import os
import sys
import time

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))

# live Tombstone static atlas = source of truth for the faces
STATIC_DIR = os.path.join(APP, "static", "assets", "sprites", "symbolsStatic")
STATIC_PNG = os.path.join(STATIC_DIR, "symbolsStatic.v13.png")
STATIC_JSON = os.path.join(STATIC_DIR, "symbolsStatic.v13.json")

# every physical copy of the spine atlas (runtime + both source trees)
ATLAS_DIRS = [
    os.path.join(APP, "static", "assets", "spines", "mm_symbols"),
    os.path.join(APP, "assets-src", "assets", "spines", "mm_symbols"),
    os.path.join(APP, "assets-src", "spines", "mm_symbols"),
]

# spine atlas region name -> static atlas frame name
FACE_MAP = {
    "h1": "h1.webp",
    "h2": "h2.webp",
    "h3": "h3.webp",
    "h4": "h4.webp",
    "h5": "h5.webp",
    "l1": "l1.webp",
    "l2": "l2.webp",
    "l3": "l3.webp",
    "l4": "l4.webp",
    "l5": "l5.webp",
    "w": "w.png",
    "s": "s.png",
    "hm": "hm_intact.png",
    "hm_cracked": "hm_cracked.png",
}

# warm ember/amber the generic glow slots are tinted toward (luminance-mapped)
EMBER = np.array([255.0, 168.0, 84.0])
EMBER_BOOST = 1.12


def robust_write_bytes(path, data, attempts=8):
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
            time.sleep(0.5 * (i + 1))
    raise SystemExit(f"could not write {path} (locked)")


def save_image(img, path):
    buf = io.BytesIO()
    if path.lower().endswith(".webp"):
        img.save(buf, format="WEBP", quality=92, method=6)
    else:
        img.save(buf, format="PNG")
    robust_write_bytes(path, buf.getvalue())


def parse_atlas(atlas_path):
    """Return { region_name: (x, y, w, h) } from a libgdx-style .atlas."""
    regions = {}
    name = None
    with open(atlas_path, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]
    for ln in lines:
        if not ln.strip():
            continue
        if ln.startswith(("size:", "filter:", "scale:", "format:", "repeat:", "pma:")):
            continue
        if ln.lower().endswith((".webp", ".png")):
            continue  # page image line
        if ln.startswith("bounds:") or ln.startswith("  bounds:") or "bounds:" in ln:
            vals = ln.split("bounds:")[1].strip()
            x, y, w, h = (int(v) for v in vals.split(","))
            if name is not None:
                regions[name] = (x, y, w, h)
            continue
        if not ln.startswith(" ") and ":" not in ln:
            name = ln.strip()
    return regions


def build_faces():
    """Crop every needed Tombstone face into a { spine_region: RGBA Image }."""
    meta = json.load(open(STATIC_JSON, "r", encoding="utf-8"))
    frames = meta["frames"]
    sheet = Image.open(STATIC_PNG).convert("RGBA")
    faces = {}
    for region, frame_name in FACE_MAP.items():
        fr = frames[frame_name]["frame"]
        crop = sheet.crop((fr["x"], fr["y"], fr["x"] + fr["w"], fr["y"] + fr["h"]))
        faces[region] = crop
    return faces


def warm_region(img):
    """Luminance-map an fx glow slot onto the ember palette, keeping alpha."""
    arr = np.array(img).astype(np.float32)
    rgb = arr[:, :, :3]
    a = arr[:, :, 3:4]
    lum = (0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]) / 255.0
    lum = np.clip(lum * EMBER_BOOST, 0.0, 1.0)[:, :, None]
    out_rgb = np.clip(lum * EMBER[None, None, :], 0, 255)
    out = np.concatenate([out_rgb, a], axis=2).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def reskin_dir(atlas_dir, faces):
    atlas_path = os.path.join(atlas_dir, "mm_symbols.atlas")
    if not os.path.exists(atlas_path):
        print(f"  skip (no atlas): {atlas_dir}")
        return
    regions = parse_atlas(atlas_path)

    # start from the existing PNG so the fx_* art is preserved (then warmed)
    base_png = os.path.join(atlas_dir, "mm_symbols.png")
    base = Image.open(base_png).convert("RGBA")
    canvas = base.copy()

    stamped = []
    for region, (x, y, w, h) in regions.items():
        if region in faces:
            face = faces[region]
            if face.size != (w, h):
                face = face.resize((w, h), Image.LANCZOS)
            canvas.paste(face, (x, y))  # replace alpha wholesale
            stamped.append(region)
        elif region.startswith("fx"):
            slot = canvas.crop((x, y, x + w, y + h))
            canvas.paste(warm_region(slot), (x, y))

    save_image(canvas, os.path.join(atlas_dir, "mm_symbols.png"))
    save_image(canvas, os.path.join(atlas_dir, "mm_symbols.webp"))
    print(f"  reskinned {len(stamped)} faces -> {atlas_dir}")


def main():
    if not os.path.exists(STATIC_PNG):
        raise SystemExit(f"missing static atlas: {STATIC_PNG}")
    faces = build_faces()
    print(f"cropped {len(faces)} Tombstone faces from symbolsStatic.v13")
    for d in ATLAS_DIRS:
        reskin_dir(d, faces)
    print("done.")


if __name__ == "__main__":
    sys.exit(main())
