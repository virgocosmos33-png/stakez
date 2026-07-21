<script lang="ts" module>
	export type EmitterEventFrameMorphHud =
		| { type: 'waysCounterUpdate'; ways: number }
		| { type: 'waysCounterHide' }
		| { type: 'freeSpinCounterShow' }
		| { type: 'freeSpinCounterHide' }
		| { type: 'freeSpinCounterUpdate'; current?: number; total?: number };
</script>

<script lang="ts">
	/**
	 * Regenerated bottom of the reel frame: THREE SEPARATE gold compartments
	 * (WAYS | FREE SPINS | WIN) — never one continuous bar.
	 * Asset: frame_bottom_compartments.png (pillars between wells).
	 */
	import { MainContainer } from 'components-layout';
	import { Sprite, Text } from 'pixi-svelte';
	import { stateBet } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import config from '../game/config';
	import { stateShake } from '../game/stateShake.svelte';
	import InfoMarquee from './InfoMarquee.svelte';

	const context = getContext();

	// Lockstep with BoardFrame.svelte
	const GOLD_INNER_X = 58;
	const GOLD_INNER_Y = 101;
	const FRAME_SCALE = 0.34;
	const GAP = 6;

	// Measured on frame_bottom_compartments.png after key+crop (tools)
	const WELL = {
		y0: 0.152,
		y1: 0.874,
		left: { x0: 0.083, x1: 0.328 },
		center: { x0: 0.404, x1: 0.62 },
		right: { x0: 0.699, x1: 0.916 },
	};

	const BASE_WAYS = config.numRows.reduce((total, rows) => total * rows, 1);
	let ways = $state(BASE_WAYS);
	let spinsShow = $state(false);
	let spinsCurrent = $state(0);
	let spinsTotal = $state(0);

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
	});

	const layout = $derived.by(() => {
		const board = context.stateGameDerived.boardLayout();
		const bw = board.width;
		const bh = board.height;
		const frameX = board.x + stateShake.x;
		const frameY = board.y + stateShake.y;
		const s = FRAME_SCALE;
		const outerW = bw + 2 * GAP + 2 * GOLD_INNER_X * s;
		const outerH = bh + 2 * GAP + 2 * GOLD_INNER_Y * s;

		const frameLeft = frameX - outerW / 2;
		const frameBottom = frameY + outerH / 2;
		const yInner = frameY + bh / 2 + GAP;

		// rail sits as the bottom morph under the reel lip, matching frame width
		const railW = outerW * 1.02;
		const railH = Math.max(48, Math.min(64, (GOLD_INNER_Y * s + GAP) * 1.55));
		const railX = frameX;
		const railY = yInner + railH * 0.42;

		// Sprite is centre-anchored → well mid-line in world Y
		const wellCy = railY - railH / 2 + ((WELL.y0 + WELL.y1) / 2) * railH;
		// centres of the three SEPARATE wells in world space
		const wellCenterX = (frac: { x0: number; x1: number }) =>
			railX - railW / 2 + ((frac.x0 + frac.x1) / 2) * railW;
		const wellW = (frac: { x0: number; x1: number }) => (frac.x1 - frac.x0) * railW * 0.92;
		const wellH = (WELL.y1 - WELL.y0) * railH * 0.72;

		const waysText = `WAYS: ${ways.toLocaleString('en-US').replaceAll(',', ' ')}`;
		const winText = `WIN: ${bookEventAmountToCurrencyString(stateBet.winBookEventAmount)}`;
		const spinsText = `FREE SPINS: ${spinsTotal - spinsCurrent}/${spinsTotal}`;

		const slots = [
			{
				x: wellCenterX(WELL.left),
				y: wellCy,
				maxW: wellW(WELL.left),
				maxH: wellH,
				text: waysText,
				show: true,
			},
			{
				x: wellCenterX(WELL.center),
				y: wellCy,
				maxW: wellW(WELL.center),
				maxH: wellH,
				text: spinsText,
				show: spinsShow,
			},
			{
				x: wellCenterX(WELL.right),
				y: wellCy,
				maxW: wellW(WELL.right),
				maxH: wellH,
				text: winText,
				show: true,
			},
		];

		const fontSize = Math.max(13, Math.floor(wellH * 0.42));
		return { railX, railY, railW, railH, slots, fontSize, frameBottom };
	});

	// Base game: the centre well shows a scrolling info ticker instead of sitting
	// empty. During free spins the FREE SPINS counter owns that well, so the two
	// are mutually exclusive (counter takes precedence).
	const showMarquee = $derived(!spinsShow && context.stateGame.gameType !== 'freegame');
</script>

<MainContainer>
	{@const L = layout}
	<!-- ONE regenerated bottom morph: 3 separated compartments + gold pillars -->
	<Sprite
		key="mirrorFrameBottomCompartments"
		anchor={0.5}
		x={L.railX}
		y={L.railY}
		width={L.railW}
		height={L.railH}
	/>
	{#each L.slots as s (s.text + String(s.show))}
		{#if s.show}
			<Text
				x={s.x}
				y={s.y}
				anchor={0.5}
				text={s.text}
				style={{
					fill: 0xf0e6d0,
					fontSize: Math.min(L.fontSize, Math.floor(s.maxW / (s.text.length * 0.55))),
					fontWeight: '700',
					fontFamily: '"Segoe UI", Arial, Helvetica, sans-serif',
					letterSpacing: 0.3,
					stroke: { color: 0x2a1608, width: 3 },
				}}
			/>
		{/if}
	{/each}

	<!-- centre well: base-game info ticker (hidden while the FREE SPINS counter
		occupies the same well during the bonus) -->
	{#if showMarquee}
		{@const c = L.slots[1]}
		<InfoMarquee x={c.x} y={c.y} width={c.maxW} height={c.maxH} fontSize={L.fontSize} />
	{/if}
</MainContainer>
