<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { Graphics } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';
	import { OnHotkey } from 'components-shared';
	import { stateBetDerived } from 'state-shared';

	import UiSprite from './UiSprite.svelte';
	import ButtonBetProvider from './ButtonBetProvider.svelte';
	import { UI_BASE_SIZE } from '../constants';
	import { drawIcon } from '../icons';

	const props: Partial<Omit<ButtonProps, 'children'>> = $props();
	const disabled = $derived(!stateBetDerived.isBetCostAvailable());
	// square cabinet panel — the reference's main spin button (square reads
	// heavier than the old circle, so keep the 1.3x footprint to preserve layout)
	const sizes = { width: UI_BASE_SIZE * 1.3, height: UI_BASE_SIZE * 1.3 };
	const iconSize = $derived(sizes.width * 0.46);
</script>

<ButtonBetProvider>
	{#snippet children({ key, onpress })}
		{@const isSpin = ['spin_default', 'spin_disabled'].includes(key)}
		{@const isDisabled = disabled || ['spin_disabled', 'stop_disabled'].includes(key)}
		{@const iconColor = isDisabled ? 0x6a6a70 : 0xffffff}
		<OnHotkey hotkey="Space" {disabled} {onpress} />
		<Button {...props} {sizes} {onpress} {disabled}>
			{#snippet children({ center, hovered, pressed })}
				<UiSprite
					{...center}
					anchor={0.5}
					tone="dark"
					shape="panel"
					width={sizes.width}
					height={sizes.height}
					{hovered}
					{pressed}
					{...isDisabled ? { backgroundColor: 0xaaaaaa } : {}}
				/>

				<Graphics
					{...center}
					alpha={isDisabled ? 0.6 : 1}
					draw={(g: PIXI.Graphics) =>
						drawIcon(g, isSpin ? 'spin' : 'stop', { size: iconSize, color: iconColor })}
				/>
			{/snippet}
		</Button>
	{/snippet}
</ButtonBetProvider>
