/**
 * Spine room stays in authored colour. Bonus only adds heat.
 * Do not desaturate the western scene — that is not in the Spine project.
 */
import { Tween } from 'svelte/motion';
import { cubicInOut } from 'svelte/easing';

import { stateGame } from './stateGame.svelte';

export type Atmosphere = 'base' | 'small' | 'super';

/** Room is in a bonus. Free-spins plaque, barrel lamp, red filter 80%. */
export const isBonusAtmosphere = (atmo: Atmosphere) => atmo !== 'base';

/** Barrel lamp follows the bonus room, including a freegame that has not graded yet. */
export const isBarrelLampOn = () =>
	isBonusAtmosphere(stateGame.atmosphere) ||
	stateGame.gameType === 'freegame' ||
	stateGame.laneSuper;

const TARGETS: Record<
	Atmosphere,
	{ sat: number; warm: number; ember: number; smoke: number; fire: number }
> = {
	base: { sat: 1, warm: 0, ember: 0, smoke: 0, fire: 0 },
	small: { sat: 1, warm: 0.85, ember: 0.28, smoke: 0, fire: 0 },
	super: { sat: 1, warm: 1, ember: 0.7, smoke: 0.75, fire: 0.7 },
};

const FADE = { duration: 720, easing: cubicInOut };

export const atmoSat = new Tween(1);
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
	const t = TARGETS[next];
	const same = stateGame.atmosphere === next;
	if (!same) stateGame.atmosphere = next;
	const fade = same ? { duration: 0 } : FADE;
	atmoSat.set(t.sat, fade);
	atmoWarm.set(t.warm, fade);
	atmoEmber.set(t.ember, fade);
	atmoSmoke.set(t.smoke, fade);
	atmoFire.set(t.fire, fade);
};

export const syncAtmosphere = (hint?: Atmosphere) => {
	setAtmosphere(hint ?? atmosphereFromState());
};
