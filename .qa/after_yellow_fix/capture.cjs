const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
async function main() {
  let puppeteer;
  try { puppeteer = require('puppeteer-core'); }
  catch (e) {
    console.error('NO_PUPPETEER_CORE', e.message);
    process.exit(2);
  }
  const chrome = 'C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe';
  const out = 'c:\\\\Users\\\\Emex33\\\\Documents\\\\tombstone reborn\\\\.qa\\\\after_yellow_fix';
  const bust = Date.now();
  const stories = [
    ['mode-base-book--dead-spin', 'pw_dead_spin.png', 25000],
    ['mode-base-book--gunsmoke', 'pw_gunsmoke.png', 45000],
    ['mode-base-book--split-gang', 'pw_split_gang.png', 45000],
    ['mode-base-book--split-outlaws', 'pw_split_outlaws.png', 45000],
  ];
  const browser = await puppeteer.launch({
    executablePath: chrome,
    headless: 'new',
    args: ['--no-sandbox','--disable-gpu','--window-size=1280,800']
  });
  for (const [id, file, wait] of stories) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    const url = `http://localhost:6009/iframe.html?id=${id}&viewMode=story&v=${bust}`;
    console.log('GOTO', id);
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 120000 }).catch(()=>{});
    await new Promise(r => setTimeout(r, wait));
    const dest = path.join(out, file);
    await page.screenshot({ path: dest, fullPage: false });
    console.log('SHOT', dest, fs.statSync(dest).size);
    await page.close();
  }
  await browser.close();
}
main().catch(e => { console.error(e); process.exit(1); });
