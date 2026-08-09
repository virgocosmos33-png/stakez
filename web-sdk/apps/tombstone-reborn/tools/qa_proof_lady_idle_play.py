"""Headless proof that SceneCharacter idle webm HTMLVideoElement is playing."""

from __future__ import annotations

import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "http://localhost:6001/iframe.html?viewMode=story&id=mode-base-book--random"
OUT = Path(__file__).resolve().parents[1] / "assets-raw" / "lady_video" / "_qa"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> int:
	logs: list[tuple[str, str]] = []
	with sync_playwright() as play:
		browser = play.chromium.launch()
		page = browser.new_page(viewport={"width": 1440, "height": 900})
		page.on("console", lambda m: logs.append((m.type, m.text)))
		page.goto(URL, wait_until="commit", timeout=120_000)

		proof = None
		for _ in range(70):
			time.sleep(1)
			# dismiss loading carousel / click story Action if present
			for text in ("CONTINUE", "Continue", "Action"):
				loc = page.get_by_text(text, exact=False).first
				try:
					if loc.is_visible():
						loc.click(timeout=400)
				except Exception:
					pass
			proof = page.evaluate("() => window.__ladyIdleProof || null")
			if proof and proof.get("playing") and proof.get("advanced"):
				break

		page.screenshot(path=str(OUT / "story_desktop.png"))
		browser.close()

	print("PROOF", json.dumps(proof, indent=2))
	print("--- SceneCharacter console ---")
	for typ, msg in logs:
		if "SceneCharacter" in msg or "idle video" in msg:
			print(typ, msg[:500])

	ok = bool(proof and proof.get("playing") and proof.get("advanced"))
	print("RESULT", "PASS" if ok else "FAIL")
	return 0 if ok else 1


if __name__ == "__main__":
	raise SystemExit(main())
