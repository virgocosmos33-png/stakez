/**
 * Console tracing for hunting frozen rounds. Active on the dev server (or with
 * ?debug in the URL), silent in production builds.
 *
 * What it prints:
 *   [trace] xstate -> {"bet":...}          every state machine transition
 *   [trace] book:reveal #12 start/done     every book event with duration
 *   [trace] gate:winLightning start/done   every BLOCKING broadcastAsync gate
 *   [trace] emit hotKey Space keyDown      key presses and skip/stop signals
 * plus a loud console.warn when a book event or gate is still running after
 * 10s - that is the hang.
 */

export const traceEnabled =
	typeof window !== 'undefined' &&
	(import.meta.env.DEV || new URLSearchParams(window.location.search).has('debug'));

const ts = () => new Date().toISOString().slice(11, 23);

export const trace = (...args: unknown[]) => {
	if (!traceEnabled) return;
	console.log(`%c[trace ${ts()}]`, 'color:#a78bfa;font-weight:bold', ...args);
};

const STUCK_MS = 10_000;
let seq = 0;

/** Wraps an async unit of work with start/done/duration + stuck detection. */
const timed = async <T>(label: string, run: () => Promise<T>): Promise<T> => {
	const id = ++seq;
	const startedAt = performance.now();
	trace(`${label} #${id} start`);
	const stuckTimer = setTimeout(() => {
		console.warn(
			`[trace] ${label} #${id} STILL RUNNING after ${STUCK_MS / 1000}s - this is likely the hang`,
		);
	}, STUCK_MS);
	try {
		return await run();
	} finally {
		clearTimeout(stuckTimer);
		trace(`${label} #${id} done in ${Math.round(performance.now() - startedAt)}ms`);
	}
};

/** Wrap every book event handler with tracing. No-op when tracing is off. */
export function traceBookHandlers<
	TMap extends Record<string, (...args: never[]) => Promise<unknown> | unknown>,
>(map: TMap): TMap {
	if (!traceEnabled) return map;
	const traced: Record<string, unknown> = {};
	for (const [type, handler] of Object.entries(map)) {
		traced[type] = (...args: never[]) =>
			timed(`book:${type}`, async () => await (handler as (...a: never[]) => unknown)(...args));
	}
	return traced as TMap;
}

// events worth logging on the fire-and-forget broadcast path (async gates are
// always traced - they are the things that can block a round)
const TRACED_BROADCASTS = new Set([
	'bet',
	'autoBet',
	'resumeBet',
	'hotKey',
	'stopButtonClick',
	'stopButtonEnable',
	'winShow',
	'winHide',
]);

type MinimalEmitter = {
	broadcast: (event: { type: string } & Record<string, unknown>) => void;
	broadcastAsync: (event: { type: string } & Record<string, unknown>) => Promise<unknown>;
};

/** Patch an event emitter so key broadcasts and ALL async gates are logged. */
export function traceEmitter(eventEmitter: MinimalEmitter) {
	if (!traceEnabled) return;

	const broadcast = eventEmitter.broadcast.bind(eventEmitter);
	eventEmitter.broadcast = (event) => {
		if (TRACED_BROADCASTS.has(event.type)) {
			const detail =
				event.type === 'hotKey' ? `${event.key as string} ${event.action as string}` : '';
			trace('emit', event.type, detail);
		}
		return broadcast(event);
	};

	const broadcastAsync = eventEmitter.broadcastAsync.bind(eventEmitter);
	eventEmitter.broadcastAsync = (event) => timed(`gate:${event.type}`, () => broadcastAsync(event));
}
