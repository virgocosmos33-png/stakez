import { SECOND } from 'constants-shared/time';

import type { MusicName, SoundEffectName } from './sound';

// Tier thresholds are bet multiples (book amount / 100 = multiplier of bet).
// At a $0.20 bet: 25x = $5, 50x = $10, 100x = $20, 500x = $100, 2500x = $500,
// and the 30000x wincap is BOOT HILL / MAX WIN.
//
// Titles are the outlaw's payoff arc, escalating from collecting a price on a
// head to being buried rich in the graveyard:
//   BOUNTY → SHOWDOWN → HIGH NOON → LAST STAND → BLOOD MONEY → BOOT HILL.
//
// These replace the Madam Mirror asylum-intake titles that were still shipping
// (INTAKE → RESTRAINT → STRUGGLE → BREAKOUT → SCRATCH → WHITEOUT). Titles are
// A-Z + space only so they render in the bitmap face without missing glyphs.
// Scatters keep their own words; celebrations do not reuse them.
export type WinCelebrationData = {
	tier: number;
	// alias/type keep compatibility with coin particles + win level sounds
	alias: 'nice' | 'big' | 'superwin' | 'mega' | 'epic' | 'max';
	type: 'small' | 'big';
	title: string | null;
	/** hero plate slug — winTierPlateKey(slug) is the loaded asset key */
	slug: string;
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
		slug: '',
		minMultiplier: 0,
		presentDuration: 1 * SECOND,
		sound: { sfx: 'sfx_win_ways', bgm: undefined },
	},
	// Big tiers: WinCelebration.svelte drives the staged celebration bed.
	// Seed a matching bed here so setWin has a stage cue to play before the
	// takeover mounts.
	{
		tier: 2,
		alias: 'big',
		type: 'big',
		title: 'BOUNTY',
		slug: 'bounty',
		minMultiplier: 25,
		presentDuration: 5 * SECOND,
		sound: { sfx: undefined, bgm: 'bgm_celeb_1' },
	},
	{
		tier: 3,
		alias: 'superwin',
		type: 'big',
		title: 'SHOWDOWN',
		slug: 'showdown',
		minMultiplier: 50,
		presentDuration: 7 * SECOND,
		sound: { sfx: undefined, bgm: 'bgm_celeb_2' },
	},
	{
		tier: 4,
		alias: 'mega',
		type: 'big',
		title: 'HIGH NOON',
		slug: 'highnoon',
		minMultiplier: 100,
		presentDuration: 10 * SECOND,
		sound: { sfx: undefined, bgm: 'bgm_celeb_3' },
	},
	{
		tier: 5,
		alias: 'epic',
		type: 'big',
		title: 'LAST STAND',
		slug: 'laststand',
		minMultiplier: 500,
		presentDuration: 14 * SECOND,
		sound: { sfx: undefined, bgm: 'bgm_celeb_4' },
	},
	{
		tier: 6,
		alias: 'epic',
		type: 'big',
		title: 'BLOOD MONEY',
		slug: 'bloodmoney',
		minMultiplier: 2500,
		presentDuration: 18 * SECOND,
		sound: { sfx: undefined, bgm: 'bgm_celeb_5' },
	},
	{
		tier: 7,
		alias: 'max',
		type: 'big',
		title: 'BOOT HILL',
		slug: 'boothill',
		minMultiplier: 30000,
		presentDuration: 24 * SECOND,
		sound: { sfx: undefined, bgm: 'bgm_celeb_6' },
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
