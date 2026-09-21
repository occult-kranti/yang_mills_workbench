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
  assert.equal(R.data.completed,6);assert.equal(R.data.planned,10);
  assert.equal(R.data.cycle_complete,false);assert.equal(R.data.next_started,false);
  for(const x of R.data.loops){
    const bytes=read(`research/round23/advisor/${x.loop}-gate.json`),g=JSON.parse(bytes);
    assert.equal(x.gate_sha256,createHash('sha256').update(bytes).digest('hex'));
    for(const key of ['claim','scope','status','target_verdict','equations','independence','next_missing_premise'])assert.deepEqual(JSON.parse(JSON.stringify(x[key])),g[key]);
    const html=R.render('round23-'+x.loop);assert(html.includes(x.gate_sha256));assert(html.includes('Scientific priority remains unverified'));comparisons++;
  }
  const home=R.render('home'),next=R.render('round23-roadmap'),t2=R.render('round23-t2');
  for(const phrase of ['6<span>/ 10','one agent','one author','Cη / 168','continuum problem remains open'])assert(home.includes(phrase),phrase);
  for(const phrase of ['planned, not started','no frozen contract','six reviewed','different model'])assert(next.includes(phrase),phrase);
  assert(t2.includes('single-agent self-review'));assert(t2.includes('Same-author obligation audit'));
  assert(t2.includes('0.006'));
  const u2=R.render('round23-u2');
  for(const phrase of ['Inconclusive','not a simulated correlation trajectory','Eight-link resonance','full mathematical derivation'])assert(u2.includes(phrase),phrase);
  assert(!u2.includes('NaN'));assert(!u2.includes('Infinity'));
  for(const id of ['newton','tesla']){
    const d=R.data.documents[id];assert.equal(d.sha256,createHash('sha256').update(read(d.path)).digest('hex'));
    assert(R.render(id).includes('Coverage'));assert(R.render(id).includes('https://'));
  }
  assert(R.render('newton').includes('Principles_of_Natural_Philosophy_(1729)/Rules_of_Reasoning_in_Philosophy'));
  assert(R.render('tesla').includes('anticipated mathematical demonstration'));
  assert(R.render('research-methods').includes('twenty selected source entries'));
  assert(R.render('round22-home').includes('legacy:home'));
  assert(R.render('journey').includes('Historical Round22 record'));
  assert.equal(R.render('plaquette'),'legacy:plaquette');
  R.data.loops[3].claim='<script>alert(1)</script>';
  assert(!R.render('round23-t2').includes('<script>'));
  R.afterRender();assert(context.document.title.startsWith('Round23'));
}
console.log(JSON.stringify({status:'passed',source_bound_loop_comparisons:comparisons,scope:'Node route, provenance, stop-boundary and escaping checks; no browser visual audit'}));
