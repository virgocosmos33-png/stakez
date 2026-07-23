export default {
	providerName: 'dramastudios',
	gameName: 'madam_mirror',
	gameID: '0_1_madam_mirror',
	rtp: 0.965,
	numReels: 5,
	numRows: [4, 4, 4, 4, 4],
	betModes: {
		base: {
			cost: 1.0,
			feature: true,
			buyBonus: false,
			rtp: 0.965,
			max_win: 22222,
		},
		bonus1: {
			cost: 100.0,
			feature: false,
			buyBonus: true,
			rtp: 0.965,
			max_win: 22222,
		},
		bonus2: {
			cost: 400.0,
			feature: false,
			buyBonus: true,
			rtp: 0.965,
			max_win: 22222,
		},
		bonus3: {
			cost: 1000.0,
			feature: false,
			buyBonus: true,
			rtp: 0.965,
			max_win: 22222,
		},
	},
	// Paytable mirrors math-sdk game_config.py (pays per way x bet).
	// High symbols are the five characters, low symbols the playing-card ranks:
	//   H1 Lady Mirror, H2 The Wife, H3 The Man, H4 The Maiden, H5 The Dog
	//   L1 Ace, L2 King, L3 Queen, L4 Jack, L5 Ten
	symbols: {
		W: {
			paytable: null,
			special_properties: ['wild'],
		},
		HM: {
			paytable: null,
			special_properties: ['mirror'],
		},
		ME: {
			paytable: null,
			special_properties: ['eye'],
		},
		S: {
			paytable: null,
			special_properties: ['scatter'],
		},
		H1: {
			paytable: [{ '5': 10 }, { '4': 3 }, { '3': 1 }],
		},
		H2: {
			paytable: [{ '5': 5 }, { '4': 1.5 }, { '3': 0.6 }],
		},
		H3: {
			paytable: [{ '5': 4 }, { '4': 1.2 }, { '3': 0.5 }],
		},
		H4: {
			paytable: [{ '5': 3 }, { '4': 1 }, { '3': 0.4 }],
		},
		H5: {
			paytable: [{ '5': 2.5 }, { '4': 0.8 }, { '3': 0.3 }],
		},
		L1: {
			paytable: [{ '5': 1.2 }, { '4': 0.4 }, { '3': 0.2 }],
		},
		L2: {
			paytable: [{ '5': 1.2 }, { '4': 0.4 }, { '3': 0.2 }],
		},
		L3: {
			paytable: [{ '5': 0.8 }, { '4': 0.3 }, { '3': 0.1 }],
		},
		L4: {
			paytable: [{ '5': 0.8 }, { '4': 0.3 }, { '3': 0.1 }],
		},
		L5: {
			paytable: [{ '5': 0.8 }, { '4': 0.3 }, { '3': 0.1 }],
		},
	},
	paddingReels: {
		basegame: '',
		freegame: '',
		superspingame: '',
	},
};
