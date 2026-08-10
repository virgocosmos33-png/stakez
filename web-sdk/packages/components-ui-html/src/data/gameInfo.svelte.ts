// Single source of truth for the game's info / pay-table content.
// The package holds the shape only: each game installs its own copy at boot
// with setGameInfo(), and every consumer (the pay-table modal and the in-HUD
// info marquee) reads it from here so both always show identical text.

export type SpecialSymbol = {
	key: string;
	name: string;
	desc: string;
};

export type InfoSection = {
	title: string;
	body?: string;
	bullets?: string[];
	rows?: { label: string; value: string }[];
};

/** `pays[i]` is the per-way pay (x bet) for `payTable.kinds[i]` of a kind */
export type PaySymbol = {
	key: string;
	name: string;
	pays: number[];
};

export type PayTable = {
	kinds: number[];
	highs: PaySymbol[];
	lows: PaySymbol[];
	/** wilds that pay on their own; may list fewer kinds than the paying symbols */
	wilds?: PaySymbol[];
	wildsNote?: string;
};

export const gameInfo = $state({
	specials: [] as SpecialSymbol[],
	sections: [] as InfoSection[],
	payTable: { kinds: [], highs: [], lows: [] } as PayTable,
});

export const setGameInfo = (
	specials: SpecialSymbol[],
	sections: InfoSection[],
	payTable: PayTable,
) => {
	gameInfo.specials = specials;
	gameInfo.sections = sections;
	gameInfo.payTable = payTable;
};

/** the section with this title, for consumers that surface a subset (marquee) */
export const getInfoSection = (title: string) =>
	gameInfo.sections.find((section) => section.title === title);
