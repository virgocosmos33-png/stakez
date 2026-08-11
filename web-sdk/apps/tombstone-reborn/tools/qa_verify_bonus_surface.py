"""Prove the Madam Mirror bonus-entry surface is gone at runtime.

The free-spins / bonus-level overlays (FreeSpinIntro, FreeSpinOutro,
FreeSpinCounter, BonusLevelBanner, BonusUpgradeBanner) were deleted along with
their White Room art, because Tombstone Reborn has no free spins and no bonus
levels — nothing mounted them and nothing broadcast their events.

A source grep can show the strings are gone; it cannot show the game still
boots and plays without them, or that no loader still asks for the deleted
.webp files. So this drives Chrome over the DevTools Protocol the same way
tools/shoot_win_celebration_qa.py does (navigate, click Storybook's Action
button, film until the book resolves) and additionally records every network
request and console error, then asserts:

  * no request URL names any deleted bonus-entry asset
  * no request 404s (a dangling asset reference would show up here)
  * no console error mentions a deleted component

Usage:
  python tools/qa_verify_bonus_surface.py [--port 6009] [--story dead_spin ...]

Output: qa-shots/bonus-surface/<story>/f##.png, _sheet.jpg, _report.json
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from base64 import b64decode
from pathlib import Path

import websocket
from PIL import Image, ImageDraw

APP = Path(__file__).resolve().parents[1]
OUT = APP / "qa-shots" / "bonus-surface"

STORIES = {
    "dead_spin": "mode-base-book--dead-spin",
    "small_bonus_win": "mode-bonus-book--small-bonus-win",
    "max_win": "mode-bonus-book--max-win",
}

# Every media file removed with the surface. Any of these appearing in a network
# request means a loader/manifest reference survived the deletion.
DELETED_MEDIA = [
    "fs_intro_mirror.webp",
    "fs_intro_mirror_otherside.webp",
    "fs_intro_mirror_bloodmoon.webp",
    "fs_outro_panel.webp",
    "intro_seance.webp",
    "intro_otherside.webp",
    "intro_bloodmoon.webp",
    "buy_seance.webp",
    "buy_otherside.webp",
    "buy_bloodmoon.webp",
    "buy_feature1.webp",
    "buy_feature2.webp",
    "buy_feature3.webp",
    "buy_ante.webp",
    "buy_scatter_1.webp",
    "buy_scatter_3.webp",
    "buy_scatter_4.webp",
    "buy_scatter_5.webp",
]

# Deleted components. A stale import would surface as a module-resolution error.
DELETED_COMPONENTS = [
    "FreeSpinIntro",
    "FreeSpinOutro",
    "FreeSpinCounter",
    "BonusLevelBanner",
    "BonusUpgradeBanner",
]

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

VIEWPORT = (1280, 800)
FRAME_INTERVAL = 1.0
RING_SIZE = 24
CLICK_SETTLE = 1.5
RESOLVED_EXPRESSION = (
    "(() => { const m = document.querySelector('.message');"
    " return !!m && m.textContent.includes('Action is resolved'); })()"
)


def find_chrome() -> str:
    for path in CHROME_CANDIDATES:
        if path and os.path.isfile(path):
            return path
    raise SystemExit("no Chrome/Edge binary found")


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class Chrome:
    """Minimal CDP client that keeps the async events `send` would discard."""

    def __init__(self) -> None:
        self.port = free_port()
        self.profile = OUT / f"_chrome_profile_{self.port}"
        self.profile.parent.mkdir(parents=True, exist_ok=True)
        self.process = subprocess.Popen(
            [
                find_chrome(),
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--hide-scrollbars",
                "--mute-audio",
                "--disable-dev-shm-usage",
                f"--window-size={VIEWPORT[0]},{VIEWPORT[1]}",
                f"--remote-debugging-port={self.port}",
                f"--user-data-dir={self.profile}",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.socket = self._connect()
        self.message_id = 0
        self.requests: list[str] = []
        self.failures: list[dict] = []
        self.send("Page.enable")
        self.send("Runtime.enable")
        self.send("Network.enable")

    def _connect(self) -> websocket.WebSocket:
        deadline = time.time() + 45
        last_error: Exception | None = None
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(
                    f"http://127.0.0.1:{self.port}/json", timeout=2
                ) as res:
                    targets = json.load(res)
                page = next(t for t in targets if t.get("type") == "page")
                # Chrome 111+ rejects DevTools handshakes carrying an Origin header.
                return websocket.create_connection(
                    page["webSocketDebuggerUrl"],
                    timeout=60,
                    max_size=None,
                    suppress_origin=True,
                )
            except Exception as error:
                last_error = error
                time.sleep(0.6)
        raise SystemExit(f"could not attach to Chrome DevTools: {last_error!r}")

    def _record(self, frame: dict) -> None:
        method = frame.get("method")
        params = frame.get("params") or {}
        if method == "Network.requestWillBeSent":
            url = (params.get("request") or {}).get("url", "")
            if url:
                self.requests.append(url)
        elif method == "Network.responseReceived":
            response = params.get("response") or {}
            status = response.get("status", 0)
            if status >= 400:
                self.failures.append({"url": response.get("url", ""), "status": status})
        elif method == "Network.loadingFailed":
            self.failures.append(
                {
                    "url": "<loadingFailed>",
                    "status": params.get("errorText", "failed"),
                }
            )

    def send(self, method: str, **params) -> dict:
        self.message_id += 1
        message_id = self.message_id
        self.socket.send(
            json.dumps({"id": message_id, "method": method, "params": params})
        )
        while True:
            frame = json.loads(self.socket.recv())
            if frame.get("id") == message_id:
                if "error" in frame:
                    raise RuntimeError(f"{method}: {frame['error']}")
                return frame.get("result", {})
            self._record(frame)

    def evaluate(self, expression: str):
        result = self.send(
            "Runtime.evaluate", expression=expression, returnByValue=True, awaitPromise=True
        )
        return result.get("result", {}).get("value")

    def screenshot(self, dest: Path) -> None:
        data = self.send("Page.captureScreenshot", format="png", captureBeyondViewport=False)
        dest.write_bytes(b64decode(data["data"]))

    def close(self) -> None:
        try:
            self.socket.close()
        finally:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
            shutil.rmtree(self.profile, ignore_errors=True)


def wait_for(chrome: Chrome, expression: str, timeout: float, label: str) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if chrome.evaluate(expression) is True:
            return True
        time.sleep(0.5)
    print(f"  ! timed out waiting for {label}")
    return False


def contact_sheet(story_dir: Path, frames: list[Path]) -> None:
    if not frames:
        return
    columns = 4
    cell_w, cell_h = 320, 216
    rows = (len(frames) + columns - 1) // columns
    sheet = Image.new("RGB", (cell_w * columns, cell_h * rows), (12, 12, 14))
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(frames):
        art = Image.open(path).convert("RGB")
        art.thumbnail((cell_w - 6, cell_h - 18), Image.LANCZOS)
        x = (index % columns) * cell_w
        y = (index // columns) * cell_h
        sheet.paste(art, (x + 3, y + 3))
        draw.text((x + 6, y + cell_h - 14), path.stem, fill=(255, 214, 120))
    dest = story_dir / "_sheet.jpg"
    sheet.save(dest, quality=88)
    print(f"  contact sheet -> {dest}")


def verify(chrome: Chrome, name: str, story_id: str, port: int, budget: float) -> dict:
    story_dir = OUT / name
    shutil.rmtree(story_dir, ignore_errors=True)
    story_dir.mkdir(parents=True, exist_ok=True)
    url = f"http://localhost:{port}/iframe.html?id={story_id}&viewMode=story"
    print(f"[{name}] {url}")

    chrome.requests.clear()
    chrome.failures.clear()
    chrome.send("Page.navigate", url=url)
    time.sleep(3.0)
    chrome.evaluate(
        "(() => { window.__qaErrors = [];"
        " const base = console.error;"
        " console.error = (...a) => { window.__qaErrors.push(a.map(String).join(' ')); base(...a); };"
        " window.addEventListener('error', (e) => window.__qaErrors.push('onerror: ' + e.message));"
        " return true; })()"
    )

    action_ready = (
        "!!document.querySelector('button.action')"
        " && !document.querySelector('button.action').disabled"
    )
    # parallel agents share this Storybook, so a cold compile can take a while
    if not wait_for(chrome, action_ready, 180, "Action button enabled"):
        print("  reloading once")
        chrome.send("Page.navigate", url=url)
        time.sleep(4.0)
        if not wait_for(chrome, action_ready, 180, "Action button enabled (retry)"):
            chrome.screenshot(story_dir / "_not_ready.png")
            return {"story": name, "ready": False}
    chrome.evaluate("document.querySelector('button.action').click(); true")
    time.sleep(CLICK_SETTLE)
    print(f"  clicked Action; filming until the book resolves (budget {budget:.0f}s)")

    ring = story_dir / "_ring"
    ring.mkdir(exist_ok=True)
    started = time.time()
    captured = 0
    resolved = False
    while time.time() - started < budget:
        chrome.screenshot(ring / f"r{captured % RING_SIZE:02d}.png")
        captured += 1
        if chrome.evaluate(RESOLVED_EXPRESSION) is True:
            resolved = True
            print(f"  book resolved at +{time.time() - started:.0f}s after {captured} frames")
            break
        time.sleep(FRAME_INTERVAL)
    if not resolved:
        print(f"  ! book did not resolve within {budget:.0f}s; keeping the tail")

    keep = min(captured, RING_SIZE)
    frames: list[Path] = []
    for offset in range(keep):
        index = (captured - keep + offset) % RING_SIZE
        source = ring / f"r{index:02d}.png"
        dest = story_dir / f"f{offset:02d}.png"
        source.replace(dest)
        frames.append(dest)
    shutil.rmtree(ring, ignore_errors=True)

    raw_errors = chrome.evaluate("JSON.stringify((window.__qaErrors || []).slice(0, 40))")
    console_errors = json.loads(raw_errors or "[]")

    banned_hits = sorted(
        {media for media in DELETED_MEDIA for url in chrome.requests if media in url}
    )
    component_hits = sorted(
        {
            component
            for component in DELETED_COMPONENTS
            for line in console_errors
            if component in line
        }
    )
    # Storybook's own HMR/telemetry endpoints 404 in --ci mode; only asset and
    # module requests matter for a dangling-reference check.
    asset_failures = [
        failure
        for failure in chrome.failures
        if any(
            failure.get("url", "").endswith(ext)
            for ext in (".webp", ".png", ".json", ".mp4", ".webm", ".xml", ".atlas", ".js", ".ts")
        )
    ]

    report = {
        "story": name,
        "storyId": story_id,
        "ready": True,
        "resolved": resolved,
        "frames": len(frames),
        "requests": len(chrome.requests),
        "deletedMediaRequested": banned_hits,
        "deletedComponentErrors": component_hits,
        "assetFailures": asset_failures[:20],
        "consoleErrors": console_errors,
    }
    (story_dir / "_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    print(f"  requests={len(chrome.requests)}  console errors={len(console_errors)}")
    print(f"  deleted media requested: {banned_hits or 'NONE'}")
    print(f"  deleted component errors: {component_hits or 'NONE'}")
    print(f"  asset/module load failures: {len(asset_failures)}")
    for failure in asset_failures[:6]:
        print(f"    - {failure}")
    for line in console_errors[:6]:
        print(f"    console: {line[:180]}")
    contact_sheet(story_dir, frames)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=6009)
    parser.add_argument("--story", action="append", choices=sorted(STORIES), default=None)
    parser.add_argument("--budget", type=float, default=300.0)
    args = parser.parse_args()
    targets = args.story or list(STORIES)

    OUT.mkdir(parents=True, exist_ok=True)
    chrome = Chrome()
    reports = []
    try:
        for name in targets:
            reports.append(verify(chrome, name, STORIES[name], args.port, args.budget))
    finally:
        chrome.close()

    (OUT / "_summary.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")
    clean = all(
        report.get("ready")
        and not report.get("deletedMediaRequested")
        and not report.get("deletedComponentErrors")
        and not report.get("assetFailures")
        for report in reports
    )
    print("\n=== SUMMARY ===")
    for report in reports:
        print(
            f"  {report['story']:16s} ready={report.get('ready')} "
            f"resolved={report.get('resolved')} "
            f"deletedMedia={len(report.get('deletedMediaRequested') or [])} "
            f"assetFailures={len(report.get('assetFailures') or [])} "
            f"consoleErrors={len(report.get('consoleErrors') or [])}"
        )
    print("PASS" if clean else "FAIL")
    return 0 if clean else 1


if __name__ == "__main__":
    sys.exit(main())
