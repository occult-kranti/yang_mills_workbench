import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const root=new URL('../',import.meta.url);
const read=p=>fs.readFileSync(new URL(p,root),'utf8');
let comparisons=0;
for(const folder of ['dist','docs']){
  const context={window:{ResearchObservatory:{render:r=>`legacy:${r}`,afterRender(){}}},location:{hash:'#research'},document:{title:''}};
  vm.createContext(context);
  for(const file of ['research-round23-data.js','research-round23.js'])vm.runInContext(read(`${folder}/${file}`),context);
  const R=context.window.ResearchRound23;
  assert.equal(R.data.completed,4);assert.equal(R.data.planned,10);
  assert.equal(R.data.cycle_complete,false);assert.equal(R.data.next_started,false);
  for(const x of R.data.loops){
    const bytes=read(`research/round23/advisor/${x.loop}-gate.json`),g=JSON.parse(bytes);
    assert.equal(x.gate_sha256,createHash('sha256').update(bytes).digest('hex'));
    for(const key of ['claim','scope','status','target_verdict','equations','independence','next_missing_premise'])assert.deepEqual(JSON.parse(JSON.stringify(x[key])),g[key]);
    const html=R.render('round23-'+x.loop);assert(html.includes(x.gate_sha256));assert(html.includes('Scientific priority remains unverified'));comparisons++;
  }
  const home=R.render('home'),next=R.render('round23-roadmap'),t2=R.render('round23-t2');
  for(const phrase of ['4<span>/ 10','one agent','one author','0.006','continuum problem remains open'])assert(home.includes(phrase),phrase);
  for(const phrase of ['planned, not started','no frozen contract','six reviewed','different model'])assert(next.includes(phrase),phrase);
  assert(t2.includes('single-agent self-review'));assert(t2.includes('Same-author obligation audit'));
  assert(R.render('round22-home').includes('legacy:home'));
  assert(R.render('journey').includes('Historical Round22 record'));
  assert.equal(R.render('plaquette'),'legacy:plaquette');
  R.data.loops[3].claim='<script>alert(1)</script>';
  assert(!R.render('round23-t2').includes('<script>'));
  R.afterRender();assert(context.document.title.startsWith('Round23'));
}
console.log(JSON.stringify({status:'passed',source_bound_loop_comparisons:comparisons,scope:'Node route, provenance, stop-boundary and escaping checks; no browser visual audit'}));
