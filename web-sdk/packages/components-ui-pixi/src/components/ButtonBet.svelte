<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { Graphics } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';
	import { OnHotkey } from 'components-shared';
	import { stateBetDerived } from 'state-shared';

	import ButtonBetProvider from './ButtonBetProvider.svelte';
	import { UI_BASE_SIZE } from '../constants';
	import { drawIcon } from '../icons';
	import { HUD_THEME as T } from '../hudTheme';

	const props: Partial<Omit<ButtonProps, 'children'>> = $props();
	const disabled = $derived(!stateBetDerived.isBetCostAvailable());
	// gold coin — same chrome as Buy Bonus
	const D = UI_BASE_SIZE * 1.2;
	const sizes = { width: D, height: D };
	const iconSize = $derived(D * 0.42);

	const drawCoin = (g: PIXI.Graphics, isDisabled: boolean, hovered: boolean) => {
		const R = D / 2;
		const c = R;
		// outer gold ring
		g.circle(c, c, R);
		g.fill({ color: isDisabled ? 0x6a6a70 : hovered ? T.spinCoinRimHover : T.spinCoinRim });
		// dark bezel
		g.circle(c, c, R - 3);
		g.fill({ color: 0x1c2530 });
		// gold body
		g.circle(c, c, R - 7);
		g.fill({ color: isDisabled ? 0x8a8a8a : T.spinCoinBody });
		if (!isDisabled) {
			g.circle(c - R * 0.22, c - R * 0.26, R * 0.62);
			g.fill({ color: 0xffd94a, alpha: 0.6 });
			g.circle(c + R * 0.16, c + R * 0.3, R * 0.6);
			g.fill({ color: 0xe29c00, alpha: 0.35 });
		}
	};
</script>

<ButtonBetProvider>
	{#snippet children({ key, onpress })}
		{@const isSpin = ['spin_default', 'spin_disabled'].includes(key)}
		{@const isDisabled = disabled || ['spin_disabled', 'stop_disabled'].includes(key)}
		{@const iconColor = isDisabled ? 0x6a6a70 : 0x12305c}
		<OnHotkey hotkey="Space" {disabled} {onpress} />
		<Button {...props} {sizes} {onpress} {disabled}>
			{#snippet children({ center, hovered })}
				<Graphics draw={(g: PIXI.Graphics) => drawCoin(g, isDisabled, hovered)} />

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
