"""Labeled contact sheet + size dump for visual audit."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import is_pack_dir, resolve_dest  # noqa: E402


def dump_sizes(dest: Path, slugs: list[str]) -> None:
    out = dest / "_review"
    out.mkdir(exist_ok=True)
    lines: list[str] = []
    for slug in slugs:
        man_path = dest / slug / "parts" / "manifest.json"
        if not man_path.is_file():
            continue
        data = json.loads(man_path.read_text(encoding="utf-8"))
        lines.append(f"==== {data.get('id', slug)} {data.get('saved_count')} ====")
        for part in data.get("parts", []):
            box = part.get("bbox", {})
            lines.append(
                f"  {part['filename']:12} {part['width']:4}x{part['height']:<4} "
                f"area={part['area']:6}  x={box.get('x')} y={box.get('y')} "
                f"w={box.get('w')} h={box.get('h')}"
            )
    (out / "sizes.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out / "sizes.txt")


def make_contact(dest: Path, slug: str) -> Path:
    frames = sorted((dest / slug / "parts").glob("frame_*.png"))
    if not frames:
        raise SystemExit(f"no frames in {slug}")
    thumbs = [(f.name, Image.open(f).convert("RGBA")) for f in frames]
    cell = 180
    cols = 8
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGBA", (cols * cell, rows * (cell + 22)), (12, 12, 14, 255))
    draw = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(thumbs):
        r, c = divmod(i, cols)
        x, y = c * cell, r * (cell + 22)
        canvas = Image.new("RGBA", (cell, cell), (8, 8, 10, 255))
        im.thumbnail((cell - 8, cell - 8), Image.Resampling.LANCZOS)
        ox = (cell - im.size[0]) // 2
        oy = (cell - im.size[1]) // 2
        canvas.paste(im, (ox, oy), im)
        sheet.paste(canvas, (x, y))
        draw.text((x + 4, y + cell + 2), name.replace(".png", ""), fill=(240, 180, 110, 255))
    out = dest / "_review"
    out.mkdir(exist_ok=True)
    dest_jpg = out / f"{slug}.jpg"
    sheet.convert("RGB").save(dest_jpg, quality=88)
    print(slug, len(thumbs), dest_jpg)
    return dest_jpg


def list_slugs(dest: Path, only: str | None) -> list[str]:
    if only:
        return [only]
    return [path.name for path in sorted(dest.iterdir()) if is_pack_dir(path)]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dest", type=Path, default=None)
    p.add_argument("--slug", default="")
    args = p.parse_args()
    dest = resolve_dest(args.dest)
    slugs = list_slugs(dest, args.slug or None)
    if not slugs:
        raise SystemExit("no packs found")
    for slug in slugs:
        make_contact(dest, slug)
    dump_sizes(dest, slugs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
