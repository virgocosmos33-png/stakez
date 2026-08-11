"""Headless capture of the win-celebration showcase stories.

The showcase stories gate behind Storybook's green "Action" button, so a plain
`chrome --screenshot` only ever captures the idle board. This drives Chrome over
the DevTools Protocol: navigate, click Action, then burst-capture while the
celebration plays so the peak of each tier is actually on film.

Usage:
  python tools/shoot_win_celebration_qa.py [--port 6009] [--story small_bonus_win]

Output: qa-shots/win/<story>/f##.png plus a contact sheet per story.
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
OUT = APP / "qa-shots" / "win"

STORIES = {
	"small_bonus_win": "mode-bonus-book--small-bonus-win",
	"super_bonus_win": "mode-bonus-book--super-bonus-win",
	"max_win": "mode-bonus-book--max-win",
}

CHROME_CANDIDATES = [
	r"C:\Program Files\Google\Chrome\Application\chrome.exe",
	r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
	os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
	r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
	r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

VIEWPORT = (1280, 800)
# A showcase book plays its whole round before the total-win takeover, which can
# take minutes and can't be predicted from the clock. The takeover is always the
# LAST thing before the action resolves, so film into a rolling buffer and keep
# the tail once Storybook reports the action resolved.
FRAME_INTERVAL = 1.0
RING_SIZE = 46
BOOK_BUDGET = 480.0
CLICK_SETTLE = 1.5
# NB: the *running* message also says "resolved" ("Make sure action is resolved
# eventually"), so match only the completion string.
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
	def __init__(self) -> None:
		self.port = free_port()
		self.profile = APP / "qa-shots" / f"_chrome_profile_{self.port}"
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
		self.send("Page.enable")
		self.send("Runtime.enable")

	def _connect(self) -> websocket.WebSocket:
		deadline = time.time() + 45
		last_error: Exception | None = None
		while time.time() < deadline:
			try:
				with urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json", timeout=2) as res:
					targets = json.load(res)
				page = next(t for t in targets if t.get("type") == "page")
				# Chrome 111+ rejects DevTools handshakes that carry an Origin header.
				return websocket.create_connection(
					page["webSocketDebuggerUrl"], timeout=60, max_size=None, suppress_origin=True
				)
			except Exception as error:
				last_error = error
				time.sleep(0.6)
		raise SystemExit(f"could not attach to Chrome DevTools: {last_error!r}")

	def send(self, method: str, **params) -> dict:
		self.message_id += 1
		message_id = self.message_id
		self.socket.send(json.dumps({"id": message_id, "method": method, "params": params}))
		while True:
			frame = json.loads(self.socket.recv())
			if frame.get("id") == message_id:
				if "error" in frame:
					raise RuntimeError(f"{method}: {frame['error']}")
				return frame.get("result", {})

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


def shoot(chrome: Chrome, name: str, story_id: str, port: int) -> None:
	story_dir = OUT / name
	shutil.rmtree(story_dir, ignore_errors=True)
	story_dir.mkdir(parents=True, exist_ok=True)
	url = f"http://localhost:{port}/iframe.html?id={story_id}&viewMode=story"
	print(f"[{name}] {url}")

	chrome.evaluate("window.__qaErrors = []")
	chrome.send("Page.navigate", url=url)
	time.sleep(3.0)
	# capture console errors for the report
	chrome.evaluate(
		"(() => { if (window.__qaHooked) return true; window.__qaErrors = [];"
		" const base = console.error;"
		" console.error = (...a) => { window.__qaErrors.push(a.map(String).join(' ')); base(...a); };"
		" window.addEventListener('error', (e) => window.__qaErrors.push('onerror: ' + e.message));"
		" window.__qaHooked = true; return true; })()"
	)

	action_ready = (
		"!!document.querySelector('button.action')"
		" && !document.querySelector('button.action').disabled"
	)
	# parallel agents share this Storybook, so a cold compile can take a while;
	# one reload covers the case where the first navigation lost the race
	if not wait_for(chrome, action_ready, 180, "Action button enabled"):
		print("  reloading once")
		chrome.send("Page.navigate", url=url)
		time.sleep(4.0)
		if not wait_for(chrome, action_ready, 180, "Action button enabled (retry)"):
			chrome.screenshot(story_dir / "_not_ready.png")
			return
	chrome.evaluate("document.querySelector('button.action').click(); true")
	time.sleep(CLICK_SETTLE)
	print(f"  clicked Action; filming a {RING_SIZE}s rolling buffer until the book resolves")

	ring = story_dir / "_ring"
	ring.mkdir(exist_ok=True)
	started = time.time()
	captured = 0
	while time.time() - started < BOOK_BUDGET:
		chrome.screenshot(ring / f"r{captured % RING_SIZE:02d}.png")
		captured += 1
		if chrome.evaluate(RESOLVED_EXPRESSION) is True:
			print(f"  book resolved at +{time.time() - started:.0f}s after {captured} frames")
			break
		time.sleep(FRAME_INTERVAL)
	else:
		print(f"  ! book never resolved within {BOOK_BUDGET:.0f}s; keeping the tail anyway")

	# unwrap the ring into chronological order, oldest kept frame first
	keep = min(captured, RING_SIZE)
	frames: list[Path] = []
	for offset in range(keep):
		index = (captured - keep + offset) % RING_SIZE
		source = ring / f"r{index:02d}.png"
		dest = story_dir / f"f{offset:02d}.png"
		source.replace(dest)
		frames.append(dest)
	shutil.rmtree(ring, ignore_errors=True)

	errors = chrome.evaluate("JSON.stringify((window.__qaErrors || []).slice(0, 20))")
	(story_dir / "_console.json").write_text(errors or "[]", encoding="utf-8")
	parsed = json.loads(errors or "[]")
	print(f"  console errors: {len(parsed)}")
	for line in parsed[:6]:
		print(f"    - {line[:190]}")
	contact_sheet(story_dir, frames)


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--port", type=int, default=6009)
	parser.add_argument("--story", action="append", choices=sorted(STORIES), default=None)
	args = parser.parse_args()
	targets = args.story or list(STORIES)

	OUT.mkdir(parents=True, exist_ok=True)
	chrome = Chrome()
	try:
		for name in targets:
			shoot(chrome, name, STORIES[name], args.port)
	finally:
		chrome.close()


if __name__ == "__main__":
	sys.exit(main())
