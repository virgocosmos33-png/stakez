"""Capture the EMPTY reel window (preSpin action clears the symbols) so the
frame + dark recess are fully exposed with nothing hiding a backing leak.

Run: python tools/qa_reel_empty.py [label]
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

LABEL = sys.argv[1] if len(sys.argv) > 1 else "after"
STORY = "components-game--pre-spin"
BASE = f"http://localhost:6001/iframe.html?viewMode=story&id={STORY}"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "reelframe"
OUT.mkdir(parents=True, exist_ok=True)
VIEWS = [("landscape", 1600, 900), ("desktop", 1422, 800), ("portrait", 540, 960)]


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader"])
        ctx = browser.new_context(viewport={"width": 1600, "height": 1200}, device_scale_factor=1)
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.locator("canvas").first.wait_for(state="visible", timeout=90000)
        btn = page.locator("button.action")
        btn.wait_for(state="visible", timeout=30000)
        for _ in range(360):
            if btn.is_enabled():
                break
            time.sleep(1)
        btn.click(timeout=5000)  # preSpin -> clears the board (empty window)
        time.sleep(4)
        for view, w, h in VIEWS:
            page.set_viewport_size({"width": w, "height": h})
            time.sleep(3)
            path = OUT / f"{LABEL}-empty-{view}.png"
            page.screenshot(path=str(path))
            print(f"[shot] {path}", flush=True)
        browser.close()
        print("[done]", flush=True)


if __name__ == "__main__":
    main()
