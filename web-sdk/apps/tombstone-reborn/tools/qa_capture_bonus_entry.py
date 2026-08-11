"""Film the BONUS-ENTRY BANNER and the WIN TAKEOVER, and prove they hand off.

A single screenshot of a bonus story shows the idle board, so it can never show an
entrance animation. This drives Chrome over the DevTools Protocol (same client as
tools/qa_verify_bonus_surface.py, imported rather than copied), clicks Storybook's
Action button and films the presentation with Page.startScreencast.

WHAT IT ASSERTS
  * the takeover really appears, promptly, and its hero window renders lit warm
    art rather than the black box a missing texture key would leave
  * no deleted Madam Mirror bonus-entry media was requested, and nothing 404s
  * zero console errors FROM THIS AGENT'S FILES, and the page was never reloaded
    under the run. Errors raised by the surfaces other agents are mid-rewrite on are
    printed but do not fail the run — see FOREIGN_SURFACES.
  * the round RESOLVES — a banner that trapped the player would never get there
  * the banner is SKIPPABLE: the same story runs twice, once with Space pressed
    inside the hold, and the measured on-screen window must collapse
  * the panel edges are croppped at 4x for the outline check the player asked for
    (the authoritative measurement of the baked frames is check_frame_edges.py)

The takeover window is measured from the frames themselves: it dims the whole
canvas, so the mean luma of the four viewport corners collapses while it is up and
recovers when it hands off.

Usage:
  python tools/qa_capture_bonus_entry.py [--port 6009] [--story dead_mans_hand ...]
  python tools/qa_capture_bonus_entry.py --rezoom   # redo crops, no browser

Output: qa-shots/bonus-entry/<run>/f###.jpg, _edge_zoom.png, _sheet.jpg, _report.json
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from base64 import b64decode
from pathlib import Path

import numpy as np
from PIL import Image

from qa_verify_bonus_surface import (
    DELETED_MEDIA,
    Chrome,
    contact_sheet,
    wait_for,
)

# Storybook's status line goes "Running..." -> "Action is resolved" -> "Click
# action to start", and the middle state can be shorter than one poll, so the
# round is treated as finished the moment it stops running. Waiting for the
# literal "resolved" text reported a hang on a round that had plainly completed.
FINISHED_EXPRESSION = (
    "(() => { const m = document.querySelector('.message');"
    " return !!m && !m.textContent.includes('Running'); })()"
)

# Records STACKS, not just messages: "TypeError: Failed to fetch" on its own says
# nothing about whose code raised it, and the pass condition is zero console errors
# FROM THE FILES THIS AGENT OWNS. Guarded so re-installing it is a no-op.
CONSOLE_HOOK = """
(() => {
  if (window.__qaHooked) return;
  window.__qaHooked = true;
  window.__qaErrors = [];
  const describe = (value) => {
    if (value && value.stack) return String(value.stack);
    if (value instanceof Error) return value.name + ': ' + value.message;
    try { return typeof value === 'string' ? value : JSON.stringify(value); }
    catch (_) { return String(value); }
  };
  const base = console.error.bind(console);
  console.error = (...args) => {
    window.__qaErrors.push(args.map(describe).join(' ').slice(0, 600));
    base(...args);
  };
  window.addEventListener('error', (event) =>
    window.__qaErrors.push('onerror: ' + describe(event.error || event.message)));
  window.addEventListener('unhandledrejection', (event) =>
    window.__qaErrors.push('unhandledrejection: ' + describe(event.reason)));
})();
"""

APP = Path(__file__).resolve().parents[1]
OUT = APP / "qa-shots" / "bonus-entry"

# Surfaces owned by the other agents working this app in parallel. Their errors are
# still printed, because a broken sibling surface is worth knowing about, but they
# cannot decide this agent's verdict — the fire/split agent in particular is mid
# rewrite and throws from SplitPanes on every split spin.
#
# Deliberately an allowlist of FOREIGN files rather than a list of mine: an error
# whose stack names nothing recognisable counts as MINE, so a stack this script
# fails to parse can never quietly excuse a bug in the banner.
FOREIGN_SURFACES = (
    "SplitPanes",
    "TargetLock",
    "CloneMorph",
    "BulletHoleMark",
    "StretchFx",
    "WildReelSlide",
    "TombstoneFxSprite",
    "tombstoneVfx",
    "splitBullets",
    "NudgeSlide",
    "StretchWays",
    "Anticipation",
    "Transition",
    "FeatureBurst",
    "FeatureFxSprite",
    "featureVfx",
    "CellSealOverlay",
    "FrameMorphHud",
    "InfoMarquee",
)


def split_errors(errors: list[str]) -> tuple[list[str], list[str]]:
    """Split console errors into (mine, another agent's), by stack origin."""
    mine, foreign = [], []
    for error in errors:
        (foreign if any(name in error for name in FOREIGN_SURFACES) else mine).append(error)
    return mine, foreign


# A takeover (banner or win tier) dims the board, so the frames worth keeping are
# the ones where the veil is up. A banner opens the round, so filming starts at the
# click; a win tier only arrives once the spin has resolved, so filming waits for
# the veil to appear.
BANNER, CELEBRATION = "banner", "celebration"

# run name -> (story id, media the surface must fetch, press Space mid-banner, kind)
RUNS: dict[str, tuple[str, tuple[str, ...], bool, str]] = {
    "dead_mans_hand": (
        "bonus-entry-banner--dead-mans-hand",
        ("bonus_entry_small.webp", "bonus_frame_small.png"),
        False,
        BANNER,
    ),
    "open_grave": (
        "bonus-entry-banner--open-grave",
        ("bonus_entry_super.webp", "bonus_frame_super.png"),
        False,
        BANNER,
    ),
    "open_grave_turbo": (
        "bonus-entry-banner--open-grave-turbo",
        ("bonus_entry_super.webp", "bonus_frame_super.png"),
        False,
        BANNER,
    ),
    # same story as open_grave, but Space a beat in — proves tap/Space skips
    "open_grave_skipped": (
        "bonus-entry-banner--open-grave",
        ("bonus_entry_super.webp", "bonus_frame_super.png"),
        True,
        BANNER,
    ),
    # The win takeover shares this capture path because the two surfaces share
    # their light and particle atlases, and because the takeover's panel outline
    # removal has to be checked at the peak of presentation, not on the idle board.
    "win_ladder": (
        "mode-bonus-book--max-win",
        ("win_frame.png",),
        False,
        CELEBRATION,
    ),
}

# Filming is a SCREENCAST, not a screenshot loop. Chrome pushes frames as the page
# changes, so there is no per-frame round trip: on this machine (100+ Chrome
# processes from other agents) a Page.captureScreenshot cost 1.5-2.5s, and the
# first frame of a 2.2s banner landed at +2.4s — the capture was slower than the
# thing it was meant to film, and reported the banner missing.
SCREENCAST_QUALITY = 92
FILM_SECONDS = {BANNER: 8.0, CELEBRATION: 26.0}
MAX_FRAMES = 220
FRAME_WAIT = 1.0  # a screencast is silent while the page is still
SETTLE_POLL = 1.5
# Only corroboration now that hand-off is proven from the film, and every extra
# second of waiting is another chance for someone else's hot reload to land.
SETTLE_BUDGET = 90.0
SKIP_AFTER_SECONDS = 0.6
VEIL_POLL = 1.0
VEIL_WAIT_BUDGET = 120.0
# A viewport corner shows the lit graveyard background at rest and the banner's
# dim veil while it is up; 26/255 sits between the two. The win celebration
# dims the board the same way LATER, so only the LEADING veiled run — the frames
# immediately after the click — is the banner.
STATIC_EXTENSIONS = (
    "webp", "png", "jpg", "json", "mp4", "webm", "xml", "atlas", "js", "ts",
    "svelte", "css", "woff", "woff2", "ttf", "mp3", "ogg", "wav", "ico", "svg",
)
DEV_SERVER_NOISE = ("/@vite", "/@fs", "/@id", "/node_modules/", "/sb-", "/index.json")

CORNER = 140
VEIL_LUMA = 26
# The banner opens the round, so its veil must appear within a beat of the click.
# Measured in SECONDS rather than frames: at screencast rates a frame budget of 4
# meant a quarter of a second.
VEIL_LEAD_SECONDS = 2.0


def film(chrome: Chrome, story_dir: Path, seconds: float) -> tuple[list[Path], list[float]]:
    """Film with Page.startScreencast, which PUSHES frames as the page changes."""
    chrome.send(
        "Page.startScreencast", format="jpeg", quality=SCREENCAST_QUALITY, everyNthFrame=1
    )
    frames: list[Path] = []
    times: list[float] = []
    started = time.time()
    chrome.socket.settimeout(FRAME_WAIT)
    try:
        while time.time() - started < seconds and len(frames) < MAX_FRAMES:
            try:
                message = json.loads(chrome.socket.recv())
            except Exception:  # noqa: BLE001 - a quiet page just yields no frame
                continue
            if message.get("method") != "Page.screencastFrame":
                # keep the network bookkeeping the Chrome client does for itself
                chrome._record(message)  # noqa: SLF001 - same toolchain, one client
                continue
            params = message["params"]
            dest = story_dir / f"f{len(frames):03d}.jpg"
            dest.write_bytes(b64decode(params["data"]))
            frames.append(dest)
            times.append(round(time.time() - started, 3))
            chrome.message_id += 1
            # acked without waiting for the reply, so acking cannot swallow the next
            # frame; the reply is skipped by the loop above
            chrome.socket.send(
                json.dumps(
                    {
                        "id": chrome.message_id,
                        "method": "Page.screencastFrameAck",
                        "params": {"sessionId": params["sessionId"]},
                    }
                )
            )
    finally:
        chrome.socket.settimeout(60)
        chrome.send("Page.stopScreencast")
    return frames, times


BOARD = 0.55  # central share of the frame the reels occupy
# Spinning reels move the board far more than the idle scene's dust does; the idle
# baseline measured under 1.0 and a spin measured well above 6.
HANDOFF_MOTION = 4.0


def motion_after(frames: list[Path], first: int) -> float:
    """Biggest frame-to-frame change in the board area from `first` onwards.

    This is the hand-off proof: once the takeover lifts, the reels have to be
    moving. It is measured inside the film rather than by waiting for Storybook to
    say the book resolved, because the wait is long enough for another agent's
    hot reload to land — and a reloaded page reports "click action to start",
    which reads exactly like a round that finished cleanly.
    """
    best = 0.0
    previous = None
    for frame in frames[first:]:
        art = np.asarray(Image.open(frame).convert("L")).astype(np.float32)
        height, width = art.shape
        inset_y, inset_x = int(height * (1 - BOARD) / 2), int(width * (1 - BOARD) / 2)
        board = art[inset_y : height - inset_y, inset_x : width - inset_x]
        if previous is not None and previous.shape == board.shape:
            best = max(best, float(np.abs(board - previous).mean()))
        previous = board
    return round(best, 2)


def hero_art(path: Path) -> dict:
    """Is a lit, warm hero plate actually on screen?

    This replaced an assertion that the tier's .webp had been REQUESTED, which was
    wrong: PIXI v8 decodes textures in a worker, so those fetches belong to the
    worker target and never appear in the page's network log — the check reported
    art missing while the art was plainly on screen. What matters anyway is that
    the plate rendered, and a failed key would leave the window black (or skip the
    banner entirely), so measuring the window is both truer and stricter.
    """
    box = plate_box(path)
    if box is None:
        return {"lit": False, "warm": False}
    art = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    left, top, right, bottom = box
    inside = art[top : bottom + 1, left : right + 1]
    red, _, blue = (float(inside[:, :, channel].mean()) for channel in range(3))
    highlight = float((inside @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)).max())
    return {
        # a missing texture leaves the window black, so the plate has to show a
        # real highlight, not merely exist
        "lit": highlight > PLATE_LUMA,
        "peakLuma": round(highlight, 1),
        "box": f"{left},{top}..{right},{bottom}",
        # every plate in this game is a warm dusty western scene; a cold or grey
        # window would mean the wrong art or the cloned game's steel palette
        "warm": red > blue * 1.25,
        "meanRed": round(red, 1),
        "meanBlue": round(blue, 1),
    }


