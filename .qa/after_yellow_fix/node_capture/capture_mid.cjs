const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');
(async () => {
  const chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const out = 'c:\\Users\\Emex33\\Documents\\tombstone reborn\\.qa\\after_yellow_fix';
  const bust = Date.now();
  const browser = await puppeteer.launch({
    executablePath: chrome,
    headless: 'new',
    args: ['--no-sandbox','--disable-gpu','--window-size=1280,800']
  });
  const jobs = [
    ['mode-base-book--gunsmoke', 'gunsmoke', 40000, 1500],
    ['mode-base-book--split-gang', 'split_gang', 40000, 1500],
    ['mode-base-book--split-outlaws', 'split_outlaws', 40000, 1500],
  ];
  for (const [id, tag, total, step] of jobs) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    const url = `http://localhost:6009/iframe.html?id=${id}&viewMode=story&v=${bust}`;
    console.log('GOTO', id);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 120000 });
    let t = 0; let i = 0;
    while (t <= total) {
      await new Promise(r => setTimeout(r, step));
      t += step; i += 1;
      const dest = path.join(out, `mid_${tag}_${String(i).padStart(2,'0')}.png`);
      await page.screenshot({ path: dest });
      console.log('FRAME', dest, fs.statSync(dest).size);
    }
    await page.close();
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
