<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { cellFrames, type Rect } from '../game/chassisArt';
	import {
		BOTTOM_SLOTS,
		RIGHT_SLOTS,
		LEFT_SLOTS,
		BOTTOM_START as bottomStart,
		openGroups,
		unlockedCellKeys,
	} from '../game/cellUnlock';
	import type { SymbolName } from '../game/types';
	import SlotSymbol from './SlotSymbol.svelte';

	// Reserved "special symbol" slots that frame the diamond board: a BOTTOM row
	// (under the middle reels), plus a RIGHT and LEFT column. They read as
	// locked/empty in the base game; during free spins they UNLOCK progressively
	// by bonus level (L1 bottom, L2 +right, L3 +left) and fill with premiums or
	// wilds that drop in (see the unlockedSlots book event). Left/right become
	// extra reel columns and the bottom extends the middle reels (best case =
	// 7-wide board).
	const context = getContext();

	// The nine cells are openings punched through the generated chassis art, so
	// their positions and sizes come from the art itself (chassisArt.ts measures
	// them) rather than from constants tuned by hand here.
	const frames = $derived(cellFrames(context.stateGameDerived.boardLayout()));

	const activeReels = $derived(context.stateGame.wildReelReels ?? []);
	const unlocked = $derived(context.stateGame.unlockedSlots);
	const groups = $derived(openGroups(context.stateGame));
	// Shared with CellChassis, which runs the gears and chains for exactly the
	// cells that open here.
	const openKeys = $derived(unlockedCellKeys(context.stateGame));

	type SlotSym = { name: SymbolName; multiplier?: number };
	type SlotPos = { key: string; frame: Rect; unlocked: boolean; symbol?: SlotSym };

	// bottom premium drops keyed by reel index
	const bottomByReel = $derived.by(() => {
		const map = new Map<number, SlotSym>();
		for (const c of unlocked?.bottom ?? []) map.set(c.reel, { name: c.name });
		return map;
	});
	// side drops keyed by "<side>:<slotRow>"
	const sideByKey = $derived.by(() => {
		const map = new Map<string, SlotSym>();
		for (const s of unlocked?.sides ?? []) {
			for (const c of s.cells) map.set(`${s.side}:${c.slotRow}`, { name: c.name, multiplier: c.multiplier });
		}
		return map;
	});
	// feature symbols (Stretch/Split/Clone) dropped into bottom cells this spin.
	// In the base game this unlocks JUST that cell; in the bonus the cell is
	// already open and the feature card simply drops in.
	const featureByReel = $derived.by(() => {
		const map = new Map<number, SymbolName>();
		for (const c of context.stateGame.featureCells ?? [])
			if (c.reel != null && c.side == null) map.set(c.reel, c.name);
		return map;
	});
	// feature cards that landed in a SIDE column slot (keyed "<side>:<slotRow>").
	const featureBySide = $derived.by(() => {
		const map = new Map<string, SymbolName>();
		for (const c of context.stateGame.featureCells ?? [])
			if (c.side != null && c.slotRow != null) map.set(`${c.side}:${c.slotRow}`, c.name);
		return map;
	});

	// remount key so a freshly dropped slot symbol replays its drop-in each spin.
	const nonce = $derived(context.stateGame.revealNonce);

	// COSMETIC per-spin reel: every spin (base game AND bonus) each still-LOCKED
	// reserved cell reels ONE fresh random symbol in behind its bars and it STAYS
	// (no re-roll, no swap). Every locked cell is guaranteed at least a random
	// premium, and the special symbols (W / STRETCH / SPLIT / CLONE) land on top of
	// that sometimes. Purely visual teasing; a locked cosmetic cell never unlocks
	// or pays. UNLOCKED cells ignore this entirely and reel in the real math
	// content (that's what pays) — so the symbol you see reel in is the final one.
	const PREMIUMS: SymbolName[] = ['H1', 'H2', 'H3', 'H4', 'H5'];
	const SPECIALS: SymbolName[] = ['W', 'STRETCH', 'SPLIT', 'CLONE'];
	const CELL_KEYS = [
		'bottom:0', 'bottom:1', 'bottom:2',
		'right:0', 'right:1', 'right:2',
		'left:0', 'left:1', 'left:2',
	];
	const pickIndex = (weights: number[]): number => {
		let r = Math.random() * weights.reduce((a, b) => a + b, 0);
		for (let i = 0; i < weights.length; i++) {
			r -= weights[i];
			if (r < 0) return i;
		}
		return weights.length - 1;
	};
	const cosmetic = $derived.by(() => {
		void nonce; // re-roll once per reveal (stable for the whole spin)
		const map = new Map<string, SlotSym>();
		for (const key of CELL_KEYS) {
			// guaranteed a symbol: ~18% a special lands, otherwise a random premium.
			const name =
				pickIndex([82, 18]) === 1
					? SPECIALS[pickIndex([60, 16, 14, 10])]
					: PREMIUMS[pickIndex([11, 15, 20, 24, 30])];
			map.set(key, { name });
		}
		return map;
	});

	const slots = $derived.by<SlotPos[]>(() => {
		const out: SlotPos[] = [];
		// bottom row: the beam's three openings extend the middle reels
		for (let i = 0; i < BOTTOM_SLOTS; i++) {
			const reel = bottomStart + i;
			// a Wild Reel is triggered by a WILD dropping INTO this bottom cell; show
			// that wild here (the reel above then turns wild via WildReelSlide).
			const wildInCell = activeReels.includes(reel);
			const feature = featureByReel.get(reel);
			const isUnlocked = openKeys.has(`bottom:${i}`);
			const realSymbol =
				bottomByReel.get(reel) ??
				(wildInCell ? { name: 'W' as SymbolName } : feature ? { name: feature } : undefined);
			out.push({
				key: `bottom:${i}`,
				frame: frames[`bottom:${i}`],
				unlocked: isUnlocked,
				// unlocked cell => real math content (may be empty); locked cell =>
				// cosmetic reel behind the closed bars.
				symbol: realSymbol ?? (isUnlocked ? undefined : cosmetic.get(`bottom:${i}`)),
			});
		}
		// side columns: three openings in each of the two chassis blocks
		for (const side of ['right', 'left'] as const) {
			const count = side === 'right' ? RIGHT_SLOTS : LEFT_SLOTS;
			for (let j = 0; j < count; j++) {
				const key = `${side}:${j}`;
				const feature = featureBySide.get(key);
				out.push({
					key,
					frame: frames[key],
					unlocked: openKeys.has(key),
					symbol:
						(feature ? { name: feature } : undefined) ??
						sideByKey.get(key) ??
						(groups.includes(side) || feature ? undefined : cosmetic.get(key)),
				});
			}
		}
		return out;
	});

	// which slots are part of a winning way this spin (mapped from the board
	// positions the winInfo handler routed to the slots)
	const winKeys = $derived.by(() => {
		const set = new Set<string>();
		const wins = context.stateGame.slotWinPositions ?? [];
		if (!unlocked || wins.length === 0) return set;
		for (const p of wins) {
			for (const c of unlocked.bottom) {
				if (c.reel === p.reel && c.row === p.row) set.add(`bottom:${c.reel - bottomStart}`);
			}
			for (const s of unlocked.sides) {
				for (const c of s.cells) {
					if (s.reel === p.reel && c.row === p.row) set.add(`${s.side}:${c.slotRow}`);
				}
			}
		}
		return set;
	});

	// The openings are not square (the beam's are taller than they are wide), so
	// the symbol is sized to whichever side is tighter and stays inside the iron.
	const symSize = (frame: Rect) => Math.min(frame.w, frame.h) * 0.96;

	// All the special symbols DROP TOGETHER (see SlotSymbol). The border lightning
	// is driven by the feature handlers instead: each feature electrifies ITS cell
	// (cellLightningOn/Off) for as long as its animation runs, in the fixed math
	// order (bottom L->R, right bottom->top, left top->bottom). See CellLightning.
	const DROP_DUR = 300; // ms a single symbol takes to reel in (all together)
