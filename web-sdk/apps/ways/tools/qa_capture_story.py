"""Capture a storybook story after a fixed settle wait (for auto-action
component stories that don't show 'Click action to start').

Run: python tools/qa_capture_story.py <story-id> <outname> [wait_s]
"""
import sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = sys.argv[1]
OUTNAME = sys.argv[2]
WAIT = int(sys.argv[3]) if len(sys.argv) > 3 else 45
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "lady"
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as play:
    browser = play.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    perr, cerr = [], []
    page.on("pageerror", lambda e: perr.append(str(e)))
    page.on("console", lambda m: cerr.append(f"{m.type}: {m.text}") if m.type == "error" else None)
    page.goto(BASE + STORY, wait_until="commit", timeout=120000)
    deadline = time.time() + WAIT
    while time.time() < deadline:
        time.sleep(3)
        body = page.evaluate("document.body.innerText")
        if "Initialising" not in body and body.strip():
            break
    time.sleep(4)  # settle mid-idle
    page.screenshot(path=str(OUT / f"{OUTNAME}.png"))
    print(f"[shot] {OUTNAME}.png", flush=True)
    browser.close()

print("pageerror:", len(perr))
for e in sorted(set(perr))[:10]:
    print("  ", e[:250])
print("console.error:", len(cerr))
for e in sorted(set(cerr))[:10]:
    print("  ", e[:250])
