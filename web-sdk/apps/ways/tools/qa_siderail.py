"""Capture FrameSideRail normal + bonus against the reel frame.

Storybook must be on :6001. Run from web-sdk/apps/ways:
  python tools/qa_siderail.py
"""

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
    ("morphframe-normal-desktop", "components-game--scene-base", 1422, 800),
    ("morphframe-bonus-desktop", "components-game--scene-bonus", 1422, 800),
    ("morphframe-bonus-ways", "components-game--ways-counter", 1422, 800),
]

WAIT_ACTION = """() => {
  const b = [...document.querySelectorAll('button')]
    .find((x) => /action/i.test(x.textContent || ''));
  return b ? b.disabled : true;
}"""


def run_story(page, story: str, settle_s: float = 12) -> bool:
    page.goto(f"{BASE}{story}", wait_until="domcontentloaded", timeout=90000)
    for _ in range(90):
        time.sleep(1)
        try:
            disabled = page.evaluate(WAIT_ACTION)
        except Exception:  # noqa: BLE001
            disabled = True
        if disabled is False:
            page.locator("button.action").first.click()
            time.sleep(settle_s)
            return True
    return False


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for label, story, w, h in JOBS:
            ctx = browser.new_context(
                viewport={"width": w, "height": h}, device_scale_factor=2
            )
            page = ctx.new_page()
            ok = run_story(page, story)
            out = OUT / f"{label}.png"
            page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": w, "height": h})
            print(f"[shot] {out} action={ok}", flush=True)
            im = Image.open(out)
            # deviceScaleFactor=2 → 2x pixels; left rail + left reels
            zoom = im.crop((320, 60, 1500, 1540))
            zoom.save(OUT / f"{label}-zoom.png")
            ctx.close()
        browser.close()
    os._exit(0)


if __name__ == "__main__":
    main()
