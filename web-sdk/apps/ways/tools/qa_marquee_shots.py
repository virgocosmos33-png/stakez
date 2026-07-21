"""Capture the base-game info marquee (two frames a second apart to prove it
scrolls) and the free-spins state (marquee gone, FREE SPINS counter shown).

Run: python tools/qa_marquee_shots.py
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)


def run_story(page, story):
    """Load a story and run its action once the board is ready. Returns
    (pageerrors, console_errors)."""
    perr, cerr = [], []
    page.on("pageerror", lambda e: perr.append(str(e)))
    page.on("console", lambda m: cerr.append(f"{m.type}: {m.text}") if m.type == "error" else None)
    page.goto(BASE + story, wait_until="commit", timeout=120000)

    # the green Action button is disabled until the game has loaded and the
    # board is rendered ("Click action to start"); wait for it to enable
    deadline = time.time() + 110
    while time.time() < deadline:
        btn = page.query_selector("button.action")
        if btn and btn.is_enabled():
            break
        time.sleep(1)
    else:
        print(f"[warn] {story}: Action button never enabled")

    # run the story action (sets gameType / counters). retry a couple of times.
    for _ in range(3):
        try:
            page.click("button.action", timeout=8000)
            break
        except Exception:
            time.sleep(1)
    # wait until the action resolves
    d2 = time.time() + 12
    while time.time() < d2:
        if "Action is resolved" in page.evaluate("document.body.innerText"):
            break
        time.sleep(0.5)
    return perr, cerr


with sync_playwright() as play:
    browser = play.chromium.launch()

    # --- base game: scrolling info marquee in the centre well ---
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    perr1, cerr1 = run_story(page, "components-game--scene-base")
    time.sleep(2.5)  # settle into idle
    page.screenshot(path=str(OUT / "marquee_base_1.png"))
    print("[shot] marquee_base_1.png", flush=True)
    page.screenshot(path=str(OUT / "marquee_base.png"))
    time.sleep(1.0)
    page.screenshot(path=str(OUT / "marquee_base_2.png"))
    print("[shot] marquee_base_2.png", flush=True)
    page.close()

    # --- free spins: counter shows, marquee hidden ---
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    perr2, cerr2 = run_story(page, "components-game--scene-bonus")
    time.sleep(2.0)
    page.screenshot(path=str(OUT / "marquee_freespins.png"))
    print("[shot] marquee_freespins.png", flush=True)
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
