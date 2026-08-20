<script lang="ts">
	/**
	 * Desktop: committed hang (size + seat).
	 * Compact (tablet / portrait): same chains-from-top, pair sits on the
	 * board crest and scales with that pocket.
	 * WIN hangs from the BOTTOM LIP of the short right timber.
	 */
	import { stateBet } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { Container } from 'pixi-svelte';

	import HudReadout from './HudReadout.svelte';

	import { getContext } from '../game/context';
	import config from '../game/config';
	import { CELL_PITCH_X, SYMBOL_SIZE } from '../game/constants';
	import { HANG_PAIR_GAP, hangPairXs, isSpecialBarVertical } from '../game/specialBarLayout';
	import { stateShake } from '../game/stateShake.svelte';
	import { getCellLeft, getReelYOffset } from '../game/utils';
	import { formatWays, formatWinMult } from '../game/waysFormat';

	type Props = {
		/** Split so the wordmark can sit between chains and boxes. */
		layer?: 'all' | 'chains' | 'hud';
	};

	const props: Props = $props();
	const layer = $derived(props.layer ?? 'all');
	const showChains = $derived(layer === 'all' || layer === 'chains');
	const showHud = $derived(layer === 'all' || layer === 'hud');

	const context = getContext();
	const BASE_WAYS = config.numRows.reduce((total, rows) => total * rows, 1);
	const PLAQUE_ASPECT = 1.6;
	/** plank thickness below the short-reel cells (matches the baked frame lip) */
	const FRAME_LIP = 28;

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
	const winValue = $derived(bookEventAmountToCurrencyString(stateBet.winBookEventAmount));
	const heldLabels: string[] = [];

	const readout = $derived.by(() => {
		if (!isSpecialBarVertical()) return null;

		const board = context.stateGameDerived.boardLayout();
		const s = board.scale;
		const main = context.stateLayoutDerived.mainLayout();
		const canvas = context.stateLayoutDerived.canvasSizes();
		const toX = (lx: number) => board.x + (lx - board.pivot.x) * s + stateShake.x;
		const toY = (ly: number) => board.y + (ly - board.pivot.y) * s + stateShake.y;
		const screenTop = (0 - canvas.height / 2) / main.scale + main.height / 2;

		// Short right timber (reels 3–4). Pair centre and box width follow
		// this pocket at every scale — a fixed 196px floor used to shove the
		// boxes into the logo on a small window, and seating them at screen
		// top left a dead gap above the frame.
		const notchL = getCellLeft(3);
		const notchR = getCellLeft(4) + CELL_PITCH_X;
		const shortTop = getReelYOffset(3);
		const shortBot = shortTop + 2 * SYMBOL_SIZE;
		const lipY = toY(shortBot + FRAME_LIP);
		const pocketW = (notchR - notchL) * s;
		const pocketBot = toY(shortTop) - 6;
		const portrait = context.stateLayoutDerived.layoutType() === 'portrait';
		const compact =
			portrait || context.stateLayoutDerived.canvasRatioType() === 'almostSquare';

		// Desktop keeps the committed hang (size + seat). Compact (tablet /
		// almost-square) follows the board crest so the pair does not float
		// off into the logo. Portrait sits a notch left of the tablet seat.
		const hangCx = compact
			? toX((notchL + notchR) / 2 + CELL_PITCH_X * (portrait ? 0.85 : 1.2))
			: toX((getCellLeft(4) + getCellLeft(5) + CELL_PITCH_X) / 2);
		const wellW = compact
			? (pocketW / (2 + HANG_PAIR_GAP)) * 1.68
			: Math.max(196, Math.min(pocketW * 0.74, 248));
		const blockH = wellW / PLAQUE_ASPECT;
		const hangY = compact
			? Math.max(
					screenTop + blockH * 0.52,
					board.visualTop + stateShake.y + blockH * 0.42,
				)
			: Math.min(screenTop + 40 + blockH * 0.5, pocketBot - blockH * 0.45) +
				stateShake.y;

		const hangSlots = [
			{ label: 'WAYS', value: formatWays(ways) },
			{ label: 'MULTI', value: formatWinMult(winMult) },
		];

		const HANG_DROP = 28;
		const pair = hangPairXs(hangCx, wellW);
		const pairGap = wellW * HANG_PAIR_GAP;
		const winY = lipY + HANG_DROP + blockH * 0.5;
		const last = context.stateGame.board.length - 1;
		const notchHang = toY(getReelYOffset(last));
		// Always from the canvas top — a crest start sits inside the bigger
		// boxes and the links never draw. Long drop also runs behind the logo.
		const boxTop = hangY - blockH * 0.5;
		const hangChainsFrom = Math.min(screenTop, boxTop - Math.max(48, blockH * 0.85));

		return {
			hang: {
				x: hangCx,
				y: hangY,
				wellW,
				slots: hangSlots,
				gap: pairGap,
				chainFromY: hangChainsFrom,
			},
			win: {
				x: pair.left,
				y: winY,
				wellW,
				slots: [{ label: 'WIN', value: winValue }],
				chainFromY: lipY,
			},
			spins: spinsShow
				? {
						x: pair.right,
						y: winY,
						wellW,
						slots: [
							{
								label: 'FREE SPINS',
								value: `${spinsTotal - spinsCurrent}/${spinsTotal}`,
							},
						],
						chainFromY: notchHang,
					}
				: null,
		};
	});
