<script lang="ts">
	import type { Snippet } from 'svelte';

	import { OnHotkey, Popup } from 'components-shared';
	import { zIndex } from 'constants-shared/zIndex';
	import { stateModal, stateSound, stateUrlDerived } from 'state-shared';
	import { socialText } from 'utils-shared/socialText';

	import ModalSettingsSound from './ModalSettingsSound.svelte';
	import { i18nDerived } from '../i18n/i18nDerived';
	// single source of truth for the special-symbol + rules copy (shared with the
	// in-HUD info marquee so both always show identical text)
	import { SPECIALS, INFO_SECTIONS } from '../data/gameInfo';

	type Props = {
		children: Snippet;
	};

	const props: Props = $props();

	type Tab = 'info' | 'settings';
	let tab = $state<Tab>('info');

	// per-way pays (x bet) for 5 / 4 / 3 of a kind — mirrors game_config paytable
	const HIGH_SYMBOLS = [
		{ key: 'h1', name: 'Lady Mirror', pays: [10, 3, 1] },
		{ key: 'h2', name: 'The Wife', pays: [5, 1.5, 0.6] },
		{ key: 'h3', name: 'The Man', pays: [4, 1.2, 0.5] },
		{ key: 'h4', name: 'The Maiden', pays: [3, 1, 0.4] },
		{ key: 'h5', name: 'The Dog', pays: [2.5, 0.8, 0.3] },
	];

	const LOW_SYMBOLS = [
		{ key: 'l1', name: 'Ace', pays: [1.2, 0.4, 0.2] },
		{ key: 'l2', name: 'King', pays: [1.2, 0.4, 0.2] },
		{ key: 'l3', name: 'Queen', pays: [0.8, 0.3, 0.1] },
		{ key: 'l4', name: 'Jack', pays: [0.8, 0.3, 0.1] },
		{ key: 'l5', name: 'Ten', pays: [0.8, 0.3, 0.1] },
	];

	const close = () => {
		tab = 'info';
		stateModal.modal = null;
	};

	const formatPay = (n: number) => (Number.isInteger(n) ? String(n) : n.toFixed(2).replace(/0$/, ''));

	// stake.us jurisdiction language: rewrite prohibited gambling terms
	const st = (text: string) => socialText(text, stateUrlDerived.social());
</script>

