<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { Graphics } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';
	import { stateModal } from 'state-shared';

	import UiSprite from './UiSprite.svelte';
	import { UI_BASE_SIZE } from '../constants';
	import { HUD_THEME as T } from '../hudTheme';
	import { drawIcon, drawTheatreMask } from '../icons';
	import { getContext } from '../context';

	type Props = Partial<Omit<ButtonProps, 'children'>> & {
		/** rendered square side (px) */
		size?: number;
	};

	const { size = UI_BASE_SIZE, ...buttonProps }: Props = $props();
	const context = getContext();

	const sizes = $derived({ width: size, height: size });
	const maskSize = $derived(size * 0.52);
	const hole = T.bodyFill;

	// brand/info tile → opens the feature & buy menu (where EXTRA BET / feature
	// spins / bonus buys live), preserving that entry point in the new layout.
	const onpress = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateModal.modal = { name: 'buyBonus' };
	};

	// decorative dotted quarter-arc + sparkle in the top-right corner
	const drawDecor = (g: PIXI.Graphics) => {
		const cx = size * 0.34;
		const cy = -size * 0.34;
		const r = size * 0.16;
		for (let i = 0; i < 6; i++) {
			const a = Math.PI * 0.5 + (i / 5) * Math.PI * 0.5; // sweeps the corner
			g.circle(cx + Math.cos(a) * r, cy - Math.sin(a) * r, Math.max(1.2, size * 0.012));
			g.fill({ color: T.line, alpha: 0.6 });
		}
	};
</script>

<Button {...buttonProps} {sizes} {onpress}>
	{#snippet children({ center, hovered, pressed })}
		<UiSprite
			{...center}
			anchor={0.5}
			shape="medallion"
			width={sizes.width}
			height={sizes.height}
			{hovered}
			{pressed}
		/>

		<!-- back mask: tragedy (frown), tilted left, offset up-left -->
		<Graphics
			x={center.x - size * 0.11}
			y={center.y - size * 0.05}
			rotation={-0.24}
			draw={(g: PIXI.Graphics) => drawTheatreMask(g, { size: maskSize, hole, smile: false })}
		/>
		<!-- front mask: comedy (smile), tilted right, offset down-right -->
		<Graphics
			x={center.x + size * 0.12}
			y={center.y + size * 0.06}
			rotation={0.18}
			draw={(g: PIXI.Graphics) => drawTheatreMask(g, { size: maskSize, hole, smile: true })}
		/>

		<Graphics x={center.x} y={center.y} draw={drawDecor} />
		<Graphics
			x={center.x + size * 0.3}
			y={center.y - size * 0.3}
			draw={(g: PIXI.Graphics) => drawIcon(g, 'sparkle', { size: size * 0.1, color: T.line })}
		/>
	{/snippet}
</Button>
