"""Film the shovel dig-break story and prove the impact decal stamps ON the
symbol at the blade bite and holds.

Captures a dense burst of frames right after the story's Action fires (the digUp
burst is ~1.7s), crops to the board, and lays a contact sheet so the strike →
crack-stamp → planted-hold beat can be reviewed in one image.

Run:  python tools/qa_dig_impact.py
Storybook must be serving on :6009.
"""

from __future__ import annotations

import base64
import io
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

STORY = sys.argv[1] if len(sys.argv) > 1 else "components-featurefx--shovel-dig-break"
# the isolated FeatureFx burst is ~1.7s; the full book needs longer to spin,
# land and then dig, so allow a bigger window when a book story is filmed.
CAPTURE_SECONDS = float(sys.argv[2]) if len(sys.argv) > 2 else 3.4
BASE = "http://localhost:6009/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[1] / "qa-shots" / "dig_impact"
BOOT_TIMEOUT_MS = 180_000
# board crop from the 1280x800 template
CROP = (360, 150, 960, 690)
COLS, ROWS = 5, 3


def main() -> None:
	OUT.mkdir(parents=True, exist_ok=True)
	for stale in OUT.glob("*.jpg"):
		stale.unlink()

	with sync_playwright() as play:
		browser = play.chromium.launch(args=["--disable-gpu", "--no-sandbox"])
		page = browser.new_page(viewport={"width": 1280, "height": 800})
		errors: list[str] = []
		page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
		page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
		page.goto(BASE + STORY, wait_until="domcontentloaded", timeout=BOOT_TIMEOUT_MS)
		action = page.get_by_text("Action", exact=True).first
		try:
			action.wait_for(state="visible", timeout=BOOT_TIMEOUT_MS)
		except Exception as error:  # noqa: BLE001
			print(f"action never appeared: {error}", flush=True)

		# The board boots behind a white loading screen and the Action button stays
		# DISABLED until assets (incl. the new decal) are loaded. Filming before
		# that just captures a white frame, so wait for it to enable first.
		boot_deadline = time.monotonic() + 120
		while time.monotonic() < boot_deadline:
			try:
				if action.is_enabled():
					break
			except Exception:  # noqa: BLE001
				pass
			page.wait_for_timeout(250)
		print(f"action enabled after boot: {action.is_enabled()}", flush=True)

		session = page.context.new_cdp_session(page)
		frames: list[bytes] = []

		def on_frame(event: dict) -> None:
			frames.append(base64.b64decode(event["data"]))
			try:
				session.send("Page.screencastFrameAck", {"sessionId": event["sessionId"]})
			except Exception:  # noqa: BLE001
				pass

		session.on("Page.screencastFrame", on_frame)
		session.send("Page.startScreencast", {"format": "jpeg", "quality": 90, "everyNthFrame": 1})

		start = time.monotonic()
		try:
			action.click(timeout=10_000)
		except Exception as error:  # noqa: BLE001
			print(f"action click failed: {error}", flush=True)
		while time.monotonic() - start < CAPTURE_SECONDS:
			page.wait_for_timeout(80)
		session.send("Page.stopScreencast")
		browser.close()

	print(f"{len(frames)} frames captured", flush=True)
	if not frames:
		return

	crops = [Image.open(io.BytesIO(d)).convert("RGB").crop(CROP) for d in frames]
	for i, im in enumerate(crops):
		im.save(OUT / f"f{i:04d}.jpg", quality=90)

	wanted = COLS * ROWS
	step = max(1, len(crops) / wanted)
	picks = [min(len(crops) - 1, int(i * step)) for i in range(wanted)]
	tw = 360
	th = int(tw * crops[0].height / crops[0].width)
	sheet = Image.new("RGB", (tw * COLS, th * ROWS), (12, 12, 14))
	draw = ImageDraw.Draw(sheet)
	for idx, fi in enumerate(picks):
		col, row = idx % COLS, idx // COLS
		sheet.paste(crops[fi].resize((tw, th)), (col * tw, row * th))
		draw.text((col * tw + 6, row * th + 4), f"{fi}", fill=(255, 220, 120))
	sheet.save(OUT.parent / "dig_impact_sheet.jpg", quality=90)
	print(f"sheet -> {OUT.parent / 'dig_impact_sheet.jpg'}", flush=True)
	for message in sorted(set(errors))[:10]:
		print(f"ERR: {message[:300]}", flush=True)


if __name__ == "__main__":
	main()
