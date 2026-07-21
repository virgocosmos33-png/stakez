import { BOARD_SIZES } from './constants';
import { stateGameDerived } from './stateGame.svelte';
import { stateLayoutDerived } from './stateLayout';

// ONE integrated left side panel flush to the gold reel frame (exact reference):
//   normal:  WAYS / WIN  (+ crystal ball baked in the art)
//   bonus:   FREE SPINS / WAYS / WIN  (+ crystal ball)
// Keep FRAME_* in sync with BoardFrame.svelte.

const FRAME_SCALE = 0.34;
const GOLD_INNER_X = 58;
const GOLD_INNER_Y = 101;
const FRAME_GAP = 6;
const FRAME_OUTSET_X = FRAME_GAP + GOLD_INNER_X * FRAME_SCALE;
const FRAME_OUTSET_Y = FRAME_GAP + GOLD_INNER_Y * FRAME_SCALE;

// Panel RIGHT edge tucks onto the gold so panel + reel frame read as ONE unit
const ATTACH_OVERLAP = 18;
const EDGE_MARGIN = 4;
const MIN_AVAIL = 90;

// side_rail_panel.png after key+crop
export const SIDE_PANEL_RATIO = 1479 / 460;

// Safe text well ABOVE the crystal-ball shelf (fractions of panel height).
// Measured on side_rail_panel.png: crest ends ~0.13, shelf/orb starts ~0.40.
const CONTENT_TOP = 0.145;
const CONTENT_BOT = 0.395;

export type TextSlot = { cx: number; cy: number; maxW: number; maxH: number };

export type SideRailLayout = {
	mounted: boolean;
	panelW: number;
	panelH: number;
	cx: number;
	cy: number;
	/** section centres top→bottom; length 2 (normal) or 3 (bonus) */
	sections: TextSlot[];
	/** divider Y between sections (absolute), length sections-1 */
	dividers: number[];
};

export const getSideRailLayout = (opts?: { freeSpins?: boolean }): SideRailLayout => {
	const board = stateGameDerived.boardLayout();
	const wide = ['desktop', 'landscape'].includes(stateLayoutDerived.layoutType());
	const count = opts?.freeSpins ? 3 : 2;

	const boardLeft = board.x - BOARD_SIZES.width / 2;
	const frameOuterLeft = boardLeft - FRAME_OUTSET_X;
	const frameOuterH = BOARD_SIZES.height + 2 * FRAME_OUTSET_Y;

	// Panel height matches the reel FRAME outer height → one continuous machine
	const panelH = frameOuterH;
	const panelW = panelH / SIDE_PANEL_RATIO;

	const rightX = frameOuterLeft + ATTACH_OVERLAP;
	const availLeft = rightX - EDGE_MARGIN;
	const mounted = wide && availLeft >= MIN_AVAIL;

	const cx = mounted ? rightX - panelW / 2 : board.x;
	const cy = board.y;
	const panelTop = cy - panelH / 2;

	const contentTop = panelTop + panelH * CONTENT_TOP;
	const contentBot = panelTop + panelH * CONTENT_BOT;
	const contentH = contentBot - contentTop;
	const slotH = contentH / count;
	const textMaxW = panelW * 0.55;
	const textMaxH = slotH * 0.72;

	const sections: TextSlot[] = Array.from({ length: count }, (_, i) => ({
		cx,
		cy: contentTop + slotH * (i + 0.5),
		maxW: textMaxW,
		maxH: textMaxH,
	}));

	const dividers = Array.from(
		{ length: count - 1 },
		(_, i) => contentTop + slotH * (i + 1),
	);

	if (!mounted) {
		// narrow: shrink panel above the board, same section logic
		const crestH = BOARD_SIZES.height * 0.42;
		const crestW = crestH / SIDE_PANEL_RATIO;
		const crestCy = board.y - BOARD_SIZES.height * 0.5 - crestH * 0.52;
		const cTop = crestCy - crestH / 2 + crestH * CONTENT_TOP;
		const cBot = crestCy - crestH / 2 + crestH * CONTENT_BOT;
		const cH = cBot - cTop;
		const sH = cH / count;
		return {
			mounted: false,
			panelW: crestW,
			panelH: crestH,
			cx: board.x,
			cy: crestCy,
			sections: Array.from({ length: count }, (_, i) => ({
				cx: board.x,
				cy: cTop + sH * (i + 0.5),
				maxW: crestW * 0.55,
				maxH: sH * 0.72,
			})),
			dividers: Array.from({ length: count - 1 }, (_, i) => cTop + sH * (i + 1)),
		};
	}

	return {
		mounted: true,
		panelW,
		panelH,
		cx,
		cy,
		sections,
		dividers,
	};
};

export const PLAQUE_RATIO = SIDE_PANEL_RATIO;
export const getRailLayout = () => getSideRailLayout();
