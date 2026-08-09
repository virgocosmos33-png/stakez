<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { Rectangle as HitRectangle, type Texture, type VideoSource } from 'pixi.js';
	import { Container, Graphics, Rectangle, Sprite, BitmapText } from 'pixi-svelte';
	import { ResponsiveBitmapText } from 'components-pixi';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { drawGlassPill } from '../game/glassChrome';
	import { getTiersPassed } from '../game/winCelebrationMap';
	import type { MusicName, SoundEffectName } from '../game/sound';
	import { winFontFamily, winFontSize, winFontTint } from '../game/winFont';

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
	// staged counter: the reel switches EXACTLY when the rolling amount
	// crosses each real trigger (25x / 50x / 100x / 500x / 2500x / maxwin),
	// with per-segment pacing:
	//   BIG 25-50x     linear
	//   SUPER 50-100x  linear
	//   MEGA 100-500x  a bit fast at start, slowing near the target
	//   EPIC 500-2500x super fast start, braking to a total stop
	//   WHITEOUT 2500x+  starts slow, keeps building speed
	//   MAX WIN        tab appears, counter parked, CONTINUE gate
	// ------------------------------------------------------------------
	const finalMult = $derived(props.finalAmount / 100);
	const tiers = $derived(getTiersPassed(props.finalAmount));
	const hasMax = $derived(tiers[tiers.length - 1]?.alias === 'max');

	const linear = (f: number) => f;
	const easeOutQuad = (f: number) => 1 - (1 - f) * (1 - f);
	const easeOutQuart = (f: number) => 1 - Math.pow(1 - f, 4);
	const easeInCubic = (f: number) => f * f * f;
	const SEGMENT_STYLE = [
		{ ease: linear, duration: 3000 },
		{ ease: linear, duration: 3000 },
		{ ease: easeOutQuad, duration: 3600 },
		{ ease: easeOutQuart, duration: 4200 },
		{ ease: easeInCubic, duration: 4800 },
	];

	type Segment = { from: number; to: number; duration: number; ease: (f: number) => number };
	const segments = $derived.by(() => {
		const countingTiers = hasMax ? tiers.slice(0, -1) : tiers;
		return countingTiers.map((tierData, index) => {
			const style = SEGMENT_STYLE[Math.min(index, SEGMENT_STYLE.length - 1)];
			const next = tiers[index + 1];
			return {
				from: index === 0 ? 0 : tierData.minMultiplier,
				to: next ? Math.min(next.minMultiplier, finalMult) : finalMult,
				duration: style.duration,
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
	// the MAX WIN scene recounts from 0: fast start, even faster ending
	let maxRecountStart = $state<number | null>(null);
	const MAX_RECOUNT_DURATION = 3500;
	const fastFaster = (f: number) => 0.55 * f + 0.45 * Math.pow(f, 4);

	// ------------------------------------------------------------------
	// transition fx: micro-fade + glitch/screen-tear interference between
	// the outgoing and incoming reels
	// ------------------------------------------------------------------
	const reelAlpha = new Tween(1);
	const glitch = new Tween(0);
	const slam = new Tween(1);
	const zoom = new Tween(1);
	let fadeToken = 0;
	type TearBand = { v: number; height: number; offset: number; speed: number };
	let tearBands = $state<TearBand[]>([]);

	// One evolving ElevenLabs asylum score, cut into contiguous 8s stage
	// slices (bgm_celeb_1..6 = BIG..MAX). Music alone carries the celebration —
	// do NOT layer Madam-era sfx_celeb_* whooshes/hits/slams (they drown the bed).
	const stageCue = (target: number): MusicName => {
		const tier = tiers[target]?.tier ?? 2;
		return `bgm_celeb_${Math.min(Math.max(tier - 1, 1), 6)}` as MusicName;
	};

	const OLD_CELEB_MUSIC: MusicName[] = [
		'bgm_winlevel_big',
		'bgm_winlevel_superwin',
		'bgm_winlevel_mega',
		'bgm_winlevel_epic',
		'bgm_winlevel_max',
		'bgm_celeb_1',
		'bgm_celeb_2',
		'bgm_celeb_3',
		'bgm_celeb_4',
		'bgm_celeb_5',
		'bgm_celeb_6',
		'bgm_main',
		'bgm_freespin',
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
		for (const name of OLD_CELEB_MUSIC) {
			context.eventEmitter.broadcast({ type: 'soundStop', name });
		}
		for (const name of OLD_CELEB_SFX) {
			context.eventEmitter.broadcast({ type: 'soundStop', name });
		}
	};

	const playStageMusic = (target: number) => {
		// Stop prior stage / Madam winlevel beds so Howler starts the slice
		// from its downbeat (pause-resume would keep old Madam audio alive).
		silenceOldCelebrationAudio();
		context.eventEmitter.broadcast({ type: 'soundMusic', name: stageCue(target) });
	};

	const showTier = (target: number) => {
		if (target === displayedIndex) return;
		playStageMusic(target);
		const token = ++fadeToken;
		// screen tear bands regenerate per transition
		tearBands = Array.from({ length: 7 }, (_, i) => ({
			v: Math.random(),
			height: 0.04 + Math.random() * 0.09,
			offset: (Math.random() - 0.5) * 2,
			speed: 4 + Math.random() * 14,
		}));
		glitch.set(1, { duration: 0 });
		glitch.set(0, { duration: 520, easing: cubicOut });
		(async () => {
			await reelAlpha.set(0, { duration: 70 });
			if (token !== fadeToken) return;
			displayedIndex = target;
			slam.set(1.12, { duration: 0 });
			slam.set(1, { duration: 450, easing: backOut });
			zoom.set(1, { duration: 0 });
			zoom.set(1.09, { duration: 8000, easing: cubicOut });
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
			// the MAX WIN tab appears and the amount rolls again from zero
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
			countMult = finalMult;
			finished = true;
			waitContinue = true;
			return;
		}
		const now = performance.now();
		if (segIndex + 1 < segments.length) {
			countMult = segments[segIndex].to;
			enterSegment(segIndex + 1, now);
		} else {
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
		// Takeover owns music: kill Madam winlevel/celeb SFX, start evolving bed stage 1
		playStageMusic(0);
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
					if (f >= 1) {
						if (segIndex + 1 < segments.length) {
							enterSegment(segIndex + 1, now);
						} else {
							finishCounting();
						}
					}
				}
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => {
			cancelAnimationFrame(raf);
			// hand the music back to the room the player is actually in
			context.eventEmitter.broadcast({
				type: 'soundMusic',
				name: context.stateGame.gameType === 'freegame' ? 'bgm_freespin' : 'bgm_main',
			});
		};
	});

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	const celebration = $derived(tiers[displayedIndex] ?? tiers[0]);
	const title = $derived(celebration?.title ?? 'INTAKE');
	const stillKey = $derived(`celebT${celebration?.tier ?? 2}`);
	const animKey = $derived(`celebT${celebration?.tier ?? 2}Anim`);
	const videoTexture = $derived(
		context.stateApp.loadedAssets?.[animKey] as Texture | undefined,
	);
	const reelKey = $derived(videoTexture ? animKey : stillKey);

	$effect(() => {
		const source = videoTexture?.source as VideoSource | undefined;
		const video = source?.resource as HTMLVideoElement | undefined;
		if (video) {
			video.loop = true;
			video.muted = true;
			if (video.paused) video.play().catch(() => {});
		}
	});

	const boardW = $derived(context.stateGameDerived.boardLayout().width);
	const frameW = $derived(boardW * 1.02);
	// Clinical monitor viewport — 16:9 matches Seedance celeb masters (cover-crop fills).
	const frameH = $derived(frameW * (9 / 16));
	const holeColW = $derived(frameW * 0.055);

	/** CSS object-fit: cover — fill the monitor, crop overflow (never letterbox/stretch bars). */
	const coverFit = (boxW: number, boxH: number, artW: number, artH: number) => {
		const scale = Math.max(boxW / Math.max(1, artW), boxH / Math.max(1, artH));
		return { width: artW * scale, height: artH * scale };
	};
	const reelArtSize = $derived.by(() => {
		const tex = context.stateApp.loadedAssets?.[reelKey] as Texture | undefined;
		const w = Number(tex?.width) || Number(tex?.source?.width) || 0;
		const h = Number(tex?.height) || Number(tex?.source?.height) || 0;
		if (w > 1 && h > 1) return { width: w, height: h };
		// Seedance / assembled masters are 16:9
		return { width: 1280, height: 720 };
	});
	const reelCover = $derived(coverFit(frameW, frameH, reelArtSize.width, reelArtSize.height));

	const jitterY = $derived((rand(Math.floor(time * 24)) - 0.5) * (3.2 + glitch.current * 9));
	const jitterX = $derived((rand(Math.floor(time * 24) * 7 + 3) - 0.5) * (1.6 + glitch.current * 7));
	const flicker = $derived(0.86 + 0.14 * rand(Math.floor(time * 18) * 13 + 1));

	// CRT / observation-monitor damage (NOT vintage film scratches)
	const drawFilmDamage = (graphics: import('pixi.js').Graphics, timeValue: number) => {
		const w = frameW;
		const h = frameH;
		const chunk = Math.floor(timeValue * 14);
		// persistent horizontal scanlines
		for (let i = 0; i < 18; i++) {
			const y = -h / 2 + (i / 18) * h;
			graphics.rect(-w / 2, y, w, 1);
			graphics.fill({ color: 0xffffff, alpha: 0.03 + (i % 3 === 0 ? 0.04 : 0) });
		}
		// dead pixels / dropouts
		for (let i = 0; i < 9; i++) {
			if (rand(chunk * 41 + i * 13) > 0.55) continue;
			const x = (rand(chunk * 19 + i * 29) - 0.5) * w;
			const y = (rand(chunk * 23 + i * 37) - 0.5) * h;
			graphics.rect(x, y, 2 + rand(chunk + i) * 6, 2 + rand(chunk + i * 2) * 4);
			graphics.fill({ color: 0x12100e, alpha: 0.55 });
		}
		// fluorescent flicker band
		if (rand(chunk * 61) > 0.7) {
			const y = (rand(chunk * 71) - 0.5) * h;
			graphics.rect(-w / 2, y, w, 6 + rand(chunk) * 14);
			graphics.fill({ color: 0xf4f1ec, alpha: 0.08 });
		}
	};

	// MEMORY WIPE transition: hard CRT tear blocks + fluorescent strobe lines
	const drawGlitchNoise = (graphics: import('pixi.js').Graphics, amount: number, timeValue: number) => {
		if (amount <= 0.01) return;
		const w = frameW;
		const h = frameH;
		const chunk = Math.floor(timeValue * 48);
		for (let i = 0; i < 14; i++) {
			if (rand(chunk * 13 + i * 7) > amount) continue;
			const y = (rand(chunk * 17 + i * 11) - 0.5) * h;
			const shear = (rand(chunk + i * 3) - 0.5) * w * 0.12 * amount;
			graphics.rect(-w / 2 + shear, y, w, 2 + rand(chunk + i) * 5);
			graphics.fill({
				color: rand(chunk * 5 + i) > 0.4 ? 0xffffff : 0x8a8680,
				alpha: 0.2 * amount + rand(chunk * 3 + i) * 0.25 * amount,
			});
		}
		// vertical memory-column wipe
		for (let i = 0; i < 3; i++) {
			if (rand(chunk * 29 + i) > amount) continue;
			const x = (rand(chunk * 31 + i * 5) - 0.5) * w;
			graphics.rect(x, -h / 2, 3 + rand(chunk + i) * 18, h);
			graphics.fill({ color: 0xf4f1ec, alpha: 0.12 * amount });
		}
	};

	// CCTV / clinical monitor bezel (NOT film sprocket frame)
	const drawFilmFrame = (graphics: import('pixi.js').Graphics) => {
		const w = frameW;
		const h = frameH;
		const bezel = holeColW * 0.85;
		graphics.roundRect(-w / 2 - bezel, -h / 2 - bezel * 0.7, w + bezel * 2, h + bezel * 1.4, 6);
		graphics.fill({ color: 0x2a2826, alpha: 0.97 });
		// steel lip
		graphics.roundRect(-w / 2 - bezel, -h / 2 - bezel * 0.7, w + bezel * 2, h + bezel * 1.4, 6);
		graphics.stroke({ color: 0x8a8680, width: 3, alpha: 0.85 });
		// status LEDs (clinical, not sprocket holes)
		for (let i = 0; i < 3; i++) {
			const x = -w / 2 - bezel * 0.45;
			const y = -h / 2 + h * (0.2 + i * 0.25);
			graphics.circle(x, y, 4);
			graphics.fill({ color: i === 0 ? 0xf4f1ec : 0x6b2a28, alpha: i === 0 ? 0.9 : 0.55 });
		}
		graphics.roundRect(-w / 2, -h / 2, w, h, 2);
		graphics.stroke({ color: 0xc8c4bc, width: 2, alpha: 0.7 });
		// REC stamp corner
		graphics.rect(w / 2 - 52, -h / 2 + 10, 40, 14);
		graphics.fill({ color: 0x6b2a28, alpha: 0.75 });
	};

	const drawVignette = (graphics: import('pixi.js').Graphics) => {
		const w = frameW;
		const h = frameH;
		// hard clinical edge falloff (not soft gothic vignette)
		for (let i = 0; i < 3; i++) {
			graphics.rect(-w / 2 + i * 4, -h / 2 + i * 4, w - i * 8, h - i * 8);
			graphics.stroke({ color: 0x12100e, width: 10, alpha: 0.18 - i * 0.04 });
		}
	};

	const amountPulse = $derived(1 + 0.025 * Math.sin(time * 3.4));
	const continuePulse = $derived(1 + 0.04 * Math.sin(time * 4.2));
	const displayAmount = $derived(countMult * 100);

	// fit the whole takeover (frame + title + amount) inside the canvas: scale
	// down when needed and center the full content block vertically
	const mainH = $derived(context.stateLayoutDerived.mainLayout().height);
	// content spans -frameH/2 (frame top) to frameH/2 + 1.85 * SYMBOL_SIZE (amount bottom)
	const contentH = $derived(frameH + SYMBOL_SIZE * 1.85);
	const fit = $derived(Math.min(1, (mainH * 0.92) / contentH));
	const centerShift = $derived(((SYMBOL_SIZE * 1.85) / 2) * fit);
</script>

<Container x={jitterX} y={jitterY - centerShift} scale={fit}>
	<Container scale={slam.current}>
		<Graphics draw={drawFilmFrame} />
		<Container scale={zoom.current} alpha={flicker * reelAlpha.current}>
			<!-- Cover-fit + mask: video fills the monitor edge-to-edge, crop overflow.
			     Never stretch-letterbox (width/height alone on padded mp4 left bars). -->
			<Rectangle isMask anchor={0.5} width={frameW} height={frameH} borderRadius={3} />
			<Sprite key={reelKey} anchor={0.5} width={reelCover.width} height={reelCover.height} />
			<!-- fluorescent blackout ghost (desaturated clinical, NOT RGB séance split) -->
			{#if glitch.current > 0.02}
				<Sprite
					key={reelKey}
					anchor={0.5}
					width={reelCover.width}
					height={reelCover.height}
					x={glitch.current * 7}
					tint={0xf4f1ec}
					alpha={0.35 * glitch.current}
				/>
				<Sprite
					key={reelKey}
					anchor={0.5}
					width={reelCover.width}
					height={reelCover.height}
					y={glitch.current * 5}
					tint={0x8a8680}
					alpha={0.22 * glitch.current}
				/>
			{/if}
		</Container>
		<!-- screen tearing: horizontal bands of the reel ripped sideways -->
		{#if glitch.current > 0.02}
			{#each tearBands as band, i (i)}
				{@const bandY = (band.v - 0.5) * frameH}
				{@const bandH = band.height * frameH}
				{@const shear =
					band.offset * glitch.current * frameW * 0.09 * (0.6 + 0.4 * Math.sin(time * band.speed + i))}
				<Container>
					<Rectangle
						isMask
						anchor={0.5}
						y={bandY}
						width={frameW}
						height={bandH}
					/>
					<Sprite
						key={reelKey}
						anchor={0.5}
						x={shear}
						width={reelCover.width}
						height={reelCover.height}
						alpha={0.9}
					/>
				</Container>
			{/each}
		{/if}
		<Graphics draw={drawVignette} />
		<Graphics draw={(graphics) => drawFilmDamage(graphics, time)} />
		<Graphics draw={(graphics) => drawGlitchNoise(graphics, glitch.current, time)} />
	</Container>

	<Container y={frameH / 2 + SYMBOL_SIZE * 0.52} scale={slam.current} alpha={reelAlpha.current}>
		<ResponsiveBitmapText
			anchor={0.5}
			maxWidth={frameW * 0.7}
			text={title}
			tint={AMOUNT_TINT}
			style={{
				fontFamily: AMOUNT_FAMILY,
				fontSize: winFontSize(0.52),
				align: 'center',
				fontWeight: 'bold',
				letterSpacing: 3,
			}}
		/>
	</Container>
	<Container y={frameH / 2 + SYMBOL_SIZE * 1.25} scale={amountPulse * slam.current}>
		<ResponsiveBitmapText
			anchor={0.5}
			maxWidth={frameW * 0.85}
			text={bookEventAmountToCurrencyString(displayAmount)}
			tint={AMOUNT_TINT}
			style={{
				fontFamily: AMOUNT_FAMILY,
				fontSize: winFontSize(1.05),
				align: 'center',
				fontWeight: 'bold',
				letterSpacing: 0,
			}}
		/>
	</Container>
	{#if (props.ways ?? 0) > 0}
		<Container y={frameH / 2 + SYMBOL_SIZE * 2.0} scale={slam.current} alpha={reelAlpha.current}>
			<ResponsiveBitmapText
				anchor={0.5}
				maxWidth={frameW * 0.7}
				text={props.ways === 1 ? '1 WAY' : `${props.ways} WAYS`}
				tint={AMOUNT_TINT}
				style={{
					fontFamily: AMOUNT_FAMILY,
					fontSize: winFontSize(0.34),
					align: 'center',
					fontWeight: 'bold',
					letterSpacing: 3,
				}}
			/>
		</Container>
	{/if}

	<!-- MAX WIN gate: CONTINUE pill + Space/stopButtonClick (see skip()).
	     Explicit hitArea so sparse Graphics fills still receive Storybook taps. -->
	{#if waitContinue}
		{@const pillW = SYMBOL_SIZE * 2.6}
		{@const pillH = SYMBOL_SIZE * 0.62}
		<Container
			y={frameH / 2 - SYMBOL_SIZE * 0.62}
			scale={continuePulse}
			eventMode="static"
			cursor="pointer"
			hitArea={new HitRectangle(-pillW / 2, -pillH / 2, pillW, pillH)}
			onpointerup={() => props.oncomplete()}
		>
			<Graphics
				eventMode="static"
				cursor="pointer"
				hitArea={new HitRectangle(-pillW / 2, -pillH / 2, pillW, pillH)}
				onpointerup={() => props.oncomplete()}
				draw={(g) => drawGlassPill(g, { width: pillW, height: pillH })}
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
		<!-- clinical chrome under the amount — dismiss prompt only -->
		<Container y={frameH / 2 + SYMBOL_SIZE * 1.72} alpha={0.72 + 0.18 * Math.sin(time * 3.2)}>
			<BitmapText
				anchor={0.5}
				text={skipHint}
				eventMode="none"
				tint={AMOUNT_TINT}
				style={{ fontFamily: AMOUNT_FAMILY, fontSize: winFontSize(0.18), letterSpacing: 3 }}
			/>
		</Container>
	{/if}
</Container>
