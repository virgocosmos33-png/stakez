<script lang="ts" module>
	import type { Position } from '../game/types';

	/** Which feature is firing. One overlay serves them all so the western FX
	 * language stays in one place instead of drifting per event. */
	export type FeatureBurstKind = 'gunsmoke' | 'coffinOpen' | 'digUp' | 'bounty';

	export type EmitterEventFeatureBurst =
		| { type: 'featureBurstShow'; kind: FeatureBurstKind; cells: Position[] }
		| { type: 'featureBurstHide' };
</script>

<script lang="ts">
	/**
	 * The western presentation for the non-split feature events.
	 *
	 *   gunsmoke   a revolver fires across the board and every copy of the
	 *              symbol is swallowed by powder smoke
	 *   coffinOpen the plot bursts: lid debris, thrown spoil, and a shaft of
	 *              lantern light standing out of the opened grave
	 *   digUp      a spade is driven into each dug cell and left standing in it
	 *   bounty     a lantern-gold bloom swells behind the bountied card
	 *
	 * Every burst is anchored on VISIBLE cells only (the diamond board pads its
	 * short reels) and is composed from real art — Scenario hero plates plus the
	 * Kenney smoke / dirt / flash / light families, see game/featureVfx.ts.
	 *
	 * Nothing here is allowed to sit opaque over a card: plumes and smoke are
	 * offset off the card centre, and glows stay below half alpha.
	 */
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite, Rectangle } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import type { SoundEffectName } from '../game/sound';
	import { SYMBOL_CARD_W, SYMBOL_CARD_H } from '../game/constants';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { fxDur } from '../game/fxTiming';
	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { FX, FEATURE_FX, FEATURE_ART, seqFrame, fxRandom, puffFade } from '../game/featureVfx';
	import FeatureFxSprite from './FeatureFxSprite.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	/** How long each kind's burst takes to play out, in ms at normal speed. */
	const BURST_MS: Record<FeatureBurstKind, number> = {
		gunsmoke: 900,
		coffinOpen: 1000,
		// long enough that the spades finish landing and then hold, planted,
		// while the player reads which cells were dug
		digUp: 1700,
		bounty: 820,
	};
	/** Debris thrown per cell. */
	const DEBRIS = 7;

	/**
	 * Spade size, in card units. The blade tip sits at BLADE_Y — below the
	 * symbol's middle, in the card's lower band — and the handle runs up past
	 * the card's top edge, which is what sells "left standing in the dirt".
	 * The width is derived from the height so the art never squashes.
	 */
	const SHOVEL_H = SYMBOL_CARD_H * 1.05;
	/** source plate aspect, so the spade never squashes */
	const SHOVEL_W = SHOVEL_H * 0.196;
	const BLADE_Y = SYMBOL_CARD_H * 0.36;

	/** Gap between one spade landing and the next, as a fraction of the burst. */
	const DIG_STAGGER = 0.07;
	/** Time from the spade entering frame to the blade biting. */
	const DIG_STRIKE = 0.11;
	/** How long the handle rings after the bite before it damps to rest. */
	const DIG_WOBBLE = 0.3;

	/**
	 * Where one cell's spade is, and how it is behaving, at burst progress
	 * `progress`. Everything is derived — no per-frame Graphics rebuilds — and
	 * every value is seeded so a replay looks identical.
	 */
	const shovelPlant = (seed: number, order: number, progress: number) => {
		// The mirror is a container scale, never a negative sprite width: Pixi's
		// width setter re-reads the current scale sign, so a negative width
		// flip-flops the sprite on every frame it is written.
		const flip = fxRandom(seed * 3 + 1) > 0.5 ? -1 : 1;
		const lean = 0.1 + (fxRandom(seed * 7 + 5) - 0.5) * 0.16;
		const x = SYMBOL_CARD_W * (0.16 + fxRandom(seed * 11 + 2) * 0.06);
		const local = progress - order * DIG_STAGGER;
		if (local <= 0) {
			return { x, flip, dy: 0, angle: lean, alpha: 0, bite: 0, since: 0 };
		}
		const drop = Math.min(1, local / DIG_STRIKE);
		const since = Math.max(0, local - DIG_STRIKE);
		const ringing = since < DIG_WOBBLE ? 1 - since / DIG_WOBBLE : 0;
		return {
			x,
			flip,
			// accelerating fall: the blade is fastest at the moment it lands
			dy: -SYMBOL_CARD_H * 1.15 * (1 - drop * drop),
			angle: lean + Math.sin(since * 74) * 0.07 * ringing * ringing,
			alpha: Math.min(1, local / 0.04) * Math.min(1, (1 - progress) / 0.1),
			bite: since > 0 ? Math.min(1, since * 8) : 0,
			since: Math.min(1, since / 0.6),
		};
	};

	let kind = $state<FeatureBurstKind>('gunsmoke');
	let cells = $state<Position[]>([]);
	const burst = new Tween(0);
	const fallOut = new Tween(0);


	const placed = $derived(
		cells.map((cell, order) => ({
			key: `${cell.reel}-${cell.row}`,
			x: getSymbolX(cell.reel),
			y: getCellCenterY(cell.reel, cell.row),
			seed: cell.reel * 41 + cell.row * 13,
			order,
		})),
	);

	const t = $derived(burst.current);
	/** rises fast, holds, then clears */
	const settle = $derived(Math.min(1, t * 3));

	/** One cue per feature for the events that read as a single action. */
	const BURST_SFX: Record<Exclude<FeatureBurstKind, 'digUp'>, SoundEffectName> = {
		gunsmoke: 'sfx_gunsmoke',
		coffinOpen: 'sfx_tombstone_open',
		bounty: 'sfx_bounty',
	};

	/**
	 * digUp is the one burst that cannot take a single cue, because each cell
	 * visibly gets its own spade. It cannot take one cue PER cell either: the
	 * blades bite roughly 50ms apart, so five cells would be a machine-gun of
	 * near-identical thunks. So it gets the same treatment as a split volley —
	 * a capped number of hits, spaced far enough apart to read as separate
	 * impacts, each a genuinely different take rather than one clip repitched.
	 * The handle shiver is one event-level accent after the last blade lands,
	 * not one per cell.
	 */
	const SHOVEL_STRIKES = [
		'sfx_shovel_strike_1',
		'sfx_shovel_strike_2',
		'sfx_shovel_strike_3',
	] as const;
	const SHOVEL_MAX_HITS = SHOVEL_STRIKES.length;
	const SHOVEL_GAP_MS = 90;
	const SHOVEL_SETTLE_MS = 220;

	let sfxTimers: number[] = [];
	const clearSfxTimers = () => {
		sfxTimers.forEach((timer) => window.clearTimeout(timer));
		sfxTimers = [];
	};
	const playLater = (name: SoundEffectName, delayMs: number) => {
		sfxTimers.push(
			window.setTimeout(
				() => context.eventEmitter.broadcast({ type: 'soundOnce', name, forcePlay: true }),
				delayMs,
			),
		);
	};

	const playBurstSfx = (burstKind: FeatureBurstKind, cellCount: number) => {
		// a new burst supersedes anything still queued from the previous one
		clearSfxTimers();
		if (burstKind !== 'digUp') {
			context.eventEmitter.broadcast({ type: 'soundOnce', name: BURST_SFX[burstKind] });
			return;
		}
		const hits = Math.min(cellCount, SHOVEL_MAX_HITS);
		// rotate the starting take so a repeat dig is not the same three thunks
		const first = Math.floor(fxRandom(cellCount * 13 + 7) * SHOVEL_STRIKES.length);
		for (let hit = 0; hit < hits; hit += 1) {
			playLater(SHOVEL_STRIKES[(first + hit) % SHOVEL_STRIKES.length], fxDur(hit * SHOVEL_GAP_MS));
		}
		playLater('sfx_shovel_settle', fxDur((hits - 1) * SHOVEL_GAP_MS + SHOVEL_SETTLE_MS));
	};

	const clear = () => {
		clearSfxTimers();
		cells = [];
		burst.set(0, { duration: 0 });
		fallOut.set(0, { duration: 0 });
	};

	onDestroy(clearSfxTimers);

	context.eventEmitter.subscribeOnMount({
		featureBurstShow: async (event) => {
			kind = event.kind;
			cells = event.cells;
			if (!cells.length) return;
			burst.set(0, { duration: 0 });
			playBurstSfx(event.kind, cells.length);
			await burst.set(1, { duration: fxDur(BURST_MS[event.kind]), easing: cubicOut });
		},
		featureBurstHide: () => clear(),
		featureFxFallOut: async () => {
			await fallOutFeatureFx(fallOut, cells.length > 0);
			clear();
		},
	});

