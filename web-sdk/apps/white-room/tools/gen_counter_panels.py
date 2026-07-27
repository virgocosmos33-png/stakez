"""Generate on-theme accents for the WAYS / FREE SPINS counters.

Reads THE WHITE ROOM (or current) game config via GAME_CONFIG for palette/theme.
Default art direction: white/silver clinical observation-glass — NOT Madam Mirror
amethyst/purple gothic.

Usage:
  python gen_counter_panels.py texture
  python gen_counter_panels.py corner
  python gen_counter_panels.py frame_ways
  python gen_counter_panels.py frame_fs
  python gen_counter_panels.py all
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import scenario_api as sc

HERE = Path(__file__).resolve().parent
RAW = HERE.parents[3] / "qa-shots" / "creatives"
RAW.mkdir(parents=True, exist_ok=True)

GEN_DIR = Path(
    os.environ.get(
        "COUNTER_FRAME_SRC",
        Path.home()
        / ".cursor"
        / "projects"
        / "c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios"
        / "assets",
    )
)
GEN_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "model_imagen4-ultra"


def _load_theme() -> dict:
    cfg_path = os.environ.get("GAME_CONFIG", "")
    theme = {
        "game": os.environ.get("GAME_NAME", "THE WHITE ROOM"),
        "palette": "bone white #f4f1ec, silver #c8c4bc, steel #8a8680, charcoal #3a3632, faint dried blood #6b2a28",
        "mood": "sterile, haunted, clinical dread",
        "style": "psychological-horror asylum isolation cell, white/silver ornate clinical frame",
    }
    if cfg_path and Path(cfg_path).is_file():
        try:
            cfg = json.loads(Path(cfg_path).read_text(encoding="utf-8"))
            pc = cfg.get("promptContext") or {}
            idn = cfg.get("identity") or {}
            theme["game"] = idn.get("workingName") or idn.get("gameName") or theme["game"]
            if pc.get("palette"):
                theme["palette"] = ", ".join(pc["palette"]) if isinstance(pc["palette"], list) else str(pc["palette"])
            if pc.get("mood"):
                theme["mood"] = pc["mood"]
            if pc.get("style") or pc.get("theme"):
                theme["style"] = pc.get("style") or pc.get("theme")
        except Exception as exc:  # noqa: BLE001
            print(f"warn: could not read GAME_CONFIG: {exc}", flush=True)
    return theme


def _jobs() -> dict:
    t = _load_theme()
    neg = (
        "NO purple, NO violet, NO amethyst, NO gold gothic, NO neon, "
        "no text, no lettering, no watermark, no UI buttons"
    )
    return {
        "texture": {
            "prompt": (
                f"Frosted clinical observation-glass texture for slot game \"{t['game']}\", "
                f"theme: {t['style']}, mood: {t['mood']}, palette: {t['palette']}. "
                "Faint hairline cracks and condensation on pale frosted glass, subtle "
                "institutional grime, soft fluorescent highlight, symmetrical centred motif "
                "fading to near-black at edges, high detail, no border frame. "
                f"{neg}"
            ),
            "aspectRatio": "1:1",
            "out": "counter_texture.png",
            "outdir": RAW,
        },
        "corner": {
            "prompt": (
                f"A single ornate corner ornament of polished antique white enamel and "
                f"brushed silver filigree for \"{t['game']}\", clinical asylum aesthetic, "
                f"palette: {t['palette']}, faint dried-blood fleck only if subtle, "
                "top-left corner piece, isolated on pure solid black background, sharp "
                f"studio lighting, metallic, high detail. {neg}"
            ),
            "aspectRatio": "1:1",
            "out": "counter_corner.png",
            "outdir": RAW,
        },
        "frame_ways": {
            "prompt": (
                f"Ornate horizontal UI counter frame plaque for ways-to-win display in "
                f"slot game \"{t['game']}\". White enamel and brushed silver antique "
                f"filigree, clinical asylum observation-window aesthetic, mood: {t['mood']}. "
                "Empty dark frosted-glass rectangular window in the centre for digits, "
                "NO gems that are purple, NO amethyst, NO gold, silver rivets and thin "
                "steel straps, faint dried-blood stain optional, isolated on PURE SOLID "
                f"BLACK background, symmetrical, high detail game UI asset. {neg}"
            ),
            "aspectRatio": "16:9",
            "out": "ways_frame_gen.png",
            "outdir": GEN_DIR,
        },
        "frame_fs": {
            "prompt": (
                f"Ornate horizontal UI counter frame plaque for free-spins display in "
                f"slot game \"{t['game']}\". Matching white enamel and brushed silver "
                f"filigree family as the ways frame, clinical observation-window look, "
                f"mood: {t['mood']}. Empty dark frosted-glass window centre, isolated on "
                f"PURE SOLID BLACK background, symmetrical, high detail. {neg}"
            ),
            "aspectRatio": "16:9",
            "out": "fs_frame_gen.png",
            "outdir": GEN_DIR,
        },
    }


def start_job(spec: dict) -> str:
    payload = {
        "prompt": spec["prompt"],
        "aspectRatio": spec["aspectRatio"],
    }
    res = sc.request("POST", f"/generate/custom/{MODEL}", payload)
    job = res.get("job", res)
    job_id = job.get("jobId") or job.get("id")
    cost = job.get("billing", {}).get("cuCost")
    print(f"job {job_id} started (cuCost={cost})", flush=True)
    return job_id


def run(name: str) -> int:
    jobs = _jobs()
    if name not in jobs:
        print(f"unknown job {name}; choose from {list(jobs)}", flush=True)
        return 2
    spec = jobs[name]
    out_probe = Path(spec["outdir"]) / spec["out"]
    # MCP path: Scenario model_run may already have written masters — skip rebill.
    if out_probe.is_file() and not (os.environ.get("FORCE_REGEN") or "").strip():
        print(f"{name}: skip gen — master already present: {out_probe}", flush=True)
        return 0
    job_id = start_job(spec)
    started = time.time()
    while True:
        job = sc.request("GET", f"/jobs/{job_id}")
        j = job.get("job", job)
        status = j.get("status")
        if status in ("success", "completed", "done"):
            break
        if status in ("failure", "failed", "error", "canceled", "cancelled"):
            print(f"{name}: FAILED {j}", flush=True)
            return 1
        if time.time() - started > 300:
            print(f"{name}: timeout", flush=True)
            return 1
        time.sleep(2)

    assets = j.get("assets") or j.get("output") or []
    if isinstance(assets, dict):
        assets = assets.get("assets") or []
    url = None
    for a in assets:
        if isinstance(a, dict):
            url = a.get("url") or a.get("downloadUrl") or a.get("src")
            if url:
                break
        elif isinstance(a, str) and a.startswith("http"):
            url = a
            break
    if not url:
        # Scenario sometimes nests under generations
        gens = j.get("generations") or []
        for g in gens:
            if isinstance(g, dict):
                url = g.get("url") or g.get("asset", {}).get("url")
                if url:
                    break
    if not url:
        print(f"{name}: no asset url in {j}", flush=True)
        return 1

    outdir = Path(spec["outdir"])
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / spec["out"]
    data = sc.download(url) if hasattr(sc, "download") else None
    if data is None:
        import urllib.request

        urllib.request.urlretrieve(url, out)
    else:
        out.write_bytes(data)
    print(f"{name}: saved {out}", flush=True)
    return 0


def main(argv: list[str]) -> int:
    which = (argv[1] if len(argv) > 1 else "all").lower()
    jobs = _jobs()
    order = list(jobs) if which == "all" else [which]
    # MCP pipeline invokes with no args — frames only (texture/corner are optional accents).
    if len(argv) <= 1:
        order = ["frame_ways", "frame_fs"]
    rc = 0
    for name in order:
        rc = run(name) or rc
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
