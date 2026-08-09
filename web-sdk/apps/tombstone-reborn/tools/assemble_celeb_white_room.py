"""Assemble UNIQUE White Room celebration stills+mp4s from Scenario masters.

Used when Scenario generate is rate-limited. Masters live in
tools/scenario_out/celeb_wr_masters/ (downloaded via Scenario MCP asset_download).

Writes:
  static/assets/sprites/celeb/celeb_tN.webp          (panel + game posters)
  static/assets/sprites/celeb/celeb_tN/celeb_tN.mp4  (game anim paths)
  static/assets/sprites/celeb/celeb_tN.mp4            (runtime roots)
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _fs_replace import replace_file  # noqa: E402

MASTERS = HERE / "scenario_out" / "celeb_wr_masters"
CELEB = HERE.parent / "static" / "assets" / "sprites" / "celeb"
W, H = 1280, 720


def md5(p: Path) -> str:
    h = hashlib.md5()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def fit(img: Image.Image, size=(W, H)) -> Image.Image:
    return ImageOps.fit(img.convert("RGB"), size, Image.Resampling.LANCZOS)


def overlay(base: Image.Image, over: Image.Image, alpha: float, box=None) -> Image.Image:
    out = base.copy()
    o = over.convert("RGBA")
    if box:
        o = o.resize((box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
        layer = Image.new("RGBA", out.size, (0, 0, 0, 0))
        layer.paste(o, (box[0], box[1]), o if o.mode == "RGBA" else None)
        out = Image.alpha_composite(out.convert("RGBA"), layer).convert("RGB")
    else:
        o = fit(o).convert("RGBA")
        a = o.split()[-1].point(lambda p: int(p * alpha))
        o.putalpha(a)
        out = Image.alpha_composite(out.convert("RGBA"), o).convert("RGB")
    return out


def save_webp(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".webp.tmpwrite")
    img.save(tmp, "WEBP", quality=90, method=6)
    replace_file(tmp, path)
    tmp.unlink(missing_ok=True)


def ffmpeg_from_still(still: Path, out_mp4: Path, vf: str, seconds: float = 5.0) -> None:
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", str(still),
        "-vf", vf,
        "-t", str(seconds), "-r", "24",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def main() -> int:
    need = [
        "cell_padded.png", "patient404_room.png", "graffiti_room.png",
        "straitjacket.png", "memory_dissolve.png",
        "patient404_face.png", "empty_chair.mp4",
        "glass_shards.png",
    ]
    missing = [n for n in need if not (MASTERS / n).is_file()]
    if missing:
        raise SystemExit(f"missing masters: {missing} — download via Scenario MCP first")

    cell = fit(Image.open(MASTERS / "cell_padded.png"))
    p404 = fit(Image.open(MASTERS / "patient404_room.png"))
    graffiti = fit(Image.open(MASTERS / "graffiti_room.png"))
    jacket = fit(Image.open(MASTERS / "straitjacket.png"))
    dissolve = fit(Image.open(MASTERS / "memory_dissolve.png"))
    face = fit(Image.open(MASTERS / "patient404_face.png"))
    shards = fit(Image.open(MASTERS / "glass_shards.png"))

    # Unique clinical stills (no gothic / no green mist)
    base3 = ImageEnhance.Color(cell).enhance(0.2)
    stills = {
        2: ImageEnhance.Brightness(ImageEnhance.Contrast(p404).enhance(1.2)).enhance(1.35),  # fluorescent intake
        3: overlay(base3, face, 0.9, (W // 5, H // 10, 4 * W // 5, 9 * H // 10)),  # Patient 404
        4: Image.blend(
            ImageEnhance.Brightness(ImageEnhance.Color(cell).enhance(0.25)).enhance(1.2),
            shards,
            0.55,
        ),  # observation glass shatter over padded cell (no ornate frame)
        5: Image.blend(graffiti, ImageEnhance.Brightness(jacket).enhance(0.35), 0.25),  # Her Side
        6: Image.blend(ImageEnhance.Color(cell).enhance(0.2), dissolve, 0.7),  # Memory Reset
        7: ImageEnhance.Color(
            ImageEnhance.Brightness(ImageEnhance.Contrast(cell).enhance(0.85)).enhance(1.85)
        ).enhance(0.15),  # padded whiteout (bright, not clipped)
    }

    posters = {}
    for n, img in stills.items():
        still_png = CELEB / f"celeb_t{n}" / f"celeb_t{n}_still.png"
        still_png.parent.mkdir(parents=True, exist_ok=True)
        img.save(still_png, "PNG")
        webp = CELEB / f"celeb_t{n}.webp"
        save_webp(img, webp)
        posters[n] = still_png
        print(f"[assemble] still t{n} -> {webp.name} md5={md5(webp)[:8]}", flush=True)

    # Unique motion per tier (clinical, not gothic)
    motion = {
        2: "scale=1280:720,eq=brightness='0.25*sin(8*PI*t)':contrast=1.2,format=yuv420p",  # fluorescent strobe
        3: "scale=8000:-1,zoompan=z='min(zoom+0.0015,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=120:s=1280x720:fps=24,eq=contrast=1.1",
        4: "scale=1280:720,eq=brightness='0.15*gt(sin(12*PI*t)\\,0.7)':saturation=0.2,format=yuv420p",  # shatter flashes
        6: "scale=1280:720,eq=brightness='0.05+0.15*t':contrast='1.1+0.1*t':saturation=0.25,format=yuv420p",  # memory dissolve
        7: "scale=1280:720,eq=brightness='min(1\\,0.2+0.25*t)':contrast=0.7,format=yuv420p",  # whiteout bloom
    }

    # t5: use Scenario Seedance empty-chair master (already unique clinical video)
    t5_src = MASTERS / "empty_chair.mp4"
    t5_dir = CELEB / "celeb_t5" / "celeb_t5.mp4"
    replace_file(t5_src, t5_dir)
    replace_file(t5_src, CELEB / "celeb_t5.mp4")
    # refresh poster from video frame 0
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(t5_src), "-frames:v", "1", str(CELEB / "celeb_t5" / "_frame.png")],
        check=True, capture_output=True,
    )
    frame = fit(Image.open(CELEB / "celeb_t5" / "_frame.png"))
    save_webp(frame, CELEB / "celeb_t5.webp")
    (CELEB / "celeb_t5" / "_frame.png").unlink(missing_ok=True)
    print(f"[assemble] video t5 Seedance empty_chair md5={md5(t5_dir)[:8]}", flush=True)

    hashes = {5: md5(t5_dir)}
    for n, vf in motion.items():
        out = CELEB / f"celeb_t{n}" / f"celeb_t{n}.mp4"
        ffmpeg_from_still(posters[n], out, vf)
        replace_file(out, CELEB / f"celeb_t{n}.mp4")
        hashes[n] = md5(out)
        print(f"[assemble] video t{n} md5={hashes[n][:8]} size={out.stat().st_size}", flush=True)

    # Prove uniqueness — no duplicated whiteout paste
    uniq = set(hashes.values())
    if len(uniq) != 6:
        raise SystemExit(f"NOT unique videos: {hashes}")
    wo = CELEB / "celeb_whiteout.mp4"
    if wo.is_file():
        woh = md5(wo)
        if woh in uniq:
            raise SystemExit("a tier still matches celeb_whiteout — abort")

    # Panel poster uniqueness
    webp_hashes = {n: md5(CELEB / f"celeb_t{n}.webp") for n in range(2, 8)}
    if len(set(webp_hashes.values())) != 6:
        raise SystemExit(f"NOT unique posters: {webp_hashes}")

    print("[assemble] OK — 6 unique clinical celebrations wired", flush=True)
    for n in range(2, 8):
        print(f"  t{n} webp={webp_hashes[n][:10]} mp4={hashes[n][:10]}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
