"""Grab a burst of frames during COMPONENTS/Game/spinCycle so the spin can be
eyeballed: does the board sweep out and refill (spin read), or snap/blank?
Composites them into one contact sheet.

Run: python tools/qa_spin_sequence.py [label]
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

LABEL = sys.argv[1] if len(sys.argv) > 1 else "spin"
PORT = sys.argv[2] if len(sys.argv) > 2 else "6009"
STORY = "components-game--spin-cycle"
BASE = f"http://localhost:{PORT}/iframe.html?viewMode=story&id={STORY}"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "spinseq"
OUT.mkdir(parents=True, exist_ok=True)
N = 14
INTERVAL = 0.06


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
        btn.click(timeout=5000)
        frames = []
        for i in range(N):
            p = OUT / f"{LABEL}-{i:02d}.png"
            page.screenshot(path=str(p))
            frames.append(p)
            time.sleep(INTERVAL)
        # contact sheet: 2 rows x 7
        imgs = [Image.open(f).convert("RGB") for f in frames]
        tw = imgs[0].width // 3
        th = imgs[0].height // 3
        cols = 7
        rows = (len(imgs) + cols - 1) // cols
        sheet = Image.new("RGB", (tw * cols, th * rows), (20, 20, 20))
        for idx, im in enumerate(imgs):
            im2 = im.resize((tw, th))
            sheet.paste(im2, ((idx % cols) * tw, (idx // cols) * th))
        sheet_path = OUT / f"{LABEL}-contact.png"
        sheet.save(sheet_path)
        print(f"[sheet] {sheet_path}", flush=True)
        browser.close()
        print("[done]", flush=True)


if __name__ == "__main__":
    main()
