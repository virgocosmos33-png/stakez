"""Rapid-fire screenshots of the mirror-burst showcase to catch the new FX:
- split detonation (hit-stop seam flare, flash, shockwave, sparks, shake)
- green plasma liner burning around the linked win symbols

Run:  python tools/qa_capture_fx.py
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "fx"
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as play:
    browser = play.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.goto(BASE + "mode-base-book--mirror-burst-showcase", wait_until="domcontentloaded")
    time.sleep(14)
    try:
        page.get_by_text("Action", exact=True).first.click(timeout=5000)
        print("action clicked", flush=True)
    except Exception as error:  # noqa: BLE001
        print(f"action click failed: {error}", flush=True)

    start = time.monotonic()
    shot = 0
    # 3s..13s covers telegraph, blade sweep, detonation, and the win liner
    while time.monotonic() - start < 3.0:
        time.sleep(0.02)
    while time.monotonic() - start < 13.0:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        page.screenshot(path=str(OUT / f"fx{shot:03d}_{elapsed_ms}.png"))
        shot += 1
    browser.close()
    print(f"{shot} shots", flush=True)
    for e in sorted(set(errors))[:10]:
        print("ERR:", e[:300], flush=True)
