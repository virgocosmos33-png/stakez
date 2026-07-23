"""Chroma-key the flat-green background out of the generated logo to alpha.

Approach (green-screen keying with spill suppression):
  1. alpha from "greenness": how much green dominates red & blue.
  2. suppress green spill on kept pixels (clamp G toward max(R,B)).
  3. autocrop to the logo bounds with a small transparent margin.
"""

import sys

import numpy as np
from PIL import Image

SRC = sys.argv[1]
DST = sys.argv[2]

img = Image.open(SRC).convert("RGBA")
arr = np.asarray(img).astype(np.float32)
r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]

# "greenness": green clearly above both red and blue = background.
green_excess = g - np.maximum(r, b)

# Full transparency well inside the green, full opacity on the artwork,
# smooth ramp between so edges don't jag.
LO, HI = 40.0, 110.0
alpha = 1.0 - np.clip((green_excess - LO) / (HI - LO), 0.0, 1.0)

# Spill suppression: on partially/near-kept pixels, pull the green channel
# down to at most the max of red/blue so no green rim survives.
keep = alpha > 0.0
cap = np.maximum(r, b)
spill = keep & (g > cap)
g[spill] = cap[spill]

out = np.dstack([r, g, b, alpha * 255.0]).astype(np.uint8)
result = Image.fromarray(out, "RGBA")

# Autocrop to non-transparent bounds + small margin.
bbox = result.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
if bbox:
    margin = 12
    left = max(bbox[0] - margin, 0)
    top = max(bbox[1] - margin, 0)
    right = min(bbox[2] + margin, result.width)
    bottom = min(bbox[3] + margin, result.height)
    result = result.crop((left, top, right, bottom))

result.save(DST)
print(f"saved {DST} size={result.size}")
