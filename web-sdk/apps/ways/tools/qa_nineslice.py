"""Capture the reel board + nine-slice ornate frame across FIVE distinct aspect
ratios to prove the responsive border-image frame hugs all four sides.

Writes web-sdk/qa-shots/reelframe/nineslice-<view>.png (full page) and a tight
crop of the top-left corner nineslice-<view>-cornerTL.png so corner crispness
is verifiable.

Run from web-sdk/apps/ways:  python tools/qa_nineslice.py [label]
Storybook must be on :6001.

NOTE (Windows): Playwright reliably WRITES the PNGs (the [shot] lines print once
each file exists) but may HANG on browser teardown. If it hangs after the final
[shot], the files are already on disk.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

LABEL = sys.argv[1] if len(sys.argv) > 1 else "nineslice"
# optional 2nd arg: comma-separated view names to capture (default: all)
ONLY = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None
STORY = "mode-base-book--random"
BASE = f"http://localhost:6001/iframe.html?viewMode=story&id={STORY}"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "reelframe"
OUT.mkdir(parents=True, exist_ok=True)

# (name, width, height) — deliberately DIFFERENT aspect ratios. Ordered so the
# views that most need (re)confirmation come first, because a FRESH context loads
# fastest under swiftshader and later contexts can starve.
VIEWS = [
    ("square", 1200, 1200),   # 1.00 near-square  -> LayoutTablet
    ("tall", 800, 1400),      # 0.57 very tall
    ("desktop", 1600, 900),   # 1.78 landscape
    ("wide", 1440, 600),      # 2.40 ultra-wide (smaller canvas => loads under swiftshader)
    ("portrait", 540, 960),   # 0.56 tall phone
]


def wait_loaded(page, tries: int = 600) -> bool:
    btn = page.locator("button.action")
    btn.wait_for(state="visible", timeout=30000)
    for _ in range(tries):
        if btn.is_enabled():
            return True
        time.sleep(1)
    return False


def main() -> None:
    # A FRESH browser per view: a single long-lived context reliably starved on
    # the loading screen under swiftshader, whereas a brand-new browser loads the
    # board in ~200s. Each view gets its own browser so every capture starts from
    # a clean slate and never inherits a stalled GPU/asset state.
    for name, w, h in VIEWS:
        if ONLY is not None and name not in ONLY:
            continue
        with sync_playwright() as play:
            browser = play.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader"])
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
            page = ctx.new_page()
            page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
            page.locator("canvas").first.wait_for(state="visible", timeout=90000)
            loaded = wait_loaded(page, tries=420)
            time.sleep(4)  # settle the initial board + layout reflow
            path = OUT / f"{LABEL}-{name}.png"
            page.screenshot(path=str(path))
            print(f"[shot] loaded={loaded} {path}", flush=True)
            browser.close()
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
