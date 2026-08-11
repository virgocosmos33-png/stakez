const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const stories = [
    ["mode-base-book--split-gang", "split_gang.png"],
    ["mode-bonus-book--super-split", "super_split.png"],
  ];
  for (const [id, file] of stories) {
    const url = `http://localhost:6009/iframe.html?id=${id}&viewMode=story`;
    console.log("goto", id);
    await page.goto(url, { waitUntil: "networkidle", timeout: 120000 });
    // wait until Initializing disappears / canvas paints
    await page.waitForTimeout(12000);
    const out = `c:/Users/Emex33/Documents/tombstone reborn/.qa/${file}`;
    await page.screenshot({ path: out, fullPage: false });
    console.log("wrote", out);
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
