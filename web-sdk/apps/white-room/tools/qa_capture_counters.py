"""Capture the WAYS + FREE SPINS counters to verify text fits inside the panels.

Loads the dedicated COMPONENTS/<Game> QA stories that broadcast the counter
events directly (deterministic, no long book playback), clicks Action, then
screenshots the viewport. Crops to the counter regions with PIL for a close
read. Run while Storybook is up on :6001.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

try:
    from PIL import Image
except Exception:  # noqa: BLE001
    Image = None

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "counters"
OUT.mkdir(parents=True, exist_ok=True)


def click_action(page) -> bool:
    # .click() auto-waits for the button to become ENABLED (it is disabled until
    # every asset has loaded), so a long timeout guarantees the game is ready.
    try:
        page.get_by_text("Action", exact=True).first.click(timeout=90000)
        return True
    except Exception as e:  # noqa: BLE001
        print(f"  [warn] action click failed: {e}", flush=True)
        return False


def shot(browser, story: str, prefix: str, w: int, h: int) -> list[str]:
    page = browser.new_page(viewport={"width": w, "height": h})
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.goto(BASE + story, wait_until="commit", timeout=120000)
    ok = click_action(page)
    if ok:
        try:
            page.get_by_text("resolved", exact=False).first.wait_for(timeout=30000)
        except Exception:  # noqa: BLE001
            pass
    # dismiss the one-shot "enter the mirror" intro carousel/video (advances on
    # tap) so the gameplay HUD + counters are visible for the screenshot
    for _ in range(4):
        page.mouse.click(w * 0.5, h * 0.5)
        time.sleep(0.6)
    # let the counters + Scenario glass texture + pop animation settle
    time.sleep(6 if ok else 20)
    full = OUT / f"{prefix}-full.png"
    page.screenshot(path=str(full), clip={"x": 0, "y": 0, "width": w, "height": h}, timeout=60000)
    print(f"[shot] {full.name}", flush=True)
    page.close()
    return errors


def crop(prefix: str, boxes: dict[str, tuple[int, int, int, int]]) -> None:
    if Image is None:
        print("[crop] PIL unavailable", flush=True)
        return
    src = OUT / f"{prefix}-full.png"
    if not src.exists():
        return
    img = Image.open(src)
    W, H = img.size
    for name, (l, t, r, b) in boxes.items():
        l, t = max(0, l), max(0, t)
        r, b = min(W, r), min(H, b)
        img.crop((l, t, r, b)).save(OUT / f"{prefix}-{name}.png")
        print(f"[crop] {prefix}-{name}.png ({r - l}x{b - t})", flush=True)


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch()
        e1 = shot(browser, "components-game--ways-counter", "land", 1280, 720)
        e2 = shot(browser, "components-game--ways-counter", "port", 720, 1280)
        e3 = shot(browser, "components-game--counters-max", "landmax", 1280, 720)
        browser.close()

    # landscape 1280x720: board centered ~640; WAYS above board top, FREE SPINS to the left
    for p in ("land", "landmax"):
        crop(p, {
            "ways": (380, 35, 900, 240),
            "freespins": (0, 60, 440, 350),
        })
    # portrait 720x1280: board centered ~360; WAYS above board top
    crop("port", {
        "ways": (110, 230, 610, 470),
    })

    for k, v in {"land": e1, "port": e2, "landmax": e3}.items():
        uniq = sorted(set(v))
        print(f"[{k}] {len(uniq)} unique console error(s)")
        for e in uniq[:8]:
            print("   ", e[:200])


if __name__ == "__main__":
    sys.exit(main())
