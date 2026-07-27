"""Mirror assets/ into static/assets/, which is what the dev server actually serves.

The app references art as root-relative URLs ('/assets/...'), so nothing is part
of Vite's module graph and Vite refuses to serve straight out of assets/ -- it is
outside the serving allow list. SvelteKit serves static/ instead, and static/assets
is a copy of assets/.

That copy is the trap this script exists for: regenerating art under assets/ has
NO effect on the running game until it is mirrored across, and the failure is
silent (the old art keeps loading) or a bare 403 for a brand-new file. Run this
after any tool that writes into assets/.

    python tools/sync_static_assets.py          # copy anything newer
    python tools/sync_static_assets.py --check  # just report what is stale
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "web-sdk/apps/white-room"
SRC = APP / "assets"
DST = APP / "static/assets"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    stale: list[Path] = []
    for path in SRC.rglob("*"):
        if not path.is_file():
            continue
        target = DST / path.relative_to(SRC)
        if (
            not target.exists()
            or target.stat().st_mtime < path.stat().st_mtime
            or target.stat().st_size != path.stat().st_size
        ):
            stale.append(path)

    for path in stale:
        target = DST / path.relative_to(SRC)
        print(f"{'stale' if args.check else 'sync '} {path.relative_to(SRC).as_posix()}")
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)

    print(f"{len(stale)} file(s) {'stale' if args.check else 'synced'}")


if __name__ == "__main__":
    main()
