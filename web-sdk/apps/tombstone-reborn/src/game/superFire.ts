import { SCENE_ART } from './saloonLamps';

/** Burning pockets on saloon_plate_super, in 0–1 of SCENE_ART. */
export type FirePocket = {
	id: string;
	/** spawn-line centre */
	cx: number;
	/** spawn-line y (base of the lick) */
	cy: number;
	/** spawn width */
	w: number;
	/** how far the lick rises */
	h: number;
	n: number;
	size: number;
	rise: number;
};

export const SUPER_FIRE_POCKETS: FirePocket[] = [
	{ id: 'leftHigh', cx: 0.08, cy: 0.18, w: 0.16, h: 0.16, n: 32, size: 78, rise: 0.9 },
	{ id: 'leftFloor', cx: 0.16, cy: 0.86, w: 0.09, h: 0.1, n: 12, size: 32, rise: 0.55 },
	{ id: 'centerHole', cx: 0.5, cy: 0.64, w: 0.28, h: 0.34, n: 40, size: 96, rise: 1.15 },
	{ id: 'rightWall', cx: 0.86, cy: 0.52, w: 0.2, h: 0.42, n: 36, size: 88, rise: 1.25 },
];

export const FIRE_PALETTE = [
	'#3a0a02',
	'#7a1502',
	'#b93a00',
	'#e2610a',
	'#f5911a',
	'#ffc94d',
	'#fff3c2',
] as const;

export const fireScene = SCENE_ART;
