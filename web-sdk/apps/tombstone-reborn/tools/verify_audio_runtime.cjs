/**
 * Live audio verification against the running Storybook (port 6009).
 *
 * Static checks cannot prove what the game actually asks Howler to play, so this
 * patches Howl.prototype.play in the page and records every sprite id requested
 * while real stories run. Any id missing from the loaded sprite is reported with
 * the cue name, which is exactly the failure that would otherwise be a silent
 * no-op in production.
 *
 * Run (from the app dir):
 *   $env:NODE_PATH="<repo>\.qa\after_yellow_fix\node_capture\node_modules"
 *   node tools/verify_audio_runtime.cjs
 */

const puppeteer = require('puppeteer-core');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const BASE = process.argv[2] || 'http://localhost:6009';
const STORIES = [
	'mode-base-book--dead-spin',
	'mode-base-book--gunsmoke',
	'mode-base-book--split-outlaws',
	'mode-base-book--tombstone-open',
	'mode-base-book--dig-up',
	'mode-bonus-book--bounty',
	'mode-bonus-book--max-win',
];
const RETIRED = [
	'sfx_madams_eye',
	'sfx_mirror_break',
	'sfx_xways_split',
	'sfx_claw_split',
	'sfx_cell_seal_h3_loop',
	'bgm_winlevel_big',
	'bgm_winlevel_superwin',
	'bgm_winlevel_mega',
	'bgm_winlevel_epic',
	'bgm_winlevel_max',
];
/** Books can run long (max win recounts for a while), so wait for the
 *  template's own "resolved" message instead of guessing a duration. */
const BOOK_TIMEOUT_MS = 150000;
const SETTLE_MS = 4000;
const AUDIO_PATTERN = /sounds\.(ogg|m4a|mp3|ac3)|\/audio\//i;

const instrument = () => {
	window.__audio = { played: {}, unknown: {}, console: [], errors: [] };
	const patch = () => {
		if (!window.Howl || window.__audio.patched) return !!window.__audio.patched;
		const original = window.Howl.prototype.play;
		window.Howl.prototype.play = function (id, internal) {
			if (typeof id === 'string') {
				const bucket = this._sprite && this._sprite[id] ? 'played' : 'unknown';
				window.__audio[bucket][id] = (window.__audio[bucket][id] || 0) + 1;
			}
			return original.call(this, id, internal);
		};
		window.__audio.patched = true;
		return true;
	};
	if (!patch()) {
		const timer = setInterval(() => {
			if (patch()) clearInterval(timer);
		}, 20);
		setTimeout(() => clearInterval(timer), 30000);
	}
};

const readHowlState = () => {
	const howls = (window.Howler && window.Howler._howls) || [];
	const loaded = howls.find((howl) => howl._sprite && Object.keys(howl._sprite).length);
	return {
		howlCount: howls.length,
		states: howls.map((howl) => howl._state),
		spriteKeys: loaded ? Object.keys(loaded._sprite) : [],
		duration: loaded ? loaded._duration : 0,
		ctxState: window.Howler && window.Howler.ctx ? window.Howler.ctx.state : 'none',
		audio: window.__audio,
	};
};

