// TOMBSTONE REBORN game info / pay-table prose. Installed over the shared
// defaults at boot via setGameInfo() - see Game.svelte. Consumed by
// ModalPayTable.svelte (info menu) AND InfoMarquee (HUD ticker).
//
// Wording note: avoid "pay"/"cost"/"buy" in running prose. The stake.us social
// rewriter maps pay->win and cost->"plays for", which mangles sentences like
// "Wins pay left to right". Phrase copy so it reads correctly in both skins.

import type { SpecialSymbol, InfoSection, PaySymbol } from 'components-ui-html';

// Per-way pays (x bet) mirroring math-sdk game_config.py paytable — 6 reels,
// so every symbol lists its 6 / 5 / 4 / 3 connection values.
export const WHITE_ROOM_PAY_KINDS = [6, 5, 4, 3];

export const WHITE_ROOM_HIGH_SYMBOLS: PaySymbol[] = [
	{ key: 'h1', name: 'The Gunslinger', pays: [5, 1.5, 0.5, 0.2] },
	{ key: 'h2', name: 'The Duchess', pays: [3, 1, 0.4, 0.2] },
	{ key: 'h3', name: 'The Butcher', pays: [2.5, 0.8, 0.3, 0.1] },
	{ key: 'h4', name: 'The Card Shark', pays: [2, 0.6, 0.3, 0.1] },
	{ key: 'h5', name: 'The Preacher', pays: [1.5, 0.5, 0.2, 0.1] },
];

export const WHITE_ROOM_LOW_SYMBOLS: PaySymbol[] = [
	{ key: 'l1', name: 'Bullet', pays: [1, 0.4, 0.2, 0.1] },
	{ key: 'l2', name: 'Whiskey', pays: [1, 0.4, 0.2, 0.1] },
	{ key: 'l3', name: 'Spur', pays: [0.8, 0.3, 0.1, 0.1] },
	{ key: 'l4', name: 'Horseshoe', pays: [0.8, 0.3, 0.1, 0.1] },
	{ key: 'l5', name: 'Dead Man\u2019s Hand', pays: [0.6, 0.2, 0.1, 0.1] },
];

export const WHITE_ROOM_SPECIALS: SpecialSymbol[] = [
	{
		key: 'w',
		name: 'Wild — The Revolver',
		desc: 'Substitutes for all paying symbols and takes part in their winning ways. Wilds never complete a way on their own — a way always needs at least one regular paying symbol. The one exception: Wilds connecting on EVERY column of the board count as a Wild connection worth 10× bet per way.',
	},
	{
		key: 's',
		name: 'Scatter — The Bonus Tombstone',
		desc: 'Pays nothing on its own and lands only in the base game. 3 BONUS tombstones trigger the SMALL BONUS: 10 bonus spins with feature symbols dropping on the board. A SUPER scatter as the 4th scatter triggers the BIG BONUS.',
	},
	{
		key: 'su',
		name: 'Super Scatter',
		desc: 'When it lands, the last-reel lane opens for that spin. On a base spin it is the 4th scatter and opens the BIG BONUS. During a small bonus it is the upgrade drop: the grave lane stays open for the rest of the round and the spins top back up.',
	},
	{
		key: 'split',
		name: 'Split',
		desc: 'Lands on the board, picks one symbol type and adds 2 to 7 extra ways to every copy of that type — extremely weighted toward 2. Adds +1 to the WIN multiplier, then turns into the revolver WILD.',
	},
	{
		key: 'gunsmoke',
		name: 'Gunsmoke',
		desc: 'Lands on the board, turns every copy of one symbol type into the revolver WILD, adding +1 to the WIN multiplier for each shot, then becomes a wild itself.',
	},
	{
		key: 'nudge',
		name: 'Nudge Ways',
		desc: 'Drops only on the 2nd or 3rd reel with 2 to 9 ways (extremely weighted toward 2). If it does not already fill the reel it nudges DOWN, doubling its ways and adding +1 to the WIN multiplier on every step. A full-reel drop keeps the initial ways with no doubling and no WIN tick.',
	},
	{
		key: 'shooter',
		name: 'Mark',
		desc: 'The open last-reel lane can drop MARK: it shoots every premium on the board and adds +1 to the WIN multiplier when it triggers, then becomes a wild.',
	},
	{
		key: 'supersplit',
		name: 'Supersplit',
		desc: 'The other last-reel special: the last reel turns WILD, EVERY paying symbol on the board splits at 2× / 5× / 10×, and the WIN multiplier goes up by +1. Then MARK/SUPERSPLIT become wilds.',
	},
];

