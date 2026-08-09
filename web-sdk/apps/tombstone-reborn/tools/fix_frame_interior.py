"""Make the ornate mirror_frame.png opening TRANSPARENT.

The shipped asset has an opaque near-white fill inside the gold border
(center pixel = RGBA(254,254,254,255)). A mirror frame must have a
see-through opening, so this floods the connected light interior from the
centre and clears its alpha, leaving the gold border (and its warm
highlights) untouched. The original is backed up once to
mirror_frame_orig.png.

Run: python tools/fix_frame_interior.py
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image

ASSET_DIR = Path(__file__).resolve().parents[1] / "static" / "assets" / "sprites" / "mirror"
SRC = ASSET_DIR / "mirror_frame.png"
BACKUP = ASSET_DIR / "mirror_frame_orig.png"

# interior fill is grey/near-white & opaque; gold border is warm & darker
BRIGHT = 165  # brightness above this == interior candidate
SAT_MAX = 26  # low saturation (grey) — spares warm gold highlights


def main() -> None:
    im = Image.open(SRC).convert("RGBA")
    if not BACKUP.exists():
        im.save(BACKUP)
        print(f"[backup] {BACKUP.name}")

    W, H = im.size
    px = im.load()

    def is_interior(x: int, y: int) -> bool:
        r, g, b, a = px[x, y]
        if a == 0:
            return False
        if (r + g + b) / 3 < BRIGHT:
            return False
        return (max(r, g, b) - min(r, g, b)) <= SAT_MAX

    # flood fill from the centre across the connected light interior
    seeds = [(W // 2, H // 2), (W // 2, int(H * 0.25)), (W // 2, int(H * 0.75))]
    seen = bytearray(W * H)
    q = deque()
    for sx, sy in seeds:
        if is_interior(sx, sy) and not seen[sy * W + sx]:
            seen[sy * W + sx] = 1
            q.append((sx, sy))

    cleared = 0
    minx, miny, maxx, maxy = W, H, 0, 0
    while q:
        x, y = q.popleft()
        r, g, b, a = px[x, y]
        px[x, y] = (r, g, b, 0)
        cleared += 1
        minx, miny = min(minx, x), min(miny, y)
        maxx, maxy = max(maxx, x), max(maxy, y)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < W and 0 <= ny < H and not seen[ny * W + nx]:
                seen[ny * W + nx] = 1
                if is_interior(nx, ny):
                    q.append((nx, ny))

    im.save(SRC)
    print(f"[fix] cleared {cleared} px ({cleared / (W * H) * 100:.1f}%)")
    print(f"[opening bbox] x[{minx}..{maxx}] ({(maxx - minx) / W:.3f} of W)  "
          f"y[{miny}..{maxy}] ({(maxy - miny) / H:.3f} of H)")
    print(f"[opening frac] L={minx / W:.3f} R={maxx / W:.3f} "
          f"T={miny / H:.3f} B={maxy / H:.3f}")


if __name__ == "__main__":
    main()
