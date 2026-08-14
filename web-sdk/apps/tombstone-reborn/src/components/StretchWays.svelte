<script lang="ts" module>
	// BOUNTY / NUDGE payoff badge — a WIN multiplier on the scored cell.
	// No White Room chain rack / clamp pull.
	export type EmitterEventStretchWays =
		| { type: 'stretchWaysShow'; cells: { reel: number; row: number; multiplier: number }[] }
		| { type: 'stretchWaysHide' };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { stateBet } from 'state-shared';

	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { fxDur } from '../game/fxTiming';
	import { getContext } from '../game/context';
	import { SYMBOL_CARD_W } from '../game/constants';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { shakeBoard } from '../game/stateShake.svelte';
	import MultBadge from './MultBadge.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	type Badge = {
		key: string;
		reel: number;
		row: number;
		multiplier: number;
		/** 0 → final multiplier (odometer climb) */
		climb: Tween<number>;
		/** pop when the badge lands */
		pop: Tween<number>;
	};

	let badges = $state<Badge[]>([]);
	let show = $state(false);
	const fallOut = new Tween(0);

	const runBadge = async (badge: Badge) => {
		const instant = stateBet.isSuperTurbo;
		const tier = (ms: number) => (instant ? 0 : fxDur(ms));

		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
		await badge.pop.set(1, { duration: tier(280), easing: backOut });
		await badge.climb.set(1, { duration: tier(520), easing: cubicOut });
		shakeBoard({ intensity: 4, duration: tier(140) });
	};

	context.eventEmitter.subscribeOnMount({
		stretchWaysShow: async ({ cells: incoming }) => {
			const jobs: Promise<void>[] = [];
			for (const c of incoming) {
				const key = `${c.reel}-${c.row}`;
				if (badges.some((b) => b.key === key)) continue;
				const badge: Badge = {
					key,
					reel: c.reel,
					row: c.row,
					multiplier: c.multiplier,
					climb: new Tween(0),
					pop: new Tween(0),
				};
				badges = [...badges, badge];
				show = true;
				jobs.push(runBadge(badge));
			}
			await Promise.all(jobs);
		},
		featureFxFallOut: async () => {
			await fallOutFeatureFx(fallOut, show && badges.length > 0);
			show = false;
			badges = [];
			fallOut.set(0, { duration: 0 });
		},
		stretchWaysHide: () => {
			show = false;
			badges = [];
			fallOut.set(0, { duration: 0 });
		},
	});

	const drawn = $derived(
		badges.map((b) => {
			const t = b.climb.current;
			const start = Math.min(2, b.multiplier);
			const raw = start + (b.multiplier - start) * t * t;
			return {
				key: b.key,
				cx: getSymbolX(b.reel),
				cy: getCellCenterY(b.reel, b.row),
				shown: Math.round(raw),
				scale: 0.85 + 0.15 * b.pop.current,
				tick: 1 + 0.1 * (1 - (raw - Math.floor(raw))) * Math.sin(Math.PI * t),
			};
		}),
	);

	/** Matches the plaque the nudge rider carries, so the ladder and the payoff
	 * badge are visibly the same object. */
	const BADGE_W = SYMBOL_CARD_W * 0.8;
</script>

<MainContainer>
	<BoardSpace yOffset={fallOut.current}>
		{#if show}
			{#each drawn as cell (cell.key)}
				{#if cell.shown > 0}
					<MultBadge
						label={`x${cell.shown}`}
						x={cell.cx}
						y={cell.cy}
						width={BADGE_W}
						scale={cell.scale * cell.tick}
					/>
				{/if}
			{/each}
		{/if}
	</BoardSpace>
</MainContainer>
