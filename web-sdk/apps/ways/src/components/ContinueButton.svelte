<script lang="ts">
	// Single continue button used across every "press to continue" moment
	// (big/max-win celebration, free-spin outro) so they always look identical:
	// the haunted-glass pill + crisp WHITE label with a black outline for
	// guaranteed legibility over any background.
	import { Container, Graphics, Text } from 'pixi-svelte';

	import { SYMBOL_SIZE } from '../game/constants';
	import { drawGlassPill } from '../game/glassChrome';

	type Props = {
		onpress: () => void;
		text?: string;
		width?: number;
		height?: number;
		/** live pulse scale (e.g. a gentle breathing tween) */
		pulse?: number;
	};

	const props: Props = $props();

	const label = $derived(props.text ?? 'CONTINUE');
	const w = $derived(props.width ?? SYMBOL_SIZE * 3.2);
	const h = $derived(props.height ?? SYMBOL_SIZE * 0.62);
</script>

<Container scale={props.pulse ?? 1}>
	<Graphics
		eventMode="static"
		cursor="pointer"
		onpointerup={() => props.onpress()}
		draw={(g) => drawGlassPill(g, { width: w, height: h })}
	/>
	<Text
		anchor={0.5}
		text={label}
		eventMode="none"
		style={{
			fill: 0xffffff,
			fontSize: h * 0.4,
			align: 'center',
			fontFamily: '"Segoe UI", Arial, Helvetica, sans-serif',
			fontWeight: '700',
			letterSpacing: 2,
			stroke: { color: 0x000000, width: 4 },
		}}
	/>
</Container>
