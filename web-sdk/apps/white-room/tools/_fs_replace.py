"""OneDrive-safe replace helpers for Windows file locks."""
from __future__ import annotations

import shutil
import time
from pathlib import Path


def replace_file(src: Path, dst: Path, retries: int = 8) -> None:
    """Copy src -> dst with unlink retries (OneDrive / antivirus locks)."""
    src = Path(src)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(dst.suffix + f".tmp{int(time.time() * 1000)}")
    shutil.copy2(src, tmp)
    last: Exception | None = None
    for i in range(retries):
        try:
            if dst.exists():
                try:
                    dst.unlink()
                except OSError:
                    # try replace over locked file via os.replace after rename
                    pass
            tmp.replace(dst)
            return
        except OSError as exc:
            last = exc
            time.sleep(0.25 * (i + 1))
    # last resort: copy into place
    try:
        shutil.copy2(tmp, dst)
        tmp.unlink(missing_ok=True)
        return
    except OSError:
        tmp.unlink(missing_ok=True)
        raise last or OSError(f"failed to replace {dst}")


def save_bytes(data: bytes, dst: Path, retries: int = 8) -> None:
    dst = Path(dst)
    tmp = dst.with_suffix(dst.suffix + f".tmp{int(time.time() * 1000)}")
    tmp.write_bytes(data)
    replace_file(tmp, dst, retries=retries)
    tmp.unlink(missing_ok=True)
