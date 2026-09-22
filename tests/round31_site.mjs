/* Renderer fixtures are explicitly synthetic and remain in memory.
 * Real bundle and gate checks run when the release bundle exists, or are required
 * by --require-release. No fake completed research bundle is written or built.
 */
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const root=fileURLToPath(new URL('../',import.meta.url));
const path=name=>new URL('../'+name,import.meta.url);
const read=name=>fs.readFileSync(path(name),'utf8');
const hash=name=>crypto.createHash('sha256').update(fs.readFileSync(path(name))).digest('hex');
const renderer=read('dist/research-round31.js');
const fixture={
  schema:'hnm-round31-presentation-v1',author:'Hruday N M (BUNZEEY)',
  summary:'SYNTHETIC RENDERER FIXTURE: not scientific results.',
  scope_statement:'SYNTHETIC scope text.',progress:{requested:3,completed:3,cycle_complete:true},
  loops:['at4','at5','at6'].map((id,index)=>({id,sequence:index+1,title:`SYNTHETIC ${id} title`,stage:'reviewed',verdict:'accepted_within_scope',accepted:`SYNTHETIC ${id} accepted text`,summary:`SYNTHETIC ${id} summary`,model:'SYNTHETIC model',limitations:['SYNTHETIC limitation'],contribution_id:`HNM-C-${id.toUpperCase()}`,derivation_steps:['SYNTHETIC step'],applications:['SYNTHETIC application'],gate_path:`research/round31/advisor/${id}-gate.json`,gate_sha256:'a'.repeat(64),reviewer_path:`research/round31/skeptic/${id}.md`,sources:[`research/round31/advisor/${id}-gate.json`]})),
  roadmap:{goals:[{id:'future',title:'SYNTHETIC future target',status:'planned_not_executed',target:'SYNTHETIC target'}]},
  survey:[{id:'synthetic-jung',area:'jung',title:'SYNTHETIC unread source',url:'https://example.test/primary',reading_depth:'Unread synthetic fixture',provenance:'SYNTHETIC record',use:'SYNTHETIC use',limits:'Inaccessible synthetic record',ledger:'research/round31/experts/jung/sources.json',passages:['SYNTHETIC section']},{id:'synthetic-modern',area:'modern',title:'SYNTHETIC modern source',url:'https://example.test/paper',reading_depth:'Selected synthetic passages',ledger:'research/round31/experts/modern/sources.json'}],
  network:{nodes:['at4','at5','at6'].map(id=>({id:'synthetic-'+id,title:'SYNTHETIC '+id,kind:'result',status:'accepted',route:'round31-'+id,summary:'SYNTHETIC node summary',sources:[`research/round31/advisor/${id}-gate.json`]})),edges:[{from:'synthetic-at4',to:'synthetic-at5',type:'proven-dependency',label:'SYNTHETIC relation'}]},
  addendum:{path:'papers/round31-addendum/main.pdf',url:'ym-round31-addendum.pdf',title:'SYNTHETIC addendum'},
  previous_draft:{path:'papers/draft-03/main.pdf',url:'ym-draft-03.pdf',title:'SYNTHETIC preserved draft'},
  registry:{contributions:[{id:'HNM-C-OLD',display_name:'SYNTHETIC old contribution',round:30,summary:'SYNTHETIC preserved summary',source_paths:['papers/draft-03/registry/hnm-registry.json']},...['at4','at5','at6'].map(id=>({id:'HNM-C-'+id.toUpperCase(),display_name:'SYNTHETIC '+id,round:31,summary:'SYNTHETIC contribution',route:'round31-'+id,source_paths:[`research/round31/advisor/${id}-gate.json`]}))]},
  calculator:{loop_id:'at5',gate_path:'research/round31/advisor/at5-gate.json',gate_sha256:'a'.repeat(64),formula_id:'zero-selected-reference-comparison-gap-six',preview_only:true,source:'research/round31/forward/at5/calculator.py',result_path:'research/round31/forward/at5/output/results.json',record:{actual_aq_enclosure:true,target_met:true,certified_datum:'1/8',certified_absolute_error:'1/100',interval_width:'1/50',actual_C_interval:{lower:'23/200',upper:'27/200'},parameters:{tau:'1/100000000000000',s:'1',L:'1000000000'},costs:{state:'1/100',centering:'0',real_time_comparison:'0',Poisson_tail:'0',arithmetic:'0'}}},
};
function environment(data=fixture,elementIds=[]) {
  let archiveCalls=0;
  const elements=Object.fromEntries(elementIds.map(id=>[id,{value:id.endsWith('-area')||id.endsWith('-round')?'all':'',innerHTML:'',textContent:'',listeners:{},focused:false,addEventListener(type,fn){this.listeners[type]=fn;},focus(){this.focused=true;},setAttribute(){}}]));
  const prior={marker:'preserved prior',render:route=>`<aside class="r30-current-banner">Current research: Round30.</aside><main>ARCHIVE:${route}</main>`,afterRender(){archiveCalls++;}};
  const context={window:{ROUND31_DATA:structuredClone(data),ResearchObservatory:prior,ResearchJourney:{cleanup(){}}},URL,location:{hash:'#research/home'},document:{title:'',getElementById:id=>elements[id]??null}};
  vm.createContext(context);vm.runInContext(renderer,context);
  return {context,R:context.window.ResearchRound31,prior,elements,archiveCalls:()=>archiveCalls};
}
const {context,R}=environment();
const routes=['home','round31','round31-results','round31-roadmap','round31-sources','round31-calculator','round31-at4','round31-at5','round31-at6','drafts','research-network','hnm-findings'];
assert.equal(R.complete(),true);assert.equal(R.counts().completed,3);
assert.equal(context.window.ResearchObservatory.marker,'preserved prior');
for(const route of routes){const html=R.render(route);assert(html.includes('Research navigation'),route);assert(html.includes('Hruday N M (BUNZEEY)'),route);assert.equal((html.match(/<h1(?:\s|>)/g)||[]).length,1,route);assert(!html.includes('undefined')&&!html.includes('NaN'),route);}
assert(R.render('home').includes('not a percentage'));
assert(R.render('drafts').includes('ym-round31-addendum.pdf')&&R.render('drafts').includes('ym-draft-03.pdf'));
assert.equal(R.normalizeRoute('round31/at4'),'round31-at4');
assert.equal(R.normalizeRoute('round31/results'),'round31-results');
for(const route of ['round30-results','round29-aq2','round23-home']){const html=R.render(route);assert(html.includes('ARCHIVE:'+route));assert(html.includes('Archived research view'));assert(!html.includes('Current research: Round30.'));}
assert.equal(R.filterSources('unread').length,1);assert.equal(R.filterSources('','jung').length,1);assert.equal(R.filterSources('no-such-title').length,0);
assert(R.sourceCards('unread').includes('Unread synthetic fixture'));
assert(R.sourceCards('unread').includes('research/round31/experts/jung/sources.json'));
assert.equal(R.filterNodes('at4').length,1);assert.equal(R.validEdges().length,1);
assert(R.networkDetails('synthetic-at4').includes('Outgoing to'));
assert(R.networkDetails('synthetic-at5').includes('Incoming from'));
assert(R.networkDetails('synthetic-at4').includes('SYNTHETIC relation'));
assert.equal(R.filterFindings('HNM-C-AT4').length,1);assert.equal(R.filterFindings('','31').length,3);
assert(R.findingCards('HNM-C-OLD').includes('papers/draft-03/registry/hnm-registry.json'));
assert(R.calculatorAdmitted());
const preview=R.referencePreview();assert.equal(preview.rigorous,false);assert.equal(preview.arithmetic_error_certified,false);assert(preview.model_error<1e-6&&preview.model_error>8e-7);assert.equal(preview.reference,Math.exp(-3)/4);
assert.equal(R.referencePreview({tau:'-1e-14'}).model_error,preview.model_error);
assert(R.referencePreview({tau:'1e-8'}).model_error>1e-6);
assert(R.referencePreview({L:'10000'}).model_error>1e-6);
assert.equal(R.referencePreview({tau:'0'}).model_error,0);
assert.equal(R.referencePreview({tau:'0'}).reference,Math.exp(-3)/4);
assert.equal(R.referencePreview({alpha:'2',hbar:'3'}).physical_Euclidean_time,1.5);
assert.equal(R.referencePreview().normalized_time,1/8);
assert.equal(R.referencePreview({tau:'1/100000000000000'}).model_error,preview.model_error);
for(const parameters of [{selected:['1','0','0']},{selected:['0','0']},{selected:[false,0,0]},{tau:'1.000001e-8'},{tau:'-1.000001e-8'},{tau:'NaN'},{tau:'Infinity'},{tau:true},{tau:'1e-400'},{s:'0'},{s:'-1'},{L:'0'},{L:'Infinity'},{alpha:'0'},{hbar:'-1'},{E_star:'0'},{lattice_spacing:'0'},{tau:'1/0'},{s:'not a number'}])assert.throws(()=>R.referencePreview(parameters));
const calcHTML=R.render('round31-calculator');assert(calcHTML.includes('Floating-point preview only.'));assert(calcHTML.includes('Recorded datum and certified absolute error'));assert(calcHTML.includes('twice the radius'));assert(calcHTML.includes('does not resolve an interaction-induced shift'));assert(calcHTML.includes('calculator.py'));
const denied=structuredClone(fixture);denied.calculator.gate_sha256='b'.repeat(64);const deniedR=environment(denied).R;assert(!deniedR.calculatorAdmitted());assert(!deniedR.render('round31-calculator').includes('data-r31-recorded-datum'));assert(deniedR.render('round31-calculator').includes('no matching admitted source binding'));
for(const edit of [data=>{data.loops[0].gate_sha256='not-a-hash';},data=>{data.loops.pop();},data=>{data.loops[0].verdict='pending';},data=>{data.loops[0].gate_path='../unbound';},data=>{data.loops[0].sequence=3;},data=>{data.progress.cycle_complete=false;}]){
  const broken=structuredClone(fixture);edit(broken);broken.summary='UNREVIEWED_SECRET';broken.loops[0].accepted='UNREVIEWED_SECRET';broken.loops[0].title='UNREVIEWED_SECRET';
  const B=environment(broken).R;assert.equal(B.complete(),false);
  for(const route of routes){const html=B.render(route);assert(!html.includes('UNREVIEWED_SECRET'),route);assert(html.includes('No Round31 scientific findings are displayed.'),route);}
}
const hostile=structuredClone(fixture);hostile.author='<img src=x onerror=alert(1)>';hostile.summary='<script>evil</script>';hostile.loops[0].title='<script>evil</script>';hostile.loops[0].accepted='</p><script>evil</script>';hostile.survey[0].url='javascript:evil';hostile.survey[0].title='<img src=x onerror=evil>';hostile.addendum.url='../private.pdf';hostile.network.nodes[0].id='" onmouseover="evil';hostile.registry.contributions[0].summary='<script>evil</script>';
const H=environment(hostile).R;
for(const route of routes){const html=H.render(route);assert(!html.includes('<script>')&&!html.includes('<img src=x'),route);assert(!html.includes('href="javascript:')&&!html.includes('src="../private.pdf'),route);}
for(const value of ['javascript:evil','https://user@example.test/','https://a.test\\evil','http://a.test/','data:text/html,hi'])assert.equal(R.safeURL(value),'');
for(const value of ['../private','a/../private','/absolute','a\\b','%2e%2e/file','a//b','a?x=1'])assert.equal(R.safePath(value),'');
assert.equal(R.safePath('research/round31/skeptic/at4.md'),'research/round31/skeptic/at4.md');
const absent={window:{ResearchObservatory:{render:()=> 'PRIOR'}}};vm.createContext(absent);vm.runInContext(renderer,absent);assert.equal(absent.window.ResearchObservatory.render(),'PRIOR');assert.equal(absent.window.ResearchRound31,undefined);

