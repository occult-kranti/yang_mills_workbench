import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const root=new URL('../',import.meta.url);
const read=p=>fs.readFileSync(new URL(p,root),'utf8');
const rational=s=>{const[a,b='1']=String(s).split('/');return Number(a)/Number(b);};
const fixture=JSON.parse(read('research/round22/forward/n1/output/results.json'));
const close=(a,b,label)=>assert(Math.abs(a-b)<=Math.abs(b)*2e-10+1e-14,label);
let comparisons=0;
for(const folder of ['dist','docs']){
  const context={window:{ResearchObservatory:{render:r=>`legacy:${r}`,afterRender:()=>{}}}};
  vm.createContext(context);
  vm.runInContext(read(`${folder}/research-round22-data.js`),context);
  vm.runInContext(read(`${folder}/research-round22.js`),context);
  const R=context.window.ResearchRound22;
  assert.equal(R.data.completed,10);
  assert.equal(R.data.next.goals.length,3);
  assert.equal(R.data.next.executed,false);
  assert.deepEqual(Array.from(R.data.loops,x=>x.loop),['n1','n2','o1','o2','p1','p2','q1','q2','r1','r2']);
  for(const row of fixture.exact_profile_checks_eta_half){
    const q=rational(row.q),b=R.evaluateBound(q,3);
    close(b.D_local,rational(row.complete_local_budget),'exact incident face budget');
    close(b.state,6*Math.sqrt(rational(row.d_certificate_squared)),'rank-one state bound');
    close(b.support,rational(row.gamma3_dynamic_certificate),'endpoint dynamic certificate');
    close(b.total,b.state+b.support,'sum of admitted terms');
    assert.equal(b.certified,false);
    comparisons++;
  }
  for(const[q,gamma]of[[0,0],[1,0],[NaN,0],[.9,-1],[.9,Infinity],[true,0]])
    assert.throws(()=>R.evaluateBound(q,gamma),{name:'RangeError'});
  assert.equal(R.evaluateBound(.99,2.5).certified,true);
  for(const x of R.data.loops){
    const bytes=read(`research/round22/advisor/${x.loop}-gate.json`),gate=JSON.parse(bytes);
    assert.equal(x.gate_sha256,createHash('sha256').update(bytes).digest('hex'));
    for(const key of ['status','claim','scope','equations','target_verdict','next_missing_premise','independence'])
      assert.deepEqual(JSON.parse(JSON.stringify(x[key])),gate[key],`${x.loop}: actual gate ${key}`);
    const html=R.render('round22-'+x.loop);
    for(const phrase of ['Original question','Supported statement','Skeptical objection','Reproduce','Scientific priority remains unverified'])assert(html.includes(phrase),x.loop+': '+phrase);
    assert(html.includes(x.gate_sha256));
    assert(html.includes('r22-proposed'));
    assert(html.includes(`research/round22/skeptic/${x.loop}.md`));
    assert(x.steps.length>=3);
  }
  const html=R.render('journey');
  assert.equal((html.match(/data-r22-go=/g)||[]).length,5);
  for(const id of ['N','O','P','Q','R'])assert(html.includes(`id="r22-chapter-${id}"`));
  assert(!html.includes('href="#r22-chapter-'),'chapter controls must not replace the application route');
  assert(html.includes('continuum problem remains open'));
  assert(html.includes('actual nonconvergence'));
  assert(R.render('round21-home').includes('legacy:home'));
  assert(R.render('journey21').includes('legacy:journey'));
  assert.equal(R.render('round21-m2'),'legacy:round21-m2');
  let cleanups=0,delegations=0,reduced=true;
  const eventNode=(value='')=>({value,events:{},addEventListener(name,handler){this.events[name]=handler;}});
  const input=eventNode('.9'),gamma=eventNode('2.5'),qLabel={},readout={};
  const chapter={focus(options){this.focused=options;},scrollIntoView(options){this.scrolled=options;}};
  const button={...eventNode(),dataset:{r22Go:'Q'}};
  const nodes={'r22-q':input,'r22-gamma':gamma,'r22-q-value':qLabel,'r22-bound-output':readout,'r22-chapter-Q':chapter};
  context.document={title:'',querySelectorAll:()=>[button],getElementById:id=>nodes[id]};
  context.location={hash:'#research/journey'};
  context.window.matchMedia=()=>({matches:reduced});
  context.window.ResearchJourney={cleanup:()=>cleanups++};
  context.window.ResearchObservatory.afterRender();
  assert.equal(cleanups,1);
  assert(readout.innerHTML.includes(R.evaluateBound(.9,2.5).total.toPrecision(5)));
  button.events.click();
  assert.equal(chapter.focused.preventScroll,true);
  assert.equal(chapter.scrolled.behavior,'instant');
  assert.equal(context.location.hash,'#research/journey');
  reduced=false;button.events.click();assert.equal(chapter.scrolled.behavior,'smooth');
  input.value='.99';input.events.input();assert.equal(qLabel.textContent,'0.990');
  assert(readout.innerHTML.includes(R.evaluateBound(.99,2.5).total.toPrecision(5)));
  gamma.value='3';gamma.events.change();
  assert(readout.innerHTML.includes('actual nonconvergence is not implied'));
  assert(readout.innerHTML.includes(R.evaluateBound(.99,3).total.toPrecision(5)));
  context.location.hash='#research/round21-home';R.afterRender();
  assert.equal(context.document.title,'Round21 research record · Yang–Mills Workbench');
  assert.equal(cleanups,2);

  // Exercise the real archived renderers, including their generic navigation links.
  const historic={window:{ResearchObservatory:{render:r=>`base:${r}`,afterRender:()=>delegations++}},URL,
    location:{hash:'#research/journey21'},document:{querySelector:()=>null}};
  vm.createContext(historic);
  for(const name of ['research-round21.js','research-journey.js','research-round22-data.js','research-round22.js'])
    vm.runInContext(read(`${folder}/${name}`),historic);
  for(const route of ['round21-home','round21-contributions','round21-m2','journey21']){
    const archive=historic.window.ResearchRound22.render(route);
    assert(archive.includes('href="#research/round21-contributions"'),route+' historical contributions');
    assert(!archive.includes('href="#research/contributions"'),route+' must preserve archive navigation');
  }
  const archivedHome=historic.window.ResearchRound22.render('round21-home');
  assert(archivedHome.includes('href="#research/home"'), 'explicit current return remains available');
  assert(archivedHome.includes('href="#research/journey21"'), 'historical journey invitation');
  historic.window.ResearchRound22.afterRender();
  assert.equal(delegations,1,'historical journey delegates after cleanup when its DOM is absent');
}
for(const name of ['research-round22.js','research-round22.css','research-round22-data.js'])assert.equal(read('dist/'+name),read('docs/'+name));
console.log(JSON.stringify({status:'passed',fixture_comparisons:comparisons,checks:['N1 exact face/state/endpoint evidence','All ten pages match actual gate bytes and statements','Archived navigation and cleanup delegation','Chapter focus, motion preference and hash preservation','Calculator initial/input/change behavior','Invalid parameters and endpoint scope','Identical Pages assets'],research_loops_added:0},null,2));
