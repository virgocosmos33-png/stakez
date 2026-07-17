/* Crawl https://stake-engine.com/docs and screenshot every docs page. */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = 'https://stake-engine.com';
const START = ROOT + '/docs';
const OUT = path.join(__dirname, 'shots');

function slug(url) {
	const u = new URL(url);
	let name = (u.pathname + (u.hash ? '_' + u.hash : '')).replace(/^\/+|\/+$/g, '');
	name = name.replace(/[^a-zA-Z0-9._-]+/g, '_');
	return (name || 'docs_home') + '.png';
}

function normalize(href) {
	try {
		const u = new URL(href, ROOT);
		if (u.origin !== ROOT) return null;
		if (!u.pathname.startsWith('/docs')) return null;
		u.hash = '';
		u.search = '';
		let s = u.toString();
		if (s.endsWith('/')) s = s.slice(0, -1);
		return s;
	} catch {
		return null;
	}
}

(async () => {
	fs.mkdirSync(OUT, { recursive: true });
	const browser = await chromium.launch();
	const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

	const queue = [normalize(START)];
	const seen = new Set(queue);
	const done = [];
	const failed = [];

	while (queue.length) {
		const url = queue.shift();
		try {
			await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
			await page.waitForTimeout(800); // let client-side rendering settle

			// discover new /docs links
			const links = await page.$$eval('a[href]', (as) => as.map((a) => a.getAttribute('href')));
			for (const href of links) {
				const n = normalize(href);
				if (n && !seen.has(n)) {
					seen.add(n);
					queue.push(n);
				}
			}

			// expand any collapsed sidebar groups so nav links get discovered too
			const expanders = await page.$$('nav button, aside button');
			for (const b of expanders) {
				try { await b.click({ timeout: 500 }); } catch {}
			}
			await page.waitForTimeout(300);
			const links2 = await page.$$eval('a[href]', (as) => as.map((a) => a.getAttribute('href')));
			for (const href of links2) {
				const n = normalize(href);
				if (n && !seen.has(n)) {
					seen.add(n);
					queue.push(n);
				}
			}

			const file = path.join(OUT, slug(url));
			await page.screenshot({ path: file, fullPage: true });
			done.push(url);
			console.log(`OK  [${done.length}] ${url} -> ${path.basename(file)} (queue: ${queue.length})`);
		} catch (e) {
			failed.push(url);
			console.log(`FAIL ${url}: ${e.message.split('\n')[0]}`);
		}
	}

	fs.writeFileSync(
		path.join(__dirname, 'crawl_report.json'),
		JSON.stringify({ done, failed, total: done.length + failed.length }, null, 2)
	);
	console.log(`\nDONE: ${done.length} pages captured, ${failed.length} failed`);
	await browser.close();
})();
