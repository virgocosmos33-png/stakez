<script lang="ts">
	/**
	 * Linked low-pay blood. CodePen nJyGmv drip on THIS letter.
	 * Parent CellClipMask is the pocket. Letter clip is canvas destination-in
	 * (studio black punched out). Do not sprite-mask the atlas card.
	 */
	import { onDestroy } from 'svelte';
	import { BaseSprite, Container } from 'pixi-svelte';
	import { Texture } from 'pixi.js';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { isLowPaySymbol } from '../game/gunsmokeSpin';
	import {
		destroyBloodPlate,
		lowFaceKey,
		makeBloodPlate,
		tickBloodPlate,
		type BloodPlate,
	} from '../game/lowLinkBlood';

	type Props = { reelIndex: number; row: number };
	const props: Props = $props();
	const context = getContext();

	let plate = $state<BloodPlate | null>(null);

	const clear = () => {
		if (plate) destroyBloodPlate(plate);
		plate = null;
	};

	const arm = () => {
		clear();
		const symbol = context.stateGame.board[props.reelIndex]?.reelState.symbols[props.row];
		const name = symbol?.rawSymbol.name;
		if (!name || !isLowPaySymbol(name)) return;
		const key = lowFaceKey(name);
		if (!key) return;
		const face = context.stateApp.loadedAssets?.[key] as Texture | undefined;
		if (!face || face === Texture.EMPTY || face.frame.width < 2) return;
		plate = makeBloodPlate(SYMBOL_SIZE * 2, SYMBOL_SIZE * 2, face);
	};

	const onTick = () => {
		if (plate) tickBloodPlate(plate);
	};

	context.eventEmitter.subscribeOnMount({
		winDimShow: ({ positions }) => {
			const hit = positions.some((p) => p.reel === props.reelIndex && p.row === props.row);
			if (hit) arm();
			else clear();
		},
		winDimHide: () => clear(),
		featureFxFallOut: () => clear(),
	});

	$effect(() => {
		if (!plate) return;
		const ticker = context.stateApp.pixiApplication?.ticker;
		if (!ticker) return;
		ticker.add(onTick);
		return () => ticker.remove(onTick);
	});

	onDestroy(() => clear());
</script>

{#if plate}
	<Container eventMode="none">
		<BaseSprite
			texture={plate.texture}
			anchor={0.5}
			width={SYMBOL_SIZE}
			height={SYMBOL_SIZE}
			eventMode="none"
		/>
	</Container>
{/if}
