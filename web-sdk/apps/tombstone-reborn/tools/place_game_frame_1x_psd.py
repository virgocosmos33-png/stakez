"""Add GAME FRAME to the 1x (1342) western_scene2 document.

Does not touch Crystal 2684 western_scene2.psd.
Does not flatten street layers. Does not export a plate.
"""
from __future__ import annotations

import sys
from pathlib import Path

from psd_tools import PSDImage
from pytoshop import enums
from pytoshop.user.nested_layers import Group
from pytoshop.user.nested_layers import Image as PsdLayer
from pytoshop.user.nested_layers import nested_layers_to_psd

from place_game_frame_psd import (
	BOARD_FRAME,
	HUD_CHAIN,
	MULTI_BOX,
	MULTI_PALLET,
	WAYS_BOX,
	WAYS_PALLET,
	WIN_BOX,
	WIN_PALLET,
	channels_rgba,
	group,
	layout,
	pixel,
	write_psd,
)

DESK = Path.home() / "Desktop"
RAW = Path(__file__).resolve().parents[1] / "assets-raw" / "scene"
SRC_CANDIDATES = (
	DESK / "western_scene2.pre-crystal.psd",
	RAW / "western_scene2.pre-crystal.psd",
)
OUTS = (
	DESK / "western_scene2.1x.psd",
	DESK / "western_scene2.pre-crystal.psd",
	RAW / "western_scene2.1x.psd",
	RAW / "western_scene2.pre-crystal.psd",
)
CANVAS_W, CANVAS_H = 1342, 892
SCALE = CANVAS_W / 2684.0


def scale_seats() -> dict[str, tuple[float, float, float, float]]:
	seats = layout()
	return {name: (x * SCALE, y * SCALE, w * SCALE, h * SCALE) for name, (x, y, w, h) in seats.items()}


def convert_layer(layer):
	name = (layer.name or "").replace("\x00", "").strip()
	if name == "GAME FRAME":
		return None
	if layer.is_group():
		kids = [convert_layer(child) for child in layer]
		kids = [kid for kid in kids if kid is not None]
		return Group(name=name or "Group", visible=bool(layer.visible), closed=False, layers=kids)
	img = layer.topil()
	if img is None:
		img = layer.composite()
	if img is None:
		return None
	img = img.convert("RGBA")
	if img.width < 1 or img.height < 1:
		return None
	bbox = layer.bbox
	left = int(bbox[0]) if bbox else 0
	top = int(bbox[1]) if bbox else 0
	return PsdLayer(
		name=name or "Layer",
		visible=bool(layer.visible),
		left=left,
		top=top,
		channels=channels_rgba(img),
	)


def convert_street(src: Path) -> list:
	psd = PSDImage.open(src)
	layers = [convert_layer(layer) for layer in psd]
	return [layer for layer in layers if layer is not None]


def game_frame_group(seats: dict[str, tuple[float, float, float, float]]):
	return group(
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


def main() -> int:
	src = next((p for p in SRC_CANDIDATES if p.is_file()), None)
	if src is None:
		print("missing 1342 source PSD", file=sys.stderr)
		return 2
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
			print(f"missing sprite {need}", file=sys.stderr)
			return 2

	existing = convert_street(src)
	seats = scale_seats()
	psd = nested_layers_to_psd(
		existing + [game_frame_group(seats)],
		color_mode=enums.ColorMode.rgb,
		compression=enums.Compression.raw,
		size=(CANVAS_W, CANVAS_H),
	)
	written = []
	for out in OUTS:
		try:
			write_psd(out, psd)
			written.append(str(out))
			print(f"wrote {out}")
		except OSError as exc:
			print(f"blocked {out}: {exc}")
	print(f"canvas {CANVAS_W}x{CANVAS_H} scale={SCALE} src={src}")
	for name, (x, y, w, h) in seats.items():
		print(f"  {name:22s} {x:7.1f},{y:7.1f}  {w:7.1f}x{h:6.1f}")
	print("written", len(written))
	return 0 if written else 1


if __name__ == "__main__":
	raise SystemExit(main())
