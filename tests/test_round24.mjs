import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const root=new URL('../',import.meta.url),read=p=>fs.readFileSync(new URL(p,root),'utf8');
let checked=0;
const expected=['v1','v2','w1','w2','x1','x2','y1','y2','z1','z2'];
for(const folder of ['dist','docs']){
 const context={window:{ResearchObservatory:{render:r=>'archive:'+r,afterRender(){}}},location:{hash:'#research'},document:{title:''}};
 vm.createContext(context);
 for(const file of ['research-round24-data.js','research-round24.js'])vm.runInContext(read(`${folder}/${file}`),context);
 const R=context.window.ResearchRound24;assert.equal(R.data.loops.length,10);
 assert.deepEqual(Array.from(R.data.loops,x=>x.loop),expected);
 const index=read(`${folder}/index.html`),scripts=Array.from(index.matchAll(/<script\s+src="([^"]+)"/g),m=>m[1].split('/').pop());
 const sequence=['research-round23.js','research-round24-data.js','research-round24.js','app.js'];
 assert(sequence.every(x=>scripts.filter(s=>s===x).length===1),'real index must load each active script exactly once');
 assert(sequence.every((x,i)=>i===0||scripts.indexOf(sequence[i-1])<scripts.indexOf(x)),'Round24 must wrap Round23 before app startup');
 for(const row of R.data.loops){
  const path=`research/round24/advisor/${row.loop}-gate.json`,bytes=read(path),g=JSON.parse(bytes);
  assert.equal(row.gate_sha256,createHash('sha256').update(bytes).digest('hex'));assert.equal(row.verdict,g.verdict);
  const page=R.render('round24-'+row.loop);assert(page.includes(row.gate_sha256));assert(page.includes('Read the independent reverse reconstruction'));assert(page.includes('Scientific priority remains unverified'));
  for(const e of row.equations)assert(page.includes(e.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;')));
  checked++;
 }
 const home=R.render('home');assert(home.includes('10<span>/ 10'));assert(home.includes('not the fraction of Yang'));assert(home.includes('continuum problem remains open'));
 assert(R.render('round24-roadmap').includes('planned and unexecuted'));
 assert(R.render('round23-home').includes('Historical six-loop checkpoint'));assert(R.render('round23-roadmap').includes('superseded'));
 assert.equal(R.render('newton'),'archive:newton');assert.equal(R.render('tesla'),'archive:tesla');
 R.data.loops[0].title='<script>bad()</script>';assert(!R.render('round24-v1').includes('<script>bad()'));
 R.afterRender();assert(context.document.title.startsWith('Round24'));
}
console.log(JSON.stringify({status:'passed',source_bound_loop_comparisons:checked,scope:'routes, evidence hashes, disclosure, archives and escaping'}));
