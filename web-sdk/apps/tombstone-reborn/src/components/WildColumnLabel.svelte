<script lang="ts" module>
	/**
	 * The label on a full wild column.
	 *
	 * Two different features put a wild column on a reel — the Wild Reel slides
	 * one in, the wild-mode Stretch pulls one open — and they used to label
	 * themselves differently ("WILD" over a multiplier versus a bare "N WAYS"),
	 * which read as two unrelated mechanics even though the column is the same
	 * thing in both. They share this so they cannot drift apart again.
	 *
	 * The type is sized off CELL_PITCH_X rather than set in absolute points. At a
	 * fixed 46px "WILD" was wider than the reel and painted over whatever the
	 * neighbouring column was showing.
	 */
	import { CELL_PITCH_X, SYMBOL_SIZE } from '../game/constants';

	const WILD_FONT = CELL_PITCH_X * 0.26;
	const WAYS_FONT = CELL_PITCH_X * 0.22;
	const PLATE_W = CELL_PITCH_X * 0.74;
	const PLATE_H = SYMBOL_SIZE * 0.34;
</script>

<script lang="ts">
	import { Container, Text } from 'pixi-svelte';

	import { trLabelStyle } from '../game/typography';
	import { formatWaysMult } from '../game/waysFormat';
	import RedGlowMark from './RedGlowMark.svelte';

	type Props = {
		x: number;
		y: number;
		/** what the whole column is worth */
		ways: number;
		/** 0 = not yet stamped, 1 = fully punched in */
		progress: number;
		/** extra scale for a count-up throb, if the caller wants one */
		pop?: number;
	};

	const props: Props = $props();

	const p = $derived(Math.min(Math.max(props.progress, 0), 1));
</script>

{#if p > 0.001}
	<Container
		x={props.x}
		y={props.y}
		scale={(0.6 + 0.4 * p) * (props.pop ?? 1)}
		alpha={Math.min(1, p * 1.8)}
	>
		<Text
			anchor={0.5}
			y={-SYMBOL_SIZE * 0.26}
			text="WILD"
			style={trLabelStyle({
				fontWeight: '700',
				fontSize: WILD_FONT,
				fill: 0xffffff,
				stroke: { color: 0x000000, width: 5 },
				letterSpacing: 1,
			})}
		/>
		<RedGlowMark
			y={SYMBOL_SIZE * 0.16}
			label={formatWaysMult(props.ways)}
			width={PLATE_W}
			height={PLATE_H}
			fontSize={WAYS_FONT}
		/>
	</Container>
{/if}
