<script lang="ts">
	/**
	 * Ambient video that must never go empty. Two decoders run the same
	 * file, offset by half a loop. Coverage drops only when a copy is
	 * seeking, ended, or in the last FADE seconds — the other copy is
	 * then mid-clip and carries the picture. Rewind happens only on the
	 * hidden copy, so a seek flash is never on screen.
	 */
	import { onMount } from 'svelte';
	import { Texture, VideoSource } from 'pixi.js';
	import { BaseSprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	type Props = {
		assetKey: string;
		x: number;
		y: number;
		width: number;
		height: number;
		anchor?: number | { x: number; y: number };
		alpha?: number;
		blendMode?: 'normal' | 'add' | 'screen' | 'multiply';
		zIndex?: number;
	};

	const props: Props = $props();
	const context = getContext();
	const FADE = 1.0;

	const assetVideo = () => {
		const tex = context.stateApp.loadedAssets?.[props.assetKey] as Texture | undefined;
		return (tex?.source as VideoSource | undefined)?.resource as HTMLVideoElement | undefined;
	};

	let texA = $state<Texture | undefined>();
	let texB = $state<Texture | undefined>();
	let weightA = $state(1);
	let weightB = $state(0);

	const master = $derived(props.alpha ?? 1);
	const anchor = $derived(props.anchor ?? 0.5);

	onMount(() => {
		const a = assetVideo();
		const assetTex = context.stateApp.loadedAssets?.[props.assetKey] as Texture | undefined;
		if (!a || !assetTex) return;

		const arm = (v: HTMLVideoElement) => {
			// Native loop snaps to 0 and flashes an empty frame. We wrap
			// the hidden copy ourselves so the visible one never seeks.
			v.loop = false;
			v.muted = true;
			v.playsInline = true;
			v.preload = 'auto';
		};
		arm(a);

		const b = document.createElement('video');
		arm(b);
		b.src = a.currentSrc || a.src;

		const bSource = new VideoSource({
			resource: b,
			autoPlay: false,
			loop: false,
			muted: true,
			playsinline: true,
		});
		const bTex = new Texture({ source: bSource });

		texA = assetTex;
		texB = bTex;

		let offsetReady = false;
		let raf = 0;

		const play = (v: HTMLVideoElement) => {
			if (v.paused) v.play().catch(() => {});
		};

		const coverage = (v: HTMLVideoElement) => {
			const d = v.duration;
			if (!d || !Number.isFinite(d)) return 0;
			if (v.ended || v.seeking || v.readyState < 2) return 0;
			const remain = d - v.currentTime;
			if (remain < FADE) return Math.max(0, remain / FADE);
			return 1;
		};

		const rewind = (v: HTMLVideoElement) => {
			const d = v.duration;
			if (!d || !Number.isFinite(d)) return;
			if (!v.ended && v.currentTime < d - 0.12) return;
			try {
				v.currentTime = 0.08;
			} catch {
				/* seek can throw before metadata */
			}
			play(v);
		};

		const placeOffset = () => {
			if (offsetReady) return;
			const d = b.duration || a.duration;
			if (!d || !Number.isFinite(d) || d < FADE * 2 + 0.5) return;
			try {
				b.currentTime = d * 0.5;
			} catch {
				return;
			}
			offsetReady = true;
			play(b);
		};

		const onMeta = () => placeOffset();
		b.addEventListener('loadedmetadata', onMeta);
		if (b.readyState >= 1) placeOffset();

		const tick = () => {
			play(a);
			play(b);
			placeOffset();

			const cA = coverage(a);
			const cB = coverage(b);
			let wA = cA;
			let wB = cB;
			if (cA >= 1 && cB >= 1) {
				wA = 1;
				wB = 0;
			} else if (cA + cB < 0.12) {
				wA = a.readyState >= 2 && !a.ended ? 1 : 0;
				wB = 1 - wA;
			} else {
				const s = cA + cB;
				wA = cA / s;
				wB = cB / s;
			}
			weightA = wA;
			weightB = wB;

			if (wB >= 0.85) rewind(a);
			if (wA >= 0.85) rewind(b);

			raf = requestAnimationFrame(tick);
		};

		play(a);
		raf = requestAnimationFrame(tick);

		return () => {
			cancelAnimationFrame(raf);
			b.removeEventListener('loadedmetadata', onMeta);
			a.pause();
			b.pause();
			b.removeAttribute('src');
			b.load();
			bTex.destroy(true);
			texB = undefined;
		};
	});
</script>

{#if texA}
	<BaseSprite
		texture={texA}
		x={props.x}
		y={props.y}
		width={props.width}
		height={props.height}
		{anchor}
		alpha={master * weightA}
		blendMode={props.blendMode}
		zIndex={props.zIndex}
		eventMode="none"
	/>
{/if}
{#if texB}
	<BaseSprite
		texture={texB}
		x={props.x}
		y={props.y}
		width={props.width}
		height={props.height}
		{anchor}
		alpha={master * weightB}
		blendMode={props.blendMode}
		zIndex={props.zIndex}
		eventMode="none"
	/>
{/if}
