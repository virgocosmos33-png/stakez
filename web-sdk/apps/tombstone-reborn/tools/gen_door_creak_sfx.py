"""Generate lane-door SFX at the exact swing lengths in laneDoor.ts.

Reads the ElevenLabs key from repo-root elevenlabscrd.txt (never committed).
Writes sfx_door_creak.mp3 (open) and sfx_door_close.mp3 (close) into
static/assets/audio, assets/audio, and assets-src/assets/audio.

Open = LANE_DOOR_OPEN_MS (cubicOut: attack up front, settle at the end).
Close = LANE_DOOR_CLOSE_MS (linear shut + latch).
"""

from __future__ import annotations

import json
import shutil
import struct
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import wave
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
REPO = APP.parents[2]
LANE_DOOR = APP / "src" / "game" / "laneDoor.ts"
KEY_FILE = REPO / "elevenlabscrd.txt"
API = "https://api.elevenlabs.io/v1/sound-generation"
DESTS = [
    APP / "static" / "assets" / "audio",
    APP / "assets" / "audio",
    APP / "assets-src" / "assets" / "audio",
]
RAW = APP / "assets-raw" / "audio_gen"

OPEN_PROMPT = (
    "A heavy riveted wooden plank door swinging open on rusty iron hinges. "
    "Sound starts on the first sample: sharp wood-and-iron latch release, "
    "then a continuous mid hinge groan that fades and settles as the door "
    "finishes opening. Dry western saloon, close microphone, no music, "
    "no voices, no slam, no leftover tail after the door is open."
)
CLOSE_PROMPT = (
    "A heavy riveted wooden plank door swinging shut on rusty iron hinges. "
    "Continuous short hinge creak that ends on a solid wood-on-frame latch "
    "thud. Dry western saloon, close microphone, no music, no voices. "
    "The whole action is one short shut, no leftover tail."
)


def lane_ms(name: str) -> int:
    text = LANE_DOOR.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith(f"export const {name}"):
            return int(line.split("=")[1].strip().rstrip(";"))
    raise SystemExit(f"{name} missing in {LANE_DOOR}")


def api_key() -> str:
    if not KEY_FILE.exists():
        raise SystemExit(f"missing {KEY_FILE}")
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    if not key.startswith("sk_"):
        raise SystemExit("elevenlabscrd.txt does not look like an ElevenLabs key")
    return key


def generate_pcm(key: str, text: str, duration_s: float) -> bytes:
    payload = json.dumps(
        {
            "text": text,
            "duration_seconds": duration_s,
            "prompt_influence": 0.75,
            "model_id": "eleven_text_to_sound_v2",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{API}?output_format=pcm_44100",
        data=payload,
        headers={"xi-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as res:
            return res.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"ElevenLabs {exc.code}: {body}") from exc


def pcm_to_wav(pcm: bytes, wav_path: Path) -> None:
    with wave.open(str(wav_path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(44100)
        wav.writeframes(pcm)


def rms_blocks(pcm: bytes, sr: int = 44100, block_ms: int = 20) -> list[float]:
    step = int(sr * block_ms / 1000) * 2
    out: list[float] = []
    for i in range(0, len(pcm) - 1, step):
        chunk = pcm[i : i + step]
        if len(chunk) < 4:
            break
        samples = struct.unpack("<" + "h" * (len(chunk) // 2), chunk[: len(chunk) // 2 * 2])
        mean = sum(s * s for s in samples) / len(samples)
        out.append(mean**0.5)
    return out


def score_open(pcm: bytes) -> float:
    blocks = rms_blocks(pcm)
    if len(blocks) < 6:
        return -1.0
    peak = max(blocks) or 1.0
    norm = [b / peak for b in blocks]
    head = sum(norm[:3]) / 3
    tail = sum(norm[-3:]) / 3
    return head - tail - (0.4 if norm[0] < 0.08 else 0.0)


def trim_or_pad_wav(src: Path, dest: Path, duration_s: float, *, keep_end: bool = False) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    # keep_end: reverse → take the new head → reverse, so the latch thud stays.
    filt = (
        f"areverse,atrim=0:{duration_s:.6f},areverse,apad=pad_dur={duration_s:.6f},atrim=0:{duration_s:.6f}"
        if keep_end
        else f"atrim=0:{duration_s:.6f},apad=pad_dur={duration_s:.6f},atrim=0:{duration_s:.6f}"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-af",
            filt,
            "-ar",
            "44100",
            "-ac",
            "1",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(dest),
        ],
        check=True,
        capture_output=True,
    )


def write_all(src: Path, name: str) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, RAW / name)
    for dest_dir in DESTS:
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / name)


def probe_seconds(path: Path) -> float:
    raw = subprocess.run(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(json.loads(raw.stdout)["format"]["duration"])


def main() -> None:
    open_ms = lane_ms("LANE_DOOR_OPEN_MS")
    close_ms = lane_ms("LANE_DOOR_CLOSE_MS")
    open_s = open_ms / 1000
    close_s = close_ms / 1000
    key = api_key()
    only_close = "--close-only" in sys.argv
    print(f"open={open_ms}ms close={close_ms}ms", flush=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        if not only_close:
            best_pcm = b""
            best_score = -1e9
            for i in range(3):
                print(f"generating open candidate {i + 1}/3...", flush=True)
                pcm = generate_pcm(key, OPEN_PROMPT, max(0.5, open_s))
                score = score_open(pcm)
                print(f"  score={score:.3f} bytes={len(pcm)}", flush=True)
                if score > best_score:
                    best_score = score
                    best_pcm = pcm
            if not best_pcm:
                raise SystemExit("no open candidates")
            open_wav = tmp_path / "open.wav"
            pcm_to_wav(best_pcm, open_wav)
            open_mp3 = tmp_path / "sfx_door_creak.mp3"
            trim_or_pad_wav(open_wav, open_mp3, open_s)
            write_all(open_mp3, "sfx_door_creak.mp3")

        print("generating close...", flush=True)
        close_pcm = generate_pcm(key, CLOSE_PROMPT, max(0.5, close_s))
        close_wav = tmp_path / "close.wav"
        pcm_to_wav(close_pcm, close_wav)
        close_mp3 = tmp_path / "sfx_door_close.mp3"
        trim_or_pad_wav(close_wav, close_mp3, close_s, keep_end=True)
        write_all(close_mp3, "sfx_door_close.mp3")

    print(f"open file {probe_seconds(DESTS[0] / 'sfx_door_creak.mp3'):.3f}s", flush=True)
    print(f"close file {probe_seconds(DESTS[0] / 'sfx_door_close.mp3'):.3f}s", flush=True)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.stderr.write((exc.stderr or b"").decode("utf-8", errors="replace"))
        raise
