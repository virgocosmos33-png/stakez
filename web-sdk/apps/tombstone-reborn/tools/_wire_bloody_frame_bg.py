import os
from PIL import Image

SRC = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"
APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def write_trees(img, sub, name, **save_kwargs):
    for base in ("assets", os.path.join("static", "assets")):
        dst = os.path.join(APP, base, "sprites", sub)
        if os.path.isdir(dst):
            path = os.path.join(dst, name)
            img.save(path, **save_kwargs)
            print("wrote", path, img.size)


# --- board wood: overwrite the bake input so make_board_frame_image.py picks it
wood = Image.open(os.path.join(SRC, "tr_wood_bloody_tile.png")).convert("RGB")
if wood.size != (1024, 1024):
    wood = wood.resize((1024, 1024), Image.LANCZOS)
write_trees(wood, "board", "board_wood_grey.webp", format="WEBP", quality=92, method=6)

# --- new background (4:3 native) — fresh filename so no cache serves the old one
bg = Image.open(os.path.join(SRC, "tr_scene_bg_v2.png")).convert("RGB")
bg = bg.resize((1536, 1152), Image.LANCZOS)
write_trees(bg, "scene", "scene_bg_v2.webp", format="WEBP", quality=88, method=6)
print("done")
