type Resolve = (value: void | PromiseLike<void>) => void;

export const waitForResolve = (callback: (resolve: Resolve) => void) =>
	new Promise<void>((resolve) => callback(resolve));

export const waitForTimeout = (time: number) =>
	new Promise<void>((resolve) => {
		const timeout = setTimeout(() => {
			clearTimeout(timeout);
			resolve();
		}, time);
	});

// Safety net for sequences that wait on a user action (CONTINUE, a click) which
// may never arrive: the round must never stall, so the timeout releases it.
export const waitForResolveOrTimeout = (
	callback: (resolve: Resolve) => void,
	time: number,
	label?: string,
) =>
	new Promise<void>((resolve) => {
		let settled = false;

		const settle = (timedOut: boolean) => {
			if (settled) return;
			settled = true;
			clearTimeout(timeout);
			if (timedOut && label) console.warn(`[wait] ${label} timed out after ${time}ms`);
			resolve();
		};

		const timeout = setTimeout(() => settle(true), time);

		callback(() => settle(false));
	});
