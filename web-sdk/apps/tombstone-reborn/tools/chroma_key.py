#!/usr/bin/env python3
"""Chroma-key a solid magenta (#FF00FF) background out of a generated image and
write a true-alpha PNG (no baked-in transparency checkerboard).

Also removes the magenta "spill" halo that AI image gen leaves around the
subject edges, so keyed sprites read cleanly on any background.

Usage:
    python chroma_key.py <input> <output> [--size N] [--thresh LO HI]

The key color is pure magenta because none of THE WHITE ROOM's cold
steel/bone-white art contains magenta, so it keys without eating the subject.
"""
import argparse
import numpy as np
from PIL import Image


def chroma_key(inp: str, outp: str, size: int | None, lo: float, hi: float) -> None:
    img = Image.open(inp).convert("RGBA")
    rgb = np.asarray(img.convert("RGB"), dtype=np.float32)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    # "magenta-ness": magenta = high R, high B, low G  ->  (R+B)/2 - G.
    mag = (r + b) * 0.5 - g

    # alpha ramp: fully opaque where mag<=lo (subject), fully cut where mag>=hi.
    alpha = np.clip((hi - mag) / max(hi - lo, 1e-3), 0.0, 1.0)

    # De-spill: pull the magenta halo (R,B pushed above G) back down toward the
    # grey/white subject tones. White/grey art (R~=G~=B) is left untouched.
    cap = g + 12.0
    r = np.minimum(r, cap)
    b = np.minimum(b, cap)

    out = np.zeros(rgb.shape[:2] + (4,), dtype=np.uint8)
    out[..., 0] = np.clip(r, 0, 255).astype(np.uint8)
    out[..., 1] = np.clip(g, 0, 255).astype(np.uint8)
    out[..., 2] = np.clip(b, 0, 255).astype(np.uint8)
    out[..., 3] = (alpha * 255.0).astype(np.uint8)

    result = Image.fromarray(out, "RGBA")
    if size:
        result = result.resize((size, size), Image.LANCZOS)
    result.save(outp)
    print(f"keyed {inp} -> {outp}  ({result.size[0]}x{result.size[1]})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--size", type=int, default=None)
    ap.add_argument("--thresh", type=float, nargs=2, default=(30.0, 90.0),
                    metavar=("LO", "HI"))
    args = ap.parse_args()
    chroma_key(args.input, args.output, args.size, args.thresh[0], args.thresh[1])