</script>

{#if readout}
	<Container sortableChildren>
	{#if showChains}
	<Container zIndex={0}>
		<HudReadout
			x={readout.hang.x}
			y={readout.hang.y}
			wellW={readout.hang.wellW}
			slots={readout.hang.slots}
			axis="x"
			hang
			parts="chains"
			gap={readout.hang.gap}
			chainFromY={readout.hang.chainFromY}
			heldLabels={heldLabels}
		/>
		<HudReadout
			x={readout.win.x}
			y={readout.win.y}
			wellW={readout.win.wellW}
			slots={readout.win.slots}
			axis="x"
			hang
			parts="chains"
			chainFromY={readout.win.chainFromY}
		/>
		{#if readout.spins}
			<HudReadout
				x={readout.spins.x}
				y={readout.spins.y}
				wellW={readout.spins.wellW}
				slots={readout.spins.slots}
				axis="x"
				hang
				parts="chains"
				chainFromY={readout.spins.chainFromY}
			/>
		{/if}
	</Container>
	{/if}
	{#if showHud}
	<Container zIndex={1}>
		<HudReadout
			x={readout.hang.x}
			y={readout.hang.y}
			wellW={readout.hang.wellW}
			slots={readout.hang.slots}
			axis="x"
			hang
			parts="plate"
			gap={readout.hang.gap}
			chainFromY={readout.hang.chainFromY}
			heldLabels={heldLabels}
		/>
		<HudReadout
			x={readout.win.x}
			y={readout.win.y}
			wellW={readout.win.wellW}
			slots={readout.win.slots}
			axis="x"
			hang
			parts="plate"
			chainFromY={readout.win.chainFromY}
		/>
		{#if readout.spins}
			<HudReadout
				x={readout.spins.x}
				y={readout.spins.y}
				wellW={readout.spins.wellW}
				slots={readout.spins.slots}
				axis="x"
				hang
				parts="plate"
				chainFromY={readout.spins.chainFromY}
			/>
		{/if}
	</Container>
	<Container zIndex={2}>
		<HudReadout
			x={readout.hang.x}
			y={readout.hang.y}
			wellW={readout.hang.wellW}
			slots={readout.hang.slots}
			axis="x"
			hang
			parts="boxes"
			gap={readout.hang.gap}
			chainFromY={readout.hang.chainFromY}
			heldLabels={heldLabels}
		/>
		<HudReadout
			x={readout.win.x}
			y={readout.win.y}
			wellW={readout.win.wellW}
			slots={readout.win.slots}
			axis="x"
			hang
			parts="boxes"
			chainFromY={readout.win.chainFromY}
		/>
		{#if readout.spins}
			<HudReadout
				x={readout.spins.x}
				y={readout.spins.y}
				wellW={readout.spins.wellW}
				slots={readout.spins.slots}
				axis="x"
				hang
				parts="boxes"
				chainFromY={readout.spins.chainFromY}
			/>
		{/if}
	</Container>
	{/if}
	</Container>
{/if}
