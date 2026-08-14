// CELL-BLOCK CHASSIS — geometry for the three heavy iron blocks that hold the
// nine reserved special cells (see CellChassis.svelte / LockedSlots.svelte).
//
// The cells used to be free-floating tiles positioned by hand-tuned constants.
// They are now openings punched through generated art, so the art decides where
// they sit: tools/make_chassis_assets.py keys the blocks off their magenta plate,
// detects the punched openings, and prints the fractions below. Everything else
// here is solved FROM those fractions, so regenerating the art and pasting a new
// ART block is all it takes to move the cells.
//
// Leaf module on purpose: it imports only the generated board numbers, never
// state or constants.ts, because constants.ts reads LOCKED_SLOTS_BOTTOM_EXTENT
// back out of it to drop the HUD rail below the beam.
import { GEN_NUM_REELS, GEN_NUM_ROWS, GEN_REEL_PADDING } from './board.generated';

const MAX_ROWS = Math.max(...GEN_NUM_ROWS);

/**
 * HORIZONTAL pitch between reel columns.
 *
 * The cell pitch is square (SYMBOL_SIZE) but the CARD painted inside it is
 * portrait (SYMBOL_CARD_W ≈ 0.75 × pitch), so a square pitch leaves a ~29px
 * channel between columns against a ~3px gap between rows — the columns read as
 * separate strips instead of one board. Pulling the columns in to 0.8 pitch
 * evens the two gutters out (≈5px vs ≈3px).
 *
 * Lives here rather than constants.ts because this is the leaf module and the
 * bottom beam has to be built from the same number — constants.ts reads it back
 * out. Anything positioning by (reel, row) must use this for x and SYMBOL_SIZE
 * for y.
 */
export const COLUMN_PITCH_SCALE = 0.8;

/** The cage/beam ART is no longer drawn (the side cells are board-plate
 * sockets now), but the measured fractions still SOLVE the layout: SYMBOL_SIZE
 * and the nine cell frames derive from them, so they stay. */
const ART = {
	side: {
		w: 355,
		h: 1505,
		/** the cage is symmetric and its openings are centred, both sides */
		cxLeft: 0.5,
		cxRight: 0.5,
		cy: [0.22129, 0.5, 0.77871],
		openW: 0.82887,
		openH: 0.25229,
	},
	beam: {
		w: 1510,
		h: 603,
		cx: [0.22765, 0.50016, 0.77345],
		cy: 0.52185,
		openW: 0.20795,
		openH: 0.58541,
	},
} as const;

// --- side cages ---------------------------------------------------------------
// The side cells are COLUMNS OF THE BOARD'S OWN GRID, not blocks bolted beside
// it. The cage is one card wide plus the gutter the board leaves between two
// cards, and it sits one column pitch outside the end reel — so the seven
// columns are evenly spaced and read as one board.
//
// It used to be a machine panel scaled to taste (SIDE_SCALE against a 605px-wide
// tile), which put the special cells about four times further from the reels
// than the reels sit from each other, and cost the board 42% of a phone screen.
const SIDE_SCALE = 0.78;

// Everything horizontal is first expressed in SYMBOL_SIZEs, because the symbol
// size is solved from them below rather than the other way round.
const SIDE_H_SCALE = MAX_ROWS * 1.15 * SIDE_SCALE;
const SIDE_W_SCALE = (SIDE_H_SCALE * ART.side.w) / ART.side.h;

/**
 * Portrait design width. The main container fits a PORTRAIT_DESIGN_W x 1422
 * design space to the screen, and on a phone the screen is proportionally taller
 * than that, so the fit is by WIDTH — these units are the phone's screen width
 * exactly. The whole card row (7 columns + 2 cage halves) is solved to add up to
 * this, so it is the single knob that scales the board + symbols: bigger here =>
 * bigger everywhere. MUST stay in sync with stateLayout's portrait main width so
 * the row keeps filling the portrait screen edge-to-edge.
 */
export const PORTRAIT_DESIGN_W = 800;

