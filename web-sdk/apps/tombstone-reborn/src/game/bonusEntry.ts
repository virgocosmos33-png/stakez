/**
 * Resume-only bonus bed. The banner itself is NOT shown here.
 *
 * Bought 10-spin books start with a basegame trigger (scatters drop, wins
 * resolve, then `freeSpinTrigger`). The banner and the room grade wait for
 * that event — see bookEventHandlerMap.freeSpinTrigger. This helper only
 * restarts the bonus bed when the player is coming back mid-round, because
 * they already saw the banner when they bought.
 */
import { stateBet } from 'state-shared';

import { eventEmitter } from './eventEmitter';
import { musicForBonusTier } from './bonusBgm';
import { bonusEntryTierOf } from './bonusEntryArt';
import { atmosphereFromMode, syncAtmosphere } from './atmosphere.svelte';
import type { Bet } from './typesBookEvent';

export const presentBonusEntry = async (bet: Bet) => {
	if (bet.state[0]?.type !== 'createBonusSnapshot') return;

	const tier = bonusEntryTierOf(stateBet.activeBetModeKey);
	if (tier === null) return;

	syncAtmosphere(atmosphereFromMode(tier) ?? 'small');
	eventEmitter.broadcast({ type: 'soundMusic', name: musicForBonusTier(tier) });
};
