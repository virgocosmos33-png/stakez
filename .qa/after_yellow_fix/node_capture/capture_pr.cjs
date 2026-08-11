const fs=require('fs');const path=require('path');const puppeteer=require('puppeteer-core');
(async()=>{
  const chrome='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const out='c:\\Users\\Emex33\\Documents\\tombstone reborn\\.qa\\after_yellow_fix';
  const bust=Date.now();
  const browser=await puppeteer.launch({executablePath:chrome,headless:'new',args:['--no-sandbox','--disable-gpu','--window-size=1280,800']});
  const page=await browser.newPage();
  await page.setViewport({width:1280,height:800});
  await page.setCacheEnabled(false);
  await page.goto(`http://localhost:6009/iframe.html?id=mode-base-book--split-gang&viewMode=story&v=${bust}`,{waitUntil:'networkidle0',timeout:180000}).catch(()=>{});
  await new Promise(r=>setTimeout(r,4000));
  await page.evaluate(()=>{const b=[...document.querySelectorAll('button')].find(x=>/action/i.test(x.textContent||'')); if(b)b.click();});
  for(let i=1;i<=12;i++){
    await new Promise(r=>setTimeout(r,1200));
    const dest=path.join(out,`postrestart_split_${String(i).padStart(2,'0')}.png`);
    await page.screenshot({path:dest});
    console.log('F',i,fs.statSync(dest).size);
  }
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