/**
 * SOLVED, not configured: seven columns and the two cage halves at either end
 * have to add up to the portrait design width, so whatever the cages do not take
 * is the board's.
 *
 * This used to be a fixed 118 from the game-builder config, which left the row
 * at 817 units against a design space of 800 — slightly overflowing, and with
 * the old columns eating 42% of the width the board only ever got 58% of a phone
 * screen. Deriving it means any change to the cage hands the reclaimed width
 * straight to the reels instead of widening the margins.
 *
 * Width is the only binding constraint: at this size the board is still inside
 * the shortest design height (desktop's 800) with room for the HUD rail.
 */
export const SYMBOL_SIZE = Math.floor(
	PORTRAIT_DESIGN_W / ((GEN_NUM_REELS + 1) * COLUMN_PITCH_SCALE + SIDE_W_SCALE),
);

export const CELL_PITCH_X = SYMBOL_SIZE * COLUMN_PITCH_SCALE;

export const SIDE_H = SYMBOL_SIZE * SIDE_H_SCALE;
export const SIDE_W = SYMBOL_SIZE * SIDE_W_SCALE;

// A side cell is a full symbol card — exactly the width and height of a card on
// the reels, nothing cropped — and the cage's openings are cut a little smaller
// (make_chassis_cage.py, 0.93 of a card) so the card always covers its hole and
// LockedSlots can recess a socket around the edge. Same numbers as
// constants.SYMBOL_CARD_W/H — duplicated because this is the leaf module
// constants.ts itself imports from.
const SIDE_CELL_H = SYMBOL_SIZE * (292 / 300);
const SIDE_CELL_W = SIDE_CELL_H * 0.775;

// --- bottom beam -------------------------------------------------------------
// The beam is NOT free to scale: its three openings extend the middle reels, so
// their pitch has to be exactly one reel wide or the cells stop lining up with
// the columns above them. That single constraint fixes the whole beam size.
const BEAM_PITCH = (ART.beam.cx[2] - ART.beam.cx[0]) / 2;
export const BEAM_W = CELL_PITCH_X / BEAM_PITCH;
export const BEAM_H = (BEAM_W * ART.beam.h) / ART.beam.w;
export const BEAM_OPEN_W = BEAM_W * ART.beam.openW;
export const BEAM_OPEN_H = BEAM_H * ART.beam.openH;

/** breathing room under the board, for the (unused) bottom beam block. The side
 * cages no longer need one: they are placed on the column grid. */
export const CHASSIS_GAP = SYMBOL_SIZE * 0.02;

/** how far the chassis reaches below the board — the HUD rail drops by this.
 * The beam WALL art is gone: the bottom cells are full board-cell-sized slots
 * flush under the board, so the extent is a cell plus its number plate. */
// the cells stop exactly at the board bottom line now; only their number
// plates hang below it
export const CHASSIS_BOTTOM_EXTENT = SYMBOL_SIZE * 0.3;

export type Rect = { cx: number; cy: number; w: number; h: number };
export type BoardBox = { x: number; y: number; width: number; height: number };

/**
 * Centre x of a column on the board's grid. Reels are 0..n-1; the two special
 * cages are the columns either side of them, -1 and n. Uses the same formula as
 * getSymbolX — CELL_PITCH_X and GEN_REEL_PADDING (0.53, NOT 0.5) — so a side
 * card lines up with the reels exactly as one reel lines up with the next.
 */
export const columnCx = (board: BoardBox, column: number) =>
	board.x - board.width * 0.5 + CELL_PITCH_X * (column + GEN_REEL_PADDING);

/**
 * How far the row of CARDS sits right of the board box that holds it.
 *
 * Card centres run at (column + GEN_REEL_PADDING) pitches from the box's left
 * edge, and that padding is 0.53 rather than 0.5, so the cards sit a hair right
 * of centre inside their own box. Centring the box therefore leaves a sliver of
 * margin down the left and none down the right — which nothing noticed while the
 * board was small, but shows the moment the seven columns fill the screen.
 * boardLayout subtracts this so it is the CARDS that end up centred.
 */
export const COLUMN_ROW_OFFSET = (GEN_REEL_PADDING - 0.5) * CELL_PITCH_X;

