"""Record the win liner (base game) and the frame fire (free spins) videos.

Outputs land in web-sdk/qa-shots/flames/.
"""

import shutil
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

QA = Path(__file__).resolve().parents[3] / "qa-shots" / "flames"
STORY = "http://localhost:6001/iframe.html?viewMode=story&id="


def record(page_context_args, story_id, seconds, out_name, browser, click_through=False):
    context = browser.new_context(**page_context_args)
    page = context.new_page()
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.goto(STORY + story_id, wait_until="domcontentloaded")
    try:
        page.get_by_role("button", name="Action").click(timeout=30000)
        print(f"{out_name}: action clicked")
    except Exception as error:
        print(f"{out_name}: no action button ({str(error)[:80]})")
    if click_through:
        # dismiss transition/banner CONTINUE prompts so free spins actually run
        elapsed = 0.0
        while elapsed < seconds:
            time.sleep(3)
            elapsed += 3
            try:
                page.mouse.click(512, 300)
            except Exception:
                pass
    else:
        time.sleep(seconds)
    video = page.video
    context.close()
    saved = Path(video.path())
    dest = QA / out_name
    shutil.move(saved, dest)
    print(f"{out_name}: saved, errors={[e[:90] for e in sorted(set(errors))][:4]}")


if __name__ == "__main__":
    QA.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as play:
        browser = play.chromium.launch()
        args = {
            "viewport": {"width": 1024, "height": 600},
            "record_video_dir": str(QA),
            "record_video_size": {"width": 1024, "height": 600},
        }
        record(args, "mode-bonus-book--random", 48, "frame.webm", browser, click_through=True)
        browser.close()
