/**
 * stake.us (social casino) language compliance.
 *
 * US requirements prohibit certain gambling terms (see Stake Engine docs:
 * Approval Guidelines > Jurisdiction Requirements). When the game is loaded
 * with ?social=true, display text must be rewritten with the suggested
 * replacement phrases. Order matters: longer phrases are replaced before the
 * single words they contain.
 */
const REPLACEMENTS: [RegExp, string][] = [
	[/\bbe awarded to player'?s accounts?\b/gi, "appear in player's accounts"],
	[/\bwin features\b/gi, 'play features'],
	[/\bwin feature\b/gi, 'play feature'],
	[/\bbuy[- ]bonus(es)?\b/gi, 'get bonus'],
	[/\bbonus buys\b/gi, 'bonus features'],
	[/\bbonus buy\b/gi, 'bonus feature'],
	[/\bfeature buys\b/gi, 'features'],
	[/\btotal bets?\b/gi, 'total play'],
	[/\bplaces? your bets?\b/gi, 'join in the game'],
	[/\bplaces a bet\b/gi, 'starts a play'],
	[/\bpaid out\b/gi, 'won'],
	[/\bpays out\b/gi, 'wins'],
	[/\bpay out\b/gi, 'win'],
	[/\bat the cost of\b/gi, 'for'],
	[/\bcost of\b/gi, 'can be played for'],
	[/\bbought\b/gi, 'instantly triggered'],
	[/\bbetting\b/gi, 'playing'],
	[/\bbets\b/gi, 'plays'],
	[/\bbet\b/gi, 'play'],
	[/\bbuys\b/gi, 'plays'],
	[/\bbuy\b/gi, 'play'],
	[/\bwagers?\b/gi, 'plays'],
	[/\bgambles?\b/gi, 'plays'],
	[/\bpurchases?\b/gi, 'plays'],
	[/\brebet\b/gi, 'respin'],
	[/\bpayer\b/gi, 'winner'],
	[/\bpaid\b/gi, 'won'],
	[/\bpays\b/gi, 'wins'],
	[/\bpay\b/gi, 'win'],
	[/\bcash\b/gi, 'coins'],
	[/\bmoney\b/gi, 'coins'],
	[/\bcosts?\b/gi, 'plays for'],
	// "Stake Engine" is a trademark and must stay intact (see disclaimer)
	[/\bstakes?\b(?!\s+engine)/gi, 'play amount'],
	[/\bcredits?\b/gi, 'coins'],
	[/\bdeposits?\b/gi, 'get coins'],
	[/\bwithdraws?\b/gi, 'redeem'],
	[/\bwithdrawals?\b/gi, 'redemptions'],
	[/\bcurrency\b/gi, 'token'],
	[/\bcurrencies\b/gi, 'tokens'],
];

/** Rewrite prohibited gambling terms for social casinos, preserving ALL-CAPS. */
export function socializeText(text: string): string {
	let result = text;
	for (const [pattern, replacement] of REPLACEMENTS) {
		result = result.replace(pattern, (match) =>
			match === match.toUpperCase() ? replacement.toUpperCase() : replacement,
		);
	}
	return result;
}

/** Identity unless social mode: convenience wrapper for display strings. */
export function socialText(text: string, social: boolean): string {
	return social ? socializeText(text) : text;
}
