"""Capture the redesigned MONO/ROUNDED HUD across all layouts + EXTRA BET off/on.

Run: python tools/qa_hud_shots.py [tag] [viewport] [story]
  tag       output filename tag (default "new")
  viewport  limit to one of desktop|landscape|portrait|tablet (optional)
  story     limit to one of off|on|prespin (optional)

Storybook must be up on :6001. Windows quirk: Playwright reliably WRITES the
PNGs but may hang on teardown — the files exist once each "[shot] ..." prints;
we os._exit(0) at the end to avoid the hang.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

VIEWPORTS = [
    ("desktop", 1600, 900),
    ("landscape", 900, 440),
    ("portrait", 560, 980),
    ("tablet", 860, 820),
]
STORIES = [
    ("off", "components-game--extra-bet-off"),
    ("on", "components-game--extra-bet-on"),
    ("prespin", "components-game--pre-spin"),
]


def click_action(page, w: int, h: int) -> None:
    # the green "Action" button stays disabled until the app has loaded; poll for
    # it to become enabled, then click to run the story action (funds balance /
    # sets the ante bet mode).
    btn = page.locator("button.action")
    for _ in range(130):
        try:
            if btn.count() and btn.first.is_enabled():
                btn.first.click(timeout=2000)
                return True
        except Exception:  # noqa: BLE001
            pass
        time.sleep(1)
    return False


def main() -> None:
    tag = sys.argv[1] if len(sys.argv) > 1 else "new"
    vfilter = sys.argv[2] if len(sys.argv) > 2 else None
    sfilter = sys.argv[3] if len(sys.argv) > 3 else None

    viewports = [v for v in VIEWPORTS if not vfilter or v[0] == vfilter]
    stories = [s for s in STORIES if not sfilter or s[0] == sfilter]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        first = True
        for sname, sid in stories:
            for vname, w, h in viewports:
                ctx = browser.new_context(
                    viewport={"width": w, "height": h}, device_scale_factor=2
                )
                page = ctx.new_page()
                page.goto(f"{BASE}{sid}", wait_until="commit", timeout=120000)
                time.sleep(4)
                click_action(page, w, h)  # polls until the button is enabled
                time.sleep(10)  # let the action apply + reels settle
                out = OUT / f"hud-{tag}-{sname}-{vname}.png"
                page.screenshot(
                    path=str(out), clip={"x": 0, "y": 0, "width": w, "height": h}
                )
                print(f"[shot] {out}", flush=True)
                ctx.close()
                first = False
        print("[done]", flush=True)
    os._exit(0)


if __name__ == "__main__":
    main()
