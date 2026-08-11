/**
 * Enumerate every sound that is ACTUALLY playing in the base game over time.
 *
 * Declared wiring lies; this reads Howler's own registry (Howler._howls -> _sounds)
 * so we see the real active voices, their sprite id, loop flag and volume. Any
 * moment with more than one looping voice is the bug we are hunting.
 *
 * Run: node tools/probe_live_loops.cjs [baseUrl] [storyId]
 */

const puppeteer = require('puppeteer-core');

const BASE = process.argv[2] || 'http://localhost:6012';
const STORY = process.argv[3] || 'mode-base-book--dead-spin';
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const SAMPLES = Number(process.argv[4]) || 12;
const SAMPLE_GAP_MS = 1500;

(async () => {
	const browser = await puppeteer.launch({
		executablePath: CHROME,
		headless: 'new',
		args: [
			'--no-sandbox',
			'--disable-gpu',
			'--autoplay-policy=no-user-gesture-required',
			'--mute-audio',
			'--window-size=1280,800',
		],
	});
	const page = await browser.newPage();
	await page.setViewport({ width: 1280, height: 800 });

	// A cue that is missing from the sprite does not throw — Howler just plays
	// nothing — so the only evidence is what the page logs. Collect it.
	const errors = [];
	const warnings = [];
	page.on('console', (msg) => {
		const text = msg.text();
		if (msg.type() === 'error') errors.push(text);
		else if (msg.type() === 'warning') warnings.push(text);
	});
	page.on('pageerror', (err) => errors.push(`pageerror: ${err.message}`));
	// "Failed to load resource" on its own does not say WHAT failed, and a 404 on
	// a sprite file is the difference between silence and working audio.
	const failed = [];
	page.on('response', (res) => {
		if (res.status() >= 400) failed.push(`${res.status()} ${res.url()}`);
	});

	// record every play() call with its sprite id, before any app code runs
	await page.evaluateOnNewDocument(() => {
		window.__plays = [];
		const hook = setInterval(() => {
			if (!window.Howl) return;
			clearInterval(hook);
			const orig = window.Howl.prototype.play;
			window.Howl.prototype.play = function (id) {
				window.__plays.push({ id: typeof id === 'string' ? id : `<${id}>`, t: Date.now() });
				return orig.apply(this, arguments);
			};
		}, 5);
	});

	await page.goto(`${BASE}/iframe.html?id=${STORY}&viewMode=story&v=${Date.now()}`, {
		waitUntil: 'domcontentloaded',
		timeout: 120000,
	});

	const sample = () =>
		page.evaluate(() => {
			const H = window.Howler;
			if (!H || !H._howls) return { error: 'no Howler' };
			const active = [];
			for (const howl of H._howls) {
				for (const s of howl._sounds || []) {
					if (s._paused || s._ended || !s._node) continue;
					active.push({
						sprite: s._sprite,
						loop: !!s._loop,
						volume: Math.round((s._volume ?? 0) * 1000) / 1000,
						seek: Math.round((s._node.currentTime ?? 0) * 100) / 100,
						rate: s._rate,
					});
				}
			}
			return { active, ctxRate: H.ctx ? H.ctx.sampleRate : null };
		});

	// Storybook compiles the story on first hit; wait for the audio engine
	// itself rather than guessing a boot duration
	await page.waitForFunction(
		() => window.Howler && window.Howler._howls && window.Howler._howls.length > 0,
		{ timeout: 180000, polling: 250 },
	);
	await page.waitForFunction(
		() => ((window.Howler && window.Howler._howls) || []).some((h) => h._state === 'loaded'),
		{ timeout: 120000, polling: 250 },
	);
	// The story gates the book behind its Action button, and that click is also
	// the gesture that unlocks the audio context. Without it nothing ever plays
	// and the probe reports a silence that the real player never hears.
	await page.waitForSelector('button.action:not([disabled])', { timeout: 90000 });
	await page.click('button.action');
	await new Promise((r) => setTimeout(r, 3000));

	console.log(`story: ${STORY}`);
	const loopCounts = [];
	for (let i = 0; i < SAMPLES; i++) {
		const snap = await sample();
		if (snap.error) {
			console.log(`  t=${i}  ${snap.error}`);
		} else {
			const loops = snap.active.filter((a) => a.loop);
			loopCounts.push(loops.length);
			const fmt = (a) =>
				`${a.sprite}${a.loop ? '[LOOP]' : ''} vol=${a.volume}${a.rate !== 1 ? ` rate=${a.rate}` : ''}`;
			console.log(
				`  t=${(i * SAMPLE_GAP_MS) / 1000}s  active=${snap.active.length} looping=${loops.length}  ${snap.active.map(fmt).join(' | ') || '(silence)'}`,
			);
		}
		await new Promise((r) => setTimeout(r, SAMPLE_GAP_MS));
	}

	const plays = await page.evaluate(() => window.__plays || []);
	const counts = {};
	for (const p of plays) counts[p.id] = (counts[p.id] || 0) + 1;
	console.log(`\nplay() calls (${plays.length} total):`);
	Object.entries(counts)
		.sort((a, b) => b[1] - a[1])
		.forEach(([id, n]) => console.log(`  ${n} x ${id}`));

	// Every id played has to exist in the sprite map, or it played silence.
	const unknown = await page.evaluate((ids) => {
		const named = new Set();
		for (const howl of (window.Howler && window.Howler._howls) || [])
			for (const key of Object.keys(howl._sprite || {})) named.add(key);
		return ids.filter((id) => !id.startsWith('<') && !named.has(id));
	}, Object.keys(counts));

	const ctxRate = (await sample()).ctxRate;
	console.log(`\naudio context sample rate: ${ctxRate}`);
	console.log(`max simultaneous looping voices: ${Math.max(0, ...loopCounts)}`);
	console.log(`cues played that are NOT in the sprite: ${unknown.join(', ') || 'none'}`);
	console.log(`console errors: ${errors.length}`);
	errors.slice(0, 12).forEach((e) => console.log(`  ERROR ${e.slice(0, 200)}`));
	console.log(`failed requests: ${failed.length}`);
	failed.slice(0, 12).forEach((f) => console.log(`  HTTP  ${f}`));
	const missing = warnings.filter((w) => /sound|howl|sprite|audio/i.test(w));
	console.log(`console warnings: ${warnings.length} (audio-related: ${missing.length})`);
	missing.slice(0, 12).forEach((w) => console.log(`  WARN  ${w.slice(0, 200)}`));

	await browser.close();
})().catch((e) => {
	console.error(e);
	process.exit(1);
});
