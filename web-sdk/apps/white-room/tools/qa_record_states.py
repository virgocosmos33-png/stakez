"""Record the mirror-burst book run to video for frame-level verification of
the revamped states: spin smears while reels fall, weighty land squash,
plasma-strobe wins, postwin smolder.

Run:  python tools/qa_record_states.py
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "states-video"
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as play:
    browser = play.chromium.launch()
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        record_video_dir=str(OUT),
        record_video_size={"width": 1280, "height": 720},
    )
    page = context.new_page()
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)

    page.goto(BASE + "mode-base-book--mirror-burst-showcase", wait_until="domcontentloaded")
    time.sleep(10)
    try:
        page.get_by_text("Action", exact=True).first.click(timeout=15000)
        print("action clicked", flush=True)
    except Exception as error:  # noqa: BLE001
        print(f"action click failed: {error}", flush=True)
    time.sleep(16)
    context.close()
    browser.close()
    for e in sorted(set(errors))[:12]:
        print("ERR:", e[:300], flush=True)
    print("video saved", flush=True)
