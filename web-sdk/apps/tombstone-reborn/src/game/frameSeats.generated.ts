/**
 * Scene-space seats from assets/spines/western_scene (Spine setup pose).
 * Canvas 1342×892 (1×), scaled ×2 into SCENE_ART.
 * Plaques / lamps / board follow the skeleton the user edited. Do not use placement.json.
 */
export const FRAME_SEATS = {
	source: "C:\\Users\\Emex33\\Documents\\tombstone reborn\\web-sdk\\apps\\tombstone-reborn\\assets\\spines\\western_scene",
	psd: { width: 1342, height: 892 },
	scale: 2,
	board: { left: 620, top: 272, right: 2070, bottom: 1496 },
	/** Interior hole of MAIN_FRAME at 2×. Tracks the board if that bone moved. */
	pocket: { left: 750, top: 374, right: 1966, bottom: 1392 },
	/** Stepped hole bands in SCENE_ART (one connected island, not 6 separate windows). */
	holeColumns: [
		{ id: 'r0', rows: 3, left: 750.0, top: 504.0, right: 956.0, bottom: 1256.0 },
		{ id: 'r12', rows: 4, left: 956.0, top: 376.0, right: 1346.0, bottom: 1390.0 },
		{ id: 'r34', rows: 2, left: 1356.0, top: 634.0, right: 1760.0, bottom: 1128.0 },
		{ id: 'r5', rows: 1, left: 1760.0, top: 762.0, right: 1966.0, bottom: 1000.0 }
	],
	beam: { left: 36, top: 106, right: 2658, bottom: 258 },
	chains: [
		{ id: "hang-0", left: 698.0, top: 186.0, right: 730.0, bottom: 488.0 },
		{ id: "hang-1", left: 906.0, top: 182.0, right: 938.0, bottom: 326.0 },
		{ id: "hang-2", left: 1372.0, top: 186.0, right: 1404.0, bottom: 326.0 }
	],
	lamps: {
		L: {
			hangX: 258.0,
			hangY: 146.0,
			left: 196.0,
			top: 146.0,
			right: 320.0,
			bottom: 610.0,
		},
		R: {
			hangX: 2438.0,
			hangY: 146.0,
			left: 2376.0,
			top: 146.0,
			right: 2500.0,
			bottom: 610.0,
		},
	},
	plaques: {
		ways: {
			box: { left: 1760, top: 302, right: 2062, bottom: 470 },
			pallet: { left: 1764, top: 282, right: 2050, bottom: 348 },
			well: { left: 1837, top: 350, right: 1974, bottom: 403 },
			chains: [
				{ id: "ways-0", key: "plaqueChainWays0", left: 1786, top: 186, right: 1818, bottom: 322 },
				{ id: "ways-1", key: "plaqueChainWays1", left: 1786, top: 426, right: 1818, bottom: 598 },
				{ id: "ways-2", key: "plaqueChainWays2", left: 1990, top: 428, right: 2022, bottom: 720 },
				{ id: "ways-3", key: "plaqueChainWays3", left: 1992, top: 186, right: 2024, bottom: 322 },
			],
		},
		multi: {
			box: { left: 1470, top: 302, right: 1772, bottom: 470 },
			pallet: { left: 1468, top: 282, right: 1760, bottom: 346 },
			well: { left: 1547, top: 348, right: 1684, bottom: 403 },
			chains: [
				{ id: "multi-0", key: "plaqueChainMulti0", left: 1500, top: 182, right: 1532, bottom: 320 },
				{ id: "multi-1", key: "plaqueChainMulti1", left: 1700, top: 186, right: 1732, bottom: 318 },
			],
		},
		win: {
			box: { left: 1470, top: 1294, right: 1772, bottom: 1460 },
			pallet: { left: 1468, top: 1264, right: 1758, bottom: 1322 },
			well: { left: 1538, top: 1322, right: 1690, bottom: 1398 },
			chains: [
				{ id: "win-0", key: "plaqueChainWin0", left: 1494, top: 1154, right: 1526, bottom: 1302 },
				{ id: "win-1", key: "plaqueChainWin1", left: 1704, top: 1154, right: 1736, bottom: 1302 },
			],
		},
		spins: {
			box: { left: 1774, top: 1294, right: 2076, bottom: 1460 },
			pallet: { left: 1776, top: 1260, right: 2050, bottom: 1326 },
			well: { left: 1842, top: 1326, right: 1994, bottom: 1398 },
			chains: [
				{ id: "spins-0", key: "plaqueChainSpins0", left: 1792, top: 1154, right: 1824, bottom: 1296 },
				{ id: "spins-1", key: "plaqueChainSpins1", left: 1992, top: 1030, right: 2024, bottom: 1302 },
			],
		},
	},
} as const;