def corner_luma(path: Path) -> float:
    art = np.asarray(Image.open(path).convert("L")).astype(np.float32)
    height, width = art.shape
    boxes = [
        art[0:CORNER, 0:CORNER],
        art[0:CORNER, width - CORNER : width],
        art[height - CORNER : height, 0:CORNER],
        art[height - CORNER : height, width - CORNER : width],
    ]
    return float(np.mean([box.mean() for box in boxes]))


def leading_veil(lumas: list[float], times: list[float]) -> tuple[list[int], float]:
    """Frames of the banner's veil and how long it stayed up, in seconds."""
    start = next(
        (
            index
            for index, luma in enumerate(lumas)
            if luma < VEIL_LUMA and times[index] <= VEIL_LEAD_SECONDS
        ),
        None,
    )
    if start is None:
        return [], 0.0
    end = start
    while end + 1 < len(lumas) and lumas[end + 1] < VEIL_LUMA:
        end += 1
    # the veil is gone by the first lit frame after the run, so that timestamp
    # bounds the window from above
    lifted = times[end + 1] if end + 1 < len(times) else times[end]
    return list(range(start, end + 1)), round(lifted - times[start], 2)


PANEL_ZOOM = 4
# The hero plate is by far the brightest thing on a takeover frame, so it is found
# by absolute luma rather than a relative threshold — the veil makes everything
# else dark, which is precisely why a relative one latched onto the HUD.
PLATE_LUMA = 90  # a lit hero window, for the "is the art there at all" check
STORYBOOK_BAR = 40  # the yellow Action toolbar is brighter than any game art
PANEL_LIFT = 10  # how far above the veil the panel has to sit to count
PANEL_THICKNESS = 40  # lit pixels a column/row must have to be crossing the panel
PATCH = 150  # crop size around each edge, generous enough to hold both edges


