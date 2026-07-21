<script lang="ts">
	import { OptionsGrid } from 'components-shared';
	import { stateBet, stateConfig } from 'state-shared';

	import BaseIcon from './BaseIcon.svelte';
	import BaseButtonContent from './BaseButtonContent.svelte';
	import { i18nDerived } from '../i18n/i18nDerived';

	// show every configured bet level (deduped) — the grid scrolls instead of
	// truncating to a fixed count
	const options = $derived(
		stateConfig.betMenuOptions.filter(
			(value, index, array) => array.indexOf(value) === index,
		),
	);

	const isMaxValue = (value: number) => value === options[options.length - 1];
	const formatValue = (value: number) => {
		if (Math.abs(value) > 999999) {
			return `${(Math.abs(value) / 1000000).toFixed(2)}M`;
		}
		if (Math.abs(value) > 999) {
			return `${(Math.abs(value) / 1000).toFixed(2)}K`;
		}
		return Math.abs(value).toFixed(2);
	};
</script>

<div class="grid-scroll">
	<OptionsGrid value={stateBet.betAmount} {options} onchange={(value) => (stateBet.betAmount = value)}>
		{#snippet option({ option })}
			<BaseIcon width="100%" height="2rem" selected={option === stateBet.betAmount} />
			<BaseButtonContent>
				<span class="opt-label" class:selected={option === stateBet.betAmount}>
					{isMaxValue(option) ? i18nDerived.max() : formatValue(option)}
				</span>
			</BaseButtonContent>
		{/snippet}
	</OptionsGrid>
</div>

<style lang="scss">
	.grid-scroll {
		width: 100%;
		max-height: 42vh;
		overflow-y: auto;
		overflow-x: hidden;
		padding: 0.35rem 0.6rem;

		// themed scrollbar
		scrollbar-width: thin;
		scrollbar-color: var(--mono-edge, #33414f) rgba(255, 255, 255, 0.06);

		&::-webkit-scrollbar {
			width: 8px;
		}
		&::-webkit-scrollbar-track {
			background: rgba(255, 255, 255, 0.05);
			border-radius: 999px;
		}
		&::-webkit-scrollbar-thumb {
			background: var(--mono-edge, #33414f);
			border-radius: 999px;
			border: 1px solid rgba(0, 0, 0, 0.4);
		}
		&::-webkit-scrollbar-thumb:hover {
			background: var(--mono-edge-hover, #3d4f63);
		}
	}

	.opt-label {
		font-family: var(--mono-font, 'Segoe UI', Arial, sans-serif);
		font-weight: 600;
		font-size: 0.85rem;
		color: var(--mono-fg, #ffffff);
		font-variant-numeric: tabular-nums;

		// on the selected (inverted white) chip the glyphs flip to dark ink
		&.selected {
			color: var(--mono-on-fill, #0a0e14);
		}
	}
</style>
