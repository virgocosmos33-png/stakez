import _ from 'lodash';

import { recordBookEvent, checkIsMultipleRevealEvents, type BookEventHandlerMap } from 'utils-book';
import { stateBet } from 'state-shared';
import { sequence } from 'utils-shared/sequence';
import { waitForTimeout } from 'utils-shared/wait';

import { eventEmitter } from './eventEmitter';
import { playBookEvent } from './utils';
import { winLevelMap, type WinLevel, type WinLevelData } from './winLevelMap';
import { getWinCelebration } from './winCelebrationMap';
import type { MusicName, SoundEffectName } from './sound';
import { stateGame, stateGameDerived } from './stateGame.svelte';
import type { BookEvent, BookEventOfType, BookEventContext } from './typesBookEvent';
import type { Position } from './types';

type WinSoundsData = {
	alias: string;
	type: string;
	sound: { sfx?: SoundEffectName; bgm?: MusicName };
};

const winLevelSoundsPlay = ({ winLevelData }: { winLevelData: WinSoundsData }) => {
	if (winLevelData?.alias === 'max') eventEmitter.broadcastAsync({ type: 'uiHide' });
	if (winLevelData?.sound?.sfx) {
		eventEmitter.broadcast({ type: 'soundOnce', name: winLevelData.sound.sfx });
	}
	if (winLevelData?.sound?.bgm) {
		eventEmitter.broadcast({ type: 'soundMusic', name: winLevelData.sound.bgm });
	}
	// no coin loop: the celebration has its own psychedelic sfx layer
};

const winLevelSoundsStop = () => {
	eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_bigwin_coinloop' });
	if (stateBet.activeBetModeKey === 'SUPERSPIN' || stateGame.gameType === 'freegame') {
		// check if SUPERSPIN, when finishing a bet.
		eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_freespin' });
	} else {
		eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_main' });
	}
	eventEmitter.broadcastAsync({ type: 'uiShow' });
};

const animateSymbols = async ({ positions }: { positions: Position[] }) => {
	eventEmitter.broadcast({ type: 'boardShow' });
	await eventEmitter.broadcastAsync({
		type: 'boardWithAnimateSymbols',
		symbolPositions: positions,
	});
};

