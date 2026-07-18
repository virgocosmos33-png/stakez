"""Capture the Components/<Symbol> contact-sheet story to verify the revamped
symbol states (spin smear, weighty land, plasma-strobe win, postwin smolder),
then a mirror-burst book run for the in-game look.

Run:  python tools/qa_capture_states.py
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "states"
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as play:
    browser = play.chromium.launch()
    page = browser.new_page(viewport={"width": 1400, "height": 800})
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)

    # 1. the symbol contact sheet: three timed shots to catch anim phases
    page.goto(BASE + "components-symbol--symbols", wait_until="domcontentloaded")
    time.sleep(12)
    for i in range(6):
        page.screenshot(path=str(OUT / f"sheet_{i}.png"))
        time.sleep(0.45)

    # 2. in-game: mirror burst book (landing smears, land squash, win strobe)
    page.goto(BASE + "mode-base-book--mirror-burst-showcase", wait_until="domcontentloaded")
    time.sleep(10)
    try:
        page.get_by_text("Action", exact=True).first.click(timeout=15000)
        print("action clicked", flush=True)
    except Exception as error:  # noqa: BLE001
        print(f"action click failed: {error}", flush=True)
    start = time.monotonic()
    shot = 0
    while time.monotonic() - start < 13.0:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        page.screenshot(path=str(OUT / f"game_{shot:03d}_{elapsed_ms}.png"))
        shot += 1
    browser.close()
    print(f"{shot} game shots", flush=True)
    for e in sorted(set(errors))[:12]:
        print("ERR:", e[:300], flush=True)
