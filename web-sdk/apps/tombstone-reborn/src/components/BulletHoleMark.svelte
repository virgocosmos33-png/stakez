<script lang="ts">
	/**
	 * One stamped bullet-hole decal + a short hot flash on birth.
	 * Atlas: tools/make_bullet_hole_atlas.py → asset key `splitHoles`.
	 */
	import * as PIXI from 'pixi.js';
	import { BaseSprite, Container, Graphics, getContextApp } from 'pixi-svelte';

	import { TOMBSTONE_FX } from '../game/tombstoneVfx';

	type Props = {
		tex: number;
		x: number;
		y: number;
		scale?: number;
		rot?: number;
		/** performance.now() when stamped */
		born: number;
		/** live clock (ms) for flash fade — pass parent `performance.now()` or derived time */
		now: number;
		size?: number;
	};

	const props: Props = $props();
	const HOLE_ASSET = 'splitHoles';
	const SIZE = $derived(props.size ?? 96);

	const appContext = getContextApp();
	const frames = $derived(
		(appContext.stateApp.loadedAssets?.[HOLE_ASSET] as PIXI.Texture[] | undefined) ?? [],
	);
	const texture = $derived(frames[Math.min(Math.max(props.tex, 0), Math.max(frames.length - 1, 0))]);

	const ageMs = $derived(Math.max(0, props.now - props.born));
	const flash = $derived(ageMs < 90 ? 1 - ageMs / 90 : 0);
	const HIT_SCALE = $derived(SIZE * (props.scale ?? 1));

	// A hot ember in the fresh hole, sized off the stamped decal. This used to be
	// a cream disc at a fixed SIZE radius, so a small hole still flashed a pale
	// circle bigger than itself — one of the "white sparkle" marks on the board.
	const drawFlash = (g: import('pixi.js').Graphics) => {
		if (flash <= 0.01) return;
		g.circle(0, 0, HIT_SCALE * 0.16 * (1 + 0.5 * flash));
		g.fill({ color: TOMBSTONE_FX.bloodRust, alpha: 0.4 * flash });
		g.circle(0, 0, HIT_SCALE * 0.07);
		g.fill({ color: TOMBSTONE_FX.brass, alpha: 0.55 * flash });
	};
</script>

{#if texture}
	<BaseSprite
		{texture}
		anchor={0.5}
		x={props.x}
		y={props.y}
		width={SIZE * (props.scale ?? 1)}
		height={SIZE * (props.scale ?? 1)}
		rotation={props.rot ?? 0}
		alpha={0.72}
	/>
	{#if flash > 0.01}
		<Container x={props.x} y={props.y}>
			<Graphics draw={drawFlash} />
		</Container>
	{/if}
{/if}
