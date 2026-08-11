const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');
(async () => {
  const chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const out = 'c:\\Users\\Emex33\\Documents\\tombstone reborn\\.qa\\after_yellow_fix';
  const bust = Date.now();
  const browser = await puppeteer.launch({
    executablePath: chrome, headless: 'new',
    args: ['--no-sandbox','--disable-gpu','--window-size=1280,800']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  await page.setCacheEnabled(false);
  async function run(id, tag) {
    await page.goto(`http://localhost:6009/iframe.html?id=${id}&viewMode=story&v=${bust}`, { waitUntil: 'networkidle0', timeout: 180000 }).catch(()=>{});
    await new Promise(r => setTimeout(r, 3000));
    await page.evaluate(() => {
      const buttons = [...document.querySelectorAll('button')];
      const hit = buttons.find(b => /action/i.test(b.textContent||''));
      if (hit) hit.click();
    });
    // capture frames during feature
    for (let i=1;i<=18;i++) {
      await new Promise(r => setTimeout(r, 1000));
      const dest = path.join(out, `final_${tag}_${String(i).padStart(2,'0')}.png`);
      await page.screenshot({ path: dest });
      console.log(tag, i, fs.statSync(dest).size);
    }
  }
  await run('mode-base-book--split-gang', 'split');
  await run('mode-base-book--gunsmoke', 'gun');
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
