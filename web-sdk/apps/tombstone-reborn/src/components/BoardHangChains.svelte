<script lang="ts">
	/**
	 * One PSD chain island per hanger, in scene cover-fit (same as the plate).
	 * Base uses extracted chains-upframe pixels. Small/super keep their atmosphere skins
	 * at the same seats.
	 */
	import { Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { FRAME_SEATS } from '../game/frameSeats.generated';
	import { sceneToMain } from '../game/saloonLamps';

	const context = getContext();

	const atmoKey = $derived.by(() => {
		const atmo = context.stateGame.atmosphere;
		if (atmo === 'super') return 'hudChainSuper';
		if (atmo === 'small') return 'hudChainSmall';
		return null;
	});

	const segs = $derived.by(() => {
		const main = context.stateLayoutDerived.mainLayout();
		const canvas = context.stateLayoutDerived.canvasSizes();
		return FRAME_SEATS.chains.map((seat, i) => {
			const a = sceneToMain(seat.left, seat.top, canvas, main);
			const b = sceneToMain(seat.right, seat.bottom, canvas, main);
			return {
				id: seat.id,
				key: atmoKey ?? (`hangChain${i}` as const),
				x: a.x,
				y: a.y,
				w: Math.max(1, b.x - a.x),
				h: Math.max(1, b.y - a.y),
			};
		});
	});
</script>

{#each segs as seg (seg.id)}
	<Sprite
		key={seg.key}
		x={seg.x}
		y={seg.y}
		width={seg.w}
		height={seg.h}
		eventMode="none"
	/>
{/each}
