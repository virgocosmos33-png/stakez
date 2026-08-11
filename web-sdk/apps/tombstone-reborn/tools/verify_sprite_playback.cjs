/**
 * Play EVERY cue of the shipped audio sprite through Howler in a real browser.
 *
 * This is deliberately independent of the game: it loads static/assets/audio
 * over plain HTTP and drives Howler directly, so the audio layer can be proven
 * even while another workstream has the app mid-refactor. It checks the things
 * that actually break in production:
 *
 *   - the sprite decodes at all (Howler 'load' fires, duration is sane)
 *   - every cue id in sounds.json is playable and reports playing()
 *   - seek() lands inside that cue's own window, so no cue can bleed into its
 *     neighbour (the classic sprite offset bug)
 *   - loop cues come back with loop() true
 *   - no Howler load/play error fires for any cue
 *
 * Run: node tools/verify_sprite_playback.cjs [baseUrl]
 */

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const BASE = process.argv[2] || 'http://localhost:6019';
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const HOWLER = path.join(
	'c:\\Users\\Emex33\\Documents\\tombstone reborn\\web-sdk\\node_modules\\.pnpm',
	'howler@2.2.4\\node_modules\\howler\\dist\\howler.min.js',
);
/** a cue must start within this many ms of its declared offset */
const SEEK_TOLERANCE_MS = 60;

(async () => {
	const browser = await puppeteer.launch({
		executablePath: CHROME,
		headless: 'new',
		args: [
			'--no-sandbox',
			'--disable-gpu',
			'--autoplay-policy=no-user-gesture-required',
			'--mute-audio',
		],
	});
	const page = await browser.newPage();
	const consoleErrors = [];
	page.on('console', (msg) => {
		if (msg.type() === 'error') consoleErrors.push(msg.text());
	});
	page.on('pageerror', (err) => consoleErrors.push(`pageerror: ${err.message}`));

	// navigate to the server first: fetch() from an about:blank origin is blocked
	await page.goto(`${BASE}/assets/audio/`, { waitUntil: 'domcontentloaded', timeout: 60000 });
	await page.addScriptTag({ content: fs.readFileSync(HOWLER, 'utf8') });

	const result = await page.evaluate(
		async (base, tolerance) => {
			const config = await (await fetch(`${base}/assets/audio/sounds.json`)).json();
			const sprite = config.sprite;
			const ids = Object.keys(sprite);

			const errors = [];
			const howl = new Howl({
				src: (config.src || ['assets/audio/sounds.mp3']).map((s) =>
					s.startsWith('http') ? s : `${base}/${s.replace(/^\.?\//, '')}`,
				),
				sprite,
				volume: 0.0001,
				onloaderror: (_, err) => errors.push(`loaderror ${err}`),
				onplayerror: (_, err) => errors.push(`playerror ${err}`),
			});

			await new Promise((resolve, reject) => {
				howl.once('load', resolve);
				howl.once('loaderror', (_, e) => reject(new Error(`sprite failed to load: ${e}`)));
				setTimeout(() => reject(new Error('sprite load timed out after 60s')), 60000);
			});

			const spriteDurationMs = howl.duration() * 1000;
			const rows = [];
			for (const id of ids) {
				const [offsetMs, lengthMs, loop] = sprite[id];
				const soundId = howl.play(id);
				// let the audio graph actually start before reading position
				await new Promise((r) => setTimeout(r, 22));
				const playing = howl.playing(soundId);
				const seekMs = howl.seek(soundId) * 1000;
				const looping = howl.loop(soundId);
				const drift = seekMs - offsetMs;
				const inWindow = seekMs >= offsetMs - tolerance && seekMs <= offsetMs + lengthMs;
				howl.stop(soundId);
				rows.push({
					id,
					offsetMs,
					lengthMs,
					loop: !!loop,
					playing,
					seekMs,
					drift,
					looping,
					inWindow,
					problems: [
						!playing ? 'not playing' : null,
						!inWindow ? `seek ${seekMs.toFixed(0)}ms outside window` : null,
						Math.abs(drift) > tolerance ? `drift ${drift.toFixed(0)}ms` : null,
						loop && !looping ? 'loop flag lost' : null,
						!loop && looping ? 'unexpectedly looping' : null,
					].filter(Boolean),
				});
			}
			return { spriteDurationMs, rows, errors };
		},
		BASE,
		SEEK_TOLERANCE_MS,
	);

	await browser.close();

	const bad = result.rows.filter((r) => r.problems.length);
	const loops = result.rows.filter((r) => r.loop);
	console.log(`sprite duration : ${(result.spriteDurationMs / 1000).toFixed(2)}s`);
	console.log(`cues swept      : ${result.rows.length}`);
	console.log(`loop cues       : ${loops.map((r) => r.id).join(', ')}`);
	const drifts = result.rows.map((r) => Math.abs(r.drift));
	console.log(`worst seek drift: ${Math.max(...drifts).toFixed(1)}ms`);

	if (result.errors.length) {
		console.log('\nHowler errors:');
		result.errors.forEach((e) => console.log(`  ! ${e}`));
	}
	if (consoleErrors.length) {
		console.log('\nconsole errors:');
		[...new Set(consoleErrors)].forEach((e) => console.log(`  ! ${e}`));
	}
	if (bad.length) {
		console.log(`\n${bad.length} cue problem(s):`);
		bad.forEach((r) => console.log(`  ! ${r.id}: ${r.problems.join('; ')}`));
		process.exit(1);
	}
	console.log('\nevery cue played, reported playing, and seeked inside its own window');
})().catch((err) => {
	console.error(err);
	process.exit(1);
});
