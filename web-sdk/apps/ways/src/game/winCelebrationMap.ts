import { SECOND } from 'constants-shared/time';

import type { MusicName, SoundEffectName } from './sound';

// Tier thresholds are bet multiples (book amount / 100 = multiplier of bet).
// At a $0.20 bet: 25x = $5, 50x = $10, 100x = $20, 500x = $100, 2500x = $500,
// and the 30000x wincap is MAX WIN.
export type WinCelebrationData = {
	tier: number;
	// alias/type keep compatibility with coin particles + win level sounds
	alias: 'nice' | 'big' | 'superwin' | 'mega' | 'epic' | 'max';
	type: 'small' | 'big';
	title: string | null;
	minMultiplier: number;
	presentDuration: number;
	sound: { sfx?: SoundEffectName; bgm?: MusicName };
};

export const winCelebrationTiers: WinCelebrationData[] = [
	{
		tier: 1,
		alias: 'nice',
		type: 'small',
		title: null,
		minMultiplier: 0,
		presentDuration: 1 * SECOND,
		sound: { sfx: 'sfx_winlevel_nice', bgm: undefined },
	},
	// no bgm on the big tiers: the celebration carries its own psychedelic
	// sfx layer instead of the old win-level music
	{
		tier: 2,
		alias: 'big',
		type: 'big',
		title: 'BIG WIN',
		minMultiplier: 25,
		presentDuration: 5 * SECOND,
		sound: { sfx: undefined, bgm: undefined },
	},
	{
		tier: 3,
		alias: 'superwin',
		type: 'big',
		title: 'SUPER WIN',
		minMultiplier: 50,
		presentDuration: 7 * SECOND,
		sound: { sfx: undefined, bgm: undefined },
	},
	{
		tier: 4,
		alias: 'mega',
		type: 'big',
		title: 'MEGA WIN',
		minMultiplier: 100,
		presentDuration: 10 * SECOND,
		sound: { sfx: undefined, bgm: undefined },
	},
	{
		tier: 5,
		alias: 'epic',
		type: 'big',
		title: 'EPIC WIN',
		minMultiplier: 500,
		presentDuration: 14 * SECOND,
		sound: { sfx: undefined, bgm: undefined },
	},
	{
		tier: 6,
		alias: 'epic',
		type: 'big',
		title: 'UNHOLY WIN',
		minMultiplier: 2500,
		presentDuration: 18 * SECOND,
		sound: { sfx: undefined, bgm: undefined },
	},
	{
		tier: 7,
		alias: 'max',
		type: 'big',
		title: 'MAX WIN',
		minMultiplier: 30000,
		presentDuration: 24 * SECOND,
		sound: { sfx: undefined, bgm: undefined },
	},
];

export const bookAmountToMultiplier = (bookAmount: number) => bookAmount / 100;

export const getWinCelebration = (bookAmount: number): WinCelebrationData => {
	const multiplier = bookAmountToMultiplier(bookAmount);
	let result = winCelebrationTiers[0];
	for (const tierData of winCelebrationTiers) {
		if (multiplier >= tierData.minMultiplier) result = tierData;
	}
	return result;
};

// every big-win tier this amount climbs through; the presentation gives each
// one an equal slice of the count-up so all celebrations are actually seen
export const getTiersPassed = (bookAmount: number): WinCelebrationData[] => {
	const multiplier = bookAmountToMultiplier(bookAmount);
	return winCelebrationTiers.filter(
		(tierData) => tierData.tier >= 2 && multiplier >= tierData.minMultiplier,
	);
};
