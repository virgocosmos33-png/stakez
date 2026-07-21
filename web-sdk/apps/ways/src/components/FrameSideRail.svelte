<script lang="ts" module>
	export type EmitterEventFrameSideRail =
		| { type: 'waysCounterUpdate'; ways: number }
		| { type: 'waysCounterHide' }
		| { type: 'freeSpinCounterShow' }
		| { type: 'freeSpinCounterHide' }
		| { type: 'freeSpinCounterUpdate'; current?: number; total?: number };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite, Graphics } from 'pixi-svelte';
	import { stateBet } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import config from '../game/config';
	import { getSideRailLayout, type TextSlot } from '../game/plaqueMount';
	import FittedText from './FittedText.svelte';

	const context = getContext();

	// EXACT reference:
	//   normal → WAYS / WIN (+ crystal ball in panel art)
	//   bonus  → FREE SPINS / WAYS / WIN (+ crystal ball)
	// One gold side panel flush to the reel frame — never separate floating plates.
	let spinsShow = $state(false);
	const rail = $derived(getSideRailLayout({ freeSpins: spinsShow }));

	const BASE_WAYS = config.numRows.reduce((total, rows) => total * rows, 1);
	let ways = $state(BASE_WAYS);
	const waysPop = new Tween(1);
	const waysText = $derived(ways.toLocaleString('en-US').replaceAll(',', ' '));

	const winText = $derived(bookEventAmountToCurrencyString(stateBet.winBookEventAmount));
	const winPop = new Tween(1);
	let lastWin = stateBet.winBookEventAmount;

	$effect(() => {
		const next = stateBet.winBookEventAmount;
		if (next !== lastWin) {
			lastWin = next;
			if (next > 0) {
				winPop.set(1.18, { duration: 0 });
				winPop.set(1, { duration: 300, easing: backOut });
			}
		}
	});

	let spinsCurrent = $state(0);
	let spinsTotal = $state(0);
	const spinsText = $derived(`${spinsTotal - spinsCurrent} / ${spinsTotal}`);

	context.eventEmitter.subscribeOnMount({
		waysCounterUpdate: (e) => {
			ways = e.ways;
			waysPop.set(1.18, { duration: 0 });
			waysPop.set(1, { duration: 300, easing: backOut });
		},
		waysCounterHide: () => (ways = BASE_WAYS),
		freeSpinCounterShow: () => (spinsShow = true),
		freeSpinCounterHide: () => (spinsShow = false),
		freeSpinCounterUpdate: (e) => {
			if (e.current !== undefined) spinsCurrent = e.current;
			if (e.total !== undefined) spinsTotal = e.total;
		},
	});

	// section list matches reference order
	const rows = $derived.by(() => {
		if (spinsShow) {
			return [
				{ slot: rail.sections[0], caption: 'FREE SPINS', value: spinsText, pop: 1 },
				{ slot: rail.sections[1], caption: 'WAYS', value: waysText, pop: waysPop.current },
				{ slot: rail.sections[2], caption: 'WIN', value: winText, pop: winPop.current },
			];
		}
		return [
			{ slot: rail.sections[0], caption: 'WAYS', value: waysText, pop: waysPop.current },
			{ slot: rail.sections[1], caption: 'WIN', value: winText, pop: winPop.current },
		];
	});

	const drawDividers = (g: import('pixi.js').Graphics) => {
		g.clear();
		const half = rail.panelW * 0.26;
		for (const y of rail.dividers) {
			g.moveTo(rail.cx - half, y);
			g.lineTo(rail.cx + half, y);
			g.stroke({ color: 0xc9a86a, width: 1.5, alpha: 0.75 });
			// small diamond flourish (reference)
			const d = 3.5;
			g.moveTo(rail.cx, y - d);
			g.lineTo(rail.cx + d, y);
			g.lineTo(rail.cx, y + d);
			g.lineTo(rail.cx - d, y);
			g.closePath();
			g.fill({ color: 0xe8d5a0, alpha: 0.85 });
		}
	};
</script>

{#snippet stacked(slot: TextSlot, caption: string, value: string, pop: number)}
	<Container x={slot.cx} y={slot.cy} scale={pop}>
		<FittedText
			x={0}
			y={-slot.maxH * 0.28}
			maxWidth={slot.maxW}
			maxHeight={slot.maxH * 0.32}
			tint={0xf0e6d0}
			text={caption}
			style={{ fontFamily: 'silver', fontSize: (slot.maxH * 0.32) / 1.69, letterSpacing: 2 }}
		/>
		<FittedText
			x={0}
			y={slot.maxH * 0.22}
			maxWidth={slot.maxW}
			maxHeight={slot.maxH * 0.52}
			tint={0xffffff}
			text={value}
			style={{ fontFamily: 'silver', fontSize: (slot.maxH * 0.52) / 1.69, letterSpacing: 1 }}
		/>
	</Container>
{/snippet}

<MainContainer>
	<!-- single gold panel + crystal ball, flush to the reel frame -->
	<Container x={rail.cx} y={rail.cy}>
		<Sprite key="mirrorSideRail" anchor={0.5} width={rail.panelW} height={rail.panelH} />
	</Container>

	<Graphics draw={drawDividers} />

	{#each rows as row}
		{@render stacked(row.slot, row.caption, row.value, row.pop)}
	{/each}
</MainContainer>
