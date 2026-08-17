/**
 * BONUS-ENTRY TRIGGER — the one place that decides a banner is owed.
 *
 * `playBet` awaits this before it plays a single book event, which makes round
 * start the trigger: the banner announces the bought mode and the reels cannot
 * spin until it hands off. That is the whole reason the five overlays deleted
 * before this one were dead code — they declared events nothing broadcast and
 * were mounted nowhere, so no trigger existed at all.
 *
 * Why round start rather than a book event: the math emits nothing that marks a
 * bought round (a bonus book is an ordinary `reveal` with a livelier board), so
 * the only truth is the bet mode the player paid for, which is
 * `stateBet.activeBetModeKey` — set by ModalBuyBonusConfirm on confirm, and reset
 * to BASE by ButtonBetProvider / AutoSpinsStartButton / the space-hold guard the
 * moment the player takes a normal spin.
 */
import { stateBet } from 'state-shared';

import { eventEmitter } from './eventEmitter';
import { musicForBonusTier } from './bonusBgm';
import { bonusEntryTierOf } from './bonusEntryArt';
import { atmosphereFromMode, syncAtmosphere } from './atmosphere.svelte';
import type { Bet } from './typesBookEvent';

/**
 * Show the bonus-entry banner if this round is a bought bonus, and resolve when
 * it hands off to the spin.
 *
 * NON-BLOCKING BY CONSTRUCTION: `broadcastAsync` resolves immediately when no
 * BonusEntry is subscribed (loading screen still up, or a story that never
 * mounts Game), and BonusEntry itself resolves immediately if its hero plate did
 * not load. A base spin returns before touching the bus at all.
 */
export const presentBonusEntry = async (bet: Bet) => {
	const tier = bonusEntryTierOf(stateBet.activeBetModeKey);
	if (tier === null) return;
	syncAtmosphere(atmosphereFromMode(tier) ?? 'small');

	// A RESUMED round is already in flight — the player saw the banner when they
	// bought it, and its first book event is the snapshot that rebuilds state, so
	// announcing the buy again here would be a second entry for one purchase.
	if (bet.state[0]?.type === 'createBonusSnapshot') return;

	eventEmitter.broadcast({ type: 'soundMusic', name: musicForBonusTier(tier) });
	await eventEmitter.broadcastAsync({ type: 'bonusEntryShow', tier });
};
