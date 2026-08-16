<script lang="ts">
	/**
	 * Desktop HUD, locked to the staircase:
	 *   WAYS + MULTI hang from the TOP OF THE SCREEN in the sky above the
	 *   short right reels.
	 *   WIN hangs from the BOTTOM LIP of that same right-hand timber.
	 * Narrow layouts leave this empty; FrameMorphHud shows the boxes under the board.
	 */
	import { stateBet } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { Container } from 'pixi-svelte';

	import HudReadout from './HudReadout.svelte';

	import { getContext } from '../game/context';
	import config from '../game/config';
	import { CELL_PITCH_X, SYMBOL_SIZE } from '../game/constants';
	import { isSpecialBarVertical } from '../game/specialBarLayout';
	import { stateShake } from '../game/stateShake.svelte';
	import { getCellLeft, getReelYOffset } from '../game/utils';
	import { formatWays } from '../game/waysFormat';

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
		const notchCx = toX((notchL + notchR) / 2);
		const hangCx = toX((getCellLeft(4) + getCellLeft(5) + CELL_PITCH_X) / 2);
		const shortTop = getReelYOffset(3);
		const shortBot = shortTop + 2 * SYMBOL_SIZE;
		const lipY = toY(shortBot + FRAME_LIP);

		const pocketW = (notchR - notchL) * s;
		const wellW = Math.max(196, Math.min(pocketW * 0.74, 248));
		const blockH = wellW / PLAQUE_ASPECT;

		const hangSlots = [
			{ label: 'WAYS', value: formatWays(ways) },
			{ label: 'MULTI', value: `${winMult}×` },
		];
		const pocketBot = toY(shortTop) - 6;
		const hangY = Math.min(screenTop + 40 + blockH * 0.5, pocketBot - blockH * 0.45);

		const winSlots: { label: string; value: string }[] = [];
		if (spinsShow) {
			winSlots.push({
				label: 'FREE SPINS',
				value: `${spinsTotal - spinsCurrent}/${spinsTotal}`,
			});
		}
		winSlots.push({ label: 'WIN', value: winValue });
		const winStackH =
			winSlots.length * blockH + Math.max(0, winSlots.length - 1) * blockH * 0.08;
		const winY = lipY + 10 + winStackH * 0.5;

		return {
			hang: {
				x: hangCx,
				y: hangY + stateShake.y,
				wellW,
				slots: hangSlots,
				chainFromY: screenTop,
			},
			win: {
				x: notchCx + CELL_PITCH_X * s * 0.18,
				y: winY,
				wellW,
				slots: winSlots,
				chainFromY: lipY,
			},
		};
	});
</script>

{#if readout}
	<Container zIndex={0}>
		<HudReadout
			x={readout.hang.x}
			y={readout.hang.y}
			wellW={readout.hang.wellW}
			slots={readout.hang.slots}
			axis="x"
			hang
			parts="chains"
			gap={-readout.hang.wellW * 0.16}
			chainFromY={readout.hang.chainFromY}
		/>
		<HudReadout
			x={readout.win.x}
			y={readout.win.y}
			wellW={readout.win.wellW}
			slots={readout.win.slots}
			axis="y"
			hang
			parts="chains"
			chainFromY={readout.win.chainFromY}
		/>
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
			gap={-readout.hang.wellW * 0.16}
			chainFromY={readout.hang.chainFromY}
		/>
		<HudReadout
			x={readout.win.x}
			y={readout.win.y}
			wellW={readout.win.wellW}
			slots={readout.win.slots}
			axis="y"
			hang
			parts="boxes"
			chainFromY={readout.win.chainFromY}
		/>
	</Container>
{/if}
