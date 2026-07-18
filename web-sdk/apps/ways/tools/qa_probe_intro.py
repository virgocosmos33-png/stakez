"""Hang-proof check that the (new) intro video is wired and loads in-app.

Pixi builds video textures from DETACHED <video> elements, so querySelectorAll
can't see them and patching createElement breaks the app. Instead we watch the
network: the loader must fetch intro_mirror.mp4 / intro_mirror_portrait.mp4
(206 = streamed video success), and the story must render a <canvas>. Combined
with the IntroVideo component playing on mount, this confirms the swap is intact.
Run:  python tools/qa_probe_intro.py
"""

from __future__ import annotations

import time

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "components-game--component-loading-screen"


def main() -> None:
    responses: list[tuple[str, int]] = []
    errors: list[str] = []
    with sync_playwright() as play:
        browser = play.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        targets = ("intro_mirror.mp4", "intro_mirror_portrait.mp4")
        page.on(
            "response",
            lambda r: responses.append((r.url.split("?")[0].split("/")[-1], r.status))
            if r.url.split("?")[0].split("/")[-1] in targets
            else None,
        )
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(BASE + STORY, wait_until="commit", timeout=120000)

        canvas = False
        for _ in range(40):  # up to ~120s (cold compile + big assets)
            time.sleep(3)
            try:
                canvas = page.evaluate("() => !!document.querySelector('canvas')")
            except Exception:  # noqa: BLE001
                canvas = False
            seen = {u for u, _ in responses}
            if "intro_mirror.mp4" in seen and "intro_mirror_portrait.mp4" in seen:
                break

        print("canvas present:", canvas, flush=True)
        print("intro responses:", responses, flush=True)

        land = any(u == "intro_mirror.mp4" and s in (200, 206) for u, s in responses)
        port = any(u == "intro_mirror_portrait.mp4" and s in (200, 206) for u, s in responses)
        fatal = [e for e in set(errors) if "intro" in e.lower() or "loadedAssets" in e]
        if land and canvas:
            print(f"PASS: intro loads (land={land} port={port}) and story renders a canvas")
        elif any("intro_mirror" in u for u, _ in responses):
            print(f"PARTIAL: intro requested; land={land} port={port} canvas={canvas}")
        else:
            print("FAIL: intro_mirror.mp4 was never requested")
        if fatal:
            print("intro-related console errors:", fatal[:6])
        browser.close()


if __name__ == "__main__":
    main()
