"""Upload Bonus Buy chrome PNGs to Scenario via REST (api key from .scenario-settings.json)."""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]  # lady mirror drama studios
SETTINGS = ROOT / "game-builder" / ".scenario-settings.json"
FILES = [
	"cta_activate.png",
	"cta_buy.png",
	"ribbon_blank.png",
	"ribbon_scatter.png",
	"ribbon_observation.png",
	"ribbon_observation_plus.png",
	"ribbon_observation_plusplus.png",
	"ribbon_fractured.png",
	"ribbon_deepness.png",
]


def main() -> None:
	settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
	api = settings["apiKey"]
	secret = settings["secretKey"]
	project = settings["projectId"]
	auth = base64.b64encode(f"{api}:{secret}".encode()).decode()

	results: dict[str, str] = {}
	for name in FILES:
		path = HERE / name
		data = path.read_bytes()
		boundary = "----CursorBoundaryChromeUI"
		parts: list[bytes] = []

		def add_field(key: str, val: str) -> None:
			parts.append(f"--{boundary}".encode())
			parts.append(f'Content-Disposition: form-data; name="{key}"'.encode())
			parts.append(b"")
			parts.append(val.encode())

		def add_file(key: str, filename: str, payload: bytes, ctype: str) -> None:
			parts.append(f"--{boundary}".encode())
			parts.append(
				f'Content-Disposition: form-data; name="{key}"; filename="{filename}"'.encode()
			)
			parts.append(f"Content-Type: {ctype}".encode())
			parts.append(b"")
			parts.append(payload)

		add_field("name", Path(name).stem)
		add_field("type", "image")
		add_file("file", name, data, "image/png")
		parts.append(f"--{boundary}--".encode())
		parts.append(b"")
		body = b"\r\n".join(parts)

		url = f"https://api.cloud.scenario.com/v1/assets?projectId={project}"
		req = urllib.request.Request(url, data=body, method="POST")
		req.add_header("Authorization", f"Basic {auth}")
		req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
		try:
			with urllib.request.urlopen(req, timeout=120) as resp:
				payload = json.loads(resp.read().decode())
		except urllib.error.HTTPError as e:
			err = e.read().decode(errors="replace")
			print(f"FAIL {name} {e.code} {err[:400]}")
			continue
		asset_id = payload.get("id") or payload.get("asset", {}).get("id") or payload.get("assetId")
		print(f"OK {name} -> {asset_id}")
		if asset_id:
			results[name] = asset_id

	out = HERE / "scenario_chrome_assets.json"
	out.write_text(json.dumps(results, indent=2), encoding="utf-8")
	print("WROTE", out)


if __name__ == "__main__":
	main()
