<script lang="ts">
	/**
	 * Tombstone Reborn big-win takeover.
	 *
	 * Each tier shows a dark western hero plate inside a weathered timber and
	 * branded-iron frame, lit by god-rays, drifting grave dust and rising gold
	 * embers, and punched on entry by a gold starburst with radiating spark
	 * streaks. BOOT HILL (max win) adds slow expanding bell rings.
	 *
	 * What this replaced: the ladder used to play Madam Mirror's `celebT2..celebT7`
	 * media — photographic "White Room" footage of a straitjacketed woman in a
	 * padded asylum cell, tier 7 a literal white-out — inside a thin amber
	 * CCTV-monitor bezel with CRT screen-tear and scanline damage, titled
	 * INTAKE / RESTRAINT / STRUGGLE / BREAKOUT / SCRATCH / WHITEOUT in the
	 * condensed light-grey `clinical` face.
	 *
	 * Art: tools/make_win_celebration_art.py, contract in game/winCelebrationArt.ts.
	 *
	 * Performance: the amount count-up runs every frame, so every animated layer
	 * here is a sprite transform (x/y/rotation/scale/alpha). The only Graphics in
	 * the tree are `Rectangle`s with constant geometry, which therefore never
	 * redraw during a count-up. Do not add a time-dependent `draw` callback.
	 */
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { Rectangle as HitRectangle, type Texture } from 'pixi.js';
	import { BaseSprite, Container, Rectangle, Sprite, BitmapText } from 'pixi-svelte';
	import { ResponsiveBitmapText } from 'components-pixi';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { getTiersPassed } from '../game/winCelebrationMap';
	import { waysLabel } from '../game/waysFormat';
	import { currentModeMusic } from '../game/bonusBgm';
	import {
		CELEB_SCENE_MS,
		celebSceneDurationMs,
		isCelebSceneBgm,
		playCelebSceneBgm,
		stopCelebSceneBgm,
	} from '../game/celebSceneBgm';
	import type { MusicName, SoundEffectName } from '../game/sound';
	import { winFontFamily, winFontSize, winFontTint } from '../game/winFont';
	import {
		WIN_CELEB_LIGHT_ASSET,
		WIN_CELEB_VFX_ASSET,
		WIN_FRAME_ASSET,
		WIN_LIGHT,
		WIN_PALETTE,
		WIN_VFX,
		WIN_VFX_CELL,
		winRand,
		winTierIntensity,
		winTierPlateKey,
	} from '../game/winCelebrationArt';

	type Props = {
		finalAmount: number; // book amount (100 = 1x bet)
		ways?: number; // ways that connected this spin, shown under the amount
		oncomplete: () => void;
	};

	const props: Props = $props();
	const context = getContext();
	const AMOUNT_FAMILY = winFontFamily();
	const AMOUNT_TINT = winFontTint();

	// ------------------------------------------------------------------
	// staged counter: each plate holds for its scene track. The amount
	// eases across that scene's range; the NEXT plate starts when the
	// track ends (or the player skips). Ease only — duration comes from
	// the mp3:
	//   BOUNTY / scene 1      linear
	//   SHOWDOWN / scene 2    linear
	//   HIGH NOON / scene 3   a bit fast at start, slowing near the target
	//   LAST STAND / scene 4  super fast start, braking to a total stop
	//   BLOOD MONEY / scene 5 starts slow, keeps building speed
	//   BOOT HILL / scene 6   tab appears, counter parked, CONTINUE gate
	// ------------------------------------------------------------------
	const finalMult = $derived(props.finalAmount / 100);
	const tiers = $derived(getTiersPassed(props.finalAmount));
	const hasMax = $derived(tiers[tiers.length - 1]?.alias === 'max');

	const linear = (f: number) => f;
	const easeOutQuad = (f: number) => 1 - (1 - f) * (1 - f);
	const easeOutQuart = (f: number) => 1 - Math.pow(1 - f, 4);
	const easeInCubic = (f: number) => f * f * f;
	const SEGMENT_STYLE = [
		{ ease: linear },
		{ ease: linear },
		{ ease: easeOutQuad },
		{ ease: easeOutQuart },
		{ ease: easeInCubic },
	];

	type Segment = { from: number; to: number; duration: number; ease: (f: number) => number };
	const segments = $derived.by(() => {
		const countingTiers = hasMax ? tiers.slice(0, -1) : tiers;
		return countingTiers.map((tierData, index) => {
			const style = SEGMENT_STYLE[Math.min(index, SEGMENT_STYLE.length - 1)];
			const next = tiers[index + 1];
			const bgm = tierData.sound.bgm ?? '';
			return {
				from: index === 0 ? 0 : tierData.minMultiplier,
				to: next ? Math.min(next.minMultiplier, finalMult) : finalMult,
				duration: celebSceneDurationMs(bgm) || CELEB_SCENE_MS.bgm_celeb_1,
				ease: style.ease,
			} satisfies Segment;
		});
	});

	let segIndex = $state(0);
	let segStart = $state(0);
	let countMult = $state(0);
	let finished = $state(false);
	let waitContinue = $state(false);
	let displayedIndex = $state(0);
	// the BOOT HILL scene recounts from 0: fast start, even faster ending
	let maxRecountStart = $state<number | null>(null);
	const MAX_RECOUNT_DURATION = CELEB_SCENE_MS.bgm_celeb_6;
	const fastFaster = (f: number) => 0.55 * f + 0.45 * Math.pow(f, 4);

	// ------------------------------------------------------------------
	// transition fx: micro-fade, slam, gunsmoke wipe and a starburst punch
	// between the outgoing and incoming tier
	// ------------------------------------------------------------------
	const reelAlpha = new Tween(1);
	/** 1 → 0 over the transition: drives the gunsmoke wipe and the entry kick */
	const wipe = new Tween(0);
	/** 1 → 0 over the entry punch: drives the starburst and spark streaks */
	const pop = new Tween(0);
	const slam = new Tween(1);
	const zoom = new Tween(1);
	let fadeToken = 0;

	// One evolving score cut into contiguous stage slices (bgm_celeb_1..6 =
	// BOUNTY..BOOT HILL). Music alone carries the celebration — do NOT layer
	// the sfx_celeb_* whooshes/hits/slams on top (they drown the bed).
	const stageCue = (target: number): MusicName => {
		const tier = tiers[target]?.tier ?? 2;
		return `bgm_celeb_${Math.min(Math.max(tier - 1, 1), 6)}` as MusicName;
	};

	const OLD_CELEB_MUSIC: MusicName[] = [
		'bgm_celeb_1',
		'bgm_celeb_2',
		'bgm_celeb_3',
		'bgm_celeb_4',
		'bgm_celeb_5',
		'bgm_celeb_6',
		'bgm_main',
	];
	const OLD_CELEB_SFX: SoundEffectName[] = [
		'sfx_celeb_whoosh',
		'sfx_celeb_whoosh_hi',
		'sfx_celeb_whoosh_lo',
		'sfx_celeb_swell',
		'sfx_celeb_wobble',
		'sfx_celeb_buildup',
		'sfx_celeb_hit',
		'sfx_celeb_maxslam',
		'sfx_bigwin_coinloop',
	];

	const silenceOldCelebrationAudio = () => {
		stopCelebSceneBgm();
		for (const name of OLD_CELEB_MUSIC) {
			context.eventEmitter.broadcast({ type: 'soundStop', name });
		}
		for (const name of OLD_CELEB_SFX) {
			context.eventEmitter.broadcast({ type: 'soundStop', name });
		}
	};

	let sceneGen = 0;

	const advanceFromAudio = (gen: number) => {
		if (gen !== sceneGen) return;
		if (finished || waitContinue) return;
		if (maxRecountStart !== null) {
			countMult = finalMult;
			finished = true;
			waitContinue = true;
			return;
		}
		const now = performance.now();
		if (segIndex + 1 < segments.length) {
			countMult = segments[segIndex].to;
			enterSegment(segIndex + 1, now);
			return;
		}
		finishCounting();
	};

	const playStageMusic = (target: number) => {
		silenceOldCelebrationAudio();
		const cue = stageCue(target);
		const gen = ++sceneGen;
		if (!isCelebSceneBgm(cue)) return;
		playCelebSceneBgm(cue, () => advanceFromAudio(gen));
	};

	const showTier = (target: number) => {
		if (target === displayedIndex) return;
		playStageMusic(target);
		const token = ++fadeToken;
		wipe.set(1, { duration: 0 });
		wipe.set(0, { duration: 620, easing: cubicOut });
		(async () => {
			await reelAlpha.set(0, { duration: 70 });
			if (token !== fadeToken) return;
			displayedIndex = target;
			slam.set(1.12, { duration: 0 });
			slam.set(1, { duration: 450, easing: backOut });
			pop.set(1, { duration: 0 });
			pop.set(0, { duration: 900, easing: cubicOut });
			// slow Ken-Burns push for the tier's dwell
			zoom.set(1, { duration: 0 });
			zoom.set(intensity.push, { duration: 8000, easing: cubicOut });
			await reelAlpha.set(1, { duration: 90 });
		})();
	};

	const enterSegment = (index: number, now: number) => {
		segIndex = index;
		segStart = now;
		showTier(index);
	};

	const finishCounting = () => {
		if (hasMax) {
			// the BOOT HILL tab appears and the amount rolls again from zero
			countMult = 0;
			maxRecountStart = performance.now();
			showTier(tiers.length - 1);
		} else {
			countMult = finalMult;
			finished = true;
		}
	};

	// Same bus as TapToSkip / HUD stop / temporary turbo (`stopButtonClick`).
	// Presentation only — never invents payouts; jumps staged FX / dismisses.
	//   counting     → end current segment (next tier)
	//   max recount  → snap to final amount + CONTINUE gate
	//   finished     → dismiss overlay (PRESS ANYWHERE)
	//   waitContinue → Space / stop / CONTINUE pill all dismiss (Storybook
	//                  Action keeps xstate idle + iframe steals clicks)
	const skip = () => {
		if (waitContinue) {
			props.oncomplete();
			return;
		}
		if (finished) {
			props.oncomplete();
			return;
		}
		if (maxRecountStart !== null) {
			sceneGen += 1;
			stopCelebSceneBgm();
			countMult = finalMult;
			finished = true;
			waitContinue = true;
			return;
		}
		const now = performance.now();
		if (segIndex + 1 < segments.length) {
			countMult = segments[segIndex].to;
			enterSegment(segIndex + 1, now);
		} else if (hasMax) {
			finishCounting();
		} else {
			sceneGen += 1;
			stopCelebSceneBgm();
			finishCounting();
		}
	};

	context.eventEmitter.subscribeOnMount({
		stopButtonClick: () => skip(),
	});

	$effect(() => {
		context.eventEmitter.broadcast({ type: 'celebrationGate', waiting: waitContinue });
	});

	// Idle / Storybook safety: once the count-up settles the overlay waits for a
	// press (PRESS ANYWHERE) to dismiss. Automated Storybook Action never presses
	// (and the iframe steals clicks), so arm a generous auto-continue the moment
	// the celebration finishes. Real players press well inside this window — it
	// only rescues an unattended overlay (same pattern as the bonus banner).
	const CONTINUE_SAFETY_MS = 6000;
	let safetyFired = false;
	$effect(() => {
		if (!(finished || waitContinue)) return;
		const id = window.setTimeout(() => {
			if (safetyFired) return;
			safetyFired = true;
			props.oncomplete();
		}, CONTINUE_SAFETY_MS);
		return () => window.clearTimeout(id);
	});

	// No prompt while the amount is counting — tapping still skips (same
	// stopButtonClick bus as everything else), the label was just clutter over
	// the celebration. Once it settles the overlay does say how to dismiss it.
	const skipHint = $derived(waitContinue || !finished ? '' : 'PRESS ANYWHERE');

	let time = $state(0);
	onMount(() => {
		// Takeover owns music: kill Madam winlevel/celeb SFX, start the bed at stage 1
		playStageMusic(0);
		pop.set(1, { duration: 0 });
		pop.set(0, { duration: 900, easing: cubicOut });
		zoom.set(intensity.push, { duration: 8000, easing: cubicOut });
		let raf = 0;
		const start = performance.now();
		segStart = start;
		const tick = (now: number) => {
			time = (now - start) / 1000;
			if (!finished) {
				if (maxRecountStart !== null) {
					const f = Math.min((now - maxRecountStart) / MAX_RECOUNT_DURATION, 1);
					countMult = finalMult * fastFaster(f);
					if (f >= 1) {
						finished = true;
						waitContinue = true;
					}
				} else {
					const segment = segments[segIndex];
					const f = Math.min((now - segStart) / segment.duration, 1);
					countMult = segment.from + (segment.to - segment.from) * segment.ease(f);
					// Park at this scene's amount. The next plate waits for
					// the track to end (or a skip) — do not climb on the clock.
				}
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => {
			cancelAnimationFrame(raf);
			sceneGen += 1;
			stopCelebSceneBgm();
			context.eventEmitter.broadcast({ type: 'soundMusic', name: currentModeMusic() });
		};
	});

	// ------------------------------------------------------------------
	// tier + art
	// ------------------------------------------------------------------
	const celebration = $derived(tiers[displayedIndex] ?? tiers[0]);
	const title = $derived(celebration?.title ?? 'BOUNTY');
	const intensity = $derived(winTierIntensity(celebration?.tier ?? 2));
	const plateKey = $derived(winTierPlateKey(celebration?.slug || 'bounty'));

	const lightTextures = $derived(
		(context.stateApp.loadedAssets?.[WIN_CELEB_LIGHT_ASSET] as Texture[] | undefined) ?? [],
	);
	const vfxTextures = $derived(
		(context.stateApp.loadedAssets?.[WIN_CELEB_VFX_ASSET] as Texture[] | undefined) ?? [],
	);
	const light = (index: number) => lightTextures[index];
	const vfx = (index: number) => vfxTextures[index];

	// ------------------------------------------------------------------
	// geometry
	// ------------------------------------------------------------------
	const boardW = $derived(context.stateGameDerived.boardLayout().width);
	const frameW = $derived(boardW * 1.02);
	const frameH = $derived(frameW * (9 / 16));
	// win_frame.png is the 1280x720 plate plus a uniform 74px timber/iron band,
	// so the frame scales with the plate and its window stays aligned.
	const FRAME_PAD_FRAC = 74 / 1280;
	const frameOuterW = $derived(frameW * (1 + FRAME_PAD_FRAC * 2));
	const frameOuterH = $derived(frameH + frameW * FRAME_PAD_FRAC * 2);

	/** CSS object-fit: cover — fill the window, crop overflow (never letterbox). */
	const plateCover = $derived.by(() => {
		const scale = Math.max(frameW / 1280, frameH / 720);
		return { width: 1280 * scale, height: 720 * scale };
	});

	const mainW = $derived(context.stateLayoutDerived.mainLayout().width);
	const mainH = $derived(context.stateLayoutDerived.mainLayout().height);
	// content spans the framed panel plus the title / amount / ways stack below
	const contentH = $derived(frameOuterH + SYMBOL_SIZE * 2.35);
	const fit = $derived(Math.min(1, (mainH * 0.94) / contentH));
	const centerShift = $derived(SYMBOL_SIZE * 1.05);
	// ember / ray field has to cover the canvas after the `fit` downscale
	const fieldW = $derived(mainW / Math.max(fit, 0.2));
	const fieldH = $derived(mainH / Math.max(fit, 0.2));

	// ------------------------------------------------------------------
	// animated layers — all sprite transforms, never a per-frame redraw
	// ------------------------------------------------------------------
	// Allocated once at the top-tier count and modulated by alpha, so escalating
	// through the ladder never churns the display list.
	const MAX_RAYS = 12;
	const MAX_EMBERS = 76;
	const MAX_STREAKS = 26;
	const MAX_DUST = 8;
	const RAYS = Array.from({ length: MAX_RAYS }, (_, i) => i);
	const EMBERS = Array.from({ length: MAX_EMBERS }, (_, i) => i);
	const STREAKS = Array.from({ length: MAX_STREAKS }, (_, i) => i);
	const DUST = Array.from({ length: MAX_DUST }, (_, i) => i);

	const kick = $derived(wipe.current * intensity.kick);
	const kickX = $derived((winRand(Math.floor(time * 40) * 7 + 3) - 0.5) * kick);
	const kickY = $derived((winRand(Math.floor(time * 40)) - 0.5) * kick);
	// lantern breathe — never a hard strobe, the plates are already high contrast
	const lantern = $derived(0.9 + 0.1 * Math.sin(time * 1.7));

	const amountPulse = $derived(1 + 0.025 * Math.sin(time * 3.4));
	const continuePulse = $derived(1 + 0.04 * Math.sin(time * 4.2));
	const displayAmount = $derived(countMult * 100);

	// title / amount chrome: constant geometry, so these Rectangles are drawn
	// once per layout change and not during the count-up
	const titlePlateW = $derived(frameW * 0.66);
	const titlePlateH = $derived(SYMBOL_SIZE * 0.74);
	const amountPlateW = $derived(frameW * 0.82);
	const amountPlateH = $derived(SYMBOL_SIZE * 1.18);
	const titleY = $derived(frameOuterH / 2 + SYMBOL_SIZE * 0.44);
	const amountY = $derived(frameOuterH / 2 + SYMBOL_SIZE * 1.34);
	const waysY = $derived(frameOuterH / 2 + SYMBOL_SIZE * 2.08);
</script>

<Container x={kickX} y={kickY - centerShift} scale={fit}>
	<!-- god-rays behind the frame: lantern / heaven light raking down -->
	{#if light(WIN_LIGHT.rayFan)}
		<Container alpha={intensity.rayAlpha * lantern}>
			{#each RAYS as index (index)}
				{#if index < intensity.rays}
					{@const seed = index * 3 + 1}
					{@const sway = Math.sin(time * (0.16 + winRand(seed) * 0.22) + index) * 0.09}
					{@const spread = (index / Math.max(intensity.rays - 1, 1) - 0.5) * 1.5}
					<BaseSprite
						texture={index % 3 === 0
							? light(WIN_LIGHT.rayStreaks)
							: index % 3 === 1
								? light(WIN_LIGHT.rayFan)
								: light(WIN_LIGHT.rayCone)}
						anchor={{ x: 0.5, y: 0 }}
						x={spread * frameW * 0.42}
						y={-frameOuterH * 0.62}
						width={frameW * (0.30 + winRand(seed * 5) * 0.22)}
						height={fieldH * 0.92}
						rotation={spread * 0.30 + sway}
						blendMode="add"
						alpha={0.55 + 0.45 * winRand(seed * 11)}
					/>
				{/if}
			{/each}
		</Container>
	{/if}

	<!-- warm lantern bloom behind the panel -->
	{#if light(WIN_LIGHT.glowWarm)}
		<BaseSprite
			texture={light(WIN_LIGHT.glowWarm)}
			anchor={0.5}
			width={frameOuterW * 1.5}
			height={frameOuterH * 1.7}
			blendMode="add"
			alpha={0.20 + intensity.rayAlpha * 0.45 * lantern}
		/>
	{/if}

	<!-- BOOT HILL bell tolls: slow bronze rings rolling out of the graveyard -->
	{#if intensity.bellTolls > 0 && light(WIN_LIGHT.ringSoft)}
		{#each [0, 1, 2] as ring (ring)}
			{@const phase = (time * intensity.bellTolls + ring / 3) % 1}
			<BaseSprite
				texture={ring % 2 === 0 ? light(WIN_LIGHT.ringSoft) : light(WIN_LIGHT.ringHard)}
				anchor={0.5}
				width={frameOuterW * (0.35 + phase * 1.5)}
				height={frameOuterW * (0.35 + phase * 1.5)}
				blendMode="add"
				alpha={0.5 * (1 - phase) * (1 - phase)}
			/>
		{/each}
	{/if}

	<Container scale={slam.current}>
		<!-- hero panel: tier plate cover-fit into the frame window, Ken-Burns push -->
		<Container alpha={reelAlpha.current * lantern}>
			<Rectangle isMask anchor={0.5} width={frameW} height={frameH} borderRadius={2} />
			<Sprite
				key={plateKey}
				anchor={0.5}
				width={plateCover.width * zoom.current}
				height={plateCover.height * zoom.current}
				x={Math.sin(time * 0.22) * frameW * 0.008}
			/>

			<!-- grave dust drifting across the plate -->
			{#if vfx(WIN_VFX.dustPuffA)}
				{#each DUST as index (index)}
					{#if index < intensity.dust}
						{@const seed = index * 7 + 2}
						{@const drift = (time * (0.045 + winRand(seed) * 0.05) + winRand(seed * 3)) % 1}
						<BaseSprite
							texture={index % 3 === 0
								? vfx(WIN_VFX.dustPlume)
								: index % 2 === 0
									? vfx(WIN_VFX.dustPuffA)
									: vfx(WIN_VFX.dustPuffB)}
							anchor={0.5}
							x={(drift - 0.5) * frameW * 1.7}
							y={(winRand(seed * 5) - 0.3) * frameH * 0.62}
							width={frameW * (0.24 + winRand(seed * 9) * 0.3)}
							height={frameW * (0.24 + winRand(seed * 9) * 0.3)}
							rotation={winRand(seed * 13) * 6.28}
							alpha={0.30 * Math.sin(drift * Math.PI)}
						/>
					{/if}
				{/each}
			{/if}

			<!-- gunsmoke wipe between tiers (replaces the CRT screen-tear bands) -->
			{#if wipe.current > 0.02 && vfx(WIN_VFX.smokeA)}
				{#each [0, 1, 2, 3, 4] as index (index)}
					{@const seed = index * 11 + 5}
					<BaseSprite
						texture={index % 2 === 0 ? vfx(WIN_VFX.smokeA) : vfx(WIN_VFX.smokeB)}
						anchor={0.5}
						x={(winRand(seed) - 0.5) * frameW * (1.1 - wipe.current * 0.5)}
						y={(winRand(seed * 3) - 0.5) * frameH * 0.8}
						width={frameW * (0.5 + winRand(seed * 5) * 0.4)}
						height={frameW * (0.5 + winRand(seed * 5) * 0.4)}
						rotation={time * (0.3 + winRand(seed * 7) * 0.4)}
						alpha={0.5 * wipe.current}
					/>
				{/each}
			{/if}
		</Container>

		<!-- weathered timber + branded-iron frame, over the panel edges -->
		<Sprite key={WIN_FRAME_ASSET} anchor={0.5} width={frameOuterW} height={frameOuterH} />
	</Container>

	<!-- entry punch: gold starburst + radiating spark streaks over the frame -->
	{#if pop.current > 0.01 && vfx(WIN_VFX.starburst)}
		{@const burst = 1 - pop.current}
		<BaseSprite
			texture={vfx(WIN_VFX.starburst)}
			anchor={0.5}
			width={frameW * intensity.popScale * (0.35 + burst * 1.1)}
			height={frameW * intensity.popScale * (0.35 + burst * 1.1)}
			rotation={burst * 0.5}
			blendMode="add"
			alpha={pop.current}
		/>
		<BaseSprite
			texture={vfx(WIN_VFX.flashPop)}
			anchor={0.5}
			width={frameW * intensity.popScale * (0.2 + burst * 0.9)}
			height={frameW * intensity.popScale * (0.2 + burst * 0.9)}
			blendMode="add"
			alpha={pop.current * 0.85}
		/>
		{#each STREAKS as index (index)}
			{#if index < intensity.streaks}
				{@const angle = (index / intensity.streaks) * Math.PI * 2 + winRand(index) * 0.3}
				{@const reach = burst * frameW * 0.5 * (0.6 + winRand(index * 3) * 0.7)}
				<BaseSprite
					texture={index % 4 === 0 ? vfx(WIN_VFX.starPoint) : vfx(WIN_VFX.sparkStreak)}
					anchor={0.5}
					x={Math.cos(angle) * reach}
					y={Math.sin(angle) * reach}
					width={frameW * 0.12}
					height={frameW * 0.12}
					rotation={angle + Math.PI / 2}
					blendMode="add"
					alpha={pop.current * 0.9}
				/>
			{/if}
		{/each}
	{/if}

	<!-- rising gold embers over the whole takeover -->
	{#if vfx(WIN_VFX.emberMote)}
		{#each EMBERS as index (index)}
			{#if index < intensity.embers}
				{@const seed = index * 13 + 4}
				{@const speed = 0.055 + winRand(seed) * 0.12}
				{@const phase = (time * speed + winRand(seed * 3)) % 1}
				{@const size = fieldW * (0.006 + winRand(seed * 7) * 0.014)}
				<BaseSprite
					texture={index % 5 === 0 ? vfx(WIN_VFX.starSmall) : vfx(WIN_VFX.emberMote)}
					anchor={0.5}
					x={(winRand(seed * 5) - 0.5) * fieldW +
						Math.sin(time * 0.7 + index) * fieldW * 0.012}
					y={(0.55 - phase) * fieldH}
					width={size}
					height={size}
					rotation={time * (0.4 + winRand(seed * 11))}
					blendMode="add"
					alpha={0.75 * Math.sin(phase * Math.PI)}
				/>
			{/if}
		{/each}
	{/if}

	<!-- tier title: branded iron plate, revolver emblems flanking.
	     LIT, NOT LINED: the plate used to carry a 2px gold border, which read as a
	     stray vector outline on top of the art. A warm bloom behind it separates it
	     from the dark instead — same treatment as the amount plate and the CONTINUE
	     gate below, and the same reason win_frame.png lost its inlay hairline. -->
	<Container y={titleY} scale={slam.current} alpha={reelAlpha.current}>
		{#if light(WIN_LIGHT.glowWarm)}
			<BaseSprite
				texture={light(WIN_LIGHT.glowWarm)}
				anchor={0.5}
				width={titlePlateW * 1.35}
				height={titlePlateH * 3.4}
				blendMode="add"
				alpha={0.34 * lantern}
			/>
		{/if}
		<Rectangle
			anchor={0.5}
			width={titlePlateW}
			height={titlePlateH}
			borderRadius={4}
			backgroundColor={WIN_PALETTE.iron}
			backgroundAlpha={0.9}
		/>
		{#if vfx(WIN_VFX.revolverEmblem)}
			{#each [-1, 1] as side (side)}
				{@const emblem = (titlePlateH * 1.6) / WIN_VFX_CELL}
				<!-- negative x scale mirrors the revolver so the pair face outward;
				     scale is used instead of width/height because the two props
				     fight each other on a PIXI.Sprite -->
				<BaseSprite
					texture={vfx(WIN_VFX.revolverEmblem)}
					anchor={0.5}
					x={side * titlePlateW * 0.6}
					scale={{ x: side * emblem, y: emblem }}
					alpha={0.85}
				/>
			{/each}
		{/if}
		<ResponsiveBitmapText
			anchor={0.5}
			maxWidth={titlePlateW * 0.88}
			text={title}
			tint={AMOUNT_TINT}
			style={{
				fontFamily: AMOUNT_FAMILY,
				fontSize: winFontSize(0.5),
				align: 'center',
				fontWeight: 'bold',
				letterSpacing: 3,
			}}
		/>
	</Container>

	<!-- amount: dark iron plate keeps gold numerals readable over any plate -->
	<Container y={amountY}>
		{#if light(WIN_LIGHT.glowWarm)}
			<BaseSprite
				texture={light(WIN_LIGHT.glowWarm)}
				anchor={0.5}
				width={amountPlateW * 1.3}
				height={amountPlateH * 2.6}
				blendMode="add"
				alpha={0.4 * lantern}
			/>
		{/if}
		<Rectangle
			anchor={0.5}
			width={amountPlateW}
			height={amountPlateH}
			borderRadius={5}
			backgroundColor={WIN_PALETTE.dark}
			backgroundAlpha={0.82}
		/>
		<Container scale={amountPulse * slam.current}>
			<ResponsiveBitmapText
				anchor={0.5}
				maxWidth={amountPlateW * 0.9}
				text={bookEventAmountToCurrencyString(displayAmount)}
				tint={AMOUNT_TINT}
				style={{
					fontFamily: AMOUNT_FAMILY,
					fontSize: winFontSize(1.0),
					align: 'center',
					fontWeight: 'bold',
					letterSpacing: 0,
				}}
			/>
		</Container>
	</Container>

	{#if (props.ways ?? 0) > 0}
		<Container y={waysY} scale={slam.current} alpha={reelAlpha.current}>
			<ResponsiveBitmapText
				anchor={0.5}
				maxWidth={frameW * 0.7}
				text={waysLabel(props.ways ?? 0)}
				tint={WIN_PALETTE.goldPale}
				style={{
					fontFamily: AMOUNT_FAMILY,
					fontSize: winFontSize(0.32),
					align: 'center',
					fontWeight: 'bold',
					letterSpacing: 3,
				}}
			/>
		</Container>
	{/if}

	<!-- BOOT HILL gate: CONTINUE plate + Space/stopButtonClick (see skip()).
	     Explicit hitArea so the plate still receives Storybook taps. -->
	{#if waitContinue}
		{@const pillW = SYMBOL_SIZE * 2.6}
		{@const pillH = SYMBOL_SIZE * 0.62}
		<Container
			y={frameOuterH / 2 - SYMBOL_SIZE * 0.62}
			scale={continuePulse}
			eventMode="static"
			cursor="pointer"
			hitArea={new HitRectangle(-pillW / 2, -pillH / 2, pillW, pillH)}
			onpointerup={() => props.oncomplete()}
		>
			<!-- the pulsing bloom is what marks this as pressable now that the pill
			     carries no gold rim; the pill itself stays a dark iron plate. -->
			{#if light(WIN_LIGHT.glowCore)}
				<BaseSprite
					texture={light(WIN_LIGHT.glowCore)}
					anchor={0.5}
					width={pillW * 1.5}
					height={pillH * 4.2}
					blendMode="add"
					alpha={0.3 + 0.14 * Math.sin(time * 4.2)}
					eventMode="none"
				/>
			{/if}
			<Rectangle
				anchor={0.5}
				width={pillW}
				height={pillH}
				borderRadius={pillH / 2}
				backgroundColor={WIN_PALETTE.iron}
				backgroundAlpha={0.94}
				eventMode="static"
				cursor="pointer"
				hitArea={new HitRectangle(-pillW / 2, -pillH / 2, pillW, pillH)}
				onpointerup={() => props.oncomplete()}
			/>
			<BitmapText
				anchor={0.5}
				text="CONTINUE"
				eventMode="none"
				tint={AMOUNT_TINT}
				style={{ fontFamily: AMOUNT_FAMILY, fontSize: winFontSize(0.32), letterSpacing: 2 }}
			/>
		</Container>
	{:else if skipHint}
		<Container y={waysY + SYMBOL_SIZE * 0.62} alpha={0.72 + 0.18 * Math.sin(time * 3.2)}>
			<BitmapText
				anchor={0.5}
				text={skipHint}
				eventMode="none"
				tint={WIN_PALETTE.goldPale}
				style={{ fontFamily: AMOUNT_FAMILY, fontSize: winFontSize(0.18), letterSpacing: 3 }}
			/>
		</Container>
	{/if}
</Container>
