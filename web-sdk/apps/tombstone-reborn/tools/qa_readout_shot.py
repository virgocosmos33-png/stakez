"""Screenshot the vertical rail so the WAYS/WIN ornate plaques can be eyeballed.
Run: python tools/qa_readout_shot.py [port]
"""
from __future__ import annotations
import sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

PORT = sys.argv[1] if len(sys.argv) > 1 else "6009"
STORY = "mode-base-book--dead-spin"
BASE = f"http://localhost:{PORT}/iframe.html?viewMode=story&id={STORY}"
OUT = Path(__file__).resolve().parents[1] / "qa-shots"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader"])
        ctx = browser.new_context(viewport={"width": 1200, "height": 760}, device_scale_factor=1)
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.locator("canvas").first.wait_for(state="visible", timeout=90000)
        btn = page.locator("button.action")
        btn.wait_for(state="visible", timeout=60000)
        for _ in range(360):
            if btn.is_enabled():
                break
            time.sleep(1)
        time.sleep(3)
        full = OUT / "readout_ingame_full.png"
        page.screenshot(path=str(full))
        # crop the left rail (WAYS top / WIN bottom)
        im = Image.open(full).convert("RGB")
        im.crop((120, 70, 340, 560)).save(OUT / "readout_ingame_rail.png")
        print(f"[shot] {full}")
        print(f"[shot] {OUT / 'readout_ingame_rail.png'}")
        browser.close()


if __name__ == "__main__":
    main()
