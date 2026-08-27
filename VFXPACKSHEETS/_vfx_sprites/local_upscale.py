"""Local Real-ESRGAN NCNN Vulkan finish for audited pack frames.

Recraft replacement when LayerAI has no credits. RGB through the network,
ORIGINAL alpha restored with LANCZOS. Never black-key.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from edit_pack import load_manifest, rewrite_spine, write_manifest  # noqa: E402
from paths import resolve_dest  # noqa: E402
from rebuild_catalog import normalize_loop, rebuild  # noqa: E402

TOOLS = Path(r"C:\Users\Emex33\.cursor\skills\vfx-sprites\tools\realesrgan-ncnn-vulkan")
EXE = TOOLS / "realesrgan-ncnn-vulkan.exe"
MODELS = TOOLS / "models"
DEFAULT_MODEL = "realesr-animevideov3"
DEFAULT_SCALE = 2
GLOW_LUMA = 220


def find_exe() -> Path:
    raw = Path(os.environ.get("REALESRGAN_EXE", "")).expanduser()
    if raw.is_file():
        return raw
    if EXE.is_file():
        return EXE
    raise FileNotFoundError(
        f"realesrgan-ncnn-vulkan.exe missing at {EXE}. Re-extract the Windows zip."
    )


def list_frames(parts_dir: Path) -> list[Path]:
    frames = sorted(
        p
        for p in parts_dir.iterdir()
        if p.is_file() and p.suffix.lower() == ".png" and p.name.startswith("frame_")
    )
    if not frames:
        raise FileNotFoundError(f"No frame_*.png in {parts_dir}")
    return frames


def restore_alpha(orig_rgba: np.ndarray, up_rgb: np.ndarray) -> np.ndarray:
    h, w = up_rgb.shape[:2]
    alpha = np.asarray(
        Image.fromarray(orig_rgba[:, :, 3]).resize((w, h), Image.Resampling.LANCZOS)
    )
    luma = up_rgb.max(axis=2)
    outside = alpha == 0
    glow = outside & (luma >= GLOW_LUMA)
    alpha = np.where(
        glow,
        np.maximum(alpha, np.clip((luma - 180) * 2, 0, 255).astype(np.uint8)),
        alpha,
    )
    out = np.dstack([up_rgb, alpha])
    out[alpha == 0, :3] = 0
    return out


def verify_alpha(path: Path) -> None:
    arr = np.asarray(Image.open(path).convert("RGBA"))
    a = arr[:, :, 3]
    if a[0, 0] != 0 or a[0, -1] != 0 or a[-1, 0] != 0 or a[-1, -1] != 0:
        raise RuntimeError(f"{path.name}: corners must be transparent")
    if len(np.unique(a)) < 8:
        raise RuntimeError(f"{path.name}: alpha looks binary, not LANCZOS AA")
    if np.any(arr[a == 0, :3] != 0):
        raise RuntimeError(f"{path.name}: RGB must be 0 where alpha is 0")


def run_realesrgan(src_dir: Path, dst_dir: Path, model: str, scale: int) -> None:
    exe = find_exe()
    dst_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(exe),
        "-i",
        str(src_dir),
        "-o",
        str(dst_dir),
        "-n",
        model,
        "-s",
        str(scale),
        "-f",
        "png",
        "-m",
        str(MODELS),
    ]
    print(" ".join(cmd))
    proc = subprocess.run(cmd, cwd=str(TOOLS), capture_output=True, text=True)
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"realesrgan failed ({proc.returncode}): {err}")
    if proc.stdout:
        print(proc.stdout.strip())
    if proc.stderr:
        print(proc.stderr.strip())


def backup_frames(frames: list[Path], backup_dir: Path) -> None:
    backup_dir.mkdir(parents=True, exist_ok=True)
    for src in frames:
        dest = backup_dir / src.name
        if not dest.exists():
            shutil.copy2(src, dest)


def upscale_parts(
    parts_dir: Path,
    *,
    model: str = DEFAULT_MODEL,
    scale: int = DEFAULT_SCALE,
    backup_dir: Path | None = None,
) -> list[Path]:
    frames = list_frames(parts_dir)
    if backup_dir is not None:
        backup_frames(frames, backup_dir)

    work = parts_dir / "_esrgan_rgb"
    out_dir = parts_dir / "_esrgan_out"
    if work.exists():
        shutil.rmtree(work)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    work.mkdir()

    originals: dict[str, np.ndarray] = {}
    for src in frames:
        orig = np.asarray(Image.open(src).convert("RGBA"))
        originals[src.name] = orig
        rgb = orig[:, :, :3].copy()
        rgb[orig[:, :, 3] == 0] = 0
        Image.fromarray(rgb, "RGB").save(work / src.name)

    run_realesrgan(work, out_dir, model, scale)

    written: list[Path] = []
    for src in frames:
        up_path = out_dir / src.name
        if not up_path.is_file():
            raise FileNotFoundError(f"ESRGAN did not write {src.name}")
        up = np.asarray(Image.open(up_path).convert("RGB"))
        restored = restore_alpha(originals[src.name], up)
        Image.fromarray(restored, "RGBA").save(src)
        verify_alpha(src)
        written.append(src)
        print(f"  {src.name}  {originals[src.name].shape[1]}x{originals[src.name].shape[0]} -> {up.shape[1]}x{up.shape[0]}")

    shutil.rmtree(work, ignore_errors=True)
    shutil.rmtree(out_dir, ignore_errors=True)
    return written


def refresh_pack(pack_dir: Path, scale: int, model: str) -> None:
    man = load_manifest(pack_dir)
    parts_dir = pack_dir / "parts"
    records = list(man["parts"])
    for rec in records:
        path = parts_dir / rec["filename"]
        with Image.open(path) as im:
            rec["width"], rec["height"] = im.size
        rec["area"] = int(rec["width"]) * int(rec["height"])
    src = man.get("source_size") or {}
    if src.get("w") and src.get("h"):
        man["source_size"] = {"w": int(src["w"]) * scale, "h": int(src["h"]) * scale}
    man["upscale"] = {
        "tool": "realesrgan-ncnn-vulkan",
        "model": model,
        "scale": scale,
    }
    loop = normalize_loop(man, len(records))
    write_manifest(pack_dir, man, records, loop)
    rewrite_spine(pack_dir, man, records, loop)


def main() -> int:
    p = argparse.ArgumentParser(description="Local Real-ESRGAN finish for pack frames")
    p.add_argument("--dest", type=Path, default=None)
    p.add_argument("--slug", type=str, default="")
    p.add_argument("--parts", type=Path, default=None, help="Direct parts/ folder")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--scale", type=int, default=DEFAULT_SCALE, choices=(2, 3, 4))
    p.add_argument("--no-catalog", action="store_true")
    args = p.parse_args()

    find_exe()
    dest = None
    parts_dir: Path
    backup_dir = None
    pack_dir = None

    if args.parts is not None:
        parts_dir = Path(args.parts).resolve()
    else:
        if not args.slug:
            raise SystemExit("Need --slug with --dest, or --parts")
        dest = resolve_dest(args.dest)
        pack_dir = (dest / args.slug).resolve()
        parts_dir = pack_dir / "parts"
        backup_dir = dest / "_upscale_backup" / args.slug

    if not parts_dir.is_dir():
        raise SystemExit(f"Missing parts folder: {parts_dir}")

    print(f"exe {find_exe()}")
    print(f"parts {parts_dir}")
    upscale_parts(parts_dir, model=args.model, scale=args.scale, backup_dir=backup_dir)

    if pack_dir is not None and (pack_dir / "parts" / "manifest.json").is_file():
        refresh_pack(pack_dir, args.scale, args.model)
        if dest is not None and not args.no_catalog:
            rebuild(dest)
        print(f"rewrote Spine for {pack_dir.name}")

    print("local upscale done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