// Exercise actual event handlers, including resets and network relation selection.
const sourceIds=['r31-source-search','r31-source-area','r31-source-cards','r31-source-count','r31-source-reset'];
const S=environment(fixture,sourceIds);S.context.location.hash='#research/round31-sources';S.R.afterRender();S.elements['r31-source-search'].value='unread';S.elements['r31-source-search'].listeners.input();assert(S.elements['r31-source-count'].textContent.startsWith('1 of 2'));S.elements['r31-source-reset'].listeners.click();assert.equal(S.elements['r31-source-search'].value,'');assert(S.elements['r31-source-count'].textContent.startsWith('2 of 2'));
const findingIds=['r31-finding-search','r31-finding-round','r31-finding-cards','r31-finding-count','r31-finding-reset'];
const F=environment(fixture,findingIds);F.context.location.hash='#research/hnm-findings?finding=HNM-C-AT4';F.R.afterRender();assert.equal(F.elements['r31-finding-search'].value,'HNM-C-AT4');assert(F.elements['r31-finding-count'].textContent.startsWith('1 of 4'));F.elements['r31-finding-reset'].listeners.click();assert(F.elements['r31-finding-count'].textContent.startsWith('4 of 4'));
const netIds=['r31-network-search','r31-network-catalog','r31-network-details','r31-network-count','r31-network-reset','r31-network-selected'];
const N=environment(fixture,netIds);N.context.location.hash='#research/research-network?node=synthetic-at4';N.R.afterRender();assert(N.elements['r31-network-details'].innerHTML.includes('Outgoing to'));N.elements['r31-network-details'].listeners.click({target:{closest(){return {getAttribute(){return 'synthetic-at5';}}}}});assert(N.elements['r31-network-details'].innerHTML.includes('Incoming from'));N.elements['r31-network-search'].value='not-a-node';N.elements['r31-network-search'].listeners.input();assert(N.elements['r31-network-count'].textContent.startsWith('0 of 3'));N.elements['r31-network-reset'].listeners.click();assert(N.elements['r31-network-count'].textContent.startsWith('3 of 3'));
const A=environment();A.context.location.hash='#research/round30-results';A.R.afterRender();assert.equal(A.archiveCalls(),1);
const calcIds=['r31-preview-form','r31-preview-output','r31-preview-error','r31-tau','r31-s','r31-L','r31-alpha','r31-hbar','r31-E-star','r31-lattice-spacing'];
const C=environment(fixture,calcIds);C.context.location.hash='#research/round31-calculator';C.R.afterRender();
const preset=name=>C.elements['r31-preview-form'].listeners.click({target:{closest(){return {getAttribute(){return name;}}}}});
preset('certified');assert(C.elements['r31-preview-output'].innerHTML.includes('model-error sum is below'));preset('cap');assert.equal(C.elements['r31-tau'].value,'1e-8');assert(C.elements['r31-preview-output'].innerHTML.includes('model-error sum exceeds'));preset('old-cutoff');assert.equal(C.elements['r31-L'].value,'10000');assert(C.elements['r31-preview-output'].innerHTML.includes('model-error sum exceeds'));preset('zero');assert(C.elements['r31-preview-output'].innerHTML.includes('model-comparison error is zero'));C.elements['r31-s'].value='0';C.elements['r31-preview-form'].listeners.submit({preventDefault(){}});assert(C.elements['r31-preview-error'].textContent.includes('positive'));assert.equal(C.elements['r31-preview-output'].innerHTML,'');

