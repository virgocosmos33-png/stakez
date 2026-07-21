"""Drive a book story to its CONTINUE gate and screenshot the button.

Run: python tools/qa_shot_continue.py <story-id> <outname>
"""
import sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = sys.argv[1]
OUTNAME = sys.argv[2]
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "lady"
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as play:
    browser = play.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    perr = []
    page.on("pageerror", lambda e: perr.append(str(e)))
    page.goto(BASE + STORY, wait_until="commit", timeout=120000)
    # wait for boot
    for _ in range(30):
        time.sleep(2)
        body = page.evaluate("document.body.innerText")
        if "Initialising" not in body and body.strip() is not None:
            break
    # kick off playback: click canvas center then press space a few times to
    # advance through the presentation until the banner gate parks
    for i in range(14):
        try:
            page.mouse.click(640, 360)
        except Exception:
            pass
        page.keyboard.press("Space")
        time.sleep(1.5)
        page.screenshot(path=str(OUT / f"{OUTNAME}_{i:02d}.png"))
    print("[done] frames written", flush=True)
    print("pageerror:", len(perr))
    for e in sorted(set(perr))[:5]:
        print("  ", e[:200])
    browser.close()
