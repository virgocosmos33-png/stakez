<script lang="ts">
	// CELL-BLOCK CHASSIS — the heavy iron structure the nine special cells live
	// in: a tall riveted column bolted to each side of the board and a shallow
	// beam slung underneath it, with padlocks and rivets baked into the art.
	//
	// The nine cells are literally holes punched through these three blocks, so
	// this component draws no cells itself. It paints the ironwork and stencils
	// the cell numbers onto the blank plates; LockedSlots fills the openings.
	//
	// The MOVING parts — the gears, the hanging counterweights and the chain
	// swags — were cut out of the block art by make_chassis_assets.py precisely so
	// they can be driven from here: when a cell opens the gears wind and the
	// chains take up the slack, as if the mechanism hauled the bars up. Each block
	// keeps a machined socket where its gear was, so a gear turns against a recess
	// instead of dragging its own baked shadow around with it.
	//
	// Mounted BEFORE LockedSlots so the symbols reel in through the openings and
	// the ironwork stays behind them.
	import { Tween } from 'svelte/motion';
	import { cubicOut, backOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import {
		chassisBlocks,
		cellFrames,
		chassisCogs,
		chassisChains,
		chassisSwag,
		platePoint,
		CELL_NUMBERS,
	} from '../game/chassisArt';
	import { SYMBOL_SIZE } from '../game/constants';
	import { unlockedCellKeys, blockOf } from '../game/cellUnlock';

	const context = getContext();

	const board = $derived(context.stateGameDerived.boardLayout());
	const blocks = $derived(chassisBlocks(board));
	const frames = $derived(cellFrames(board));
	const cogs = $derived(chassisCogs(board));
	const chains = $derived(chassisChains(board));
	const swag = $derived(chassisSwag(board));

	// --- mechanism ------------------------------------------------------------
	// One wind of the gears per opening, accumulated rather than reset, so cells
	// opening back to back keep the gears turning forward instead of snapping.
	const WIND = Math.PI * 0.55;
	const WIND_MS = 820;
	// The counterweights drop and settle. Kept to a jolt rather than a real fall:
	// the chain sprite is exactly as long as the column, so a big move would open
	// a gap at the end it travels away from.
	const CHAIN_TRAVEL = 0.012; // of the column height
	// The swags are free to move much further because they travel UP, behind the
	// beam that hides their anchors — the chain simply pulls taut.
	const SWAG_TRAVEL = -0.5; // of the swag's own height

	const spin = new Tween(0, { duration: WIND_MS, easing: cubicOut });
	const chainPull = { l: new Tween(0), r: new Tween(0) };
	const swagPull = new Tween(0);

	const haul = async (t: Tween<number>, amount: number) => {
		await t.set(amount, { duration: 190, easing: cubicOut });
		t.set(0, { duration: 760, easing: backOut });
	};

	// Watch the cells rather than any one book event: every route to an open cell
	// (a whole group unlocking, a wild rising out of a bottom cell, a lone feature
	// card unlocking its own cell in the base game) lands here.
	let seen: Set<string> | null = null;
	$effect(() => {
		const open = unlockedCellKeys(context.stateGame);
		// First pass only records the state: resuming a bonus mid-flight arrives
		// with cells already open, and that is not something opening.
		const fresh = seen === null ? [] : [...open].filter((key) => !seen!.has(key));
		seen = open;
		if (fresh.length === 0) return;

		// The gears drive the whole rig, so any opening winds all of them; only the
		// chains belonging to the blocks that actually opened take up slack.
		spin.set(spin.target + WIND);
		const blocksOpened = new Set(fresh.map(blockOf));
		if (blocksOpened.has('left')) haul(chainPull.l, CHAIN_TRAVEL);
		if (blocksOpened.has('right')) haul(chainPull.r, CHAIN_TRAVEL);
		if (blocksOpened.has('bottom')) haul(swagPull, SWAG_TRAVEL);
	});

	// Numbers are runtime text, not baked art: the right-hand column is the left
	// column's art mirrored, so anything stencilled into the plate would read
	// backwards on that side.
	const plates = $derived(
		Object.entries(frames).map(([key, frame]) => ({
			key,
			label: CELL_NUMBERS[key],
			...platePoint(frame, !key.startsWith('bottom')),
			size: (key.startsWith('bottom') ? frame.h : frame.h) * 0.19,
		})),
	);
</script>

<MainContainer>
	<!-- Behind the ironwork: the hanging chains and the beam's swags, so the ends
		they travel on stay tucked under the blocks that anchor them. -->
	<Container>
		{#each chains as chain (chain.key)}
			<Sprite
				key={chain.assetKey}
				anchor={0}
				x={chain.x}
				y={chain.y + chainPull[chain.key as 'l' | 'r'].current * chain.h}
				width={chain.w}
				height={chain.h}
			/>
		{/each}
		<Sprite
			key="chassisSwag"
			anchor={0}
			x={swag.x}
			y={swag.y + swagPull.current * swag.h}
			width={swag.w}
			height={swag.h}
		/>
	</Container>

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
		<Sprite
			key="chassisBeam"
			anchor={0}
			x={blocks.beam.x}
			y={blocks.beam.y}
			width={blocks.w.beam}
			height={blocks.h.beam}
		/>
	</Container>

	<!-- Gears, turning in the sockets left behind in the block art. Adjacent
		gears wind opposite ways, the way a meshed pair would. -->
	<Container>
		{#each cogs as cog, i (cog.key)}
			<Container x={cog.cx} y={cog.cy} rotation={i % 2 === 0 ? spin.current : -spin.current}>
				<Sprite key="chassisCog" anchor={0.5} width={cog.size} height={cog.size} />
			</Container>
		{/each}
	</Container>

	<!-- stencilled cell numbers on the blank riveted plates -->
	<Container>
		{#each plates as plate (plate.key)}
			<Text
				anchor={0.5}
				x={plate.x}
				y={plate.y}
				text={plate.label}
				style={{
					fontFamily: 'Arial',
					fontWeight: '900',
					fontSize: plate.size,
					fill: 0xd8dce0,
					letterSpacing: SYMBOL_SIZE * 0.012,
				}}
			/>
		{/each}
	</Container>
</MainContainer>
