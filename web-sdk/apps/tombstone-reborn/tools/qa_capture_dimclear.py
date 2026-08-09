"""QA: prove the loser-dim CLEARS on the next spin.

Plays a winning book (dim + winner glint hold), then triggers a second spin and
captures the board again - the dim must be gone (board back to normal).

Run:  python tools/qa_capture_dimclear.py
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--mirror-burst-showcase"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "dim"
OUT.mkdir(parents=True, exist_ok=True)
CLIP = {"x": 360, "y": 120, "width": 560, "height": 480}


def click_action(page):
    try:
        page.get_by_text("Action", exact=True).first.click(timeout=20000)
        print("action clicked", flush=True)
    except Exception as error:  # noqa: BLE001
        print(f"action click failed: {error}", flush=True)


with sync_playwright() as play:
    browser = play.chromium.launch()
    try:
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto(BASE + STORY, wait_until="commit", timeout=120000)
        time.sleep(30)

        click_action(page)          # spin 1: produces wins
        time.sleep(16)              # let wins present + dim/glint settle
        page.screenshot(path=str(OUT / "clear_1_dimheld.png"), clip=CLIP, timeout=60000)
        print("captured dim held", flush=True)

        click_action(page)          # spin 2: reveal -> winCycleStop clears dim
        time.sleep(2.5)
        page.screenshot(path=str(OUT / "clear_2_spinning.png"), clip=CLIP, timeout=60000)
        time.sleep(4.0)
        page.screenshot(path=str(OUT / "clear_3_settled.png"), clip=CLIP, timeout=60000)
        print("captured cleared", flush=True)
    finally:
        browser.close()
    print("done", flush=True)
