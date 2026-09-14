import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { execFileSync } from 'node:child_process';

const root = new URL('../../', import.meta.url);
const dist = new URL('../../dist/', import.meta.url);
const index = fs.readFileSync(new URL('index.html', dist), 'utf8');
const scripts = [...index.matchAll(/<script src="(research[^\"]*\.js)"/g)].map(m => m[1]);
assert.equal(scripts.filter(s=>s==='research-round21.js').length,1);
assert(scripts.indexOf('research-round21.js')>scripts.indexOf('research-contributions.js'));
assert.equal((index.match(/href="research-round21.css"/g)||[]).length,1);
const nodes = new Map();
const node = key => {
  if(!nodes.has(key))nodes.set(key,{innerHTML:'',textContent:'',addEventListener(){},setAttribute(){},querySelector(){return node(key+' child');}});
  return nodes.get(key);
};
const ctx={console,URL,Blob,Math,location:{hash:'#research/home'},localStorage:{getItem(){return null;},setItem(){}},
  document:{title:'',querySelector:node,getElementById:id=>node('#'+id),addEventListener(){}},addEventListener(){}};
ctx.window=ctx;
vm.createContext(ctx);
let historical;
for(const script of scripts){
  if(script==='research-round21.js')historical=ctx.ResearchObservatory;
  vm.runInContext(fs.readFileSync(new URL(script,dist),'utf8'),ctx,{filename:script});
}
const current=ctx.ResearchRound21,D=current.data;
assert(current&&historical);
const loops=D.goals.flatMap(g=>g.loops);
assert.equal(loops.length,10);
assert.equal(new Set(loops.map(l=>l.id)).size,10);
assert.deepEqual(Array.from(D.goals,g=>g.id),['I','J','K','L','M']);
assert.equal(D.completed_research_loops,loops.filter(l=>l.gate_review.verified).length);
assert.equal(D.accepted_research_loops,loops.filter(l=>l.status==='accepted').length);
assert.equal(D.limited_research_loops,loops.filter(l=>l.status==='limited').length);
const routes=['home','contributions','round21-roadmap','round21-review','round21-variables',...loops.map(l=>'round21-'+l.id.toLowerCase())];
for(const route of routes){
  const html=ctx.ResearchObservatory.render(route);
  assert.equal((html.match(/<h1>/g)||[]).length,1,route+' one primary heading');
  assert(html.includes('aria-label="Round21 research navigation"'),route);
  assert(!html.includes('Research page not found'),route);
  assert(html.includes('#research/review20-home'),route+' keeps prior home accessible');
  assert(html.includes('#research/contributions20'),route+' keeps prior contributions accessible');
  ctx.location.hash='#research/'+route;
  ctx.ResearchObservatory.afterRender();
  assert(ctx.document.title.endsWith('Yang–Mills Workbench'),route);
}
for(const loop of loops){
  if(['accepted','limited'].includes(loop.status)){
    assert(loop.gate_review.verified,loop.id);
    assert(loop.gate_review.file_count>0,loop.id);
    assert.equal(loop.claim,loop.gate_review.claim,loop.id+' claim from gate');
    assert.equal(loop.scope,loop.gate_review.scope,loop.id+' scope from gate');
    assert.equal(loop.target_verdict,loop.gate_review.target_verdict,loop.id+' target verdict from gate');
    const html=current.render('round21-'+loop.id.toLowerCase());
    assert(html.includes('Target verdict'),loop.id+' verdict shown');
  }
}
for(const contribution of D.contributions){
  if(contribution.classification==='Supported model-specific result')assert(contribution.gate_review.verified,contribution.id);
}
const home=current.render('home');
assert(home.includes(`${D.completed_research_loops}<span>/ 10</span>`));
assert(home.includes('They do not measure progress toward a continuum mass-gap proof.'));
assert(home.includes('A successful validation supports its stated result.'));
assert(home.includes('Scientific priority')||current.render('contributions').includes('Scientific priority'));
assert.equal((home.match(/class="rc-goal"/g)||[]).length,5);
assert(home.includes('Four models. Keep their conclusions separate.'));
assert(current.render('round21-variables').includes('Every variable has a role.'));
for(const loop of loops){
  const html=current.render('round21-'+loop.id.toLowerCase());
  assert(html.includes('Variable definitions and units for '+loop.id));
  if(loop.reproduction){assert(loop.reproduction.includes('--loops '+loop.id.toLowerCase()));assert(!loop.reproduction.includes('--from-loop'));}
}

