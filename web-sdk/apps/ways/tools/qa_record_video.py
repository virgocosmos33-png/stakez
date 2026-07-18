"""Record a video of the mirror-burst story to verify motion effects
(cut blade sweep, symbol win spines, ambient bg video).

Run:  python tools/qa_record_video.py
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "round3"
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as play:
    browser = play.chromium.launch()
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        record_video_dir=str(OUT),
        record_video_size={"width": 1280, "height": 720},
    )
    page = context.new_page()
    page.goto(BASE + "mode-base-book--mirror-burst-showcase", wait_until="domcontentloaded")
    time.sleep(12)
    try:
        page.get_by_text("Action", exact=True).first.click(timeout=5000)
        print("action clicked", flush=True)
    except Exception as error:  # noqa: BLE001
        print(f"action click failed: {error}", flush=True)
    time.sleep(16)
    video_path = page.video.path()
    context.close()
    browser.close()
    print(f"video: {video_path}", flush=True)
