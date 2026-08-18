<script lang="ts">
	/**
	 * Counter mark: black well, white face, bone edge. No red.
	 * Win multi reads "x4"; extra-ways reads "2x".
	 */
	import { Container, Graphics, Text } from 'pixi-svelte';
	import type { Graphics as PixiGraphics } from 'pixi.js';

	import { trValueStyle } from '../game/typography';

	type Props = {
		label: string;
		x?: number;
		y?: number;
		width?: number;
		height?: number;
		fontSize?: number;
		scale?: number;
		alpha?: number;
		/** default centre. `{x:1,y:1}` hangs from the bottom-right like a split count. */
		anchor?: { x: number; y: number };
	};

	const props: Props = $props();

	const fontSize = $derived(
		props.fontSize ?? Math.round((props.height ?? 28) * 0.55),
	);
	const box = $derived.by(() => {
		const padX = fontSize * 0.58;
		const padY = fontSize * 0.36;
		const w =
			props.width ??
			Math.max(fontSize * 1.85, props.label.length * fontSize * 0.62 + padX * 2);
		const h = props.height ?? fontSize + padY * 2;
		return { w, h };
	});
	const origin = $derived.by(() => {
		const a = props.anchor ?? { x: 0.5, y: 0.5 };
		return { x: (0.5 - a.x) * box.w, y: (0.5 - a.y) * box.h };
	});

	const drawPlate = (g: PixiGraphics, w: number, h: number) => {
		const r = Math.min(w, h) * 0.14;
		g.roundRect(-w / 2, -h / 2, w, h, r);
		g.fill({ color: 0x05070a, alpha: 0.94 });
		g.roundRect(-w / 2, -h / 2, w, h, r);
		g.stroke({ width: Math.max(1.5, h * 0.06), color: 0xd8d0c4, alpha: 0.7 });
	};
</script>

<Container
	x={props.x ?? 0}
	y={props.y ?? 0}
	scale={props.scale ?? 1}
	alpha={props.alpha ?? 1}
	eventMode="none"
>
	<Container x={origin.x} y={origin.y} eventMode="none">
		<Graphics draw={(g) => drawPlate(g, box.w, box.h)} eventMode="none" />
		<Text
			anchor={0.5}
			text={props.label}
			eventMode="none"
			style={trValueStyle({
				fontSize,
				fill: 0xffffff,
				letterSpacing: 0.6,
				stroke: { color: 0x05070a, width: Math.max(2, fontSize * 0.12) },
			})}
		/>
	</Container>
</Container>
