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

export const playExternalOnce = (src: string, options?: { volume?: number; forcePlay?: boolean }) => {
	const howl = getHowl(src);
	howl.volume((options?.volume ?? 1) * stateSoundDerived.volumeSoundEffect());
	if (!options?.forcePlay) howl.stop();
	howl.play();
};

export const unloadExternalSounds = () => {
	howlMap.forEach((howl) => howl.unload());
	howlMap.clear();
};
