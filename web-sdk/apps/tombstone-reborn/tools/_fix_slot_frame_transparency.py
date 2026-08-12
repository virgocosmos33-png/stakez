"""Knock the opaque near-white interior out of board_slot_frame.png so the
scene shows through the cells (the slot frame should be a thin iron BORDER with
a transparent centre, not a white plate). Keeps the dark iron border and its
anti-aliased inner edge via a luminance ramp.
"""
from PIL import Image

PATHS = [
    r"web-sdk\apps\tombstone-reborn\assets\sprites\board\board_slot_frame.png",
    r"web-sdk\apps\tombstone-reborn\static\assets\sprites\board\board_slot_frame.png",
]

# luminance <= KEEP  -> fully opaque (dark iron border stays)
# luminance >= DROP  -> fully transparent (white interior gone)
# linear ramp between -> smooth inner edge
KEEP = 140.0
DROP = 200.0


def fix(path):
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    changed = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            if lum <= KEEP:
                continue
            if lum >= DROP:
                new_a = 0
            else:
                new_a = int(a * (DROP - lum) / (DROP - KEEP))
            if new_a != a:
                px[x, y] = (r, g, b, new_a)
                changed += 1
    im.save(path)
    print(f"{path}: {changed} px cleared, center now {im.getpixel((w // 2, h // 2))}")


for p in PATHS:
    fix(p)
