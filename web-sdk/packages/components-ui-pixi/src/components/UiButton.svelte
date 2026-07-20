<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { Graphics } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';

	import UiSprite from './UiSprite.svelte';
	import type { ButtonIcon } from '../types';
	import type { Snippet } from 'svelte';
	import { drawIcon } from '../icons';
	import { HUD_THEME as T } from '../hudTheme';

	type Props = Omit<ButtonProps, 'children'> & {
		icon: ButtonIcon;
		sizes: { width: number; height: number };
		active?: boolean;
		children?: Snippet;
		/** light = gilt-brass medallion, dark = tarnished-steel medallion */
		variant?: 'dark' | 'light';
		/** flat control-bar chrome (dark fill + steel border) */
		flat?: boolean;
		/** force the icon colour (overrides the active/disabled defaults) */
		iconColor?: number;
	};

	const {
		icon,
		active,
		variant = 'dark',
		flat = false,
		iconColor: iconColorProp,
		children: childrenFromParent,
		...buttonProps
	}: Props = $props();

	const tone = $derived(variant === 'light' ? 'accent' : 'dark');

	// warm ivory by default; turns gold when the button is active (e.g. turbo on)
	const iconColor = $derived(
		buttonProps.disabled
			? T.disabledIcon
			: iconColorProp != null
				? iconColorProp
				: active
					? T.accent
					: T.textPrimary,
	);

	const iconSize = $derived(Math.min(buttonProps.sizes.width, buttonProps.sizes.height) * 0.46);

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
			{flat}
			shape="medallion"
			{hovered}
			{pressed}
			{active}
			{...buttonProps.disabled ? { backgroundColor: 0xaaaaaa } : {}}
		/>

		<Graphics {...center} draw={drawFace} alpha={buttonProps.disabled ? 0.6 : 1} />

		{@render childrenFromParent?.()}
	{/snippet}
</Button>
