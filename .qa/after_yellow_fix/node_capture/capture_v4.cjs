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
  async function run(id, tag, frames) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    await page.setCacheEnabled(false);
    const url = `http://localhost:6009/iframe.html?id=${id}&viewMode=story&v=${bust}`;
    console.log('GOTO', id);
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 180000 }).catch(()=>{});
    await new Promise(r => setTimeout(r, 4000));
    // Click Storybook Action "play" / start
    const clicked = await page.evaluate(() => {
      const buttons = [...document.querySelectorAll('button, [role="button"], a')];
      const hit = buttons.find(b => /action|play|start|run/i.test((b.textContent||'') + (b.getAttribute('aria-label')||'')));
      if (hit) { hit.click(); return 'btn:' + (hit.textContent||'').slice(0,40); }
      // addon-actions panel or storybook interactive
      const any = document.querySelector('[class*="action"], [data-action], .sb-action');
      if (any) { any.click(); return 'action-el'; }
      // click canvas center as fallback
      return 'none';
    });
    console.log('CLICK', clicked);
    if (clicked === 'none') {
      await page.mouse.click(640, 400);
      console.log('CLICK canvas center');
    }
    for (let i = 1; i <= frames; i++) {
      await new Promise(r => setTimeout(r, 1200));
      const dest = path.join(out, `v4_${tag}_${String(i).padStart(2,'0')}.png`);
      await page.screenshot({ path: dest });
      console.log('F', tag, i, fs.statSync(dest).size);
    }
    await page.close();
  }
  await run('mode-base-book--gunsmoke', 'gunsmoke', 28);
  await run('mode-base-book--split-gang', 'split', 28);
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
