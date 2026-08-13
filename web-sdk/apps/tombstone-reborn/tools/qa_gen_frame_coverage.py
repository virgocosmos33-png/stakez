"""Check the GENERATED frame paint against the stencil BEFORE wiring.

Samples the mid-ring path (silhouette at BORDER/2) densely and reports, per
edge, what fraction of samples carry paint (luminance < 235 after resizing the
generation to the guide canvas). Any long white run on the ring would become a
hole in the baked frame, so this must be ~100% on every edge.
"""

import os

import numpy as np
from PIL import Image

from _gen_frame_guide import GEN, guide_geometry
from make_board_frame_image import BORDER, silhouette, to_px

cols, x0, y0, size, pad_x, canvas = guide_geometry()
src = Image.open(os.path.join(GEN, "tr_frame_generated.png")).convert("RGB")
src = src.resize(canvas, Image.LANCZOS).crop((pad_x, 0, pad_x + size[0], size[1]))
lum = np.array(src, float).mean(axis=2)

mid = to_px(silhouette(cols, BORDER / 2), x0, y0)
worst = 1.0
for i in range(len(mid)):
    a, b = mid[i], mid[(i + 1) % len(mid)]
    n = max(int(np.hypot(b[0] - a[0], b[1] - a[1]) / 4), 2)
    ts = np.linspace(0, 1, n)
    xs = np.clip((a[0] + (b[0] - a[0]) * ts).astype(int), 0, size[0] - 1)
    ys = np.clip((a[1] + (b[1] - a[1]) * ts).astype(int), 0, size[1] - 1)
    cov = float((lum[ys, xs] < 235).mean())
    worst = min(worst, cov)
    flag = "" if cov > 0.97 else "  <-- GAP"
    print(f"edge {i:2d} ({int(a[0])},{int(a[1])})->({int(b[0])},{int(b[1])}) cov={cov:.3f}{flag}")
print("worst edge coverage:", round(worst, 3))
