import type { BetModeMeta, BetModeData } from 'state-shared';
import { socializeText } from 'utils-shared/socialText';

/**
 * TOMBSTONE REBORN bet modes. Keys must match the math engine bet mode ids
 * (base / bonus_small / bonus_super). Buy menu uses `assets.icon` as card art.
 *
 * `detail` is the RTP for that mode, and must agree with the RTP table in
 * gameInfo.ts — the two are read side by side.
 *
 * Asset URLs must be resolved relative to the module (like assets.ts does):
 * the game is served from a subdirectory on Stake Engine, so absolute
 * "/assets/..." paths 404 there. They also have to be plain string literals —
 * Vite only rewrites `new URL()` when it can read the path statically.
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
		maxWin: 99999,
	},
	bonus_small: {
		mode: 'bonus_small',
		costMultiplier: 80,
		type: 'buy',
		parent: '',
		children: '',
		assets: {
			icon: new URL('../../assets/sprites/tombstone/buy_small.png', import.meta.url).href,
			volatility: '',
			button: new URL('../../assets/sprites/tombstone/buy_small.png', import.meta.url).href,
			dialogImage: new URL('../../assets/sprites/tombstone/buy_small.png', import.meta.url).href,
			dialogVolatility: '',
		},
		text: {
			showTitle: true,
			detail: 'RTP 96.50%',
			title: 'SMALL BONUS',
			dialog:
				'One enhanced spin at 80x your bet: feature symbols drop on the board — Gang Split, Outlaw Split, Gunsmoke, Dig Up and Tombstone Open — then turn into wilds. Around 40% of these spins return exactly 0; the top of the range reaches the 99,999x max win.',
			description: 'One enhanced spin. Feature symbols drop on the board.',
			button: 'BUY',
			betAmountLabel: 'SMALL BONUS',
			tickerIdle: 'SMALL BONUS',
			tickerSpin: 'GOOD LUCK',
		},
		maxWin: 99999,
	},
	bonus_super: {
		mode: 'bonus_super',
		costMultiplier: 1000,
		type: 'buy',
		parent: '',
		children: '',
		assets: {
			icon: new URL('../../assets/sprites/tombstone/buy_super.png', import.meta.url).href,
			volatility: '',
			button: new URL('../../assets/sprites/tombstone/buy_super.png', import.meta.url).href,
			dialogImage: new URL('../../assets/sprites/tombstone/buy_super.png', import.meta.url).href,
			dialogVolatility: '',
		},
		text: {
			showTitle: true,
			detail: 'RTP 96.50%',
			title: 'SUPER BONUS',
			dialog:
				'One enhanced spin at 1,000x your bet: feature symbols drop on the board AND the sealed last-reel lane is open — premiums with stacked WIN multipliers, MARK (shoots every premium, +1 multi per hit), and SUPERSPLIT. Most of these spins return less than they play for; the top of the range reaches the 99,999x max win.',
			description: 'One enhanced spin. Last lane open: premiums, MARK, Supersplit.',
			button: 'BUY',
			betAmountLabel: 'SUPER BONUS',
			tickerIdle: 'SUPER BONUS',
			tickerSpin: 'GOOD LUCK',
		},
		maxWin: 99999,
	},
	freespins: {
		mode: 'freespins',
		costMultiplier: 80,
		type: 'buy',
		parent: '',
		children: '',
		assets: {
			icon: new URL('../../assets/sprites/tombstone/buy_freespins.png', import.meta.url).href,
			volatility: '',
			button: new URL('../../assets/sprites/tombstone/buy_freespins.png', import.meta.url).href,
			dialogImage: new URL('../../assets/sprites/tombstone/buy_freespins.png', import.meta.url)
				.href,
			dialogVolatility: '',
		},
		text: {
			showTitle: true,
			detail: 'RTP 96.50%',
			title: 'SMALL BONUS · 10 SPINS',
			dialog:
				'THE WAKE — 10 bonus spins at 80x your bet, triggered by 3 BONUS tombstones. Feature symbols drop on the board every spin. No retriggers, and the rounds are extremely volatile: most pay back less than they cost, the top of the range reaches the 99,999x max win. Around 1 in 100 rounds drops a SUPER tombstone mid-round and UPGRADES to the big bonus — the grave lane tears open for the rest and the spins top back up.',
			description: '10 bonus spins. Feature symbols drop on the board.',
			button: 'BUY',
			betAmountLabel: 'SMALL BONUS',
			tickerIdle: 'THE WAKE',
			tickerSpin: 'GOOD LUCK',
		},
		maxWin: 99999,
	},
	superspins: {
		mode: 'superspins',
		costMultiplier: 2000,
		type: 'buy',
		parent: '',
		children: '',
		assets: {
			icon: new URL('../../assets/sprites/tombstone/buy_superspins.png', import.meta.url).href,
			volatility: '',
			button: new URL('../../assets/sprites/tombstone/buy_superspins.png', import.meta.url).href,
			dialogImage: new URL('../../assets/sprites/tombstone/buy_superspins.png', import.meta.url)
				.href,
			dialogVolatility: '',
		},
		text: {
			showTitle: true,
			detail: 'RTP 96.50%',
			title: 'BIG BONUS · 10 SPINS',
			dialog:
				'THE RECKONING — 10 bonus spins at 2,000x your bet, triggered by 3 BONUS tombstones plus a SUPER tombstone. Feature symbols drop on the board AND the grave lane is torn open on every spin: premiums with stacked WIN multipliers, MARK (shoots every premium) and SUPERSPLIT. About 1 in 4 rounds pays more than it costs. No retriggers, brutally volatile; the top of the range reaches the 99,999x max win.',
			description: '10 bonus spins. Lane open: premiums, MARK, Supersplit. ~25% profitable.',
			button: 'BUY',
			betAmountLabel: 'BIG BONUS',
			tickerIdle: 'THE RECKONING',
			tickerSpin: 'GOOD LUCK',
		},
		maxWin: 99999,
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
