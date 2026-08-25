<script lang="ts">
	/**
	 * Desktop HUD plaques at PSD seats (scene cover-fit). Art is the
	 * extracted WAYS / MULTI / WIN / FREE SPINS layer pixels.
	 */
	import { stateBet } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { Container } from 'pixi-svelte';

	import HudReadout from './HudReadout.svelte';

	import { getContext } from '../game/context';
	import config from '../game/config';
	import { isBonusAtmosphere } from '../game/atmosphere.svelte';
	import { plaqueGeom, type HudPlaqueGeom } from '../game/hudPlaqueSeats';
	import { isSpecialBarVertical } from '../game/specialBarLayout';
	import { formatWays, formatWinMult } from '../game/waysFormat';

	type Props = {
		layer?: 'all' | 'hud';
	};

	const props: Props = $props();
	const layer = $derived(props.layer ?? 'all');
	const showHud = $derived(layer === 'all' || layer === 'hud');

	const context = getContext();
	const BASE_WAYS = config.numRows.reduce((total, rows) => total * rows, 1);

	let ways = $state(BASE_WAYS);
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
		freeSpinCounterHide: () => {
			spinsCurrent = 0;
			spinsTotal = 0;
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

	const plaques = $derived.by((): HudPlaqueGeom[] | null => {
		if (!isSpecialBarVertical()) return null;
		const main = context.stateLayoutDerived.mainLayout();
		const canvas = context.stateLayoutDerived.canvasSizes();
		const atmo = context.stateGame.atmosphere;
		const rows: { label: string; value: string }[] = [
			{ label: 'WAYS', value: formatWays(ways) },
			{ label: 'MULTI', value: formatWinMult(winMult) },
			{ label: 'WIN', value: winValue },
		];
		if (isBonusAtmosphere(atmo)) {
			rows.push({
				label: 'FREE SPINS',
				value: spinsTotal > 0 ? `${spinsTotal - spinsCurrent}/${spinsTotal}` : '',
			});
		}
		return rows
			.map((row) => plaqueGeom(row.label, row.value, atmo, canvas, main))
			.filter((g): g is HudPlaqueGeom => g != null);
	});
</script>

{#if plaques && showHud}
	<Container sortableChildren>
	<Container zIndex={1}>
		<HudReadout plaques={plaques} parts="plate" heldLabels={heldLabels} />
	</Container>
	<Container zIndex={2}>
		<HudReadout plaques={plaques} parts="boxes" heldLabels={heldLabels} />
	</Container>
	</Container>
{/if}
