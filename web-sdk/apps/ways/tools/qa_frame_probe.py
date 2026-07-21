from __future__ import annotations
from pathlib import Path
from PIL import Image

ASSET = (
    Path(__file__).resolve().parents[1]
    / "static" / "assets" / "sprites" / "mirror" / "mirror_frame.png"
)

im = Image.open(ASSET)
print("mode:", im.mode, "size:", im.size, "info:", im.info.get("transparency"))
rgba = im.convert("RGBA")
W, H = rgba.size
pts = {
    "center": (W // 2, H // 2),
    "top-mid": (W // 2, int(H * 0.10)),
    "left-mid": (int(W * 0.10), H // 2),
    "corner-tl": (2, 2),
    "quarter": (W // 4, H // 4),
    "inner-upper": (W // 2, int(H * 0.25)),
}
for name, (x, y) in pts.items():
    print(f"{name:12s} ({x:3d},{y:3d}) RGBA={rgba.getpixel((x, y))}")

# histogram of alpha
alpha = rgba.getchannel("A")
hist = alpha.histogram()
transparent = sum(hist[0:16])
opaque = sum(hist[240:256])
mid = W * H - transparent - opaque
print(f"alpha: transparent(<16)={transparent}  mid={mid}  opaque(>=240)={opaque}  total={W*H}")
