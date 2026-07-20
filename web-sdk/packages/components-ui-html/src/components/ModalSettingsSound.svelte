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
	$gold: #c99a3f;
	$gold-lt: #ffe9a8;
	$accent: #ffc12e;

	.setting {
		display: flex;
		flex-direction: column;
		gap: 0.55rem;
	}

	.label {
		font-family: 'Cinzel', Georgia, serif;
		font-weight: 700;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		font-size: 0.82rem;
		color: #e9dcc0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.7);
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
		border: 1px solid rgba(0, 0, 0, 0.6);
		background: linear-gradient(180deg, #2a2a33, #141419);
		box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.7);
		transition: background 0.2s ease;
	}
	.switch.on {
		border-color: rgba(201, 154, 63, 0.9);
		background: linear-gradient(180deg, #7a5a1c, #b8892f);
		box-shadow:
			inset 0 1px 2px rgba(255, 233, 168, 0.4),
			0 0 10px rgba(255, 193, 46, 0.35);
	}

	.knob {
		position: absolute;
		top: 50%;
		left: 0.15rem;
		width: 1.35rem;
		height: 1.35rem;
		border-radius: 50%;
		transform: translateY(-50%);
		background: radial-gradient(circle at 35% 30%, #fdfdfd, #cfcfcf 60%, #8a8a8a);
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.6);
		transition: left 0.18s ease;
	}
	.switch.on .knob {
		left: calc(100% - 1.5rem);
		background: radial-gradient(circle at 35% 30%, #{$gold-lt}, #{$gold} 60%, #6b4e1c);
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
		color: #2a1c05;
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
		border: 1px solid rgba(0, 0, 0, 0.55);
		background: linear-gradient(
			90deg,
			#{$accent} 0%,
			#{$gold-lt} var(--pct),
			rgba(255, 255, 255, 0.08) var(--pct),
			rgba(255, 255, 255, 0.08) 100%
		);
		box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.8);
	}
	.range.muted {
		background: rgba(255, 255, 255, 0.08);
		box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.8);
	}

	// webkit thumb – a gold gem
	.range::-webkit-slider-thumb {
		-webkit-appearance: none;
		width: 1.15rem;
		height: 1.15rem;
		border-radius: 50%;
		background: radial-gradient(circle at 35% 30%, #{$gold-lt}, #{$gold} 58%, #5f4417);
		border: 1px solid #3a2a0e;
		box-shadow:
			0 0 6px rgba(255, 193, 46, 0.7),
			0 2px 3px rgba(0, 0, 0, 0.6);
		cursor: pointer;
	}
	// firefox thumb + progress
	.range::-moz-range-thumb {
		width: 1.15rem;
		height: 1.15rem;
		border-radius: 50%;
		background: radial-gradient(circle at 35% 30%, #{$gold-lt}, #{$gold} 58%, #5f4417);
		border: 1px solid #3a2a0e;
		box-shadow:
			0 0 6px rgba(255, 193, 46, 0.7),
			0 2px 3px rgba(0, 0, 0, 0.6);
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
		background: linear-gradient(90deg, #{$accent}, #{$gold-lt});
	}

	/* ---------- value ---------- */
	.value {
		flex: 0 0 auto;
		min-width: 2.2rem;
		text-align: right;
		font-family: 'Cinzel', Georgia, serif;
		font-weight: 700;
		font-size: 1rem;
		color: #{$accent};
		text-shadow: 0 0 8px rgba(255, 193, 46, 0.35);
	}
</style>
