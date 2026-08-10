from pathlib import Path

jp = Path(__file__).with_name("scenario_sfx_prompts.json")
raw = jp.read_bytes()
for enc in ("utf-8", "cp1252", "latin-1"):
    try:
        text = raw.decode(enc)
        break
    except UnicodeDecodeError:
        continue
else:
    raise SystemExit("cannot decode prompts json")

replacements = {
    "\u2014": "-",
    "\u2013": "-",
    "\u201c": '"',
    "\u201d": '"',
    "\u2019": "'",
    "\u2026": "...",
    "\x97": "-",
    "\x96": "-",
    "\x93": '"',
    "\x94": '"',
    "\x91": "'",
    "\x92": "'",
    "\x85": "...",
}
for src, dst in replacements.items():
    text = text.replace(src, dst)

jp.write_text(text, encoding="utf-8")
import json

data = json.loads(jp.read_text(encoding="utf-8"))
print("ok", {k: len(v) if isinstance(v, dict) else v for k, v in data.items()})
