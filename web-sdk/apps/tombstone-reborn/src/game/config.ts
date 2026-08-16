// TOMBSTONE REBORN live game config (mirrors math-sdk/games/0_3_tombstone_reborn
// game_config.py). Board: 6 reels, 3/4/4/2/2/1 rows, ways pays, 99,999x cap.
//
// NOTE: the legacy special symbol keys (STRETCH/SPLIT/CLONE/HM/ME/S) stay in
// `symbols` because SymbolName derives from these keys and the shared symbol
// renderer still carries entries for them — they never appear on the reels.
export default {
	providerName: 'dramastudios',
	gameName: 'tombstone_reborn',
	gameID: '0_3_tombstone_reborn',
	rtp: 0.965,
	numReels: 6,
	numRows: [3, 4, 4, 2, 2, 1],
	betModes: {
		base: {
			cost: 1.0,
			feature: true,
			buyBonus: false,
			rtp: 0.965,
			max_win: 99999,
		},
		bonus_small: {
			cost: 80.0,
			feature: false,
			buyBonus: true,
			rtp: 0.965,
			max_win: 99999,
		},
		bonus_super: {
			cost: 1000.0,
			feature: false,
			buyBonus: true,
			rtp: 0.965,
			max_win: 99999,
		},
		// BONUS ROUNDS (multi-spin, scatter-triggered, also buyable)
		freespins: {
			cost: 80.0,
			feature: false,
			buyBonus: true,
			rtp: 0.965,
			max_win: 99999,
		},
		superspins: {
			cost: 2000.0,
			feature: false,
			buyBonus: true,
			rtp: 0.965,
			max_win: 99999,
		},
	},
	symbols: {
		W: {
			paytable: [{ '6': 10 }],
			special_properties: ['wild'],
		},
		STRETCH: {
			paytable: null,
			special_properties: ['stretch'],
		},
		SPLIT: {
			paytable: null,
			special_properties: ['split'],
		},
		CLONE: {
			paytable: null,
			special_properties: ['clone'],
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
		SU: {
			paytable: null,
			special_properties: ['scatter'],
		},
		SP: {
			paytable: null,
			special_properties: ['feature'],
		},
		GS: {
			paytable: null,
			special_properties: ['feature'],
		},
		TS: {
			paytable: null,
			special_properties: ['feature'],
		},
		NW: {
			paytable: null,
			special_properties: ['feature'],
		},
		SG: {
			paytable: null,
			special_properties: ['feature'],
		},
		SO: {
			paytable: null,
			special_properties: ['feature'],
		},
		DU: {
			paytable: null,
			special_properties: ['feature'],
		},
		CF: {
			paytable: null,
			special_properties: ['feature'],
		},
		SH: {
			paytable: null,
			special_properties: ['feature'],
		},
		SS: {
			paytable: null,
			special_properties: ['feature'],
		},
		H1: {
			paytable: [{ '6': 5 }, { '5': 1.5 }, { '4': 0.5 }, { '3': 0.2 }],
		},
		H2: {
			paytable: [{ '6': 3 }, { '5': 1 }, { '4': 0.4 }, { '3': 0.2 }],
		},
		H3: {
			paytable: [{ '6': 2.5 }, { '5': 0.8 }, { '4': 0.3 }, { '3': 0.1 }],
		},
		H4: {
			paytable: [{ '6': 2 }, { '5': 0.6 }, { '4': 0.3 }, { '3': 0.1 }],
		},
		H5: {
			paytable: [{ '6': 1.5 }, { '5': 0.5 }, { '4': 0.2 }, { '3': 0.1 }],
		},
		L1: {
			paytable: [{ '6': 1 }, { '5': 0.4 }, { '4': 0.2 }, { '3': 0.1 }],
		},
		L2: {
			paytable: [{ '6': 1 }, { '5': 0.4 }, { '4': 0.2 }, { '3': 0.1 }],
		},
		L3: {
			paytable: [{ '6': 0.8 }, { '5': 0.3 }, { '4': 0.1 }, { '3': 0.1 }],
		},
		L4: {
			paytable: [{ '6': 0.8 }, { '5': 0.3 }, { '4': 0.1 }, { '3': 0.1 }],
		},
		L5: {
			paytable: [{ '6': 0.6 }, { '5': 0.2 }, { '4': 0.1 }, { '3': 0.1 }],
		},
	},
	paddingReels: {
		basegame: '',
		freegame: '',
		superspingame: '',
	},
};
