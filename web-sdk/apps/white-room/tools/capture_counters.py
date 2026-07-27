"""Screenshot the WAYS / FREE SPINS counter stories for a visual panel-fit QA.

Storybook must be running on :6001 (npm run storybook). Captures both the
typical and worst-case counter stories at desktop size.

Run: python tools/capture_counters.py
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

import sys

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORIES = sys.argv[1:] or ["components-game--ways-counter", "components-game--counters-max"]
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "counters"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1600, 900


def run_action(page) -> None:
    # StoryGameTemplate renders <button class="action">Action</button>; it is
    # disabled until stateApp.loaded, then the message reads "Click action to
    # start". Wait for it to enable, click, and confirm the action ran.
    btn = page.locator("button.action")
    for _ in range(40):
        try:
            if btn.is_enabled():
                break
        except Exception:  # noqa: BLE001
            pass
        time.sleep(1)
    for _ in range(6):
        try:
            # call the DOM click() directly so the Svelte onclick fires even if
            # the pixi canvas sits over the button
            btn.evaluate("el => el.click()")
        except Exception:  # noqa: BLE001
            try:
                btn.dispatch_event("click")
            except Exception:  # noqa: BLE001
                pass
        time.sleep(1.5)
        msg = ""
        try:
            msg = page.locator("span.message").inner_text(timeout=1500)
        except Exception:  # noqa: BLE001
            pass
        safe = msg.encode("ascii", "replace").decode("ascii")
        print(f"   action msg: {safe!r}", flush=True)
        if "resolved" in msg or "Running" in msg:
            return


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        first = True
        for story in STORIES:
            ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=2)
            page = ctx.new_page()
            page.goto(f"{BASE}{story}", wait_until="commit", timeout=120000)
            time.sleep(28)
            run_action(page)
            time.sleep(7)
            out = OUT / f"{story}.png"
            page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": W, "height": H})
            print(f"[shot] {out.name}", flush=True)
            ctx.close()
            first = False
        browser.close()


if __name__ == "__main__":
    main()
