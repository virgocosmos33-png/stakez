"""Capture the digUp spades from the Storybook showcase book.

page.screenshot() costs well over a second per frame in headless-without-GPU,
which is longer than the whole burst — every earlier attempt at this landed its
first frame after the spades had already cleared, which read as "the overlay
never rendered". This streams frames over CDP instead, so the strike, the
wobble and the planted hold are all on disk, and picks the window afterwards
by change detection over the dug lane rather than by guessing a delay.

Run Storybook on 6009 first, then:  python tools/qa_digup_live.py
"""

from __future__ import annotations

import asyncio
import base64
import io
import os
import time

import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(APP, "qa-shots", "feature_vfx")
CAST = os.path.join(OUT, "cast")

STORY = "http://localhost:6009/iframe.html?viewMode=story&id=mode-base-book--dig-up"
BOOT_TIMEOUT_MS = 180_000
RECORD_S = 22.0
# the dug lane is the single-row reel on the right of the diamond board
CROP = (790, 240, 980, 480)
TILES = 8


async def record() -> tuple[list[tuple[int, bytes]], int | None]:
	frames: list[tuple[int, bytes]] = []
	mark: list[int] = []
	async with async_playwright() as play:
		browser = await play.chromium.launch(args=["--disable-gpu", "--no-sandbox"])
		page = await browser.new_page(viewport={"width": 1280, "height": 800})
		await page.goto(STORY, wait_until="domcontentloaded", timeout=300_000)
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
			if "featureBurstShow digUp" in message.text:
				mark.append(int((time.monotonic() - start) * 1000))

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
			{"format": "jpeg", "quality": 80, "maxWidth": 1280, "maxHeight": 800},
		)
		start = time.monotonic()
		await action.click(force=True)
		await asyncio.sleep(RECORD_S)
		await client.send("Page.stopScreencast")
		await browser.close()
	return frames, (mark[0] if mark else None)


def main() -> None:
	os.makedirs(CAST, exist_ok=True)
	for stale in os.listdir(CAST):
		os.remove(os.path.join(CAST, stale))
	frames, mark = asyncio.run(record())
	if not frames:
		raise SystemExit("no screencast frames — is Storybook up on 6009?")

	lanes = []
	for index, (ms, blob) in enumerate(frames):
		image = Image.open(io.BytesIO(blob)).convert("RGB")
		image.save(os.path.join(CAST, f"c{index:04d}_{ms}.jpg"), quality=88)
		lanes.append(np.array(image.crop(CROP)).astype(np.int16))

	# Prefer the component's own event mark if it happens to be logging one.
	# Otherwise find the spades directly: they are lit steel laid over a dark
	# card, so they are the one thing that makes the dug lane BRIGHTER than it
	# ends up at rest. A single argmax lands on the reel-landing flash instead,
	# so take the median of the brightest frames, which sits inside the plant.
	if mark is not None:
		start = min(range(len(frames)), key=lambda i: abs(frames[i][0] - mark))
	else:
		rest = lanes[-1].max(axis=2)
		lit = [int(((lane.max(axis=2) - rest) > 40).sum()) for lane in lanes]
		best = sorted(range(len(lit)), key=lambda i: -lit[i])[:TILES]
		start = max(0, sorted(best)[len(best) // 2] - 3)
	picks = [min(len(frames) - 1, start + offset) for offset in range(TILES)]

	tiles = [Image.open(io.BytesIO(frames[i][1])).convert("RGB").crop(CROP) for i in picks]
	width, height = tiles[0].size
	sheet = Image.new("RGB", (width * TILES, height), (0, 0, 0))
	for slot, tile in enumerate(tiles):
		sheet.paste(tile, (slot * width, 0))
	sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.LANCZOS)
	sheet.save(os.path.join(OUT, "_digup_sheet.jpg"), quality=92)
	print(
		f"[digup] {len(frames)} frames over {frames[-1][0]}ms;"
		f" burst from {frames[start][0]}ms (mark {mark}) -> _digup_sheet.jpg"
	)


if __name__ == "__main__":
	main()
