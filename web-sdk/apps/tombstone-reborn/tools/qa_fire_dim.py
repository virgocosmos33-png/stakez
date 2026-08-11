"""Verify linked-cell fire recedes when a feature burst raises over the board.
Drives COMPONENTS/FeatureFx/fire dims under burst: fire lights on reels 1-2,
then a bounty burst fires on reel 4 at ~900ms. Grabs a frame BEFORE the burst
and one DURING it, and reports the mean brightness of the fire region (reels
1-2) for each. The fire uses additive orange, so a real dim shows a clear drop.

Run: python tools/qa_fire_dim.py
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageStat

PORT = sys.argv[1] if len(sys.argv) > 1 else "6009"
STORY = "components-featurefx--fire-dims-under-burst"
BASE = f"http://localhost:{PORT}/iframe.html?viewMode=story&id={STORY}"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "firedim"
OUT.mkdir(parents=True, exist_ok=True)
# fire region over reels 1-2 in a 1200x760 viewport (left-of-centre board area)
CROP = (330, 150, 560, 500)


def fire_brightness(path: Path) -> float:
    im = Image.open(path).convert("RGB").crop(CROP)
    # weight toward the fire's warm channels (R+G) minus blue to isolate flame
    r, g, b = ImageStat.Stat(im).mean
    return round((r + g) / 2 - b * 0.5, 1)


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader"])
        ctx = browser.new_context(viewport={"width": 1200, "height": 760}, device_scale_factor=1)
        page = ctx.new_page()
        msgs = []
        page.on("console", lambda m: msgs.append(f"{m.type}: {m.text}"))
        page.on("pageerror", lambda e: msgs.append(f"PAGEERROR: {e}"))
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
        # BEFORE burst: fire fully caught, burst raises at ~1100ms
        while time.time() - t0 < 1.0:
            time.sleep(0.02)
        before = OUT / "fire-before.png"
        page.screenshot(path=str(before))
        # DURING burst: dim applied (~260ms after the 1100ms burst)
        while time.time() - t0 < 1.9:
            time.sleep(0.02)
        after = OUT / "fire-during.png"
        page.screenshot(path=str(after))
        b0 = fire_brightness(before)
        b1 = fire_brightness(after)
        print(f"[fire] before burst = {b0}   during burst = {b1}", flush=True)
        if b0 > 0:
            print(f"[fire] fire region brightness retained = {round(b1 / b0 * 100)}%", flush=True)
        print(f"[shot] {before}\n[shot] {after}", flush=True)
        # surface any asset-load / runtime issues that would suppress the fire
        interesting = [m for m in msgs if any(k in m.lower() for k in ("error", "warn", "fail", "cell_fire", "cellfire", "404"))]
        for m in interesting[:25]:
            print(f"[console] {m}", flush=True)
        browser.close()
        print("[done]", flush=True)


if __name__ == "__main__":
    main()
