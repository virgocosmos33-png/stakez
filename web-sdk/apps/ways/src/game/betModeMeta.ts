import type { BetModeMeta } from 'state-shared';

/**
 * Madam Mirror bet modes. Keys must match the math engine's bet mode ids
 * (games/0_1_madam_mirror/game_config.py): base / bonus1 / bonus2 / bonus3.
 * The buy menu renders `assets.icon` as the card art.
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
	bonus1: {
		mode: 'bonus1',
		costMultiplier: 100,
		type: 'buy',
		parent: '',
		children: '',
		assets: {
			icon: '/assets/sprites/mirror/buy_seance.webp',
			volatility: '',
			button: '/assets/sprites/mirror/buy_seance.webp',
			dialogImage: '/assets/sprites/mirror/intro_seance.webp',
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
			icon: '/assets/sprites/mirror/buy_otherside.webp',
			volatility: '',
			button: '/assets/sprites/mirror/buy_otherside.webp',
			dialogImage: '/assets/sprites/mirror/intro_otherside.webp',
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
			icon: '/assets/sprites/mirror/buy_bloodmoon.webp',
			volatility: '',
			button: '/assets/sprites/mirror/buy_bloodmoon.webp',
			dialogImage: '/assets/sprites/mirror/intro_bloodmoon.webp',
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