</script>

<MainContainer>
	{#if cells.length > 0 && t < 1}
		<BoardSpace yOffset={fallOut.current}>
				{#each placed as cell (cell.key)}
					<Container x={cell.x} y={cell.y}>
						{#if kind === 'gunsmoke'}
							<!-- the shot itself, then the powder cloud rolling off the card -->
							{#if t < 0.3}
								<Sprite
									key={FEATURE_ART.muzzleFlash}
									anchor={0.5}
									x={SYMBOL_CARD_W * (1.5 - t * 3)}
									width={SYMBOL_CARD_W * 2.1}
									height={SYMBOL_CARD_H * 0.9}
									alpha={Math.min(1, t / 0.08) * (1 - t / 0.3)}
								/>
							{/if}
							{#if t < 0.42}
								<FeatureFxSprite
									tex={seqFrame(FX.muzzle, t / 0.42)}
									width={SYMBOL_CARD_W * (1 + t * 2.4)}
									height={SYMBOL_CARD_W * (1 + t * 2.4)}
									alpha={0.9 * (1 - t / 0.42)}
									blendMode="add"
								/>
							{/if}
							<!-- the plume climbs OFF the top of the card: parked over the
							card centre it just reads as a white sticker on the symbol -->
							<FeatureFxSprite
								tex={seqFrame(FX.gunsmoke, t)}
								x={-SYMBOL_CARD_W * 0.3 * t}
								y={-SYMBOL_CARD_H * (0.34 + 0.72 * t)}
								width={SYMBOL_CARD_W * (1.05 + t * 1.2)}
								height={SYMBOL_CARD_W * (1.05 + t * 1.2)}
								alpha={0.7 * puffFade(t)}
							/>
							<FeatureFxSprite
								tex={FX.scorch[cell.seed % FX.scorch.length]}
								width={SYMBOL_CARD_W * 0.95}
								height={SYMBOL_CARD_H * 0.7}
								rotation={fxRandom(cell.seed) * Math.PI}
								alpha={0.24 * settle * (1 - t * 0.6)}
							/>
						{/if}

						{#if kind === 'coffinOpen'}
							<!-- lantern light standing out of the opened plot. The shaft
							is a light mask over a near-black board, so it needs real
							alpha to register at all — at a third it was invisible. -->
							<FeatureFxSprite
								tex={FX.shaft[cell.seed % FX.shaft.length]}
								y={-SYMBOL_CARD_H * (0.5 + 0.55 * settle)}
								width={SYMBOL_CARD_W * 1.3}
								height={SYMBOL_CARD_H * 2.4 * settle}
								alpha={0.7 * settle * (1 - t * 0.55)}
								blendMode="add"
							/>
							<!-- the lid letting go: a lit blast of spoil out of the plot,
							thrown up the card rather than parked on the symbol -->
							{#if t < 0.55}
								<FeatureFxSprite
									tex={seqFrame(FX.burst, t / 0.55)}
									y={SYMBOL_CARD_H * (0.42 - 0.75 * t)}
									width={SYMBOL_CARD_W * (0.95 + t * 0.9)}
									height={SYMBOL_CARD_W * (0.95 + t * 0.9)}
									alpha={0.95 * (1 - t / 0.55)}
								/>
							{/if}
							<!-- a flare at the moment the lid gives, so the beat has a
							front edge instead of only a slow cloud -->
							{#if t < 0.22}
								<FeatureFxSprite
									tex={FX.flash[0]}
									y={SYMBOL_CARD_H * 0.36}
									width={SYMBOL_CARD_W * (0.9 + t * 4)}
									height={SYMBOL_CARD_W * (0.9 + t * 4)}
									alpha={0.8 * (1 - t / 0.22)}
									blendMode="add"
								/>
							{/if}
							<!-- grave spoil thrown onto the sill, kept at the card's foot -->
							<FeatureFxSprite
								tex={FX.splat[cell.seed % FX.splat.length]}
								y={SYMBOL_CARD_H * 0.44}
								width={SYMBOL_CARD_W * 0.95}
								height={SYMBOL_CARD_W * 0.42}
								alpha={0.45 * settle * (1 - t * 0.6)}
							/>
						{/if}

						{#if kind === 'digUp'}
							{@const plant = shovelPlant(cell.seed, cell.order, t)}
						<Container scale={{ x: plant.flip, y: 1 }}>
							<!-- THE IMPACT ON THE CARD, CLIPPED TO THE CELL. The gouge and
								the turned-earth scar are damage ON the symbol, so they are
								masked to the card rectangle: the strike decal is near
								card-sized and rotated, and without a mask its corners spill
								over the frame onto the neighbouring cell / the graveyard.
								The mask keeps every mark framed inside its own cell. The
								spade, smoke, thrown spoil and flash below are NOT masked —
								those are meant to stand up out of the cell and rise off it. -->
							<Container>
								<Rectangle
									isMask
									anchor={0.5}
									width={SYMBOL_CARD_W}
									height={SYMBOL_CARD_H}
									backgroundColor={0xffffff}
								/>
								<!-- The instant the blade bites, a cracked-strike decal is
									stamped ON the symbol — a gouge with cracks radiating
									across the face — and stays for the rest of the event so the
									hit is FELT on the card. Cracks on transparency, so it marks
									the symbol without washing it out. -->
								<Sprite
									key={FEATURE_ART.digImpact}
									anchor={0.5}
									x={plant.x * 0.55}
									y={BLADE_Y * 0.5}
									width={SYMBOL_CARD_W * (0.7 + 0.28 * plant.bite)}
									height={SYMBOL_CARD_H * (0.62 + 0.25 * plant.bite)}
									rotation={(fxRandom(cell.seed * 5 + 3) - 0.5) * 0.5}
									alpha={0.92 * plant.bite}
								/>
								<!-- turned earth where the blade went in -->
								<Sprite
									key={FEATURE_ART.digScar}
									anchor={0.5}
									x={plant.x}
									y={BLADE_Y - SYMBOL_CARD_H * 0.02}
									width={SYMBOL_CARD_W * 0.52}
									height={SYMBOL_CARD_H * 0.17}
									alpha={0.85 * plant.bite}
								/>
							</Container>
								<!-- the spade itself: fast strike down, then planted for
								the rest of the event so the dug cells stay readable. It
								sits to one side, so the symbol keeps the card's middle. -->
								<Sprite
									key={FEATURE_ART.shovel}
									anchor={{ x: 0.5, y: 1 }}
									x={plant.x}
									y={BLADE_Y + plant.dy}
									width={SHOVEL_W}
									height={SHOVEL_H}
									rotation={plant.angle}
									alpha={plant.alpha}
								/>
								<!-- spoil thrown over the blade tip, which is what makes the
								blade read as buried rather than resting on the card -->
								<FeatureFxSprite
									tex={FX.splat[cell.seed % FX.splat.length]}
									x={plant.x}
									y={BLADE_Y - SYMBOL_CARD_H * 0.03}
									width={SYMBOL_CARD_W * 0.36}
									height={SYMBOL_CARD_W * 0.16}
									alpha={0.7 * plant.bite}
								/>
							<!-- THE BREAK: the instant the blade bites, the cell cracks
							open in a burst of dirt and smoke so the strike reads as a
							real impact, not a spade quietly placed on the card. -->
							{#if plant.bite > 0 && plant.since < 0.95}
								<!-- crack flash at the moment of contact, earthy not white -->
								{#if plant.since < 0.28}
									<FeatureFxSprite
										tex={FX.flash[0]}
										x={plant.x}
										y={BLADE_Y - SYMBOL_CARD_H * 0.02}
										width={SYMBOL_CARD_W * (0.6 + plant.since * 4.4)}
										height={SYMBOL_CARD_W * (0.6 + plant.since * 4.4)}
										alpha={0.95 * (1 - plant.since / 0.28)}
										tint={FEATURE_FX.sand}
										blendMode="add"
									/>
								{/if}
								<!-- smoke rolling up off the broken ground: two offset plumes
								so the break reads as a real cloud, not a single wisp -->
								<FeatureFxSprite
									tex={seqFrame(FX.gunsmoke, plant.since / 0.95)}
									x={plant.x - SYMBOL_CARD_W * 0.08}
									y={BLADE_Y - SYMBOL_CARD_H * (0.12 + 0.72 * plant.since)}
									width={SYMBOL_CARD_W * (0.9 + plant.since * 1.5)}
									height={SYMBOL_CARD_W * (0.9 + plant.since * 1.5)}
									alpha={0.85 * puffFade(plant.since)}
								/>
								<FeatureFxSprite
									tex={seqFrame(FX.gunsmoke, Math.min(0.999, plant.since / 0.95 + 0.35))}
									x={plant.x + SYMBOL_CARD_W * 0.12}
									y={BLADE_Y - SYMBOL_CARD_H * (0.06 + 0.5 * plant.since)}
									width={SYMBOL_CARD_W * (0.7 + plant.since * 1.1)}
									height={SYMBOL_CARD_W * (0.7 + plant.since * 1.1)}
									alpha={0.62 * puffFade(plant.since)}
								/>
								<!-- kicked dirt haze at the entry, sand-toned -->
								<FeatureFxSprite
									tex={seqFrame(FX.dust, Math.min(0.999, plant.since / 0.6))}
									x={plant.x}
									y={BLADE_Y - SYMBOL_CARD_H * 0.3 * plant.since}
									width={SYMBOL_CARD_W * (0.75 + plant.since * 1.2)}
									height={SYMBOL_CARD_W * (0.56 + plant.since * 0.84)}
									alpha={0.9 * (1 - plant.since / 0.95)}
									tint={FEATURE_FX.sand}
								/>
								<!-- thrown spoil: a wide spray of turned earth flung out of
								the break, arcing up then falling back -->
								{#each { length: 12 } as _, i}
									{@const spread = fxRandom(cell.seed + i * 7)}
									{@const lift = fxRandom(cell.seed + i * 13)}
									{@const p = Math.min(1, plant.since / 0.6)}
									<FeatureFxSprite
										tex={FX.dirt[i % FX.dirt.length]}
										x={plant.x + (spread - 0.5) * SYMBOL_CARD_W * 1.5 * p}
										y={BLADE_Y -
											SYMBOL_CARD_H * ((0.24 + lift * 0.45) * p - 1.15 * p * p)}
										width={SYMBOL_CARD_W * (0.2 + lift * 0.14)}
										height={SYMBOL_CARD_W * (0.2 + lift * 0.14)}
										rotation={p * (spread - 0.5) * 11}
										alpha={0.9 * (1 - p * 0.9)}
									/>
								{/each}
							{/if}
							</Container>
						{/if}

						{#if kind === 'bounty'}
							<!-- Lantern-gold bloom behind the bountied card. This used to
							be a multi-point starburst plate, which on a dark board read
							as a fan of hard grey-white triangles laid over the art — the
							stray-spike look the feature set was rejected for. A soft
							additive bloom carries the same "this card just paid" beat
							without putting a single hard edge over the symbol. -->
							<FeatureFxSprite
								tex={FX.glow}
								width={SYMBOL_CARD_W * (1.5 + 1.4 * settle)}
								height={SYMBOL_CARD_W * (1.5 + 1.4 * settle)}
								alpha={0.75 * settle * (1 - t * 0.55)}
								blendMode="add"
							/>
							{#if t < 0.4}
								<FeatureFxSprite
									tex={seqFrame(FX.flash, t / 0.4)}
									width={SYMBOL_CARD_W * (0.7 + t * 3)}
									height={SYMBOL_CARD_W * (0.7 + t * 3)}
									alpha={0.85 * (1 - t / 0.4)}
									blendMode="add"
								/>
							{/if}
							<!-- gold dust lifting off the card, kept off its centre -->
							<FeatureFxSprite
								tex={seqFrame(FX.dust, t)}
								y={SYMBOL_CARD_H * (0.4 - 0.5 * t)}
								width={SYMBOL_CARD_W * (0.9 + t * 1.1)}
								height={SYMBOL_CARD_W * (0.9 + t * 1.1)}
								alpha={0.45 * puffFade(t)}
							/>
						{/if}

						<!-- thrown debris: dirt clods for the grave features, spent brass
						for the shot ones. digUp is excluded — its spoil is thrown from
						the blade's entry point on that cell's own strike timing. -->
						{#each kind === 'digUp' ? [] : { length: DEBRIS } as _, i}
							{@const spread = fxRandom(cell.seed + i * 7)}
							{@const lift = fxRandom(cell.seed + i * 13)}
							{@const grave = kind === 'coffinOpen'}
							{@const frames = grave ? FX.dirt : FX.spark}
							<FeatureFxSprite
								tex={frames[i % frames.length]}
								x={(spread - 0.5) * SYMBOL_CARD_W * 2.4 * t}
								y={SYMBOL_CARD_H * (0.2 - (0.4 + lift * 0.9) * t + 1.5 * t * t)}
								width={SYMBOL_CARD_W * (grave ? 0.6 : 0.42)}
								height={SYMBOL_CARD_W * (grave ? 0.6 : 0.42)}
								rotation={t * (spread - 0.5) * 9}
								alpha={0.85 * puffFade(t)}
							/>
						{/each}
					</Container>
				{/each}
		</BoardSpace>
	{/if}
</MainContainer>
