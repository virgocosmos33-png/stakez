"""QA: winner-highlight / loser-dim + idle static (no morph) verification.

Usage:  python tools/qa_capture_dim.py <story-id> <label> [t0 t1 t2 ...]

Loads a Storybook story, clicks Action, and saves CLIPPED board screenshots at
the given seconds-after-action. Small board clip avoids the full-canvas WebGL
screenshot stall. Always closes the browser in finally.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "dim"
OUT.mkdir(parents=True, exist_ok=True)

story = sys.argv[1] if len(sys.argv) > 1 else "mode-base-bookevent--win-info"
label = sys.argv[2] if len(sys.argv) > 2 else "wininfo"
times = [float(t) for t in sys.argv[3:]] or [1.5, 3.0, 5.0, 7.0, 9.0, 11.0]

# board clip for a 1280x720 viewport (centred reels, generous margin)
CLIP = {"x": 360, "y": 120, "width": 560, "height": 480}

with sync_playwright() as play:
    browser = play.chromium.launch()
    try:
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        errors: list[str] = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(BASE + story, wait_until="commit", timeout=120000)
        # first-load shader/asset compile can take a while
        time.sleep(30)

        # idle (pre-action) reference
        page.screenshot(path=str(OUT / f"{label}_idle.png"), clip=CLIP, timeout=60000)

        try:
            page.get_by_text("Action", exact=True).first.click(timeout=20000)
            print("action clicked", flush=True)
        except Exception as error:  # noqa: BLE001
            print(f"action click failed: {error}", flush=True)

        start = time.monotonic()
        for t in times:
            wait = t - (time.monotonic() - start)
            if wait > 0:
                time.sleep(wait)
            ms = int((time.monotonic() - start) * 1000)
            page.screenshot(path=str(OUT / f"{label}_{ms:05d}.png"), clip=CLIP, timeout=60000)
            print(f"shot @ {ms}ms", flush=True)
    finally:
        browser.close()
    for e in sorted(set(errors))[:12]:
        print("ERR:", e[:300], flush=True)
    print("done", flush=True)
