/**
 * Small / big bonus beds. Long loops stay as their own mp3s — they are not
 * packed into the SFX sprite (that atlas is for stings, not full songs).
 *
 *   bonusgame 1 bgm.mp3 → bgm_bonus_small  (freespins / bonus_small)
 *   bonusgame 2 bgm.mp3 → bgm_bonus_super  (superspins / bonus_super)
 *   ember.mp3           → layered under bgm_bonus_super only
 */
import { Howl } from 'howler';

import { stateSoundDerived } from 'state-shared';

import type { BonusEntryTier } from './bonusEntryArt';
import { sound, type MusicName } from './sound';

export const BONUS_BGM_SMALL = 'bgm_bonus_small' as const;
export const BONUS_BGM_SUPER = 'bgm_bonus_super' as const;

export type BonusBgmName = typeof BONUS_BGM_SMALL | typeof BONUS_BGM_SUPER;

const SRC: Record<BonusBgmName, string> = {
	bgm_bonus_small: '/assets/audio/bgm_bonus_small.mp3',
	bgm_bonus_super: '/assets/audio/bgm_bonus_super.mp3',
};

const EMBER_SRC = '/assets/audio/bgm_super_ember.mp3';
/** Sit under the super score so both beds read, not one drown. */
const EMBER_VOL = 0.62;

const howls = new Map<BonusBgmName, Howl>();
let active: BonusBgmName | null = null;
let playId: number | null = null;
let emberHowl: Howl | null = null;
let emberPlayId: number | null = null;

const bed = (name: BonusBgmName) => {
	const existing = howls.get(name);
	if (existing) return existing;
	const howl = new Howl({
		src: [SRC[name]],
		loop: true,
		preload: true,
		html5: true,
	});
	howls.set(name, howl);
	return howl;
};

const emberBed = () => {
	if (emberHowl) return emberHowl;
	emberHowl = new Howl({
		src: [EMBER_SRC],
		loop: true,
		preload: true,
		html5: true,
	});
	return emberHowl;
};

const applyVolume = (howl: Howl) => {
	howl.volume(stateSoundDerived.volumeMusic());
};

const applyEmberVolume = () => {
	if (!emberHowl) return;
	emberHowl.volume(stateSoundDerived.volumeMusic() * EMBER_VOL);
};

const playEmber = () => {
	const howl = emberBed();
	applyEmberVolume();
	if (emberPlayId != null && howl.playing(emberPlayId)) return;
	if (emberPlayId != null && !howl.playing(emberPlayId)) {
		howl.play(emberPlayId);
		return;
	}
	emberPlayId = howl.play();
};

const pauseEmber = () => {
	if (!emberHowl) return;
	if (emberPlayId != null) emberHowl.pause(emberPlayId);
	else emberHowl.pause();
};

const stopEmber = () => {
	if (emberHowl) emberHowl.stop();
	emberPlayId = null;
};

export const preloadBonusBgm = () => {
	bed(BONUS_BGM_SMALL);
	bed(BONUS_BGM_SUPER);
	emberBed();
};

export const isBonusBgm = (name: string): name is BonusBgmName =>
	name === BONUS_BGM_SMALL || name === BONUS_BGM_SUPER;

export const musicForBonusTier = (tier: BonusEntryTier): BonusBgmName =>
	tier === 'superspins' || tier === 'bonus_super' ? BONUS_BGM_SUPER : BONUS_BGM_SMALL;

export const currentModeMusic = (): MusicName => active ?? 'bgm_main';

export const playBonusBgm = (name: BonusBgmName) => {
	if (active === name && playId != null && bed(name).playing(playId)) {
		applyVolume(bed(name));
		if (name === BONUS_BGM_SUPER) playEmber();
		else stopEmber();
		return;
	}
	if (active && active !== name) {
		bed(active).stop();
		playId = null;
		stopEmber();
	}
	const howl = bed(name);
	applyVolume(howl);
	if (playId != null && howl.playing(playId)) {
		active = name;
		if (name === BONUS_BGM_SUPER) playEmber();
		else stopEmber();
		return;
	}
	if (playId != null && !howl.playing(playId)) {
		howl.play(playId);
	} else {
		playId = howl.play();
	}
	active = name;
	if (name === BONUS_BGM_SUPER) playEmber();
	else stopEmber();
};

export const pauseBonusBgm = () => {
	if (!active) return;
	const howl = bed(active);
	if (playId != null) howl.pause(playId);
	else howl.pause();
	pauseEmber();
};

export const resumeBonusBgm = () => {
	if (!active) return;
	const howl = bed(active);
	applyVolume(howl);
	if (playId != null) {
		if (!howl.playing(playId)) howl.play(playId);
	} else if (!howl.playing()) {
		playId = howl.play();
	}
	if (active === BONUS_BGM_SUPER) playEmber();
};

export const stopBonusBgm = () => {
	if (active) bed(active).stop();
	active = null;
	playId = null;
	stopEmber();
};

export const syncBonusBgmVolume = () => {
	if (active) applyVolume(bed(active));
	applyEmberVolume();
};

/** Silence the looping bed (base or bonus) without losing its place. */
export const pauseModeBeds = () => {
	pauseBonusBgm();
	sound.players?.music.pause();
};

/** Pick the bed back up after a celebration plate. */
export const resumeModeBeds = () => {
	if (active) {
		resumeBonusBgm();
		return;
	}
	sound.players?.music.play({ name: 'bgm_main' });
};
