<script lang="ts">
	/**
	 * Desktop HUD, locked to the staircase:
	 *   WAYS + MULTI hang from the TOP OF THE SCREEN in the sky above the
	 *   short right reels. MULTI stays on the chains in base (shows x1
	 *   until a feature ticks it).
	 *   WIN hangs from the BOTTOM LIP of that same right-hand timber.
	 *   WIN + FREE SPINS are the same pair as WAYS + MULTI: same width, same
	 *   gap, same centre. FREE SPINS sits under MULTI.
	 * Narrow layouts leave this empty; FrameMorphHud shows the boxes under the board.
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

		const notchL = getCellLeft(3);
		const notchR = getCellLeft(4) + CELL_PITCH_X;
		const hangCx = toX((getCellLeft(4) + getCellLeft(5) + CELL_PITCH_X) / 2);
		const shortTop = getReelYOffset(3);
		const shortBot = shortTop + 2 * SYMBOL_SIZE;
		const lipY = toY(shortBot + FRAME_LIP);

		const pocketW = (notchR - notchL) * s;
		const wellW = Math.max(196, Math.min(pocketW * 0.74, 248));
		const blockH = wellW / PLAQUE_ASPECT;

		const hangSlots = [
			{ label: 'WAYS', value: formatWays(ways) },
			{ label: 'MULTI', value: formatWinMult(winMult) },
		];
		const pocketBot = toY(shortTop) - 6;
		const hangY = Math.min(screenTop + 40 + blockH * 0.5, pocketBot - blockH * 0.45);

		const HANG_DROP = 28;
		const pair = hangPairXs(hangCx, wellW);
		const pairGap = wellW * HANG_PAIR_GAP;
		const winY = lipY + HANG_DROP + blockH * 0.5;
		const last = context.stateGame.board.length - 1;
		const notchHang = toY(getReelYOffset(last));

		return {
			hang: {
				x: hangCx,
				y: hangY + stateShake.y,
				wellW,
				slots: hangSlots,
				gap: pairGap,
				chainFromY: screenTop,
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
	</Container>
{/if}
