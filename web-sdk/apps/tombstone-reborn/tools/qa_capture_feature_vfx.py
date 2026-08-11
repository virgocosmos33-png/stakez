"""Capture the non-split feature-event stories at video framerate and build a
contact sheet per story so the whole event window can be reviewed in one image.

Run:  python tools/qa_capture_feature_vfx.py [story-id ...]

Storybook must already be serving on :6009. Frames come from the CDP screencast
(plain page.screenshot() costs ~0.9s and skips clean over sub-second beats).
Each story writes:
    qa-shots/feature_vfx/<story>/f####.jpg   every captured frame
    qa-shots/feature_vfx/<story>_sheet.jpg   evenly sampled contact sheet
"""

from __future__ import annotations

import base64
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

BASE = "http://localhost:6009/iframe.html?viewMode=story&id="
OUT_ROOT = Path(__file__).resolve().parents[1] / "qa-shots" / "feature_vfx"

DEFAULT_STORIES = (
	"mode-base-book--dead-spin",
	"mode-base-book--special-bar-hit",
	"mode-base-book--tombstone-open",
	"mode-base-book--gunsmoke",
	"mode-base-book--dig-up",
	"mode-bonus-book--bounty",
	"mode-bonus-book--nudge",
)

# The showcase harness exposes an "Action" control that plays the story's book.
# `button.action` is the game's own spin button — clicking that just runs the
# tutorial carousel, which is what the first pass of this script filmed.
BOOT_TIMEOUT_MS = 180_000
CAPTURE_SECONDS = 50.0
SHEET_COLUMNS = 6
SHEET_ROWS = 5
SHEET_TILE_W = 420


def build_sheet(frames: list[bytes], out_path: Path, story: str) -> None:
	if not frames:
		return
	wanted = SHEET_COLUMNS * SHEET_ROWS
	step = max(1, len(frames) / wanted)
	picks = [frames[min(len(frames) - 1, int(i * step))] for i in range(wanted)]

	import io

	tiles = [Image.open(io.BytesIO(data)).convert("RGB") for data in picks]
	ratio = tiles[0].height / tiles[0].width
	tile_h = int(SHEET_TILE_W * ratio)
	sheet = Image.new("RGB", (SHEET_TILE_W * SHEET_COLUMNS, tile_h * SHEET_ROWS), (12, 12, 14))
	draw = ImageDraw.Draw(sheet)
	for index, tile in enumerate(tiles):
		col = index % SHEET_COLUMNS
		row = index // SHEET_COLUMNS
		sheet.paste(tile.resize((SHEET_TILE_W, tile_h)), (col * SHEET_TILE_W, row * tile_h))
		frame_index = min(len(frames) - 1, int(index * step))
		draw.text((col * SHEET_TILE_W + 6, row * tile_h + 4), f"{frame_index}", fill=(255, 220, 120))
	sheet.save(out_path, quality=88)
	print(f"[{story}] sheet -> {out_path}", flush=True)


def capture(story: str) -> None:
	out = OUT_ROOT / story
	out.mkdir(parents=True, exist_ok=True)
	for stale in out.glob("*.jpg"):
		stale.unlink()

	with sync_playwright() as play:
		browser = play.chromium.launch(args=["--disable-gpu", "--no-sandbox"])
		page = browser.new_page(viewport={"width": 1280, "height": 800})
		errors: list[str] = []
		page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
		page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
		page.goto(BASE + story, wait_until="domcontentloaded", timeout=BOOT_TIMEOUT_MS)
		action = page.get_by_text("Action", exact=True).first
		try:
			action.wait_for(state="visible", timeout=BOOT_TIMEOUT_MS)
		except Exception as error:  # noqa: BLE001
			print(f"[{story}] action never appeared: {error}", flush=True)

		session = page.context.new_cdp_session(page)
		frames: list[bytes] = []

		def on_frame(event: dict) -> None:
			frames.append(base64.b64decode(event["data"]))
			try:
				session.send("Page.screencastFrameAck", {"sessionId": event["sessionId"]})
			except Exception:  # noqa: BLE001 — screencast already stopped
				pass

		session.on("Page.screencastFrame", on_frame)
		session.send("Page.startScreencast", {"format": "jpeg", "quality": 88, "everyNthFrame": 1})

		start = time.monotonic()
		try:
			action.click(timeout=10_000)
		except Exception as error:  # noqa: BLE001
			print(f"[{story}] action click failed: {error}", flush=True)

		while time.monotonic() - start < CAPTURE_SECONDS:
			page.wait_for_timeout(200)
		session.send("Page.stopScreencast")
		browser.close()

	for index, data in enumerate(frames):
		(out / f"f{index:04d}.jpg").write_bytes(data)
	print(f"[{story}] {len(frames)} frames -> {out}", flush=True)
	build_sheet(frames, OUT_ROOT / f"{story}_sheet.jpg", story)

	for message in sorted(set(errors))[:12]:
		print(f"[{story}] ERR: {message[:300]}", flush=True)


def main() -> None:
	OUT_ROOT.mkdir(parents=True, exist_ok=True)
	stories = tuple(sys.argv[1:]) or DEFAULT_STORIES
	for story in stories:
		capture(story)


if __name__ == "__main__":
	main()
