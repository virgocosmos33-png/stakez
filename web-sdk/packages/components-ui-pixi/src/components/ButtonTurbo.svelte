<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { Graphics } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';
	import { stateBet, stateBetDerived } from 'state-shared';

	import UiSprite from './UiSprite.svelte';
	import { UI_BASE_SIZE } from '../constants';
	import { getContext } from '../context';
	import { HUD_THEME } from '../hudTheme';

	const props: Partial<Omit<ButtonProps, 'children'>> = $props();
	const context = getContext();
	const sizes = { width: UI_BASE_SIZE, height: UI_BASE_SIZE };

	// 0 = off, 1 = turbo, 2 = super turbo
	const level = $derived(stateBetDerived.turboLevel());
	const active = $derived(level > 0);
	const disabled = $derived(stateBet.isSpaceHold);

	const onpress = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		// off -> turbo -> super turbo -> off
		stateBetDerived.cycleTurbo();
	};

	context.eventEmitter.subscribeOnMount({
		stopButtonClick: () => stateBetDerived.updateIsTurbo(true, { persistent: false }),
		stopButtonEnable: () => stateBetDerived.updateIsTurbo(false, { persistent: false }),
	});

	const LIT = HUD_THEME.turboLit; // gold: an engaged bolt (themeable)
	const DIM = 0x5a6672; // steel: a dormant bolt

	// lightning bolt path (from icons.ts 'turbo'), centred, shifted by dx
	const boltPoly = (s: number, dx: number) =>
		(
			[
				[s * 0.08, -s * 0.4],
				[-s * 0.26, s * 0.06],
				[-s * 0.02, s * 0.06],
				[-s * 0.12, s * 0.4],
				[s * 0.28, -s * 0.1],
				[s * 0.02, -s * 0.1],
			] as const
		).flatMap(([x, y]) => [x + dx, y]);

	// two bolts side by side: left lights at turbo, right adds at super turbo
	const drawBolts = (g: PIXI.Graphics) => {
		const s = UI_BASE_SIZE * 0.36;
		const dx = UI_BASE_SIZE * 0.08;

		g.poly(boltPoly(s, -dx));
		g.fill({ color: level >= 1 ? LIT : DIM, alpha: level >= 1 ? 1 : 0.5 });

		g.poly(boltPoly(s, dx));
		g.fill({ color: level >= 2 ? LIT : DIM, alpha: level >= 2 ? 1 : 0.35 });
	};
</script>

<Button {...props} {sizes} {onpress} {disabled}>
	{#snippet children({ center, hovered, pressed })}
		<UiSprite
			{...center}
			anchor={0.5}
			width={sizes.width}
			height={sizes.height}
			tone="dark"
			flat
			shape="medallion"
			{hovered}
			{pressed}
			{active}
			{...disabled ? { backgroundColor: 0xaaaaaa } : {}}
		/>

		<Graphics {...center} draw={drawBolts} alpha={disabled ? 0.6 : 1} />
	{/snippet}
</Button>
