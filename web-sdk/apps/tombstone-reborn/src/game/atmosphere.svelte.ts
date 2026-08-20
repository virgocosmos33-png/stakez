/**
 * Nolimit-style room grade: base is monochrome, small bonus warms up,
 * big bonus burns. Drives BOTH the saloon plate and the wood board.
 */
import { Tween } from 'svelte/motion';
import { cubicInOut } from 'svelte/easing';

import { stateGame } from './stateGame.svelte';

export type Atmosphere = 'base' | 'small' | 'super';

const TARGETS: Record<
	Atmosphere,
	{ sat: number; warm: number; ember: number; smoke: number; fire: number }
> = {
	base: { sat: 0, warm: 0, ember: 0, smoke: 0, fire: 0 },
	// bonus plates are already painted — do not re-grade them
	small: { sat: 1, warm: 0, ember: 0, smoke: 0, fire: 0 },
	super: { sat: 1, warm: 0, ember: 0, smoke: 0, fire: 0 },
};

const FADE = { duration: 720, easing: cubicInOut };

export const atmoSat = new Tween(0);
export const atmoWarm = new Tween(0);
export const atmoEmber = new Tween(0);
export const atmoSmoke = new Tween(0);
export const atmoFire = new Tween(0);

export const atmosphereFromMode = (modeKey?: string | null): Atmosphere | null => {
	const mode = (modeKey ?? '').toLowerCase();
	if (mode === 'superspins' || mode === 'bonus_super') return 'super';
	if (mode === 'freespins' || mode === 'bonus_small') return 'small';
	return null;
};

export const atmosphereFromState = (): Atmosphere => {
	// Bet mode is NOT a visual signal. A bought BIG BONUS still plays its
	// trigger spin on the base room — scatters land, wins resolve, then the
	// banner grades the room. Reading activeBetModeKey here flipped the
	// background the instant the buy was confirmed.
	if (stateGame.laneSuper) return 'super';
	if (stateGame.gameType === 'freegame') return 'small';
	return 'base';
};

export const setAtmosphere = (next: Atmosphere) => {
	if (stateGame.atmosphere === next) return;
	stateGame.atmosphere = next;
	const t = TARGETS[next];
	atmoSat.set(t.sat, FADE);
	atmoWarm.set(t.warm, FADE);
	atmoEmber.set(t.ember, FADE);
	atmoSmoke.set(t.smoke, FADE);
	atmoFire.set(t.fire, FADE);
};

export const syncAtmosphere = (hint?: Atmosphere) => {
	setAtmosphere(hint ?? atmosphereFromState());
};
