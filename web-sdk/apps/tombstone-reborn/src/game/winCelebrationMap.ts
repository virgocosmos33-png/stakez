import { SECOND } from 'constants-shared/time';

import type { MusicName, SoundEffectName } from './sound';

/** Probed length of each hero-plate clip (all six masters are 10s). */
export const CELEB_VIDEO_MS = 10_000;

/** Scene beds loop, so a plate holds for the clip — skip still cuts early. */
export const celebPlateDurationMs = (_bgm?: string) => CELEB_VIDEO_MS;

// Tier thresholds are bet multiples (book amount / 100 = multiplier of bet).
// At a $0.20 bet: 25x = $5, 50x = $10, 100x = $20, 500x = $100, 2500x = $500,
// and the 30000x wincap is BACK FROM HELL & BACK TO HELL & BACK / MAX WIN.
//
// Titles are Silas hunting the other premiums, one plate per clip:
//   LAST AMEN → DUST TRAIL → HANG THE PIG → THE LAST WORDS → HAUL THE DEAD → BACK FROM HELL & BACK TO HELL & BACK.
//
// These replace the generic western ladder (BOUNTY → BOOT HILL). Titles are
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
	// Big tiers: each plate stays until its clip (and scene track) finish,
	// then the next plate starts (unless the player skips).
	{
		tier: 2,
		alias: 'big',
		type: 'big',
		title: 'LAST AMEN',
		slug: 'bounty',
		minMultiplier: 25,
		presentDuration: celebPlateDurationMs('bgm_celeb_1'),
		sound: { sfx: undefined, bgm: 'bgm_celeb_1' },
	},
	{
		tier: 3,
		alias: 'superwin',
		type: 'big',
		title: 'DUST TRAIL',
		slug: 'showdown',
		minMultiplier: 50,
		presentDuration: celebPlateDurationMs('bgm_celeb_2'),
		sound: { sfx: undefined, bgm: 'bgm_celeb_2' },
	},
	{
		tier: 4,
		alias: 'mega',
		type: 'big',
		title: 'HANG THE PIG',
		slug: 'highnoon',
		minMultiplier: 100,
		presentDuration: celebPlateDurationMs('bgm_celeb_3'),
		sound: { sfx: undefined, bgm: 'bgm_celeb_3' },
	},
	{
		tier: 5,
		alias: 'epic',
		type: 'big',
		title: 'THE LAST WORDS',
		slug: 'laststand',
		minMultiplier: 500,
		presentDuration: celebPlateDurationMs('bgm_celeb_4'),
		sound: { sfx: undefined, bgm: 'bgm_celeb_4' },
	},
	{
		tier: 6,
		alias: 'epic',
		type: 'big',
		title: 'HAUL THE DEAD',
		slug: 'bloodmoney',
		minMultiplier: 2500,
		presentDuration: celebPlateDurationMs('bgm_celeb_5'),
		sound: { sfx: undefined, bgm: 'bgm_celeb_5' },
	},
	{
		tier: 7,
		alias: 'max',
		type: 'big',
		title: 'BACK FROM HELL & BACK TO HELL & BACK',
		slug: 'boothill',
		minMultiplier: 30000,
		presentDuration: celebPlateDurationMs('bgm_celeb_6'),
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

// every big-win tier this amount climbs through; each plate stays until
// its clip finishes, then the next plate starts
export const getTiersPassed = (bookAmount: number): WinCelebrationData[] => {
	const multiplier = bookAmountToMultiplier(bookAmount);
	return winCelebrationTiers.filter(
		(tierData) => tierData.tier >= 2 && multiplier >= tierData.minMultiplier,
	);
};

/** Wall-clock of every scene this amount will play, for the winUpdate safety net. */
export const celebrationRollupMs = (bookAmount: number) =>
	getTiersPassed(bookAmount).reduce((sum, tierData) => sum + tierData.presentDuration, 0);
