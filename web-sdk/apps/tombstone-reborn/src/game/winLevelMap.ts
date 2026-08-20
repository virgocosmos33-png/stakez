import { SECOND } from 'constants-shared/time';

export const winLevelMap = {
	1: {
		level: 1,
		alias: 'zero',
		type: 'small',
		text: null,
		presentDuration: 0,
		sound: { sfx: undefined, bgm: undefined },
		animation: undefined,
	},
	2: {
		level: 2,
		alias: 'standard',
		type: 'small',
		text: null,
		presentDuration: 0.6 * SECOND,
		sound: { sfx: undefined, bgm: undefined },
		animation: undefined,
	},
	3: {
		level: 3,
		alias: 'small',
		type: 'small',
		text: null,
		presentDuration: 1 * SECOND,
		sound: { sfx: undefined, bgm: undefined },
		animation: undefined,
	},
	4: {
		level: 4,
		alias: 'nice',
		type: 'medium',
		text: null,
		presentDuration: 1.5 * SECOND,
		sound: { sfx: undefined, bgm: undefined },
		animation: undefined,
	},
	5: {
		level: 5,
		alias: 'substantial',
		type: 'medium',
		text: null,
		presentDuration: 2.0 * SECOND,
		sound: { sfx: undefined, bgm: undefined },
		animation: undefined,
	},
	6: {
		level: 6,
		alias: 'big',
		type: 'big',
		text: 'LAST AMEN',
		presentDuration: 6 * SECOND,
		// staged celebration bed
		sound: { sfx: undefined, bgm: 'bgm_celeb_1' },
		animation: undefined,
	},
	7: {
		level: 7,
		alias: 'superwin',
		type: 'big',
		text: 'DUST TRAIL',
		presentDuration: 18 * SECOND,
		sound: { sfx: undefined, bgm: 'bgm_celeb_2' },
		animation: undefined,
	},
	8: {
		level: 8,
		alias: 'mega',
		type: 'big',
		text: 'HANG THE PIG',
		presentDuration: 20 * SECOND,
		sound: { sfx: undefined, bgm: 'bgm_celeb_3' },
		animation: undefined,
	},
	9: {
		level: 9,
		alias: 'epic',
		type: 'big',
		text: 'THE LAST WORDS',
		presentDuration: 26 * SECOND,
		sound: { sfx: undefined, bgm: 'bgm_celeb_4' },
		animation: undefined,
	},
	10: {
		level: 10,
		alias: 'max',
		type: 'big',
		text: 'BACK FROM HELL & BACK TO HELL & BACK',
		presentDuration: 32 * SECOND,
		sound: { sfx: undefined, bgm: 'bgm_celeb_6' },
		animation: undefined,
	},
} as const;

export type WinLevelMap = typeof winLevelMap;
export type WinLevel = keyof typeof winLevelMap;
export type WinLevelData = WinLevelMap[WinLevel];
export type WinLevelAlias = WinLevelData['alias'];
