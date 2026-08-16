<script lang="ts" module>
	export type EmitterEventNudgeWays =
		| {
				type: 'nudgeWaysPark';
				reel: number;
				fullReel: boolean;
				startRow: number;
				initialWays: number;
		  }
		| {
				type: 'nudgeWaysShow';
				reel: number;
				fullReel: boolean;
				startRow: number;
				initialWays: number;
				finalWays: number;
				steps: { row: number; ways: number }[];
		  }
		| { type: 'nudgeWaysHide' };
</script>

<script lang="ts">
	/**
	 * One full-reel image. Parked the instant that reel stops — overflow
	 * hidden on top, so the landed rows already show part of the same card.
	 * nudgeWaysShow only slides it down. Individual NW cells are hidden.
	 */
	import { Texture } from 'pixi.js';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicIn } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite, Rectangle, BaseSprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_CARD_W, SYMBOL_CARD_H } from '../game/constants';
	import { getReelPocket, getReelRows, getRowPitch } from '../game/utils';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { shakeBoard } from '../game/stateShake.svelte';
	import { FEATURE_ART } from '../game/featureVfx';
	import { createEdgeFireFilter, type EdgeFireUniforms } from './LinkedCellFire.svelte';
	import MultBadge from './MultBadge.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const FIRE_STRIP = 56;
	const makeEdge = (horizontal: number, flip: number) => {
		const filter = createEdgeFireFilter();
		filter.padding = 0;
		const uniforms = (filter.resources as Record<string, { uniforms: EdgeFireUniforms }>)
			.edgeUniforms.uniforms;
		uniforms.uHorizontal = horizontal;
		uniforms.uFlipDepth = flip;
		return { filter, uniforms };
	};
	const fireLeft = makeEdge(0, 1);
	const fireRight = makeEdge(0, 0);
	const fireEdges = [fireLeft, fireRight];

	const context = getContext();

	let show = $state(false);
	let ways = $state(2);
	let activeReel = $state(0);
	const slideY = new Tween(0);
	const badgePop = new Tween(1);
	const fallOut = new Tween(0);
	const ignite = new Tween(0);
	/** wall-clock for the flame lick — starts lazy, then runs hotter */
	let fireClock = 0;
	let fireLast = 0;

	const pocket = $derived(getReelPocket(activeReel));
	const colW = SYMBOL_CARD_W;
	const colTop = $derived(pocket.top);
	const cx = $derived((pocket.left + pocket.right) / 2);
	const fullH = $derived(Math.max(1, pocket.bottom - pocket.top));

	const hiddenY = (reel: number, visibleRow: number) => {
		const count = getReelRows(reel);
		const step = getRowPitch(reel);
		const shown = Math.min(count, Math.max(1, visibleRow));
		return -Math.max(0, count - shown) * step;
	};

	const clearCover = () => {
		context.stateGame.nudgeCoverReel = null;
	};

	const park = (e: {
		reel: number;
		fullReel: boolean;
		startRow: number;
		initialWays: number;
	}) => {
		activeReel = e.reel;
		ways = e.initialWays;
		slideY.set(e.fullReel ? 0 : hiddenY(e.reel, e.startRow), { duration: 0 });
		badgePop.set(1, { duration: 0 });
		fallOut.set(0, { duration: 0 });
		context.stateGame.nudgeCoverReel = e.reel;
		show = true;
		fireClock = 0;
		fireLast = 0;
		ignite.set(0, { duration: 0 });
	};

	const igniteFire = async () => {
		if (ignite.current > 0.01 || ignite.target === 1) return;
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_fire_ignite' });
		context.eventEmitter.broadcast({ type: 'soundLoop', name: 'sfx_fire_loop' });
		await ignite.set(1, { duration: fxDur(240), easing: cubicIn });
		shakeBoard({ intensity: 11, duration: fxDur(140) });
	};

	const douseFire = () => {
		context.eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_fire_loop' });
		fireClock = 0;
		fireLast = 0;
		ignite.set(0, { duration: 0 });
	};

	const punchWays = (next: number) => {
		ways = next;
		badgePop.set(1.45, { duration: 0 });
		badgePop.set(1, { duration: fxDur(320) });
	};

	const run = async (e: {
		reel: number;
		fullReel: boolean;
		startRow: number;
		initialWays: number;
		finalWays: number;
		steps: { row: number; ways: number }[];
	}) => {
		if (!show) park(e);

		if (e.fullReel) {
			punchWays(e.finalWays);
			await igniteFire();
			return;
		}

		punchWays(e.initialWays);
		await fxWait(80);

		const thud = async (y: number, nextWays: number) => {
			context.eventEmitter.broadcast({
				type: 'soundOnce',
				name: 'sfx_reel_nudge',
				forcePlay: true,
			});
			await slideY.set(y, { duration: fxDur(320), easing: backOut });
			punchWays(nextWays);
			shakeBoard({ intensity: 8, duration: fxDur(180) });
			await fxWait(200);
		};

		for (const step of e.steps) {
			await thud(hiddenY(e.reel, step.row), step.ways);
		}
		if (Math.abs(slideY.current) > 0.5) {
			await thud(0, e.finalWays);
		}

		await igniteFire();
	};

	context.eventEmitter.subscribeOnMount({
		nudgeWaysPark: (e) => park(e),
		nudgeWaysShow: (e) => run(e),
		nudgeWaysHide: () => {
			douseFire();
			show = false;
			clearCover();
		},
		featureFxFallOut: async () => {
			context.eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_fire_loop' });
			await fallOutFeatureFx(fallOut, show);
			show = false;
			clearCover();
			fireClock = 0;
			fireLast = 0;
			ignite.set(0, { duration: 0 });
		},
	});

	$effect(() => {
		if (!show) return;
		let raf = 0;
		fireLast = 0;
		const tick = (now: number) => {
			const dt = fireLast ? now - fireLast : 16;
			fireLast = now;
			const p = ignite.current;
			// lick starts almost still, then runs ~2x once the column is up
			fireClock += dt * (0.9 + 3.4 * p * p);
			for (const edge of fireEdges) {
				edge.uniforms.uTime = fireClock;
				edge.uniforms.uIntensity = 0.55 + 0.85 * p;
				edge.uniforms.uProgress = p;
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
</script>

<MainContainer>
	<BoardSpace yOffset={fallOut.current}>
		{#if show}
			<Container x={cx} y={colTop}>
				<Container>
					<Rectangle
						isMask
						anchor={{ x: 0.5, y: 0 }}
						width={colW}
						height={fullH}
						backgroundColor={0xffffff}
					/>
					<Sprite
						key={FEATURE_ART.nudgeColumn}
						y={slideY.current}
						anchor={{ x: 0.5, y: 0 }}
						width={colW}
						height={fullH}
					/>
				</Container>
				{#if ignite.current > 0.01}
					<Container x={-colW / 2} y={fullH / 2} filters={[fireLeft.filter]}>
						<BaseSprite
							texture={Texture.WHITE}
							anchor={{ x: 1, y: 0.5 }}
							width={FIRE_STRIP}
							height={fullH}
						/>
					</Container>
					<Container x={colW / 2} y={fullH / 2} filters={[fireRight.filter]}>
						<BaseSprite
							texture={Texture.WHITE}
							anchor={{ x: 0, y: 0.5 }}
							width={FIRE_STRIP}
							height={fullH}
						/>
					</Container>
				{/if}
				<MultBadge
					label={`x${ways}`}
					y={slideY.current + fullH}
					width={SYMBOL_CARD_W * 0.86}
					scale={badgePop.current}
				/>
			</Container>
		{/if}
	</BoardSpace>
</MainContainer>
