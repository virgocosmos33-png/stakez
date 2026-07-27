"""Tight close-up of the Lady's head/face region for evidence."""
from pathlib import Path
from PIL import Image

OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "lady"
img = Image.open(OUT / "fixed.png").convert("RGB")
w, h = img.size
# she stands in the right ~quarter; crop her upper body (head/face/veil)
crop = img.crop((int(w * 0.78), int(h * 0.02), w, int(h * 0.55)))
crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)
crop.save(OUT / "fixed_face.png")
print("wrote fixed_face.png", crop.size)
