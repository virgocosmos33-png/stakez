"""A-Z live SFX via ElevenLabs sound-generation.

Reads tools/sfx_revamp_spec.json and repo-root elevenlabscrd.txt.
Never prints the key. Never overwrites door cues.
Sub-500ms cues are generated at 0.5s then trimmed. Loops use loop=true.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
REPO = APP.parents[2]
KEY_FILE = REPO / "elevenlabscrd.txt"
SPEC_PATH = Path(__file__).resolve().parent / "sfx_revamp_spec.json"
API = "https://api.elevenlabs.io/v1/sound-generation"
DESTS = [
    APP / "static" / "assets" / "audio",
    APP / "assets" / "audio",
    APP / "assets-src" / "assets" / "audio",
]
RAW = APP / "assets-raw" / "audio_gen"
DOOR = {"sfx_door_creak", "sfx_door_close"}


def api_key() -> str:
    if not KEY_FILE.exists():
        raise SystemExit(f"missing {KEY_FILE}")
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    if not key.startswith("sk_"):
        raise SystemExit("elevenlabscrd.txt does not look like an ElevenLabs key")
    return key


def load_spec() -> dict:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def all_cues(spec: dict, family: str | None, only: str | None) -> list[tuple[str, dict]]:
    out: list[tuple[str, dict]] = []
    for fam, cues in spec["families"].items():
        if family and fam != family:
            continue
        for cue in cues:
            if only and cue["name"] != only:
                continue
            out.append((fam, cue))
    return out


def generate_pcm(key: str, text: str, duration_s: float, *, loop: bool) -> bytes:
    body: dict = {
        "text": text,
        "duration_seconds": duration_s,
        "prompt_influence": 0.75,
        "model_id": "eleven_text_to_sound_v2",
    }
    if loop:
        body["loop"] = True
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{API}?output_format=pcm_44100",
        data=payload,
        headers={"xi-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    last_err = ""
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as res:
                return res.read()
        except urllib.error.HTTPError as exc:
            last_err = exc.read().decode("utf-8", errors="replace")
            if exc.code in {429, 500, 502, 503} and attempt < 4:
                wait = 8 * (2**attempt)
                print(f"  HTTP {exc.code}, retry in {wait}s", flush=True)
                time.sleep(wait)
                continue
            raise SystemExit(f"ElevenLabs {exc.code}: {last_err}") from exc
        except urllib.error.URLError as exc:
            last_err = str(exc)
            if attempt < 4:
                time.sleep(8 * (2**attempt))
                continue
            raise SystemExit(f"ElevenLabs network: {last_err}") from exc
    raise SystemExit(f"ElevenLabs failed: {last_err}")


def pcm_to_wav(pcm: bytes, wav_path: Path) -> None:
    with wave.open(str(wav_path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(44100)
        wav.writeframes(pcm)


def trim_or_pad_wav(src: Path, dest: Path, duration_s: float) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    filt = f"atrim=0:{duration_s:.6f},apad=pad_dur={duration_s:.6f},atrim=0:{duration_s:.6f}"
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


def dest_mp3(name: str) -> Path:
    return DESTS[0] / f"{name}.mp3"


def verify(spec: dict) -> int:
    skip = set(spec.get("skip", [])) | DOOR
    bad = 0
    for fam, cues in spec["families"].items():
        for cue in cues:
            name = cue["name"]
            path = dest_mp3(name)
            want = cue["duration_ms"] / 1000
            if not path.exists():
                print(f"MISSING {fam}/{name}")
                bad += 1
                continue
            got = probe_seconds(path)
            delta = abs(got - want)
            mark = "OK" if delta <= 0.04 else "LEN"
            if mark != "OK":
                bad += 1
            print(f"{mark:3} {fam}/{name:24} want={want:.3f}s got={got:.3f}s")
    for name in skip:
        if name in DOOR and dest_mp3(name).exists():
            print(f"OK  door/{name:24} kept {probe_seconds(dest_mp3(name)):.3f}s")
    return bad


def generate_one(key: str, spec: dict, cue: dict) -> None:
    name = cue["name"]
    if name in DOOR or name in spec.get("skip", []):
        print(f"skip {name}", flush=True)
        return
    want_s = cue["duration_ms"] / 1000
    loop = bool(cue.get("loop"))
    text = f"{cue['prompt']} {spec['shared_suffix']} Lasts {want_s:.3f}s."
    if len(text) > 450:
        raise SystemExit(f"{name} prompt is {len(text)} chars (max 450)")
    gen_s = max(0.5, want_s)
    print(f"gen {name} {want_s:.3f}s loop={loop} ...", flush=True)
    pcm = generate_pcm(key, text, gen_s, loop=loop)
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / f"{name}.wav"
        mp3 = Path(tmp) / f"{name}.mp3"
        pcm_to_wav(pcm, wav)
        trim_or_pad_wav(wav, mp3, want_s)
        write_all(mp3, f"{name}.mp3")
    print(f"  wrote {probe_seconds(dest_mp3(name)):.3f}s", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=["knives", "guns", "board", "lane", "fire", "bonus"])
    parser.add_argument("--only")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    spec = load_spec()
    if args.verify:
        bad = verify(spec)
        raise SystemExit(1 if bad else 0)

    key = api_key()
    cues = all_cues(spec, args.family, args.only)
    if not cues:
        raise SystemExit("no cues matched")
    for i, (fam, cue) in enumerate(cues, 1):
        name = cue["name"]
        path = dest_mp3(name)
        if name in DOOR or name in spec.get("skip", []):
            print(f"[{i}/{len(cues)}] skip {fam}/{name}", flush=True)
            continue
        if path.exists() and args.skip_existing and not args.force:
            print(f"[{i}/{len(cues)}] exists {fam}/{name}", flush=True)
            continue
        print(f"[{i}/{len(cues)}] {fam}/{name}", flush=True)
        generate_one(key, spec, cue)
        time.sleep(0.8)
    bad = verify(spec) if not args.family and not args.only else 0
    if args.family or args.only:
        print("family pass done; run --verify after all families", flush=True)
    elif bad:
        raise SystemExit(f"verify failed: {bad} cues")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.stderr.write((exc.stderr or b"").decode("utf-8", errors="replace"))
        raise
