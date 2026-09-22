/* Optional rendered QA. Install Playwright and its Chromium, or provide the two YM_* paths. */
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.YM_PLAYWRIGHT_MODULE||'playwright');
const root=fileURLToPath(new URL('../',import.meta.url));
const output=process.env.YM_QA_OUTPUT||'/tmp/yang-mills-round29-site-qa';fs.mkdirSync(output,{recursive:true});
const server=spawn('python3',['-m','http.server','8013','--bind','127.0.0.1','--directory',path.join(root,'docs')],{stdio:'ignore'});
let browser;
try{
 await new Promise(resolve=>setTimeout(resolve,500));
 browser=await chromium.launch({headless:true,...(process.env.YM_CHROMIUM_EXECUTABLE?{executablePath:process.env.YM_CHROMIUM_EXECUTABLE}:{}),args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--no-zygote','--single-process']});
 const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1});const errors=[],checks=[];
 page.on('pageerror',error=>errors.push(String(error)));
 await page.goto('http://127.0.0.1:8013/');
 assert.equal(await page.locator('h1').count(),1);
 await page.screenshot({path:path.join(output,'home-desktop.png'),fullPage:true});
 const snapshot=await page.evaluate(()=>({completed:window.ROUND29_DATA.progress.completed,registry:window.ROUND29_DATA.registry.contributions.length,equations:(window.ROUND29_DATA.registry.equations||[]).length,quantities:(window.ROUND29_DATA.registry.quantities||[]).length,networkNodes:window.ROUND29_DATA.network.nodes.length,statements:(window.ROUND29_DATA.registry.statements||[]).length,ak2Extensions:(window.ROUND29_DATA.registry.contributions.find(x=>x.id==='HNM-C-AK2')?.current_extensions||[]).length,am2Extensions:(window.ROUND29_DATA.registry.contributions.find(x=>x.id==='HNM-C-AM2')?.current_extensions||[]).length,loopRoutes:window.ROUND29_DATA.loops.map(x=>'round29-'+x.id),pdf:window.ROUND29_DATA.addendum?.url}));
 await page.setViewportSize({width:390,height:844});
 await page.screenshot({path:path.join(output,'home-mobile.png'),fullPage:true});
 const routes=['home','hnm-priorities','hnm-findings','research-network','round29-results','round29-sources','round29-roadmap','round29-proof','drafts','sharing','round28-home','round28-ak2',...snapshot.loopRoutes];
 for(const route of routes){
  await page.goto('http://127.0.0.1:8013/#research/'+route);
  const heading=await page.locator('h1').first().textContent();
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
  assert(heading.trim(),route);assert(!overflow,'page overflow: '+route);checks.push({route,heading,mobileOverflow:overflow});
 }
 await page.goto('http://127.0.0.1:8013/#research/hnm-findings');await page.locator('#r29-finding-search').fill('HNM-C-AK2');
 assert.equal(await page.locator('.r29-finding').count(),1);assert((await page.locator('#r29-finding-count').textContent()).startsWith('1 of '));
 if(snapshot.ak2Extensions)assert.equal(await page.locator('.r29-current-extensions').count(),1);
 await page.locator('.r29-finding').screenshot({path:path.join(output,'catalog-mobile.png')});
 if(snapshot.statements){
  await page.locator('#r29-finding-search').fill('HNM-T-AM2');assert.equal(await page.locator('.r29-finding').count(),1);
  await page.locator('.r29-statements summary').first().click();assert((await page.locator('.r29-statements details[open]').textContent()).includes('Scope:'));
  if(snapshot.am2Extensions)assert.equal(await page.locator('.r29-current-extensions').count(),1);
  await page.locator('.r29-finding').screenshot({path:path.join(output,'statement-mobile.png')});
 }
 if(snapshot.am2Extensions){
  await page.goto('http://127.0.0.1:8013/#research/round29-am2');assert.equal(await page.locator('.r29-current-extensions').count(),1);
 }
 if(snapshot.ak2Extensions){
  await page.goto('http://127.0.0.1:8013/#research/round28-ak2');assert(await page.locator('.r29-alias-notice .r29-current-extensions').count()>0);
 }
 await page.goto('http://127.0.0.1:8013/#research/research-network');await page.locator('#r29-network-search').fill('AK2');
 assert((await page.locator('#r29-network-count').textContent()).includes('match'));
 await page.locator('#r29-network-map-toggle').click();assert(await page.locator('#r29-network-map').isHidden());
 await page.locator('#r29-network-map-toggle').click();assert(await page.locator('#r29-network-map').isVisible());
 await page.locator('#r29-network-reset').click();assert.equal(await page.locator('#r29-network-search').inputValue(),'');
 await page.screenshot({path:path.join(output,'network-mobile.png'),fullPage:true});
 if(snapshot.pdf){const response=await page.request.get('http://127.0.0.1:8013/'+snapshot.pdf);assert.equal(response.status(),200);assert.equal((await response.body()).subarray(0,5).toString(),'%PDF-');}
 assert.equal(errors.length,0);
 const receipt={status:'passed',date:new Date().toISOString(),scope:'Rendered desktop home and mobile current/archive routes, no page overflow, registry search, network search/reset/map visibility, PDF asset when present. Screenshots require separate visual inspection.',viewports:[{width:1440,height:1100},{width:390,height:844}],checkpoint:snapshot,checks,pageErrors:errors};
 fs.writeFileSync(path.join(output,'site-qa.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt));
}finally{if(browser)await browser.close();server.kill();}
