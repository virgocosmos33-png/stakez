<script lang="ts">
	import { Container, ParticleEmitter } from 'pixi-svelte';
	import { MainContainer } from 'components-layout';
	import { LEVEL_PARTICLE_COIN_MAP } from 'constants-shared/particleCoin';

	import { getContext } from '../game/context';
	import type { WinLevelAlias } from '../game/winLevelMap';
	import { TOMBSTONE_COIN_FALL } from '../game/tombstoneVfx';

	type Props = {
		emit?: boolean;
		levelAlias?: WinLevelAlias;
	};

	const props: Props = $props();
	const context = getContext();

	// Tombstone: brass / dust falls from the ceiling (not White Room ceramic).
	// Sheet key stays "coins" for asset wiring.
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
