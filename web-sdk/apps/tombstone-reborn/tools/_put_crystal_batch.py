"""PUT extracted scene layers to Scenario presigned part URLs."""
from __future__ import annotations

import urllib.request
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "assets-raw" / "scene" / "crystal_src"

# (slug, upload_id) — URLs live in _u_<slug>.txt next to the PNGs
JOBS = [
	("wagon_wheel", "upl_hrwpqsw4No3UKvyArt4p6tfd"),
	("barrel", "upl_1DeTjW1UU7urbHGLLm6Rnt5D"),
	("skull", "upl_ZzKsoqu6aK7GxWhd77pMjUWz"),
	("grass_03", "upl_GXHf2L6B3Np3GqozHqZckUPk"),
	("cowboy_hat", "upl_ZKMMxxXuxZySPUyuoZ5T324h"),
	("left_hanging_lamp", "upl_oCjtV5mTEGDUvdK6nAAZbVkp"),
]


def put(slug: str) -> None:
	url = (SRC / f"_u_{slug}.txt").read_text(encoding="utf-8").strip()
	path = SRC / f"{slug}.png"
	req = urllib.request.Request(url, data=path.read_bytes(), method="PUT")
	with urllib.request.urlopen(req, timeout=180) as resp:
		print(resp.status, slug, path.stat().st_size)


if __name__ == "__main__":
	for slug, _ in JOBS:
		put(slug)
