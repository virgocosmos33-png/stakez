import { locales } from 'config-lingui';
import { page } from '$app/state';

export type Language = (typeof locales)[number];

export type Key =
	// keys for play
	| 'sessionID'
	| 'rgs_url'
	| 'lang'
	| 'currency'
	| 'device'
	| 'social'
	| 'demo'
	// keys for replay 
	| 'replay'
	| 'amount'
	| 'game'
	| 'mode'
	| 'version'
	| 'event'
	;

const getUrlSearchParam = (key: Key) => page.url.searchParams.get(key) as string;

// Local mock RGS (tools/mock_rgs.py). The fetcher always hits https://${rgsUrl}/...,
// so an empty rgs_url becomes https:///wallet/authenticate — Chrome then tries
// the host "wallet" and dies with ERR_NAME_NOT_RESOLVED. On localhost we default
// to the mock so opening the app without query params still authenticates.
const isLocalHost = () => {
	const host = page.url.hostname;
	return host === 'localhost' || host === '127.0.0.1';
};

// params for play
const lang = () =>
	getUrlSearchParam('lang') === 'br' ? 'pt' : (getUrlSearchParam('lang') as Language) || 'en';
const sessionID = () => getUrlSearchParam('sessionID') || (isLocalHost() ? 'dev' : '');
const rgsUrl = () => getUrlSearchParam('rgs_url') || (isLocalHost() ? 'localhost:7777' : '');
const social = () => getUrlSearchParam('social') === 'true';

// params for replay
const replay = () => getUrlSearchParam('replay') === 'true';
const amount = () => Number(getUrlSearchParam('amount')) || 0;
const game = () => getUrlSearchParam('game') || '';
const version = () => getUrlSearchParam('version') || '';
const mode = () => getUrlSearchParam('mode') || '';
const event = () => getUrlSearchParam('event') || '';

export const stateUrlDerived = {
	// states for play
	lang,
	sessionID,
	rgsUrl,
	social,
	// states for replay
	replay,
	amount,
	game,
	mode,
	version,
	event,
};
