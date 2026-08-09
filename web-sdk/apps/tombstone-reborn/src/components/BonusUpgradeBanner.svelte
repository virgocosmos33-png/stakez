<script lang="ts" module>
	/** Mid-bonus scatter climbed the bonus one level (bookEventHandlerMap
	 * broadcasts this from bonusLevelUp) — NOT a retrigger, no spins added. */
	export type EmitterEventBonusUpgradeBanner = {
		type: 'levelUpBannerShow';
		level: 1 | 2 | 3;
	};
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { CanvasSizeRectangle, MainContainer } from 'components-layout';
	import { Container, Text } from 'pixi-svelte';
	import { playExternalOnce } from 'utils-sound';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { fxDur } from '../game/fxTiming';

	const context = getContext();

	const BRAND_FAMILY = 'Impact, "Arial Black", "Arial Narrow", Arial, sans-serif';
	const COPY = 0xece8df;
	const BLOOD = 0xff2d2d;

	// the level names the intro panels use — the upgrade stamps WHERE you are now
	const LEVEL_TITLES = {
		1: 'THE INTAKE',
		2: 'HER SIDE',
		3: 'WHITEOUT',
	} as const;

	// haunting sting shipped with the banner (trimmed to ~3s, fades out)
	const UPGRADE_SFX = new URL('../../assets/audio/bonus_upgrade.mp3', import.meta.url).href;

	/** how long BONUS UPGRADE holds on screen */
	const HOLD_MS = 2000;

	let show = $state(false);
	let level = $state<1 | 2 | 3>(1);
	const scale = new Tween(0);
	const alpha = new Tween(1);

	context.eventEmitter.subscribeOnMount({
		levelUpBannerShow: async (emitterEvent) => {
			level = emitterEvent.level;
			alpha.set(1, { duration: 0 });
			scale.set(0, { duration: 0 });
			show = true;
			playExternalOnce(UPGRADE_SFX);
			await scale.set(1, { duration: fxDur(320), easing: backOut });
			await new Promise((resolve) => setTimeout(resolve, HOLD_MS));
			await alpha.set(0, { duration: fxDur(260), easing: cubicOut });
			show = false;
		},
	});

	let time = $state(0);
	$effect(() => {
		if (!show) return;
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			time = (now - start) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
	const pulse = $derived(1 + 0.03 * Math.sin(time * 5));
</script>

{#if show}
	<Container alpha={alpha.current * 0.7}>
		<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.7} />
	</Container>
	<MainContainer>
		<Container
			x={context.stateGameDerived.boardLayout().x}
			y={context.stateGameDerived.boardLayout().y}
			scale={scale.current * pulse}
			alpha={alpha.current}
		>
			<Text
				anchor={0.5}
				y={-SYMBOL_SIZE * 0.42}
				text="BONUS UPGRADE"
				eventMode="none"
				style={{
					fontFamily: BRAND_FAMILY,
					fontWeight: '800',
					fontSize: SYMBOL_SIZE * 0.62,
					fill: COPY,
					align: 'center',
					letterSpacing: 4,
					stroke: { color: 0x000000, width: SYMBOL_SIZE * 0.05 },
					dropShadow: { color: 0x000000, blur: 14, distance: 6, alpha: 0.8 },
				}}
			/>
			<Text
				anchor={0.5}
				y={SYMBOL_SIZE * 0.34}
				text={LEVEL_TITLES[level]}
				eventMode="none"
				style={{
					fontFamily: BRAND_FAMILY,
					fontWeight: '800',
					fontSize: SYMBOL_SIZE * 0.3,
					fill: BLOOD,
					align: 'center',
					letterSpacing: 6,
					stroke: { color: 0x000000, width: SYMBOL_SIZE * 0.032 },
				}}
			/>
		</Container>
	</MainContainer>
{/if}