</script>

<MainContainer>
	<!-- Each reserved cell is a 2-layer z-stack drawn INTO an opening in the
	     cell-block chassis (CellChassis paints the ironwork behind this):
	       z0  SlotSymbol  the symbol reeling inside the opening
	       z1  bars        closed while locked / swung-open once unlocked
	     The BARS live in their own layer mounted after every cell, NOT as a
	     sibling inside each cell: a Pixi child that gets rebuilt is APPENDED to
	     its parent, so a cell-level bar would fall behind the symbol and the
	     symbol would escape its cage.
	     Base game: every opening shows its symbol behind CLOSED bars. Bonus: the
	     unlocked groups swing OPEN and premiums/wilds drop in (a bottom WILD
	     rises into its reel as a Wild Reel instead). -->
	<Container>
		{#each slots as slot (slot.key)}
			<Container x={slot.frame.cx} y={slot.frame.cy}>
				<!-- Mounted PERMANENTLY (no {#if}/{#key}): SlotSymbol owns the swap,
					so the outgoing symbol reels out on the new spin instead of
					blinking away, and an emptied cell animates out too. Destroying it
					per spin would skip both. -->
				<SlotSymbol
					cx={0}
					cy={0}
					size={symSize(slot.frame)}
					name={slot.symbol?.name}
					multiplier={slot.symbol?.multiplier}
					win={winKeys.has(slot.key)}
					dropDur={DROP_DUR}
					locked={!slot.unlocked}
				/>
			</Container>
		{/each}
	</Container>
	<!-- z1: prison bars, filling each chassis opening, above every symbol -->
	<Container>
		{#each slots as slot (slot.key)}
			<Sprite
				x={slot.frame.cx}
				y={slot.frame.cy}
				anchor={0.5}
				width={slot.frame.w}
				height={slot.frame.h}
				key={slot.unlocked ? 'prisonBarsOpen' : 'prisonBarsClosed'}
			/>
		{/each}
	</Container>
</MainContainer>