assert.equal((home.match(/<i class="rc-/g)||[]).length,10);
assert(current.render('round21-review').includes('interpreter caches cannot support an accepted label'));

// The wrapper preserves old route rendering byte-for-byte, except explicit aliases.
const historicalRoutes=['round20-roadmap','round20-review',...['d','e','f','g','h'].flatMap(g=>[1,2].map(i=>'round20-'+g+i)),
  'review19-home','paired-roadmap','paired-review','paired-a1','paired-c2','review18-home','review17-home'];
for(const route of historicalRoutes){
  assert.equal(current.render(route),historical.render(route),route+' delegates unchanged');
  assert(!current.render(route).includes('Research page not found'),route);
}
for(const [alias,original] of [['review20-home','home'],['contributions20','contributions']]){
  const html=current.render(alias);
  assert(html.includes('Round20 research record.'));
  const old=historical.render(original).replaceAll('href="#research/home"','href="#research/review20-home"').replaceAll('href="#research/contributions"','href="#research/contributions20"');
  assert(html.endsWith(old));
  ctx.location.hash='#research/'+alias;
  current.afterRender();
  assert(ctx.document.title.startsWith('Round20 research record'));
}
if(ctx.ResearchContributions.data.goals.flatMap(g=>g.loops).find(l=>l.id==='H1')?.gate_review.verified){
  const slider=node('#rc-h1-q');
  assert.equal(typeof slider.oninput,'function','archived calculator still binds');
  slider.value='0.9';slider.oninput();
  assert(node('#rc-h1-readout').innerHTML.includes('Certificate insufficient'));
  assert(!node('#rc-h1-readout').innerHTML.includes('gap / α ≥ -'));
  slider.value='0.5';slider.oninput();
  assert(node('#rc-h1-readout').innerHTML.includes('gap / α ≥ 0.112616'));
}
for(const route of ['__proto__','constructor','round21-z1','round21-i3'])assert(current.render(route).includes('Research page not found'),route+' does not create a page');

// Rendered prose, expressions, attribute values and URLs all need escaping.
assert.equal(current.format('alphabetical metadata'),'alphabetical metadata');
assert(current.format('<script>alpha <= beta</script>').includes('&lt;script&gt;α ≤ β&lt;/script&gt;'));
for(const invalid of ['javascript:alert(1)','data:text/html,<script>','https://user:pass@example.com/','/local'])assert.equal(current.safeUrl(invalid),'#research/round21-review');
const malicious='<img src=x onerror=alert(1)>';
D.title=malicious;
loops[0].claim=malicious;
loops[0].equations=[malicious];
loops[0].scope=malicious;
loops[0].derivation=[malicious];
loops[0].failure=malicious;
loops[0].workaround=malicious;
for(const route of ['home','round21-i1']){
  const html=current.render(route);
  assert(!html.includes(malicious),route);
  assert(html.includes('&lt;img src=x onerror=alert(1)&gt;'),route);
}

// Actual temporary files exercise the acceptance boundary, rather than mock it.
const py=String.raw`
import tempfile, pathlib, shutil, json, hashlib, importlib.util
real=pathlib.Path(${JSON.stringify(new URL('.',import.meta.url).pathname)})
with tempfile.TemporaryDirectory(prefix='ym21-site-integrity-') as td:
    root=pathlib.Path(td); r=root/'research/round21'; (r/'advisor').mkdir(parents=True)
    shutil.copy(real/'build_site.py',r/'build_site.py')
    spec=importlib.util.spec_from_file_location('fixture',r/'build_site.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    assert m.prepare()['completed_research_loops']==0
    assert len(m.prepare()['goals'])==5
    evidence=r/'evidence.txt'; evidence.write_text('reviewed fixture')
    rel='research/round21/evidence.txt'; sha=hashlib.sha256(evidence.read_bytes()).hexdigest()
    gate={'loop':'i1','status':'accepted','files':{rel:sha},'claim':'Authoritative statement','equations':['x = 1'],
          'scope':'Declared fixture only','target_verdict':'Original numerical threshold remains insufficient'}
    gate_path=r/'advisor/i1-gate.json'
    data={'goals':[{'id':'I','title':'Fixture','loops':[{'id':'I1','status':'accepted','gate':'advisor/i1-gate.json',
          'claim':'UNREVIEWED EDITORIAL CLAIM','equations':['x = 999'],'target_verdict':'Target solved','scope':'Every theory'}]}],
          'contributions':[{'id':'fixture','title':'Fixture','loop':'I1','claim':'UNREVIEWED CONTRIBUTION'}]}
    (r/'site-data.json').write_text(json.dumps(data))
    def write_gate(g=gate): gate_path.write_text(json.dumps(g))
    def reject(reason):
        out=m.prepare(); assert out['completed_research_loops']==0,reason
        assert out['goals'][0]['loops'][0]['status']=='running',reason
        assert out['contributions'][0]['classification']=='Candidate contribution',reason
    write_gate(); out=m.prepare(); loop=out['goals'][0]['loops'][0]
    assert out['completed_research_loops']==1
    assert loop['claim']==gate['claim'] and loop['equations']==gate['equations'] and loop['scope']==gate['scope']
    assert loop['target_verdict']==gate['target_verdict']
    assert out['contributions'][0]['claim']==gate['claim']
    gate['status']='limited'; write_gate(); assert m.prepare()['limited_research_loops']==1
    gate['status']='accepted'; write_gate()
    evidence.write_text('changed'); reject('changed source')
    evidence.unlink(); reject('missing source')
    evidence.write_text('reviewed fixture')
    for inventory in [{},{'evidence.txt':sha},{'/etc/passwd':sha},{'research/round21/../round21/evidence.txt':sha},
                      {'research/round21/__pycache__/check.pyc':sha},{rel:'invalid-digest'}]:
        write_gate({**gate,'files':inventory}); reject('invalid inventory')
    outside=root/'outside.txt'; outside.write_text('reviewed fixture'); (r/'escape.txt').symlink_to(outside)
    write_gate({**gate,'files':{'research/round21/escape.txt':sha}}); reject('escaping symlink')
    (r/'linked-parent').symlink_to(r,target_is_directory=True)
    linked_source=r/'linked-parent/evidence.txt'
    assert not linked_source.is_symlink() and linked_source.resolve().is_relative_to(root)
    assert hashlib.sha256(linked_source.read_bytes()).hexdigest()==sha
    write_gate({**gate,'files':{'research/round21/linked-parent/evidence.txt':sha}})
    reject('parent symlink stays inside repository but is not an admitted file path')
    assert not m.evidence('research/round21/linked-parent/evidence.txt')['exists']
    write_gate()
    linked_gate=m.verify_gate('linked-parent/advisor/i1-gate.json','i1')
    assert not linked_gate['verified'] and linked_gate['state']=='pending'
    for value in ['j1','I1',None]:
        write_gate({**gate,'loop':value}); reject('wrong or absent loop id')
    for field in ['claim','scope','target_verdict','equations']:
        invalid=dict(gate); invalid.pop(field); write_gate(invalid); reject('missing '+field)
    write_gate({**gate,'status':'solved'}); reject('unknown status')
    gate_path.write_text('{invalid-json'); reject('malformed JSON')
    gate_path.write_text('{"loop":"i1","loop":"i1"}'); reject('duplicate keys')
    write_gate()
    data['title']='</script><script>alert(1)</script>\u2028'
    (r/'site-data.json').write_text(json.dumps(data)); m.build()
    script=(root/'dist/research-round21.js').read_text()
    assert '</script><script>alert(1)' not in script and '\\u003c/script>' in script
    assert '\u2028' not in script
    data['goals'][0]['loops'].append(dict(data['goals'][0]['loops'][0]))
    (r/'site-data.json').write_text(json.dumps(data))
    try: m.prepare()
    except ValueError: pass
    else: raise AssertionError('Duplicate loop admitted')
    assert m.resolve_path('../../outside') is None
print('Source mutation, missing files, hashes, paths, final and parent symlinks, caches, gate fields, authoritative content, duplicate IDs and script boundaries passed.')
`;
const controls=execFileSync('python3',['-B','-c',py],{cwd:root,encoding:'utf8'});
console.log(JSON.stringify({routes:routes.length,historicalRoutes:historicalRoutes.length+2,loops:10,
  verified:D.completed_research_loops,sourceControls:controls.trim()}));
