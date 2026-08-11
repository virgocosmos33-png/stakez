"""Capture the new baked board reel-frame in Storybook at several canvas sizes.

Verifies the frame skin (BoardPlate.svelte) live: base board + a feature board,
at desktop / landscape / portrait, and reports pageerror + console.error counts.

Run: python tools/qa_capture_board_frame.py [port]
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = sys.argv[1] if len(sys.argv) > 1 else "6009"
BASE = f"http://localhost:{PORT}/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "board_frame"
OUT.mkdir(parents=True, exist_ok=True)

SHOTS = [
	("mode-base-book--dead-spin", "base", 1600, 900),
	("mode-base-book--dead-spin", "base_portrait", 540, 960),
	("mode-base-book--dead-spin", "base_desktop", 1422, 800),
	("mode-bonus-book--small-bonus-win", "bonus", 1600, 900),
	("mode-bonus-book--super-split", "supersplit", 1600, 900),
]
BOOT_BUDGET = 90  # s to wait for the engine to leave "Initialising..."
SETTLE = 6  # s mid-idle after boot


def wait_booted(page) -> None:
	deadline = time.time() + BOOT_BUDGET
	while time.time() < deadline:
		time.sleep(2)
		try:
			body = page.evaluate("document.body.innerText")
		except Exception:
			body = ""
		if body and "Initialising" not in body:
			return


def main() -> None:
	with sync_playwright() as play:
		browser = play.chromium.launch()
		for story, name, w, h in SHOTS:
			page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
			perr: list[str] = []
			cerr: list[str] = []
			page.on("pageerror", lambda e: perr.append(str(e)))
			page.on(
				"console",
				lambda m: cerr.append(f"{m.type}: {m.text}") if m.type == "error" else None,
			)
			page.goto(BASE + story, wait_until="commit", timeout=120000)
			wait_booted(page)
			time.sleep(SETTLE)
			out = OUT / f"{name}.png"
			page.screenshot(path=str(out))
			print(f"[shot] {out.name}  ({w}x{h})  story={story}", flush=True)
			print(f"       pageerror={len(perr)}  console.error={len(cerr)}", flush=True)
			for e in sorted(set(perr))[:6]:
				print("   PE:", e[:200], flush=True)
			for e in sorted(set(cerr))[:6]:
				print("   CE:", e[:200], flush=True)
			page.close()
		browser.close()


if __name__ == "__main__":
	main()
