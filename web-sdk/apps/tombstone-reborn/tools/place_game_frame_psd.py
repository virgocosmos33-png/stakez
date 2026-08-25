"""Place live GAME FRAME sprites into western_scene2.psd as movable layers.

Does not flatten the street, does not export a plate, does not rewrite game code.
Uses the same pytoshop size tuple as write_crystal_psd: (width, height).
"""
from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np
from PIL import Image
from pytoshop import PsdFile, enums
from pytoshop.user.nested_layers import Group
from pytoshop.user.nested_layers import Image as PsdLayer
from pytoshop.user.nested_layers import nested_layers_to_psd, psd_to_nested_layers

from export_western_scene2 import PSD_NAME, RAW

DESK = Path.home() / "Desktop" / PSD_NAME
CANVAS_W, CANVAS_H = 2684, 1784
SPRITES = Path(__file__).resolve().parents[1] / "assets" / "sprites"

# Live base-atmosphere files (HudReadout / BoardPlate / BoardHangChains).
BOARD_FRAME = SPRITES / "board" / "board_frame.png"
WAYS_BOX = SPRITES / "tombstone" / "wood_readout_ways.png"
MULTI_BOX = SPRITES / "tombstone" / "wood_readout_multi.png"
WIN_BOX = SPRITES / "tombstone" / "wood_readout_win.png"
WAYS_PALLET = SPRITES / "tombstone" / "wood_pallet_ways.png"
MULTI_PALLET = SPRITES / "tombstone" / "wood_pallet_multi.png"
WIN_PALLET = SPRITES / "tombstone" / "wood_pallet_win.png"
HUD_CHAIN = SPRITES / "tombstone" / "hud_chain.png"


def channels_rgba(im: Image.Image) -> dict[int, np.ndarray]:
	arr = np.asarray(im.convert("RGBA"))
	return {0: arr[:, :, 0], 1: arr[:, :, 1], 2: arr[:, :, 2], -1: arr[:, :, 3]}


def fit_rgba(path: Path, w: float, h: float) -> Image.Image:
	im = Image.open(path).convert("RGBA")
	tw = max(1, int(round(w)))
	th = max(1, int(round(h)))
	if im.size == (tw, th):
		return im
	return im.resize((tw, th), Image.Resampling.LANCZOS)


def pixel(name: str, path: Path, left: float, top: float, w: float, h: float) -> PsdLayer:
	im = fit_rgba(path, w, h)
	return PsdLayer(
		name=name,
		visible=True,
		left=int(round(left)),
		top=int(round(top)),
		channels=channels_rgba(im),
	)


def group(name: str, layers: list) -> Group:
	return Group(name=name, visible=True, closed=False, layers=layers)


