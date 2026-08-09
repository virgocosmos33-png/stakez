"""Generate THE WHITE ROOM free-spin intro/outro panels via Scenario Imagen.

Outputs (processed to webp):
  mirror/fs_intro_mirror.webp           → THE_INTAKE
  mirror/fs_intro_mirror_otherside.webp → HER_SIDE
  mirror/fs_intro_mirror_bloodmoon.webp → WHITEOUT
  mirror/fs_outro_panel.webp            → YOU WON / TOTAL WIN clinical plaque

Run via DramaStudioMCP regenerate_assets scope=fsPanels.
"""
from __future__ import annotations

import os
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

HERE = Path(__file__).resolve().parent
MIRROR = HERE.parent / "static" / "assets" / "sprites" / "mirror"
MODEL = "model_imagen4-ultra"

JOBS = {
    "fs_intro_mirror.webp": (
        "Ornate white enamel and brushed silver observation-window plaque for free-spins intro, "
        "clinical asylum aesthetic, empty dark frosted oval centre for a spin count, "
        "THE INTAKE mood — cold fluorescent, no purple, no amethyst, no gold gothic, "
        "isolated on pure black, UI game asset, no text lettering"
    ),
    "fs_intro_mirror_otherside.webp": (
        "Matching white/silver observation-window plaque, HER SIDE mood — deeper shadows, "
        "faint dried-blood fleck on silver rim, empty dark frosted oval centre, "
        "isolated on pure black, no purple, no text"
    ),
    "fs_intro_mirror_bloodmoon.webp": (
        "Matching white/silver observation-window plaque, WHITEOUT mood — overexposed clinical "
        "flare, sparse dried-blood stains, empty dark frosted oval centre, isolated on pure black, "
        "no purple, no text"
    ),
    "fs_outro_panel.webp": (
        "Ornate white enamel and brushed silver YOU WON / TOTAL WIN panel plaque, titles "
        "baked as clinical stamped serif in silver (YOU WON above, TOTAL WIN below), empty "
        "centre band for runtime amount, padded-cell aesthetic, no purple, no amethyst, "
        "isolated on pure black"
    ),
}


def run_one(name: str, prompt: str) -> bool:
    res = s.request(
        "POST",
        f"/generate/custom/{MODEL}",
        {"prompt": prompt, "aspectRatio": "16:9"},
    )
    jid = (res.get("job") or res).get("jobId") or (res.get("job") or res).get("id")
    print(f"[fs-panels] {name} job {jid}", flush=True)
    for _ in range(100):
        time.sleep(2)
        st = s.request("GET", f"/jobs/{jid}")
        j = st.get("job", st)
        status = j.get("status")
        if status in ("success", "completed", "done"):
            url = None
            for a in j.get("assets") or []:
                if isinstance(a, dict) and a.get("url"):
                    url = a["url"]
                    break
            if not url:
                print(f"[fs-panels] no url: {j}", flush=True)
                return False
            raw = MIRROR / f"_{name}.png"
            urllib.request.urlretrieve(url, raw)
            img = Image.open(raw).convert("RGBA")
            # light black-key if solid bg
            out = MIRROR / name
            img.save(out, "WEBP", quality=90, method=6)
            print(f"[fs-panels] saved {out}", flush=True)
            return True
        if status in ("failure", "failed", "error"):
            print(f"[fs-panels] fail {j}", flush=True)
            return False
    return False


def main() -> int:
    MIRROR.mkdir(parents=True, exist_ok=True)
    force = os.environ.get("FORCE") == "1"
    rc = 0
    for name, prompt in JOBS.items():
        dest = MIRROR / name
        if dest.exists() and not force and dest.stat().st_mtime > time.time() - 3600:
            # still regenerate if FORCE; otherwise always replace Madam-era panels
            pass
        if not run_one(name, prompt):
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
