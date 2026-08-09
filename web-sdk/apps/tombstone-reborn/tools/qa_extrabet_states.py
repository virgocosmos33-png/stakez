"""Capture the idle HUD with EXTRA BET OFF vs ON across all four layouts.

Uses the dedicated QA/ExtraBet stories (off | on) which just set
stateBet.activeBetModeKey, so the HUD renders idle in either state — no spin.

Run: python tools/qa_extrabet_states.py [off|on|both]  (Storybook on :6001)

Note: on Windows this Playwright script reliably writes every PNG but may hang
on browser teardown. The files are on disk once the [shot] lines print.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY_ID = {"off": "components-game--extra-bet-off", "on": "components-game--extra-bet-on"}
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

# heaviest layout (tablet) first while the browser is freshest
VIEWPORTS = [
    ("tablet", 860, 820),
    ("desktop", 1600, 900),
    ("landscape", 900, 440),
    ("portrait", 560, 980),
]

# tight crop of the BET pill / EXTRA BET tab per layout (unscaled CSS px)
def pill_clip(layout: str, w: int, h: int) -> dict:
    if layout in ("desktop", "landscape"):
        return {"x": 0, "y": max(0, h - 210), "width": min(w, 460), "height": min(h, 210)}
    # portrait / tablet: pill sits bottom-centre-left
    return {"x": 0, "y": max(0, h - 320), "width": w, "height": min(h, 320)}


def wait_action_ready(page, timeout_s: int = 220) -> bool:
    end = time.time() + timeout_s
    while time.time() < end:
        try:
            btn = page.locator("button.action").first
            if btn.is_enabled(timeout=1000):
                return True
        except Exception:  # noqa: BLE001
            pass
        time.sleep(1.5)
    return False


def run_action(page) -> bool:
    """Click Action and confirm the story action actually ran (message flips to
    'resolved'). The first click on a freshly-booted app sometimes no-ops, so
    retry (forced) until the resolved banner shows."""
    time.sleep(1.5)
    btn = page.locator("button.action").first
    for _ in range(10):
        try:
            btn.click(timeout=5000, force=True)
        except Exception:  # noqa: BLE001
            pass
        try:
            page.get_by_text("resolved", exact=False).first.wait_for(timeout=5000)
            return True
        except Exception:  # noqa: BLE001
            time.sleep(1.0)
    return False


def boot(page, url: str) -> bool:
    """Load the story; if the app never reaches the Action-ready state on the
    first (cold) attempt, reload once — the second load is cache-warm and boots
    much faster on slow Windows machines."""
    page.goto(url, wait_until="commit", timeout=120000)
    if wait_action_ready(page, 200):
        return True
    try:
        page.reload(wait_until="commit", timeout=120000)
    except Exception:  # noqa: BLE001
        pass
    return wait_action_ready(page, 200)


def capture(page, url: str, state: str, layout: str, w: int, h: int) -> None:
    ready = boot(page, url)
    resolved = run_action(page) if ready else False
    # let the toggle settle + pixi repaint
    time.sleep(3)
    full = OUT / f"extrabet-{state}-{layout}.png"
    page.screenshot(path=str(full), clip={"x": 0, "y": 0, "width": w, "height": h})
    print(f"[shot] {full.name} (ready={ready} resolved={resolved})", flush=True)
    crop = OUT / f"extrabet-{state}-{layout}-pill.png"
    page.screenshot(path=str(crop), clip=pill_clip(layout, w, h))
    print(f"[shot] {crop.name}", flush=True)


def main() -> None:
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    states = ["off", "on"] if which == "both" else [which]
    only_layout = sys.argv[2] if len(sys.argv) > 2 else None
    viewports = [v for v in VIEWPORTS if (only_layout is None or v[0] == only_layout)]

    with sync_playwright() as p:
        # one warm browser for the whole run (cache persists across contexts)
        browser = p.chromium.launch(args=["--disable-dev-shm-usage"])
        for state in states:
            for layout, w, h in viewports:
                ctx = browser.new_context(
                    viewport={"width": w, "height": h}, device_scale_factor=2
                )
                page = ctx.new_page()
                url = f"{BASE}{STORY_ID[state]}&t={int(time.time())}"
                capture(page, url, state, layout, w, h)
                ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
