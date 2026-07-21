// Single source of truth for the game's info / pay-table prose.
// Consumed by ModalPayTable.svelte (the info menu) AND the in-HUD info marquee
// so both always show the SAME copy. Do not duplicate these strings elsewhere.

export type SpecialSymbol = {
	key: string;
	name: string;
	desc: string;
};

export const SPECIALS: SpecialSymbol[] = [
	{
		key: 'w',
		name: 'Wild',
		desc: 'Substitutes for all paying symbols. Does not substitute for Scatter, Haunted Mirror or Madam\'s Eye.',
	},
	{
		key: 's',
		name: 'Scatter',
		desc: '3 / 4 / 5 Scatters trigger THE SÉANCE, THE OTHER SIDE or BLOOD MOON. During free spins, 2+ Scatters add +3 spins.',
	},
	{
		key: 'hm',
		name: 'Haunted Mirror',
		desc: 'Appears on reels 2–4. Bursts and reflects neighbouring symbols into split apparitions (×2–×4). Then resolves into the highest-paying neighbour.',
	},
	{
		key: 'me',
		name: "Madam's Eye",
		desc: 'Can only land when splits are in play. Converts every split symbol — and itself — into a Wild for that spin. Apparition counts are kept.',
	},
];

export type InfoSection = {
	title: string;
	body?: string;
	bullets?: string[];
	rows?: { label: string; value: string }[];
};

export const INFO_SECTIONS: InfoSection[] = [
	{
		title: 'GAME INFO',
		body: 'Madam Mirror is a 5-reel, 4-row video slot with 1024 ways to win and 14 symbols (5 highs, 5 lows, Wild, Scatter, Haunted Mirror, Madam\'s Eye). Wins pay left to right on adjacent reels from the leftmost reel, regardless of row.',
		bullets: [
			'All wins are shown as a multiplier of the total bet and are paid per way.',
			'Split apparitions count as multiple symbols on their reel, multiplying the number of ways.',
			'Only the highest win per way is paid. Simultaneous wins on different ways are added.',
		],
	},
	{
		title: 'WAYS PAYS',
		body: 'Matching symbols on adjacent reels from reel 1 create ways. With no splits the grid pays up to 1024 ways (4×4×4×4×4). Each split cell with apparition count m counts as m symbols on that reel, so ways can grow far beyond 1024 on a single spin.',
	},
	{
		title: 'HAUNTED MIRRORS',
		bullets: [
			'In the base game, mirrors can appear on roughly 1 in 7 spins, usually as a single mirror on reels 2–4.',
			'When a mirror bursts it reflects 1–6 neighbouring cells into split apparitions (2, 3 or 4 symbols each).',
			'The mirror then transforms into the highest-paying neighbour and can take part in wins.',
			'Multi-mirror base spins are rare and are the main path to the largest base-game wins.',
		],
	},
	{
		title: "MADAM'S EYE",
		bullets: [
			'A rare golden symbol that only drops when split symbols are already on the board (fresh burst or persistent haunt).',
			'Converts every split symbol into a Wild for that spin, keeping its apparition count.',
			'The Eye itself resolves into a Wild.',
			'Haunted-cell persistence is unchanged — the conversion lasts one spin only.',
		],
	},
	{
		title: 'FREE SPINS',
		body: 'Landing 3, 4 or 5 Scatters in the base game triggers one of three bonus levels. During any free-spin bonus, 2 or more Scatters award +3 extra spins.',
		rows: [
			{ label: '3 Scatters — THE SÉANCE', value: '8 free spins' },
			{ label: '4 Scatters — THE OTHER SIDE', value: '10 free spins' },
			{ label: '5 Scatters — BLOOD MOON', value: '12 free spins' },
		],
	},
	{
		title: 'THE SÉANCE',
		body: 'Level 1 free spins. Mirrors are much more common than in the base game (~40% of spins). Haunted cells last for the spin they are created. Re-hitting a haunted cell keeps the higher apparition count but does not stack further.',
	},
	{
		title: 'THE OTHER SIDE',
		body: 'Level 2 free spins. Mirror chance ~45%. Haunted cells survive one extra spin and can stack: new bursts add apparitions with no cap and refresh the cell\'s lifetime.',
	},
	{
		title: 'BLOOD MOON',
		body: 'Level 3 free spins. Mirror chance ~50%. Haunted cells are sticky for the entire bonus and stack freely — the longest, densest hauntings in the game.',
	},
	{
		title: 'EXTRA BET & FEATURE SPINS',
		body: 'These modes stay active until you turn them off. Every spin is charged at the listed cost and uses the mode rules:',
		rows: [
			{ label: 'EXTRA BET — scatter on reel 1 every spin', value: '1.25× bet' },
			{ label: 'MIRROR SPIN — 1+ Haunted Mirror every spin', value: '10× bet' },
			{ label: 'TWIN MIRRORS — 2+ Haunted Mirrors every spin', value: '20× bet' },
			{ label: 'TRIPLE MIRRORS — 3 Haunted Mirrors every spin', value: '40× bet' },
		],
	},
	{
		title: 'BONUS BUYS',
		body: 'Bonus rounds can be bought directly from the menu:',
		rows: [
			{ label: 'THE SÉANCE (3 Scatters)', value: '100× bet' },
			{ label: 'THE OTHER SIDE (4 Scatters)', value: '400× bet' },
			{ label: 'BLOOD MOON (5 Scatters)', value: '1000× bet' },
		],
	},
	{
		title: 'RETURN TO PLAYER (RTP)',
		body: 'Theoretical RTP by mode (long-term expected return):',
		rows: [
			{ label: 'Main game', value: '96.20%' },
			{ label: 'EXTRA BET', value: '96.20%' },
			{ label: 'MIRROR SPIN', value: '96.50%' },
			{ label: 'TWIN MIRRORS', value: '96.50%' },
			{ label: 'TRIPLE MIRRORS', value: '96.50%' },
			{ label: 'THE SÉANCE buy', value: '96.50%' },
			{ label: 'THE OTHER SIDE buy', value: '96.60%' },
			{ label: 'BLOOD MOON buy', value: '96.65%' },
		],
	},
	{
		title: 'MAX WIN',
		body: 'The maximum win is 30,000× the bet in all modes. Once the cap is reached the round ends immediately.',
	},
	{
		title: 'USER INTERFACE',
		bullets: [
			'Menu (≡) — opens this pay table, game rules and sound settings.',
			'Coins — opens the bet amount menu to change the bet size.',
			'Speaker — mutes or unmutes all game sounds.',
			'Arrow (▶) — places a bet and spins the reels. Spacebar does the same.',
			'Circular arrows — autoplay: choose a number of spins and confirm to start; press again to stop.',
			'Lightning bolt — toggles turbo mode for faster spins.',
			'BONUS — opens the bonus / feature menu (buys and activate modes).',
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
