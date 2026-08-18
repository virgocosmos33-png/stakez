"""Copy static/assets → assets so Vite `new URL('../../assets/...')` resolves.

Storybook and `vite dev` resolve those URLs from apps/tombstone-reborn/assets,
not from static/. After a main pull, new files often land only under static/.
Missing files abort the Vite module graph and Storybook stays on loading.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "static" / "assets"
DST = ROOT / "assets"


def main() -> None:
    if not SRC.is_dir():
        raise SystemExit(f"missing source {SRC}")
    copied = 0
    skipped = 0
    for src in SRC.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(SRC)
        dst = DST / rel
        if dst.exists() and dst.stat().st_size == src.stat().st_size:
            skipped += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1
        print(f"copied {rel}")
    print(f"done copied={copied} already={skipped}")


if __name__ == "__main__":
    main()
