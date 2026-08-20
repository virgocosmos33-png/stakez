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
				added?: number;
				winMult?: number;
		  }
		| { type: 'nudgeWaysHide' }
		| { type: 'nudgeWaysPunch'; reel: number; ways: number };
</script>

<script lang="ts">
	/**
	 * One full-reel NUDGE column per reel. The same tall card always slides:
	 * the reel window shows the landed foot, and the NUDGE header seats on
	 * the board lip. A growing mask would pin the header in the first cell.
	 * Two nudges each keep their own totem.
	 */
	import { Texture } from 'pixi.js';
	import { Tween } from 'svelte/motion';
	import { cubicIn } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite, Rectangle, BaseSprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_CARD_W, SYMBOL_CARD_H } from '../game/constants';
	import { getCellCenterY, getCardHeight, getReelPocket, getReelRows } from '../game/utils';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { shakeBoard } from '../game/stateShake.svelte';
	import { FEATURE_ART } from '../game/featureVfx';
	import {
		createFireRingFilter,
		FIRE_RATIO,
		fireQuadSize,
		type RingUniforms,
	} from './LinkedCellFire.svelte';
	import { formatWaysMult } from '../game/waysFormat';
	import MultBadge from './MultBadge.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const BADGE_RATIO = 199 / 512;
	/** NUDGE plaque share of fx_nudge_column.png (header px / image h). */
	const HEADER_FRAC = 200 / 2360;
	const COL_BOX_X = 0.58;
	const COL_BOX_Y = 0.72;

	const context = getContext();

	type Totem = {
		reel: number;
		startRow: number;
		ways: number;
		revealRow: Tween<number>;
		badgePop: Tween<number>;
		ignite: Tween<number>;
		fire: ReturnType<typeof createFireRingFilter>;
		fireUniforms: RingUniforms;
		fireClock: number;
	};

	let totems = $state<Totem[]>([]);
	const fallOut = new Tween(0);
	let fireLast = 0;

	const colW = SYMBOL_CARD_W;
	const badgeH = colW * 0.86 * BADGE_RATIO;
	const show = $derived(totems.length > 0);

	const makeFire = () => {
		const fire = createFireRingFilter();
		fire.padding = 0;
		const fireUniforms = (fire.resources as Record<string, { uniforms: RingUniforms }>)
			.ringUniforms.uniforms;
		fireUniforms.uRatio = FIRE_RATIO;
		fireUniforms.uHideTop = 0;
		fireUniforms.uHideBot = 0;
		fireUniforms.uBoxX = COL_BOX_X;
		fireUniforms.uBoxY = COL_BOX_Y;
		fireUniforms.uCorner = 0.13;
		fireUniforms.uThickness = 0.11;
		fireUniforms.uLockBox = 1;
		return { fire, fireUniforms };
	};

	const layoutOf = (reel: number) => {
		const pocket = getReelPocket(reel);
		const fullH = Math.max(1, pocket.bottom - pocket.top);
		const headerH = fullH * (HEADER_FRAC / (1 - HEADER_FRAC));
		const spriteH = headerH + fullH;
		const totemTop = -headerH;
		const totemBot = fullH + badgeH / 2;
		const totemH = Math.max(1, totemBot - totemTop);
		return {
			cx: (pocket.left + pocket.right) / 2,
			colTop: pocket.top,
			fullH,
			headerH,
			spriteH,
			cardH: getCardHeight(reel),
			rows: getReelRows(reel),
			fireY: (totemTop + totemBot) / 2,
			fireYScale: totemH / SYMBOL_CARD_H,
			fireQuad: fireQuadSize(colW, totemH, COL_BOX_X, COL_BOX_Y),
		};
	};

	/** Bottom of the landed stack, relative to the reel lip. */
	const revealBotOf = (reel: number, revealRow: number) => {
		const layout = layoutOf(reel);
		const row = Math.min(layout.rows, Math.max(1, revealRow));
		const bottom = getCellCenterY(reel, row) + layout.cardH / 2;
		return Math.min(layout.fullH, Math.max(layout.cardH * 0.5, bottom - layout.colTop));
	};

	/** 0 when seated; negative while the foot is still high in the reel. */
	const slideYOf = (reel: number, revealRow: number) =>
		revealBotOf(reel, revealRow) - layoutOf(reel).fullH;

	const coverReel = (reel: number) => {
		context.stateGame.nudgeCoverReel = reel;
		if (!context.stateGame.nudgeCoverReels.includes(reel)) {
			context.stateGame.nudgeCoverReels = [...context.stateGame.nudgeCoverReels, reel];
		}
	};

	const coverStack = (reel: number, fromRow: number, toRow: number) => {
		coverReel(reel);
		const kept = context.stateGame.nudgeCoverCells.filter((cell) => cell.reel !== reel);
		const floor = layoutOf(reel).rows;
		const lo = Math.min(floor, Math.max(1, Math.round(fromRow)));
		const hi = Math.min(floor, Math.max(lo, Math.round(toRow)));
		for (let row = lo; row <= hi; row++) kept.push({ reel, row });
		context.stateGame.nudgeCoverCells = kept;
	};

	const clearCover = () => {
		context.stateGame.nudgeCoverReel = null;
		context.stateGame.nudgeCoverReels = [];
		context.stateGame.nudgeCoverCells = [];
		for (const push of context.stateGame.nudgePush) {
			push.rows = [];
			push.bumpRows = [];
			push.t.set(0, { duration: 0 });
		}
	};

	const shoveOut = async (reel: number, fromRow: number, toRow: number, duration: number) => {
		const push = context.stateGame.nudgePush[reel];
		if (!push) return;
		const lo = Math.min(fromRow, toRow) + 1;
		const hi = Math.max(fromRow, toRow);
		const floor = layoutOf(reel).rows;
		const rows: number[] = [];
		const bumpRows: number[] = [];
		for (let row = lo; row <= floor; row++) {
			if (row <= hi) rows.push(row);
			else bumpRows.push(row);
		}
		push.rows = rows;
		push.bumpRows = bumpRows;
		push.t.set(0, { duration: 0 });
		if (!rows.length && !bumpRows.length) return;
		await push.t.set(1, { duration, easing: cubicIn });
		push.rows = [];
		push.bumpRows = [];
		push.t.set(0, { duration: 0 });
	};

	const park = (e: {
		reel: number;
		fullReel: boolean;
		startRow: number;
		initialWays: number;
	}) => {
		const rows = layoutOf(e.reel).rows;
		const startRow = e.fullReel ? 1 : Math.min(rows, Math.max(1, e.startRow));
		const reveal = e.fullReel ? rows : startRow;
		const existing = totems.find((totem) => totem.reel === e.reel);
		const totem =
			existing ??
			({
				reel: e.reel,
				startRow,
				ways: e.initialWays,
				revealRow: new Tween(reveal),
				badgePop: new Tween(1),
				ignite: new Tween(0),
				fireClock: 0,
				...makeFire(),
			} satisfies Totem);
		totem.startRow = startRow;
		totem.ways = e.initialWays;
		totem.revealRow.set(reveal, { duration: 0 });
		totem.badgePop.set(1, { duration: 0 });
		totem.ignite.set(0, { duration: 0 });
		fallOut.set(0, { duration: 0 });
		coverStack(e.reel, startRow, reveal);
		if (!existing) totems = [...totems, totem];
		else totems = [...totems];
	};

	const igniteFire = async (totem: Totem) => {
		if (totem.ignite.current > 0.01 || totem.ignite.target === 1) return;
		// Visual only. The fire bed is a hiss/crackle loop and reads as
		// white-noise glitch on the nudge-ways book.
		await totem.ignite.set(1, { duration: fxDur(240), easing: cubicIn });
		shakeBoard({ intensity: 11, duration: fxDur(140) });
	};

	const douseFire = () => {
		fireLast = 0;
		for (const totem of totems) {
			totem.ignite.set(0, { duration: 0 });
			totem.fireClock = 0;
		}
	};

	const punchWays = (totem: Totem, next: number) => {
		totem.ways = next;
		totem.badgePop.set(1.45, { duration: 0 });
		void totem.badgePop.set(1, { duration: fxDur(280) });
		totems = [...totems];
	};

	const run = async (e: {
		reel: number;
		fullReel: boolean;
		startRow: number;
		initialWays: number;
		finalWays: number;
		steps: { row: number; ways: number }[];
		added?: number;
		winMult?: number;
	}) => {
		if (!totems.some((totem) => totem.reel === e.reel)) park(e);
		const totem = totems.find((item) => item.reel === e.reel);
		if (!totem) return;

		if (e.fullReel) {
			punchWays(totem, e.finalWays);
			await igniteFire(totem);
			return;
		}

		punchWays(totem, e.initialWays);
		await fxWait(60);

		const added = e.added ?? 0;
		const endMult = e.winMult ?? 1;
		let running = Math.max(1, endMult - added);

		const thud = async (row: number, nextWays: number, tickWin: boolean) => {
			const from = totem.revealRow.current;
			const dist = Math.max(0.35, Math.abs(row - from));
			const duration = fxDur(180 + 80 * dist);
			coverStack(totem.reel, totem.startRow, Math.round(from));
			context.eventEmitter.broadcast({
				type: 'soundOnce',
				name: 'sfx_reel_nudge',
				forcePlay: true,
			});
			await Promise.all([
				totem.revealRow.set(row, { duration, easing: cubicIn }),
				shoveOut(totem.reel, Math.round(from), row, duration),
			]);
			coverStack(totem.reel, totem.startRow, row);
			punchWays(totem, nextWays);
			if (tickWin && added > 0) {
				running = Math.min(endMult, running + 1);
				context.eventEmitter.broadcast({ type: 'winMultUpdate', value: running });
			}
			shakeBoard({ intensity: 8, duration: fxDur(140) });
			await fxWait(90);
		};

		for (const step of e.steps) {
			await thud(step.row, step.ways, true);
		}
		const floor = layoutOf(totem.reel).rows;
		if (totem.revealRow.current < floor - 0.05 && e.steps.length) {
			await thud(floor, e.finalWays, false);
		}

		await igniteFire(totem);
	};

	context.eventEmitter.subscribeOnMount({
		nudgeWaysPark: (e) => park(e),
		nudgeWaysShow: (e) => run(e),
		nudgeWaysPunch: ({ reel, ways }) => {
			const totem = totems.find((item) => item.reel === reel);
			if (!totem || ways <= totem.ways) return;
			punchWays(totem, ways);
		},
		nudgeWaysHide: () => {
			douseFire();
			totems = [];
			clearCover();
		},
		featureFxFallOut: async () => {
			douseFire();
			await fallOutFeatureFx(fallOut, show);
			totems = [];
			clearCover();
		},
	});

	$effect(() => {
		if (!show) return;
		let raf = 0;
		fireLast = 0;
		const tick = (now: number) => {
			const dt = fireLast ? now - fireLast : 16;
			fireLast = now;
			for (const totem of totems) {
				const hot = totem.ignite.current;
				const layout = layoutOf(totem.reel);
				totem.fireClock += dt * (0.9 + 3.4 * hot * hot);
				totem.fireUniforms.uTime = totem.fireClock;
				totem.fireUniforms.uIntensity = 0.55 + 0.85 * hot;
				totem.fireUniforms.uProgress = hot;
				totem.fireUniforms.uYScale = layout.fireYScale;
				totem.fireUniforms.uFlash = 0;
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
</script>

<MainContainer>
	<BoardSpace yOffset={fallOut.current}>
		{#each totems as totem (totem.reel)}
			{@const layout = layoutOf(totem.reel)}
			{@const slideY = slideYOf(totem.reel, totem.revealRow.current)}
			{@const revealBot = revealBotOf(totem.reel, totem.revealRow.current)}
			{@const showHeader = totem.startRow === 1 || slideY > -layout.headerH * 0.35}
			<Container x={layout.cx} y={layout.colTop}>
				{#if showHeader}
					<Container>
						<Rectangle
							isMask
							y={-layout.headerH}
							anchor={{ x: 0.5, y: 0 }}
							width={colW}
							height={layout.headerH}
							backgroundColor={0xffffff}
						/>
						<Sprite
							key={FEATURE_ART.nudgeColumn}
							y={-layout.headerH}
							anchor={{ x: 0.5, y: 0 }}
							width={colW}
							height={layout.spriteH}
						/>
					</Container>
				{/if}
				<Container>
					<Rectangle
						isMask
						anchor={{ x: 0.5, y: 0 }}
						width={colW}
						height={layout.fullH}
						backgroundColor={0xffffff}
					/>
					<Sprite
						key={FEATURE_ART.nudgeColumn}
						y={slideY - layout.headerH}
						anchor={{ x: 0.5, y: 0 }}
						width={colW}
						height={layout.spriteH}
					/>
				</Container>
				{#if totem.ignite.current > 0.01}
					<Container y={layout.fireY} filters={[totem.fire]}>
						<BaseSprite
							texture={Texture.WHITE}
							anchor={0.5}
							width={layout.fireQuad.w}
							height={layout.fireQuad.h}
						/>
					</Container>
				{/if}
				<MultBadge
					label={formatWaysMult(totem.ways)}
					y={revealBot + badgeH * 0.15}
					width={SYMBOL_CARD_W * 0.86}
					scale={totem.badgePop.current}
				/>
			</Container>
		{/each}
	</BoardSpace>
</MainContainer>
