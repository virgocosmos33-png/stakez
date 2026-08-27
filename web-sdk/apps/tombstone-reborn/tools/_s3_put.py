"""PUT local files to Scenario multipart URLs. No extra AWS checksum headers."""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path


def main() -> None:
	jobs = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
	src = Path(sys.argv[2])
	for job in jobs:
		path = src / f"{job['slug']}.png"
		data = path.read_bytes()
		req = urllib.request.Request(job["url"], data=data, method="PUT")
		with urllib.request.urlopen(req, timeout=120) as resp:
			print(resp.status, job["slug"], len(data))


if __name__ == "__main__":
	main()