def layout() -> dict[str, tuple[float, float, float, float]]:
	"""Scene-pixel seats from live boardLayout + SpecialBar + HudReadout math.

	Assumes the PSD canvas is the cover-fit scene (2684x1784) over desktop main
	(1422x800). Starting seat only — user will move/scale in Photoshop.
	"""
	num_rows = [3, 4, 4, 2, 2, 1]
	max_rows = 4
	side_h_scale = max_rows * 1.15 * 0.78
	side_w_scale = side_h_scale * 355 / 1505
	symbol = int(800 / ((6 + 1) * 0.8 + side_w_scale))
	pitch = symbol * 0.8
	pad = 0.53
	col_off = (pad - 0.5) * pitch
	board_w = pitch * 6
	board_h = symbol * max_rows
	frame_outer = 48
	border = 30 + 60

	def cell_left(reel: int) -> float:
		return pitch * (reel + pad) - pitch / 2

	def reel_top(i: int) -> float:
		rows = num_rows[i]
		if i == len(num_rows) - 1:
			neighbor = num_rows[i - 1]
			return ((max_rows - neighbor) / 2 + (neighbor - rows) / 2) * symbol
		return ((max_rows - rows) / 2) * symbol

	tops = [reel_top(i) for i in range(6)]
	bots = [tops[i] + num_rows[i] * symbol for i in range(6)]
	content_top = min(tops) - frame_outer
	content_bot = max(bots) + frame_outer

	scene_w, scene_h = CANVAS_W, CANVAS_H
	main_w, main_h = 1422.0, 800.0
	main_scale = min(scene_w / main_w, scene_h / main_h)
	hook_y = 148.0

	def scene_to_main(sx: float, sy: float) -> tuple[float, float]:
		return (
			main_w / 2 + (sx - scene_w / 2) / main_scale,
			main_h / 2 + (sy - scene_h / 2) / main_scale,
		)

	def main_to_scene(mx: float, my: float) -> tuple[float, float]:
		return (
			scene_w / 2 + (mx - main_w / 2) * main_scale,
			scene_h / 2 + (my - main_h / 2) * main_scale,
		)

	beam_main = scene_to_main(scene_w * 0.5, hook_y)[1]
	hang_ceiling = max(20.0, beam_main + 38.0)
	floor_y = main_h - 120.0
	available = max(1.0, floor_y - hang_ceiling)
	live_h = max(1.0, content_bot - content_top)
	live_w = board_w + frame_outer * 2
	board_scale = min(available / live_h, max(0.2, main_w / live_w)) * 0.85
	pivot_x, pivot_y = board_w / 2, board_h / 2
	board_x = main_w * 0.5 - col_off
	board_y = hang_ceiling - (content_top - pivot_y) * board_scale
	visual_bot = board_y + (content_bot - pivot_y) * board_scale
	if visual_bot > floor_y:
		board_y -= visual_bot - floor_y

	def board_to_main(lx: float, ly: float) -> tuple[float, float]:
		return (
			board_x + (lx - pivot_x) * board_scale,
			board_y + (ly - pivot_y) * board_scale,
		)

	def box(l: float, t: float, r: float, b: float) -> tuple[float, float, float, float]:
		x0, y0 = main_to_scene(*board_to_main(l, t))
		x1, y1 = main_to_scene(*board_to_main(r, b))
		return (x0, y0, x1 - x0, y1 - y0)

	fx = cell_left(0) - border
	fy = min(tops) - border
	fw = cell_left(5) + pitch + border - fx
	fh = max(bots) + border - fy

	seats: dict[str, tuple[float, float, float, float]] = {
		"board_frame": box(fx, fy, fx + fw, fy + fh),
	}

	notch_l = cell_left(3)
	notch_r = cell_left(4) + pitch
	short_top = reel_top(3)
	short_bot = short_top + 2 * symbol
	lip_main = board_to_main((notch_l + notch_r) / 2, short_bot + 28)[1]
	hang_cx_main = board_to_main((cell_left(4) + cell_left(5) + pitch) / 2, 0)[0]
	pocket_w = (notch_r - notch_l) * board_scale
	well_w = max(196.0, min(pocket_w * 0.74, 248.0))
	block_h = well_w / 1.6
	screen_top = (0 - scene_h / 2) / main_scale + main_h / 2
	pocket_bot = board_to_main((notch_l + notch_r) / 2, short_top)[1] - 6
	hang_y_main = min(screen_top + 40 + block_h * 0.5, pocket_bot - block_h * 0.45)
	gap = well_w * -0.16
	ways_cx = hang_cx_main - (well_w + gap) / 2
	multi_cx = hang_cx_main + (well_w + gap) / 2
	win_y_main = lip_main + 28 + block_h * 0.5
	win_cx = ways_cx

	def plaque(
		cx_main: float,
		cy_main: float,
		pallet_path: Path,
		key_box: str,
		key_pal: str,
		chain_from_scene: float | None = None,
	) -> None:
		cx, cy = main_to_scene(cx_main, cy_main)
		sw = well_w * main_scale
		sh = block_h * main_scale
		seats[key_box] = (cx - sw / 2, cy - sh / 2, sw, sh)
		aspect = Image.open(pallet_path).size
		pal_aspect = aspect[1] / aspect[0]
		pw = sw * 1.02
		ph = min(sh * 0.2, pw * pal_aspect)
		py = cy - sh / 2 + (112 / 400) * sh
		seats[key_pal] = (cx - pw / 2, py - ph / 2, pw, ph)
		inset = sw * 0.22
		col_w = max(7 * main_scale, min(sw * 0.07, 11 * main_scale))
		chain_bot = py - ph * 0.38
		min_h = col_w * (288 / 56) * 0.55
		if chain_from_scene is None:
			chain_top = max(70.0, min(hook_y, chain_bot - min_h))
		else:
			chain_top = min(chain_from_scene, chain_bot - min_h)
		drop = max(min_h, chain_bot - chain_top)
		prefix = key_box.split("_")[0]
		seats[f"chain_{prefix}_l"] = (cx - inset - col_w / 2, chain_top, col_w, drop)
		seats[f"chain_{prefix}_r"] = (cx + inset - col_w / 2, chain_top, col_w, drop)

	plaque(ways_cx, hang_y_main, WAYS_PALLET, "ways_box", "ways_pallet")
	plaque(multi_cx, hang_y_main, MULTI_PALLET, "multi_box", "multi_pallet")
	lip_scene = main_to_scene(win_cx, lip_main)[1]
	plaque(win_cx, win_y_main, WIN_PALLET, "win_box", "win_pallet", chain_from_scene=lip_scene)

	col_w_local = 9 / board_scale
	chain_aspect = 288 / 56
	hook_main = beam_main
	hook_local = pivot_y + (hook_main - board_y) / board_scale
	into = 6 / board_scale
	min_drop = 18 / board_scale
	step_i = 0
	step_top = tops[0]
	for i in range(1, 6):
		if tops[i] > step_top + 0.5:
			step_i = i
			step_top = tops[i - 1]
			break
	corners = [
		("chain_board_far_left", cell_left(0) + 10, tops[0]),
		("chain_board_step", cell_left(step_i) + 8, step_top),
		("chain_board_far_right", cell_left(5) + pitch - 10, tops[5]),
	]
	for name, lx, timber_y in corners:
		top_l = min(hook_local, timber_y - min_drop)
		bot_l = timber_y + into
		drop_l = max(col_w_local * chain_aspect * 0.55, bot_l - top_l)
		x0, y0 = main_to_scene(*board_to_main(lx - col_w_local / 2, top_l))
		x1, y1 = main_to_scene(*board_to_main(lx + col_w_local / 2, top_l + drop_l))
		seats[name] = (x0, y0, x1 - x0, y1 - y0)

	return seats


