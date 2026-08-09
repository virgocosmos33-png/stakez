"""God Mode AI idle → Spine 4.1 for Cell Seal full-reel characters (H1–H5).

Uploads each assets-raw/cellSeal/{id}_full.png, runs sidescrolling/idle sprite
generation, packs a Spine 4.1.23 sequence skeleton named ``idle`` under:

  static/assets/spines/cellSeal/{id}.json
  static/assets/spines/cellSeal/cellSeal.atlas
  static/assets/spines/cellSeal/cellSeal.webp

Auth: game-builder/.godmode-settings.json  {"apiKey":"gmd_..."}
Env: CELL_SEAL_IDS=H1,H2  GODMODE_ACTION=sidescrolling_idle_ffg

Run:
  python tools/godmode_cell_seal_spines.py
  python tools/godmode_cell_seal_spines.py --ids H1
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
from pathlib import Path

# Reuse lady GodMode helpers (auth, upload, sprite, slice, sequence skel).
sys.path.insert(0, str(Path(__file__).resolve().parent))
import godmode_lady_spine as gm  # noqa: E402

APP = Path(__file__).resolve().parents[1]
RAW = APP / "assets-raw" / "cellSeal"
OUT = APP / "static" / "assets" / "spines" / "cellSeal"
GM_RAW = APP / "tools" / "scenario_out" / "godmode_cellSeal"
SYMBOLS = ["H1", "H2", "H3", "H4", "H5"]

PROMPTS = {
    "H1": (
        "Pale gaunt woman in white straitjacket, full-body vertical reel character, "
        "shallow breathing idle, clinical asylum padded cell, transparent background"
    ),
    "H2": (
        "Young pale doctor in white lab coat holding clipboard, full-body vertical "
        "reel character, subtle idle breathing, clinical asylum, transparent background"
    ),
    "H3": (
        "Terrifying bald grinning grey figure full-body vertical reel character, "
        "subtle idle presence, clinical asylum horror, transparent background"
    ),
    "H4": (
        "Young girl in thin hospital gown full-body vertical reel character near "
        "dark doorway, subtle idle sway, clinical dread, transparent background"
    ),
    "H5": (
        "Restrained patient with 404 stamped on forehead, leather straps, full-body "
        "vertical reel character, subtle idle breathing, transparent background"
    ),
}
NEGATIVE = (
    "circular medallion, coin icon, UI badge, text overlay, casino neon, purple, "
    "extra limbs, deformed hands, busy background, logo"
)


def write_shared_atlas(built: dict[str, tuple], fps: float) -> None:
    """built[prefix] = (packed_frames, display_w, display_h, json_name)."""
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
    page = gm.Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for r in all_regions:
        page.alpha_composite(r["img"], (r["ax"], r["ay"]))

    OUT.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    page.save(buf, "WEBP", lossless=True, quality=100)
    gm.robust_write(OUT / "cellSeal.webp", buf.getvalue())

    lines = ["cellSeal.webp", f"size:{W},{H}", "filter:Linear,Linear", "scale:1"]
    for r in all_regions:
        w, h = r["img"].size
        lines.append(r["name"])
        lines.append(f"bounds:{r['ax']},{r['ay']},{w},{h}")
    gm.robust_write(OUT / "cellSeal.atlas", ("\n".join(lines) + "\n").encode("utf-8"))
    print(f"[atlas] cellSeal.webp {W}x{H} regions={len(all_regions)}", flush=True)

    for prefix, (frames, dw, dh, json_name) in built.items():
        skel = gm.build_sequence_skel(prefix, len(frames), dw, dh, fps=fps)
        gm.robust_write(OUT / json_name, json.dumps(skel).encode("utf-8"))
        print(f"[skel] {json_name} frames={len(frames)} display={dw}x{dh}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="GodMode idle → Cell Seal spines H1–H5")
    ap.add_argument("--ids", default=os.environ.get("CELL_SEAL_IDS", ",".join(SYMBOLS)))
    ap.add_argument("--action", default=os.environ.get("GODMODE_ACTION", gm.DEFAULT_ACTION))
    ap.add_argument("--view", default=os.environ.get("GODMODE_VIEW", "side-scrolling"))
    ap.add_argument("--skip-bg", action="store_true")
    ap.add_argument("--fps", type=float, default=12.0)
    ap.add_argument("--target-h", type=int, default=1400)
    args = ap.parse_args()

    ids = [s.strip().upper() for s in args.ids.split(",") if s.strip()]
    ids = [s for s in ids if s in SYMBOLS]
    if not ids:
        raise SystemExit("no valid CELL_SEAL ids")

    key = gm.load_api_key()
    print(f"[auth] key={gm.mask_key(key)}", flush=True)
    GM_RAW.mkdir(parents=True, exist_ok=True)

    built: dict[str, tuple] = {}
    for sym in ids:
        src = RAW / f"{sym}_full.png"
        if not src.exists() or src.stat().st_size < 200_000:
            print(f"[skip] {sym}: missing/small still {src}", flush=True)
            continue
        # Reject obvious medallion composites (too flat / short of real full-body).
        try:
            im = gm.Image.open(src)
            if im.size[1] < 1200:
                print(f"[skip] {sym}: not tall enough {im.size}", flush=True)
                continue
        except Exception as e:
            print(f"[skip] {sym}: {e}", flush=True)
            continue

        prompts = {
            "positive": PROMPTS[sym],
            "negative": NEGATIVE,
        }
        print(f"[variant] {sym} src={src.name}", flush=True)
        # Stage a copy under GM_RAW so downloads have unique stems.
        staged = GM_RAW / f"{sym}_src.png"
        staged.write_bytes(src.read_bytes())
        frames = gm.run_variant(
            key, staged, args.action, args.view, prompts, skip_bg=args.skip_bg
        )
        packed, dw, dh = gm.normalize_frames(frames, args.target_h)
        prefix = f"{sym.lower()}_idle"
        built[prefix] = (packed, dw, dh, f"{sym}.json")

    if not built:
        raise SystemExit("no spines built — need Scenario full-body stills in assets-raw/cellSeal/")

    write_shared_atlas(built, fps=args.fps)
    print(json.dumps({"ok": True, "symbols": list(built.keys()), "out": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
