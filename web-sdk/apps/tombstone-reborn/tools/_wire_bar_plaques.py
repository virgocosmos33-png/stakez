"""Wire the v2 special-bar plaques: gold-on-iron nameplates (generated 16:9)
squashed to the bar's 2:1 plaque aspect and dropped over the old files.

The seated-card path in SpecialBarPlaque draws the sprite at cellW x cellH with
PLAQUE_ASPECT = 384/192 = 2:1, so a gentle 11% vertical squash beats cropping
into the riveted border.
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

FILES = {
    "tr_plaque_gang.png": "bar_plaque_gang.png",
    "tr_plaque_outlaw.png": "bar_plaque_outlaw.png",
    "tr_plaque_smoke.png": "bar_plaque_smoke.png",
    "tr_plaque_digup.png": "bar_plaque_digup.png",
    "tr_plaque_open.png": "bar_plaque_open.png",
}

W, H = 512, 256

for src_name, out_name in FILES.items():
    src = os.path.join(GEN, src_name)
    if not os.path.isfile(src):
        print("missing", src)
        continue
    img = Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)
    for base in ("assets", os.path.join("static", "assets")):
        dst_dir = os.path.join(APP, base, "sprites", "tombstone")
        if not os.path.isdir(dst_dir):
            continue
        path = os.path.join(dst_dir, out_name)
        img.save(path, optimize=True)
        print("wrote", path, img.size)
print("done")
