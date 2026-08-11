<script lang="ts">
	/**
	 * Weathered western reel frame.
	 *
	 *   - boardFrame       ONE baked transparent PNG, pre-shaped to the AUTHORED
	 *                      staircase (tools/make_board_frame_image.py): grey
	 *                      timber ring with bevels, keylines, iron bolts and the
	 *                      shadow it casts inward. Placed 1:1 at the authored
	 *                      outer box — nothing is cut or masked at runtime.
	 *                      Re-bake the PNG whenever the board shape changes.
	 *   - (no field)       the inside of the frame is TRANSPARENT by design —
	 *                      the graveyard scene shows through between the cards
	 *                      while they spin.
	 *   - boardSlotFrame   a thin iron slot border drawn in EVERY visible cell
	 *                      (behind the card) so the board reads as a grid of
	 *                      framed slots. Tiles flush at CELL_PITCH_X × row pitch,
	 *                      so neighbouring borders meet instead of doubling up.
	 *
	 * GEOMETRY IS FROZEN: cell rects, CELL_PITCH_X, SYMBOL_SIZE and the per-reel
	 * windows (getCellLeft/getReelWindow) are unchanged — a parallel feature
	 * traces fire around this exact geometry, so only the ART changed.
	 */
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { CELL_PITCH_X, SYMBOL_SIZE, NUM_ROWS, MAX_ROWS } from '../game/constants';
	import { getCellLeft, getReelWindow, getReelRows } from '../game/utils';

	const context = getContext();

	/** MUST match BORDER + MARGIN in tools/make_board_frame_image.py — the frame
	 * canvas carries an extra margin for the plank ends / chains that overflow
	 * past the frame line, so the sprite is anchored that much further out.
	 * (The frame art itself is GENERATED over the exact staircase stencil — see
	 * tools/_gen_frame_guide.py + tools/wire_generated_frame.py.) */
	const BORDER = 30 + 60;

	type Column = { left: number; right: number; top: number; bottom: number };

	/** LIVE columns — follow wild-reel growth / stretch, for the slot grid */
	const columns = $derived.by(() =>
		context.stateGame.board.map((_, reel): Column => {
			const window = getReelWindow(reel);
			return {
				left: getCellLeft(reel),
				right: getCellLeft(reel) + CELL_PITCH_X,
				top: window.top,
				bottom: window.bottom,
			};
		}),
	);

	/**
	 * AUTHORED outer box of the baked frame PNG (board-local units). Mirrors the
	 * bake tool: reels centred on MAX_ROWS, except the LAST reel which centres on
	 * its left neighbour (utils.getReelYOffset special lane rule). Never reads
	 * live state, so the frame holds still while reels grow.
	 */
	const frameBox = (() => {
		const tops = NUM_ROWS.map((rows, i) => {
			if (i === NUM_ROWS.length - 1) {
				const neighbor = NUM_ROWS[i - 1] ?? rows;
				return ((MAX_ROWS - neighbor) / 2 + (neighbor - rows) / 2) * SYMBOL_SIZE;
			}
			return ((MAX_ROWS - rows) / 2) * SYMBOL_SIZE;
		});
		const bottoms = tops.map((top, i) => top + NUM_ROWS[i] * SYMBOL_SIZE);
		const x = getCellLeft(0) - BORDER;
		const y = Math.min(...tops) - BORDER;
		return {
			x,
			y,
			w: getCellLeft(NUM_ROWS.length - 1) + CELL_PITCH_X + BORDER - x,
			h: Math.max(...bottoms) + BORDER - y,
		};
	})();

	/** one slot per VISIBLE cell. Row pitch is the reel window / row count, so a
	 * stretched (racked) reel's slots spread with its symbols. */
	const slots = $derived.by(() =>
		columns.flatMap((col, reel) => {
			const rows = getReelRows(reel);
			if (rows <= 0) return [];
			const pitch = (col.bottom - col.top) / rows;
			return Array.from({ length: rows }, (_, r) => ({
				key: `${reel}:${r}`,
				cx: col.left + CELL_PITCH_X / 2,
				cy: col.top + (r + 0.5) * pitch,
				h: pitch,
			}));
		}),
	);
</script>

<Container
	x={context.stateGameDerived.boardLayout().x -
		context.stateGameDerived.boardLayout().width * 0.5}
	y={context.stateGameDerived.boardLayout().y -
		context.stateGameDerived.boardLayout().height * 0.5}
>
	<!-- NO field under the symbols: the inside of the frame is TRANSPARENT, so
		the graveyard scene shows through between the cards while they spin. -->

	<!-- per-cell slot border, behind the cards; tiles flush so the board reads as
		a grid of framed slots -->
	{#each slots as slot (slot.key)}
		<Sprite
			key="boardSlotFrame"
			x={slot.cx}
			y={slot.cy}
			anchor={0.5}
			width={CELL_PITCH_X}
			height={slot.h}
		/>
	{/each}

	<!-- the baked, pre-shaped transparent frame, placed 1:1 (never cut) -->
	<Sprite
		key="boardFrame"
		x={frameBox.x}
		y={frameBox.y}
		width={frameBox.w}
		height={frameBox.h}
	/>
</Container>
