<script lang="ts">
	/**
	 * The WIN multiplier badge shared by the nudge rider and the bounty/nudge
	 * payoff cells (StretchWays). Both used to hand-roll their own `roundRect`
	 * with a gold stroke and set `fontFamily: 'Arial'`, which is the flat amber
	 * outlined box the nudge event was reported for. One piece of real art and
	 * one typography token instead.
	 *
	 * The plate is oak banded with iron (Layer AI, tools/make_nudge_ui.py). Text
	 * takes the shared amount family so it moves with the game's type system.
	 */
	import { Container, Sprite, Text } from 'pixi-svelte';

	import { FEATURE_ART } from '../game/featureVfx';
	import { trAmountFamily } from '../game/typography';

	type Props = {
		/** already-formatted face, e.g. "x3" — the caller owns the odometer */
		label: string;
		x?: number;
		y?: number;
		/** plate width in board px; height follows the art's own ratio */
		width?: number;
		scale?: number;
		alpha?: number;
	};

	const { label, x = 0, y = 0, width = 84, scale = 1, alpha = 1 }: Props = $props();

	const AMOUNT_FAMILY = trAmountFamily();
	/** measured off fx_mult_plaque.png (512x199) */
	const PLATE_RATIO = 199 / 512;
	/** the oak field inside the iron band, as a share of the plate */
	const FACE_H = 0.52;

	const height = $derived(width * PLATE_RATIO);
</script>

<Container {x} {y} {scale} {alpha}>
	<Sprite key={FEATURE_ART.multPlaque} anchor={0.5} width={width} {height} />
	<Text
		anchor={0.5}
		text={label}
		eventMode="none"
		style={{
			fontFamily: AMOUNT_FAMILY,
			fontSize: Math.round(height * FACE_H),
			fill: 0xf2d79a,
			letterSpacing: 1,
			stroke: { color: 0x120c06, width: Math.max(2, height * 0.1) },
		}}
	/>
</Container>
