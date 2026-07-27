"""Key + install THE WHITE ROOM padded/steel main reel frame.

Reads mirror_frame_wide_gen.png (or *_gen_a/b.png) from COUNTER_FRAME_SRC /
Cursor assets folder, keys exterior near-black to alpha, punches the center
well transparent (nine-slice compatible), scales so the opening matches
mirror_frame_wide_GOTHIC_BAK.png (1803x1386), and writes:

  static/assets/sprites/mirror/mirror_frame_wide.png
  assets/sprites/mirror/mirror_frame_wide.png
  static/assets/sprites/mirror/mirror_frame.png  (legacy alias)

Opening size/position is bak-locked so BoardFrame nine-slice insets stay valid.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
GEN_DIR = Path(
    os.environ.get(
        "COUNTER_FRAME_SRC",
        Path.home()
        / ".cursor"
        / "projects"
        / "c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios"
        / "assets",
    )
)
STATIC_DIR = HERE.parent / "static" / "assets" / "sprites" / "mirror"
APP_ASSETS_DIR = HERE.parent / "assets" / "sprites" / "mirror"
OUT_NAME = "mirror_frame_wide.png"
SRC_CANDIDATES = (
    "mirror_frame_wide_gen.png",
    "mirror_frame_wide_gen_a.png",
    "mirror_frame_wide_gen_b.png",
)
BG_THRESH = 40
BAK_NAME = "mirror_frame_wide_GOTHIC_BAK.png"
DARK = 55


def key_exterior_black(rgb: Image.Image) -> np.ndarray:
    w, h = rgb.size
    work = rgb.copy()
    sentinel = (255, 0, 255)
    seeds = [
        (0, 0),
        (w - 1, 0),
        (0, h - 1),
        (w - 1, h - 1),
        (w // 2, 0),
        (w // 2, h - 1),
        (0, h // 2),
        (w - 1, h // 2),
    ]
    for seed in seeds:
        ImageDraw.floodfill(work, seed, sentinel, thresh=BG_THRESH)
    arr = np.asarray(work)
    is_bg = np.all(arr == np.array(sentinel), axis=-1)
    return np.where(is_bg, 0, 255).astype(np.uint8)


def max_run(row: np.ndarray) -> tuple[int, int]:
    if not row.any():
        return 0, 0
    padded = np.concatenate(([0], row.astype(np.int8), [0]))
    d = np.diff(padded)
    starts = np.where(d == 1)[0]
    ends = np.where(d == -1)[0]
    lengths = ends - starts
    k = int(lengths.argmax())
    return int(lengths[k]), int(starts[k])


def find_opening_transparent(im: Image.Image) -> tuple[int, int, int, int]:
    a = np.asarray(im.convert("RGBA"))
    alpha = a[..., 3]
    w, h = im.size
    ow, ox = max_run((alpha < 20)[h // 2])
    oh, oy = max_run((alpha < 20)[:, w // 2])
    return ox, oy, ow, oh


def punch_dark_center(img: Image.Image) -> tuple[Image.Image, int, int, int, int]:
    a = np.asarray(img).copy()
    r, g, b, alpha = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    w, h = img.size
    darkm = (alpha > 180) & (r < DARK) & (g < DARK) & (b < DARK)
    interior: list[tuple[int, int, int]] = []
    for y in range(h):
        ln, s = max_run(darkm[y])
        if ln > 0.40 * w:
            interior.append((y, s, ln))
    if not interior:
        raise SystemExit("could not find dark center well to punch")
    top = interior[0][0]
    bot = interior[-1][0]
    left = int(np.median([s for _, s, _ in interior]))
    right = int(np.median([s + ln for _, s, ln in interior]))
    pad = 2
    a[top + pad : bot - pad, left + pad : right - pad, 3] = 0
    ox, oy = left + pad, top + pad
    ow, oh = right - left - 2 * pad, bot - top - 2 * pad
    return Image.fromarray(a, "RGBA"), ox, oy, ow, oh


def resolve_src() -> Path:
    env = (os.environ.get("WIDE_FRAME_SRC") or "").strip()
    if env:
        p = Path(env)
        if p.is_file():
            return p
        raise SystemExit(f"WIDE_FRAME_SRC missing: {p}")
    for name in SRC_CANDIDATES:
        p = GEN_DIR / name
        if p.is_file():
            return p
    raise SystemExit(f"missing gen master in {GEN_DIR} ({SRC_CANDIDATES})")


def main() -> None:
    src = resolve_src()
    print(f"src={src}", flush=True)

    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    APP_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    GEN_DIR.mkdir(parents=True, exist_ok=True)

    bak = STATIC_DIR / BAK_NAME
    dest = STATIC_DIR / OUT_NAME
    if dest.is_file() and not bak.is_file():
        shutil.copy2(dest, bak)
        print(f"backed up gothic original -> {bak.name}", flush=True)
    if not bak.is_file():
        raise SystemExit(f"missing bak geometry lock: {bak}")

    bak_im = Image.open(bak).convert("RGBA")
    tw, th = bak_im.size
    bak_ox, bak_oy, bak_ow, bak_oh = find_opening_transparent(bak_im)
    print(
        f"bak {tw}x{th} opening=({bak_ow}x{bak_oh}) at ({bak_ox},{bak_oy})",
        flush=True,
    )

    rgba_in = Image.open(src).convert("RGBA")
    if int(np.asarray(rgba_in)[..., 3].min()) < 10:
        img = rgba_in
        print("source already has transparency; skipping exterior key", flush=True)
    else:
        rgb = rgba_in.convert("RGB")
        alpha = key_exterior_black(rgb)
        img = Image.fromarray(np.dstack([np.asarray(rgb), alpha]), "RGBA")

    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    img, ox, oy, ow, oh = punch_dark_center(img)
    print(f"punched opening ({ow}x{oh}) at ({ox},{oy}) in {img.size}", flush=True)

    # Non-uniform scale so opening locks to bak opening; paste aligned.
    sx = bak_ow / max(ow, 1)
    sy = bak_oh / max(oh, 1)
    nw = max(1, int(round(img.width * sx)))
    nh = max(1, int(round(img.height * sy)))
    scaled = img.resize((nw, nh), Image.Resampling.LANCZOS)
    sox = int(round(ox * sx))
    soy = int(round(oy * sy))
    canvas = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    canvas.alpha_composite(scaled, (bak_ox - sox, bak_oy - soy))

    ca = np.asarray(canvas).copy()
    ca[bak_oy : bak_oy + bak_oh, bak_ox : bak_ox + bak_ow, 3] = 0
    canvas = Image.fromarray(ca, "RGBA")

    raw_path = GEN_DIR / "mirror_frame_wide_raw.png"
    canvas.save(raw_path)

    fox, foy, fow, foh = find_opening_transparent(canvas)
    print(
        f"final {canvas.size} opening=({fow}x{foh}) at ({fox},{foy}) "
        f"frac=({fow / tw:.4f},{foh / th:.4f})",
        flush=True,
    )
    if (fox, foy, fow, foh) != (bak_ox, bak_oy, bak_ow, bak_oh):
        print(
            f"WARN: opening drift vs bak ({bak_ox},{bak_oy},{bak_ow},{bak_oh})",
            flush=True,
        )

    # Scenario gens often bake a bright dashed cut-path on the opening rim.
    # Seal it with dark bevel paint before install (opening bbox unchanged).
    from strip_frame_cutline import strip_cutline

    canvas = strip_cutline(canvas)
    fox2, foy2, fow2, foh2 = find_opening_transparent(canvas)
    if (fox2, foy2, fow2, foh2) != (fox, foy, fow, foh):
        raise SystemExit(
            f"cutline strip moved opening {(fox, foy, fow, foh)} -> "
            f"{(fox2, foy2, fow2, foh2)}"
        )
    print("cutline seal applied (opening unchanged)", flush=True)

    tmp = dest.with_name(OUT_NAME + ".tmp.png")
    canvas.save(tmp, format="PNG")
    try:
        tmp.replace(dest)
    except OSError as e:
        alt = dest.with_name("mirror_frame_wide_wr.png")
        canvas.save(alt)
        print(f"[warn] locked {dest.name} ({e}); wrote {alt.name}", flush=True)
    else:
        print(f"wrote {dest} ({dest.stat().st_size} bytes)", flush=True)

    dest_assets = APP_ASSETS_DIR / OUT_NAME
    canvas.save(dest_assets)
    print(f"wrote {dest_assets} ({dest_assets.stat().st_size} bytes)", flush=True)

    legacy = STATIC_DIR / "mirror_frame.png"
    canvas.save(legacy)
    print(f"wrote {legacy}", flush=True)
    print("OK: padded/steel reel frame installed (gothic bak-locked)", flush=True)


if __name__ == "__main__":
    main()
