<script lang="ts">
	import type { Snippet } from 'svelte';

	import { getContextEventEmitter } from 'utils-event-emitter';

	import type { EmitterEventModal } from '../types';

	type Props = {
		value: number;
		children: Snippet;
	};

	let { value = $bindable(), children }: Props = $props();
	const { eventEmitter } = getContextEventEmitter<EmitterEventModal>();

	const toggle = () => {
		eventEmitter.broadcast({ type: 'soundPressGeneral' });
		value = value === 0 ? 50 : 0;
	};
</script>

<div class="setting">
	<span class="label">{@render children()}</span>

	<div class="controls">
		<!-- themed on/off switch -->
		<button
			type="button"
			class="switch"
			class:on={value > 0}
			onclick={toggle}
			aria-label="toggle sound"
			aria-pressed={value > 0}
		>
			<span class="state">{value > 0 ? 'ON' : 'OFF'}</span>
			<span class="knob"></span>
		</button>

		<!-- custom gothic slider -->
		<input
			class="range"
			class:muted={value === 0}
			style="--pct: {value}%"
			type="range"
			min="0"
			max="100"
			bind:value
		/>

		<!-- value read-out -->
		<span class="value">{value}</span>
	</div>
</div>

<style lang="scss">
	.setting {
		display: flex;
		flex-direction: column;
		gap: 0.55rem;
	}

	.label {
		font-family: var(--mono-font, 'Segoe UI', Arial, sans-serif);
		font-weight: 700;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		font-size: 0.82rem;
		color: var(--mono-fg-dim, #8b96a3);
	}

	.controls {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 0.9rem;
	}

	/* ---------- on/off switch ---------- */
	.switch {
		position: relative;
		flex: 0 0 auto;
		width: 3.6rem;
		height: 1.7rem;
		border-radius: 999px;
		cursor: pointer;
		padding: 0;
		border: 1px solid var(--mono-edge, #33414f);
		background: var(--mono-surface, #141b23);
		box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.6);
		transition:
			background 0.2s ease,
			border-color 0.2s ease;
	}
	.switch.on {
		border-color: var(--mono-fill, #ffffff);
		background: var(--mono-fill, #ffffff);
		box-shadow: none;
	}

	.knob {
		position: absolute;
		top: 50%;
		left: 0.15rem;
		width: 1.35rem;
		height: 1.35rem;
		border-radius: 50%;
		transform: translateY(-50%);
		background: #c3ccd6;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.6);
		transition:
			left 0.18s ease,
			background 0.18s ease;
	}
	.switch.on .knob {
		left: calc(100% - 1.5rem);
		background: var(--mono-on-fill, #0a0e14);
	}

	.state {
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
		font-size: 0.52rem;
		font-weight: 800;
		letter-spacing: 0.08em;
		color: rgba(255, 255, 255, 0.85);
		pointer-events: none;
	}
	.switch:not(.on) .state {
		right: 0.42rem;
	}
	.switch.on .state {
		left: 0.5rem;
		color: var(--mono-on-fill, #0a0e14);
	}

	/* ---------- slider ---------- */
	.range {
		flex: 1 1 auto;
		-webkit-appearance: none;
		appearance: none;
		height: 0.5rem;
		border-radius: 999px;
		outline: none;
		cursor: pointer;
		border: 1px solid var(--mono-hairline, #2a3542);
		background: linear-gradient(
			90deg,
			var(--mono-fill, #ffffff) 0%,
			var(--mono-fill, #ffffff) var(--pct),
			rgba(255, 255, 255, 0.08) var(--pct),
			rgba(255, 255, 255, 0.08) 100%
		);
		box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.8);
	}
	.range.muted {
		background: rgba(255, 255, 255, 0.08);
		box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.8);
	}

	// webkit thumb – a flat white disc
	.range::-webkit-slider-thumb {
		-webkit-appearance: none;
		width: 1.15rem;
		height: 1.15rem;
		border-radius: 50%;
		background: var(--mono-fill, #ffffff);
		border: 1px solid var(--mono-edge, #33414f);
		box-shadow: 0 2px 3px rgba(0, 0, 0, 0.6);
		cursor: pointer;
	}
	// firefox thumb + progress
	.range::-moz-range-thumb {
		width: 1.15rem;
		height: 1.15rem;
		border-radius: 50%;
		background: var(--mono-fill, #ffffff);
		border: 1px solid var(--mono-edge, #33414f);
		box-shadow: 0 2px 3px rgba(0, 0, 0, 0.6);
		cursor: pointer;
	}
	.range::-moz-range-track {
		height: 0.5rem;
		border-radius: 999px;
		background: rgba(255, 255, 255, 0.08);
	}
	.range::-moz-range-progress {
		height: 0.5rem;
		border-radius: 999px;
		background: var(--mono-fill, #ffffff);
	}

	/* ---------- value ---------- */
	.value {
		flex: 0 0 auto;
		min-width: 2.2rem;
		text-align: right;
		font-family: var(--mono-font, 'Segoe UI', Arial, sans-serif);
		font-weight: 700;
		font-size: 1rem;
		color: var(--mono-fg, #ffffff);
		font-variant-numeric: tabular-nums;
	}
</style>
