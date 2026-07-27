"""Capture the bottom HUD bar after the font-legibility change.

font_base.png      base game    -> WAYS + info marquee + WIN
font_freespins.png free spins   -> WAYS + FREE SPINS counter + WIN
font_crop.png      tight crop of the bottom bar (legibility check)

Run: python tools/qa_font_shots.py
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)


def run_story(page, story):
    perr, cerr = [], []
    page.on("pageerror", lambda e: perr.append(str(e)))
    page.on("console", lambda m: cerr.append(f"{m.type}: {m.text}") if m.type == "error" else None)
    page.goto(BASE + story, wait_until="commit", timeout=120000)

    # green Action button is disabled until the board has rendered
    deadline = time.time() + 110
    while time.time() < deadline:
        btn = page.query_selector("button.action")
        if btn and btn.is_enabled():
            break
        time.sleep(1)
    else:
        print(f"[warn] {story}: Action button never enabled")

    for _ in range(3):
        try:
            page.click("button.action", timeout=8000)
            break
        except Exception:
            time.sleep(1)
    d2 = time.time() + 12
    while time.time() < d2:
        if "Action is resolved" in page.evaluate("document.body.innerText"):
            break
        time.sleep(0.5)
    return perr, cerr


with sync_playwright() as play:
    browser = play.chromium.launch()

    page = browser.new_page(viewport={"width": 1280, "height": 720})
    perr1, cerr1 = run_story(page, "components-game--scene-base")
    time.sleep(2.5)
    page.screenshot(path=str(OUT / "font_base.png"))
    print("[shot] font_base.png", flush=True)
    # tight crop of the bottom bar (bottom ~180px, centred)
    page.screenshot(path=str(OUT / "font_crop.png"),
                    clip={"x": 240, "y": 540, "width": 800, "height": 170})
    print("[shot] font_crop.png", flush=True)
    page.close()

    page = browser.new_page(viewport={"width": 1280, "height": 720})
    perr2, cerr2 = run_story(page, "components-game--scene-bonus")
    time.sleep(2.0)
    page.screenshot(path=str(OUT / "font_freespins.png"))
    print("[shot] font_freespins.png", flush=True)
    page.close()

    browser.close()

for label, perr, cerr in [("base", perr1, cerr1), ("freespins", perr2, cerr2)]:
    print(f"--- {label} ---")
    print("pageerror:", len(perr))
    for e in sorted(set(perr))[:10]:
        print("  ", e[:250])
    print("console.error:", len(cerr))
    for e in sorted(set(cerr))[:10]:
        print("  ", e[:250])
