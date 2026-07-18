<script lang="ts">
	import type { Texture, VideoSource } from 'pixi.js';
	import { Sprite } from 'pixi-svelte';
	import { onMount } from 'svelte';

	import { getContext } from '../game/context';

	type Props = {
		oncomplete: () => void;
	};

	const props: Props = $props();
	const context = getContext();

	// "Enter the mirror" intro: a cinematic dive THROUGH Madam Mirror's haunted
	// glass into a swirling violet void, generated image-to-video from the game's
	// own key art (tools/scenario_intro_video.py + post_process_intro.py). It ends
	// faded to the game's dark violet so the hand-off to the board is seamless.
	// Landscape 16:9 / portrait 9:16.
	const LANDSCAPE = { width: 1280, height: 720 };
	const PORTRAIT = { width: 720, height: 1280 };

	const isPortrait = $derived(context.stateLayoutDerived.layoutType() === 'portrait');
	const key = $derived(isPortrait ? 'introMirrorPortrait' : 'introMirror');
	const art = $derived(isPortrait ? PORTRAIT : LANDSCAPE);

	const videoTextureOf = (assetKey: string) =>
		context.stateApp.loadedAssets?.[assetKey] as Texture | undefined;

	// cover-fit the clip to the canvas, cropping the overflow
	const coverProps = () => {
		const canvas = context.stateLayoutDerived.canvasSizes();
		const scale = Math.max(canvas.width / art.width, canvas.height / art.height);
		return {
			anchor: 0.5,
			x: canvas.width / 2,
			y: canvas.height / 2,
			width: art.width * scale,
			height: art.height * scale,
		};
	};

	let finished = false;
	const finish = () => {
		if (finished) return;
		finished = true;
		props.oncomplete();
	};

	// play the clip once from the top (Pixi may have autoplayed/looped it while it
	// sat loaded), then hand off to the game when it ends
	$effect(() => {
		const source = videoTextureOf(key)?.source as VideoSource | undefined;
		const video = source?.resource as HTMLVideoElement | undefined;
		if (!video) return;
		video.loop = false;
		video.muted = true;
		try {
			video.currentTime = 0;
		} catch {
			/* seeking before metadata is fine to ignore */
		}
		video.play().catch(() => {});
		video.onended = finish;
	});

	onMount(() => {
		// never strand the player: skip straight to the game if the clip is missing,
		// and keep a safety net in case the 'ended' event never fires
		if (!videoTextureOf(key)) {
			finish();
			return;
		}
		const timer = setTimeout(finish, 9000);
		return () => clearTimeout(timer);
	});
</script>

{#if videoTextureOf(key)}
	<Sprite {key} {...coverProps()} />
{/if}
