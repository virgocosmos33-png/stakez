import os
import numpy as np
from PIL import Image

SRC = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets\tr_cell_frame_grey.png"
APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

img = Image.open(SRC).convert("RGBA")
# trim transparent margin to the frame's alpha bbox
alpha = img.getchannel("A")
bbox = alpha.getbbox()
if bbox:
    img = img.crop(bbox)
print("trimmed size", img.size)

# fit to the cell aspect CELL_PITCH_X:SYMBOL_SIZE = 0.8 (300x375)
img = img.resize((300, 375), Image.LANCZOS)

# force fully transparent pixels to RGB 0 so pixi premultiply can't fringe
d = np.array(img)
d[d[:, :, 3] == 0] = (0, 0, 0, 0)
img = Image.fromarray(d, "RGBA")

for base in ("assets", os.path.join("static", "assets")):
    dst = os.path.join(APP, base, "sprites", "board")
    if os.path.isdir(dst):
        path = os.path.join(dst, "board_cell_frame.png")
        img.save(path, optimize=True)
        print("wrote", path)
print("done")
