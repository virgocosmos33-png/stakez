"""Build SceneCharacter BONUS idle v6: Scenario alpha + audio, no ping-pong.

Source: asset_mmvxxR2qWvKd3CxSawDxw27q (Pixelcut alpha VP9 + Opus).
Playback (FE): play full once, then SWAP to lady_idle_bonus_v9_loop
(last 1.0s ping-pong) — audio stays ON. See _build_lady_idle_bonus_v9_loop.py.

Run: python tools/_build_lady_idle_bonus_v6.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from _post_lady_idle_alpha import MIN_ISLAND, robust_copy, strip_detached_islands

APP = Path(__file__).resolve().parents[1]
SRC_DIR = APP / "assets-raw" / "lady_video" / "_bonus_v6_src"
RAW = APP / "assets-raw" / "lady_video"
STATIC = APP / "static" / "assets" / "sprites" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
QA = SRC_DIR / "qa"
FPS = 24
OUT_NAME = "lady_idle_bonus_v6.webm"
SRC_WEBM = SRC_DIR / "bonus_src.webm"


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd[:10])}...\n{result.stderr[-2500:]}")


def extract_rgba_frames(src: Path, frames_dir: Path) -> int:
    frames_dir.mkdir(parents=True, exist_ok=True)
    for p in frames_dir.glob("*.png"):
        p.unlink()
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-c:v", "libvpx-vp9", "-i", str(src),
            "-pix_fmt", "rgba",
            str(frames_dir / "f_%04d.png"),
        ]
    )
    paths = sorted(frames_dir.glob("f_*.png"))
    if not paths:
        raise RuntimeError(f"no frames extracted from {src}")
    return len(paths)


def scrub_frames(frames_dir: Path) -> int:
    total = 0
    for p in sorted(frames_dir.glob("f_*.png")):
        arr = np.array(Image.open(p).convert("RGBA"))
        cleaned, dropped = strip_detached_islands(arr)
        total += dropped
        Image.fromarray(cleaned).save(p)
    return total


def encode_alpha_webm_with_audio(frames_glob: str, audio_src: Path, out_webm: Path) -> None:
    out_webm.parent.mkdir(parents=True, exist_ok=True)
    # Video from scrubbed frames + original Opus audio (keeps bonus bed audible).
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", str(FPS),
            "-i", frames_glob,
            "-i", str(audio_src),
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "libvpx-vp9",
            "-pix_fmt", "yuva420p",
            "-b:v", "0",
            "-crf", "28",
            "-auto-alt-ref", "0",
            "-c:a", "libopus",
            "-b:a", "128k",
            "-shortest",
            str(out_webm),
        ]
    )


def qa_frame(webm: Path, ss: str, dest: Path) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-c:v", "libvpx-vp9", "-ss", ss, "-i", str(webm),
            "-frames:v", "1", "-pix_fmt", "rgba", str(dest),
        ]
    )
    a = np.array(Image.open(dest).convert("RGBA"))[..., 3]
    n, _, stats, _ = cv2.connectedComponentsWithStats((a > 24).astype(np.uint8), 8)
    extras = []
    if n > 1:
        main_i = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        extras = [
            int(stats[i, cv2.CC_STAT_AREA])
            for i in range(1, n)
            if i != main_i and int(stats[i, cv2.CC_STAT_AREA]) >= MIN_ISLAND
        ]
    return {
        "ss": ss,
        "frac0": float((a < 8).mean()),
        "opaque": float((a > 200).mean()),
        "extras": extras,
        "size_kb": webm.stat().st_size // 1024,
    }


def main() -> None:
    if not SRC_WEBM.exists():
        raise SystemExit(f"missing source: {SRC_WEBM}")

    work = Path(tempfile.mkdtemp(prefix="lady_bonus_v6_"))
    frames = work / "frames"
    print(f"[bonus_v6] extract {SRC_WEBM.name}", flush=True)
    n = extract_rgba_frames(SRC_WEBM, frames)
    print(f"[bonus_v6] frames={n}", flush=True)
    dropped = scrub_frames(frames)
    print(f"[bonus_v6] scrub dropped_island_px~{dropped}", flush=True)

    out_tmp = work / OUT_NAME
    encode_alpha_webm_with_audio(str(frames / "f_%04d.png"), SRC_WEBM, out_tmp)

    # Duration / streams proof
    probe = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "stream=codec_type,codec_name,pix_fmt",
            "-show_entries", "format=duration",
            "-of", "json",
            str(out_tmp),
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    meta = json.loads(probe)
    print(f"[bonus_v6] probe {meta}", flush=True)
    has_audio = any(s.get("codec_type") == "audio" for s in meta.get("streams", []))
    if not has_audio:
        raise SystemExit("bonus v6 encode missing audio stream")

    QA.mkdir(parents=True, exist_ok=True)
    for ss, tag in (("0.25", "start"), ("3.5", "mid"), ("6.5", "tail")):
        info = qa_frame(out_tmp, ss, QA / f"bonus_v6_{tag}.png")
        print(f"[bonus_v6] qa @{ss}s {info}", flush=True)
        if info["extras"]:
            raise SystemExit(f"floating islands remain @{ss}s: {info['extras']}")
        if info["frac0"] < 0.2:
            raise SystemExit(f"alpha key failed @{ss}s")

    # Install cache-busted name
    for dest_dir in (VITE, STATIC):
        robust_copy(out_tmp, dest_dir / OUT_NAME)
        print(f"[bonus_v6] installed {dest_dir / OUT_NAME}", flush=True)

    # Keep a raw copy next to sources
    robust_copy(out_tmp, RAW / OUT_NAME.replace(".webm", "_ship.webm"))

    note = SRC_DIR / "SOURCE_SCENARIO_BONUS_V6.txt"
    note.write_text(
        "Scenario bonus side character (freegame only)\n"
        "asset_id: asset_mmvxxR2qWvKd3CxSawDxw27q\n"
        "parent (img2video): asset_DkQXkEfQakceXJ9bqVxcFSkW\n"
        "Pixelcut ALPHA_MODE=1 VP9 + Opus audio kept.\n"
        f"shipped: sprites/scene/{OUT_NAME}\n"
        "FE: SceneCharacter play full once then SWAP to lady_idle_bonus_v9_loop.\n"
        "Basegame breath/move v5 sequencer unchanged.\n",
        encoding="utf-8",
    )
    print("[bonus_v6] DONE", flush=True)

    # cleanup frames
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
