import { Howl } from 'howler';

import { stateSoundDerived } from 'state-shared';

// One-shot for audio that ships outside the sprite (a single mp3 imported by a
// component). Howls are cached per src so repeated stings reuse one decode, and
// global mute still applies because Howler owns the master volume.
const howlMap = new Map<string, Howl>();

const getHowl = (src: string) => {
	const existingHowl = howlMap.get(src);
	if (existingHowl) return existingHowl;

	const howl = new Howl({ src: [src], preload: true });
	howlMap.set(src, howl);
	return howl;
};

export const preloadExternal = (src: string) => {
	getHowl(src);
};

export const playExternalOnce = (
	src: string,
	options?: { volume?: number; forcePlay?: boolean; durationMs?: number },
) => {
	const howl = getHowl(src);
	const start = () => {
		const fileMs = howl.duration() * 1000;
		const rate = options?.durationMs && fileMs > 0 ? fileMs / options.durationMs : 1;
		howl.loop(false);
		howl.rate(rate);
		howl.volume((options?.volume ?? 1) * stateSoundDerived.volumeSoundEffect());
		if (!options?.forcePlay) howl.stop();
		howl.play();
	};
	if (howl.state() === 'loaded') start();
	else howl.once('load', start);
};

const loopMap = new Map<string, Howl>();

const getLoopHowl = (src: string) => {
	const existing = loopMap.get(src);
	if (existing) return existing;
	const howl = new Howl({ src: [src], loop: true, preload: true });
	loopMap.set(src, howl);
	return howl;
};

export const playExternalLoop = (src: string, options?: { volume?: number }) => {
	const howl = getLoopHowl(src);
	howl.volume((options?.volume ?? 1) * stateSoundDerived.volumeSoundEffect());
	if (!howl.playing()) howl.play();
};

export const fadeExternal = (src: string, from: number, to: number, durationMs: number) => {
	const howl = loopMap.get(src) ?? howlMap.get(src);
	if (!howl) return false;
	const master = stateSoundDerived.volumeSoundEffect();
	howl.fade(from * master, to * master, durationMs);
	return true;
};

export const stopExternal = (src: string) => {
	howlMap.get(src)?.stop();
	loopMap.get(src)?.stop();
};

export const unloadExternalSounds = () => {
	howlMap.forEach((howl) => howl.unload());
	loopMap.forEach((howl) => howl.unload());
	howlMap.clear();
	loopMap.clear();
};
