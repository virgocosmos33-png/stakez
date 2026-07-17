<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import type { Texture, VideoSource } from 'pixi.js';
	import { Container, Graphics, Rectangle, Sprite, BitmapText } from 'pixi-svelte';
	import { ResponsiveBitmapText } from 'components-pixi';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { getTiersPassed } from '../game/winCelebrationMap';
	import type { SoundEffectName } from '../game/sound';

	type Props = {
		finalAmount: number; // book amount (100 = 1x bet)
		oncomplete: () => void;
	};

	const props: Props = $props();
	const context = getContext();

	// ------------------------------------------------------------------
	// staged counter: the reel switches EXACTLY when the rolling amount
	// crosses each real trigger (25x / 50x / 100x / 500x / 2500x / maxwin),
	// with per-segment pacing:
	//   BIG 25-50x     linear
	//   SUPER 50-100x  linear
	//   MEGA 100-500x  a bit fast at start, slowing near the target
	//   EPIC 500-2500x super fast start, braking to a total stop
	//   UNHOLY 2500x+  starts slow, keeps building speed
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

	const TIER_ENTRY_SOUND: Record<string, SoundEffectName> = {
		superwin: 'sfx_celeb_swell',
		mega: 'sfx_celeb_swell',
		epic: 'sfx_celeb_wobble',
	};

	// reverse whooshes ride the first second of every scene, pitch rotating
	// per scene: 0ms one pitch, ~620ms the complementary pitch
	const WHOOSH_SETS: [SoundEffectName, SoundEffectName][] = [
		['sfx_celeb_whoosh', 'sfx_celeb_whoosh_hi'],
		['sfx_celeb_whoosh_hi', 'sfx_celeb_whoosh_lo'],
		['sfx_celeb_whoosh_lo', 'sfx_celeb_whoosh'],
	];
	const sceneSounds = (target: number) => {
		const [first, second] = WHOOSH_SETS[target % WHOOSH_SETS.length];
		context.eventEmitter.broadcast({ type: 'soundOnce', name: first, forcePlay: true });
		setTimeout(() => {
			context.eventEmitter.broadcast({ type: 'soundOnce', name: second, forcePlay: true });
		}, 620);
	};

	const showTier = (target: number) => {
		if (target === displayedIndex) return;
		// the hit fires synchronously so a skip click is heard the same instant
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_celeb_hit', forcePlay: true });
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
			sceneSounds(target);
			const alias = tiers[target]?.alias ?? '';
			const entry = TIER_ENTRY_SOUND[alias];
			if (tiers[target]?.title === 'UNHOLY WIN') {
				context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_celeb_buildup' });
			} else if (alias === 'max') {
				context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_celeb_maxslam' });
			} else if (entry) {
				context.eventEmitter.broadcast({ type: 'soundOnce', name: entry });
			}
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

	context.eventEmitter.subscribeOnMount({
		celebrationSkip: () => skip(),
	});

	// tell the press catcher in Win.svelte when the CONTINUE gate is up
	$effect(() => {
		context.eventEmitter.broadcast({ type: 'celebrationGate', waiting: waitContinue });
	});

	// press anywhere: jump the current segment to its end (next reel starts
	// animating immediately); once on MAX WIN only the CONTINUE button works
	const skip = () => {
		if (waitContinue) return;
		if (finished) {
			props.oncomplete();
			return;
		}
		if (maxRecountStart !== null) {
			// clicking during the max recount jumps it to the end
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

	let time = $state(0);
	onMount(() => {
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_celeb_swell' });
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_celeb_hit', forcePlay: true });
		sceneSounds(0);
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
		return () => cancelAnimationFrame(raf);
	});

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	const celebration = $derived(tiers[displayedIndex] ?? tiers[0]);
	const title = $derived(celebration?.title ?? 'BIG WIN');
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
	const frameH = $derived(frameW * (1024 / 1536));
	const holeColW = $derived(frameW * 0.055);

	const jitterY = $derived((rand(Math.floor(time * 24)) - 0.5) * (3.2 + glitch.current * 9));
	const jitterX = $derived((rand(Math.floor(time * 24) * 7 + 3) - 0.5) * (1.6 + glitch.current * 7));
	const flicker = $derived(0.86 + 0.14 * rand(Math.floor(time * 18) * 13 + 1));

	const drawFilmDamage = (graphics: import('pixi.js').Graphics, timeValue: number) => {
		const w = frameW;
		const h = frameH;
		const chunk = Math.floor(timeValue * 12);
		for (let i = 0; i < 3; i++) {
			if (rand(chunk * 31 + i * 97) > 0.45) continue;
			const x = (rand(chunk * 17 + i * 53) - 0.5) * w;
			graphics.moveTo(x, -h / 2);
			graphics.lineTo(x + (rand(chunk + i) - 0.5) * 6, h / 2);
			graphics.stroke({
				color: rand(chunk * 3 + i) > 0.5 ? 0xd8cbb0 : 0x120a06,
				width: 1 + rand(chunk * 7 + i) * 1.4,
				alpha: 0.1 + rand(chunk * 11 + i) * 0.2,
			});
		}
		for (let i = 0; i < 7; i++) {
			if (rand(chunk * 41 + i * 13) > 0.5) continue;
			const x = (rand(chunk * 19 + i * 29) - 0.5) * w;
			const y = (rand(chunk * 23 + i * 37) - 0.5) * h;
			graphics.circle(x, y, 1 + rand(chunk * 29 + i) * 3.5);
			graphics.fill({ color: 0x0d0704, alpha: 0.25 + rand(chunk + i * 3) * 0.3 });
		}
		if (rand(chunk * 61) > 0.86) {
			const edgeX = rand(chunk * 67) > 0.5 ? w * 0.46 : -w * 0.46;
			graphics.circle(edgeX, (rand(chunk * 71) - 0.5) * h, 8 + rand(chunk * 73) * 18);
			graphics.fill({ color: 0x3a1a05, alpha: 0.35 });
		}
	};

	// glitch noise: static lines + blocks flashing during transitions
	const drawGlitchNoise = (graphics: import('pixi.js').Graphics, amount: number, timeValue: number) => {
		if (amount <= 0.01) return;
		const w = frameW;
		const h = frameH;
		const chunk = Math.floor(timeValue * 40);
		for (let i = 0; i < 10; i++) {
			if (rand(chunk * 13 + i * 7) > amount) continue;
			const y = (rand(chunk * 17 + i * 11) - 0.5) * h;
			graphics.rect(-w / 2, y, w, 1 + rand(chunk + i) * 2.5);
			graphics.fill({
				color: rand(chunk * 5 + i) > 0.5 ? 0xffffff : 0x2bff66,
				alpha: 0.14 * amount + rand(chunk * 3 + i) * 0.2 * amount,
			});
		}
		for (let i = 0; i < 5; i++) {
			if (rand(chunk * 23 + i * 19) > amount * 0.8) continue;
			const x = (rand(chunk * 29 + i * 3) - 0.5) * w;
			const y = (rand(chunk * 31 + i * 5) - 0.5) * h;
			graphics.rect(x, y, 20 + rand(chunk + i * 9) * 90, 4 + rand(chunk + i * 13) * 16);
			graphics.fill({ color: 0x000000, alpha: 0.5 * amount });
		}
	};

	const drawFilmFrame = (graphics: import('pixi.js').Graphics) => {
		const w = frameW;
		const h = frameH;
		const hole = holeColW;
		graphics.roundRect(-w / 2 - hole * 1.6, -h / 2 - 10, w + hole * 3.2, h + 20, 4);
		graphics.fill({ color: 0x0a0503, alpha: 0.96 });
		const holeH = h / 7;
		for (let i = 0; i < 6; i++) {
			const y = -h / 2 + holeH * (i + 0.5);
			for (const side of [-1, 1]) {
				graphics.roundRect(
					side * (w / 2 + hole * 0.35) - hole * 0.42,
					y - holeH * 0.26,
					hole * 0.84,
					holeH * 0.52,
					3,
				);
				graphics.fill({ color: 0x000000, alpha: 1 });
				graphics.roundRect(
					side * (w / 2 + hole * 0.35) - hole * 0.42,
					y - holeH * 0.26,
					hole * 0.84,
					holeH * 0.52,
					3,
				);
				graphics.stroke({ color: 0x2b1d10, width: 1.5, alpha: 0.9 });
			}
		}
		graphics.roundRect(-w / 2, -h / 2, w, h, 3);
		graphics.stroke({ color: 0x1c120a, width: 5, alpha: 1 });
	};

	const drawVignette = (graphics: import('pixi.js').Graphics) => {
		const w = frameW;
		const h = frameH;
		for (let i = 0; i < 4; i++) {
			graphics.roundRect(-w / 2 + i * 3, -h / 2 + i * 3, w - i * 6, h - i * 6, 6);
			graphics.stroke({ color: 0x000000, width: 14, alpha: 0.16 - i * 0.03 });
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
			<Rectangle isMask anchor={0.5} width={frameW} height={frameH} borderRadius={3} />
			<Sprite key={reelKey} anchor={0.5} width={frameW * 1.03} height={frameH * 1.03} />
			<!-- RGB-split ghosts: chromatic interference while glitching -->
			{#if glitch.current > 0.02}
				<Sprite
					key={reelKey}
					anchor={0.5}
					width={frameW * 1.03}
					height={frameH * 1.03}
					x={glitch.current * 11}
					tint={0xff4050}
					alpha={0.3 * glitch.current}
				/>
				<Sprite
					key={reelKey}
					anchor={0.5}
					width={frameW * 1.03}
					height={frameH * 1.03}
					x={-glitch.current * 11}
					tint={0x35ffe8}
					alpha={0.3 * glitch.current}
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
						width={frameW * 1.03}
						height={frameH * 1.03}
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
			style={{
				fontFamily: 'gold',
				fontSize: SYMBOL_SIZE * 0.52,
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
			style={{
				fontFamily: 'gold',
				fontSize: SYMBOL_SIZE * 1.05,
				align: 'center',
				fontWeight: 'bold',
				letterSpacing: 0,
			}}
		/>
	</Container>

	<!-- MAX WIN gate: the only way out is the CONTINUE button, overlaid on the
		lower part of the film frame so it is always on screen -->
	{#if waitContinue}
		<Container y={frameH / 2 - SYMBOL_SIZE * 0.62} scale={continuePulse}>
			<Rectangle
				anchor={0.5}
				width={SYMBOL_SIZE * 2.6}
				height={SYMBOL_SIZE * 0.62}
				borderRadius={SYMBOL_SIZE * 0.31}
				backgroundColor={0x0a0503}
				backgroundAlpha={0.92}
				borderColor={0x2bff66}
				borderWidth={3}
				borderAlpha={0.9}
				eventMode="static"
				cursor="pointer"
				onpointerup={() => props.oncomplete()}
			/>
			<BitmapText
				anchor={0.5}
				text="CONTINUE"
				eventMode="none"
				style={{ fontFamily: 'gold', fontSize: SYMBOL_SIZE * 0.32, letterSpacing: 2 }}
			/>
		</Container>
	{/if}
</Container>
