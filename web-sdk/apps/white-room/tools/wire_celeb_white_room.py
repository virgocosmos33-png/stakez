"""Wire White Room celebration mp4s into assets.ts load paths.

Copies celeb/celeb_tN/celeb_tN.mp4 -> celeb/celeb_tN.mp4 (runtime root)
and extracts a poster webp still from frame 0 when ffmpeg is available.

Run via DramaStudioMCP regenerate_assets scope=celebration.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _fs_replace import replace_file  # noqa: E402

HERE = Path(__file__).resolve().parent
# Panel serves static/; Vite FE loads assets/ — keep both in sync.
CELEB_STATIC = HERE.parent / "static" / "assets" / "sprites" / "celeb"
CELEB_ASSETS = HERE.parent / "assets" / "sprites" / "celeb"
TIERS = list(range(2, 8))


def extract_poster(mp4: Path, webp: Path) -> bool:
    try:
        png = webp.with_suffix(".png")
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(mp4), "-frames:v", "1", "-q:v", "2", str(png)],
            check=True,
            capture_output=True,
        )
        if png.exists():
            from PIL import Image

            tmp = webp.with_suffix(".webp.tmpwrite")
            Image.open(png).convert("RGB").save(tmp, "WEBP", quality=88, method=6)
            png.unlink(missing_ok=True)
            replace_file(tmp, webp)
            tmp.unlink(missing_ok=True)
            return True
    except Exception as exc:  # noqa: BLE001
        print(f"[wire-celeb] poster skip {mp4.name}: {exc}", flush=True)
    return False


def sync_tree(src_root: Path, dst_root: Path) -> None:
    """Mirror celebration tree into Vite assets/ load path."""
    import shutil

    dst_root.mkdir(parents=True, exist_ok=True)
    for n in TIERS:
        for name in (
            f"celeb_t{n}.mp4",
            f"celeb_t{n}.webp",
        ):
            src = src_root / name
            if src.is_file():
                dst = dst_root / name
                shutil.copy2(src, dst)
                print(f"[wire-celeb] assets sync {name} ({dst.stat().st_size})", flush=True)
        folder = f"celeb_t{n}"
        src_dir = src_root / folder
        if src_dir.is_dir():
            dst_dir = dst_root / folder
            dst_dir.mkdir(parents=True, exist_ok=True)
            for child in src_dir.iterdir():
                if child.is_file():
                    shutil.copy2(child, dst_dir / child.name)


def main() -> int:
    CELEB = CELEB_STATIC
    CELEB.mkdir(parents=True, exist_ok=True)
    for n in TIERS:
        src = CELEB / f"celeb_t{n}" / f"celeb_t{n}.mp4"
        dst = CELEB / f"celeb_t{n}.mp4"
        if not src.is_file():
            print(f"[wire-celeb] MISSING {src}", flush=True)
            continue
        # Cover-crop: encode full-bleed 1280x720 (scale+crop) so Seedance letterbox never ships.
        cover = CELEB / f"celeb_t{n}" / f"celeb_t{n}_cover.mp4"
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(src),
                    "-vf",
                    "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1",
                    "-an",
                    "-c:v",
                    "libx264",
                    "-pix_fmt",
                    "yuv420p",
                    "-crf",
                    "18",
                    "-movflags",
                    "+faststart",
                    str(cover),
                ],
                check=True,
                capture_output=True,
            )
            replace_file(cover, src)
            cover.unlink(missing_ok=True)
            print(f"[wire-celeb] cover-crop {src.name}", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"[wire-celeb] cover-crop skip t{n}: {exc}", flush=True)
        replace_file(src, dst)
        print(f"[wire-celeb] copied {src.name} -> {dst.name} ({dst.stat().st_size})", flush=True)
        webp = CELEB / f"celeb_t{n}.webp"
        # Prefer assembled clinical still if present; only overwrite when missing.
        still = CELEB / f"celeb_t{n}" / f"celeb_t{n}_still.png"
        if still.is_file():
            from PIL import Image, ImageOps

            tmp = webp.with_suffix(".webp.tmpwrite")
            ImageOps.fit(Image.open(still).convert("RGB"), (1280, 720), Image.Resampling.LANCZOS).save(
                tmp, "WEBP", quality=90, method=6
            )
            replace_file(tmp, webp)
            tmp.unlink(missing_ok=True)
            print(f"[wire-celeb] poster from still {webp.name}", flush=True)
        elif extract_poster(dst, webp):
            print(f"[wire-celeb] poster {webp.name}", flush=True)
    sync_tree(CELEB_STATIC, CELEB_ASSETS)
    print("[wire-celeb] done", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
