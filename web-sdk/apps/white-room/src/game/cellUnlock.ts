// Which of the nine reserved cells are OPEN right now.
//
// Two components need this answer and must never disagree: LockedSlots decides
// whether a cell shows open or barred, and CellChassis runs the ironwork -- the
// gears and chains -- when a cell opens. If they derived it separately the
// mechanism could turn for a cell that stayed shut, so the rule lives here once.
//
// A cell opens for any of three reasons: its GROUP is unlocked for the bonus
// (level 1 bottom, 2 +right, 3 +left), a WILD landed in a bottom cell and rose
// into a Wild Reel, or a feature card (Stretch/Split/Clone) landed in it -- which
// in the base game unlocks just that one cell.
import { BOARD_DIMENSIONS } from './constants';

export const BOTTOM_SLOTS = 3;
export const RIGHT_SLOTS = 3;
export const LEFT_SLOTS = 3;

/** bottom slot i sits under reel (BOTTOM_START + i) -- the middle reels */
export const BOTTOM_START = (BOARD_DIMENSIONS.x - BOTTOM_SLOTS) / 2;

type CellState = {
	unlockedGroups?: ('bottom' | 'right' | 'left')[] | null;
	unlockedSlots?: { unlocked: ('bottom' | 'right' | 'left')[] } | null;
	wildReelReels?: number[] | null;
	featureCells?: { reel?: number; side?: 'left' | 'right'; slotRow?: number }[] | null;
};

/**
 * Open groups for the whole bonus. `unlockedGroups` persists across the bonus so
 * a cell reads open the instant it reveals; this spin's event is only a fallback.
 */
export const openGroups = (state: CellState) =>
	state.unlockedGroups ?? state.unlockedSlots?.unlocked ?? [];

/** keys of every open cell: 'bottom:0'..'bottom:2', 'left|right:0'..:2 */
export const unlockedCellKeys = (state: CellState): Set<string> => {
	const groups = openGroups(state);
	const wildReels = state.wildReelReels ?? [];
	const features = state.featureCells ?? [];
	const keys = new Set<string>();

	for (let i = 0; i < BOTTOM_SLOTS; i++) {
		const reel = BOTTOM_START + i;
		const hasFeature = features.some((c) => c.reel === reel && c.side == null);
		if (groups.includes('bottom') || wildReels.includes(reel) || hasFeature) {
			keys.add(`bottom:${i}`);
		}
	}
	for (const side of ['right', 'left'] as const) {
		const count = side === 'right' ? RIGHT_SLOTS : LEFT_SLOTS;
		for (let j = 0; j < count; j++) {
			const hasFeature = features.some((c) => c.side === side && c.slotRow === j);
			if (groups.includes(side) || hasFeature) keys.add(`${side}:${j}`);
		}
	}
	return keys;
};

/** which chassis block a cell key belongs to */
export const blockOf = (key: string) => key.split(':')[0] as 'bottom' | 'left' | 'right';
