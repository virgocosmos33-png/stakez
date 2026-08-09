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
		key: 'split_gang',
		name: 'Gang Split',
		desc: 'A bar card that splits EVERY premium character on the board: each one gains +1 to +10 extra ways. The dead multiply.',
	},
	{
		key: 'split_outlaws',
		name: 'Outlaw Split',
		desc: 'A bar card that splits EVERY low symbol on the board: each one gains +1 to +10 extra ways.',
	},
	{
		key: 'gunsmoke',
		name: 'Gunsmoke',
		desc: 'A bar card that turns every copy of one symbol type into the revolver WILD. The smoke clears and only gun metal remains.',
	},
	{
		key: 'digup',
		name: 'Dig Up',
		desc: 'A bar card that cracks open the sealed LAST-REEL LANE for the current spin — even in the base game. Whatever is buried there joins the board.',
	},
	{
		key: 'coffin',
		name: 'Tombstone Open',
		desc: 'A bar card that grows short reels taller, revealing extra buried symbols and multiplying the ways.',
	},
	{
		key: 'bounty',
		name: 'Bounty',
		desc: 'The unlocked last-reel lane can drop a random premium carrying a WIN multiplier (×2 up to ×100) that multiplies the WHOLE spin win.',
	},
	{
		key: 'nudge',
		name: 'Horizontal Nudge',
		desc: 'A bounty premium can NUDGE left across the board, climbing its WIN multiplier for every premium it passes — and leaving each one as a WILD.',
	},
	{
		key: 'supersplit',
		name: 'Supersplit',
		desc: 'SUPER BONUS only: the last reel turns fully WILD and EVERY paying symbol on the board splits at once.',
	},
];

export const WHITE_ROOM_INFO_SECTIONS: InfoSection[] = [
	{
		title: 'GAME INFO',
		body: 'TOMBSTONE REBORN is a 6-reel ways slot on a broken-grave grid (3/4/4/2/2/1 rows) with 10 paying symbols (5 highs, 5 lows) plus the revolver Wild and the special bar cards. Wins are awarded strictly left to right on adjacent columns, regardless of row.',
		bullets: [
			'All wins are shown as a multiplier of the total bet and are awarded per way.',
			'Cells carrying extra ways (splits) count as multiple symbols on their reel, multiplying the number of ways.',
			'Only the highest win per way counts. Simultaneous wins on different ways are added.',
			'This game is EXTREMELY volatile: most spins return nothing at all, and the pay comes from the rare spins where the features stack.',
		],
	},
	{
		title: 'THE SPECIAL BAR',
		body: 'Six sealed cells run along the top of the board, one over each reel. In the base game each cell has a very small chance to flip a card that really fires; in the bonuses the bar is fully awake. Cards fire one at a time, left to right, so a later card lands on a board an earlier card already changed.',
		bullets: [
			'GANG SPLIT — every premium on the board gains extra ways.',
			'OUTLAW SPLIT — every low on the board gains extra ways.',
			'GUNSMOKE — every copy of one symbol type becomes the revolver WILD.',
			'DIG UP — the sealed last-reel lane cracks open for this spin.',
			'TOMBSTONE OPEN — short reels grow taller, revealing buried symbols.',
		],
	},
	{
		title: 'THE LAST-REEL LANE',
		body: 'The sixth reel is a single sealed grave cell. It opens through DIG UP, or on every spin of the SUPER BONUS. An open lane can drop:',
		bullets: [
			'BOUNTY — a random premium carrying a WIN multiplier (×2 to ×100) on the whole spin.',
			'NUDGE — the bounty premium slides left, climbing its WIN multiplier for every premium it passes and leaving each as a WILD.',
			'SUPERSPLIT (Super Bonus only) — the lane turns WILD and every paying symbol on the board splits.',
		],
	},
	{
		title: 'BONUSES',
		body: 'Both bonuses are a SINGLE enhanced spin, not a set of free spins:',
		rows: [
			{ label: 'SMALL BONUS — special bar fully awake', value: '80× bet' },
			{ label: 'SUPER BONUS — bar awake + last lane open + Supersplit', value: '1,000× bet' },
		],
		bullets: [
			'The SMALL BONUS returns exactly 0 on about 40% of spins — and can, very rarely, reach the max win.',
			'The SUPER BONUS returns less than it plays for most of the time; the top of its range reaches the max win.',
		],
	},
	{
		title: 'RETURN TO PLAYER (RTP)',
		body: 'Theoretical RTP by mode (long-term expected return):',
		rows: [
			{ label: 'Main game', value: '96.50%' },
			{ label: 'SMALL BONUS', value: '96.50%' },
			{ label: 'SUPER BONUS', value: '96.50%' },
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
