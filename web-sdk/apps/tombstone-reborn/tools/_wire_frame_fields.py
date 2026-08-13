import os
from PIL import Image

SRC = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"
APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

JOBS = [
    ("tr_wood_grey_tile.png", "board_wood_grey.webp"),
    ("tr_stone_grey_tile.png", "board_stone_grey.webp"),
]

for src_name, out_name in JOBS:
    img = Image.open(os.path.join(SRC, src_name)).convert("RGB")
    if img.size != (1024, 1024):
        img = img.resize((1024, 1024), Image.LANCZOS)
    for base in ("assets", os.path.join("static", "assets")):
        dst = os.path.join(APP, base, "sprites", "board")
        if os.path.isdir(dst):
            path = os.path.join(dst, out_name)
            img.save(path, format="WEBP", quality=90, method=6)
            print("wrote", path)
print("done")
