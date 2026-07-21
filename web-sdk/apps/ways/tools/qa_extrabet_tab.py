"""QA: EXTRA BET folder-tab fit via mode-base-book + direct state flip.

Run: python tools/qa_extrabet_tab.py  (Storybook on :6001)
"""

from __future__ import annotations

import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--random"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1600, 900
CLIP = {"x": 0, "y": H - 160, "width": 480, "height": 160}

STATE_SHARED = (
    "/@fs/C:/Users/xheih/OneDrive/Documents/lady%20mirror%20drama%20studios"
    "/web-sdk/packages/state-shared/index.ts"
)


def white_ratio(im: Image.Image, box) -> float:
    crop = im.crop(box)
    n = crop.width * crop.height
    w = sum(1 for (r, g, b) in crop.getdata() if r > 225 and g > 225 and b > 225)
    return w / max(1, n)


def wait_idle_hud(page, timeout_s=180) -> bool:
    tmp = OUT / "_extrabet_idle.png"
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        page.screenshot(path=str(tmp), timeout=60000)
        im = Image.open(tmp).convert("RGB")
        iw, ih = im.size
        br = white_ratio(im, (iw // 2, ih // 2, iw, ih))
        bl = white_ratio(im, (0, int(ih * 0.85), int(iw * 0.25), ih))
        print(f"[extrabet] poll br={br:.3f} bl={bl:.3f}", flush=True)
        if 0.03 < br < 0.30 and 0.010 < bl < 0.12:
            return True
        time.sleep(2)
    return False


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(f"{BASE}{STORY}&t={int(time.time())}", wait_until="commit", timeout=120000)

        idle = wait_idle_hud(page, timeout_s=180)
        print(f"[extrabet] idle_hud={idle}", flush=True)
        if not idle:
            page.screenshot(path=str(OUT / "extrabet-tab-full.png"), timeout=60000)
            print("[extrabet] abort: HUD never painted", flush=True)
            ctx.close()
            browser.close()
            return

        page.screenshot(path=str(OUT / "extrabet-tab-before.png"), clip=CLIP, timeout=60000)

        flipped = page.evaluate(
            """async (url) => {
                const mod = await import(url);
                mod.stateBet.activeBetModeKey = 'ante';
                return {
                    key: mod.stateBet.activeBetModeKey,
                    label: mod.stateBetDerived?.activeBetMode?.()?.text?.betAmountLabel
                        ?? mod.stateBetDerived?.activeBetMode?.()?.text?.betAmountLabel,
                    cost: mod.stateBetDerived?.betCost?.(),
                };
            }""",
            STATE_SHARED,
        )
        print(f"[extrabet] flipped={flipped}", flush=True)
        time.sleep(1.5)

        page.screenshot(path=str(OUT / "extrabet-tab-after.png"), clip=CLIP, timeout=60000)
        page.screenshot(path=str(OUT / "extrabet-tab-full.png"), timeout=60000)
        print("[extrabet] wrote extrabet-tab-before/after/full.png", flush=True)
        ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
