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
	 * One full-reel NUDGE coffin per reel. Closed lid first; after the
	 * drop the cover slides down and the open interior + ways mark sit
	 * inside. No old NUDGE header plaque.
	 */
	import { Texture } from 'pixi.js';
	import { Tween } from 'svelte/motion';
	import { cubicIn } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite, Rectangle, BaseSprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { NUDGE_COFFIN_Z, SYMBOL_CARD_W, SYMBOL_CARD_H } from '../game/constants';
	import { getCellCenterY, getCardHeight, getReelPocket, getReelRows } from '../game/utils';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { shakeBoard } from '../game/stateShake.svelte';
	import {
		FEATURE_ART,
		FEATURE_FX,
		FX,
		fxRandom,
		nudgeCoffinOpenKey,
		puffFade,
		seqFrame,
	} from '../game/featureVfx';
	import { playThemedOnce } from '../game/sfxTheme';
	import FeatureFxSprite from './FeatureFxSprite.svelte';
	import {
		createFireRingFilter,
		FIRE_RATIO,
		fireQuadSize,
		type RingUniforms,
	} from './LinkedCellFire.svelte';
	import { formatWaysMult } from '../game/waysFormat';
	import MultBadge from './MultBadge.svelte';
	import BoardSpace from './BoardSpace.svelte';

	/** Sheet canvas after uniform install (tools/install_nudge_coffin_sheet.py). */
	const COFFIN_ART_W = 681;
	const COFFIN_ART_H = 1674;
	/** Width-only squeeze. Height stays the reel. */
	const COFFIN_WIDTH_TIGHT = 0.81;
	/** Ways mark sits on the crossed hands, not under the foot. */
	const MULT_INSIDE = 0.60;
	const LID_MS = 540;
	/** Empty hold after the coffin seats, before the lid slides. */
	const LID_HOLD_MS = 500;
	const DUST_LIFE = 0.62;
	const DUST_GAP = 0.12;
	const COL_BOX_X = 0.58;
	const COL_BOX_Y = 0.72;

	const context = getContext();

	type Totem = {
		reel: number;
		startRow: number;
		/** Landed 2–9. Coffin art stays on this, not the doubled stamp. */
		initialWays: number;
		ways: number;
		revealRow: Tween<number>;
		badgePop: Tween<number>;
		lid: Tween<number>;
		ignite: Tween<number>;
		fire: ReturnType<typeof createFireRingFilter>;
		fireUniforms: RingUniforms;
		fireClock: number;
		dustEmit: number;
	};

	type LidDust = {
		key: number;
		reel: number;
		x: number;
		y: number;
		life: number;
		seed: number;
		size: number;
		dirt: boolean;
	};

	let totems = $state<Totem[]>([]);
	let lidDust = $state<LidDust[]>([]);
	const fallOut = new Tween(0);
	let fireLast = 0;
	let dustClock = 0;
	let dustKey = 0;

	const colW = SYMBOL_CARD_W;
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
		const totemTop = 0;
		const totemBot = fullH;
		const totemH = Math.max(1, totemBot - totemTop);
		const coffinH = fullH;
		const coffinW = coffinH * (COFFIN_ART_W / COFFIN_ART_H) * COFFIN_WIDTH_TIGHT;
		return {
			cx: (pocket.left + pocket.right) / 2,
			colTop: pocket.top,
			fullH,
			coffinH,
			coffinW,
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
				initialWays: e.initialWays,
				ways: e.initialWays,
				revealRow: new Tween(reveal),
				badgePop: new Tween(1),
				lid: new Tween(0),
				ignite: new Tween(0),
				fireClock: 0,
				dustEmit: 0,
				...makeFire(),
			} satisfies Totem);
		totem.startRow = startRow;
		totem.initialWays = e.initialWays;
		totem.ways = e.initialWays;
		totem.revealRow.set(reveal, { duration: 0 });
		totem.badgePop.set(1, { duration: 0 });
		totem.lid.set(0, { duration: 0 });
		totem.ignite.set(0, { duration: 0 });
		totem.dustEmit = 0;
		fallOut.set(0, { duration: 0 });
		coverStack(e.reel, startRow, reveal);
		if (!existing) totems = [...totems, totem];
		else totems = [...totems];
	};

	const spawnDust = (
		reel: number,
		x: number,
		y: number,
		seed: number,
		size: number,
		dirt = false,
	) => {
		dustKey += 1;
		lidDust = [
			...lidDust.filter((puff) => puff.life < 1),
			{ key: dustKey, reel, x, y, life: 0, seed, size, dirt },
		];
	};

	const kickLidDust = (totem: Totem) => {
		const layout = layoutOf(totem.reel);
		const slideY = slideYOf(totem.reel, totem.revealRow.current);
		const coffinY = slideY - (layout.coffinH - layout.fullH) * 0.5;
		for (let i = 0; i < 3; i++) {
			const seed = totem.reel * 71 + i * 19 + 5;
			spawnDust(
				totem.reel,
				(fxRandom(seed) - 0.5) * layout.coffinW * 0.62,
				coffinY + layout.coffinH * (0.02 + fxRandom(seed + 1) * 0.08),
				seed,
				0.55 + fxRandom(seed + 2) * 0.35,
				i === 2,
			);
		}
		totem.dustEmit = dustClock;
	};

	const openLid = async (totem: Totem) => {
		if (totem.lid.current > 0.95) return;
		await fxWait(LID_HOLD_MS);
		playThemedOnce('sfx_nudge_reveal', { forcePlay: true });
		kickLidDust(totem);
		await totem.lid.set(1, { duration: fxDur(LID_MS), easing: cubicIn });
	};

	const igniteFire = async (totem: Totem) => {
		if (totem.ignite.current > 0.01 || totem.ignite.target === 1) return;
		// Visual only. No slam — the lid already did the beat.
		await totem.ignite.set(1, { duration: fxDur(240), easing: cubicIn });
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
			await openLid(totem);
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
			playThemedOnce('sfx_nudge', { forcePlay: true });
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

		await openLid(totem);
		punchWays(totem, e.finalWays);
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
			lidDust = [];
			totems = [];
			clearCover();
		},
		featureFxFallOut: async () => {
			douseFire();
			await fallOutFeatureFx(fallOut, show);
			lidDust = [];
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
			dustClock = now / 1000;
			for (const totem of totems) {
				const hot = totem.ignite.current;
				const layout = layoutOf(totem.reel);
				totem.fireClock += dt * (0.9 + 3.4 * hot * hot);
				totem.fireUniforms.uTime = totem.fireClock;
				totem.fireUniforms.uIntensity = 0.55 + 0.85 * hot;
				totem.fireUniforms.uProgress = hot;
				totem.fireUniforms.uYScale = layout.fireYScale;
				totem.fireUniforms.uFlash = 0;
				const lid = totem.lid.current;
				if (lid > 0.04 && lid < 0.97 && dustClock - totem.dustEmit >= DUST_GAP) {
					totem.dustEmit = dustClock;
					const slideY = slideYOf(totem.reel, totem.revealRow.current);
					const coffinY = slideY - (layout.coffinH - layout.fullH) * 0.5;
					const lipY = coffinY + lid * layout.coffinH;
					const seed = totem.reel * 53 + Math.floor(lid * 40);
					spawnDust(
						totem.reel,
						(fxRandom(seed) - 0.5) * layout.coffinW * 0.55,
						lipY,
						seed,
						0.4 + fxRandom(seed + 3) * 0.32,
					);
					if (fxRandom(seed + 9) > 0.45) {
						spawnDust(
							totem.reel,
							(fxRandom(seed + 7) > 0.5 ? 0.36 : -0.36) * layout.coffinW,
							lipY + layout.cardH * 0.04,
							seed + 11,
							0.32 + fxRandom(seed + 8) * 0.22,
							true,
						);
					}
				}
			}
			if (lidDust.length) {
				const step = dt / 1000 / DUST_LIFE;
				lidDust = lidDust
					.map((puff) => ({ ...puff, life: puff.life + step }))
					.filter((puff) => puff.life < 1);
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
</script>

<Container zIndex={NUDGE_COFFIN_Z} eventMode="none">
<MainContainer>
	<BoardSpace yOffset={fallOut.current}>
		{#each totems as totem (totem.reel)}
			{@const layout = layoutOf(totem.reel)}
			{@const slideY = slideYOf(totem.reel, totem.revealRow.current)}
			{@const coffinY = slideY - (layout.coffinH - layout.fullH) * 0.5}
			{@const lid = totem.lid.current}
			{@const badgeAlpha = Math.min(1, Math.max(0, (lid - 0.35) / 0.4))}
			<Container x={layout.cx} y={layout.colTop}>
				<Container>
					<Rectangle
						isMask
						anchor={{ x: 0.5, y: 0 }}
						width={layout.coffinW}
						height={layout.fullH}
						backgroundColor={0xffffff}
					/>
					<Sprite
						key={nudgeCoffinOpenKey(totem.initialWays)}
						y={coffinY}
						anchor={{ x: 0.5, y: 0 }}
						width={layout.coffinW}
						height={layout.coffinH}
					/>
					<Sprite
						key={FEATURE_ART.nudgeCoffinCover}
						y={coffinY + lid * layout.coffinH}
						anchor={{ x: 0.5, y: 0 }}
						width={layout.coffinW}
						height={layout.coffinH}
					/>
				</Container>
				{#each lidDust.filter((puff) => puff.reel === totem.reel) as puff (puff.key)}
					{@const t = puff.life}
					{@const span = layout.coffinW * (0.26 + t * 0.2) * puff.size}
					<FeatureFxSprite
						tex={puff.dirt
							? FX.dirt[Math.floor(fxRandom(puff.seed + 4) * FX.dirt.length)]
							: seqFrame(FX.dust, t)}
						x={puff.x + (fxRandom(puff.seed) - 0.5) * layout.coffinW * 0.1 * t}
						y={puff.y - layout.cardH * 0.16 * t}
						width={span}
						height={span}
						rotation={fxRandom(puff.seed * 3) * Math.PI * 2}
						alpha={(puff.dirt ? 0.34 : 0.4) * puffFade(t)}
						tint={puff.dirt ? FEATURE_FX.powder : FEATURE_FX.sand}
					/>
				{/each}
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
					y={coffinY + layout.coffinH * MULT_INSIDE}
					width={SYMBOL_CARD_W * 0.58}
					scale={totem.badgePop.current}
					alpha={badgeAlpha}
				/>
			</Container>
		{/each}
	</BoardSpace>
</MainContainer>
</Container>
