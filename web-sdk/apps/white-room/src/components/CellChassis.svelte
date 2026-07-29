<script lang="ts">
	// CELL-BLOCK CHASSIS — the heavy iron structure the special cells live in:
	// a tall riveted column bolted to each side of the board (the bottom beam
	// wall and the hanging counterweight chains are gone). The gears cut out of
	// the block art still wind hard for one second on each unlock/spin.
	import { Tween } from 'svelte/motion';
	import { cubicInOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { chassisBlocks, chassisCogs } from '../game/chassisArt';
	import { unlockedCellKeys, blockOf } from '../game/cellUnlock';

	const context = getContext();

	const board = $derived(context.stateGameDerived.boardLayout());
	const blocks = $derived(chassisBlocks(board));
	const cogs = $derived(chassisCogs(board));

	// --- mechanism ------------------------------------------------------------
	const WIND_MS = 1000; // one hard gear wind
	/** ~3/4 turn in that one second */
	const WIND_RAD = Math.PI * 1.5;

	/** settled gear angle — only advances, never rewinds */
	let gearAngle = $state(0);
	/** live wind delta applied on top of gearAngle during the 1s turn */
	const spinDrive = new Tween(0, { duration: WIND_MS, easing: cubicInOut });

	let winding = false;

	const wind = async (_sides: { l?: boolean; r?: boolean; beam?: boolean }) => {
		if (winding) return;
		winding = true;
		spinDrive.set(0, { duration: 0 });
		await spinDrive.set(WIND_RAD, { duration: WIND_MS, easing: cubicInOut });
		gearAngle += WIND_RAD;
		spinDrive.set(0, { duration: 0 }); // gears stay put; delta already baked in
		winding = false;
	};

	const gearRot = (i: number) => {
		const ang = gearAngle + spinDrive.current;
		return i % 2 === 0 ? ang : -ang;
	};

	let seen: Set<string> | null = null;
	$effect(() => {
		const open = unlockedCellKeys(context.stateGame);
		const fresh = seen === null ? [] : [...open].filter((key) => !seen!.has(key));
		seen = open;
		if (fresh.length === 0) return;
		const blocksOpened = new Set(fresh.map(blockOf));
		wind({
			l: blocksOpened.has('left') || blocksOpened.has('bottom'),
			r: blocksOpened.has('right') || blocksOpened.has('bottom'),
			beam: blocksOpened.has('bottom'),
		});
	});

	let lastReveal = -1;
	$effect(() => {
		const nonce = context.stateGame.revealNonce ?? 0;
		if (lastReveal < 0) {
			lastReveal = nonce;
			return;
		}
		if (nonce === lastReveal) return;
		lastReveal = nonce;
		wind({ l: true, r: true, beam: true });
	});

	// NO cell number plates anywhere any more. The bottom ones went when their
	// beam wall did; the side ones went when the side cells grew to full board-
	// card size on the board's row pitch — the ~4px left between openings has no
	// room for a stencilled "02", and the cells read as board grid now anyway.
</script>

<MainContainer>
	<!-- hanging counterweight chains REMOVED (and the beam wall + swag before
		them): the swaying strips read as a bad loop, so the side columns are
		clean iron now. -->

	<Container>
		<Sprite
			key="chassisSideL"
			anchor={0}
			x={blocks.sideL.x}
			y={blocks.sideL.y}
			width={blocks.w.side}
			height={blocks.h.side}
		/>
		<Sprite
			key="chassisSideR"
			anchor={0}
			x={blocks.sideR.x}
			y={blocks.sideR.y}
			width={blocks.w.side}
			height={blocks.h.side}
		/>
	</Container>

	<Container>
		{#each cogs as cog, i (cog.key)}
			<Container x={cog.cx} y={cog.cy} rotation={gearRot(i)}>
				<Sprite key="chassisCog" anchor={0.5} width={cog.size} height={cog.size} />
			</Container>
		{/each}
	</Container>
</MainContainer>
