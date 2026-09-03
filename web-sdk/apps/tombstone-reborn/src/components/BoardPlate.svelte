<script lang="ts">
	/**
	 * One timber ring: backgroundSPINE MAIN_FRAME, seated in scene cover-fit
	 * like the plate. Cards live in the hole and draw ON TOP of this chrome
	 * (BOARD_REELS_Z > BOARD_TIMBER_Z). Spine MAIN_FRAME stays hidden so this
	 * ring is the only copy.
	 */
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { BOARD_TIMBER_Z, CELL_PITCH_X } from '../game/constants';
	import { FRAME_SEATS } from '../game/frameSeats.generated';
	import { sceneToMain } from '../game/saloonLamps';
	import { stateShake } from '../game/stateShake.svelte';
	import { getCellLeft, getReelWindow, getReelRows } from '../game/utils';

	type Props = { layer?: 'back' | 'ring' };
	const props: Props = $props();
	const layer = $derived(props.layer ?? 'back');

	const context = getContext();
	const frameKey = 'boardFrame';

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

	const layout = $derived(context.stateGameDerived.boardLayout());

	const timber = $derived.by(() => {
		const main = context.stateLayoutDerived.mainLayout();
		const canvas = context.stateLayoutDerived.canvasSizes();
		const seat = FRAME_SEATS.board;
		const tl = sceneToMain(seat.left, seat.top, canvas, main);
		const br = sceneToMain(seat.right, seat.bottom, canvas, main);
		return {
			x: tl.x,
			y: tl.y,
			w: Math.max(1, br.x - tl.x),
			h: Math.max(1, br.y - tl.y),
		};
	});
</script>

{#if layer === 'back'}
	<Container
		zIndex={0}
		x={layout.x + stateShake.x}
		y={layout.y + stateShake.y}
		pivot={layout.pivot}
		scale={layout.scale}
	>
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
	</Container>
{:else}
	<Container zIndex={BOARD_TIMBER_Z}>
		<Sprite
			key={frameKey}
			x={timber.x + stateShake.x}
			y={timber.y + stateShake.y}
			width={timber.w}
			height={timber.h}
		/>
	</Container>
{/if}
