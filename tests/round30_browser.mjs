/* Render final, admitted data. Screenshots still require a separate visual read. */
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.YM_PLAYWRIGHT_MODULE||'/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=fileURLToPath(new URL('../',import.meta.url));
const site=process.env.YM_SITE_FOLDER||'dist',port=Number(process.env.YM_SITE_PORT||8030);
const output=process.env.YM_QA_OUTPUT||'/tmp/yang-mills-round30-site-qa'; fs.mkdirSync(output,{recursive:true});
const server=spawn('python3',['-m','http.server',String(port),'--bind','127.0.0.1','--directory',path.join(root,site)],{stdio:'ignore'});
let browser;
try{
  await new Promise(resolve=>setTimeout(resolve,500));
  browser=await chromium.launch({headless:true,executablePath:process.env.YM_CHROMIUM_EXECUTABLE||'/tmp/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--no-zygote','--single-process']});
  const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1}),errors=[],checks=[];
  page.on('pageerror',error=>errors.push(String(error)));
  const base='http://127.0.0.1:'+port+'/'; await page.goto(base);
  const snapshot=await page.evaluate(()=>({completed:window.ResearchRound30?.counts().completed,loops:window.ROUND30_DATA?.loops.map(row=>({id:row.id,title:row.title,contribution_id:row.contribution_id,node_id:window.ROUND30_DATA.network.nodes.find(node=>node.route==='round30-'+row.id)?.id})),pdf:window.ROUND30_DATA?.draft.url,registry:window.ROUND30_DATA?.registry.contributions.length,networkNodes:window.ROUND30_DATA?.network.nodes.length,sources:window.ROUND30_DATA?.survey.length}));
  assert.equal(snapshot.completed,3,'complete reviewed data required');
  assert.equal(await page.locator('h1').count(),1);
  await page.screenshot({path:path.join(output,'home-desktop.png'),fullPage:true});
  await page.setViewportSize({width:390,height:844}); await page.screenshot({path:path.join(output,'home-mobile.png'),fullPage:true});
  const routes=['home','drafts','round30-results','round30-roadmap','round30-sources','round30-proof','round30-calculator','hnm-findings','hnm-priorities','research-network','round29','round29-aq2',...snapshot.loops.map(row=>'round30-'+row.id)];
  for(const route of routes){
    await page.goto(base+'#research/'+route);
    assert.equal(await page.locator('h1').count(),1,route);
    const heading=await page.locator('h1').textContent(),overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
    assert(heading.trim(),route); assert(!overflow,'mobile overflow '+route); checks.push({route,heading,mobileOverflow:overflow});
  }
  await page.goto(base+'#research/round30-sources'); await page.locator('#r30-source-search').fill('Newton');
  assert(await page.locator('.r30-source').count()>0); await page.locator('#r30-source-area').selectOption('modern');
  assert((await page.locator('#r30-source-count').textContent()).startsWith('0 of '));
  await page.locator('#r30-source-reset').click(); assert.equal(await page.locator('.r30-source').count(),snapshot.sources);
  await page.locator('#r30-source-search').fill('hnm30-historical-jung-automatisms');
  assert.equal(await page.locator('.r30-source').count(),1);
  await page.screenshot({path:path.join(output,'sources-mobile.png'),fullPage:true});
  await page.goto(base+'#research/hnm-findings'); await page.locator('#r29-finding-search').fill(snapshot.loops[0].contribution_id);
  assert.equal(await page.locator('.r29-finding').count(),1); await page.locator('.r29-finding').screenshot({path:path.join(output,'catalog-mobile.png')});
  await page.goto(base+'#research/research-network');
  assert.equal(await page.locator('#r29-network-selected').textContent(),snapshot.loops.at(-1).title);
  await page.locator('#r29-network-search').fill(snapshot.loops[0].node_id);
  assert.equal(await page.locator('#r29-network-selected').textContent(),snapshot.loops[0].title);
  assert(await page.locator('#r29-network-catalog button').count()>0); await page.locator('#r29-network-map-toggle').click(); assert(await page.locator('#r29-network-map').isHidden());
  await page.locator('#r29-network-map-toggle').click(); assert(await page.locator('#r29-network-map').isVisible());
  const centered=await page.locator('.r29-map-scroll').evaluate(element=>{const selected=element.querySelector('.r29-map-node[aria-pressed="true"]');const frame=element.getBoundingClientRect(),card=selected.getBoundingClientRect();return card.left>=frame.left-1&&card.right<=frame.right+1&&card.top>=frame.top-1&&card.bottom<=frame.bottom+1;});
  assert(centered,'selected network card must be visible on mobile');
  await page.locator('.r29-network-map-section').screenshot({path:path.join(output,'network-mobile.png')});
  await page.goto(base+'#research/round30-'+snapshot.loops[0].id); await page.screenshot({path:path.join(output,'result-mobile.png'),fullPage:true});
  await page.goto(base+'#research/round30-calculator');await page.locator('#r30-alpha').fill('2');await page.locator('[data-r30-preset="0"]').click();
  assert((await page.locator('#r30-calc-output').textContent()).includes('144'));
  await page.locator('#r30-tau').fill('0.1');await page.locator('#r30-certificate-form button[type=submit]').click();
  assert((await page.locator('#r30-calc-error').textContent()).includes('outside the reviewed interval'));assert.equal((await page.locator('#r30-calc-output').textContent()).trim(),'');
  await page.locator('#r30-alpha').fill('1');await page.locator('[data-r30-preset="-1e-8"]').click();
  assert.equal((await page.locator('#r30-calc-error').textContent()).trim(),'');await page.screenshot({path:path.join(output,'calculator-mobile.png'),fullPage:true});
  for(const asset of [snapshot.pdf,'ym-draft-02.pdf','hnm-registry-r30.json','hnm-spectral-certificates.png']){
    const response=await page.request.get(base+asset); assert.equal(response.status(),200,asset);
    if(asset.endsWith('.pdf'))assert.equal((await response.body()).subarray(0,5).toString(),'%PDF-',asset);
  }
  assert.equal(errors.length,0,errors.join('\n'));
  const receipt={status:'passed',date:new Date().toISOString(),site,viewports:[{width:1440,height:1100},{width:390,height:844}],checkpoint:snapshot,checks,pageErrors:errors,scope:'Rendered current/archive routes, no mobile page overflow, source filtering/reset, current contribution search, network controls, exact calculator interaction/domain rejection and downloadable assets. Screenshots require separate visual inspection.'};
  fs.writeFileSync(path.join(output,'site-qa.json'),JSON.stringify(receipt,null,2)+'\n'); console.log(JSON.stringify(receipt));
}finally{if(browser)await browser.close();server.kill();}
