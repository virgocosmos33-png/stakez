<script lang="ts">
	/**
	 * Both PSD hanging lanterns, always mounted inside SaloonScene's cover-fit.
	 * PSD stills paint first (never gated). Spine idle draws on top only when
	 * loadedAssets holds real SkeletonData — a truthy-but-unusable spine key
	 * used to hide stills and leave the beam bare.
	 */
	import { onMount } from 'svelte';
	import { Texture } from 'pixi.js';
	import { BaseSprite, Container, Sprite, SpineProvider, SpineTrack } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { FRAME_SEATS } from '../game/frameSeats.generated';
	import { HANGING_LAMPS } from '../game/hangingLamps.generated';
	import {
		LAMP_BODY,
		ensureHangingLampSkeletons,
		isLampSkeleton,
		lampBodyTexture,
		loadHangingLampSources,
	} from '../game/ensureHangingLamps';

	const context = getContext();
	const seatL = FRAME_SEATS.lamps.L;
	const seatR = FRAME_SEATS.lamps.R;
	const stillSizeL = { w: seatL.right - seatL.left, h: seatL.bottom - seatL.top };
	const stillSizeR = { w: seatR.right - seatR.left, h: seatR.bottom - seatR.top };

	const injectSkeletons = () => {
		const cur = context.stateApp.loadedAssets;
		if (!cur?.hangingLampsAtlas) return;
		if (isLampSkeleton(cur.hangingLampL) && isLampSkeleton(cur.hangingLampR)) return;
		void loadHangingLampSources()
			.then((src) => {
				const latest = context.stateApp.loadedAssets;
				if (!latest?.hangingLampsAtlas) return;
				if (isLampSkeleton(latest.hangingLampL) && isLampSkeleton(latest.hangingLampR)) return;
				context.stateApp.loadedAssets = ensureHangingLampSkeletons(latest, src);
			})
			.catch((err) => {
				console.error('[HangingLamps] skeleton bootstrap failed', err);
			});
	};

	$effect.pre(() => {
		injectSkeletons();
	});

	const hasSpineL = $derived(isLampSkeleton(context.stateApp.loadedAssets?.['hangingLampL']));
	const hasSpineR = $derived(isLampSkeleton(context.stateApp.loadedAssets?.['hangingLampR']));
	const hasPsdL = $derived(Boolean(context.stateApp.loadedAssets?.['hangingLampStillL']));
	const hasPsdR = $derived(Boolean(context.stateApp.loadedAssets?.['hangingLampStillR']));
	const atlasTex = $derived(
		context.stateApp.loadedAssets?.['hangingLampsAtlas'] as Texture | undefined,
	);
	const atlasStillL = $derived(!hasPsdL && atlasTex ? lampBodyTexture(atlasTex, 'L') : null);
	const atlasStillR = $derived(!hasPsdR && atlasTex ? lampBodyTexture(atlasTex, 'R') : null);

	let swingT = $state(0);
	onMount(() => {
		let raf = 0;
		const origin = performance.now();
		const tick = (now: number) => {
			swingT = (now - origin) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	const period = HANGING_LAMPS.period;
	const swingL = $derived(((13 * Math.PI) / 180) * Math.cos((swingT * Math.PI * 2) / period));
	const swingR = $derived(((-16 * Math.PI) / 180) * Math.cos((swingT * Math.PI * 2) / period));
</script>

<Container zIndex={20} eventMode="none" sortableChildren>
	<Container
		x={HANGING_LAMPS.L.x}
		y={HANGING_LAMPS.L.y}
		rotation={hasSpineL ? 0 : swingL}
		zIndex={0}
		eventMode="none"
	>
		{#if hasPsdL}
			<Sprite
				key="hangingLampStillL"
				anchor={{ x: 0.5, y: 0 }}
				width={stillSizeL.w}
				height={stillSizeL.h}
			/>
		{:else if atlasStillL}
			<BaseSprite
				texture={atlasStillL}
				anchor={{ x: 0.5, y: 0 }}
				width={LAMP_BODY.L.w}
				height={LAMP_BODY.L.h}
			/>
		{/if}
	</Container>
	<Container
		x={HANGING_LAMPS.R.x}
		y={HANGING_LAMPS.R.y}
		rotation={hasSpineR ? 0 : swingR}
		zIndex={0}
		eventMode="none"
	>
		{#if hasPsdR}
			<Sprite
				key="hangingLampStillR"
				anchor={{ x: 0.5, y: 0 }}
				width={stillSizeR.w}
				height={stillSizeR.h}
			/>
		{:else if atlasStillR}
			<BaseSprite
				texture={atlasStillR}
				anchor={{ x: 0.5, y: 0 }}
				width={LAMP_BODY.R.w}
				height={LAMP_BODY.R.h}
			/>
		{/if}
	</Container>
	{#if hasSpineL}
		<SpineProvider key="hangingLampL" x={HANGING_LAMPS.L.x} y={HANGING_LAMPS.L.y} anchor={0} zIndex={1}>
			<SpineTrack trackIndex={0} animationName="idle" loop={true} />
		</SpineProvider>
	{/if}
	{#if hasSpineR}
		<SpineProvider key="hangingLampR" x={HANGING_LAMPS.R.x} y={HANGING_LAMPS.R.y} anchor={0} zIndex={1}>
			<SpineTrack trackIndex={0} animationName="idle" loop={true} />
		</SpineProvider>
	{/if}
</Container>
