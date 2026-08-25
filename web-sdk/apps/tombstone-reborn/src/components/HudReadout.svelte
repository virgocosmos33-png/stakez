<script lang="ts">
	/**
	 * WAYS / MULTI / WIN / FREE SPINS drawn from PSD layer pixels at PSD
	 * seats (scene cover-fit). Box + pallet stack like the PSD. Numbers
	 * sit in the well only — they do not cover the wood label.
	 * WIN / FREE SPINS wells are the box PNG opening below the pallet.
	 */
	import { Container, Rectangle, Sprite, Text } from 'pixi-svelte';

	import type { HudPlaqueGeom } from '../game/hudPlaqueSeats';
	import { hudColor } from '../game/hud.generated';
	import { multiHang, multiHangPose, syncMultiHang } from '../game/multiHang';
	import { fitFontSize, trValueStyle } from '../game/typography';

	type Props = {
		plaques: HudPlaqueGeom[];
		parts?: 'all' | 'chains' | 'plate' | 'boxes';
		heldLabels?: string[];
	};

	const props: Props = $props();
	const parts = $derived(props.parts ?? 'all');
	const hasMulti = $derived(props.plaques.some((p) => p.label === 'MULTI'));
	const multiLive = $derived(hasMulti && !(props.heldLabels ?? []).includes('MULTI'));

	$effect(() => {
		if (!hasMulti) return;
		syncMultiHang(multiLive);
	});

	const VALUE_COLOR = hudColor('text', 0xf0e6d0);
	const VALUE_TRACKING = 0.3;
	const INK_STROKE = { color: 0x05070a, width: 2 } as const;
	const INK_SHADOW = {
		color: 0x000000,
		blur: 3,
		distance: 1,
		alpha: 0.6,
		angle: Math.PI / 2,
	} as const;

	const hangOf = (p: HudPlaqueGeom) => {
		if (p.label !== 'MULTI') return null;
		const t = multiHang.current;
		if (t <= 0.001 && !multiLive) return { hide: true as const };
		const pose = multiHangPose(t);
		return { hide: false as const, swing: pose.swing, sway: pose.sway };
	};
</script>

{#snippet plaqueFace(p: HudPlaqueGeom, ox: number, oy: number)}
	{#if parts === 'all' || parts === 'plate'}
		<Rectangle
			x={p.well.x + ox}
			y={p.well.y + oy}
			width={p.well.w}
			height={p.well.h}
			backgroundColor={0x000000}
			eventMode="none"
		/>
	{/if}
	{#if parts === 'all' || parts === 'boxes'}
		<Sprite
			key={p.boxKey}
			x={p.box.x + ox}
			y={p.box.y + oy}
			width={p.box.w}
			height={p.box.h}
			eventMode="none"
		/>
		<Sprite
			key={p.palletKey}
			x={p.pallet.x + ox}
			y={p.pallet.y + oy}
			width={p.pallet.w}
			height={p.pallet.h}
			eventMode="none"
		/>
		<Text
			x={p.well.x + ox + p.well.w * 0.5}
			y={p.well.y + oy + p.well.h * 0.5}
			anchor={0.5}
			text={p.value}
			eventMode="none"
			style={trValueStyle({
				fill: VALUE_COLOR,
				fontSize: fitFontSize(p.value, {
					role: 'value',
					base: Math.max(11, Math.floor(p.well.h * 0.42)),
					maxWidth: p.well.w * 0.88,
					min: 9,
					letterSpacing: VALUE_TRACKING,
				}),
				letterSpacing: VALUE_TRACKING,
				stroke: INK_STROKE,
				dropShadow: INK_SHADOW,
			})}
		/>
	{/if}
{/snippet}

<Container>
	{#each props.plaques as p (p.label)}
		{@const hang = hangOf(p)}
		{#if !hang?.hide}
			{#if hang}
				<Container x={hang.sway} y={0} rotation={hang.swing} eventMode="none">
					{#if parts === 'all' || parts === 'chains'}
						{#each p.chains as seg (`${p.label}-${seg.id}`)}
							<Sprite
								key={seg.key}
								x={seg.x}
								y={seg.y}
								width={seg.w}
								height={seg.h}
								eventMode="none"
							/>
						{/each}
					{/if}
					{@render plaqueFace(p, 0, 0)}
				</Container>
			{:else}
				{#if parts === 'all' || parts === 'chains'}
					{#each p.chains as seg (`${p.label}-${seg.id}`)}
						<Sprite
							key={seg.key}
							x={seg.x}
							y={seg.y}
							width={seg.w}
							height={seg.h}
							eventMode="none"
						/>
					{/each}
				{/if}
				{@render plaqueFace(p, 0, 0)}
			{/if}
		{/if}
	{/each}
</Container>
