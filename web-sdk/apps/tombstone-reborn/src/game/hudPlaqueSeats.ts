/**
 * WAYS / MULTI / WIN / FREE SPINS seats from the PSD bbox, converted with
 * the same sceneToMain cover-fit as FRAME timber and hang chains.
 */
import { FRAME_SEATS } from './frameSeats.generated';
import { sceneRectToMain } from './saloonLamps';

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

const chainKey = (
	psdKey: string,
	atmo: string,
): string => {
	if (atmo === 'super') return 'hudChainSuper';
	if (atmo === 'small') return 'hudChainSmall';
	return psdKey;
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
	return {
		label,
		value,
		boxKey: boxKey(label, atmo),
		palletKey: palletKey(label, atmo),
		box: sceneRectToMain(seat.box, canvas, main),
		pallet: sceneRectToMain(seat.pallet, canvas, main),
		well: sceneRectToMain(seat.well, canvas, main),
		chains: seat.chains.map((c) => ({
			id: c.id,
			key: chainKey(c.key, atmo),
			...sceneRectToMain(c, canvas, main),
		})),
	};
};
