"""Prove the linked-cell fire no longer breathes (scales in/out).

Opens COMPONENTS/FeatureFx/fire-dims-under-burst, lights the fire, then grabs
three frames during the STEADY burn window (before the burst raises at ~1.1s)
and measures the vertical extent (bounding box height) of the warm flame pixels
in the reel-1..2 region. If the fire were still pulsing, that height would
oscillate frame to frame; a held footprint means the pulse is gone. The mean
brightness is also printed to confirm the tongues are still animating (they
should differ slightly) and that the fire still renders.

Run: python tools/qa_fire_nopulse.py [port]
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

PORT = sys.argv[1] if len(sys.argv) > 1 else "6009"
STORY = "components-featurefx--fire-dims-under-burst"
BASE = f"http://localhost:{PORT}/iframe.html?viewMode=story&id={STORY}"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "firedim"
OUT.mkdir(parents=True, exist_ok=True)
CROP = (330, 150, 560, 500)


def flame_metrics(path: Path) -> tuple[int, float]:
    im = Image.open(path).convert("RGB").crop(CROP)
    px = im.load()
    w, h = im.size
    top, bot, warm_sum, warm_n = None, None, 0.0, 0
    for y in range(h):
        row_warm = False
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            warm = (r + g) / 2 - b * 0.5
            if warm > 40:
                row_warm = True
                warm_sum += warm
                warm_n += 1
        if row_warm:
            if top is None:
                top = y
            bot = y
    height = 0 if top is None else (bot - top + 1)
    mean = round(warm_sum / warm_n, 1) if warm_n else 0.0
    return height, mean


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader"])
        ctx = browser.new_context(viewport={"width": 1200, "height": 760}, device_scale_factor=1)
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.locator("canvas").first.wait_for(state="visible", timeout=90000)
        btn = page.locator("button.action")
        btn.wait_for(state="visible", timeout=30000)
        for _ in range(360):
            if btn.is_enabled():
                break
            time.sleep(1)
        t0 = time.time()
        btn.click(timeout=5000)
        results = []
        for i, when in enumerate((0.55, 0.72, 0.9)):
            while time.time() - t0 < when:
                time.sleep(0.01)
            shot = OUT / f"nopulse-{i}.png"
            page.screenshot(path=str(shot))
            hgt, mean = flame_metrics(shot)
            results.append((when, hgt, mean))
            print(f"[frame {i}] t={when}s  flame_height={hgt}px  warm_mean={mean}", flush=True)
        heights = [h for _, h, _ in results]
        spread = max(heights) - min(heights)
        print(f"[footprint] heights={heights}  spread={spread}px", flush=True)
        print("[verdict] " + ("STEADY (no pulse)" if spread <= 4 else "STILL PULSING"), flush=True)
        browser.close()


if __name__ == "__main__":
    main()
