/**
 * Scene-space seats from backgroundSPINE/spine-scene MAIN_FRAME.
 * Canvas 1342×892 (1×), scaled ×2 into SCENE_ART 2684×1784.
 * Plaques = extracted layer pixels (box + pallet). Lamps stay Spine — nails only.
 */
export const FRAME_SEATS = {
	source: "C:\\Users\\Emex33\\Documents\\fire frame vfx\\backgroundSPINE\\spine-scene",
	psd: { width: 1342, height: 892 },
	scale: 2,
	board: { left: 620, top: 272, right: 2070, bottom: 1496 },
	/** Interior hole of MAIN_FRAME at 2×. */
	pocket: { left: 750, top: 374, right: 1966, bottom: 1392 },
	/** Stepped hole bands in SCENE_ART (one connected island, not 6 separate windows). */
	holeColumns: [
		{ id: 'r0', rows: 3, left: 750, top: 504, right: 956, bottom: 1256 },
		{ id: 'r12', rows: 4, left: 956, top: 376, right: 1346, bottom: 1390 },
		{ id: 'r34', rows: 2, left: 1356, top: 634, right: 1760, bottom: 1128 },
		{ id: 'r5', rows: 1, left: 1760, top: 762, right: 1966, bottom: 1000 },
	],
	beam: { left: 36, top: 106, right: 2658, bottom: 258 },
	chains: [
		{ id: "hang-0", left: 698, top: 186, right: 730, bottom: 488 },
		{ id: "hang-1", left: 906, top: 182, right: 938, bottom: 326 },
		{ id: "hang-2", left: 1372, top: 186, right: 1404, bottom: 326 }
	],
	lamps: {
		L: {
			hangX: 258,
			hangY: 146,
			left: 196,
			top: 146,
			right: 320,
			bottom: 610,
		},
		R: {
			hangX: 2438,
			hangY: 146,
			left: 2376,
			top: 146,
			right: 2500,
			bottom: 610,
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
