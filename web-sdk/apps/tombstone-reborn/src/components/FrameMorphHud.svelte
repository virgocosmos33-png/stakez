<script lang="ts" module>
	export type EmitterEventFrameMorphHud =
		| { type: 'waysCounterUpdate'; ways: number }
		| { type: 'waysCounterHide' }
		| { type: 'freeSpinCounterShow' }
		| { type: 'freeSpinCounterHide' }
		| { type: 'freeSpinCounterUpdate'; current?: number; total?: number }
		| { type: 'winMultUpdate'; value: number };
</script>

<script lang="ts">
	/**
	 * Narrow-layout WAYS / WIN fallback — the same stacked nameplates SpecialBar
	 * draws on the right, laid in a row under the board when the special bar
	 * is flat. The vertical decision is shared (game/specialBarLayout.ts) so
	 * exactly one place shows them. When the side rail stands, this component
	 * renders nothing.
	 */
	import { MainContainer } from 'components-layout';
	import { Container } from 'pixi-svelte';
	import { stateBet, stateUi } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import HudReadout from './HudReadout.svelte';
	import { getContext } from '../game/context';
	import config from '../game/config';
	import { BOARD_PLATE_PAD } from '../game/constants';
	import { COLUMN_ROW_OFFSET } from '../game/chassisArt';
	import { isSpecialBarVertical } from '../game/specialBarLayout';
	import { stateShake } from '../game/stateShake.svelte';
	import { formatWays } from '../game/waysFormat';

	const context = getContext();

	/** air between BoardPlate bottom lip and the cluster */
	const PLATE_CLEAR = 14;
	const PLAQUE_ASPECT = 1.6;

	const BASE_WAYS = config.numRows.reduce((total, rows) => total * rows, 1);
	let ways = $state(BASE_WAYS);
	let spinsShow = $state(false);
	let spinsCurrent = $state(0);
	let spinsTotal = $state(0);
	let winMult = $state(1);

	context.eventEmitter.subscribeOnMount({
		waysCounterUpdate: (e) => {
			ways = e.ways;
		},
		waysCounterHide: () => {
			ways = BASE_WAYS;
		},
		freeSpinCounterShow: () => {
			spinsShow = true;
		},
		freeSpinCounterHide: () => {
			spinsShow = false;
		},
		freeSpinCounterUpdate: (e) => {
			if (e.current !== undefined) spinsCurrent = e.current;
			if (e.total !== undefined) spinsTotal = e.total;
		},
		winMultUpdate: (e) => {
			winMult = Math.max(1, e.value);
		},
	});

	const layout = $derived.by(() => {
		const board = context.stateGameDerived.boardLayout();
		const s = board.scale;
		const bw = board.visualRight - board.visualLeft;

		const barVertical = isSpecialBarVertical(board);
		if (barVertical) return { anyShow: false } as const;

		const waysValue = formatWays(ways);
		const winValue = bookEventAmountToCurrencyString(stateBet.winBookEventAmount);
		const spinsValue = `${spinsTotal - spinsCurrent}/${spinsTotal}`;
		const slots = [
			{ label: 'WAYS', value: waysValue },
			{ label: 'MULTI', value: `${winMult}×` },
			spinsShow ? { label: 'FREE SPINS', value: spinsValue } : null,
			{ label: 'WIN', value: winValue },
		].filter((d): d is { label: string; value: string } => d !== null);

		const wellW = Math.max(124, (bw / Math.max(slots.length, 1)) * 0.54);
		const blockH = wellW / PLAQUE_ASPECT;

		const plateBottom = board.visualBottom + BOARD_PLATE_PAD * s;
		const preferredY = plateBottom + PLATE_CLEAR + blockH / 2;
		const main = context.stateLayoutDerived.mainLayout();
		const canvasH = context.stateLayoutDerived.canvasSizes().height;
		const hudTopScreen = stateUi.hudBarTopScreenY;
		const HUD_CLEAR_PX = 12;
		const floor =
			hudTopScreen > 0
				? main.height / 2 + (hudTopScreen - HUD_CLEAR_PX - canvasH / 2) / main.scale - blockH / 2
				: Number.POSITIVE_INFINITY;

		return {
			anyShow: true as const,
			x: board.x + COLUMN_ROW_OFFSET * s,
			y: Math.min(preferredY, floor),
			wellW,
			slots,
		};
	});
</script>

{#if layout.anyShow}
	<MainContainer>
		<Container x={stateShake.x} y={stateShake.y}>
			<HudReadout
				x={layout.x}
				y={layout.y}
				wellW={layout.wellW}
				slots={layout.slots}
				axis="x"
				hang
			/>
		</Container>
	</MainContainer>
{/if}
