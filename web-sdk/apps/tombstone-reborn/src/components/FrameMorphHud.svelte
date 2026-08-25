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
	 * Narrow-layout fallback. Live plaques are SpecialBar at PSD seats.
	 * If the side bar ever lies flat, this draws the same PSD art/seats
	 * — never the old wellW stack under the board.
	 */
	import { MainContainer } from 'components-layout';
	import { Container } from 'pixi-svelte';
	import { stateBet } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import HudReadout from './HudReadout.svelte';
	import { getContext } from '../game/context';
	import config from '../game/config';
	import { plaqueGeom, type HudPlaqueGeom } from '../game/hudPlaqueSeats';
	import { isSpecialBarVertical } from '../game/specialBarLayout';
	import { formatWays, formatWinMult } from '../game/waysFormat';

	const context = getContext();
	const BASE_WAYS = config.numRows.reduce((total, rows) => total * rows, 1);
	let ways = $state(BASE_WAYS);
	let spinsShow = $state(false);
	let spinsCurrent = $state(0);
	let spinsTotal = $state(0);
	let winMult = $state(1);
	const heldLabels: string[] = [];

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

	const plaques = $derived.by((): HudPlaqueGeom[] | null => {
		if (isSpecialBarVertical()) return null;
		const main = context.stateLayoutDerived.mainLayout();
		const canvas = context.stateLayoutDerived.canvasSizes();
		const atmo = context.stateGame.atmosphere;
		const rows: { label: string; value: string }[] = [
			{ label: 'WAYS', value: formatWays(ways) },
			{ label: 'MULTI', value: formatWinMult(winMult) },
			{ label: 'WIN', value: bookEventAmountToCurrencyString(stateBet.winBookEventAmount) },
		];
		if (spinsShow) {
			rows.push({
				label: 'FREE SPINS',
				value: `${spinsTotal - spinsCurrent}/${spinsTotal}`,
			});
		}
		return rows
			.map((row) => plaqueGeom(row.label, row.value, atmo, canvas, main))
			.filter((g): g is HudPlaqueGeom => g != null);
	});
</script>

{#if plaques}
	<MainContainer>
		<Container zIndex={0}>
			<HudReadout plaques={plaques} parts="chains" heldLabels={heldLabels} />
		</Container>
		<Container zIndex={1}>
			<HudReadout plaques={plaques} parts="plate" heldLabels={heldLabels} />
		</Container>
		<Container zIndex={2}>
			<HudReadout plaques={plaques} parts="boxes" heldLabels={heldLabels} />
		</Container>
	</MainContainer>
{/if}
