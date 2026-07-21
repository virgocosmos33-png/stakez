"""Generate mirror_backing.png: a solid dark plate shaped EXACTLY like the
ornate frame's transparent opening (dilated a little so it tucks under the
gold border). Rendered at the same rect as mirror_frame.png, it fills the
reel recess with deep shadow and can never poke past the frame silhouette.

Run: python tools/generate_backing.py
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

ASSET_DIR = Path(__file__).resolve().parents[1] / "static" / "assets" / "sprites" / "mirror"
FRAME = ASSET_DIR / "mirror_frame.png"          # interior already made transparent
OUT = ASSET_DIR / "mirror_backing.png"

DARK = (13, 12, 16)   # deep near-black recess (faint cool tint)
DILATE_PASSES = 5     # MaxFilter(9) ~4px each -> ~20px under the gold border
FEATHER = 2.5         # soft edge so the plate melts under the frame


def main() -> None:
    im = Image.open(FRAME).convert("RGBA")
    W, H = im.size
    px = im.load()

    # flood the transparent INTERIOR from the centre (the outer corners are
    # also transparent but are walled off by the opaque gold ring)
    inside = bytearray(W * H)
    seen = bytearray(W * H)
    q = deque([(W // 2, H // 2)])
    seen[(H // 2) * W + (W // 2)] = 1
    while q:
        x, y = q.popleft()
        if px[x, y][3] >= 128:  # hit the gold ring -> stop
            continue
        inside[y * W + x] = 1
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < W and 0 <= ny < H and not seen[ny * W + nx]:
                seen[ny * W + nx] = 1
                q.append((nx, ny))

    mask = Image.frombytes("L", (W, H), bytes(255 if b else 0 for b in inside))
    for _ in range(DILATE_PASSES):
        mask = mask.filter(ImageFilter.MaxFilter(9))
    mask = mask.filter(ImageFilter.GaussianBlur(FEATHER))

    out = Image.new("RGBA", (W, H), (*DARK, 0))
    out.putalpha(mask)
    # paint the dark colour under the mask
    solid = Image.new("RGBA", (W, H), (*DARK, 255))
    out = Image.composite(solid, Image.new("RGBA", (W, H), (*DARK, 0)), mask)
    out.save(OUT)

    bbox = mask.getbbox()
    print(f"[backing] {OUT.name}  size={out.size}  bbox={bbox}")


if __name__ == "__main__":
    main()
