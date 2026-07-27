from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

PKG = Path(__file__).resolve().parents[3] / "packages" / "components-ui-html" / "src" / "assets" / "paytable"
TMP = Path(__file__).resolve().parents[1] / ".tmp_paytable_chrome"


def sil(a: np.ndarray) -> np.ndarray:
	al = a[..., 3] > 40
	al = ndimage.binary_opening(al, iterations=1)
	closed = ndimage.binary_closing(al, iterations=5)
	filled = ndimage.binary_fill_holes(closed)
	labeled, n = ndimage.label(filled)
	counts = np.bincount(labeled.ravel())
	counts[0] = 0
	return labeled == counts.argmax()


def main() -> None:
	for name in (
		"section_magenta.png",
		"section_magenta_wide.png",
		"blanked_section_magenta.png",
		"blanked_section_magenta_wide.png",
	):
		p = PKG / name if (PKG / name).exists() else TMP / name
		if not p.exists():
			print("missing", name)
			continue
		a = np.array(Image.open(p).convert("RGBA"))
		rgb = a[..., :3].astype(float)
		body = sil(a)
		interior = ndimage.binary_erosion(body, iterations=3)
		edge = body & ~interior
		low = rgb[..., 0] < 170
		print(
			f"{p.name}: lowR interior={(interior & low).sum()} edge={(edge & low).sum()} "
			f"Rmin_int={rgb[interior, 0].min() if interior.any() else None}"
		)

	from_ref = np.array(Image.open(TMP / "section_magenta_wide_from_ref.png").convert("RGBA"))
	blank = np.array(Image.open(PKG / "section_magenta_wide.png").convert("RGBA"))
	fr = np.array(Image.fromarray(from_ref).resize((blank.shape[1], blank.shape[0]), Image.NEAREST))
	h = max(fr.shape[0], blank.shape[0])
	w = fr.shape[1]
	canvas = np.zeros((h * 2 + 20, w, 4), dtype=np.uint8)
	canvas[: fr.shape[0], :w] = fr
	canvas[h + 20 : h + 20 + blank.shape[0], :w] = blank
	Image.fromarray(canvas).save(TMP / "compare_wide_before_after.png")
	c = blank[:, 350:750]
	Image.fromarray(c).resize((800, c.shape[0] * 2), Image.NEAREST).save(TMP / "wide_center_2x.png")
	cn = np.array(Image.open(PKG / "section_magenta.png").convert("RGBA"))
	c2 = cn[80:230, 250:650]
	Image.fromarray(c2).resize((800, c2.shape[0] * 2), Image.NEAREST).save(TMP / "narrow_center_2x.png")
	print("wrote compare + center crops")


if __name__ == "__main__":
	main()
