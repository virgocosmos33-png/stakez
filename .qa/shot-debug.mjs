// CDP screenshot + console capture for Storybook QA
import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const url =
	process.argv[2] ||
	'http://localhost:6009/iframe.html?id=mode-base-book--dead-spin&viewMode=story';
const out = process.argv[3] || 'c:/Users/Emex33/Documents/tombstone reborn/.qa/deadspin-cdp.png';
const waitMs = Number(process.argv[4] ?? 25000);
const width = Number(process.argv[5] ?? 1280);
const height = Number(process.argv[6] ?? 800);
const clickAction = process.argv[7] === 'click';
const PORT = 9235;

const chrome = spawn(
	'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
	[
		'--headless=new',
		'--disable-gpu',
		'--no-sandbox',
		'--hide-scrollbars',
		'--mute-audio',
		`--window-size=${width},${height}`,
		`--remote-debugging-port=${PORT}`,
		`--user-data-dir=${mkdtempSync(join(tmpdir(), 'qa-chrome-'))}`,
		'about:blank',
	],
	{ stdio: 'ignore' },
);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const logs = [];

const browserWsUrl = await (async () => {
	for (let i = 0; i < 80; i++) {
		try {
			const res = await fetch(`http://127.0.0.1:${PORT}/json/version`);
			return (await res.json()).webSocketDebuggerUrl;
		} catch {
			await sleep(250);
		}
	}
	throw new Error('chrome devtools never came up');
})();

const ws = new WebSocket(browserWsUrl);
await new Promise((resolve, reject) => {
	ws.onopen = resolve;
	ws.onerror = reject;
});

let nextId = 1;
const pending = new Map();
const eventHandlers = [];
ws.onmessage = (event) => {
	const msg = JSON.parse(event.data);
	if (msg.id != null) {
		const entry = pending.get(msg.id);
		if (!entry) return;
		pending.delete(msg.id);
		msg.error ? entry.reject(new Error(JSON.stringify(msg.error))) : entry.resolve(msg.result);
		return;
	}
	for (const h of eventHandlers) h(msg);
};

const send = (method, params = {}, sessionId) =>
	new Promise((resolve, reject) => {
		const id = nextId++;
		pending.set(id, { resolve, reject });
		ws.send(JSON.stringify({ id, method, params, sessionId }));
	});

const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });

eventHandlers.push((msg) => {
	if (msg.sessionId !== sessionId) return;
	if (msg.method === 'Runtime.consoleAPICalled') {
		const args = (msg.params.args || []).map((a) => a.value ?? a.description ?? a.type);
		logs.push(['console', msg.params.type, ...args].join(' | '));
	}
	if (msg.method === 'Runtime.exceptionThrown') {
		const d = msg.params.exceptionDetails || {};
		const ex = d.exception || {};
		logs.push(
			[
				'exception',
				d.text,
				ex.description || ex.value || '',
				d.url || '',
				d.lineNumber,
				d.columnNumber,
			].join(' | '),
		);
	}
});

await send('Runtime.enable', {}, sessionId);
await send('Page.enable', {}, sessionId);
await send(
	'Emulation.setDeviceMetricsOverride',
	{ width, height, deviceScaleFactor: 1, mobile: false },
	sessionId,
);
await send('Page.navigate', { url }, sessionId);

// Poll until Action message leaves Initialising or timeout
const started = Date.now();
let lastMsg = '';
while (Date.now() - started < waitMs) {
	const { result } = await send(
		'Runtime.evaluate',
		{
			expression: `(() => {
        const msg = document.querySelector('.message')?.textContent || '';
        const btn = document.querySelector('button.action');
        const canvas = document.querySelector('canvas');
        return JSON.stringify({
          msg,
          disabled: !!btn?.disabled,
          canvas: canvas ? [canvas.width, canvas.height] : null,
          loadedHint: msg.includes('Click action') || msg.includes('resolved'),
        });
      })()`,
			returnByValue: true,
		},
		sessionId,
	);
	const state = JSON.parse(result.value);
	lastMsg = state.msg;
	if (state.loadedHint) {
		logs.push('READY ' + JSON.stringify(state));
		break;
	}
	await sleep(500);
}
logs.push('FINAL_MSG ' + lastMsg);

if (clickAction) {
	await send(
		'Runtime.evaluate',
		{
			expression: `document.querySelector('button.action')?.click(); 'clicked'`,
			returnByValue: true,
		},
		sessionId,
	);
	await sleep(8000);
}

const shot = await send('Page.captureScreenshot', { format: 'png' }, sessionId);
writeFileSync(out, Buffer.from(shot.data, 'base64'));
writeFileSync(out.replace(/\.png$/, '-console.txt'), logs.join('\n'));
console.log('wrote', out, 'bytes', Buffer.from(shot.data, 'base64').length);
console.log('logs', logs.length);
console.log(logs.filter((l) => /exception|error|Error|READY|FINAL/i.test(l)).slice(0, 40).join('\n'));

chrome.kill();
process.exit(0);