/** where each block is drawn, anchored top-left, for a given board rect */
export const chassisBlocks = (board: BoardBox) => {
	const top = board.y - board.height * 0.5;
	return {
		// the cage hangs on its own column, centred on that column's card
		sideL: {
			x: columnCx(board, -1) - ART.side.cxLeft * SIDE_W,
			y: board.y - ART.side.cy[1] * SIDE_H,
		},
		sideR: {
			x: columnCx(board, GEN_NUM_REELS) - ART.side.cxRight * SIDE_W,
			y: board.y - ART.side.cy[1] * SIDE_H,
		},
		beam: { x: board.x - BEAM_W * 0.5, y: top + board.height + CHASSIS_GAP },
		w: { side: SIDE_W, beam: BEAM_W },
		h: { side: SIDE_H, beam: BEAM_H },
	};
};

/**
 * The nine cell openings in board space, keyed the way the book events address
 * them: 'left:0'..'left:2' and 'right:0'..'right:2' top-to-bottom, 'bottom:0'..
 * 'bottom:2' left-to-right. LockedSlots, CellLightning and CellChassis all read
 * this, so a cell, its cage and its lightning can never drift apart.
 */
export const cellFrames = (board: BoardBox): Record<string, Rect> => {
	const blocks = chassisBlocks(board);
	const out: Record<string, Rect> = {};
	// side cells: one full board card each (see SIDE_CELL_W/H above), stacked at
	// the board's ROW PITCH (SYMBOL_SIZE) and vertically centred on the board,
	// in the column the cage hangs on. Both axes are the board's own grid now,
	// so a side symbol sits exactly like a board symbol — and the cage art is
	// cut to that grid rather than the grid being fitted to the art.
	for (let j = 0; j < 3; j++) {
		const cy = board.y + (j - 1) * SYMBOL_SIZE;
		out[`left:${j}`] = {
			cx: blocks.sideL.x + ART.side.cxLeft * SIDE_W,
			cy,
			w: SIDE_CELL_W,
			h: SIDE_CELL_H,
		};
		out[`right:${j}`] = {
			cx: blocks.sideR.x + ART.side.cxRight * SIDE_W,
			cy,
			w: SIDE_CELL_W,
			h: SIDE_CELL_H,
		};
	}
	// bottom cells: no beam wall any more — each cell is a full board-cell-sized
	// slot tucked FLUSH under its own middle reel, filling the diamond's lower
	// notch, so it reads as that reel's extra bottom cell rather than a cage
	// floating below the whole board. Positions use the AUTHORED diamond heights
	// (never the live board), so the cells hold still when a wild reel grows.
	const boardTop = board.y - board.height * 0.5;
	// the board's true bottom line, set by the tall OUTER reels — every bottom
	// cell ends exactly on it, never past it
	const boardBottom = boardTop + MAX_ROWS * SYMBOL_SIZE;
	// EXACT board grid: each bottom cell fills its reel's notch from the reel's
	// bottom edge down to the board bottom line (04/06 shorter than 05).
	// cx MUST use the same formula as getSymbolX — reel + GEN_REEL_PADDING
	// (0.53, NOT 0.5) — or the cells land a few px left of the symbols above.
	// Width is the symbol CARD width, so the special symbols read exactly as
	// wide as the normal symbols on the reels.
	const GROUT = 1.75;
	const CARD_W = SYMBOL_SIZE * (292 / 300) * 0.775; // = constants.SYMBOL_CARD_W
	const boardLeft = board.x - board.width * 0.5;
	for (let i = 0; i < 3; i++) {
		const reelIndex = i + 1; // bottom cells extend the three middle reels
		const rows = GEN_NUM_ROWS[reelIndex] ?? MAX_ROWS;
		const reelBottom = boardTop + ((MAX_ROWS - rows) / 2 + rows) * SYMBOL_SIZE;
		const cellH = boardBottom - reelBottom - GROUT * 2;
		out[`bottom:${i}`] = {
			cx: boardLeft + CELL_PITCH_X * (reelIndex + GEN_REEL_PADDING),
			cy: reelBottom + GROUT + cellH * 0.5,
			w: CARD_W,
			h: cellH,
		};
	}
	return out;
};

// The animated movers (gears, hanging chains, beam swags) are gone with the
// cage art itself: the side cells are sockets of the board plate now
// (BoardPlate.svelte), with only the prison bars (LockedSlots) over them.

// The stencilled cell-number plates ("01".."09") are gone: the full-card side
// cells sit on the board's row pitch with ~4px between openings, leaving no
// room for a plate (the bottom cells lost theirs when the beam wall went).
