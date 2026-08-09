"""Capture the base-game HUD at 1280x720 and scan the bottom bar for gold hues.

Verifies the URGENT color revert: every HUD outline/rim/border must read as
dark steel/slate, with ~0 gold pixels (the 0xc99a3f/0xe9c877 brass family).

Run: python tools/qa_no_gold.py
Storybook must be up on :6001.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright
from PIL import Image

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "components-game--pre-spin"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1280, 720


def wait_ready(page) -> str:
    """Click the story Action button once enabled; return the final state text."""
    btn = page.locator("button.action")
    for _ in range(130):
        try:
            if btn.count() and btn.first.is_enabled():
                label = (btn.first.inner_text() or "").strip()
                btn.first.click(timeout=2000)
                return label
        except Exception:  # noqa: BLE001
            pass
        time.sleep(1)
    return "(action never enabled)"


def is_gold(r: int, g: int, b: int) -> bool:
    # brass/gold family: 0xc99a3f (201,154,63) / 0xe9c877 (233,200,119)
    return r > 150 and 120 <= g <= 200 and b < 110


def scan(img: Image.Image, y0: int, y1: int):
    px = img.convert("RGB").load()
    w, h = img.size
    y0 = max(0, y0)
    y1 = min(h, y1)
    count = 0
    samples = []
    for y in range(y0, y1):
        for x in range(w):
            r, g, b = px[x, y]
            if is_gold(r, g, b):
                count += 1
                if len(samples) < 12:
                    samples.append((x, y, r, g, b))
    return count, (w, h), samples


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": W, "height": H}, device_scale_factor=1
        )
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on(
            "console",
            lambda m: errors.append(f"console.{m.type}: {m.text}")
            if m.type == "error"
            else None,
        )
        page.goto(f"{BASE}{STORY}", wait_until="commit", timeout=120000)
        time.sleep(4)
        label = wait_ready(page)
        time.sleep(10)  # let action apply + reels settle

        full = OUT / "no_gold_outlines.png"
        page.screenshot(path=str(full), clip={"x": 0, "y": 0, "width": W, "height": H})
        print(f"[shot] {full}  (action label was: {label!r})", flush=True)

        # tight bottom-bar crop: bottom ~150px of the 720 frame
        img = Image.open(full)
        crop_y0 = H - 160
        crop = img.crop((0, crop_y0, W, H))
        cropp = OUT / "no_gold_crop.png"
        crop.save(cropp)
        print(f"[crop] {cropp}", flush=True)

        count, size, samples = scan(img, crop_y0, H)
        print(f"[scan] image size {size}, HUD bar region y={crop_y0}..{H}", flush=True)
        print(f"[scan] GOLD pixel count on HUD bar = {count}", flush=True)
        if samples:
            print(f"[scan] sample gold pixels (x,y,r,g,b): {samples}", flush=True)

        # also scan full frame for context
        fcount, _, _ = scan(img, 0, H)
        print(f"[scan] GOLD pixel count full frame = {fcount}", flush=True)

        print(f"[errors] page/console errors = {len(errors)}", flush=True)
        for e in errors[:20]:
            print(f"   {e}", flush=True)
        print("[done]", flush=True)
        ctx.close()
    os._exit(0)


if __name__ == "__main__":
    main()