{#if stateModal.modal?.name === 'payTable'}
	<OnHotkey hotkey="Escape" onpress={close} />
	<Popup zIndex={zIndex.modal} persistent onclose={close}>
		<div class="shell" role="dialog" aria-label="Game menu">
			<aside class="rail">
				<button
					class="rail-btn"
					class:active={tab === 'info'}
					aria-label="Pay table and game rules"
					onclick={() => (tab = 'info')}
				>
					<svg viewBox="0 0 24 24" aria-hidden="true">
						<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8" />
						<path
							d="M12 10.5v6M12 7.5h.01"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
						/>
					</svg>
				</button>

				<button
					class="rail-btn"
					class:active={tab === 'settings'}
					aria-label="Sound settings"
					onclick={() => (tab = 'settings')}
				>
					<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8">
						<path stroke-linejoin="round" stroke-linecap="round" d="M4 9.5v5h3l4.5 3.5V6L7 9.5H4Z" />
						<path stroke-linecap="round" d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11" />
					</svg>
				</button>

				<button class="rail-btn close" aria-label="Close menu" onclick={close}>
					<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2">
						<path stroke-linecap="round" d="M7 7l10 10M17 7 7 17" />
					</svg>
				</button>
			</aside>

			<main class="panel">
				{#if tab === 'info'}
					<header class="head">
						<h1>{stateUrlDerived.social() ? 'Game info' : 'Pay table'}</h1>
					</header>

					<div class="scroll">
						<section class="block">
							<h2>PAYOUT</h2>
							<div class="pay-row">
								{#each HIGH_SYMBOLS as s (s.key)}
									<div class="pay-cell">
										<img src="assets/paytable/{s.key}.png" alt={s.name} />
										<div class="pay-list">
											<span><em>5</em> {formatPay(s.pays[0])}</span>
											<span><em>4</em> {formatPay(s.pays[1])}</span>
											<span><em>3</em> {formatPay(s.pays[2])}</span>
										</div>
									</div>
								{/each}
							</div>
							<div class="pay-row lows">
								{#each LOW_SYMBOLS as s (s.key)}
									<div class="pay-cell">
										<img src="assets/paytable/{s.key}.png" alt={s.name} />
										<div class="pay-list">
											<span><em>5</em> {formatPay(s.pays[0])}</span>
											<span><em>4</em> {formatPay(s.pays[1])}</span>
											<span><em>3</em> {formatPay(s.pays[2])}</span>
										</div>
									</div>
								{/each}
							</div>
							<p class="foot">{st('All wins are shown as a multiplier of the total bet, paid per way.')}</p>
						</section>

						<section class="block">
							<h2>SPECIAL SYMBOLS</h2>
							<div class="specials">
								{#each SPECIALS as s (s.key)}
									<div class="special">
										<img src="assets/paytable/{s.key}.png" alt={s.name} />
										<div>
											<strong>{s.name}</strong>
											<p>{st(s.desc)}</p>
										</div>
									</div>
								{/each}
							</div>
						</section>

						{#each INFO_SECTIONS as r (r.title)}
							<section class="block rule">
								<h2>{st(r.title)}</h2>
								{#if r.body}
									<p>{st(r.body)}</p>
								{/if}
								{#if r.bullets?.length}
									<ul>
										{#each r.bullets as bullet}
											<li>{st(bullet)}</li>
										{/each}
									</ul>
								{/if}
								{#if r.rows?.length}
									<div class="info-rows">
										{#each r.rows as row}
											<div class="info-row">
												<span>{st(row.label)}</span>
												<strong>{st(row.value)}</strong>
											</div>
										{/each}
									</div>
								{/if}
							</section>
						{/each}

						<div class="version">{@render props.children()}</div>
					</div>
				{:else}
					<header class="head">
						<h1>Settings</h1>
					</header>
					<div class="scroll settings">
						<ModalSettingsSound bind:value={stateSound.volumeValueMusic}>
							{i18nDerived.musicVolume()}
						</ModalSettingsSound>
						<ModalSettingsSound bind:value={stateSound.volumeValueSoundEffect}>
							{i18nDerived.soundEffectVolume()}
						</ModalSettingsSound>
						<ModalSettingsSound bind:value={stateSound.volumeValueMaster}>
							{i18nDerived.masterVolume()}
						</ModalSettingsSound>
					</div>
				{/if}
			</main>
		</div>
	</Popup>
{/if}

<style lang="scss">
	.shell {
		position: relative;
		z-index: 100;
		width: 100%;
		height: 100%;
		max-height: 100%;
		display: grid;
		grid-template-columns: minmax(0, 1fr) 4.5rem;
		color: #f4f4f6;
		pointer-events: auto;
		overflow: hidden;
		box-sizing: border-box;
	}

	.rail {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 1.1rem;
		padding: 1.25rem 0.75rem;
		order: 2;
		z-index: 5;
		pointer-events: auto;
	}

	.rail-btn {
		width: 3.4rem;
		height: 3.4rem;
		flex: 0 0 auto;
		border-radius: 999px;
		border: 2.5px solid #ffffff;
		background: rgba(0, 0, 0, 0.35);
		color: #fff;
		display: grid;
		place-items: center;
		cursor: pointer;
		padding: 0;
		transition:
			background 0.15s ease,
			border-color 0.15s ease,
			color 0.15s ease,
			transform 0.12s ease;

		svg {
			width: 1.55rem;
			height: 1.55rem;
			display: block;
		}

		&:hover {
			transform: scale(1.05);
			background: rgba(255, 255, 255, 0.08);
		}

		&.active {
			border-color: var(--mono-fill, #ffffff);
			background: var(--mono-fill, #ffffff);
			color: var(--mono-on-fill, #0a0e14);
		}

		&.close {
			margin-top: 0.4rem;
		}
	}

	.panel {
		order: 1;
		min-width: 0;
		min-height: 0;
		height: 100%;
		max-height: 100%;
		display: flex;
		flex-direction: column;
		padding: 1.5rem 1rem 1.5rem 2.5rem;
		box-sizing: border-box;
		overflow: hidden;
	}

	.head {
		flex: 0 0 auto;
		padding-bottom: 0.85rem;
		margin-bottom: 0.5rem;
		border-bottom: 1px solid rgba(255, 255, 255, 0.22);

		h1 {
			margin: 0;
			font-size: clamp(1.6rem, 3vw, 2.2rem);
			font-weight: 700;
			font-style: italic;
			letter-spacing: 0.01em;
		}
	}

	.scroll {
		flex: 1 1 0;
		min-height: 0;
		overflow-y: scroll;
		overflow-x: hidden;
		padding-right: 1rem;
		-webkit-overflow-scrolling: touch;
		overscroll-behavior: contain;
		scrollbar-width: thin;
		scrollbar-color: rgba(255, 255, 255, 0.45) transparent;
		touch-action: pan-y;

		&::-webkit-scrollbar {
			width: 6px;
		}

		&::-webkit-scrollbar-thumb {
			background: rgba(255, 255, 255, 0.45);
			border-radius: 999px;
		}
	}

	.block {
		margin-bottom: 2rem;

		h2 {
			margin: 0 0 1rem;
			font-size: clamp(1.1rem, 2vw, 1.45rem);
			font-weight: 800;
			letter-spacing: 0.06em;
			text-transform: uppercase;
		}

		&.rule {
			p {
				margin: 0 0 0.75rem;
				max-width: 52rem;
				line-height: 1.55;
				color: rgba(244, 244, 246, 0.9);
				font-size: 1.02rem;
			}

			ul {
				margin: 0;
				padding: 0 0 0 1.2rem;
				max-width: 52rem;
				display: flex;
				flex-direction: column;
				gap: 0.45rem;
			}

			li {
				line-height: 1.5;
				color: rgba(244, 244, 246, 0.9);
				font-size: 1.02rem;
			}
		}
	}

	.info-rows {
		display: flex;
		flex-direction: column;
		gap: 0.45rem;
		max-width: 40rem;
		margin-top: 0.35rem;
	}

	.info-row {
		display: flex;
		justify-content: space-between;
		gap: 1.5rem;
		padding: 0.45rem 0.7rem;
		background: rgba(0, 0, 0, 0.28);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 0.4rem;
		font-size: 0.98rem;

		span {
			color: rgba(244, 244, 246, 0.85);
		}

		strong {
			color: var(--mono-fg, #ffffff);
			font-variant-numeric: tabular-nums;
			white-space: nowrap;
		}
	}

	.pay-row {
		display: grid;
		grid-template-columns: repeat(5, minmax(0, 1fr));
		gap: 0.75rem 1rem;
		margin-bottom: 1.25rem;

		&.lows {
			margin-bottom: 0.5rem;
		}

		@media (max-width: 900px) {
			grid-template-columns: repeat(3, minmax(0, 1fr));
		}

		@media (max-width: 560px) {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}
	}

	.pay-cell {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.45rem;
		text-align: center;

		img {
			width: clamp(3.6rem, 8vw, 5.5rem);
			height: clamp(3.6rem, 8vw, 5.5rem);
			object-fit: contain;
			filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.45));
		}
	}

	.pay-list {
		display: flex;
		flex-direction: column;
		gap: 0.12rem;
		font-variant-numeric: tabular-nums;
		font-size: 0.92rem;
		color: #fff;

		em {
			display: inline-block;
			min-width: 0.9rem;
			margin-right: 0.35rem;
			font-style: normal;
			color: rgba(255, 255, 255, 0.55);
			font-weight: 600;
		}
	}

	.foot {
		margin: 0.75rem 0 0;
		color: rgba(255, 255, 255, 0.45);
		font-size: 0.85rem;
	}

	.specials {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 0.85rem 1.5rem;

		@media (max-width: 720px) {
			grid-template-columns: 1fr;
		}
	}

	.special {
		display: flex;
		align-items: center;
		gap: 0.85rem;
		text-align: left;

		img {
			width: 4.2rem;
			height: 4.2rem;
			object-fit: contain;
			flex-shrink: 0;
		}

		strong {
			display: block;
			margin-bottom: 0.2rem;
			font-size: 1.05rem;
		}

		p {
			margin: 0;
			color: rgba(244, 244, 246, 0.78);
			line-height: 1.4;
			font-size: 0.95rem;
		}
	}

	.settings {
		display: flex;
		flex-direction: column;
		gap: 1.4rem;
		max-width: 36rem;
		padding-top: 1rem;
	}

	.version {
		margin: 2rem 0 1rem;
		opacity: 0.45;
		font-size: 0.85rem;
	}

	@media (max-width: 640px) {
		.panel {
			padding: 1rem 0.5rem 1rem 1rem;
		}

		.rail {
			padding: 0.75rem 0.65rem;
			gap: 0.85rem;
		}

		.rail-btn {
			width: 2.7rem;
			height: 2.7rem;
		}
	}
</style>
