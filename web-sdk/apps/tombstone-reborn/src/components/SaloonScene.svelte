<script lang="ts" module>
	import { SCENE_ART as SCENE_ART_SRC } from '../game/saloonLamps';

	export const SCENE_ART = SCENE_ART_SRC;
</script>

<script lang="ts">
	/**
	 * Live western room from TR2-Spine-Background-scene.
	 * Spine paints sky / clouds / town in PSD Z order when loaded.
	 * Flatten plate is fallback only. Hanging lamps always paint.
	 */
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import BarrelLampGlow from './BarrelLampGlow.svelte';
	import HangingLamps from './HangingLamps.svelte';
	import WesternSceneFx from './WesternSceneFx.svelte';
	import WesternSceneSpine from './WesternSceneSpine.svelte';
	import { isWesternSceneSkeleton } from '../game/westernScene';

	const context = getContext();

	const fit = $derived.by(() => {
		const canvas = context.stateLayoutDerived.canvasSizes();
		const scale = Math.max(canvas.width / SCENE_ART.width, canvas.height / SCENE_ART.height);
		return {
			x: canvas.width / 2,
			y: canvas.height / 2,
			scale: { x: scale, y: scale },
			pivot: { x: SCENE_ART.width / 2, y: SCENE_ART.height / 2 },
		};
	});

	const hasScene = $derived(isWesternSceneSkeleton(context.stateApp.loadedAssets?.westernScene));
	const plateKey = $derived(
		hasScene
			? null
			: context.stateApp.loadedAssets?.westernSceneBg
				? 'westernSceneBg'
				: context.stateApp.loadedAssets?.saloonPlate
					? 'saloonPlate'
					: null,
	);
</script>

<Container
	x={fit.x}
	y={fit.y}
	scale={fit.scale}
	pivot={fit.pivot}
	sortableChildren
>
	{#if plateKey}
		<Sprite
			key={plateKey}
			x={0}
			y={0}
			width={SCENE_ART.width}
			height={SCENE_ART.height}
			zIndex={0}
		/>
	{/if}
	<WesternSceneFx />
	<WesternSceneSpine />
	<BarrelLampGlow />
	<HangingLamps />
</Container>
