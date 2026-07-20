<script lang="ts">
	import { Text } from 'pixi-svelte';
	import { Sprite, getContextApp } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';
	import { stateModal, stateBet, stateBetDerived } from 'state-shared';

	import UiSprite from './UiSprite.svelte';
	import { UI_BASE_SIZE } from '../constants';
	import { HUD_THEME as T } from '../hudTheme';
	import { getContext } from '../context';

	const props: Partial<Omit<ButtonProps, 'children'>> = $props();
	const { stateXstateDerived, eventEmitter } = getContext();
	const appContext = getContextApp();
	const loadedAssets = $derived(appContext?.stateApp?.loadedAssets);

	// same width as the spin (bet) button
	const sizes = { width: UI_BASE_SIZE * 1.3, height: UI_BASE_SIZE * 0.55 };
	const disabled = $derived(!stateXstateDerived.isIdle());
	const active = $derived(stateBetDerived.activeBetMode()?.type === 'activate');
	const label = $derived(active ? 'ACTIVE' : 'BONUS');

	// optional studio/game emblem baked by the host app. Swap the art by
	// registering a `buyBonusLogo` sprite asset — nothing else needs to change.
	const LOGO_KEY = 'buyBonusLogo';
	const hasLogo = $derived(Boolean(loadedAssets?.[LOGO_KEY]));

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

	// with a logo the text sits to the right of the emblem; without, it centres
	const logoSize = $derived(sizes.height * 0.72);
</script>

<Button {...props} {sizes} {disabled} {onpress}>
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
			active
			{...disabled ? { backgroundColor: 0xaaaaaa } : {}}
		/>

		{#if hasLogo}
			<Sprite
				key={LOGO_KEY}
				anchor={0.5}
				x={center.x - sizes.width * 0.3}
				y={center.y}
				width={logoSize}
				height={logoSize}
				alpha={disabled ? 0.55 : 1}
			/>
			<Text
				x={center.x + sizes.width * 0.08}
				y={center.y}
				anchor={0.5}
				text={label}
				alpha={disabled ? 0.55 : 1}
				style={{
					fontFamily: T.fontDisplay,
					fontWeight: '900',
					fontSize: sizes.height * 0.34,
					fill: T.accent,
					letterSpacing: 2,
				}}
			/>
		{:else}
			<Text
				x={center.x}
				y={center.y}
				anchor={0.5}
				text={label}
				alpha={disabled ? 0.55 : 1}
				style={{
					fontFamily: T.fontDisplay,
					fontWeight: '900',
					fontSize: sizes.height * 0.42,
					fill: T.accent,
					letterSpacing: 3,
				}}
			/>
		{/if}
	{/snippet}
</Button>
