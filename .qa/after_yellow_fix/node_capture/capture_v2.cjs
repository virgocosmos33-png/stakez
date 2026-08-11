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
    args: ['--no-sandbox','--disable-gpu','--window-size=1280,800','--disk-cache-size=1']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  // hard reload gunsmoke with cache disable
  await page.setCacheEnabled(false);
  const url = `http://localhost:6009/iframe.html?id=mode-base-book--gunsmoke&viewMode=story&v=${bust}`;
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 120000 });
  for (let i = 1; i <= 20; i++) {
    await new Promise(r => setTimeout(r, 1500));
    const dest = path.join(out, `v2_gunsmoke_${String(i).padStart(2,'0')}.png`);
    await page.screenshot({ path: dest });
    console.log('F', dest, fs.statSync(dest).size);
  }
  await page.goto(`http://localhost:6009/iframe.html?id=mode-base-book--split-outlaws&viewMode=story&v=${bust}`, { waitUntil: 'domcontentloaded', timeout: 120000 });
  for (let i = 1; i <= 16; i++) {
    await new Promise(r => setTimeout(r, 1500));
    const dest = path.join(out, `v2_outlaws_${String(i).padStart(2,'0')}.png`);
    await page.screenshot({ path: dest });
    console.log('F', dest, fs.statSync(dest).size);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
