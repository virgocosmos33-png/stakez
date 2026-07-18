<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { Graphics } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';

	import UiSprite from './UiSprite.svelte';
	import type { ButtonIcon } from '../types';
	import type { Snippet } from 'svelte';
	import { drawIcon } from '../icons';

	type Props = Omit<ButtonProps, 'children'> & {
		icon: ButtonIcon;
		sizes: { width: number; height: number };
		active?: boolean;
		children?: Snippet;
		/** light = gilt-brass medallion, dark = tarnished-steel medallion */
		variant?: 'dark' | 'light';
	};

	const {
		icon,
		active,
		variant = 'dark',
		children: childrenFromParent,
		...buttonProps
	}: Props = $props();

	const tone = $derived(variant === 'light' ? 'accent' : 'dark');

	const iconColor = $derived.by(() => {
		if (buttonProps.disabled) return 0x6a6a70;
		if (icon === 'soundOn') return 0xffc12e;
		if (icon === 'turbo') return active ? 0xffc12e : 0xf1f1f4;
		if (active) return 0xffc12e;
		return 0xf1f1f4;
	});

	const iconSize = $derived(Math.min(buttonProps.sizes.width, buttonProps.sizes.height) * 0.5);
	const shadowOffset = $derived(Math.max(1.5, iconSize * 0.06));

	const drawShadow = (g: PIXI.Graphics) => drawIcon(g, icon, { size: iconSize, color: 0x000000 });
	const drawFace = (g: PIXI.Graphics) =>
		drawIcon(g, icon, { size: iconSize, color: iconColor, accent: iconColor });
</script>

<Button {...buttonProps}>
	{#snippet children({ center, hovered, pressed })}
		<UiSprite
			{...center}
			anchor={0.5}
			width={buttonProps.sizes.width}
			height={buttonProps.sizes.height}
			{tone}
			shape="medallion"
			{hovered}
			{pressed}
			{active}
			{...buttonProps.disabled ? { backgroundColor: 0xaaaaaa } : {}}
		/>

		<Graphics
			{...center}
			y={center.y + shadowOffset}
			draw={drawShadow}
			alpha={buttonProps.disabled ? 0.25 : 0.45}
		/>
		<Graphics {...center} draw={drawFace} alpha={buttonProps.disabled ? 0.6 : 1} />

		{@render childrenFromParent?.()}
	{/snippet}
</Button>
