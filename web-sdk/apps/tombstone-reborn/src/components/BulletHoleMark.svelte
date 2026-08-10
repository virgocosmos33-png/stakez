<script lang="ts">
	/**
	 * One stamped bullet-hole decal + a short hot flash on birth.
	 * Atlas: tools/make_bullet_hole_atlas.py → asset key `splitHoles`.
	 */
	import * as PIXI from 'pixi.js';
	import { BaseSprite, Container, Graphics, getContextApp } from 'pixi-svelte';

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

	const drawFlash = (g: import('pixi.js').Graphics) => {
		if (flash <= 0.01) return;
		g.circle(0, 0, SIZE * 0.22 * (1 + flash));
		g.fill({ color: 0xf0d78c, alpha: 0.55 * flash });
		g.circle(0, 0, SIZE * 0.1);
		g.fill({ color: 0xc9a34a, alpha: 0.8 * flash });
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
		alpha={0.95}
	/>
	{#if flash > 0.01}
		<Container x={props.x} y={props.y}>
			<Graphics draw={drawFlash} />
		</Container>
	{/if}
{/if}
