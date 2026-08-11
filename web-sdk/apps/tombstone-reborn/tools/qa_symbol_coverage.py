"""Prove every symbol the math can emit resolves to a loaded asset at runtime.

Two halves, both of which have to pass:

STATIC
  Enumerate every symbol name the math can put on the board — the reel strips
  under math-sdk/games/0_3_tombstone_reborn/reels, the paytable in
  game_config.py, the generated showcase books, and the frontend's own initial
  board — then resolve each through SYMBOL_INFO_MAP (src/game/constants.ts) to
  the asset keys its states actually ask Pixi for, and check each of those keys
  is either registered in src/game/assets.ts or is a frame of a `sprites`-type
  atlas registered there. A key that resolves to neither is a guaranteed
  `Sprite: key "..." is not found in the loadedAssets` at runtime.

RUNTIME
  A static check cannot see a sheet that 404s, races the first paint, or throws
  in the loader — the symbols still come out as dark empty boxes. So drive
  Chrome over the DevTools Protocol the same way tools/shoot_win_celebration_qa.py
  and tools/qa_verify_bonus_surface.py do (navigate, click Storybook's Action
  button, film a rolling buffer until the book resolves), with the console hook
  installed BEFORE any page script runs so boot-time misses are caught too, and
  assert no story ever logs a missing asset key. Each story gets its OWN cold
  browser, so the load under test is never served out of a warm HTTP cache.

  Then remount, via Storybook's own forceRemount, and keep watching. Be clear
  about what this does and does not buy: measured against the bug (see below),
  the remount phase does NOT reproduce it, because PIXI.Assets caches by URL, so
  a second load inside the same page resolves in the same microtask burst and
  the preload-only window never lasts long enough for a sprite to observe it. It
  is kept as a cheap regression net for misses that appear only on re-render,
  and for the frames it films — not as this bug's guard.

WHICH HALF ACTUALLY GUARDS THE BUG
  The STATIC half. AssetsLoader publishes `loadedAssets = <preload batch>` and
  renders the game, and only merges the rest in a later effect; Game.svelte
  swaps LoadingScreen for the board the moment stateLayout.showLoadingScreen is
  false. stateLayout is module scope and survives an in-place remount with that
  flag already false, so on any HMR or re-render the board paints against the
  preload batch alone — every non-preloaded symbol is a miss. That is a static,
  checkable invariant (`symbol art must be preloaded`), and removing
  `preload: true` from symbolsStatic makes run_static fail with all twenty
  h1..h5 / l1..l5 keys, blur frames included. A cold load, by contrast, cannot
  fail, because showLoadingScreen only drops once stateApp.loaded is true —
  which is why every runtime story here passed even with the bug present.

Usage:
  python tools/qa_symbol_coverage.py                  # static + runtime, all stories
  python tools/qa_symbol_coverage.py --static-only
  python tools/qa_symbol_coverage.py --story small_bonus_win --story max_win

Output: qa-shots/symbol-coverage/<story>/f##.png, _sheet.jpg, _report.json
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from base64 import b64decode
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
ROOT = APP.parents[2]
MATH = ROOT / "math-sdk" / "games" / "0_3_tombstone_reborn"
OUT = APP / "qa-shots" / "symbol-coverage"

STORIES = {
	"dead_spin": "mode-base-book--dead-spin",
	"special_bar_hit": "mode-base-book--special-bar-hit",
	"tombstone_open": "mode-base-book--tombstone-open",
	"gunsmoke": "mode-base-book--gunsmoke",
	"split_gang": "mode-base-book--split-gang",
	"split_outlaws": "mode-base-book--split-outlaws",
	"dig_up": "mode-base-book--dig-up",
	"small_bonus_win": "mode-bonus-book--small-bonus-win",
	"super_bonus_win": "mode-bonus-book--super-bonus-win",
	"bounty": "mode-bonus-book--bounty",
	"nudge": "mode-bonus-book--nudge",
	"super_split": "mode-bonus-book--super-split",
	"max_win": "mode-bonus-book--max-win",
}

# The symbol states SYMBOL_INFO_MAP declares. Every one of them is reachable:
# `spin` is the falling smear, `land`/`win`/`postWin` the settle beats.
SYMBOL_STATES = ("static", "spin", "land", "win", "postWin", "postWinStatic")

MISSING_KEY_RE = re.compile(r'key "([^"]+)" is not found in the loadedAssets')

CHROME_CANDIDATES = [
	r"C:\Program Files\Google\Chrome\Application\chrome.exe",
	r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
	os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
	r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
	r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

VIEWPORT = (1280, 800)
FRAME_INTERVAL = 1.0
RING_SIZE = 20
CLICK_SETTLE = 1.5
# Frames filmed across the remount window, where the board repaints against a
# loadedAssets that has just been reset to the preload batch.
REMOUNT_FRAMES = 8
# Storybook is shared with other agents, so a cold Vite compile of the story
# chunk can run well past the usual few seconds.
COMPILE_BUDGET = 300.0
RESOLVED_EXPRESSION = (
	"(() => { const m = document.querySelector('.message');"
	" return !!m && m.textContent.includes('Action is resolved'); })()"
)

# Installed before any page script: Sprite.svelte reports a miss through
# console.error, and a miss during boot happens long before a post-navigate hook
# could be attached.
CONSOLE_HOOK = """
(() => {
  window.__qaMissing = {};
  window.__qaErrors = [];
  const base = console.error.bind(console);
  console.error = (...args) => {
    const line = args.map((a) => {
      try { return typeof a === 'string' ? a : JSON.stringify(a); } catch (_) { return String(a); }
    }).join(' ');
    const hit = /key "([^"]+)" is not found in the loadedAssets/.exec(line);
    if (hit) window.__qaMissing[hit[1]] = (window.__qaMissing[hit[1]] || 0) + 1;
    else window.__qaErrors.push(line.slice(0, 400));
    base(...args);
  };
  window.addEventListener('error', (e) => window.__qaErrors.push('onerror: ' + e.message));
  window.addEventListener('unhandledrejection', (e) =>
    window.__qaErrors.push('unhandledrejection: ' + String(e.reason)));
})();
"""


# --------------------------------------------------------------------------
# STATIC
# --------------------------------------------------------------------------


def math_symbol_names() -> dict[str, list[str]]:
	"""Every symbol name the math can emit, by where it came from."""
	sources: dict[str, set[str]] = collections.defaultdict(set)

	reels = MATH / "reels"
	if reels.is_dir():
		for path in sorted(reels.glob("*.csv")):
			with path.open(encoding="utf-8", newline="") as fh:
				for row in csv.reader(fh):
					for cell in row:
						cell = cell.strip()
						if cell:
							sources[f"reels/{path.name}"].add(cell)

	config = MATH / "game_config.py"
	if config.is_file():
		text = config.read_text(encoding="utf-8")
		sources["game_config.paytable"].update(
			re.findall(r"\(\s*\d+\s*,\s*[\"']([A-Z0-9_]+)[\"']\s*\)", text)
		)
		for name in re.findall(r"wild_symbol\s*=\s*[\"']([A-Z0-9_]+)[\"']", text):
			sources["game_config.wild"].add(name)
		for name in re.findall(r"scatter_symbol\s*=\s*[\"']([A-Z0-9_]+)[\"']", text):
			sources["game_config.scatter"].add(name)

	showcase = APP / "src" / "showcase.generated.json"
	if showcase.is_file():
		found: set[str] = set()

		def walk(node) -> None:
			if isinstance(node, dict):
				name = node.get("name")
				if isinstance(name, str):
					found.add(name)
				for value in node.values():
					walk(value)
			elif isinstance(node, list):
				for value in node:
					walk(value)

		walk(json.loads(showcase.read_text(encoding="utf-8")))
		sources["showcase.generated.json"] = found

	board = (APP / "src" / "game" / "board.generated.ts").read_text(encoding="utf-8")
	pool = re.search(r"FILL_POOL[^=]*=\s*\[([^\]]*)\]", board)
	if pool:
		sources["board.generated.FILL_POOL"] = set(re.findall(r'"([A-Z0-9_]+)"', pool.group(1)))

	return {key: sorted(value) for key, value in sorted(sources.items())}


def frontend_symbol_keys() -> dict[str, set[str]]:
	"""SYMBOL_INFO_MAP / SCATTER_WORD_INFO / WILD_EXPAND_INFO -> asset keys.

	constants.ts builds the map out of a handful of small helpers, so rather
	than half-parsing TypeScript this resolves the same helpers by name: each
	`const <n>Static = { ... assetKey: '<k>' ... }` binding, the `spineState` /
	`blurState` / `scatterWord` shapes, and the `cardStates(<binding>, ...)`
	entries of SYMBOL_INFO_MAP.
	"""
	text = (APP / "src" / "game" / "constants.ts").read_text(encoding="utf-8")

	bindings = dict(
		re.findall(
			r"const\s+(\w+)\s*=\s*\{[^}]*?assetKey:\s*'([^']+)'",
			text,
			re.S,
		)
	)

	def blur_of(asset_key: str) -> str:
		# blurState(): assetKey.replace('.', '_blur.')
		return asset_key.replace(".", "_blur.", 1)

	per_symbol: dict[str, set[str]] = {}

	body = text[text.index("export const SYMBOL_INFO_MAP") :]
	body = body[: body.index("\n} as const;")]

	# cardStates(<binding>, ...) -> card in every state, blur while spinning
	for name, binding in re.findall(r"^\t(\w+):\s*cardStates\((\w+),", body, re.M):
		key = bindings.get(binding)
		if not key:
			raise SystemExit(f"constants.ts: cannot resolve binding {binding} for {name}")
		per_symbol[name] = {key, blur_of(key)}

	# explicit literal blocks: { static: <binding>, spin: blurState('x'), ... }
	for match in re.finditer(r"^\t([A-Z][A-Z0-9_]*):\s*\{(.*?)^\t\},", body, re.S | re.M):
		name, block = match.group(1), match.group(2)
		keys: set[str] = set()
		for binding in re.findall(r":\s*(\w+)\s*,", block):
			if binding in bindings:
				keys.add(bindings[binding])
		for literal in re.findall(r"blurState\('([^']+)'\)", block):
			keys.add(blur_of(literal))
		if keys:
			per_symbol[name] = keys

	# S delegates to SCATTER_WORD_INFO[1]; the board can wear faces 1..5
	scatter = {f"wrScatter{n}" for n in (1, 2, 3, 4, 5)}
	scatter.update(re.findall(r"assetKey:\s*'(wrScatterBlur)'", text))
	per_symbol["S"] = scatter

	# an expanding W wears WILD_EXPAND_INFO on top of its normal card
	expand = re.search(r"export const WILD_EXPAND_INFO[^;]*?;", text, re.S)
	if expand:
		for binding in re.findall(r":\s*(\w+)\s*,", expand.group(0)):
			if binding in bindings:
				per_symbol.setdefault("W", set()).add(bindings[binding])

	return per_symbol


def exists_exact(path: Path) -> bool:
	"""is_file(), but case-sensitive even on Windows."""
	try:
		return path.name in {entry.name for entry in path.parent.iterdir()}
	except OSError:
		return False


def registered_assets() -> tuple[dict[str, bool], dict[str, set[str]], list[str]]:
	"""What src/game/assets.ts registers: {key: isPreloaded}, plus atlas frames.

	A `sprites`-type asset is spread into loadedAssets under its FRAME names
	(see PROCESS_METHOD_MAP.sprites in packages/pixi-svelte/src/lib/assetLoad.ts),
	so a symbol asking for `h2.webp` is asking for a frame, not for a top-level
	registration — and that frame inherits its atlas's preload flag.
	"""
	text = (APP / "src" / "game" / "assets.ts").read_text(encoding="utf-8")

	# Each top-level entry runs from its own key to the next one. Registrations
	# are written both multi-line and on a single line (winTier*), so slicing
	# between key starts covers both rather than assuming a closing-brace shape.
	starts = [(m.start(), m.group(1)) for m in re.finditer(r"^\t(\w+):\s*\{", text, re.M)]
	entries: dict[str, str] = {}
	for index, (offset, name) in enumerate(starts):
		end = starts[index + 1][0] if index + 1 < len(starts) else len(text)
		entries[name] = text[offset:end]

	top_level = {
		name: bool(re.search(r"preload:\s*true", body)) for name, body in entries.items()
	}

	frames: dict[str, set[str]] = {}
	problems: list[str] = []
	for name, body in entries.items():
		kind = re.search(r"type:\s*'(\w+)'", body)
		src = re.search(r"src:\s*new URL\('([^']+)'", body)
		if not kind or not src or kind.group(1) != "sprites":
			continue
		atlas = (APP / "src" / "game" / src.group(1)).resolve()
		# Path.is_file() is case-INSENSITIVE on Windows, which is where this game
		# is developed and exactly how a name that only works locally ships to a
		# case-sensitive Linux host. Match against the real directory listing.
		if not exists_exact(atlas):
			problems.append(f"assets.ts {name}: atlas JSON missing on disk (case-exact): {atlas}")
			continue
		data = json.loads(atlas.read_text(encoding="utf-8"))
		frames[name] = set(data.get("frames", {}))
		image = (data.get("meta") or {}).get("image")
		if image and not exists_exact(atlas.parent / image):
			problems.append(
				f"assets.ts {name}: atlas image missing on disk (case-exact): {image}"
			)

	return top_level, frames, problems


def run_static() -> tuple[bool, dict]:
	print("=== STATIC symbol coverage ===")
	sources = math_symbol_names()
	emitted: set[str] = set()
	for label, names in sources.items():
		print(f"  {label}: {' '.join(names)}")
		emitted.update(names)
	print(f"  -> math can emit: {' '.join(sorted(emitted))}")

	per_symbol = frontend_symbol_keys()
	top_level, frames, problems = registered_assets()
	# key -> is it in the PRELOAD batch? atlas frames inherit their atlas's flag
	preloaded: dict[str, bool] = dict(top_level)
	for atlas_name, atlas_frames in frames.items():
		for frame in atlas_frames:
			preloaded[frame] = preloaded.get(frame, False) or top_level.get(atlas_name, False)

	unmapped = sorted(name for name in emitted if name not in per_symbol)
	missing: dict[str, list[str]] = {}
	# AssetsLoader renders the game once the PRELOAD batch resolves, and Board
	# mounts whenever showLoadingScreen is false — already the case on an
	# in-place <App> remount. Symbol art that is not preloaded therefore draws as
	# Texture.EMPTY (a dark box) for that whole window. This is the invariant
	# that the h2/h4/h5/l3 "not found in the loadedAssets" bug violated.
	late: dict[str, list[str]] = {}
	for name in sorted(emitted):
		for key in sorted(per_symbol.get(name, ())):
			if key not in preloaded:
				missing.setdefault(name, []).append(key)
			elif not preloaded[key]:
				late.setdefault(name, []).append(key)

	print(f"  frontend maps {len(per_symbol)} symbols to {sum(len(v) for v in per_symbol.values())} asset keys")
	print(f"  registry exposes {len(top_level)} top-level keys + {sum(len(v) for v in frames.values())} atlas frames")
	if unmapped:
		print(f"  !! symbols with NO frontend entry: {unmapped}")
	for name, keys in missing.items():
		print(f"  !! {name} asks for unregistered keys: {keys}")
	for name, keys in late.items():
		print(f"  !! {name} asks for NON-PRELOADED keys (dark box until fully loaded): {keys}")
	for problem in problems:
		print(f"  !! {problem}")
	ok = not unmapped and not missing and not late and not problems
	print("  STATIC", "PASS" if ok else "FAIL")
	return ok, {
		"sources": sources,
		"emitted": sorted(emitted),
		"unmapped": unmapped,
		"missingKeys": missing,
		"notPreloaded": late,
		"atlasProblems": problems,
	}


# --------------------------------------------------------------------------
# RUNTIME
# --------------------------------------------------------------------------


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
		import websocket  # noqa: PLC0415 - optional dep, only needed for --runtime

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
		self.websocket = websocket
		self.socket = self._connect()
		self.message_id = 0
		self.failures: list[dict] = []
		self.send("Page.enable")
		self.send("Runtime.enable")
		self.send("Network.enable")
		self.send("Page.addScriptToEvaluateOnNewDocument", source=CONSOLE_HOOK)

	def _connect(self):
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
				return self.websocket.create_connection(
					page["webSocketDebuggerUrl"],
					timeout=60,
					max_size=None,
					suppress_origin=True,
				)
			except Exception as error:  # noqa: BLE001 - retried until the deadline
				last_error = error
				time.sleep(0.6)
		raise SystemExit(f"could not attach to Chrome DevTools: {last_error!r}")

	def _record(self, frame: dict) -> None:
		method = frame.get("method")
		params = frame.get("params") or {}
		if method == "Network.responseReceived":
			response = params.get("response") or {}
			if response.get("status", 0) >= 400:
				self.failures.append(
					{"url": response.get("url", ""), "status": response.get("status")}
				)
		elif method == "Network.loadingFailed":
			self.failures.append(
				{"url": "<loadingFailed>", "status": params.get("errorText", "failed")}
			)

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
	try:
		from PIL import Image, ImageDraw  # noqa: PLC0415 - optional dep
	except ImportError:
		return
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


def run_story(chrome: Chrome, name: str, story_id: str, port: int, budget: float) -> dict:
	story_dir = OUT / name
	shutil.rmtree(story_dir, ignore_errors=True)
	story_dir.mkdir(parents=True, exist_ok=True)
	url = f"http://localhost:{port}/iframe.html?id={story_id}&viewMode=story"
	print(f"[{name}] {url}")

	chrome.failures.clear()
	chrome.send("Page.navigate", url=url)
	time.sleep(3.0)

	action_ready = (
		"!!document.querySelector('button.action')"
		" && !document.querySelector('button.action').disabled"
	)
	# parallel agents share this Storybook, so a cold compile can take a while
	if not wait_for(chrome, action_ready, COMPILE_BUDGET, "Action button enabled"):
		print("  reloading once")
		chrome.send("Page.navigate", url=url)
		time.sleep(4.0)
		if not wait_for(chrome, action_ready, COMPILE_BUDGET, "Action button enabled (retry)"):
			chrome.screenshot(story_dir / "_not_ready.png")
			return {"story": name, "ready": False}

	# A click can land before Svelte has attached its delegated handler, which
	# leaves the story sitting on the idle board for the whole budget. Confirm
	# the button actually latched, and click again if it did not.
	running = "((document.querySelector('.message')||{}).textContent || '').includes('Running')"
	started_book = False
	for _ in range(4):
		chrome.evaluate("document.querySelector('button.action').click(); true")
		time.sleep(CLICK_SETTLE)
		if chrome.evaluate(running) is True:
			started_book = True
			break
	if not started_book:
		print("  ! Action click never latched")
		chrome.screenshot(story_dir / "_no_click.png")
		return {"story": name, "ready": False}
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

	# Re-render the story in place and keep watching. This is NOT the guard for
	# the preload bug — verified by removing preload from symbolsStatic, which
	# run_static catches and this phase does not: PIXI.Assets caches by URL, so
	# AssetsLoader's second pass republishes both batches in one microtask burst
	# and no sprite ever sees the preload-only window. It is here to catch misses
	# that only show up on a re-render, and for the frames.
	remount = chrome.evaluate(
		"(() => { const c = window.__STORYBOOK_ADDONS_CHANNEL__;"
		f" if (!c) return false; c.emit('forceRemount', {{ storyId: '{story_id}' }});"
		" return true; })()"
	)
	if remount is True:
		for index in range(REMOUNT_FRAMES):
			time.sleep(FRAME_INTERVAL)
			chrome.screenshot(story_dir / f"remount{index:02d}.png")
	else:
		print("  ! Storybook channel unavailable; remount path NOT exercised")

	missing = json.loads(chrome.evaluate("JSON.stringify(window.__qaMissing || {})") or "{}")
	errors = json.loads(chrome.evaluate("JSON.stringify((window.__qaErrors || []).slice(0, 40))") or "[]")
	loaded_keys = chrome.evaluate(
		"(() => { const s = window.__qaLoadedAssetKeys; return s ? s.length : -1; })()"
	)
	asset_failures = [
		failure
		for failure in chrome.failures
		if any(
			failure.get("url", "").endswith(ext)
			for ext in (".webp", ".png", ".json", ".mp4", ".webm", ".xml", ".atlas")
		)
	]

	report = {
		"story": name,
		"storyId": story_id,
		"ready": True,
		"resolved": resolved,
		"frames": len(frames),
		"remountExercised": remount is True,
		"missingAssetKeys": missing,
		"loadedAssetKeyCount": loaded_keys,
		"assetFailures": asset_failures[:20],
		"consoleErrors": errors,
	}
	(story_dir / "_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

	print(f"  missing asset keys: {missing or 'NONE'}")
	print(f"  asset request failures: {len(asset_failures)}")
	for failure in asset_failures[:6]:
		print(f"    - {failure}")
	print(f"  other console errors: {len(errors)}")
	for line in errors[:6]:
		print(f"    console: {line[:180]}")
	contact_sheet(story_dir, frames)
	return report


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--port", type=int, default=6009)
	parser.add_argument("--story", action="append", choices=sorted(STORIES), default=None)
	parser.add_argument("--budget", type=float, default=300.0)
	parser.add_argument("--static-only", action="store_true")
	args = parser.parse_args()
	# A full sweep runs for many minutes; block-buffered stdout would show
	# nothing at all until it ends.
	sys.stdout.reconfigure(line_buffering=True)

	static_ok, static_report = run_static()
	OUT.mkdir(parents=True, exist_ok=True)
	(OUT / "_static.json").write_text(json.dumps(static_report, indent=2), encoding="utf-8")
	if args.static_only:
		return 0 if static_ok else 1

	targets = args.story or list(STORIES)
	print("\n=== RUNTIME symbol coverage ===")
	reports = []
	for name in targets:
		# One browser PER STORY, for two reasons. Correctness: a fresh profile
		# means a cold asset load every time, which is the boot window the
		# missing-symbol bug actually lived in — reusing a warm browser would
		# hide it behind Chrome's HTTP cache. Robustness: thirteen WebGL books
		# in one process eventually kills the tab, and a dead DevTools socket
		# must cost one story, not the whole sweep.
		chrome = None
		try:
			chrome = Chrome()
			reports.append(run_story(chrome, name, STORIES[name], args.port, args.budget))
		except Exception as error:  # noqa: BLE001 - one story must not abort the sweep
			print(f"  ! {name} crashed the driver: {error!r}")
			reports.append({"story": name, "ready": False, "driverError": repr(error)})
		finally:
			if chrome is not None:
				try:
					chrome.close()
				except Exception:  # noqa: BLE001 - already tearing down
					pass

	(OUT / "_summary.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")
	runtime_ok = all(
		report.get("ready")
		and report.get("remountExercised")
		and not report.get("missingAssetKeys")
		and not report.get("assetFailures")
		for report in reports
	)
	print("\n=== SUMMARY ===")
	for report in reports:
		print(
			f"  {report['story']:18s} ready={report.get('ready')} "
			f"resolved={report.get('resolved')} "
			f"remount={report.get('remountExercised')} "
			f"missingKeys={sorted((report.get('missingAssetKeys') or {}))} "
			f"assetFailures={len(report.get('assetFailures') or [])} "
			f"consoleErrors={len(report.get('consoleErrors') or [])}"
		)
	print(f"  static: {'PASS' if static_ok else 'FAIL'}")
	print("PASS" if (static_ok and runtime_ok) else "FAIL")
	return 0 if (static_ok and runtime_ok) else 1


if __name__ == "__main__":
	sys.exit(main())
