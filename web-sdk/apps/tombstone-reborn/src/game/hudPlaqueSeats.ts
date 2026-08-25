/**
 * WAYS / MULTI / WIN / FREE SPINS seats from the PSD bbox, converted with
 * the same sceneToMain cover-fit as FRAME timber and hang chains.
 *
 * The box sprites are U-frames (open top, floor plank). The PSD well was a
 * 12%/18% inset of the whole box — that rectangle runs through the posts and
 * into the floor, so the value sits on the bottom lip. The well is the inner
 * U opening of the live box art, clipped under the labeled pallet.
 */
import { FRAME_SEATS } from './frameSeats.generated';
import { sceneRectToMain, type SceneRect } from './saloonLamps';

export type HudRect = { x: number; y: number; w: number; h: number };

export type HudPlaqueGeom = {
	label: string;
	value: string;
	boxKey: string;
	palletKey: string;
	box: HudRect;
	pallet: HudRect;
	well: HudRect;
	chains: { id: string; key: string; x: number; y: number; w: number; h: number }[];
};

const BOX_BASE: Record<string, string> = {
	WAYS: 'woodReadoutWays',
	MULTI: 'woodReadoutMulti',
	WIN: 'woodReadoutWin',
	'FREE SPINS': 'woodReadoutSpins',
};

const PALLET_BASE: Record<string, string> = {
	WAYS: 'woodPalletWays',
	MULTI: 'woodPalletMulti',
	WIN: 'woodPalletWin',
	'FREE SPINS': 'woodPalletSpins',
};

const SLUG: Record<string, keyof typeof FRAME_SEATS.plaques> = {
	WAYS: 'ways',
	MULTI: 'multi',
	WIN: 'win',
	'FREE SPINS': 'spins',
};

const boxKey = (label: string, atmo: string) => {
	const base = BOX_BASE[label] ?? 'woodReadoutWays';
	if (atmo === 'super') return `${base}Super`;
	if (atmo === 'small') return `${base}Small`;
	return base;
};

const palletKey = (label: string, atmo: string) => {
	const base = PALLET_BASE[label] ?? 'woodPalletWays';
	if (atmo === 'super' && label !== 'FREE SPINS') return `${base}Super`;
	if (atmo === 'small' && label !== 'FREE SPINS') return `${base}Small`;
	return base;
};

const chainKey = (psdKey: string, atmo: string) => {
	if (atmo === 'super') return 'hudChainSuper';
	if (atmo === 'small') return 'hudChainSmall';
	return psdKey;
};

/** Inner U opening as fractions of the box sprite. y0 is the pallet, not the box top. */
type PocketBand = { x0: number; x1: number; y1: number };

const BASE_POCKET: Record<string, PocketBand> = {
	ways: { x0: 0.255, x1: 0.708, y1: 0.6 },
	multi: { x0: 0.255, x1: 0.708, y1: 0.6 },
	win: { x0: 0.255, x1: 0.708, y1: 0.595 },
	spins: { x0: 0.255, x1: 0.708, y1: 0.595 },
};

/** Bonus box PNGs are padded glow plates; the wood opening sits further in. */
const BONUS_POCKET: Record<string, PocketBand> = {
	ways: { x0: 0.293, x1: 0.721, y1: 0.57 },
	multi: { x0: 0.311, x1: 0.718, y1: 0.578 },
	win: { x0: 0.297, x1: 0.716, y1: 0.57 },
	spins: { x0: 0.301, x1: 0.711, y1: 0.558 },
};

const pocketBand = (slug: string, atmo: string): PocketBand => {
	const table = atmo === 'small' || atmo === 'super' ? BONUS_POCKET : BASE_POCKET;
	return table[slug] ?? BASE_POCKET.ways;
};

const PALLET_GAP = 2;
const WELL_MIN_H = 8;

const wellFromBox = (slug: string, atmo: string, box: SceneRect, pallet: SceneRect): SceneRect => {
	const band = pocketBand(slug, atmo);
	const bw = box.right - box.left;
	const bh = box.bottom - box.top;
	const left = box.left + bw * band.x0;
	const right = box.left + bw * band.x1;
	const bottom = box.top + bh * band.y1;
	const top = Math.min(bottom - WELL_MIN_H, Math.max(pallet.bottom + PALLET_GAP, box.top));
	return { left, top, right, bottom };
};

export const plaqueGeom = (
	label: string,
	value: string,
	atmo: string,
	canvas: { width: number; height: number },
	main: { width: number; height: number; scale: number },
): HudPlaqueGeom | null => {
	const slug = SLUG[label];
	if (slug == null) return null;
	const seat = FRAME_SEATS.plaques[slug];
	const well = wellFromBox(slug, atmo, seat.box, seat.pallet);
	return {
		label,
		value,
		boxKey: boxKey(label, atmo),
		palletKey: palletKey(label, atmo),
		box: sceneRectToMain(seat.box, canvas, main),
		pallet: sceneRectToMain(seat.pallet, canvas, main),
		well: sceneRectToMain(well, canvas, main),
		chains: seat.chains.map((c) => ({
			id: c.id,
			key: chainKey(c.key, atmo),
			...sceneRectToMain(c, canvas, main),
		})),
	};
};
