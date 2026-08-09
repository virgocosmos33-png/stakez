"""Strip baked observation-window / padded frames from White Room symbol cards.

Restores from newest quarantine backup when present, then crops tightly to the
subject aperture and composites onto a dark charcoal void — no padded wall,
no fluorescent housing, no steel bezel left in the card.

Does NOT call Scenario / regenerate art.

Run:  python tools/strip_baked_symbol_frames.py
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

SRC = Path(__file__).resolve().parent / "symbol_art"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
QUAR = SRC / "_OLD_PADDED_WINDOW"

FRAMED = [
	"card_h1_the_patient.png",
	"card_h2_the_doctor.png",
	"card_h3_the_grin.png",
	"card_h4_the_doorway.png",
	"card_h5_file_404.png",
	"card_w_the_sealed.png",
	"card_me_it_knows.png",
	"card_hm_observation_pane.png",
	"card_s_memory_reset.png",
]


def _latest_backup(name: str) -> Path | None:
	matches = sorted(QUAR.glob(f"*_{name}"), key=lambda p: p.stat().st_mtime, reverse=True)
	return matches[0] if matches else None


def strip_frame(im: Image.Image) -> Image.Image:
	"""Aggressive center crop: subject through glass only, no housing chrome."""
	im = im.convert("RGBA")
	w, h = im.size
	# Tight aperture — original plates put subject in ~40% center window
	# under the fluorescent bar; bias down to skip the tube housing.
	crop_frac = 0.42
	cw, ch = int(w * crop_frac), int(h * crop_frac)
	x0 = (w - cw) // 2
	y0 = (h - ch) // 2 + int(h * 0.06)
	subject = im.crop((x0, y0, x0 + cw, y0 + ch))

	out = Image.new("RGBA", (w, h), (18, 16, 14, 255))
	# Fill most of the plate so the UI bezel can sit outside the subject
	tw, th = int(w * 0.92), int(h * 0.92)
	subject = subject.resize((tw, th), Image.LANCZOS)

	mask = Image.new("L", (tw, th), 0)
	md = ImageDraw.Draw(mask)
	pad = max(6, tw // 50)
	md.rounded_rectangle([pad, pad, tw - pad - 1, th - pad - 1], radius=tw // 18, fill=255)
	mask = mask.filter(ImageFilter.GaussianBlur(2))

	placed = Image.new("RGBA", (w, h), (0, 0, 0, 0))
	ox, oy = (w - tw) // 2, (h - th) // 2
	placed.paste(subject, (ox, oy), mask)
	out.alpha_composite(placed)
	return out


def main() -> None:
	QUAR.mkdir(parents=True, exist_ok=True)
	n = 0
	for name in FRAMED:
		src = SRC / name
		bak = _latest_backup(name)
		# Prefer original framed master from quarantine so re-runs don't re-crop strips
		source_path = bak if bak and bak.is_file() else src
		if not source_path.is_file():
			print(f"skip missing {name}")
			continue
		# Keep a fresh backup of whatever we strip from if no quarantine yet
		if bak is None and src.is_file():
			shutil.copy2(src, QUAR / f"{STAMP}_{name}")
			print(f"quarantined {name}")
		stripped = strip_frame(Image.open(source_path))
		stripped.save(src, "PNG")
		print(f"stripped {name} from {source_path.name}")
		n += 1
	print(f"done: {n} cards")


if __name__ == "__main__":
	main()
