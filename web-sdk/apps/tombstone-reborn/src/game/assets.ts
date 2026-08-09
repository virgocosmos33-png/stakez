// TOMBSTONE REBORN asset registry (MAIN GAME ONLY).
//
// Single source of truth for every art/audio key the base game loads. The
// referenced files under ../../assets/ are the deliverables (see
// ASSET_CHECKLIST_TOMBSTONE_REBORN.md). Keys are stable; swap the files behind
// them as art lands. Feature assets (Gunslinger face rig, win cutscenes,
// Revenge Spins bg/music) are added in the feature pass.
const spineSrc = (folder: string, skeleton: string) => ({
	atlas: new URL(`../../assets/spines/${folder}/${folder}.atlas`, import.meta.url).href,
	skeleton: new URL(`../../assets/spines/${folder}/${skeleton}.json`, import.meta.url).href,
	scale: 1,
});
const spriteSrc = (file: string) => new URL(`../../assets/sprites/${file}`, import.meta.url).href;
const audioSrc = (file: string) => new URL(`../../assets/audio/${file}`, import.meta.url).href;

export default {
	// ---- Premium symbol spines (win + land + postwin animations) ----
	H1: { type: 'spine', src: spineSrc('tr_symbols', 'h1') }, // Gunslinger
	H2: { type: 'spine', src: spineSrc('tr_symbols', 'h2') }, // Duchess
	H3: { type: 'spine', src: spineSrc('tr_symbols', 'h3') }, // Butcher
	H4: { type: 'spine', src: spineSrc('tr_symbols', 'h4') }, // Card Shark
	H5: { type: 'spine', src: spineSrc('tr_symbols', 'h5') }, // Preacher
	L1: { type: 'spine', src: spineSrc('tr_symbols', 'l1') },
	L2: { type: 'spine', src: spineSrc('tr_symbols', 'l2') },
	L3: { type: 'spine', src: spineSrc('tr_symbols', 'l3') },
	L4: { type: 'spine', src: spineSrc('tr_symbols', 'l4') },
	L5: { type: 'spine', src: spineSrc('tr_symbols', 'l5') },

	// ---- Static symbol cards (reels + spin smear) ----
	'h1.webp': { type: 'sprite', src: spriteSrc('h1.webp') },
	'h2.webp': { type: 'sprite', src: spriteSrc('h2.webp') },
	'h3.webp': { type: 'sprite', src: spriteSrc('h3.webp') },
	'h4.webp': { type: 'sprite', src: spriteSrc('h4.webp') },
	'h5.webp': { type: 'sprite', src: spriteSrc('h5.webp') },
	'l1.webp': { type: 'sprite', src: spriteSrc('l1.webp') },
	'l2.webp': { type: 'sprite', src: spriteSrc('l2.webp') },
	'l3.webp': { type: 'sprite', src: spriteSrc('l3.webp') },
	'l4.webp': { type: 'sprite', src: spriteSrc('l4.webp') },
	'l5.webp': { type: 'sprite', src: spriteSrc('l5.webp') },
	'w.webp': { type: 'sprite', src: spriteSrc('w.webp') }, // revolver wild

	// ---- Background ----
	bgGraveyard: { type: 'sprite', src: spriteSrc('bg_graveyard.webp') },

	// ---- Audio ----
	musicBase: { type: 'audio', src: audioSrc('music_base.mp3') },
	sfxGunshot: { type: 'audio', src: audioSrc('sfx_gunshot.mp3') },
	sfxReelStop: { type: 'audio', src: audioSrc('sfx_reel_stop.mp3') },
} as const;
