<script lang="ts">
	/**
	 * Win-multi / ways stamp. Same RIP red glow as the hanging WAYS / MULTI
	 * wells so a cell mark and the HUD read as one language.
	 */
	import RedGlowMark from './RedGlowMark.svelte';

	type Props = {
		/** already-formatted face — win multi "x3", ways "3x". Caller owns the odometer. */
		label: string;
		x?: number;
		y?: number;
		/** plate width in board px; height follows a short RIP box */
		width?: number;
		scale?: number;
		alpha?: number;
	};

	const { label, x = 0, y = 0, width = 84, scale = 1, alpha = 1 }: Props = $props();
	const height = $derived(width * 0.42);
</script>

<RedGlowMark {label} {x} {y} {width} {height} {scale} {alpha} />
