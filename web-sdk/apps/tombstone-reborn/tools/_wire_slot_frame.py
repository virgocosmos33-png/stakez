import os
import numpy as np
from PIL import Image

SRC = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets\tr_slot_frame.png"
APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

img = Image.open(SRC).convert("RGBA")
bbox = img.getchannel("A").getbbox()
if bbox:
    img = img.crop(bbox)
# cell aspect CELL_PITCH_X:SYMBOL_SIZE = 118.4:148 = 0.8 -> 300x375
img = img.resize((300, 375), Image.LANCZOS)

d = np.array(img)
d[d[:, :, 3] == 0] = (0, 0, 0, 0)
img = Image.fromarray(d, "RGBA")

for base in ("assets", os.path.join("static", "assets")):
    dst = os.path.join(APP, base, "sprites", "board")
    if os.path.isdir(dst):
        path = os.path.join(dst, "board_slot_frame.png")
        img.save(path, optimize=True)
        print("wrote", path)
print("done")
