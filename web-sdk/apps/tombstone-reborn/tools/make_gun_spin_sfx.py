"""Synthesize a short revolver-twirl whoosh for Gunsmoke.

Writes sfx_gun_spin.wav / .mp3 into assets-src/audio and static/assets/audio.
"""

from __future__ import annotations

import math
import os
import struct
import subprocess
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
OUT_DIRS = [
	os.path.join(APP, "assets-src", "audio"),
	os.path.join(APP, "static", "assets", "audio"),
]

RATE = 44100
DURATION = 0.38
NAME = "sfx_gun_spin"


def clamp(value: float) -> int:
	return max(-32767, min(32767, int(value * 32767)))


def synth() -> list[float]:
	n = int(RATE * DURATION)
	samples = [0.0] * n
	# deterministic noise
	seed = 1_234_567
	noise = [0.0] * n
	for i in range(n):
		seed = (seed * 1664525 + 1013904223) & 0xFFFFFFFF
		noise[i] = (seed / 0xFFFFFFFF) * 2.0 - 1.0

	# whoosh: rising then falling band-limited noise
	state = 0.0
	for i in range(n):
		t = i / n
		env = (t / 0.12) if t < 0.12 else max(0.0, (1.0 - t) / 0.72)
		env = min(1.0, env) ** 1.15
		cutoff = 0.08 + 0.42 * (1.0 - abs(t - 0.28) * 1.8)
		cutoff = max(0.04, min(0.55, cutoff))
		state += cutoff * (noise[i] - state)
		samples[i] += state * env * 0.72

	# metallic ratchet clicks as the cylinder spins
	clicks = (0.04, 0.10, 0.16, 0.22, 0.28)
	for index, start in enumerate(clicks):
		freq = 2100 + index * 180
		length = int(RATE * 0.028)
		origin = int(start * RATE)
		for k in range(length):
			if origin + k >= n:
				break
			life = 1.0 - k / length
			tone = math.sin(2 * math.pi * freq * k / RATE) * life * life
			click = tone * (0.22 if index % 2 == 0 else 0.16)
			samples[origin + k] += click

	peak = max(0.001, max(abs(s) for s in samples))
	return [s / peak * 0.92 for s in samples]


def write_wav(path: str, samples: list[float]) -> None:
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with wave.open(path, "w") as handle:
		handle.setnchannels(1)
		handle.setsampwidth(2)
		handle.setframerate(RATE)
		handle.writeframes(b"".join(struct.pack("<h", clamp(s)) for s in samples))


def maybe_mp3(wav_path: str, mp3_path: str) -> bool:
	ffmpeg = os.environ.get("FFMPEG", "ffmpeg")
	try:
		subprocess.run(
			[ffmpeg, "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-q:a", "4", mp3_path],
			check=True,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
		)
		return True
	except (OSError, subprocess.CalledProcessError):
		return False


def main() -> None:
	samples = synth()
	made_mp3 = False
	for folder in OUT_DIRS:
		os.makedirs(folder, exist_ok=True)
		wav_path = os.path.join(folder, f"{NAME}.wav")
		mp3_path = os.path.join(folder, f"{NAME}.mp3")
		write_wav(wav_path, samples)
		print(f"wrote {wav_path}")
		if maybe_mp3(wav_path, mp3_path):
			made_mp3 = True
			print(f"wrote {mp3_path}")
	if not made_mp3:
		print("ffmpeg not available — playing the wav")


if __name__ == "__main__":
	main()