// Admission failures only: synthetic incomplete findings never reach gate loading.
const admission=spawnSync('python3',['-B','-c',`
import importlib.util,json,pathlib,tempfile
spec=importlib.util.spec_from_file_location('r31site','research/round31/presentation/build_site.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as d:
 p=pathlib.Path(d);a=p/'research/round31/advisor';a.mkdir(parents=True)
 (a/'findings.json').write_text(json.dumps({'completed':2,'loops':[{},{}]}))
 try: m.build(p)
 except ValueError as e: assert 'exactly three' in str(e)
 else: raise AssertionError('incomplete findings admitted')
 assert not (p/'dist/research-round31-data.js').exists()
 for bad in ['../escape','/absolute','a/../b','a\\\\b','a%2fb']:
  try: m.local(p,bad)
  except ValueError: pass
  else: raise AssertionError('unsafe path admitted '+bad)
print('incomplete and unsafe source inputs rejected')
`],{cwd:root,encoding:'utf8'});
assert.equal(admission.status,0,admission.stderr||admission.stdout);

let release='not built; only synthetic in-memory renderer and rejection tests executed';
if(fs.existsSync(path('dist/research-round31-data.js'))){
  const raw={window:{}};vm.createContext(raw);vm.runInContext(read('dist/research-round31-data.js'),raw);const data=raw.window.ROUND31_DATA;
  assert.equal(data.author,'Hruday N M (BUNZEEY)');assert.equal(data.loops.length,3);
  for(const [name,expected] of Object.entries(data.input_bindings))assert.equal(hash(name),expected,'changed presentation input '+name);
  for(const loop of data.loops){const gate=JSON.parse(read(loop.gate_path));assert.equal(hash(loop.gate_path),loop.gate_sha256);assert.equal(loop.accepted,gate.accepted);assert.equal(loop.title,gate.title);assert.equal(loop.verdict,gate.verdict);assert(gate.bindings[gate.reviewer_path]);for(const [name,expected] of Object.entries(gate.bindings))assert.equal(hash(name),expected,'changed gate input '+name);}
  const inherited=JSON.parse(read(data.registry_source));assert.equal(JSON.stringify(data.registry.contributions.slice(0,inherited.contributions.length)),JSON.stringify(inherited.contributions));assert.equal(data.registry.contributions.length,inherited.contributions.length+3);
  const actual=environment(data).R;assert(actual.complete());for(const route of routes)assert.equal((actual.render(route).match(/<h1(?:\s|>)/g)||[]).length,1,'real route '+route);
  for(const loop of data.loops)assert(actual.findingCards(loop.contribution_id).includes(loop.contribution_id));
  const before=hash('dist/research-round31-data.js');const replay=spawnSync('python3',['-B','research/round31/presentation/build_site.py','--check'],{cwd:root,encoding:'utf8'});assert.equal(replay.status,0,replay.stderr||replay.stdout);assert.equal(hash('dist/research-round31-data.js'),before,'--check mutated the bundle');
  release='actual gate hashes, catalog preservation and exact nonmutating rebuild passed';
} else if(process.argv.includes('--require-release')) {
  throw new Error('The real Round31 release bundle is required. Synthetic renderer tests are not publication verification.');
}
console.log(JSON.stringify({status:'passed',renderer_fixture:'explicitly synthetic; in memory only',routes:routes.length,checks:'navigation, archive fallback, review suppression, escaping, source paths, provenance display, catalog additions, source/catalog/network interactions, float calculator domain/sign/zero/cap/cutoff/clock controls, certified-versus-preview display, incomplete-build rejection',release}));