def strip_game_frame(layers: list) -> list:
	return [layer for layer in layers if getattr(layer, "name", "") != "GAME FRAME"]


def materialize(layers: list) -> None:
	"""Copy lazy PSD channel pixels into numpy so the source file can close."""
	for layer in layers:
		if isinstance(layer, Group):
			materialize(layer.layers)
			continue
		if not isinstance(layer, PsdLayer):
			continue
		fresh: dict[int, np.ndarray] = {}
		for key, ch in layer.channels.items():
			img = getattr(ch, "image", ch)
			fresh[int(key)] = np.array(img, copy=True)
		layer.channels = fresh


def write_psd(path: Path, psd) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	tmp = path.with_suffix(".psd.tmp")
	with tmp.open("wb") as fh:
		psd.write(fh)
	try:
		tmp.replace(path)
	except OSError:
		shutil.copy2(tmp, path)
		tmp.unlink(missing_ok=True)


def main() -> None:
	src = DESK if DESK.is_file() else (RAW / PSD_NAME)
	if not src.is_file():
		raise SystemExit(f"missing {src}")
	for need in (
		BOARD_FRAME,
		WAYS_BOX,
		MULTI_BOX,
		WIN_BOX,
		WAYS_PALLET,
		MULTI_PALLET,
		WIN_PALLET,
		HUD_CHAIN,
	):
		if not need.is_file():
			raise SystemExit(f"missing sprite {need}")

	with src.open("rb") as fh:
		existing = psd_to_nested_layers(PsdFile.read(fh))
		existing = strip_game_frame(existing)
		materialize(existing)
	seats = layout()

	game_frame = group(
		"GAME FRAME",
		[
			group(
				"CHAINS",
				[
					pixel("chain_board_far_left", HUD_CHAIN, *seats["chain_board_far_left"]),
					pixel("chain_board_step", HUD_CHAIN, *seats["chain_board_step"]),
					pixel("chain_board_far_right", HUD_CHAIN, *seats["chain_board_far_right"]),
					pixel("chain_ways_l", HUD_CHAIN, *seats["chain_ways_l"]),
					pixel("chain_ways_r", HUD_CHAIN, *seats["chain_ways_r"]),
					pixel("chain_multi_l", HUD_CHAIN, *seats["chain_multi_l"]),
					pixel("chain_multi_r", HUD_CHAIN, *seats["chain_multi_r"]),
					pixel("chain_win_l", HUD_CHAIN, *seats["chain_win_l"]),
					pixel("chain_win_r", HUD_CHAIN, *seats["chain_win_r"]),
				],
			),
			group("BOARD", [pixel("board_frame", BOARD_FRAME, *seats["board_frame"])]),
			group(
				"WAYS",
				[
					pixel("ways_box", WAYS_BOX, *seats["ways_box"]),
					pixel("ways_pallet", WAYS_PALLET, *seats["ways_pallet"]),
				],
			),
			group(
				"MULTI",
				[
					pixel("multi_box", MULTI_BOX, *seats["multi_box"]),
					pixel("multi_pallet", MULTI_PALLET, *seats["multi_pallet"]),
				],
			),
			group(
				"WIN",
				[
					pixel("win_box", WIN_BOX, *seats["win_box"]),
					pixel("win_pallet", WIN_PALLET, *seats["win_pallet"]),
				],
			),
		],
	)

	psd = nested_layers_to_psd(
		existing + [game_frame],
		color_mode=enums.ColorMode.rgb,
		compression=enums.Compression.raw,
		size=(CANVAS_W, CANVAS_H),
	)
	raw_psd = RAW / PSD_NAME
	write_psd(raw_psd, psd)
	desk_ok = True
	try:
		write_psd(DESK, psd)
	except OSError as exc:
		desk_ok = False
		print(f"Desktop write blocked ({exc}); wrote {raw_psd} only")
	print(f"canvas {CANVAS_W}x{CANVAS_H}")
	print(f"raw {raw_psd}")
	print(f"desk {DESK} ok={desk_ok}")
	for name, (x, y, w, h) in seats.items():
		print(f"  {name:22s} {x:7.1f},{y:7.1f}  {w:7.1f}x{h:6.1f}")


if __name__ == "__main__":
	main()
