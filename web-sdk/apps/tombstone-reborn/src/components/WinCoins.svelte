<script lang="ts">
	import { Container, ParticleEmitter } from 'pixi-svelte';
	import { MainContainer } from 'components-layout';
	import { LEVEL_PARTICLE_COIN_MAP } from 'constants-shared/particleCoin';

	import { getContext } from '../game/context';
	import type { WinLevelAlias } from '../game/winLevelMap';

	type Props = {
		emit?: boolean;
		levelAlias?: WinLevelAlias;
	};

	const props: Props = $props();
	const context = getContext();

	// THE WHITE ROOM: ceramic ID tags / restraint buckles FALL from ceiling
	// (ceiling dust), not coin fountain upward. Sheet key stays "coins" for
	// asset wiring; art is patient-ID flipbook from make_gem_flipbook.py.
	const WHITE_ROOM_FALL = {
		alpha: { start: 0.95, end: 0.15 },
		scale: { start: 0.22, end: 0.38, minimumScaleMultiplier: 0.7 },
		color: { start: '#f4f1ec', end: '#8a8680' },
		speed: { start: 180, end: 420, minimumSpeedMultiplier: 0.6 },
		acceleration: { x: 0, y: 980 },
		maxSpeed: 0,
		startRotation: { min: 70, max: 110 },
		noRotation: false,
		rotationSpeed: { min: -220, max: 220 },
		lifetime: { min: 2.2, max: 3.4 },
		blendMode: 'normal',
		frequency: 0.08,
		emitterLifetime: -1,
		maxParticles: 140,
		pos: { x: 0, y: 0 },
		addAtBack: false,
		spawnType: 'rect',
		spawnRect: { x: -280, y: -220, w: 560, h: 40 },
	} as const;

	const extraConfig = $derived(
		props?.levelAlias ? LEVEL_PARTICLE_COIN_MAP[props.levelAlias] : null,
	);
	const config = $derived({
		...WHITE_ROOM_FALL,
		...(extraConfig ?? {}),
		// force ceiling spawn even when level map overrides fountain rect
		spawnType: 'rect',
		spawnRect: { x: -280, y: -220, w: 560, h: 40 },
		acceleration: { x: 0, y: 980 },
		startRotation: { min: 70, max: 110 },
		rotationSpeed: { min: -220, max: 220 },
	});
</script>

{#if config}
	<MainContainer>
		<Container
			x={context.stateGameDerived.boardLayout().x}
			y={context.stateGameDerived.boardLayout().y}
		>
			<ParticleEmitter {config} key="coins" emit={props.emit} />
		</Container>
	</MainContainer>
{/if}
