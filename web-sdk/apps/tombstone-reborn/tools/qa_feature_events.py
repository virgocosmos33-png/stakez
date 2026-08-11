"""Screencast every non-split feature event and pull its peak frame.

page.screenshot() costs over a second per frame in headless-without-GPU, which
is longer than most of these bursts — screenshotting on a timer walks straight
past the event and reads as "the overlay never rendered". This streams frames
over CDP instead and then finds the event by change detection over the board,
so every event is judged on a frame it actually occupies.

Outputs, per story:
  qa-shots/events/<story>/cast/*.jpg   every streamed frame
  qa-shots/events/<story>_peak.jpg     the busiest board frame, full size
  qa-shots/events/<story>_strip.jpg    the run either side of the peak

Run Storybook on 6009 first, then:
  python tools/qa_feature_events.py [story-id ...]
"""

from __future__ import annotations

import asyncio
import base64
import io
import os
import sys
import time

import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(APP, "qa-shots", "events")

BASE = "http://localhost:6009/iframe.html?viewMode=story&id="
BOOT_TIMEOUT_MS = 180_000
# the bonus books run five split events before their own feature, so they need
# a much longer window than the base ones
RECORD_S = float(os.environ.get("QA_RECORD_S", "16"))
# the board and both rails, so a nudge riding off a reel is still in frame
BOARD = (250, 80, 1030, 620)
STRIP = 8

STORIES = [
	"mode-bonus-book--nudge",
	"mode-base-book--gunsmoke",
	"mode-base-book--tombstone-open",
	"mode-base-book--special-bar-hit",
	"mode-bonus-book--bounty",
	"mode-base-book--dead-spin",
	"mode-base-book--dig-up",
]


async def record(story: str) -> tuple[list[tuple[int, bytes]], list[tuple[int, str]]]:
	frames: list[tuple[int, bytes]] = []
	marks: list[tuple[int, str]] = []
	async with async_playwright() as play:
		browser = await play.chromium.launch(args=["--disable-gpu", "--no-sandbox"])
		page = await browser.new_page(viewport={"width": 1280, "height": 800})
		await page.goto(BASE + story, wait_until="domcontentloaded", timeout=300_000)
		# the Storybook control, not the game's spin button: the game button
		# opens the tutorial carousel instead of running the book
		action = page.get_by_text("Action", exact=True).first
		await action.wait_for(timeout=BOOT_TIMEOUT_MS)
		await page.wait_for_function(
			"() => { const b = [...document.querySelectorAll('button')]"
			".find(b => b.textContent.trim() === 'Action'); return b && !b.disabled; }",
			timeout=BOOT_TIMEOUT_MS,
		)
		await asyncio.sleep(2)

		client = await page.context.new_cdp_session(page)
		start = time.monotonic()

		def on_console(message) -> None:
			if message.text.startswith("[qa-mark]"):
				marks.append(
					(int((time.monotonic() - start) * 1000), message.text.split(" ", 1)[1])
				)

		page.on("console", on_console)

		def on_frame(params: dict) -> None:
			frames.append(
				(int((time.monotonic() - start) * 1000), base64.b64decode(params["data"]))
			)
			asyncio.get_running_loop().create_task(
				client.send("Page.screencastFrameAck", {"sessionId": params["sessionId"]})
			)

		client.on("Page.screencastFrame", on_frame)
		await client.send(
			"Page.startScreencast",
			{"format": "jpeg", "quality": 82, "maxWidth": 1280, "maxHeight": 800},
		)
		start = time.monotonic()
		await action.click(force=True)
		await asyncio.sleep(RECORD_S)
		await client.send("Page.stopScreencast")
		await browser.close()
	return frames, marks


def shoot(story: str) -> None:
	cast = os.path.join(OUT, story, "cast")
	os.makedirs(cast, exist_ok=True)
	for stale in os.listdir(cast):
		os.remove(os.path.join(cast, stale))

	frames, marks = asyncio.run(record(story))
	if not frames:
		raise SystemExit(f"{story}: no screencast frames — is Storybook up on 6009?")

	boards = []
	for index, (ms, blob) in enumerate(frames):
		image = Image.open(io.BytesIO(blob)).convert("RGB")
		image.save(os.path.join(cast, f"c{index:04d}_{ms}.jpg"), quality=86)
		boards.append(np.array(image.crop(BOARD)).astype(np.int16))

	# These books run several features before the one the story is named for —
	# splits, linked fire, win lines — and any of those can out-score the event
	# under test. So when the overlays are announcing themselves, cut a strip
	# per announcement; the busiest-board fallback is only for when they are not.
	for at, name in marks:
		first = min(range(len(frames)), key=lambda i: abs(frames[i][0] - at))
		picks = [min(len(frames) - 1, first + step) for step in range(STRIP)]
		tiles = [
			Image.open(io.BytesIO(frames[i][1])).convert("RGB").crop(BOARD) for i in picks
		]
		width, height = tiles[0].size
		sheet = Image.new("RGB", (width * 4, height * 2), (0, 0, 0))
		for slot, tile in enumerate(tiles):
			sheet.paste(tile, ((slot % 4) * width, (slot // 4) * height))
		sheet.save(os.path.join(OUT, f"{story}__{name}.jpg"), quality=93)

	rest = boards[-1]
	scores = [float(np.abs(board - rest).mean()) for board in boards]
	peak = int(np.argmax(scores))

	Image.open(io.BytesIO(frames[peak][1])).convert("RGB").save(
		os.path.join(OUT, f"{story}_peak.jpg"), quality=92
	)

	picks = [min(len(frames) - 1, max(0, peak - 2 + step)) for step in range(STRIP)]
	tiles = [Image.open(io.BytesIO(frames[i][1])).convert("RGB").crop(BOARD) for i in picks]
	width, height = tiles[0].size
	sheet = Image.new("RGB", (width * STRIP, height), (0, 0, 0))
	for slot, tile in enumerate(tiles):
		sheet.paste(tile, (slot * width, 0))
	sheet.save(os.path.join(OUT, f"{story}_strip.jpg"), quality=88)

	# whole-run contact sheet: these books run several features before the one
	# the story is named for, so the peak alone is not enough to judge by
	step = max(1, len(frames) // 24)
	life = [
		Image.open(io.BytesIO(frames[i][1])).convert("RGB").crop(BOARD).resize((260, 180))
		for i in range(0, len(frames), step)
	][:24]
	board_sheet = Image.new("RGB", (260 * 6, 180 * 4), (0, 0, 0))
	for slot, tile in enumerate(life):
		board_sheet.paste(tile, ((slot % 6) * 260, (slot // 6) * 180))
	board_sheet.save(os.path.join(OUT, f"{story}_life.jpg"), quality=88)

	print(
		f"[events] {story}: {len(frames)} frames over {frames[-1][0]}ms,"
		f" peak {frames[peak][0]}ms (score {scores[peak]:.1f}); marks {marks}",
		flush=True,
	)


def main() -> None:
	os.makedirs(OUT, exist_ok=True)
	for story in sys.argv[1:] or STORIES:
		shoot(story)


if __name__ == "__main__":
	main()
