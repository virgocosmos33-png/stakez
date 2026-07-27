import type { BetModeMeta, BetModeData } from 'state-shared';
import { socializeText } from 'utils-shared/socialText';

/**
 * THE WHITE ROOM bet modes. Keys must match the math engine bet mode ids
 * (base / ante / bonus1–3). Buy menu uses `assets.icon` as card art.
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
			title: 'SCATTER',
			dialog:
				'Play at 1.25x your bet: a Scatter is guaranteed on reel 1 every spin, DOUBLING your chance to trigger a bonus. Stays active until you turn it off.',
			description: 'A scatter on reel 1 every spin. Double bonus chance.',
			button: 'ACTIVATE',
			betAmountLabel: 'SCATTER',
			tickerIdle: 'SCATTER IS ACTIVE',
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
			title: 'THE INTAKE',
			dialog:
				'Buy an 8-spin bonus at level 1: THE INTAKE. The BOTTOM cells unlock — every spin they drop premiums or a rising Wild Reel. Cost: 100x your bet.',
			description: '8 free spins. Bottom cells unlock (premiums + Wild Reels).',
			button: 'BUY',
			betAmountLabel: 'THE INTAKE',
			tickerIdle: 'THE INTAKE',
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
			title: 'HER SIDE',
			dialog:
				'Buy a 10-spin bonus at level 2: HER SIDE. The BOTTOM and RIGHT cells unlock, expanding the board to 6 reels for bigger ways wins. Cost: 400x your bet.',
			description: '10 free spins. Bottom + right unlock (6-wide board).',
			button: 'BUY',
			betAmountLabel: 'HER SIDE',
			tickerIdle: 'HER SIDE',
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
			title: 'WHITEOUT',
			dialog:
				'Buy a 12-spin bonus at level 3: WHITEOUT. BOTTOM, RIGHT and LEFT cells all unlock — the full 7-wide board with premiums and Wild Reels. Cost: 1,000x your bet.',
			description: '12 free spins. Full 7-wide board unlocks.',
			button: 'BUY',
			betAmountLabel: 'WHITEOUT',
			tickerIdle: 'WHITEOUT',
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
