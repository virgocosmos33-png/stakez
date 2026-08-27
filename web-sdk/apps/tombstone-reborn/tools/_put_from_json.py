"""PUT files listed in a JSON array of {slug, url}."""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "assets-raw" / "scene" / "crystal_src"


def main() -> None:
	jobs = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
	for job in jobs:
		slug = job["slug"]
		path = SRC / f"{slug}.png"
		req = urllib.request.Request(job["url"], data=path.read_bytes(), method="PUT")
		try:
			with urllib.request.urlopen(req, timeout=180) as resp:
				print("OK", resp.status, slug)
		except urllib.error.HTTPError as err:
			print("FAIL", err.code, slug, err.reason)


if __name__ == "__main__":
	main()
