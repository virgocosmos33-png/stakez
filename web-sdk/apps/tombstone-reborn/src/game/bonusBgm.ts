/**
 * Small / big bonus beds. Long loops stay as their own mp3s — they are not
 * packed into the SFX sprite (that atlas is for stings, not full songs).
 *
 *   bonusgame 1 bgm.mp3 → bgm_bonus_small  (freespins / bonus_small)
 *   bonusgame 2 bgm.mp3 → bgm_bonus_super  (superspins / bonus_super)
 */
import { Howl } from 'howler';

import { stateSoundDerived } from 'state-shared';

import type { BonusEntryTier } from './bonusEntryArt';
import type { MusicName } from './sound';

export const BONUS_BGM_SMALL = 'bgm_bonus_small' as const;
export const BONUS_BGM_SUPER = 'bgm_bonus_super' as const;

export type BonusBgmName = typeof BONUS_BGM_SMALL | typeof BONUS_BGM_SUPER;

const SRC: Record<BonusBgmName, string> = {
	bgm_bonus_small: '/assets/audio/bgm_bonus_small.mp3',
	bgm_bonus_super: '/assets/audio/bgm_bonus_super.mp3',
};

const howls = new Map<BonusBgmName, Howl>();
let active: BonusBgmName | null = null;

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

const applyVolume = (howl: Howl) => {
	howl.volume(stateSoundDerived.volumeMusic());
};

export const isBonusBgm = (name: string): name is BonusBgmName =>
	name === BONUS_BGM_SMALL || name === BONUS_BGM_SUPER;

export const musicForBonusTier = (tier: BonusEntryTier): BonusBgmName =>
	tier === 'superspins' || tier === 'bonus_super' ? BONUS_BGM_SUPER : BONUS_BGM_SMALL;

export const currentModeMusic = (): MusicName => active ?? 'bgm_main';

export const playBonusBgm = (name: BonusBgmName) => {
	if (active === name && bed(name).playing()) {
		applyVolume(bed(name));
		return;
	}
	if (active && active !== name) bed(active).stop();
	const howl = bed(name);
	applyVolume(howl);
	if (!howl.playing()) howl.play();
	active = name;
};

export const pauseBonusBgm = () => {
	if (active) bed(active).pause();
};

export const resumeBonusBgm = () => {
	if (!active) return;
	const howl = bed(active);
	applyVolume(howl);
	if (!howl.playing()) howl.play();
};

export const stopBonusBgm = () => {
	if (active) bed(active).stop();
	active = null;
};

export const syncBonusBgmVolume = () => {
	if (active) applyVolume(bed(active));
};
