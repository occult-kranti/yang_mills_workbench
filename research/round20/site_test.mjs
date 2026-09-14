import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { execFileSync } from 'node:child_process';

const root = new URL('../../', import.meta.url);
const dist = new URL('../../dist/', import.meta.url);
const index = fs.readFileSync(new URL('index.html', dist), 'utf8');
const scripts = [...index.matchAll(/<script src="(research[^\"]*\.js)"/g)].map(m => m[1]);
assert(scripts.indexOf('research-contributions.js') > scripts.indexOf('research-paired.js'));
assert(index.includes('research-contributions.css'));
const nodes = new Map();
const node = key => {
  if (!nodes.has(key)) nodes.set(key, { innerHTML:'', textContent:'', addEventListener(){}, querySelector(){return node(key+' child');} });
  return nodes.get(key);
};
const ctx = {
  console, URL, Blob, Math, location:{ hash:'#research/home' },
  localStorage:{ getItem(){return null;}, setItem(){} },
  document:{ title:'', querySelector:node, getElementById:id=>node('#'+id), addEventListener(){} },
  addEventListener(){}
};
ctx.window = ctx;
vm.createContext(ctx);
for (const file of scripts) vm.runInContext(fs.readFileSync(new URL(file,dist),'utf8'),ctx,{filename:file});
const D = ctx.ResearchContributions.data;
const pretty = ctx.ResearchContributions.displayFormula('epsilon_L = alpha |tau|; Gamma(S); hbar; ||P-P_L|| <= 1; x^2');
assert(pretty.includes('ε<sub>L</sub> = α |τ|'));
assert(pretty.includes('Γ(S); ℏ; ‖P-P<sub>L</sub>‖ ≤ 1; x<sup>2</sup>'));
assert.equal(ctx.ResearchContributions.displayFormula('alphabetical metadata'), 'alphabetical metadata');
assert(ctx.ResearchContributions.displayFormula('<script>alpha</script>').includes('&lt;script&gt;α&lt;/script&gt;'));
const loops = D.goals.flatMap(g => g.loops);
assert.equal(loops.length, 10);
assert.equal(new Set(loops.map(l=>l.id)).size, 10);
const routes = ['home','contributions','round20-roadmap','round20-review',...loops.map(l=>'round20-'+l.id.toLowerCase())];
for (const route of routes) {
  ctx.location.hash = '#research/'+route;
  const html = ctx.ResearchObservatory.render(route);
  assert.equal((html.match(/<h1>/g)||[]).length,1,route+' has a single h1');
  assert(!html.includes('Research page not found'),route);
  assert(html.includes('aria-label="Current research navigation"'),route);
  ctx.ResearchObservatory.afterRender();
  assert(ctx.document.title.endsWith('Yang–Mills Workbench'),route);
}
const home = ctx.ResearchObservatory.render('home');
assert(home.includes('What we can show.'));
assert(home.includes(`${D.completed_research_loops}<span>/ 10</span>`));
assert(home.includes('not progress toward a mass-gap proof'));
assert(home.includes('Fibonacci-inspired spirals'));
assert(home.includes('not a physical result'));
assert.equal((home.match(/class="rc-spiral-node /g)||[]).length,20);
assert.equal((home.match(/class="rc-goal"/g)||[]).length,5);
assert(home.includes('Scientific novelty requires a separate literature audit'));
for (const l of loops) {
  if (l.status === 'accepted') assert(l.gate_review.verified && l.gate_review.source.sha256 && l.gate_review.file_count>0,l.id);
}
assert.equal(D.accepted_research_loops,loops.filter(l=>l.status==='accepted').length);
const baseline=ctx.ResearchContributions.h1Value(.5);
assert(Math.abs(baseline.budget-107/135)<1e-14);
assert(Math.abs(baseline.margin-973/8640)<1e-14);
assert(ctx.ResearchContributions.h1Value(.9).margin<0);
assert.throws(()=>ctx.ResearchContributions.h1Value(1));
if (loops.find(l=>l.id==='H1')?.gate_review.verified) {
  ctx.location.hash='#research/round20-roadmap';
  const initial=ctx.ResearchObservatory.render('round20-roadmap');
  assert(initial.includes('973/8640'));
  assert(initial.includes('0.764003 &lt; qcrit &lt; 0.764004'));
  assert(initial.includes('gap / α ≥ 0.112616'));
  ctx.ResearchObservatory.afterRender();
  const slider=node('#rc-h1-q');
  assert.equal(typeof slider.oninput,'function');
  slider.value='0.9';slider.oninput();
  assert(node('#rc-h1-readout').innerHTML.includes('Certificate insufficient'));
  assert(node('#rc-h1-readout').innerHTML.includes('does not establish physical gap closure'));
  assert(!node('#rc-h1-readout').innerHTML.includes('gap / α ≥ -'));
  assert(node('#rc-h1-plot').innerHTML.includes('q 0.900'));
  slider.value='0.5';slider.oninput();
  assert(node('#rc-h1-readout').innerHTML.includes('gap / α ≥ 0.112616'));
  assert.equal(node('#rc-h1-q-value').textContent,'0.500');
  slider.value='0.9';slider.oninput();
  assert.equal(ctx.ResearchObservatory.render('round20-roadmap'),initial,'Route re-render deterministically returns to declared baseline');
  assert(ctx.ResearchObservatory.render('contributions').includes('id="rc-h1-q"'));
}
for (const c of D.contributions || []) {
  if(c.classification==='accepted within model') assert(c.gate_review.verified,c.id);
  assert(['accepted within model','candidate hypothesis','known method','obstruction'].includes(c.classification));
}
if ((D.contributions || []).some(c=>c.loop==='F2')) {
  assert(home.includes('Conditional three-link space SU(2)^3'));
  assert(home.includes('No equivalence to a gauge fixing of the full unfixed graph is proved'));
  assert(ctx.ResearchObservatory.render('round20-f2').includes('Conditional three-link space SU(2)^3'));
  assert(ctx.ResearchObservatory.render('contributions').includes('f-conditional-space-clarification.md'));
  const e2=(D.contributions || []).find(c=>c.loop==='E2');
  const f2=(D.contributions || []).find(c=>c.loop==='F2');
  if(e2)assert(home.indexOf('id="contribution-'+e2.id+'"')<home.indexOf('id="contribution-'+f2.id+'"'));
}
if ((D.contributions || []).some(c=>c.loop==='H2')) {
  const h2=D.contributions.find(c=>c.loop==='H2');
  assert(home.includes('id="contribution-'+h2.id+'"'));
}
assert(!/\/blob\/(?:research\/round19-paired|research\/round20)/.test(home),'Current dashboard evidence links use main');
const old = ctx.ResearchObservatory.render('review19-home');
assert(old.includes('Round19 research record'));
assert.equal((old.match(/class="paired-card /g)||[]).length,6);
assert(old.includes('Round19 home'));
for (const r of ['paired-a1','paired-a2','paired-b1','paired-b2','paired-c1','paired-c2','paired-roadmap','paired-review','review18-home','review17-home']) {
  const html=ctx.ResearchObservatory.render(r);
  assert(!html.includes('Research page not found'),r+' still resolves');
  assert(!html.includes('Current research navigation'),r+' delegates to its historical renderer');
}
assert(ctx.ResearchObservatory.render('__proto__').includes('Research page not found'));
assert(ctx.ResearchObservatory.render('round20-z1').includes('Research page not found'));

// Escaping is exercised with data, including the inline standalone script boundary.
D.title='<img src=x onerror=alert(1)>';
const escaped=ctx.ResearchObservatory.render('home');
assert(escaped.includes('&lt;img src=x onerror=alert(1)&gt;'));
assert(!escaped.includes('<img src=x onerror=alert(1)>'));

// Render the generated standalone without loading legacy research bundles.
const standalone=fs.readFileSync(new URL('overview.html',import.meta.url),'utf8');
assert(!standalone.includes('<script src='));
const standaloneCtx={console,URL,Math,location:{hash:'#research/home'},document:{title:'',getElementById(){return {innerHTML:''};}},addEventListener(){},scrollTo(){}};
standaloneCtx.window=standaloneCtx;
vm.createContext(standaloneCtx);
for(const m of standalone.matchAll(/<script>([\s\S]*?)<\/script>/g))vm.runInContext(m[1],standaloneCtx);
assert(standaloneCtx.ResearchContributions.render('round20-roadmap').includes('Five goals, ten research loops.'));

// A copied build fixture proves an accepted label cannot survive stale/missing evidence.
const py = String.raw`
import tempfile, pathlib, shutil, json, hashlib, importlib.util
real=pathlib.Path(${JSON.stringify(new URL('.',import.meta.url).pathname)})
with tempfile.TemporaryDirectory(prefix='ym20-ui-gates-') as td:
    root=pathlib.Path(td); r=root/'research/round20'; (r/'advisor').mkdir(parents=True)
    shutil.copy(real/'build_site.py',r/'build_site.py')
    shutil.copy(real/'site-content.json',r/'site-content.json')
    source=r/'evidence.txt'; source.write_text('reviewed scientific fixture')
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    gate={'loop':'d1','status':'accepted','files':{'evidence.txt':sha}}
    (r/'advisor/d1-gate.json').write_text(json.dumps(gate))
    data={'goals':[{'id':'D','title':'Fixture','loops':[{'id':'D1','status':'accepted','gate':'advisor/d1-gate.json'}]}],
          'contributions':[{'id':'fixture','title':'Gate fixture','classification':'accepted within model','loop':'D1'}]}
    (r/'site-data.json').write_text(json.dumps(data))
    spec=importlib.util.spec_from_file_location('fixture',r/'build_site.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    d=m.prepare(); assert d['accepted_research_loops']==1; assert d['contributions'][0]['classification']=='accepted within model'
    source.write_text('changed after review')
    d=m.prepare(); assert d['accepted_research_loops']==0; assert d['goals'][0]['loops'][0]['status']=='running'; assert d['contributions'][0]['classification']=='candidate hypothesis'
    source.unlink()
    d=m.prepare(); assert d['accepted_research_loops']==0; assert 'Missing source' in d['goals'][0]['loops'][0]['gate_review']['problems'][0]
    gate['files']={}; (r/'advisor/d1-gate.json').write_text(json.dumps(gate))
    assert m.prepare()['accepted_research_loops']==0
    gate['files']={'evidence.txt':sha}; gate['loop']='e2'; source.write_text('reviewed scientific fixture'); (r/'advisor/d1-gate.json').write_text(json.dumps(gate))
    assert m.prepare()['accepted_research_loops']==0
    assert m.resolve_path('../../../../outside') is None
print('Source mutation, missing inventory, wrong loop and path controls passed.')
`;
const gateOutput=execFileSync('python',['-c',py],{cwd:root,encoding:'utf8'});
console.log(JSON.stringify({routes:routes.length,historicalRoutes:11,loops:loops.length,accepted:D.accepted_research_loops,c2:D.c2.status,sourceControls:gateOutput.trim()}));
