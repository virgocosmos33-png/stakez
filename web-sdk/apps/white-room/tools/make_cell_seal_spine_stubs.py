"""Build single-frame Spine 4.1 stubs from Cell Seal stills (offline, no CU).

Produces looping ``idle`` that holds the full-reel still until GodMode replaces
the atlas with a multi-frame sheet. Safe for Vite asset imports.

  python tools/make_cell_seal_spine_stubs.py
"""

from __future__ import annotations

import io
import json
from pathlib import Path

from PIL import Image

import godmode_lady_spine as gm

APP = Path(__file__).resolve().parents[1]
RAW = APP / "assets-raw" / "cellSeal"
STATIC = APP / "static" / "assets" / "sprites" / "cellSeal"
OUT = APP / "static" / "assets" / "spines" / "cellSeal"
ASSETS_SPINE = APP / "assets" / "spines" / "cellSeal"
SYMBOLS = ["H1", "H2", "H3", "H4", "H5"]
TARGET_H = 1400


def main() -> None:
    built: dict[str, tuple] = {}
    for sym in SYMBOLS:
        src = None
        for p in (RAW / f"{sym}_full.png", STATIC / f"{sym}_full.webp", RAW / f"{sym}_full.webp"):
            if p.exists() and p.stat().st_size > 20_000:
                src = p
                break
        if src is None:
            print(f"[skip] {sym}: no still", flush=True)
            continue
        im = Image.open(src).convert("RGBA")
        packed, dw, dh = gm.normalize_frames([im], TARGET_H)
        prefix = f"{sym.lower()}_idle"
        built[prefix] = (packed, dw, dh, f"{sym}.json")

    if not built:
        raise SystemExit("no stills for stubs")

    # Shared atlas write (same as godmode_cell_seal_spines.write_shared_atlas)
    all_regions: list[dict] = []
    for prefix, (frames, _dw, _dh, _jn) in built.items():
        for i, fr in enumerate(frames):
            all_regions.append({"name": f"{prefix}/{i:02d}", "img": fr})
    pad = 2
    x = pad
    y = pad
    row_h = 0
    W = 0
    max_w = 4096
    for r in all_regions:
        w, h = r["img"].size
        if x + w + pad > max_w:
            x = pad
            y += row_h + pad
            row_h = 0
        r["ax"], r["ay"] = x, y
        x += w + pad
        row_h = max(row_h, h)
        W = max(W, x)
    H = y + row_h + pad
    page = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for r in all_regions:
        page.alpha_composite(r["img"], (r["ax"], r["ay"]))

    OUT.mkdir(parents=True, exist_ok=True)
    ASSETS_SPINE.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    page.save(buf, "WEBP", lossless=True, quality=100)
    data = buf.getvalue()
    (OUT / "cellSeal.webp").write_bytes(data)
    (ASSETS_SPINE / "cellSeal.webp").write_bytes(data)

    lines = ["cellSeal.webp", f"size:{W},{H}", "filter:Linear,Linear", "scale:1"]
    for r in all_regions:
        w, h = r["img"].size
        lines.append(r["name"])
        lines.append(f"bounds:{r['ax']},{r['ay']},{w},{h}")
    atlas = ("\n".join(lines) + "\n").encode("utf-8")
    (OUT / "cellSeal.atlas").write_bytes(atlas)
    (ASSETS_SPINE / "cellSeal.atlas").write_bytes(atlas)

    for prefix, (frames, dw, dh, json_name) in built.items():
        skel = gm.build_sequence_skel(prefix, len(frames), dw, dh, fps=12.0)
        raw = json.dumps(skel).encode("utf-8")
        (OUT / json_name).write_bytes(raw)
        (ASSETS_SPINE / json_name).write_bytes(raw)
        print(f"[stub] {json_name} display={dw}x{dh} frames={len(frames)}", flush=True)

    print(json.dumps({"ok": True, "symbols": list(built.keys()), "out": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
