"""Remove embedded audio tracks from every shipped video asset.

A slot game's sound must come from the audio sprite alone. Any audio baked into
a video file is inherited from the cloned game and plays the moment the video
element mounts, which no amount of sprite work can silence.

The video stream is copied bit-for-bit (-c:v copy -an), so this cannot change a
single rendered pixel. Only the audio track is dropped.

Run: python tools/strip_video_audio.py [--dry-run]
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
ROOTS = (APP / "static" / "assets", APP / "src" / "assets")
VIDEO_SUFFIXES = {".webm", ".mp4", ".mov", ".m4v"}


def audio_codecs(path: Path) -> list[str]:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=codec_name", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return [line for line in result.stdout.split() if line]


def video_signature(path: Path) -> str:
    """Codec + geometry + frame count, to prove the video stream is untouched."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
         "-show_entries", "stream=codec_name,width,height,nb_read_packets",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


def publish(staged: Path, dest: Path) -> None:
    """Replace dest even when OneDrive briefly locks the previous file."""
    last_error: Exception | None = None
    for attempt in range(8):
        try:
            staged.replace(dest)
            return
        except OSError as error:
            last_error = error
            try:
                shutil.copy2(staged, dest)
                staged.unlink(missing_ok=True)
                return
            except OSError as copy_error:
                last_error = copy_error
            time.sleep(0.4 * (attempt + 1))
    raise RuntimeError(f"could not publish {dest.name}: {last_error}")


def strip(path: Path) -> tuple[str, str]:
    before = video_signature(path)
    # stage beside the target: a temp dir can sit on another volume, and the
    # atomic replace only works within one
    staged = path.with_name(f"_stripping_{path.name}")
    try:
        result = subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(path),
             "-c:v", "copy", "-an", "-map", "0:v:0", str(staged)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"{path.name}: {result.stderr[-400:]}")
        after = video_signature(staged)
        if after != before:
            raise RuntimeError(f"{path.name}: video stream changed ({before} -> {after})")
        publish(staged, path)
    finally:
        staged.unlink(missing_ok=True)
    return before, after


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    targets: list[tuple[Path, list[str]]] = []
    for root in ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.suffix.lower() in VIDEO_SUFFIXES and path.is_file():
                codecs = audio_codecs(path)
                if codecs:
                    targets.append((path, codecs))

    if not targets:
        print("no shipped video carries an audio track — clean")
        return

    print(f"{len(targets)} video(s) carrying old-game audio:\n")
    for path, codecs in targets:
        label = str(path.relative_to(APP))
        if dry_run:
            print(f"  would strip [{','.join(codecs)}] {label}")
            continue
        before, _ = strip(path)
        remaining = audio_codecs(path)
        status = "clean" if not remaining else f"STILL HAS {remaining}"
        print(f"  stripped [{','.join(codecs)}] {label}  video={before}  -> {status}")

    if not dry_run:
        leftover = [
            str(path.relative_to(APP))
            for root in ROOTS if root.exists()
            for path in root.rglob("*")
            if path.suffix.lower() in VIDEO_SUFFIXES and path.is_file() and audio_codecs(path)
        ]
        print(f"\nvideos still carrying audio: {len(leftover)}")
        for label in leftover:
            print(f"  ! {label}")
        sys.exit(1 if leftover else 0)


if __name__ == "__main__":
    main()
