<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { Graphics } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';
	import { stateModal, stateBet, stateBetDerived } from 'state-shared';

	import UiSprite from './UiSprite.svelte';
	import { UI_BASE_SIZE } from '../constants';
	import { getContext } from '../context';
	import { drawIcon } from '../icons';

	const props: Partial<Omit<ButtonProps, 'children'>> = $props();
	const { stateXstateDerived, eventEmitter } = getContext();
	const sizes = { width: UI_BASE_SIZE, height: UI_BASE_SIZE };
	const disabled = $derived(!stateXstateDerived.isIdle());
	const active = $derived(stateBetDerived.activeBetMode()?.type === 'activate');
	const iconSize = $derived(sizes.width * 0.5);
	const shadowOffset = $derived(iconSize * 0.06);

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

	const iconColor = $derived(disabled ? 0x6a6a70 : active ? 0xffc12e : 0xf1f1f4);
</script>

<Button {...props} {sizes} {disabled} {onpress}>
	{#snippet children({ center, hovered, pressed })}
		<UiSprite
			{...center}
			anchor={0.5}
			tone="dark"
			shape="medallion"
			width={sizes.width}
			height={sizes.height}
			{hovered}
			{pressed}
			{active}
			{...disabled ? { backgroundColor: 0xaaaaaa } : {}}
		/>

		<Graphics
			{...center}
			y={center.y + shadowOffset}
			alpha={0.4}
			draw={(g: PIXI.Graphics) => drawIcon(g, 'crown', { size: iconSize, color: 0x000000 })}
		/>
		<Graphics
			{...center}
			alpha={disabled ? 0.6 : 1}
			draw={(g: PIXI.Graphics) => drawIcon(g, 'crown', { size: iconSize, color: iconColor })}
		/>
	{/snippet}
</Button>
