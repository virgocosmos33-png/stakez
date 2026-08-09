// TOMBSTONE REBORN - frontend game config (MAIN GAME ONLY).
// Mirror of math-sdk/games/0_3_tombstone_reborn/game_config.py. The math build
// also writes an authoritative copy to
// library/configs/config_fe_0_3_tombstone_reborn.json.
// Free spins / scatter / bonus buys arrive in the feature pass.
export default {
	providerName: 'dramastudios',
	gameName: 'tombstone_reborn',
	gameID: '0_3_tombstone_reborn',
	rtp: 0.965,
	numReels: 6,
	numRows: [3, 4, 4, 2, 2, 1],
	betModes: {
		base: { cost: 1.0, feature: false, buyBonus: false, rtp: 0.965, max_win: 2000 },
	},
	symbols: {
		// The revolver. Substitutes for every paying symbol; pays on its own
		// only as a full six-reel wild line ((6,'W') in the math paytable).
		W: {
			paytable: [{ '6': 5.0 }],
			special_properties: ['wild'],
		},
		// H1 The Gunslinger, H2 The Duchess, H3 The Butcher,
		// H4 The Card Shark, H5 The Preacher
		H1: { paytable: [{ '6': 5.0 }, { '5': 1.5 }, { '4': 0.5 }, { '3': 0.2 }] },
		H2: { paytable: [{ '6': 3.0 }, { '5': 1.0 }, { '4': 0.4 }, { '3': 0.2 }] },
		H3: { paytable: [{ '6': 2.5 }, { '5': 0.8 }, { '4': 0.3 }, { '3': 0.1 }] },
		H4: { paytable: [{ '6': 2.0 }, { '5': 0.6 }, { '4': 0.3 }, { '3': 0.1 }] },
		H5: { paytable: [{ '6': 1.5 }, { '5': 0.5 }, { '4': 0.2 }, { '3': 0.1 }] },
		// L1 bullet, L2 whiskey, L3 spur, L4 horseshoe, L5 playing card
		L1: { paytable: [{ '6': 1.0 }, { '5': 0.4 }, { '4': 0.2 }, { '3': 0.1 }] },
		L2: { paytable: [{ '6': 1.0 }, { '5': 0.4 }, { '4': 0.2 }, { '3': 0.1 }] },
		L3: { paytable: [{ '6': 0.8 }, { '5': 0.3 }, { '4': 0.1 }, { '3': 0.1 }] },
		L4: { paytable: [{ '6': 0.8 }, { '5': 0.3 }, { '4': 0.1 }, { '3': 0.1 }] },
		L5: { paytable: [{ '6': 0.6 }, { '5': 0.2 }, { '4': 0.1 }, { '3': 0.1 }] },
	},
	paddingReels: {
		basegame: '',
		freegame: '',
	},
} as const;
