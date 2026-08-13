"""Wire the last-reel lane art: the locked-lid cover + the three golden
special cards (BOUNTY / SUPER SPLIT / NUDGE) shown when the lane fires.

All four are opaque full-bleed cards, so no keying — just downscale and drop
into the sprite folders (assets/ + static/assets mirror when present).
"""

import os

from PIL import Image

GEN = os.path.normpath(
    os.path.join(
        os.path.expanduser("~"),
        ".cursor",
        "projects",
        "c-Users-Emex33-Desktop-stakez",
        "assets",
    )
)
APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# generated file -> output name (all land in sprites/tombstone/)
FILES = {
    "tr_lid_lock.png": "lane_lid_lock",
    "tr_gold_bounty.png": "lane_gold_bounty",
    "tr_gold_supersplit.png": "lane_gold_supersplit",
    "tr_gold_nudge.png": "lane_gold_nudge",
}

TARGET_W = 384  # plenty for a ~120px cell

for src_name, out_name in FILES.items():
    src = os.path.join(GEN, src_name)
    if not os.path.isfile(src):
        print("missing", src)
        continue
    img = Image.open(src).convert("RGB")
    scale = TARGET_W / img.width
    img = img.resize((TARGET_W, round(img.height * scale)), Image.LANCZOS)
    for base in ("assets", os.path.join("static", "assets")):
        dst_dir = os.path.join(APP, base, "sprites", "tombstone")
        if not os.path.isdir(dst_dir):
            continue
        path = os.path.join(dst_dir, f"{out_name}.webp")
        img.save(path, "WEBP", quality=88, method=6)
        print("wrote", path, img.size)
print("done")
