<script lang="ts">
	/**
	 * Weathered western reel frame — ONE baked transparent PNG, laid from the
	 * plank sheet piece by piece (tools/make_board_frame_image.py). Pre-shaped
	 * to the authored staircase. The inside is transparent so the saloon shows
	 * through while the reels spin.
	 *
	 * Per-cell iron slot borders sit behind the cards. The baked ring is
	 * authored geometry (holds still if a reel grows). The container follows
	 * boardLayout scale/pivot so the timber stays locked to the cards.
	 */
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { CELL_PITCH_X, SYMBOL_SIZE, NUM_ROWS, MAX_ROWS } from '../game/constants';
	import { getCellLeft, getReelWindow, getReelRows } from '../game/utils';
	import ReelChains from './ReelChains.svelte';

	const context = getContext();
	const frameKey = $derived(
		context.stateGame.atmosphere === 'super'
			? 'boardFrameSuper'
			: context.stateGame.atmosphere === 'small'
				? 'boardFrameSmall'
				: 'boardFrame',
	);

	/** MUST match BORDER + MARGIN in tools/make_board_frame_image.py */
	const BORDER = 30 + 60;

	type Column = { left: number; right: number; top: number; bottom: number };

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

	const slots = $derived.by(() =>
		columns.flatMap((col, reel) => {
			// Last reel is the door lid — the iron slot under it is the grey
			// strip that shows through every seam in the swing.
			if (reel === columns.length - 1) return [];
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

	const layout = $derived(context.stateGameDerived.boardLayout());
</script>

<Container zIndex={1} x={layout.x} y={layout.y} pivot={layout.pivot} scale={layout.scale}>
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

	<ReelChains />

	<Sprite
		key={frameKey}
		x={frameBox.x}
		y={frameBox.y}
		width={frameBox.w}
		height={frameBox.h}
	/>
</Container>
