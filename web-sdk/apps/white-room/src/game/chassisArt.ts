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
import { GEN_SYMBOL_SIZE, GEN_NUM_ROWS } from './board.generated';

const SYMBOL_SIZE = GEN_SYMBOL_SIZE;
const MAX_ROWS = Math.max(...GEN_NUM_ROWS);

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
export const SIDE_H = MAX_ROWS * SYMBOL_SIZE * 1.15;
export const SIDE_W = (SIDE_H * ART.side.w) / ART.side.h;
export const SIDE_OPEN_W = SIDE_W * ART.side.openW;
export const SIDE_OPEN_H = SIDE_H * ART.side.openH;

// --- bottom beam -------------------------------------------------------------
// The beam is NOT free to scale: its three openings extend the middle reels, so
// their pitch has to be exactly one reel wide or the cells stop lining up with
// the columns above them. That single constraint fixes the whole beam size.
const BEAM_PITCH = (ART.beam.cx[2] - ART.beam.cx[0]) / 2;
export const BEAM_W = SYMBOL_SIZE / BEAM_PITCH;
export const BEAM_H = (BEAM_W * ART.beam.h) / ART.beam.w;
export const BEAM_OPEN_W = BEAM_W * ART.beam.openW;
export const BEAM_OPEN_H = BEAM_H * ART.beam.openH;

/** breathing room between the board edge and the blocks bolted to it */
export const CHASSIS_GAP = SYMBOL_SIZE * 0.04;

/** how far the chassis reaches below the board — the HUD rail drops by this */
export const CHASSIS_BOTTOM_EXTENT = CHASSIS_GAP + BEAM_H;

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
	for (let j = 0; j < 3; j++) {
		const cy = blocks.sideL.y + ART.side.cy[j] * SIDE_H;
		out[`left:${j}`] = {
			cx: blocks.sideL.x + ART.side.cxLeft * SIDE_W,
			cy,
			w: SIDE_OPEN_W,
			h: SIDE_OPEN_H,
		};
		out[`right:${j}`] = {
			cx: blocks.sideR.x + ART.side.cxRight * SIDE_W,
			cy,
			w: SIDE_OPEN_W,
			h: SIDE_OPEN_H,
		};
	}
	for (let i = 0; i < 3; i++) {
		out[`bottom:${i}`] = {
			cx: blocks.beam.x + ART.beam.cx[i] * BEAM_W,
			cy: blocks.beam.y + ART.beam.cy * BEAM_H,
			w: BEAM_OPEN_W,
			h: BEAM_OPEN_H,
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

/** the hanging chain + counterweights down the outer edge of each column */
export const chassisChains = (board: BoardBox) => {
	const blocks = chassisBlocks(board);
	const w = MOVERS.chainW * SIDE_W;
	return [
		{ key: 'l', assetKey: 'chassisChainL', x: blocks.sideL.x, y: blocks.sideL.y, w, h: SIDE_H },
		{
			key: 'r',
			assetKey: 'chassisChainR',
			x: blocks.sideR.x + SIDE_W - w,
			y: blocks.sideR.y,
			w,
			h: SIDE_H,
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

/** blank riveted plate above each opening, where the cell number is drawn */
export const platePoint = (frame: Rect, side: boolean) => ({
	x: frame.cx,
	y: frame.cy - frame.h * (side ? 0.72 : 0.62),
});

/** cell numbers stencilled on the plates: left 01-03, bottom 04-06, right 07-09 */
export const CELL_NUMBERS: Record<string, string> = {
	'left:0': '01',
	'left:1': '02',
	'left:2': '03',
	'bottom:0': '04',
	'bottom:1': '05',
	'bottom:2': '06',
	'right:0': '07',
	'right:1': '08',
	'right:2': '09',
};
