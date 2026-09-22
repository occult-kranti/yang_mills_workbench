/* Real browser interactions against the completed source-bound Round31 site. */
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.YM_PLAYWRIGHT_MODULE||'/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=fileURLToPath(new URL('../',import.meta.url));
const site=process.env.YM_SITE_FOLDER||'docs',port=Number(process.env.YM_SITE_PORT||8031);
const output=process.env.YM_QA_OUTPUT||'/tmp/yang-mills-round31-site-qa';fs.mkdirSync(output,{recursive:true});
const serverArgs=site==='docs'?['scripts/preview_pages.py','--port',String(port)]:['-m','http.server',String(port),'--bind','127.0.0.1','--directory',path.join(root,site)];
const server=spawn('python3',serverArgs,{cwd:root,stdio:'ignore'});
let browser;
try{
  await new Promise(resolve=>setTimeout(resolve,500));
  browser=await chromium.launch({headless:true,executablePath:process.env.YM_CHROMIUM_EXECUTABLE||'/tmp/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-vulkan','--no-zygote','--single-process']});
  const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1}),errors=[],checks=[];
  page.on('pageerror',error=>errors.push(String(error)));
  const prefix=site==='docs'?JSON.parse(fs.readFileSync(path.join(root,'docs/build-manifest.json'),'utf8')).base:'/';
  const base='http://127.0.0.1:'+port+prefix;await page.goto(base);
  const snapshot=await page.evaluate(()=>({completed:window.ROUND31_DATA?.progress.completed,loops:window.ROUND31_DATA?.loops.map(row=>({id:row.id,title:row.title,contribution_id:row.contribution_id})),pdf:window.ROUND31_DATA?.addendum.url,sources:window.ROUND31_DATA?.survey.length,networkNodes:window.ROUND31_DATA?.network.nodes.length}));
  assert.equal(snapshot.completed,3,'three reviewed loops required');assert.equal(await page.locator('h1').count(),1);
  await page.screenshot({path:path.join(output,'home-desktop.png'),fullPage:true});
  await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(output,'home-mobile.png'),fullPage:true});
  const routes=['home','drafts','round31-results','round31-roadmap','round31-sources','round31-calculator','hnm-findings','research-network','round30-results','round30-at3',...snapshot.loops.map(row=>'round31-'+row.id)];
  for(const route of routes){
    await page.goto(base+'#research/'+route);assert.equal(await page.locator('h1').count(),1,route);
    const heading=await page.locator('h1').textContent(),overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
    assert(heading.trim(),route);assert(!overflow,'mobile overflow '+route);checks.push({route,heading,mobileOverflow:overflow});
  }
  await page.goto(base+'#research/round31-sources');await page.locator('#r31-source-search').fill('Newton');
  assert(await page.locator('.r31-source').count()>0);await page.locator('#r31-source-area').selectOption('modern');
  assert.equal(await page.locator('.r31-source').count(),0);await page.locator('#r31-source-reset').click();assert.equal(await page.locator('.r31-source').count(),snapshot.sources);
  await page.locator('#r31-source-search').fill('cryptomnesia');assert(await page.locator('.r31-source').count()>0);
  await page.screenshot({path:path.join(output,'sources-mobile.png'),fullPage:true});
  await page.goto(base+'#research/hnm-findings');await page.locator('#r31-finding-search').fill(snapshot.loops[0].contribution_id);
  assert.equal(await page.locator('#r31-finding-cards article').count(),1);await page.locator('#r31-finding-cards').screenshot({path:path.join(output,'catalog-mobile.png')});
  await page.locator('#r31-finding-reset').click();await page.locator('#r31-finding-round').selectOption('31');assert.equal(await page.locator('#r31-finding-cards article').count(),3);
  await page.goto(base+'#research/research-network');await page.locator('#r31-network-search').fill('r31-at4');
  await page.locator('#r31-network-catalog [data-r31-node="r31-at4"]').click();assert.equal(await page.locator('#r31-network-selected').textContent(),snapshot.loops[0].title);
  assert((await page.locator('#r31-network-details').textContent()).includes('Direct relations'));await page.locator('#r31-network-details').screenshot({path:path.join(output,'network-mobile.png')});
  await page.goto(base+'#research/round31-at6');assert.equal(await page.locator('.r31-source-inventory').getAttribute('open'),null);await page.screenshot({path:path.join(output,'result-mobile.png'),fullPage:true});
  await page.goto(base+'#research/round31-calculator');
  assert((await page.locator('[data-r31-recorded-radius]').textContent()).includes('8.086'));
  const recordedBefore=await page.locator('[data-r31-recorded-datum]').textContent();
  await page.locator('[data-r31-preset="cap"]').click();assert((await page.locator('#r31-preview-output').textContent()).includes('model-error sum exceeds'));
  await page.locator('[data-r31-preset="old-cutoff"]').click();assert((await page.locator('#r31-preview-output').textContent()).includes('model-error sum exceeds'));
  await page.locator('[data-r31-preset="zero"]').click();assert((await page.locator('#r31-preview-output').textContent()).includes('model-comparison error is zero'));
  await page.locator('#r31-s').fill('0');await page.locator('#r31-preview-form button[type=submit]').click();
  assert((await page.locator('#r31-preview-error').textContent()).includes('positive'));assert.equal((await page.locator('#r31-preview-output').textContent()).trim(),'');
  await page.locator('[data-r31-preset="certified"]').click();assert((await page.locator('#r31-preview-output').textContent()).includes('model-error sum is below'));
  assert.equal(await page.locator('[data-r31-recorded-datum]').textContent(),recordedBefore,'preview must not rewrite recorded certificate');
  assert(await page.locator('.r31-table-wrap').evaluateAll(elements=>elements.every(el=>el.scrollWidth<=el.clientWidth+1)),'numeric tables must fit the mobile column');
  await page.screenshot({path:path.join(output,'calculator-mobile.png'),fullPage:true});
  for(const asset of [snapshot.pdf,'ym-draft-03.pdf']){
    const response=await page.request.get(base+asset);assert.equal(response.status(),200,asset);assert.equal((await response.body()).subarray(0,5).toString(),'%PDF-',asset);
  }
  assert.equal(errors.length,0,errors.join('\n'));
  const receipt={status:'passed',date:new Date().toISOString(),site,viewports:[{width:1440,height:1100},{width:390,height:844}],checkpoint:snapshot,checks,pageErrors:errors,scope:'Real browser current/archive routes, mobile overflow, source and contribution filters, network relations, calculator interaction and exact PDF assets. Visual inspection is recorded separately.'};
  fs.writeFileSync(path.join(output,'site-qa.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt));
}finally{if(browser)await browser.close();server.kill();}
