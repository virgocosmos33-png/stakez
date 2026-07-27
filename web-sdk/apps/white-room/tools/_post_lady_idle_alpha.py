"""Chromakey lady idle mp4s to alpha webm WITHOUT crossfade-wrap.

Local sine-loop idles already close the loop (phase 0 == phase 2pi), so
crossfade-wrap only creates double-body / double-chair ghosts. Encode VP9
yuva420p after blue key, then strip detached alpha islands (floating oval /
magnifying-glass chroma garbage near lap/chair).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

APP = Path(__file__).resolve().parents[1]
SRC = APP / "assets-raw" / "lady_video"
STATIC = APP / "static" / "assets" / "sprites" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
TMP = Path(tempfile.gettempdir()) / "lady_idle_post"
TMP.mkdir(parents=True, exist_ok=True)

KEY = "chromakey=0x0000FF:0.20:0.10,despill=type=blue:mix=0.55:expand=0.08"
BOTTOM_KEEP = 0.955
MIN_ISLAND = 80  # drop detached blobs smaller than this (oval garbage)


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd[:8])}...\n{result.stderr[-2000:]}")


def probe_h(mp4: Path) -> int:
    out = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=height",
            "-of",
            "json",
            str(mp4),
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return int(json.loads(out)["streams"][0]["height"])


def strip_detached_islands(rgba: np.ndarray) -> tuple[np.ndarray, int]:
    """Drop small detached alpha blobs (floating oval). Never gut the figure."""
    alpha = rgba[:, :, 3]
    binary = (alpha > 24).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    bridged = cv2.dilate(binary, k)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(bridged, 8)
    if n <= 1:
        return rgba, 0
    areas = stats[1:, cv2.CC_STAT_AREA]
    main = 1 + int(np.argmax(areas))
    main_area = int(stats[main, cv2.CC_STAT_AREA])
    total = int(areas.sum())
    # Safety: if "main" is not clearly the figure, do nothing
    if main_area < max(5000, int(0.55 * total)):
        return rgba, 0

    # Keep main + any large secondaries; drop only small islands (oval garbage)
    keep = labels == main
    for i in range(1, n):
        if i == main:
            continue
        area = int(stats[i, cv2.CC_STAT_AREA])
        if area > main_area * 0.15:
            keep |= labels == i

    drop_mask = (binary > 0) & (~keep)
    # Only count drops that were meaningful islands
    dropped = int(drop_mask.sum())
    if dropped < MIN_ISLAND:
        return rgba, 0
    out = rgba.copy()
    out[drop_mask, 3] = 0
    out[out[:, :, 3] < 8, :3] = 0
    return out, dropped


def scrub_webm_frames(webm: Path) -> int:
    """Decode → strip islands per frame → re-encode alpha webm in place."""
    work = Path(tempfile.mkdtemp(prefix="lady_scrub_"))
    frames_dir = work / "frames"
    frames_dir.mkdir()
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-c:v", "libvpx-vp9", "-i", str(webm),
            "-pix_fmt", "rgba", str(frames_dir / "f_%04d.png"),
        ]
    )
    total_dropped = 0
    paths = sorted(frames_dir.glob("f_*.png"))
    for p in paths:
        arr = np.array(Image.open(p).convert("RGBA"))
        cleaned, dropped = strip_detached_islands(arr)
        total_dropped += dropped
        Image.fromarray(cleaned).save(p)
    scrubbed = work / "scrubbed.webm"
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", "24",
            "-i", str(frames_dir / "f_%04d.png"),
            "-c:v", "libvpx-vp9",
            "-pix_fmt", "yuva420p",
            "-b:v", "0",
            "-crf", "28",
            "-auto-alt-ref", "0",
            "-an",
            str(scrubbed),
        ]
    )
    webm.write_bytes(scrubbed.read_bytes())
    # cleanup
    for p in frames_dir.glob("*.png"):
        p.unlink()
    frames_dir.rmdir()
    scrubbed.unlink(missing_ok=True)
    work.rmdir()
    return total_dropped


def robust_copy(src: Path, dest: Path, attempts: int = 10) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    for i in range(attempts):
        try:
            if dest.exists():
                try:
                    dest.unlink()
                except OSError:
                    pass
            shutil.copy2(src, dest)
            return
        except OSError:
            time.sleep(0.4 * (i + 1))
    # last resort: write bytes
    dest.write_bytes(src.read_bytes())


def main() -> None:
    STATIC.mkdir(parents=True, exist_ok=True)
    VITE.mkdir(parents=True, exist_ok=True)
    for mp4 in sorted(SRC.glob("lady_idle_*.mp4")):
        # Skip helper/temp encodes (e.g. lady_idle_base_TRIMMED_CLEAN.mp4)
        if mp4.stem not in ("lady_idle_base", "lady_idle_bonus"):
            continue
        h = probe_h(mp4)
        keep_h = (round(h * BOTTOM_KEEP) // 2) * 2
        vf = (
            f"{KEY},format=yuva420p,"
            f"crop=iw:{keep_h}:0:0,pad=iw:{h}:0:0:color=0x00000000"
        )
        tmp_out = TMP / f"{mp4.stem}.webm"
        print(f"[post] {mp4.name} -> {tmp_out.name} (temp)", flush=True)
        if tmp_out.exists():
            tmp_out.unlink()
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(mp4),
                "-vf",
                vf,
                "-c:v",
                "libvpx-vp9",
                "-pix_fmt",
                "yuva420p",
                "-b:v",
                "0",
                "-crf",
                "30",
                "-auto-alt-ref",
                "0",
                "-an",
                str(tmp_out),
            ]
        )
        dropped = scrub_webm_frames(tmp_out)
        print(f"[scrub] {tmp_out.name} dropped_island_px~{dropped}", flush=True)
        out = STATIC / f"{mp4.stem}.webm"
        robust_copy(tmp_out, out)
        robust_copy(tmp_out, VITE / out.name)
        # verify alpha + no floating islands mid-loop
        SRC.joinpath("_qa").mkdir(parents=True, exist_ok=True)
        for ss, tag in (("0.25", "oval"), ("1.5", "mid")):
            dest = SRC / "_qa" / f"{mp4.stem}_{tag}_check.png"
            run(
                [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-c:v", "libvpx-vp9", "-ss", ss, "-i", str(tmp_out),
                    "-frames:v", "1", "-pix_fmt", "rgba", str(dest),
                ]
            )
            a = np.array(Image.open(dest).convert("RGBA"))[..., 3]
            n, _, stats, _ = cv2.connectedComponentsWithStats((a > 24).astype(np.uint8), 8)
            if n <= 1:
                extras = []
            else:
                main_i = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
                extras = [
                    int(stats[i, cv2.CC_STAT_AREA])
                    for i in range(1, n)
                    if i != main_i and int(stats[i, cv2.CC_STAT_AREA]) >= MIN_ISLAND
                ]
            print(
                f"[alpha] {out.name} @{ss}s size={out.stat().st_size // 1024}KB "
                f"frac0={float((a < 8).mean()):.3f} extras>={MIN_ISLAND}:{extras}",
                flush=True,
            )
            if extras:
                raise SystemExit(f"floating islands remain in {out.name} @{ss}s: {extras}")
        if float((a < 8).mean()) < 0.2:
            raise SystemExit(f"alpha key failed for {out.name}")


if __name__ == "__main__":
    main()
