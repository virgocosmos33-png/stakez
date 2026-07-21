"""Diagnose why the base story renders blank: capture pageerror + console
error + whether the pixi canvas ever gets content. Longer wait for Vite.

Run:  python tools/qa_probe_boot.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--random"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "lady"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page_errors: list[str] = []
        console_errors: list[str] = []
        page.on("pageerror", lambda e: page_errors.append(str(e)))
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.goto(BASE + STORY, wait_until="commit", timeout=120000)

        prev = 0
        for wait_s in (20, 35, 50, 65):
            time.sleep(wait_s - prev)
            prev = wait_s
            has_canvas = page.evaluate("!!document.querySelector('canvas')")
            body_txt = page.evaluate("document.body.innerText.slice(0,120)")
            safe = body_txt.encode("ascii", "replace").decode("ascii").replace("\n", " ")
            print(f"@{wait_s}s canvas={has_canvas} body={safe!r}", flush=True)
        page.screenshot(path=str(OUT / "boot.png"))
        print("[shot] boot.png", flush=True)
        browser.close()

    print("\n=== pageerror ===", flush=True)
    for e in sorted(set(page_errors))[:15]:
        print("  ", e[:300])
    print("=== console.error ===", flush=True)
    for e in sorted(set(console_errors))[:15]:
        print("  ", e[:300])


if __name__ == "__main__":
    sys.exit(main())
