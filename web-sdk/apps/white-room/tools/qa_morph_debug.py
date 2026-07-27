"""Debug FrameMorphHud visibility + console errors."""
from __future__ import annotations

import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "scene"
OUT.mkdir(parents=True, exist_ok=True)
URL = "http://localhost:6001/iframe.html?viewMode=story&id=components-game--ways-counter"


def main() -> None:
    errs: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1422, "height": 800})
        page.on("pageerror", lambda e: errs.append(f"PE:{e}"))
        page.on(
            "console",
            lambda m: errs.append(f"{m.type}:{m.text}")
            if m.type in ("error", "warning")
            else None,
        )
        page.goto(URL, wait_until="domcontentloaded", timeout=120000)
        for _ in range(60):
            time.sleep(1)
            disabled = page.evaluate(
                """() => {
                const b = [...document.querySelectorAll('button')]
                  .find(x => /action/i.test(x.textContent || ''));
                return b ? b.disabled : true;
            }"""
            )
            if disabled is False:
                page.locator("button.action").first.click()
                time.sleep(10)
                break
        page.screenshot(path=str(OUT / "morph-ways-full.png"))
        print("ERRS", len(errs), flush=True)
        for e in errs:
            if any(k in e.lower() for k in ("morph", "frame", "error", "pe:", "failed")):
                print(e[:500], flush=True)
        for e in errs[:12]:
            print(e[:300], flush=True)
        browser.close()
    os._exit(0)


if __name__ == "__main__":
    main()
