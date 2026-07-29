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
import { GEN_SYMBOL_SIZE, GEN_NUM_ROWS, GEN_REEL_PADDING } from './board.generated';

const SYMBOL_SIZE = GEN_SYMBOL_SIZE;
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
export const CELL_PITCH_X = SYMBOL_SIZE * COLUMN_PITCH_SCALE;

/** Measured by tools/make_chassis_assets.py. Fractions of the cropped tile. */
const ART = {
	side: {
		w: 605,
		h: 1505,
		/** opening centre x: the master art, and its mirror used on the right */
		cxLeft: 0.51657,
		cxRight: 0.48178,
		cy: [0.29181, 0.52703, 0.76299],
		openW: 0.35702,
		openH: 0.15282,
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

// --- side columns ------------------------------------------------------------
// Scale is capped by the screen, not by taste: the block is centred on the board
// and the design space only runs to y=0, so anything taller than this clips off
// the top. The openings land wherever that leaves them.
//
// SIDE_SCALE keeps the stone/chain columns from dominating the board — at 1.0
// each side was ~37% of board width. 0.78 trims that without regenerating art.
const SIDE_SCALE = 0.78;
export const SIDE_H = MAX_ROWS * SYMBOL_SIZE * 1.15 * SIDE_SCALE;
export const SIDE_W = (SIDE_H * ART.side.w) / ART.side.h;

// The side CELLS no longer use the art's baked openings (ART.side.openW/H,
// ~0.52 x 0.55 of a symbol): the special symbols must read at EXACTLY board
// scale, same width and height as a normal board card, nothing cropped. Each
// side cell is therefore a full symbol card, and LockedSlots recesses a socket
// through the iron over the (smaller) baked hole. Same numbers as
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

/** breathing room between the board edge and the blocks bolted to it */
export const CHASSIS_GAP = SYMBOL_SIZE * 0.02;

/** how far the chassis reaches below the board — the HUD rail drops by this.
 * The beam WALL art is gone: the bottom cells are full board-cell-sized slots
 * flush under the board, so the extent is a cell plus its number plate. */
// the cells stop exactly at the board bottom line now; only their number
// plates hang below it
export const CHASSIS_BOTTOM_EXTENT = SYMBOL_SIZE * 0.3;

export type Rect = { cx: number; cy: number; w: number; h: number };
export type BoardBox = { x: number; y: number; width: number; height: number };

/** where each block is drawn, anchored top-left, for a given board rect */
export const chassisBlocks = (board: BoardBox) => {
	const left = board.x - board.width * 0.5;
	const top = board.y - board.height * 0.5;
	return {
		// middle opening centred on the board, so the three openings straddle it
		sideL: { x: left - CHASSIS_GAP - SIDE_W, y: board.y - ART.side.cy[1] * SIDE_H },
		sideR: { x: left + board.width + CHASSIS_GAP, y: board.y - ART.side.cy[1] * SIDE_H },
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
	// the board's ROW PITCH (SYMBOL_SIZE) and vertically centred on the board —
	// the same grid a reel uses, so a side symbol sits exactly like a board
	// symbol. The art's baked openings are smaller and off this pitch; the
	// horizontal centres still come from the art (the machined face of the
	// column), only the vertical layout is now the board grid.
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

/**
 * The parts that were cut OUT of the block art so they can be animated: the two
 * gears on each side column, the free-hanging chain and counterweights down its
 * outer edge, and the chain swags slung under the beam. The blocks now carry a
 * machined socket where each gear was, so the gear can turn without dragging a
 * baked shadow around with it. Measured by tools/make_chassis_assets.py.
 *
 * `r` is the sprite's half-size (tooth tips plus a little clearance), not the
 * tooth-tip radius, so the game can scale the sprite straight from it.
 */
const MOVERS = {
	cogs: [
		{ cx: 0.50579, cy: 0.06844, r: 0.06312 },
		{ cx: 0.50413, cy: 0.92625, r: 0.06578 },
	],
	chainW: 0.09917,
	swagY: 0.9005,
} as const;

export type CogSpot = { key: string; cx: number; cy: number; size: number };

/** every gear on both side columns, in board space */
export const chassisCogs = (board: BoardBox): CogSpot[] => {
	const blocks = chassisBlocks(board);
	const out: CogSpot[] = [];
	for (const [side, block] of [
		['l', blocks.sideL],
		['r', blocks.sideR],
	] as const) {
		MOVERS.cogs.forEach((cog, i) => {
			// the right column is the left column's art mirrored, so its sockets
			// sit at the mirrored fraction
			const fx = side === 'l' ? cog.cx : 1 - cog.cx;
			out.push({
				key: `${side}${i}`,
				cx: block.x + fx * SIDE_W,
				cy: block.y + cog.cy * SIDE_H,
				size: 2 * cog.r * SIDE_H,
			});
		});
	}
	return out;
};

/**
 * How tall the tiled chain strip is vs the column. Built by
 * tools/make_chassis_chain_tile.py (3913 / 1505) so the strip has runway to
 * scroll down behind a mask while the gears wind.
 */
export const CHAIN_STRIP_RATIO = 3913 / 1505;

/** the hanging chain + counterweights down the outer edge of each column */
export const chassisChains = (board: BoardBox) => {
	const blocks = chassisBlocks(board);
	const w = MOVERS.chainW * SIDE_W;
	const stripH = SIDE_H * CHAIN_STRIP_RATIO;
	return [
		{
			key: 'l',
			assetKey: 'chassisChainL',
			x: blocks.sideL.x,
			y: blocks.sideL.y,
			w,
			h: SIDE_H,
			stripH,
		},
		{
			key: 'r',
			assetKey: 'chassisChainR',
			x: blocks.sideR.x + SIDE_W - w,
			y: blocks.sideR.y,
			w,
			h: SIDE_H,
			stripH,
		},
	];
};

/** the chain swags draped under the beam */
export const chassisSwag = (board: BoardBox) => {
	const blocks = chassisBlocks(board);
	return {
		x: blocks.beam.x,
		y: blocks.beam.y + MOVERS.swagY * BEAM_H,
		w: BEAM_W,
		h: (1 - MOVERS.swagY) * BEAM_H,
	};
};

// The stencilled cell-number plates ("01".."09") are gone: the full-card side
// cells sit on the board's row pitch with ~4px between openings, leaving no
// room for a plate (the bottom cells lost theirs when the beam wall went).
