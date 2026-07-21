<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { BaseSprite, Graphics } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';
	import { stateModal, stateBet, stateBetDerived } from 'state-shared';

	import { UI_BASE_SIZE } from '../constants';
	import { getContext } from '../context';
	import { BUY_BONUS_LOGO_DATA_URL } from '../assets/buyBonusLogoData';

	const props: Partial<Omit<ButtonProps, 'children'>> = $props();
	const { stateXstateDerived, eventEmitter } = getContext();

	const D = UI_BASE_SIZE * 1.2;
	const sizes = { width: D, height: D };
	const disabled = $derived(!stateXstateDerived.isIdle());
	const active = $derived(stateBetDerived.activeBetMode()?.type === 'activate');

	let logoTexture = $state<PIXI.Texture | null>(null);

	$effect(() => {
		let cancelled = false;
		const img = new Image();
		img.decoding = 'async';
		img.onload = () => {
			if (cancelled) return;
			logoTexture = PIXI.Texture.from(img);
		};
		img.onerror = () => console.error('ButtonBuyBonus logo decode failed');
		img.src = BUY_BONUS_LOGO_DATA_URL;
		return () => {
			cancelled = true;
		};
	});

	const openModal = () => (stateModal.modal = { name: 'buyBonus' });
	const disableActiveBetMode = () => (stateBet.activeBetModeKey = 'BASE');
	const onpress = () => {
		eventEmitter.broadcast({ type: 'soundPressGeneral' });
		if (active) {
			disableActiveBetMode();
		} else {
			openModal();
		}
	};

	const logoAlpha = $derived(disabled ? 0.35 : active ? 1 : 0.7);
	const logoSize = D * 0.78;

	const drawCircle = (g: PIXI.Graphics, hovered: boolean) => {
		const R = D / 2;
		const c = R;
		// face
		g.circle(c, c, R);
		g.fill({ color: disabled ? 0x14181f : hovered || active ? 0x161d26 : 0x10161d });
		// steel ring so it matches the rest of the HUD (no gold anywhere)
		g.circle(c, c, R - 1.5);
		g.stroke({ color: disabled ? 0x2a3542 : hovered || active ? 0x5a6672 : 0x3a4552, width: 3 });
	};
</script>

<Button {...props} {sizes} {disabled} {onpress}>
	{#snippet children({ center, hovered })}
		<Graphics draw={(g: PIXI.Graphics) => drawCircle(g, hovered)} />
		{#if logoTexture}
			<BaseSprite
				texture={logoTexture}
				anchor={0.5}
				x={center.x}
				y={center.y}
				width={logoSize}
				height={logoSize}
				alpha={logoAlpha}
			/>
		{/if}
	{/snippet}
</Button>