def widest_run(profile: np.ndarray, floor: int) -> tuple[int, int] | None:
    """Longest contiguous stretch of the profile above `floor`."""
    best = span = None
    start = None
    for index, value in enumerate(profile):
        if value > floor:
            start = index if start is None else start
            continue
        if start is not None:
            if span is None or index - start > span:
                span, best = index - start, (start, index - 1)
            start = None
    if start is not None and (span is None or profile.size - start > span):
        best = (start, profile.size - 1)
    return best


def plate_box(path: Path) -> tuple[int, int, int, int] | None:
    """Bounding box of the takeover PANEL, measured against the veil around it.

    Not an absolute luma threshold: the hero plates differ hugely in brightness
    (HIGH NOON is a bright orange sky, BOOT HILL is nearly black), and an absolute
    one clipped the dark tiers to a fragment of the panel. The veil is uniform, so
    the panel is whatever stands above it — read as the widest continuous run, so
    HUD glints outside the panel cannot stretch the box.
    """
    luma = np.asarray(Image.open(path).convert("L")).astype(np.float32)[STORYBOOK_BAR:]
    height, width = luma.shape
    corner = 60
    veil = float(
        np.median(
            np.concatenate(
                [
                    luma[:corner, :corner].ravel(),
                    luma[:corner, -corner:].ravel(),
                    luma[-corner:, :corner].ravel(),
                    luma[-corner:, -corner:].ravel(),
                ]
            )
        )
    )
    lit = luma > veil + PANEL_LIFT
    columns = widest_run(lit.sum(axis=0), PANEL_THICKNESS)
    rows = widest_run(lit.sum(axis=1), PANEL_THICKNESS)
    if columns is None or rows is None:
        return None
    if columns[1] - columns[0] < 80 or rows[1] - rows[0] < 60:
        return None
    return columns[0], rows[0] + STORYBOOK_BAR, columns[1], rows[1] + STORYBOOK_BAR