export const WHITE_ROOM_INFO_SECTIONS: InfoSection[] = [
	{
		title: 'GAME INFO',
		body: 'TOMBSTONE REBORN is a 6-reel ways slot on a broken-grave grid (3/4/4/2/2/1 rows) with 10 paying symbols (5 highs, 5 lows) plus the revolver Wild and feature symbols that land on the board. Wins are awarded strictly left to right on adjacent columns, regardless of row.',
		bullets: [
			'All wins are shown as a multiplier of the total bet and are awarded per way.',
			'Cells carrying extra ways (splits, nudge stacks, last-reel premiums) count as multiple symbols on their reel, multiplying the number of ways.',
			'The HUD WIN multiplier is a separate stack. It starts at 1× and multiplies the whole spin after ways are counted.',
			'Only the highest win per way counts. Simultaneous wins on different ways are added.',
			'This game is EXTREMELY volatile: most spins return nothing at all, and the pay comes from the rare spins where the features stack.',
		],
	},
	{
		title: 'FEATURE SYMBOLS',
		body: 'Feature symbols land on the reel grid itself. After they fire they transform into the revolver WILD. In the base game they are rare; in the bonuses they drop much more often.',
		bullets: [
			'SPLIT — one symbol type on the board gains 2 to 7 extra ways, the WIN multiplier goes up by +1, then the card becomes a wild. If a NUDGE stack is already standing, the split also hits it and doubles its ways.',
			'GUNSMOKE — every remaining copy of one symbol type becomes the revolver WILD (+1 WIN multi per shot), then the card becomes a wild. It cannot shoot a NUDGE stack or any row the nudge already swallowed.',
			'NUDGE WAYS — fires first. Lands on the 2nd or 3rd reel and replaces every symbol from that cell down, doubling ways and adding +1 WIN multi on every step. A full-reel drop keeps the initial ways. Nothing is left below the totem for GUNSMOKE to shoot. A later SPLIT can land on that stack and double it again.',
		],
	},
	{
		title: 'THE LAST-REEL LANE',
		body: 'The sixth reel is a single sealed grave cell. It opens when a SUPER scatter lands, or on every spin of the SUPER BONUS / big bonus round. An open lane NEVER drops lows — only:',
		bullets: [
			'A PREMIUM carrying extra WAYS (×2 to ×100) on that cell — separate from the HUD WIN multiplier.',
			'MARK — shoots every premium on the board and adds +1 to the WIN multiplier when it triggers.',
			'SUPERSPLIT — the lane turns WILD, every symbol on the board splits at 2× / 5× / 10×, and the WIN multiplier goes up by +1.',
			'The WIN multiplier is sticky across SUPER / big-bonus spins and resets every SMALL bonus spin.',
		],
	},
	{
		title: 'BONUSES',
		body: 'Two single-spin buys and two 10-spin bonus rounds (scatter-triggered, also buyable).',
		rows: [
			{ label: 'SMALL BONUS — one spin, feature symbols on the board', value: '80× bet' },
			{ label: 'SUPER BONUS — one spin, last lane open (premiums / MARK / SUPERSPLIT)', value: '1,000× bet' },
			{ label: 'THE WAKE — 10 spins, feature symbols on the board', value: '80× bet' },
			{ label: 'THE RECKONING — 10 spins, last lane open; ~25% of rounds profitable', value: '2,000× bet' },
		],
		bullets: [
			'The SMALL BONUS returns exactly 0 on about 40% of spins — and can, very rarely, reach the max win.',
			'THE RECKONING is built so only about 1 in 4 rounds pays more than it costs.',
		],
	},
	{
		title: 'RETURN TO PLAYER (RTP)',
		body: 'Theoretical RTP by mode (long-term expected return):',
		rows: [
			{ label: 'Main game', value: '96.50%' },
			{ label: 'SMALL BONUS / THE WAKE', value: '96.50%' },
			{ label: 'SUPER BONUS / THE RECKONING', value: '96.50%' },
		],
	},
	{
		title: 'MAX WIN',
		body: 'The maximum win is 99,999× the bet in all modes. Once the cap is reached the round ends immediately. When it lands, the Gunslinger finally smiles.',
	},
	{
		title: 'USER INTERFACE',
		bullets: [
			'Menu (≡) — opens this game info, rules and sound settings.',
			'Coins — opens the bet amount menu to change the bet size.',
			'Speaker — mutes or unmutes all game sounds.',
			'Arrow (▶) — places a bet and spins the reels. Spacebar does the same.',
			'Circular arrows — autoplay: choose a number of spins and confirm to start; press again to stop.',
			'Lightning bolt — toggles turbo mode for faster spins.',
			'BONUS — opens the bonus menu (single-spin bonus buys).',
			'BET and BALANCE — show the current bet size and your balance.',
		],
	},
	{
		title: 'DISCLAIMER',
		bullets: [
			'Malfunction voids all wins and plays.',
			'A consistent internet connection is required. In the event of a disconnection, reload the game to finish any uncompleted rounds.',
			'The expected return is calculated over many plays.',
			'The game display is not representative of any physical device and is for illustrative purposes only.',
			'Winnings are settled according to the amount received from the Remote Game Server and not from events within the web browser.',
			'TM and \u00a9 2026 Stake Engine.',
		],
	},
];
