"""Confirm files, manifest, spine, and catalog agree."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import resolve_dest  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dest", type=Path, default=None)
    args = p.parse_args()
    dest = resolve_dest(args.dest)
    cat = json.loads((dest / "catalog.json").read_text(encoding="utf-8"))
    js = (dest / "catalog.js").read_text(encoding="utf-8")
    if not js.startswith("window.VFX_CATALOG"):
        raise SystemExit("catalog.js missing window.VFX_CATALOG")
    errors = 0
    for pack in cat["packs"]:
        parts = list((dest / pack["partsDir"]).glob("frame_*.png"))
        man = json.loads((dest / pack["partsDir"] / "manifest.json").read_text(encoding="utf-8"))
        spine = json.loads((dest / pack["spine"]).read_text(encoding="utf-8"))
        attach = spine["animations"]["play"]["slots"]["fx"]["attachment"]
        skins = spine["skins"]["default"]["fx"]
        n = len(parts)
        expected = [f"frame_{i:02d}" for i in range(1, n + 1)]
        attach_names = [key.get("name") for key in attach]
        spine_names_ok = attach_names == expected or (
            len(attach_names) == n + 1
            and attach_names[:n] == expected
            and attach_names[-1] == expected[-1]
        )
        times = [key.get("time") for key in attach]
        times_ok = (
            len(times) >= n
            and all(isinstance(t, (int, float)) for t in times)
            and all(times[i] <= times[i + 1] for i in range(len(times) - 1))
        )
        ok = (
            n == pack["frameCount"] == man["saved_count"] == len(skins)
            and spine_names_ok
            and times_ok
        )
        print(
            f"{pack['id']:28} files={n:2} cat={pack['frameCount']:2} "
            f"man={man['saved_count']:2} spine={len(attach):2} "
            f"skins={len(skins):2} peak={pack['peakFrame']}"
        )
        if not ok:
            errors += 1
            print("  COUNT MISMATCH")
            if not spine_names_ok:
                print("  SPINE ATTACHMENT NAMES", attach_names)
            if not times_ok:
                print("  SPINE ATTACHMENT TIMES", times)
        names = [f"frame_{i:02d}.png" for i in range(1, n + 1)]
        have = sorted(f.name for f in parts)
        if have != names:
            errors += 1
            print("  GAP OR BAD NAMES", have)
        leftover = [
            f.name
            for f in (dest / pack["partsDir"]).iterdir()
            if f.suffix == ".png" and not f.name.startswith("frame_")
        ]
        if leftover:
            errors += 1
            print("  leftover", leftover)
    if errors:
        raise SystemExit(f"{errors} pack(s) failed")
    print("all counts match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
