<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	export type EmitterEventNudgeSlide =
		| {
				type: 'nudgeSlideShow';
				baseMult: number;
				winMult: number;
				/**
				 * The full walk, one cell per reel, ordered right-to-left and ending
				 * on the first reel's middle cell (the rider's resting place).
				 * `from` is the symbol that WAS in the cell: the handler has already
				 * swapped the whole wake to nudge WILDs, so the ghost card covering
				 * each cell has to carry the original face until the rider's impact
				 * knocks it out. `premium` marks the steps that bump the multiplier.
				 */
				steps: { reel: number; row: number; from: SymbolName; premium: boolean }[];
		  }
		| { type: 'nudgeSlideHide' };
</script>

<script lang="ts">
	/**
	 * Horizontal NUDGE — xNudge sideways. The NUDGE WILD (its own card: spur
	 * wheel, left arrows, NUDGE wordmark) is blasted out of the last-reel lane
	 * and RACKS LEFT one mechanical notch per reel: cock (a short recoil against
	 * the travel direction), slam over to the next cell — half-steps and
	 * diagonals where the diamond rows don't line up — impact. Every cell it
	 * steps through has its old card SHUNTED out along the direction of travel,
	 * uncovering the nudge wild the handler already swapped in; premium cells
	 * hit harder and bump the WIN multiplier. It comes to rest seated on the
	 * FIRST reel's middle cell and hands over to the board's own wild.
	 *
	 * Everything visible here is real art: a Layer AI iron-and-wood card frame
	 * and multiplier plaque over Kenney smoke, dust, flash and scorch (see
	 * game/featureVfx.ts). The residue is deliberately off-centre and low-alpha
	 * so the wild it marks always reads through it.
	 */
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicInOut, cubicOut, backOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_CARD_W, SYMBOL_CARD_H } from '../game/constants';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { shakeBoard, stateShake } from '../game/stateShake.svelte';
	import { FX, FEATURE_ART, seqFrame, fxRandom, puffFade } from '../game/featureVfx';
	import FeatureFxSprite from './FeatureFxSprite.svelte';
	import MultBadge from './MultBadge.svelte';
	import Symbol from './Symbol.svelte';

	const context = getContext();

	/** How far a shunted card is knocked out of its cell, as a share of card width. */
	const SHUNT_TRAVEL = 0.62;
	/** Dust puffs dragged behind the rider. */
	const TRAIL_COUNT = 7;
	/** Seconds a trail puff lives. */
	const TRAIL_LIFE = 0.5;

	type Mark = {
		key: string;
		reel: number;
		row: number;
		from: SymbolName;
		premium: boolean;
		/** unit direction of travel at impact — the shunted card leaves this way */
		kx: number;
		ky: number;
		seed: number;
		/** 0 → 1 as the impact lands: drives flash, smoke and the scorch settling */
		hit: Tween<number>;
		/** 0 → 1 as the old card is knocked out of the cell and fades */
		shunt: Tween<number>;
	};

	type TrailPuff = { key: number; x: number; y: number; born: number; seed: number };

	let show = $state(false);
	let mult = $state(1);
	let marks = $state<Mark[]>([]);
	let trail = $state<TrailPuff[]>([]);
	let time = $state(0);
	let trailKey = 0;

	const rideX = new Tween(0);
	const rideY = new Tween(0);
	const riderScale = new Tween(1);
	const riderAlpha = new Tween(1);
	const launch = new Tween(0);
	/** 0 → 1 once the rider is seated on its resting cell: drives the halo ring */
	const rest = new Tween(0);
	const badgePop = new Tween(1);
	const fallOut = new Tween(0);

	const lastReel = () => context.stateGame.board.length - 1;

	/** Board-LOCAL cell centre. Rendered under the live board origin, so a resize
	 * mid-slide moves the whole overlay with the board instead of stranding it. */
	const cellLocal = (reel: number, row: number) => ({
		x: getSymbolX(reel),
		y: getCellCenterY(reel, row),
	});

	const boardLayout = $derived(context.stateGameDerived.boardLayout());
	const originX = $derived(boardLayout.x - boardLayout.width * 0.5);
	const originY = $derived(boardLayout.y - boardLayout.height * 0.5);

	const reset = () => {
		marks = [];
		trail = [];
		fallOut.set(0, { duration: 0 });
		launch.set(0, { duration: 0 });
		rest.set(0, { duration: 0 });
	};

	const dropTrail = (x: number, y: number) => {
		trailKey += 1;
		trail = [
			...trail.filter((puff) => time - puff.born < TRAIL_LIFE),
			{ key: trailKey, x, y, born: time, seed: trailKey * 37 },
		];
	};

	const scoreCell = (
		step: { reel: number; row: number; from: SymbolName; premium: boolean },
		dir: { x: number; y: number },
		index: number,
	) => {
		const mark: Mark = {
			key: `${step.reel}-${step.row}`,
			reel: step.reel,
			row: step.row,
			from: step.from,
			premium: step.premium,
			kx: dir.x,
			ky: dir.y,
			seed: step.reel * 31 + step.row * 17 + index * 97,
			hit: new Tween(0),
			shunt: new Tween(0),
		};
		marks = [...marks, mark];
		mark.hit.set(1, { duration: fxDur(step.premium ? 620 : 460), easing: cubicOut });
		// the knocked-out card leaves fast, then the wild underneath is uncovered
		mark.shunt.set(1, { duration: fxDur(step.premium ? 380 : 300), easing: backOut });
	};

	const run = async (e: {
		baseMult: number;
		winMult: number;
		steps: { reel: number; row: number; from: SymbolName; premium: boolean }[];
	}) => {
		mult = e.baseMult;
		reset();

		const start = cellLocal(lastReel(), 1);
		rideX.set(start.x, { duration: 0 });
		rideY.set(start.y, { duration: 0 });
		riderScale.set(1, { duration: 0 });
		riderAlpha.set(1, { duration: 0 });
		show = true;

		// blasted out of the lane: the reel mechanism kicking a notch over
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_reel_nudge' });
		launch.set(1, { duration: fxDur(460), easing: cubicOut });
		await riderScale.set(1.24, { duration: fxDur(320), easing: backOut });

		// RACK LEFT, one mechanical notch per reel. Each notch: cock (a short
		// recoil against the travel direction), slam over — the y component
		// makes half-steps and diagonals read as real sideways nudges — impact.
		let prev = start;
		let index = 0;
		for (const step of e.steps) {
			const dest = cellLocal(step.reel, step.row);
			const len = Math.hypot(dest.x - prev.x, dest.y - prev.y) || 1;
			const dir = { x: (dest.x - prev.x) / len, y: (dest.y - prev.y) / len };

			// cock: the mechanism winds up before the notch slams over
			await Promise.all([
				rideX.set(prev.x - dir.x * SYMBOL_CARD_W * 0.09, {
					duration: fxDur(140),
					easing: cubicOut,
				}),
				rideY.set(prev.y - dir.y * SYMBOL_CARD_W * 0.09, {
					duration: fxDur(140),
					easing: cubicOut,
				}),
			]);
			// slam: one hard notch with a little overshoot-and-settle
			await Promise.all([
				rideX.set(dest.x, { duration: fxDur(250), easing: backOut }),
				rideY.set(dest.y, { duration: fxDur(250), easing: backOut }),
			]);

			index += 1;
			scoreCell(step, dir, index);
			if (step.premium) {
				// a premium crushed under the wild: the WIN multiplier clicks up
				mult = Math.min(e.winMult, mult + 1);
				badgePop.set(1.55, { duration: 0 });
				badgePop.set(1, { duration: fxDur(380) });
			}
			shakeBoard({
				intensity: step.premium ? 10 : 6,
				duration: fxDur(step.premium ? 260 : 180),
			});
			// each notch is another kick of the same mechanism
			context.eventEmitter.broadcast({
				type: 'soundOnce',
				name: 'sfx_reel_nudge',
				forcePlay: true,
			});
			// dwell so the shunt and the uncovered wild both read before the next notch
			await fxWait(step.premium ? 360 : 230);
			prev = dest;
		}

		// came to rest seated on the first reel's middle cell: settle, flash the
		// halo, then hand the cell over to the board's own nudge wild underneath
		mult = e.winMult;
		badgePop.set(1.55, { duration: 0 });
		badgePop.set(1, { duration: fxDur(380) });
		rest.set(1, { duration: fxDur(600), easing: cubicOut });
		await riderScale.set(1, { duration: fxDur(280), easing: backOut });
		await fxWait(460);
		await riderAlpha.set(0, { duration: fxDur(300) });
		// the rider is spent; the scorch it left behind stays until the next spin
		show = false;
		launch.set(0, { duration: 0 });
	};

	context.eventEmitter.subscribeOnMount({
		nudgeSlideShow: (e) => run(e),
		nudgeSlideHide: () => {
			show = false;
			reset();
		},
		featureFxFallOut: async () => {
			await fallOutFeatureFx(fallOut, marks.length > 0);
			show = false;
			reset();
		},
	});

	onMount(() => {
		let raf = 0;
		const started = performance.now();
		const tick = (now: number) => {
			time = (now - started) / 1000;
			if (show) dropTrail(rideX.current, rideY.current);
			else if (trail.length) trail = trail.filter((puff) => time - puff.born < TRAIL_LIFE);
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	/** The rider's frame, sized so its open centre clears the symbol art. */
	const FRAME_W = SYMBOL_CARD_W * 1.3;
	const FRAME_H = SYMBOL_CARD_H * 1.24;

	const visibleTrail = $derived(
		trail
			.map((puff) => ({ ...puff, life: (time - puff.born) / TRAIL_LIFE }))
			.filter((puff) => puff.life > 0 && puff.life < 1)
			.slice(-TRAIL_COUNT),
	);
</script>

<MainContainer>
	<Container x={stateShake.x} y={stateShake.y + fallOut.current}>
		<Container x={originX} y={originY}>
			<!-- Powder burn left on every scored cell. Hollow ring + off-centre
			scorch: the WILD underneath has to stay readable. -->
			{#each marks as mark (mark.key)}
				{@const cell = cellLocal(mark.reel, mark.row)}
				{@const lit = mark.hit.current}
				{@const knock = mark.shunt.current}
				<Container x={cell.x} y={cell.y}>
					<!-- irregular powder smudge, NOT a stamped star: a spiked burst on
					a dark card reads as a sticker glued over the symbol -->
					<FeatureFxSprite
						tex={FX.scorch[mark.seed % FX.scorch.length]}
						width={SYMBOL_CARD_W * 1.02}
						height={SYMBOL_CARD_H * 0.78}
						y={SYMBOL_CARD_H * 0.2}
						rotation={fxRandom(mark.seed) * Math.PI}
						alpha={0.32 * lit}
					/>
					<!-- a thin wisp still curling off the cell long after the impact.
					Kept small and faint: a full plume here sits on top of the wild
					the mark is supposed to be advertising. -->
					<FeatureFxSprite
						tex={FX.gunsmoke[6]}
						x={-SYMBOL_CARD_W * 0.34}
						y={-SYMBOL_CARD_H * (0.42 + 0.04 * Math.sin(time * 1.6 + mark.seed))}
						width={SYMBOL_CARD_W * 0.55}
						height={SYMBOL_CARD_W * 0.55}
						alpha={0.16 * lit}
					/>

					<!-- impact: flash, then a gunsmoke plume rolling off the cell -->
					{#if lit < 0.55}
						{@const punch = mark.premium ? 2.1 : 1.4}
						<FeatureFxSprite
							tex={seqFrame(FX.flash, lit / 0.55)}
							width={SYMBOL_CARD_W * (1.1 + lit * punch)}
							height={SYMBOL_CARD_W * (1.1 + lit * punch)}
							alpha={0.95 * (1 - lit / 0.55)}
						/>
					{/if}
					<!-- a premium crushed under the wild gets a brass ring on top of
					the flash — the beat the multiplier clicks up on -->
					{#if mark.premium && lit > 0.08 && lit < 0.9}
						<FeatureFxSprite
							tex={FX.ring}
							width={SYMBOL_CARD_W * (0.9 + lit * 1.6)}
							height={SYMBOL_CARD_W * (0.9 + lit * 1.6)}
							alpha={0.75 * (1 - lit)}
						/>
					{/if}
					{#if lit > 0.02 && lit < 0.98}
						<FeatureFxSprite
							tex={seqFrame(FX.gunsmoke, lit)}
							x={-SYMBOL_CARD_W * 0.5 * lit}
							y={-SYMBOL_CARD_H * 0.34 * lit}
							width={SYMBOL_CARD_W * (0.95 + lit * 0.6)}
							height={SYMBOL_CARD_W * (0.95 + lit * 0.6)}
							alpha={0.55 * (1 - lit)}
						/>
					{/if}
					{#each FX.dirt as dirtFrame, i}
						{@const drift = Math.min(1, lit * 1.6)}
						<FeatureFxSprite
							tex={dirtFrame}
							x={-SYMBOL_CARD_W * (0.2 + 0.5 * fxRandom(mark.seed + i)) * drift}
							y={SYMBOL_CARD_H * (0.1 - 0.5 * fxRandom(mark.seed + i * 3)) * drift}
							width={SYMBOL_CARD_W * 0.85}
							height={SYMBOL_CARD_W * 0.85}
							rotation={fxRandom(mark.seed + i * 7) * Math.PI * 2}
							alpha={0.7 * (1 - drift)}
						/>
					{/each}

					<!-- The card that was here, knocked clean out of its cell ALONG the
					rider's direction of travel (diagonal notches knock diagonally).
					It hides the wild the handler already swapped in until it clears. -->
					{#if knock < 0.995}
						<Container
							x={mark.kx * SYMBOL_CARD_W * SHUNT_TRAVEL * knock}
							y={mark.ky * SYMBOL_CARD_W * SHUNT_TRAVEL * knock -
								SYMBOL_CARD_H * 0.14 * Math.sin(knock * Math.PI)}
							rotation={(mark.kx >= 0 ? 0.42 : -0.42) * knock}
							scale={1 - 0.18 * knock}
							alpha={1 - knock * knock}
						>
							<Symbol state="static" rawSymbol={{ name: mark.from }} />
						</Container>
					{/if}
				</Container>
			{/each}

			<!-- grave dust kicked up along the ride -->
			{#each visibleTrail as puff (puff.key)}
				<FeatureFxSprite
					tex={seqFrame(FX.dust, puff.life)}
					x={puff.x}
					y={puff.y + 12 * puff.life + (fxRandom(puff.seed) - 0.5) * 14}
					width={SYMBOL_CARD_W * (0.5 + puff.life * 0.85)}
					height={SYMBOL_CARD_W * (0.5 + puff.life * 0.85)}
					rotation={fxRandom(puff.seed * 3) * Math.PI * 2}
					alpha={0.5 * puffFade(puff.life)}
				/>
			{/each}

			{#if show}
				<Container x={rideX.current} y={rideY.current} alpha={riderAlpha.current}>
					<!-- the blast that kicked the rider out of the lane, aimed LEFT
					down the ride; left behind at the lane as the card pulls away -->
					{#if launch.current > 0.01 && launch.current < 1}
						<FeatureFxSprite
							tex={seqFrame(FX.muzzle, launch.current)}
							x={SYMBOL_CARD_W * 0.5}
							width={SYMBOL_CARD_W * (1.4 + launch.current * 1.2)}
							height={SYMBOL_CARD_W * (1.4 + launch.current * 1.2)}
							rotation={-Math.PI * 0.5}
							alpha={0.85 * (1 - launch.current)}
						/>
					{/if}

					<Container scale={riderScale.current}>
						<!-- speed streaks trailing back toward the lane it came from -->
						{#each FX.trace as traceFrame, i}
							<FeatureFxSprite
								tex={traceFrame}
								x={SYMBOL_CARD_W * (0.62 + i * 0.26)}
								y={SYMBOL_CARD_H * (fxRandom(i * 13) - 0.5) * 0.5}
								width={SYMBOL_CARD_W * (0.9 - i * 0.12)}
								height={SYMBOL_CARD_H * 0.5}
								rotation={Math.PI * 0.5}
								alpha={(0.5 - i * 0.13) * (0.8 + 0.2 * Math.sin(time * 13 + i))}
							/>
						{/each}
						<!-- the rider has to out-read a very dark board of near-black
						cards, so it carries its own lantern glow behind the frame -->
						<FeatureFxSprite
							tex={FX.glow}
							width={SYMBOL_CARD_W * 2.4}
							height={SYMBOL_CARD_W * 2.4}
							alpha={0.5 + 0.08 * Math.sin(time * 9)}
						/>
						<!-- the rider IS the nudge wild — spur wheel, left arrows,
						NUDGE wordmark (its own card, not a premium's face) -->
						<Symbol state="static" rawSymbol={{ name: 'W', nudged: true }} />
						<!-- iron-and-wood frame over the card. Its centre is open art,
						so it rims the symbol instead of covering it — this replaced a
						flat stroked roundRect that read as an empty outlined cell. -->
						<Sprite
							key={FEATURE_ART.riderFrame}
							anchor={0.5}
							width={FRAME_W}
							height={FRAME_H}
						/>
						<!-- hot core at the leading edge, the direction of travel -->
						<FeatureFxSprite
							tex={FX.flash[0]}
							x={-SYMBOL_CARD_W * 0.62}
							width={SYMBOL_CARD_W * 0.7}
							height={SYMBOL_CARD_W * 0.7}
							alpha={0.5 + 0.15 * Math.sin(time * 17)}
						/>

						<!-- seated: a halo ring blooms once the walk is over, the beat
						where the rider hands the cell to the board's own wild -->
						{#if rest.current > 0.02 && rest.current < 0.98}
							<FeatureFxSprite
								tex={FX.ring}
								width={SYMBOL_CARD_W * (1.0 + rest.current * 1.8)}
								height={SYMBOL_CARD_W * (1.0 + rest.current * 1.8)}
								alpha={0.85 * (1 - rest.current)}
							/>
						{/if}

						<MultBadge
							label={`x${mult}`}
							y={SYMBOL_CARD_H * 0.6}
							width={SYMBOL_CARD_W * 0.86}
							scale={badgePop.current}
						/>
					</Container>
				</Container>
			{/if}
		</Container>
	</Container>
</MainContainer>
