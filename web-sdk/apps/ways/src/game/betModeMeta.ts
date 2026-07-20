import type { BetModeMeta, BetModeData } from 'state-shared';
import { socializeText } from 'utils-shared/socialText';

/**
 * Madam Mirror bet modes. Keys must match the math engine's bet mode ids
 * (games/0_1_madam_mirror/game_config.py): base / bonus1 / bonus2 / bonus3.
 * The buy menu renders `assets.icon` as the card art.
 *
 * Asset URLs must be resolved relative to the module (like assets.ts does):
 * the game is served from a subdirectory on Stake Engine, so absolute
 * "/assets/..." paths 404 there.
 */
export const betModeMeta: BetModeMeta = {
	base: {
		mode: 'base',
		costMultiplier: 1.0,
		type: 'default',
		parent: '',
		children: '',
		assets: { icon: '', volatility: '', button: '', dialogImage: '', dialogVolatility: '' },
		text: {
			title: '',
			dialog: '',
			button: '',
			betAmountLabel: '',
			tickerIdle: '',
			tickerSpin: '',
		},
		maxWin: 30000,
	},
	ante: {
		mode: 'ante',
		costMultiplier: 1.25,
		type: 'activate',
		parent: '',
		children: '',
		assets: {
			icon: new URL('../../assets/sprites/mirror/buy_ante.webp', import.meta.url).href,
			volatility: '',
			button: new URL('../../assets/sprites/mirror/buy_ante.webp', import.meta.url).href,
			dialogImage: new URL('../../assets/sprites/mirror/buy_ante.webp', import.meta.url).href,
			dialogVolatility: '',
		},
		text: {
			title: 'EXTRA BET',
			dialog:
				'Play at 1.25x your bet: a Scatter is guaranteed on reel 1 every spin, DOUBLING your chance to trigger a bonus. Stays active until you turn it off.',
			description: 'A scatter on reel 1 every spin. Double bonus chance.',
			button: 'ACTIVATE',
			betAmountLabel: 'EXTRA BET',
			tickerIdle: 'EXTRA BET IS ACTIVE',
			tickerSpin: 'GOOD LUCK',
		},
		maxWin: 30000,
	},
	feature1: {
		mode: 'feature1',
		costMultiplier: 10,
		type: 'buy',
		parent: '',
		children: '',
		assets: {
			icon: new URL('../../assets/sprites/mirror/buy_feature1.webp', import.meta.url).href,
			volatility: '',
			button: new URL('../../assets/sprites/mirror/buy_feature1.webp', import.meta.url).href,
			dialogImage: new URL('../../assets/sprites/mirror/buy_feature1.webp', import.meta.url).href,
			dialogVolatility: '',
		},
		text: {
			title: 'MIRROR SPIN',
			dialog:
				'One spin with a guaranteed Haunted Mirror (or more). The mirror bursts and splits its neighbors into apparitions. Cost: 10x your bet.',
			description: 'One spin. 1+ Haunted Mirror guaranteed.',
			button: 'BUY',
			betAmountLabel: 'MIRROR SPIN',
			tickerIdle: 'MIRROR SPIN',
			tickerSpin: 'GOOD LUCK',
		},
		maxWin: 30000,
	},
	feature2: {
		mode: 'feature2',
		costMultiplier: 20,
		type: 'buy',
		parent: '',
		children: '',
		assets: {
			icon: new URL('../../assets/sprites/mirror/buy_feature2.webp', import.meta.url).href,
			volatility: '',
			button: new URL('../../assets/sprites/mirror/buy_feature2.webp', import.meta.url).href,
			dialogImage: new URL('../../assets/sprites/mirror/buy_feature2.webp', import.meta.url).href,
			dialogVolatility: '',
		},
		text: {
			title: 'TWIN MIRRORS',
			dialog:
				'One spin with 2 or more guaranteed Haunted Mirrors bursting together. Cost: 20x your bet.',
			description: 'One spin. 2+ Haunted Mirrors guaranteed.',
			button: 'BUY',
			betAmountLabel: 'TWIN MIRRORS',
			tickerIdle: 'TWIN MIRRORS',
			tickerSpin: 'GOOD LUCK',
		},
		maxWin: 30000,
	},
	feature3: {
		mode: 'feature3',
		costMultiplier: 40,
		type: 'buy',
		parent: '',
		children: '',
		assets: {
			icon: new URL('../../assets/sprites/mirror/buy_feature3.webp', import.meta.url).href,
			volatility: '',
			button: new URL('../../assets/sprites/mirror/buy_feature3.webp', import.meta.url).href,
			dialogImage: new URL('../../assets/sprites/mirror/buy_feature3.webp', import.meta.url).href,
			dialogVolatility: '',
		},
		text: {
			title: 'TRIPLE MIRRORS',
			dialog:
				'One spin with 3 guaranteed Haunted Mirrors - the full set, the base game path to the biggest wins. Cost: 40x your bet.',
			description: 'One spin. 3 Haunted Mirrors guaranteed.',
			button: 'BUY',
			betAmountLabel: 'TRIPLE MIRRORS',
			tickerIdle: 'TRIPLE MIRRORS',
			tickerSpin: 'GOOD LUCK',
		},
		maxWin: 30000,
	},
	bonus1: {
		mode: 'bonus1',
		costMultiplier: 100,
		type: 'buy',
		parent: '',
		children: '',
		assets: {
			icon: new URL('../../assets/sprites/mirror/buy_seance.webp', import.meta.url).href,
			volatility: '',
			button: new URL('../../assets/sprites/mirror/buy_seance.webp', import.meta.url).href,
			dialogImage: new URL('../../assets/sprites/mirror/intro_seance.webp', import.meta.url).href,
			dialogVolatility: '',
		},
		text: {
			title: 'THE SÉANCE',
			dialog:
				'Buy an 8-spin bonus at level 1: THE SÉANCE. Haunted cells persist across spins, holding their apparitions. Cost: 100x your bet.',
			description: '8 free spins. Haunted cells persist between spins.',
			button: 'BUY',
			betAmountLabel: 'THE SÉANCE',
			tickerIdle: 'THE SÉANCE',
			tickerSpin: 'GOOD LUCK',
		},
		maxWin: 30000,
	},
	bonus2: {
		mode: 'bonus2',
		costMultiplier: 400,
		type: 'buy',
		parent: '',
		children: '',
		assets: {
			icon: new URL('../../assets/sprites/mirror/buy_otherside.webp', import.meta.url).href,
			volatility: '',
			button: new URL('../../assets/sprites/mirror/buy_otherside.webp', import.meta.url).href,
			dialogImage: new URL('../../assets/sprites/mirror/intro_otherside.webp', import.meta.url).href,
			dialogVolatility: '',
		},
		text: {
			title: 'THE OTHER SIDE',
			dialog:
				'Buy a 10-spin bonus at level 2: THE OTHER SIDE. Haunted cells persist AND deepen — every win through a haunted cell adds another apparition, up to 4. Cost: 400x your bet.',
			description: '10 free spins. Haunted cells persist and deepen on wins.',
			button: 'BUY',
			betAmountLabel: 'THE OTHER SIDE',
			tickerIdle: 'THE OTHER SIDE',
			tickerSpin: 'GOOD LUCK',
		},
		maxWin: 30000,
	},
	bonus3: {
		mode: 'bonus3',
		costMultiplier: 1000,
		type: 'buy',
		parent: '',
		children: '',
		assets: {
			icon: new URL('../../assets/sprites/mirror/buy_bloodmoon.webp', import.meta.url).href,
			volatility: '',
			button: new URL('../../assets/sprites/mirror/buy_bloodmoon.webp', import.meta.url).href,
			dialogImage: new URL('../../assets/sprites/mirror/intro_bloodmoon.webp', import.meta.url).href,
			dialogVolatility: '',
		},
		text: {
			title: 'BLOOD MOON',
			dialog:
				'Buy a 12-spin bonus at level 3: BLOOD MOON. Persistence and deepening, 4 pre-haunted cells with 2 apparitions each, and a guaranteed mirror every spin. Cost: 1,000x your bet.',
			description: '12 free spins. Starts pre-haunted. A mirror bursts every spin.',
			button: 'BUY',
			betAmountLabel: 'BLOOD MOON',
			tickerIdle: 'BLOOD MOON',
			tickerSpin: 'GOOD LUCK',
		},
		maxWin: 30000,
	},
};

/** Bet modes with stake.us-compliant wording when the game runs in social mode. */
export function getBetModeMeta(social: boolean): BetModeMeta {
	if (!social) return betModeMeta;
	const socialized: BetModeMeta = {};
	for (const [key, mode] of Object.entries(betModeMeta)) {
		const text = Object.fromEntries(
			Object.entries(mode.text).map(([k, v]) => [k, typeof v === 'string' ? socializeText(v) : v]),
		) as BetModeData['text'];
		socialized[key] = { ...mode, text };
	}
	return socialized;
}
