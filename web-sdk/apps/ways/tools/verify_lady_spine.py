"""Reconstruct the Spine SETUP pose from lady.atlas + lady.json/lady_bonus.json
so we can eyeball that the cut-out parts reassemble into the full figure.

Renders each region at its setup-pose world position (bones have no rotation in
setup) onto a transparent canvas. -> tools/scenario_out/_rig_{base,bonus}.png
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

OUT = Path(__file__).resolve().parents[1] / "static" / "assets" / "spines" / "lady"
DBG = Path(__file__).parent / "scenario_out"
DBG.mkdir(exist_ok=True)


def parse_atlas(path: Path):
    regions = {}
    lines = path.read_text(encoding="utf-8").splitlines()
    page = lines[0]
    i = 4
    while i < len(lines):
        name = lines[i].strip()
        b = lines[i + 1].strip()
        assert b.startswith("bounds:")
        x, y, w, h = (int(v) for v in b[len("bounds:"):].split(","))
        regions[name] = (x, y, w, h)
        i += 2
    return page, regions


def render(json_name: str, out_name: str):
    skel = json.loads((OUT / json_name).read_text(encoding="utf-8"))
    page_name, regions = parse_atlas(OUT / "lady.atlas")
    page = Image.open(OUT / page_name).convert("RGBA")

    Wt = int(skel["skeleton"]["width"])
    Ht = int(skel["skeleton"]["height"])

    bones = {b["name"]: b for b in skel["bones"]}

    def world(name):
        x, y = 0.0, 0.0
        cur = name
        while cur is not None:
            b = bones[cur]
            x += b.get("x", 0.0)
            y += b.get("y", 0.0)
            cur = b.get("parent")
        return x, y

    slot_bone = {s["name"]: s["bone"] for s in skel["slots"]}
    attach = skel["skins"][0]["attachments"]

    canvas = Image.new("RGBA", (Wt, Ht), (0, 0, 0, 0))
    for slot in skel["slots"]:  # draw order back->front
        sl = slot["name"]
        region_name = slot["attachment"]
        a = attach[sl][region_name]
        bwx, bwy = world(slot_bone[sl])
        cx = bwx + a.get("x", 0.0)
        cy = bwy + a.get("y", 0.0)
        w, h = a["width"], a["height"]
        # spine center -> image top-left
        ix = int(cx + Wt / 2 - w / 2)
        iy = int(Ht / 2 - cy - h / 2)
        rx, ry, rw, rh = regions[region_name]
        sub = page.crop((rx, ry, rx + rw, ry + rh))
        if (rw, rh) != (w, h):  # atlas packed at reduced res -> upscale to display
            sub = sub.resize((int(w), int(h)), Image.LANCZOS)
        canvas.alpha_composite(sub, (ix, iy))

    bg = Image.new("RGBA", (Wt, Ht), (60, 60, 70, 255))
    bg.alpha_composite(canvas)
    bg.convert("RGB").save(DBG / out_name)
    print(f"[verify] {out_name} {Wt}x{Ht}", flush=True)


if __name__ == "__main__":
    render("lady.json", "_rig_base.png")
    render("lady_bonus.json", "_rig_bonus.png")