(async () => {
	const browser = await puppeteer.launch({
		executablePath: CHROME,
		headless: 'new',
		args: [
			'--no-sandbox',
			'--disable-gpu',
			'--autoplay-policy=no-user-gesture-required',
			'--window-size=1280,800',
		],
	});

	const failures = [];
	const allPlayed = new Set();
	const allUnknown = new Map();
	let spriteKeys = [];
	let spriteDuration = 0;

	for (const story of STORIES) {
		const page = await browser.newPage();
		await page.setViewport({ width: 1280, height: 800 });
		await page.evaluateOnNewDocument(instrument);

		const messages = [];
		const badUrls = [];
		page.on('console', (message) => {
			const text = message.text();
			if (/error|missing|unsupported|decode|Howler|sprite/i.test(text)) {
				messages.push(`[${message.type()}] ${text}`);
			}
		});
		page.on('pageerror', (error) => messages.push(`[pageerror] ${error.message}`));
		page.on('response', (response) => {
			if (response.status() >= 400) badUrls.push(`${response.status()} ${response.url()}`);
		});
		page.on('requestfailed', (request) =>
			badUrls.push(`FAILED ${request.url()} (${request.failure()?.errorText})`),
		);

		const url = `${BASE}/iframe.html?id=${story}&viewMode=story&v=${Date.now()}`;
		await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 120000 });

		try {
			await page.waitForFunction(
				() => {
					const howls = (window.Howler && window.Howler._howls) || [];
					return howls.some((howl) => howl._state === 'loaded');
				},
				{ timeout: 90000, polling: 250 },
			);
		} catch {
			failures.push(`${story}: sprite never reached state "loaded"`);
		}

		// The story template gates the book behind its Action button; clicking it
		// is both the book trigger and the gesture that unlocks Howler's context.
		let bookRan = false;
		try {
			await page.waitForSelector('button.action:not([disabled])', { timeout: 90000 });
			await page.click('button.action');
			await page.waitForFunction(
				() => (document.querySelector('.message')?.textContent || '').includes('resolved'),
				{ timeout: BOOK_TIMEOUT_MS, polling: 500 },
			);
			bookRan = true;
		} catch (error) {
			failures.push(`${story}: book never completed (${error.message.split('\n')[0]})`);
		}

		await new Promise((resolve) => setTimeout(resolve, SETTLE_MS));
		const state = await page.evaluate(readHowlState);

		if (state.spriteKeys.length) {
			spriteKeys = state.spriteKeys;
			spriteDuration = state.duration;
		}
		Object.keys(state.audio.played).forEach((key) => allPlayed.add(key));
		for (const [key, count] of Object.entries(state.audio.unknown)) {
			allUnknown.set(key, (allUnknown.get(key) || 0) + count);
			failures.push(`${story}: played sprite id NOT in sprite -> ${key} (x${count})`);
		}
		messages
			.filter((line) => /pageerror/i.test(line))
			.forEach((line) => failures.push(`${story}: ${line}`));
		const audioUrlFailures = [...new Set(badUrls)].filter((line) => AUDIO_PATTERN.test(line));
		audioUrlFailures.forEach((line) => failures.push(`${story}: audio request failed -> ${line}`));

		console.log(
			`${story.padEnd(34)} howls=${state.howlCount} state=${state.states.join('/')} ` +
				`ctx=${state.ctxState} cues=${state.spriteKeys.length} ` +
				`book=${bookRan ? 'ran' : 'STALLED'} ` +
				`played=${Object.keys(state.audio.played).length} ` +
				`unknown=${Object.keys(state.audio.unknown).length}`,
		);
		const nonAudioBad = [...new Set(badUrls)].filter((line) => !AUDIO_PATTERN.test(line));
		if (nonAudioBad.length) {
			console.log(`    non-audio request problems (not mine, listed for context):`);
			nonAudioBad.slice(0, 4).forEach((line) => console.log(`      ${line}`));
		}
		await page.close();
	}

	// A book only fires the handful of cues its events need. Sweep every sprite
	// id through Howler so all 71 are proven playable, not just the ones that
	// happened to trigger.
	const sweepPage = await browser.newPage();
	await sweepPage.setViewport({ width: 1280, height: 800 });
	await sweepPage.evaluateOnNewDocument(instrument);
	await sweepPage.goto(`${BASE}/iframe.html?id=${STORIES[0]}&viewMode=story&v=${Date.now()}`, {
		waitUntil: 'domcontentloaded',
		timeout: 120000,
	});
	await sweepPage.waitForFunction(
		() => ((window.Howler && window.Howler._howls) || []).some((h) => h._state === 'loaded'),
		{ timeout: 90000, polling: 250 },
	);
	await sweepPage.waitForSelector('button.action:not([disabled])', { timeout: 90000 });
	await sweepPage.click('button.action');
	await new Promise((resolve) => setTimeout(resolve, 1500));

	const sweep = await sweepPage.evaluate(async () => {
		const howl = window.Howler._howls.find((h) => h._sprite && h._state === 'loaded');
		const results = [];
		for (const key of Object.keys(howl._sprite)) {
			const id = howl.play(key);
			await new Promise((resolve) => setTimeout(resolve, 90));
			const playing = typeof id === 'number' && howl.playing(id);
			const seek = typeof id === 'number' ? Number(howl.seek(id)) || 0 : -1;
			const [start, length] = howl._sprite[key];
			// seek must land inside the cue's own window, or the offsets are wrong
			const insideWindow = seek * 1000 >= start - 60 && seek * 1000 <= start + length + 400;
			howl.stop(id);
			results.push({ key, ok: playing && insideWindow, playing, seekMs: Math.round(seek * 1000), start, length });
		}
		return results;
	});
	await sweepPage.close();
	await browser.close();

	const sweepBad = sweep.filter((entry) => !entry.ok);
	console.log(`\nfull sprite sweep: ${sweep.length - sweepBad.length}/${sweep.length} cues played and seeked inside their own window`);
	for (const entry of sweepBad) {
		failures.push(
			`sweep ${entry.key}: playing=${entry.playing} seek=${entry.seekMs}ms ` +
				`window=[${entry.start}..${entry.start + entry.length}]`,
		);
	}

	console.log(`\nsprite cues loaded in browser : ${spriteKeys.length}`);
	console.log(`sprite duration seen by Howler: ${spriteDuration.toFixed(2)}s`);
	const legacy = RETIRED.filter((key) => spriteKeys.includes(key));
	console.log(`retired keys present in browser: ${legacy.length ? legacy.join(', ') : 'NONE'}`);
	legacy.forEach((key) => failures.push(`retired key loaded in browser: ${key}`));

	const played = [...allPlayed].sort();
	console.log(`\ncues actually heard across stories (${played.length}):`);
	console.log(`  ${played.join(', ')}`);

	console.log(`\n${failures.length} failure(s)`);
	failures.forEach((failure) => console.log(`  ! ${failure}`));
	process.exit(failures.length ? 1 : 0);
})().catch((error) => {
	console.error(error);
	process.exit(1);
});
