"""High-framerate capture of the SPLIT / target-lock feature stories.

Run:  python tools/qa_capture_split_lock.py [story-id ...]

Plain `page.screenshot()` costs ~0.9s a frame, which skips clean over the strike
(the seam sweep + detonation together last well under a second). This drives the
CDP screencast instead, so the whole telegraph -> lock -> strike -> settle window
lands at video framerate, and reports any console errors the run produced.
"""

from __future__ import annotations

import base64
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6009/iframe.html?viewMode=story&id="
OUT_ROOT = Path(__file__).resolve().parents[1] / "qa-shots" / "split_lock"

DEFAULT_STORIES = (
	"mode-base-book--split-gang",
	"mode-base-book--split-outlaws",
	"mode-bonus-book--super-split",
)

BOOT_SECONDS = 14.0
CAPTURE_SECONDS = 26.0


def capture(story: str) -> None:
	out = OUT_ROOT / story
	out.mkdir(parents=True, exist_ok=True)
	for stale in out.glob("*.png"):
		stale.unlink()
	for stale in out.glob("*.jpg"):
		stale.unlink()

	with sync_playwright() as play:
		browser = play.chromium.launch(args=["--disable-gpu", "--no-sandbox"])
		page = browser.new_page(viewport={"width": 1280, "height": 800})
		errors: list[str] = []
		page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
		page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
		# generous: a cold Vite dev server compiles the story graph on demand and
		# the first navigation after a cache clear runs well past the 30s default
		page.goto(BASE + story, wait_until="domcontentloaded", timeout=180_000)
		# Wait for the story's own Action control to exist rather than sleeping a
		# fixed number of seconds and hoping. A cold dev server can take longer
		# than any fixed boot delay to compile the graph, and when it did, every
		# frame captured was the loading spinner on a blank white page — a
		# "successful" run with 842 frames of nothing.
		action = page.get_by_text("Action", exact=True).first
		try:
			action.wait_for(state="visible", timeout=180_000)
		except Exception as error:  # noqa: BLE001
			print(f"[{story}] no Action control: {error}", flush=True)
		time.sleep(BOOT_SECONDS)

		session = page.context.new_cdp_session(page)
		frames: list[bytes] = []
		start = time.monotonic()

		def on_frame(event: dict) -> None:
			frames.append(base64.b64decode(event["data"]))
			try:
				session.send("Page.screencastFrameAck", {"sessionId": event["sessionId"]})
			except Exception:  # noqa: BLE001 — screencast already stopped
				pass

		session.on("Page.screencastFrame", on_frame)
		session.send(
			"Page.startScreencast",
			{"format": "jpeg", "quality": 90, "everyNthFrame": 1},
		)

		try:
			action.click(timeout=30_000)
		except Exception as error:  # noqa: BLE001
			print(f"[{story}] action click failed: {error}", flush=True)

		while time.monotonic() - start < CAPTURE_SECONDS:
			page.wait_for_timeout(200)
		session.send("Page.stopScreencast")
		browser.close()

	for index, data in enumerate(frames):
		(out / f"f{index:04d}.jpg").write_bytes(data)

	print(f"[{story}] {len(frames)} frames -> {out}", flush=True)
	for message in sorted(set(errors))[:10]:
		print(f"[{story}] ERR: {message[:300]}", flush=True)


def main() -> None:
	stories = tuple(sys.argv[1:]) or DEFAULT_STORIES
	for story in stories:
		capture(story)


if __name__ == "__main__":
	main()
