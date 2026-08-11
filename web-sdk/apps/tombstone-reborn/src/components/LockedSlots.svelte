<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backIn } from 'svelte/easing';
	import type { Graphics as PixiGraphics } from 'pixi.js';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Rectangle } from 'pixi-svelte';

	import { stateBet } from 'state-shared';
	import { waitForTimeout } from 'utils-shared/wait';

	import { getContext } from '../game/context';
	import { cellFrames, type Rect } from '../game/chassisArt';
	import { GRAVEYARD_PALETTE } from '../game/graveyardFx';
	import {
		BOTTOM_SLOTS,
		RIGHT_SLOTS,
		LEFT_SLOTS,
		BOTTOM_START as bottomStart,
		openGroups,
		unlockedCellKeys,
	} from '../game/cellUnlock';
	import type { SymbolName } from '../game/types';
	import {
		SYMBOL_SIZE,
		NUM_ROWS,
		SPIN_OPTIONS_DEFAULT,
		SPIN_OPTIONS_FAST,
	} from '../game/constants';
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

	// reels whose OWN bottom cell holds the wild card. Deliberately NOT
	// wildReelReels: a cage wild grows a column on a main reel from across the
	// board, and that reel's bottom cell must stay shut and empty.
	const activeReels = $derived(context.stateGame.wildCardReels ?? []);
	const unlocked = $derived(context.stateGame.unlockedSlots);
	const groups = $derived(openGroups(context.stateGame));
	// Shared with CellChassis, which runs the gears and chains for exactly the
	// cells that open here.
	const openKeys = $derived(unlockedCellKeys(context.stateGame));

	type SlotSym = { name: SymbolName; multiplier?: number; expanding?: boolean };
	type SlotPos = { key: string; frame: Rect; unlocked: boolean; symbol?: SlotSym };

	// bottom premium drops keyed by reel index
	const bottomByReel = $derived.by(() => {
		const map = new Map<number, SlotSym>();
		// a W here is a PLAIN paying multiplier wild sitting in the cell itself
		// (same as the side cage wilds) — the EXPANDING card never rides
		// unlockedSlots, it arrives via the wildReel event (wildCardReels)
		for (const c of unlocked?.bottom ?? [])
			map.set(c.reel, { name: c.name, multiplier: c.multiplier });
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
	// A W here is the EXPANDING wild — it reaches out and turns a main reel into
	// a column rather than paying in place, so it wears the arrow card, same as
	// a bottom-cell wild does.
	const featureBySide = $derived.by(() => {
		const map = new Map<string, SlotSym>();
		for (const c of context.stateGame.featureCells ?? [])
			if (c.side != null && c.slotRow != null)
				map.set(`${c.side}:${c.slotRow}`, { name: c.name, expanding: c.name === 'W' });
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
				(wildInCell
					? { name: 'W' as SymbolName, expanding: true }
					: feature
						? { name: feature }
						: undefined);
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
						feature ??
						sideByKey.get(key) ??
						(groups.includes(side) ? undefined : cosmetic.get(key)),
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

	// EVERY cell shows its symbol at EXACTLY board scale (size = SYMBOL_SIZE,
	// scale 1) with the overflow cropped by the cell's opening — identical to a
	// board symbol with its edges cut off, NEVER a shrunken one. Side openings
	// used to fit the symbol to the tighter side (~half board scale), which read
	// as a broken mini-symbol next to the full-size board cards.
	const CELL_CLIP_RADIUS = 7;

	// EVERY cell's socket, recessed straight into whatever sits behind it — the
	// BoardPlate for the bottom cells, the iron column for the side cells. Same
	// inset/radius as the board's cells. The side cells NEED this: they are now
	// full board-card size, bigger than the openings baked into the chassis art,
	// so the socket is what actually punches the larger hole through the iron
	// (it fully covers the old baked opening and its bezel).
	const drawSockets = (g: import('pixi.js').Graphics, all: SlotPos[]) => {
		for (const slot of all) {
			const f = slot.frame;
			g.roundRect(f.cx - f.w / 2, f.cy - f.h / 2, f.w, f.h, CELL_CLIP_RADIUS);
			g.fill({ color: 0x0c0d0f, alpha: 0.9 });
			g.roundRect(f.cx - f.w / 2, f.cy - f.h / 2, f.w, f.h, CELL_CLIP_RADIUS);
			g.stroke({ color: 0x000000, width: 3, alpha: 0.5 });
		}
	};

	// --- column timing ---------------------------------------------------------
	// The special cells reel in and out as COLUMNS OF THE BOARD, not as one
	// synchronised frame: the left cage is the first column to move, the bottom
	// cells belong to their own middle reels, and the right cage is the last
	// column. The main reels' pre-spin stagger was shifted to slots 1..5
	// (stateGame reelIndex+1) so the left cage owns slot 0.
	//
	// Fall-OUT is a fixed delay per column (the board's own reelFallOutDelay per
	// slot; zero on turbo, where the board skips its stagger too). Fall-IN can't
	// be a fixed delay — anticipation and slams reshape the reveal — so each
	// cell GATES on its own column's live reel motion instead (see SlotSymbol).
	const spinOpts = () => (stateBet.isTurbo ? SPIN_OPTIONS_FAST : SPIN_OPTIONS_DEFAULT);

	/** which fall-out stagger slot a cell's column occupies (left 0, reels 1..5, right 6) */
	const staggerSlotOf = (key: string): number => {
		const [block, row] = key.split(':');
		if (block === 'left') return 0;
		if (block === 'right') return context.stateGame.board.length + 1;
		return bottomStart + Number(row) + 1;
	};

	const fallOutDelays = new Map(
		CELL_KEYS.map((key) => [
			key,
			() => (stateBet.isTurbo ? 0 : staggerSlotOf(key) * spinOpts().reelFallOutDelay),
		] as const),
	);

	/** poll a reel's live motion (slam-safe: 'stopped' always satisfies) */
	const waitForReel = async (reel: number, ready: (motion: string) => boolean) => {
		const deadline = Date.now() + 15_000;
		while (
			!ready(context.stateGame.board[reel].reelState.motion) &&
			Date.now() < deadline
		) {
			await waitForTimeout(16);
		}
	};

	const makeFallInGate = (key: string) => {
		const [block, rowStr] = key.split(':');
		const row = Number(rowStr);
		return async () => {
			const lastReel = context.stateGame.board.length - 1;
			if (block === 'left') {
				// the left column LEADS: it may drop as soon as reel 0 has finished
				// falling out — reel 0's own fall-in then starts a beat later, so
				// the cage lands first. Bottom cell of the stack lands first, like
				// the bottom row of a reel.
				await waitForReel(0, (m) => m !== 'fallingOut');
				await waitForTimeout(spinOpts().symbolFallInInterval * (LEFT_SLOTS - row));
			} else if (block === 'right') {
				// the right column TRAILS the last reel: wait for its fall-in, then
				// one more beat than its rows need, so the cage is the last landing
				await waitForReel(lastReel, (m) => m === 'fallingIn' || m === 'stopped');
				await waitForTimeout(
					spinOpts().symbolFallInInterval *
						((NUM_ROWS[lastReel] ?? 0) + 2 + (RIGHT_SLOTS - row)),
				);
			} else {
				// a bottom cell is its reel's own extra bottom row: it starts the
				// moment the reel starts falling in, and being the lowest cell it
				// lands first — exactly like the reel's bottom symbol does
				await waitForReel(bottomStart + row, (m) => m === 'fallingIn' || m === 'stopped');
			}
		};
	};
	const fallInGates = new Map(CELL_KEYS.map((key) => [key, makeFallInGate(key)] as const));

	// The border lightning is driven by the feature handlers instead: each
	// feature electrifies ITS cell (cellLightningOn/Off) for as long as its
	// animation runs, in the fixed math order (bottom L->R, right bottom->top,
	// left top->bottom). See CellLightning.

	// --- prison bars -----------------------------------------------------------
	// VERTICAL steel bars drawn procedurally over each opening, replacing the old
	// cage/door PNGs. The bar count is solved from the frame width against a fixed
	// pitch, so thickness and spacing are identical on every cell — the short
	// bottom cells no longer need the crop-instead-of-squash hack. On unlock the
	// bars RETRACT DOWN into the cell floor (masked to the frame), instead of
	// swapping to an open-door sprite.
	const BAR_PITCH = 26; // target px between bar centres
	const BAR_W = 7;
	// bars run past the frame on both ends (masked away while idle): the top
	// extension hides the rounded caps so the bars read as set into the ceiling,
	// the bottom one covers backIn's anticipation dip (the bars rise a touch
	// before dropping) so no gap opens at the floor line.
	const BAR_TOP_EXT = 8;
	const BAR_BOTTOM_EXT = 0.14; // fraction of frame height
	const barTravel = (frame: Rect) => frame.h + BAR_TOP_EXT + 2;

	const drawBars = (g: PixiGraphics, w: number, h: number) => {
		const count = Math.max(2, Math.round(w / BAR_PITCH));
		const pitch = w / count;
		const top = -h / 2 - BAR_TOP_EXT;
		const len = h + BAR_TOP_EXT + h * BAR_BOTTOM_EXT;
		for (let i = 0; i < count; i++) {
			const x = -w / 2 + pitch * (i + 0.5);
			// jail bar in weathered iron: dark core, lit left flank, thin lantern
			// specular, shaded right edge. Warm throughout — the blue-grey steel it
			// used to be belonged to the old clinical palette.
			g.roundRect(x - BAR_W / 2, top, BAR_W, len, BAR_W / 2);
			g.fill({ color: 0x33291f });
			g.roundRect(x - BAR_W / 2 + 1, top + 1, BAR_W * 0.42, len - 2, BAR_W * 0.21);
			g.fill({ color: GRAVEYARD_PALETTE.iron, alpha: 0.55 });
			g.roundRect(x - BAR_W / 2 + 1.6, top + 2, 1.4, len - 4, 0.7);
			g.fill({ color: GRAVEYARD_PALETTE.dust, alpha: 0.4 });
			g.roundRect(x + BAR_W / 2 - 1.8, top + 1, 1.8, len - 2, 0.9);
			g.fill({ color: 0x000000, alpha: 0.45 });
		}
	};

	// slide progress per cell: 0 = bars up (locked), 1 = fully retracted (open).
	// Cells already open when the component mounts start at 1, so a session that
	// begins mid-bonus shows no bars without replaying the drop.
	const initialOpen = unlockedCellKeys(context.stateGame);
	const slide = new Map(
		CELL_KEYS.map((key) => [key, new Tween(initialOpen.has(key) ? 1 : 0)] as const),
	);

	$effect(() => {
		for (const key of CELL_KEYS) {
			const t = slide.get(key)!;
			if (openKeys.has(key)) {
				if (t.target !== 1) t.set(1, { duration: 500, easing: backIn });
			} else if (t.target !== 0) {
				// relock (bonus over, back to base game): bars snap straight back up
				t.set(0, { duration: 0 });
			}
		}
	});
</script>

<MainContainer>
	<!-- z-1: recessed socket behind EVERY cell, matching the board plate
	     exactly — for the side cells this is what cuts the full-card opening
	     through the iron column (the art's baked holes are smaller) -->
	<Container>
		<Graphics draw={(g) => drawSockets(g, slots)} />
	</Container>
	<!-- Each reserved cell is a 2-layer z-stack drawn INTO an opening in the
	     cell-block chassis (CellChassis paints the ironwork behind this):
	       z0  SlotSymbol  the symbol reeling inside the opening
	       z1  bars        vertical bars while locked / retracted once unlocked
	     The BARS live in their own layer mounted after every cell, NOT as a
	     sibling inside each cell: a Pixi child that gets rebuilt is APPENDED to
	     its parent, so a cell-level bar would fall behind the symbol and the
	     symbol would escape its cage.
	     Base game: every opening shows its symbol behind its bars. Bonus: the
	     unlocked groups' bars retract into the floor and premiums/wilds drop in
	     (a bottom WILD rises into its reel as a Wild Reel instead). -->
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
					size={SYMBOL_SIZE}
					clipH={slot.frame.h}
					clipW={slot.frame.w}
					clipRadius={CELL_CLIP_RADIUS}
					name={slot.symbol?.name}
					multiplier={slot.symbol?.multiplier}
					expanding={slot.symbol?.expanding}
					win={winKeys.has(slot.key)}
					locked={!slot.unlocked}
					fallOutDelay={fallOutDelays.get(slot.key)}
					fallInGate={fallInGates.get(slot.key)}
				/>
			</Container>
		{/each}
	</Container>
	<!-- z1: prison bars, filling each chassis opening, above every symbol.
	     Each cell's mask container stays PERMANENTLY mounted (per-slot remounts
	     would be harmless here since cells never overlap, but permanence keeps
	     the exit animation alive: the bars must stay mounted to slide out). -->
	<Container>
		{#each slots as slot (slot.key)}
			{@const t = slide.get(slot.key)!.current}
			<Container x={slot.frame.cx} y={slot.frame.cy}>
				<Rectangle
					isMask
					anchor={0.5}
					width={slot.frame.w}
					height={slot.frame.h}
					backgroundColor={0xffffff}
				/>
				{#if t < 1}
					<Container y={t * barTravel(slot.frame)}>
						<Graphics draw={(g) => drawBars(g, slot.frame.w, slot.frame.h)} />
					</Container>
				{/if}
			</Container>
		{/each}
	</Container>
</MainContainer>
