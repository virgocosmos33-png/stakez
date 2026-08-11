<script lang="ts">
	/**
	 * Bounty payout scatter: aged gold coins and brass rifle cartridges raining
	 * over the board during a win celebration.
	 *
	 * The sheet used to be `coins` → assets/sprites/coin/SD2_Coin.json, the
	 * Samurai Dogs 2 template coin atlas. That was the generic gold-coin confetti;
	 * it is replaced by `winScatter`, cut from Layer AI coin/cartridge art by
	 * tools/make_win_celebration_art.py.
	 */
	import { Container, ParticleEmitter } from 'pixi-svelte';
	import { MainContainer } from 'components-layout';
	import { LEVEL_PARTICLE_COIN_MAP } from 'constants-shared/particleCoin';

	import { getContext } from '../game/context';
	import type { WinLevelAlias } from '../game/winLevelMap';
	import { TOMBSTONE_COIN_FALL } from '../game/tombstoneVfx';
	import { WIN_SCATTER_ASSET } from '../game/winCelebrationArt';

	type Props = {
		emit?: boolean;
		levelAlias?: WinLevelAlias;
	};

	const props: Props = $props();
	const context = getContext();

	// Bigger tiers throw more metal. Falls back to the base rate for the small
	// tiers, which do not carry a coin fall at all in LEVEL_PARTICLE_COIN_MAP.
	const TIER_FREQUENCY: Partial<Record<WinLevelAlias, number>> = {
		big: 0.085,
		superwin: 0.07,
		mega: 0.055,
		epic: 0.04,
		max: 0.026,
	};

	const extraConfig = $derived(
		props?.levelAlias ? LEVEL_PARTICLE_COIN_MAP[props.levelAlias] : null,
	);
	const config = $derived({
		...TOMBSTONE_COIN_FALL,
		...(extraConfig ?? {}),
		// force ceiling spawn even when level map overrides fountain rect
		spawnType: 'rect',
		spawnRect: { x: -280, y: -220, w: 560, h: 40 },
		acceleration: { x: 0, y: 980 },
		startRotation: { min: 70, max: 110 },
		rotationSpeed: { min: -220, max: 220 },
		// The scatter art is already aged gold and brass, so it only gets a warm
		// key and then sinks into shadow — the old config tinted flat template
		// coins gold, which now double-tints real metal.
		color: { start: '#fff0d4', end: '#4a3e32' },
		scale: { start: 0.26, end: 0.42, minimumScaleMultiplier: 0.68 },
		frequency: (props.levelAlias && TIER_FREQUENCY[props.levelAlias]) ?? TOMBSTONE_COIN_FALL.frequency,
		maxParticles: 180,
	});
</script>

{#if config}
	<MainContainer>
		<Container
			x={context.stateGameDerived.boardLayout().x}
			y={context.stateGameDerived.boardLayout().y}
		>
			<ParticleEmitter {config} key={WIN_SCATTER_ASSET} emit={props.emit} />
		</Container>
	</MainContainer>
{/if}