export const bookEventHandlerMap: BookEventHandlerMap<BookEvent, BookEventContext> = {
	reveal: async (bookEvent: BookEventOfType<'reveal'>, { bookEvents }: BookEventContext) => {
		const isBonusGame = checkIsMultipleRevealEvents({ bookEvents });
		if (isBonusGame) {
			eventEmitter.broadcast({ type: 'stopButtonEnable' });
			recordBookEvent({ bookEvent });
		}

		eventEmitter.broadcast({ type: 'apparitionsHide' });
		eventEmitter.broadcast({ type: 'winCycleStop' });
		stateGame.gameType = bookEvent.gameType;

		// mirrors are not a symbol of their own: the cell lands as the symbol
		// it will become, trapped behind a glass overlay until the burst.
		// Look ahead to this reveal's mirrorBurst to dress those cells.
		let revealEvent = bookEvent;
		const eventIndex = bookEvents.indexOf(bookEvent);
		for (let i = eventIndex + 1; i >= 0 && i < bookEvents.length; i++) {
			const nextEvent = bookEvents[i];
			if (nextEvent.type === 'reveal') break;
			if (nextEvent.type === 'mirrorBurst') {
				const board = bookEvent.board.map((reel) => reel.map((rawSymbol) => ({ ...rawSymbol })));
				nextEvent.mirrors.forEach(({ mirror, mirrorBecomes }) => {
					board[mirror.reel][mirror.row] = { name: mirrorBecomes.name, glass: true };
				});
				revealEvent = { ...bookEvent, board };
				break;
			}
		}

		await stateGameDerived.enhancedBoard.spin({ revealEvent });
		eventEmitter.broadcast({ type: 'soundScatterCounterClear' });
		// persistent haunted cells arrive on the reveal board via the multiplier attribute
		eventEmitter.broadcast({ type: 'apparitionsRefresh' });
	},
	winInfo: async (bookEvent: BookEventOfType<'winInfo'>) => {
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_winlevel_small' });
		await sequence(bookEvent.wins, async (win) => {
			// non-winning symbols dim so only the connecting combination pops;
			// a golden sweep runs left-to-right over it while any haunted cells
			// in the combination grow
			eventEmitter.broadcast({ type: 'winDimShow', positions: win.positions });
			eventEmitter.broadcast({ type: 'apparitionsWinGrow', positions: win.positions });
			eventEmitter.broadcast({ type: 'winSweep', positions: win.positions });
			await animateSymbols({ positions: win.positions });
			eventEmitter.broadcast({ type: 'apparitionsWinRelease' });
		});
		// hold EVERY winning cell lit (union) under the overlay through the
		// money count-up - the glass glint sweep is deferred to the very end
		// (setWin, after the count-up) so it only plays once the spin settles
		eventEmitter.broadcast({
			type: 'winDimShow',
			positions: bookEvent.wins.flatMap((win) => win.positions),
		});
		eventEmitter.broadcast({
			type: 'winCycleSet',
			wins: bookEvent.wins.map((win) => win.positions),
		});
	},
	// customised: Haunted Mirrors crack, reflect neighbors into apparitions, then resolve
	mirrorBurst: async (bookEvent: BookEventOfType<'mirrorBurst'>) => {
		const mirrorPositions = bookEvent.mirrors.map((mirror) => mirror.mirror);

		// crack: swap the intact glass overlay for the cracked pane and hold a beat
		const crackedBoard = stateGameDerived
			.boardRaw()
			.map((reel) => reel.map((rawSymbol) => ({ ...rawSymbol })));
		bookEvent.mirrors.forEach(({ mirror }) => {
			delete crackedBoard[mirror.reel][mirror.row].glass;
		});
		eventEmitter.broadcast({ type: 'boardSettle', board: crackedBoard });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_mirror_break' });
		await eventEmitter.broadcastAsync({ type: 'mirrorBreak', positions: mirrorPositions });

		// shatter: the cracked pane bursts into shards and animates away
		eventEmitter.broadcast({ type: 'mirrorShatter', positions: mirrorPositions });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
		await animateSymbols({ positions: mirrorPositions });

		// reflect: rewrite the settled board with apparition counts + resolved
		// mirrors (glass flag dropped - the glass is gone now)
		const newBoard = stateGameDerived
			.boardRaw()
			.map((reel) => reel.map((rawSymbol) => ({ ...rawSymbol })));
		bookEvent.mirrors.forEach(({ mirror, reflected, mirrorBecomes }) => {
			newBoard[mirror.reel][mirror.row] = { name: mirrorBecomes.name };
			reflected.forEach((cell) => {
				newBoard[cell.reel][cell.row] = {
					...newBoard[cell.reel][cell.row],
					multiplier: cell.apparitions,
				};
			});
		});
		eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });

		// telegraph: show which neighbouring cells the mirror is about to split
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_combine_a' });
		await eventEmitter.broadcastAsync({
			type: 'mirrorTelegraph',
			pairs: bookEvent.mirrors.map(({ mirror, reflected }) => ({
				mirror,
				targets: reflected,
			})),
		});

		// then the split happens
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_up' });
		await eventEmitter.broadcastAsync({
			type: 'apparitionsPulse',
			positions: bookEvent.mirrors.flatMap((mirror) => mirror.reflected),
		});

		// the séance tally ticks up
		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		await waitForTimeout(350);
	},
	// customised: levels 2/3 - wins through haunted cells deepen the haunting
	hauntDeepen: async (bookEvent: BookEventOfType<'hauntDeepen'>) => {
		const newBoard = stateGameDerived
			.boardRaw()
			.map((reel) => reel.map((rawSymbol) => ({ ...rawSymbol })));
		bookEvent.cells.forEach((cell) => {
			newBoard[cell.reel][cell.row] = {
				...newBoard[cell.reel][cell.row],
				multiplier: cell.apparitions,
			};
		});
		eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
		await eventEmitter.broadcastAsync({ type: 'apparitionsPulse', positions: bookEvent.cells });
	},
	// customised: announces which of the three bonus levels was awarded
	bonusLevel: async (bookEvent: BookEventOfType<'bonusLevel'>) => {
		await eventEmitter.broadcastAsync({ type: 'bonusLevelShow', level: bookEvent.level });
	},
	setTotalWin: async (bookEvent: BookEventOfType<'setTotalWin'>) => {
		stateBet.winBookEventAmount = bookEvent.amount;
	},
	freeSpinTrigger: async (
		bookEvent: BookEventOfType<'freeSpinTrigger'>,
		{ bookEvents }: BookEventContext,
	) => {
		// the bonusLevel event follows in the same book; scatter count is the
		// fallback mapping (3/4/5 scatters -> level 1/2/3)
		const bonusLevelEvent = bookEvents.find(
			(event): event is BookEventOfType<'bonusLevel'> => event.type === 'bonusLevel',
		);
		const level = (bonusLevelEvent?.level ??
			Math.min(Math.max(bookEvent.positions.length - 2, 1), 3)) as 1 | 2 | 3;
		eventEmitter.broadcast({ type: 'winCycleStop' });
		// animate scatters
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_scatter_win_v2' });
		await animateSymbols({ positions: bookEvent.positions });
		// show free spin intro
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_superfreespin' });
		await eventEmitter.broadcastAsync({ type: 'uiHide' });
		await eventEmitter.broadcastAsync({ type: 'transition' });
		eventEmitter.broadcast({ type: 'freeSpinIntroShow', level });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'jng_intro_fs' });
		eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_freespin' });
		await eventEmitter.broadcastAsync({
			type: 'freeSpinIntroUpdate',
			totalFreeSpins: bookEvent.totalFs,
		});
		stateGame.gameType = 'freegame';
		eventEmitter.broadcast({ type: 'freeSpinIntroHide' });
		eventEmitter.broadcast({ type: 'boardFrameGlowShow' });
		eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: undefined,
			total: bookEvent.totalFs,
		});
		await eventEmitter.broadcastAsync({ type: 'uiShow' });
		await eventEmitter.broadcastAsync({ type: 'drawerButtonShow' });
		eventEmitter.broadcast({ type: 'drawerFold' });
	},
	updateFreeSpin: async (bookEvent: BookEventOfType<'updateFreeSpin'>) => {
		eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: bookEvent.amount,
			total: bookEvent.total,
		});
	},
	// extra scatters during free spins: animate them and bump the total
	freeSpinRetrigger: async (bookEvent: BookEventOfType<'freeSpinRetrigger'>) => {
		eventEmitter.broadcast({ type: 'winCycleStop' });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_scatter_win_v2' });
		await animateSymbols({ positions: bookEvent.positions });
		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: undefined,
			total: bookEvent.totalFs,
		});
	},
	freeSpinEnd: async (bookEvent: BookEventOfType<'freeSpinEnd'>) => {
		const winLevelData = winLevelMap[bookEvent.winLevel as WinLevel];

		eventEmitter.broadcast({ type: 'waysCounterHide' });
		eventEmitter.broadcast({ type: 'apparitionsHide' });
		eventEmitter.broadcast({ type: 'winCycleStop' });
		await eventEmitter.broadcastAsync({ type: 'uiHide' });
		stateGame.gameType = 'basegame';
		eventEmitter.broadcast({ type: 'boardFrameGlowHide' });
		eventEmitter.broadcast({ type: 'freeSpinOutroShow' });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_youwon_panel' });
		winLevelSoundsPlay({ winLevelData });
		await eventEmitter.broadcastAsync({
			type: 'freeSpinOutroCountUp',
			amount: bookEvent.amount,
			winLevelData,
		});
		winLevelSoundsStop();
		eventEmitter.broadcast({ type: 'freeSpinOutroHide' });
		eventEmitter.broadcast({ type: 'freeSpinCounterHide' });
		await eventEmitter.broadcastAsync({ type: 'transition' });
		await eventEmitter.broadcastAsync({ type: 'uiShow' });
		await eventEmitter.broadcastAsync({ type: 'drawerUnfold' });
		eventEmitter.broadcast({ type: 'drawerButtonHide' });
	},
	setWin: async (bookEvent: BookEventOfType<'setWin'>) => {
		// the celebration tier is chosen by win amount in bet multiples
		const celebration = getWinCelebration(bookEvent.amount);

		// winners stay lit under the overlay while the amount counts up (no glint)
		eventEmitter.broadcast({ type: 'winShow' });
		winLevelSoundsPlay({ winLevelData: celebration });
		await eventEmitter.broadcastAsync({
			type: 'winUpdate',
			amount: bookEvent.amount,
		});
		winLevelSoundsStop();
		eventEmitter.broadcast({ type: 'winHide' });

		// end of spin: NOW sweep the glass glint across each winning way (loops
		// through idle until the next spin clears it)
		eventEmitter.broadcast({ type: 'winCycleStart' });
	},
	finalWin: async (bookEvent: BookEventOfType<'finalWin'>) => {
		// Do nothing
	},
	// customised
	createBonusSnapshot: async (bookEvent: BookEventOfType<'createBonusSnapshot'>) => {
		const { bookEvents } = bookEvent;

		function findLastBookEvent<T>(type: T) {
			return _.findLast(bookEvents, (bookEvent) => bookEvent.type === type) as
				| BookEventOfType<T>
				| undefined;
		}

		const lastFreeSpinTriggerEvent = findLastBookEvent('freeSpinTrigger' as const);
		const lastUpdateFreeSpinEvent = findLastBookEvent('updateFreeSpin' as const);
		const lastSetTotalWinEvent = findLastBookEvent('setTotalWin' as const);
		const lastUpdateGlobalMultEvent = findLastBookEvent('updateGlobalMult' as const);

		if (lastFreeSpinTriggerEvent) await playBookEvent(lastFreeSpinTriggerEvent, { bookEvents });
		if (lastUpdateFreeSpinEvent) playBookEvent(lastUpdateFreeSpinEvent, { bookEvents });
		if (lastSetTotalWinEvent) playBookEvent(lastSetTotalWinEvent, { bookEvents });
		if (lastUpdateGlobalMultEvent) playBookEvent(lastUpdateGlobalMultEvent, { bookEvents });
	},
};
