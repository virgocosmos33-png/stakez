/**
 * Small / big bonus beds. Long loops stay as their own mp3s — they are not
 * packed into the SFX sprite (that atlas is for stings, not full songs).
 *
 *   Tombstone Showdown → bgm_bonus_small  (freespins / bonus_small)
 *   Desert Standoff    → bgm_bonus_super  (superspins / bonus_super)
 *   ember.mp3          → layered under bgm_bonus_super only
 *   bonus wait screen  → bgm_bonus_wait_small  (banner, PRESS ANYWHERE)
 *   super bonus wait   → bgm_bonus_wait_super  (super banner wait)
 */
import { Howl } from 'howler';

import { stateSoundDerived } from 'state-shared';

import { setBaseAmbientCelebHold } from './baseAmbientSfx';
import type { BonusEntryTier } from './bonusEntryArt';
import { sound, type MusicName } from './sound';

export const BONUS_BGM_SMALL = 'bgm_bonus_small' as const;
export const BONUS_BGM_SUPER = 'bgm_bonus_super' as const;
export const BONUS_WAIT_SMALL = 'bgm_bonus_wait_small' as const;
export const BONUS_WAIT_SUPER = 'bgm_bonus_wait_super' as const;

export type BonusBgmName = typeof BONUS_BGM_SMALL | typeof BONUS_BGM_SUPER;
export type BonusWaitName = typeof BONUS_WAIT_SMALL | typeof BONUS_WAIT_SUPER;

const SRC: Record<BonusBgmName, string> = {
	bgm_bonus_small: '/assets/audio/bgm_bonus_small.mp3',
	bgm_bonus_super: '/assets/audio/bgm_bonus_super.mp3',
};

const WAIT_SRC: Record<BonusWaitName, string> = {
	bgm_bonus_wait_small: '/assets/audio/bgm_bonus_wait_small.mp3?v=tr20',
	bgm_bonus_wait_super: '/assets/audio/bgm_bonus_wait_super.mp3?v=tr20',
};

const EMBER_SRC = '/assets/audio/bgm_super_ember.mp3';
/** Sit under the super score so both beds read, not one drown. */
const EMBER_VOL = 0.62;

const howls = new Map<BonusBgmName, Howl>();
const waitHowls = new Map<BonusWaitName, Howl>();
let active: BonusBgmName | null = null;
let waitActive: BonusWaitName | null = null;
/** Which bed a celebration should return to. Cleared when the bonus ends so
 * a win plate cannot bring Tombstone Showdown / Desert Standoff back. */
let desired: BonusBgmName | null = null;
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

const waitBed = (name: BonusWaitName) => {
	const existing = waitHowls.get(name);
	if (existing) return existing;
	const howl = new Howl({
		src: [WAIT_SRC[name]],
		loop: true,
		preload: true,
		html5: true,
	});
	waitHowls.set(name, howl);
	return howl;
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
	waitBed(BONUS_WAIT_SMALL);
	waitBed(BONUS_WAIT_SUPER);
};

export const waitMusicForBonusTier = (tier: BonusEntryTier): BonusWaitName =>
	tier === 'superspins' || tier === 'bonus_super' ? BONUS_WAIT_SUPER : BONUS_WAIT_SMALL;

export const playBonusWait = (tier: BonusEntryTier) => {
	const name = waitMusicForBonusTier(tier);
	setBaseAmbientCelebHold(true);
	pauseBonusBgm();
	sound.players?.music.pause();
	if (waitActive && waitActive !== name) waitBed(waitActive).stop();
	const howl = waitBed(name);
	howl.volume(stateSoundDerived.volumeMusic());
	if (waitActive === name && howl.playing()) return;
	howl.seek(0);
	howl.play();
	waitActive = name;
};

export const stopBonusWait = () => {
	for (const howl of waitHowls.values()) howl.stop();
	waitActive = null;
	setBaseAmbientCelebHold(false);
};

export const syncBonusWaitVolume = () => {
	if (waitActive) waitBed(waitActive).volume(stateSoundDerived.volumeMusic());
};

export const isBonusBgm = (name: string): name is BonusBgmName =>
	name === BONUS_BGM_SMALL || name === BONUS_BGM_SUPER;

export const musicForBonusTier = (tier: BonusEntryTier): BonusBgmName =>
	tier === 'superspins' || tier === 'bonus_super' ? BONUS_BGM_SUPER : BONUS_BGM_SMALL;

export const currentModeMusic = (): MusicName => desired ?? active ?? 'bgm_main';

const playBaseMusic = () => {
	const music = sound.players?.music;
	if (!music) return;
	// The sprite player no-ops play() when it still thinks bgm_main is
	// running. After a bonus we paused it — stop first so play is a new start.
	music.stop({ name: 'bgm_main' });
	music.play({ name: 'bgm_main' });
};

export const playBonusBgm = (name: BonusBgmName) => {
	stopBonusWait();
	desired = name;
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
	const name = desired ?? active;
	if (!name) return;
	if (!active) {
		playBonusBgm(name);
		return;
	}
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
	stopBonusWait();
	for (const howl of howls.values()) howl.stop();
	active = null;
	desired = null;
	playId = null;
	stopEmber();
};

/** Hard end: bonus + ember off, base bed starts from the top. */
export const restoreBaseMusic = () => {
	stopBonusBgm();
	playBaseMusic();
};

export const syncBonusBgmVolume = () => {
	if (active) applyVolume(bed(active));
	applyEmberVolume();
	syncBonusWaitVolume();
};

/** Silence the looping bed (base or bonus) without losing its place. */
export const pauseModeBeds = () => {
	setBaseAmbientCelebHold(true);
	pauseBonusBgm();
	sound.players?.music.pause();
};

/** Pick the bed back up after a celebration plate. */
export const resumeModeBeds = () => {
	setBaseAmbientCelebHold(false);
	if (desired) {
		resumeBonusBgm();
		return;
	}
	restoreBaseMusic();
};
