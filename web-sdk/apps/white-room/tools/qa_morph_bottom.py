"""Capture bottom-mounted morph HUD (normal + bonus)."""
from __future__ import annotations

import os
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "scene"
OUT.mkdir(parents=True, exist_ok=True)

JOBS = [
    ("morph-bottom-normal", "components-game--scene-base", 1422, 800),
    ("morph-bottom-bonus", "components-game--ways-counter", 1422, 800),
]


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for label, story, w, h in JOBS:
            ctx = browser.new_context(
                viewport={"width": w, "height": h}, device_scale_factor=2
            )
            page = ctx.new_page()
            page.goto(f"{BASE}{story}", wait_until="domcontentloaded", timeout=90000)
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
            out = OUT / f"{label}.png"
            page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": w, "height": h})
            im = Image.open(out)
            ww, hh = im.size
            # bottom of board + HUD
            im.crop((int(ww * 0.15), int(hh * 0.45), int(ww * 0.85), int(hh * 0.95))).save(
                OUT / f"{label}-zoom.png"
            )
            print(f"[shot] {out}", flush=True)
            ctx.close()
        browser.close()
    os._exit(0)


if __name__ == "__main__":
    main()
