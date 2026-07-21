"""Capture the reel board + ornate frame across orientations for the
Madam Mirror reel-frame QA (white-backing-leak fix).

Writes PNGs to web-sdk/qa-shots/reelframe/<label>-<view>.png.

Run: python tools/qa_reel_frame.py [label]   (label e.g. before|after)

NOTE (Windows): Playwright reliably WRITES the PNGs (the [shot] lines
print once each file exists) but may HANG on browser teardown. If it
hangs after the final [shot], the files are already on disk.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

LABEL = sys.argv[1] if len(sys.argv) > 1 else "before"
# no action click -> the settled INITIAL_BOARD (symbols visible), matching
# the live game reel view the user screenshotted.
STORY = "components-game--pre-spin"
BASE = f"http://localhost:6001/iframe.html?viewMode=story&id={STORY}"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "reelframe"
OUT.mkdir(parents=True, exist_ok=True)

# (view name, width, height) — cover the orientations the board reflows in
VIEWS = [
    ("landscape", 1600, 900),
    ("desktop", 1422, 800),
    ("portrait", 540, 960),
    ("tablet", 820, 1180),
]


def main() -> None:
    # Load the game ONCE (assets are slow to decode under swiftshader), then
    # resize the viewport per view. One context avoids WebGL-context exhaustion.
    with sync_playwright() as play:
        browser = play.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader"])
        ctx = browser.new_context(viewport={"width": 1600, "height": 1200}, device_scale_factor=1)
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.locator("canvas").first.wait_for(state="visible", timeout=90000)

        # the Action button is DISABLED while the loading screen is up; it flips
        # to enabled the moment every asset is loaded (== board fully painted).
        # We do NOT click it -> the settled INITIAL_BOARD stays on screen.
        btn = page.locator("button.action")
        btn.wait_for(state="visible", timeout=30000)
        loaded = False
        for _ in range(360):
            if btn.is_enabled():
                loaded = True
                break
            time.sleep(1)
        print(f"[load] loaded={loaded}", flush=True)
        time.sleep(3)

        for view, w, h in VIEWS:
            page.set_viewport_size({"width": w, "height": h})
            time.sleep(3)  # let the layout reflow + repaint
            path = OUT / f"{LABEL}-{view}.png"
            page.screenshot(path=str(path))
            print(f"[shot] {path}", flush=True)

        browser.close()
        print("[done]", flush=True)


if __name__ == "__main__":
    main()