def edge_zoom(source: Path, dest: Path) -> str:
    """Blow up the three edges where a stray outline would show, at 4x.

    Left to right: the hero window's top-left corner (the inner edge the reference
    frame pointed at), the frame band's outer top-left corner, and the title
    plate's left edge below the panel.
    """
    art = Image.open(source).convert("RGB")
    box = plate_box(source)
    if box is None:
        return "no panel found"
    left, top, right, bottom = box
    middle = (top + bottom) // 2
    centre = (left + right) // 2
    boxes = [
        # panel's top-left corner: outer edge and window corner in one crop
        (left - 20, top - 20, left + PATCH, top + PATCH),
        # left edge at mid-height, away from the corner straps
        (left - 20, middle - PATCH // 2, left + PATCH, middle + PATCH // 2),
        # below the panel: the title plate's own edges
        (centre - PATCH, bottom + 4, centre + PATCH, bottom + 4 + PATCH),
    ]
    crops = [
        art.crop(clamped)
        for clamped in (
            (
                max(box[0], 0),
                max(box[1], 0),
                min(box[2], art.width),
                min(box[3], art.height),
            )
            for box in boxes
        )
        if clamped[2] - clamped[0] > 8 and clamped[3] - clamped[1] > 8
    ]
    # Magenta gutters, because the artifact being judged here is a thin WARM line:
    # the gold gutter this used to paint was indistinguishable from a gold hairline
    # at the crop seams, which is the one mistake this sheet must not invite.
    sheet = Image.new(
        "RGB",
        (
            sum(crop.width for crop in crops) * PANEL_ZOOM + 8 * (len(crops) - 1),
            max(crop.height for crop in crops) * PANEL_ZOOM,
        ),
        (255, 0, 255),
    )
    offset = 0
    for crop in crops:
        scaled = crop.resize(
            (crop.width * PANEL_ZOOM, crop.height * PANEL_ZOOM), Image.NEAREST
        )
        sheet.paste(scaled, (offset, 0))
        offset += scaled.width + 8
    sheet.save(dest)
    return f"panel x={left}..{right} y={top}..{bottom}"


def press_space(chrome: Chrome) -> None:
    for event in ("keyDown", "keyUp"):
        chrome.send(
            "Input.dispatchKeyEvent",
            type=event,
            key=" ",
            code="Space",
            windowsVirtualKeyCode=32,
            nativeVirtualKeyCode=32,
        )


def run(chrome: Chrome, name: str, port: int) -> dict:
    story_id, required_media, skip, kind = RUNS[name]
    story_dir = OUT / name
    shutil.rmtree(story_dir, ignore_errors=True)
    story_dir.mkdir(parents=True, exist_ok=True)
    url = f"http://localhost:{port}/iframe.html?id={story_id}&viewMode=story"
    print(f"[{name}] {url}")

    chrome.requests.clear()
    chrome.failures.clear()
    # Installed as a boot script, not after navigation: Vite forces a full reload
    # the first time it optimises a story's new dependencies, which wiped a
    # post-navigation hook and lost every error raised before it was reattached.
    chrome.send("Page.addScriptToEvaluateOnNewDocument", source=CONSOLE_HOOK)
    chrome.send("Page.navigate", url=url)
    time.sleep(3.0)

    action_ready = (
        "!!document.querySelector('button.action')"
        " && !document.querySelector('button.action').disabled"
    )
    if not wait_for(chrome, action_ready, 180, "Action button enabled"):
        chrome.screenshot(story_dir / "_not_ready.png")
        # Raised rather than returned so this takes the same retry-on-a-fresh-browser
        # path as a dropped socket: a story that never armed compiled nothing and
        # rendered nothing, so it is a harness failure, not a verdict on the surface.
        # If the retry does not arm either, the raise surfaces as a hard FAIL.
        raise RuntimeError(f"{name}: Storybook never armed the Action button")

    baseline = story_dir / "_idle.png"
    chrome.screenshot(baseline)
    idle_luma = corner_luma(baseline)

    # Marked once the board is up and about to be filmed. The hook above survives a
    # reload by design, so this mark is what tells a reload apart from a page that
    # stayed ours; marking here means Vite's one-off dependency reload, which lands
    # during boot, is not mistaken for the page dying mid-film.
    chrome.evaluate(f"window.__qaRunMark = {json.dumps(name)}; true")

    chrome.evaluate("document.querySelector('button.action').click(); true")
    print(f"  clicked Action; kind={kind} skip={skip}")

    started = time.time()
    pressed_at: float | None = None
    if skip:
        # BEFORE filming, on a wall clock: a screenshot round-trip costs over a
        # second on this machine, so pressing between frames landed after the
        # banner had already handed off and proved nothing.
        time.sleep(SKIP_AFTER_SECONDS)
        press_space(chrome)
        pressed_at = round(time.time() - started, 2)
        print(f"  pressed Space at +{pressed_at:.2f}s, inside the hold")

    waited = 0.0
    if kind == CELEBRATION:
        # the win ladder only takes over once the spin has resolved, so idle away
        # the reels rather than filming them
        probe = story_dir / "_wait.png"
        started_wait = time.time()
        while time.time() - started_wait < VEIL_WAIT_BUDGET:
            chrome.screenshot(probe)
            if corner_luma(probe) < VEIL_LUMA:
                break
            time.sleep(VEIL_POLL)
        waited = round(time.time() - started_wait, 2)
        probe.unlink(missing_ok=True)
        print(f"  takeover veil up at +{waited:.1f}s")

    seconds = FILM_SECONDS[kind]
    frames, times = film(chrome, story_dir, seconds)
    lumas = [corner_luma(frame) for frame in frames]
    rate = len(frames) / seconds if seconds else 0
    print(f"  filmed {len(frames)} frames over {seconds:.0f}s ({rate:.1f}/s)")

    veiled, banner_seconds = leading_veil(lumas, times)
    banner_frames = len(veiled)
    banner_window = (
        f"f{veiled[0]:03d}..f{veiled[-1]:03d}" if veiled else "none detected"
    )

    # zoom the panel edge on the most veiled frame — a thin bright outline is only
    # honestly judgeable at 4x, which is how the reference frame was sent
    zoom_note = "not captured"
    art_check: dict = {"lit": False}
    if veiled:
        peak = min(veiled, key=lambda index: lumas[index])
        zoom_note = edge_zoom(frames[peak], story_dir / "_edge_zoom.png")
        art_check = hero_art(frames[peak])
        print(f"  edge zoom from f{peak:03d}: {zoom_note}")
        print(f"  hero art on screen: {art_check}")

    # Hand-off is measured from the frame after the takeover lifts, or from the
    # very first frame when no takeover was on screen at all — which is the skip
    # run's expected state, Space having gone in before filming started. Skipping
    # the measurement in that case reported a hand-off of zero for the one run
    # most likely to wedge the round, i.e. it graded the riskiest path blind.
    handoff_from = veiled[-1] + 1 if veiled else 0
    handoff_motion = motion_after(frames, handoff_from)
    print(f"  board motion after the takeover lifted: {handoff_motion}")

    # Checked BEFORE the settle wait, so the film is judged on a page that was
    # demonstrably alive while it was being filmed.
    page_survived = chrome.evaluate("window.__qaRunMark") == name
    raw_errors = chrome.evaluate("JSON.stringify((window.__qaErrors || []).slice(0, 40))")
    own_errors, foreign_errors = split_errors(json.loads(raw_errors or "[]"))
    if not page_survived:
        print("  ! the page reloaded while filming (Vite dep optimisation or HMR)")

    if kind == CELEBRATION:
        # BOOT HILL parks on a CONTINUE gate by design, so the round cannot finish
        # on its own. Space is the documented release, and using it here proves the
        # gate responds rather than trapping the player.
        press_space(chrome)
        print("  pressed Space to release the CONTINUE gate")

    resolved_at: float | None = None
    deadline = time.time() + SETTLE_BUDGET
    while time.time() < deadline:
        if chrome.evaluate(FINISHED_EXPRESSION) is True:
            resolved_at = round(time.time() - started, 2)
            break
        time.sleep(SETTLE_POLL)
    # a reload during the settle also lands on "click action to start", which reads
    # like a clean finish, so the reading is only trusted if the page is still ours
    still_ours = chrome.evaluate("window.__qaRunMark") == name
    if resolved_at is not None and still_ours:
        print(f"  round finished at +{resolved_at:.1f}s")
    elif resolved_at is not None:
        print("  round finish unreadable: the page reloaded during the wait")
        resolved_at = None
    else:
        chrome.screenshot(story_dir / "_stuck.png")
        print(f"  ! round did not finish within {SETTLE_BUDGET:.0f}s")

    banned_hits = sorted(
        {media for media in DELETED_MEDIA for url in chrome.requests if media in url}
    )
    asset_failures = [
        failure
        for failure in chrome.failures
        if any(
            failure.get("url", "").endswith(ext)
            for ext in (".webp", ".png", ".json", ".mp4", ".webm", ".xml", ".atlas", ".js")
        )
    ]
    # Everything that is not a static file or dev-server plumbing. A bought round
    # places its bet before the banner opens, so a POST appearing here in the SKIP
    # run and not in the plain run would mean the skip press was ALSO reaching the
    # spin button — an accidental second bet, which is worth failing over.
    api_requests = sorted(
        {
            url
            for url in chrome.requests
            if not any(f".{ext}" in url for ext in STATIC_EXTENSIONS)
            and not any(marker in url for marker in DEV_SERVER_NOISE)
        }
    )

    report = {
        "run": name,
        "storyId": story_id,
        "kind": kind,
        "ready": True,
        "pageSurvived": page_survived,
        "waitedForVeilSeconds": waited,
        "edgeZoom": zoom_note,
        "skipPressedAtSeconds": pressed_at,
        "resolvedAtSeconds": resolved_at,
        "frames": len(frames),
        "idleCornerLuma": round(idle_luma, 2),
        "cornerLuma": [round(value, 2) for value in lumas],
        "frameTimes": [round(value, 2) for value in times],
        "bannerFrames": banner_frames,
        "bannerWindow": banner_window,
        "bannerSeconds": banner_seconds,
        "heroArt": art_check,
        "handoffMotion": handoff_motion,
        "apiRequests": api_requests,
        "frames": [frame.name for frame in frames],
        # informational: PIXI's own texture fetches happen off-thread and are not
        # in here, so this is a record of what the page itself pulled, not a check
        "spriteRequests": sorted(
            {url.split("/")[-1] for url in chrome.requests if "/sprites/" in url}
        ),
        "deletedMediaRequested": banned_hits,
        "assetFailures": asset_failures[:20],
        "consoleErrors": own_errors,
        "foreignErrors": foreign_errors,
    }
    (story_dir / "_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(
        f"  idle corner luma {idle_luma:.1f} -> takeover {banner_window} "
        f"({banner_frames} frames, {banner_seconds:.2f}s on screen)"
    )
    print(f"  deleted media requested: {banned_hits or 'NONE'}")
    print(
        f"  asset/module load failures: {len(asset_failures)}"
        f"  console errors: {len(own_errors)} mine, {len(foreign_errors)} another agent's"
    )
    for failure in asset_failures[:6]:
        print(f"    - {failure}")
    for line in own_errors[:8]:
        print(f"    MINE: {line[:190]}")
    for line in foreign_errors[:4]:
        print(f"    theirs: {line[:150]}")
    contact_sheet(story_dir, frames)
    return report


def rezoom() -> int:
    """Redo the edge crops from frames already on disk, without a browser."""
    for report_path in sorted(OUT.glob("*/_report.json")):
        story_dir = report_path.parent
        report = json.loads(report_path.read_text(encoding="utf-8"))
        veiled, _ = leading_veil(report.get("cornerLuma", []), report.get("frameTimes", []))
        if not veiled:
            print(f"  {story_dir.name:20s} no takeover frame to zoom")
            continue
        peak = min(veiled, key=lambda index: report["cornerLuma"][index])
        frame = story_dir / report["frames"][peak]
        note = edge_zoom(frame, story_dir / "_edge_zoom.png")
        print(f"  {story_dir.name:20s} {frame.name}: {note}  art={hero_art(frame)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=6009)
    parser.add_argument("--story", action="append", choices=sorted(RUNS), default=None)
    parser.add_argument(
        "--rezoom",
        action="store_true",
        help="regenerate the edge crops from the last capture's frames",
    )
    args = parser.parse_args()
    if args.rezoom:
        return rezoom()
    targets = args.story or list(RUNS)

    OUT.mkdir(parents=True, exist_ok=True)
    chrome = Chrome()
    reports: list[dict] = []
    try:
        for name in targets:
            # A starved headless tab can drop the DevTools socket mid-film. That is
            # an infrastructure failure, not a verdict on the surface, so the run is
            # retried on a fresh browser before it is allowed to fail.
            for attempt in (1, 2):
                try:
                    reports.append(run(chrome, name, args.port))
                    break
                except Exception as error:  # noqa: BLE001 - any harness failure retries
                    print(f"  ! capture failed on a fresh browser retry ({error!r})")
                    try:
                        chrome.close()
                    finally:
                        chrome = Chrome()
                    if attempt == 2:
                        reports.append({"run": name, "ready": False, "error": repr(error)})
    finally:
        chrome.close()

    (OUT / "_summary.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")
    by_name = {report["run"]: report for report in reports}

    print("\n=== SUMMARY ===")
    clean = True
    for report in reports:
        art = report.get("heroArt") or {}
        ok = bool(
            report.get("ready")
            and report.get("pageSurvived")
            and not report.get("deletedMediaRequested")
            and not report.get("assetFailures")
            and not report.get("consoleErrors")
        )
        # A banner MUST hand the round back, proven by the reels moving once it
        # lifts. The win ladder's BOOT HILL tier ends on a CONTINUE gate by design,
        # so its round is not required to finish on its own.
        if report.get("kind") == BANNER:
            ok = ok and report.get("handoffMotion", 0) > HANDOFF_MOTION
        # The skip run is the one case where seeing NOTHING is the pass: Space went
        # in before the first frame, so the takeover should already be gone.
        judged_on_art = report.get("skipPressedAtSeconds") is None
        if judged_on_art:
            ok = ok and report.get("bannerFrames", 0) > 0 and art.get("lit") and art.get("warm")
        clean = clean and ok
        print(
            f"  {report['run']:20s} takeover={report.get('bannerWindow')} "
            f"({report.get('bannerSeconds')}s) handoffMotion={report.get('handoffMotion')} "
            f"finished={report.get('resolvedAtSeconds')}s "
            f"art={('lit+warm' if art.get('lit') and art.get('warm') else 'MISSING') if judged_on_art else 'n/a (skipped)'} "
            f"errors={len(report.get('consoleErrors') or [])}"
            f"(+{len(report.get('foreignErrors') or [])} theirs) "
            f"assetFailures={len(report.get('assetFailures') or [])} {'ok' if ok else 'FAIL'}"
        )

    # skippability: pressing Space a beat in must shorten the on-screen window
    full = by_name.get("open_grave")
    skipped = by_name.get("open_grave_skipped")
    if full and skipped:
        shorter = skipped.get("bannerSeconds", 0) < full.get("bannerSeconds", 0)
        print(
            f"  SKIP CHECK: {full.get('bannerSeconds')}s unskipped vs "
            f"{skipped.get('bannerSeconds')}s after Space -> {'ok' if shorter else 'FAIL'}"
        )
        clean = clean and shorter

    print("PASS" if clean else "FAIL")
    return 0 if clean else 1


if __name__ == "__main__":
    sys.exit(main())
