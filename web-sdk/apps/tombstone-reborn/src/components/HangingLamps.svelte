<script lang="ts">
	/**
	 * Visible street lanterns. Stills always paint so the beam is never bare.
	 * Swing + oil light are the ready scene `idle` clip. Do not freeze
	 * stills when a lamp skeleton duck-types true.
	 */
	import { onMount } from 'svelte';
	import { Texture } from 'pixi.js';
	import { BaseSprite, Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { FRAME_SEATS } from '../game/frameSeats.generated';
	import { HANGING_LAMPS } from '../game/hangingLamps.generated';
	import { LAMP_BODY, lampBodyTexture } from '../game/ensureHangingLamps';
	import { westernIdleLampLight, westernIdleLampRotation } from '../game/westernScene';

	const context = getContext();
	const seatL = FRAME_SEATS.lamps.L;
	const seatR = FRAME_SEATS.lamps.R;
	const stillSizeL = { w: seatL.right - seatL.left, h: seatL.bottom - seatL.top };
	const stillSizeR = { w: seatR.right - seatR.left, h: seatR.bottom - seatR.top };

	const hasPsdL = $derived(Boolean(context.stateApp.loadedAssets?.['hangingLampStillL']));
	const hasPsdR = $derived(Boolean(context.stateApp.loadedAssets?.['hangingLampStillR']));
	const hasLightL = $derived(Boolean(context.stateApp.loadedAssets?.['hangingLampLightL']));
	const hasLightR = $derived(Boolean(context.stateApp.loadedAssets?.['hangingLampLightR']));
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

	const swingL = $derived(westernIdleLampRotation('L', swingT));
	const swingR = $derived(westernIdleLampRotation('R', swingT));
	const lightL = $derived(westernIdleLampLight('L', swingT));
	const lightR = $derived(westernIdleLampLight('R', swingT));
</script>

<Container zIndex={20} eventMode="none" sortableChildren>
	<Container x={HANGING_LAMPS.L.x} y={HANGING_LAMPS.L.y} rotation={swingL} zIndex={0} eventMode="none">
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
		{#if hasLightL}
			<Sprite
				key="hangingLampLightL"
				anchor={{ x: 0.5, y: 0 }}
				width={stillSizeL.w}
				height={stillSizeL.h}
				alpha={lightL.a}
				tint={0xffffff}
				blendMode="add"
			/>
		{/if}
	</Container>
	<Container x={HANGING_LAMPS.R.x} y={HANGING_LAMPS.R.y} rotation={swingR} zIndex={0} eventMode="none">
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
		{#if hasLightR}
			<Sprite
				key="hangingLampLightR"
				anchor={{ x: 0.5, y: 0 }}
				width={stillSizeR.w}
				height={stillSizeR.h}
				alpha={lightR.a}
				tint={0xffffff}
				blendMode="add"
			/>
		{/if}
	</Container>
</Container>
