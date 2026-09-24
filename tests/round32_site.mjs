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
const renderer=read('dist/research-round32.js');
const IDS=['av1','av2','aw1','aw2','ax1','ax2','ay1','ay2','az1','az2'];
const fixture={
  schema:'hnm-round32-presentation-v1',author:'Hruday N M (BUNZEEY)',
  summary:'SYNTHETIC RENDERER FIXTURE: not scientific results.',
  scope_statement:'SYNTHETIC scope text.',
  progress:{requested:10,completed:10,cycle_complete:true,subrounds_completed:5},
  subrounds:[1,2,3,4,5].map(id=>({id,title:`SYNTHETIC sub-round ${id} title`,goal_id:`goal-${id}`,
    loops:IDS.slice((id-1)*2,id*2),
    selection_note_path:`research/round32/advisor/selection-subround${id}.md`,
    panel_update_path:`research/round32/advisor/panel-update-${id}-newton-tesla.md`})),
  loops:IDS.map((id,index)=>({id,sequence:index+1,subround:Math.floor(index/2)+1,
    title:`SYNTHETIC ${id} title`,stage:'reviewed',verdict:'accepted_within_scope',
    accepted:`SYNTHETIC ${id} accepted text`,summary:`SYNTHETIC ${id} summary`,model:'SYNTHETIC model',
    limitations:['SYNTHETIC limitation'],contribution_id:`HNM-C-${id.toUpperCase()}`,
    derivation_steps:['SYNTHETIC step'],applications:['SYNTHETIC application'],
    producers:index%2===0?['forward','reverse']:['forward'],
    direction:index%2===0?'paired':'single+skeptic',
    gate_path:`research/round32/advisor/${id}-gate.json`,gate_sha256:'a'.repeat(64),
    reviewer_path:`research/round32/skeptic/${id}.md`,
    sources:[`research/round32/advisor/${id}-gate.json`],
    all_sources:[`research/round32/advisor/${id}-gate.json`,`research/round32/skeptic/${id}.md`]})),
  roadmap:{goals:[{id:'future',title:'SYNTHETIC future target',status:'planned_not_executed',target:'SYNTHETIC target'}]},
  survey:[{id:'synthetic-jung',area:'jung',title:'SYNTHETIC unread source',url:'https://example.test/primary',reading_depth:'Unread synthetic fixture',provenance:'SYNTHETIC record',use:'SYNTHETIC use',limits:'Inaccessible synthetic record',ledger:'research/round32/experts/jung/sources.json',passages:['SYNTHETIC section']},{id:'synthetic-modern',area:'modern',title:'SYNTHETIC modern source',url:'https://example.test/paper',reading_depth:'Selected synthetic passages',ledger:'research/round32/experts/modern/sources.json'}],
  network:{nodes:IDS.map(id=>({id:'synthetic-'+id,title:'SYNTHETIC '+id,kind:'result',status:'accepted',route:'round32-'+id,summary:'SYNTHETIC node summary',sources:[`research/round32/advisor/${id}-gate.json`]})),edges:[{from:'synthetic-av1',to:'synthetic-av2',type:'proven-dependency',label:'SYNTHETIC relation'}]},
  panel:{deliberation:[1,2,3].map(loop=>({loop,path:`research/round32/advisor/deliberation-${loop}.md`,summary:`SYNTHETIC deliberation ${loop} summary`})),
    updates:[1,2,3,4,5].map(subround=>({subround,lens:'newton-tesla',path:`research/round32/advisor/panel-update-${subround}-newton-tesla.md`}))},
  calculators:[{loop_id:'av2',title:'SYNTHETIC calculator',gate_path:'research/round32/advisor/av2-gate.json',gate_sha256:'a'.repeat(64),formula_id:'synthetic-formula',preview_only:true,source:'research/round32/forward/av2/calculator.py',result_path:'research/round32/forward/av2/output/results.json',record:{certified_datum:'1/8',certified_absolute_error:'1/100',costs:{state:'1/100',centering:'0'},parameters:{tau:'1/100000000000000'}}}],
  figures:[{path:'round32-figures/av1-setup.png',title:'SYNTHETIC figure',caption:'SYNTHETIC caption text',source_path:'research/round32/forward/av1/figure.py'}],
  addendum:{path:'papers/round32-addendum/main.pdf',url:'ym-round32-addendum.pdf',title:'SYNTHETIC addendum',available:true},
  round31_addendum:{path:'papers/round31-addendum/main.pdf',url:'ym-round31-addendum.pdf',title:'SYNTHETIC round31 addendum'},
  previous_draft:{path:'papers/draft-03/main.pdf',url:'ym-draft-03.pdf',title:'SYNTHETIC preserved draft'},
  registry:{contributions:[{id:'HNM-C-OLD',display_name:'SYNTHETIC old contribution',round:30,summary:'SYNTHETIC preserved summary',source_paths:['papers/draft-03/registry/hnm-registry.json']},...IDS.map(id=>({id:'HNM-C-'+id.toUpperCase(),display_name:'SYNTHETIC '+id,round:32,summary:'SYNTHETIC contribution',route:'round32-'+id,source_paths:[`research/round32/advisor/${id}-gate.json`]}))]},
};
function environment(data=fixture,elementIds=[]) {
  let archiveCalls=0;
  const elements=Object.fromEntries(elementIds.map(id=>[id,{value:id.endsWith('-area')||id.endsWith('-round')?'all':'',innerHTML:'',textContent:'',listeners:{},focused:false,addEventListener(type,fn){this.listeners[type]=fn;},focus(){this.focused=true;},setAttribute(){}}]));
  const prior={marker:'preserved prior',render:route=>`<aside class="r31-current-banner">Current research: Round31.</aside><main>ARCHIVE:${route}</main>`,afterRender(){archiveCalls++;}};
  const context={window:{ROUND32_DATA:structuredClone(data),ResearchObservatory:prior,ResearchJourney:{cleanup(){}}},URL,location:{hash:'#research/home'},document:{title:'',getElementById:id=>elements[id]??null}};
  vm.createContext(context);vm.runInContext(renderer,context);
  return {context,R:context.window.ResearchRound32,prior,elements,archiveCalls:()=>archiveCalls};
}
const {context,R}=environment();
const routes=['home','round32','round32-results','round32-subrounds','round32-roadmap','round32-sources','round32-panel','round32-calculators','round32-figures',...IDS.map(id=>'round32-'+id),'drafts','research-network','hnm-findings'];
assert.equal(R.complete(),true);assert.equal(R.counts().completed,10);
assert.equal(context.window.ResearchObservatory.marker,'preserved prior');
for(const route of routes){const html=R.render(route);assert(html.includes('Research navigation'),route);assert(html.includes('Hruday N M (BUNZEEY)'),route);assert.equal((html.match(/<h1(?:\s|>)/g)||[]).length,1,route);assert(!html.includes('undefined')&&!html.includes('NaN'),route);}
assert(R.render('home').includes('not a percentage'));
assert(R.render('home').includes('10<span> / 10</span>'));
assert(R.render('drafts').includes('ym-round32-addendum.pdf')&&R.render('drafts').includes('ym-round31-addendum.pdf')&&R.render('drafts').includes('ym-draft-03.pdf'));
assert(R.render('round32-subrounds').includes('Selection note')||R.render('round32-subrounds').includes('selection-subround1.md'));
assert(R.render('round32-panel').includes('deliberation-1.md')||R.render('round32-panel').includes('Deliberation loop'));
assert(R.render('round32-calculators').includes('Recorded exact values; not a live computation.'));
assert(R.render('round32-figures').includes('<img'));
assert.equal(R.normalizeRoute('round32/av1'),'round32-av1');
assert.equal(R.normalizeRoute('round32/results'),'round32-results');
assert.equal(R.normalizeRoute('round32/subrounds'),'round32-subrounds');
for(const route of ['round31-results','round30-results','round29-aq2']){const html=R.render(route);assert(html.includes('ARCHIVE:'+route),route);assert(html.includes('Archived research view'),route);assert(!html.includes('Current research: Round31.'),route);}
assert.equal(R.filterSources('unread').length,1);assert.equal(R.filterSources('','jung').length,1);assert.equal(R.filterSources('no-such-title').length,0);
assert(R.sourceCards('unread').includes('Unread synthetic fixture'));
assert(R.sourceCards('unread').includes('research/round32/experts/jung/sources.json'));
assert.equal(R.filterNodes('av1').length,1);assert.equal(R.validEdges().length,1);
assert(R.networkDetails('synthetic-av1').includes('Outgoing to'));
assert(R.networkDetails('synthetic-av2').includes('Incoming from'));
assert(R.networkDetails('synthetic-av1').includes('SYNTHETIC relation'));
assert.equal(R.filterFindings('HNM-C-AV1').length,1);assert.equal(R.filterFindings('','32').length,10);
assert(R.findingCards('HNM-C-OLD').includes('papers/draft-03/registry/hnm-registry.json'));
const subroundHTML=R.subroundCards();assert(subroundHTML.includes('SYNTHETIC sub-round 1 title'));assert(subroundHTML.includes('2 of 2 investigations reviewed.'));
const figureHTML=R.figureCards();assert(figureHTML.includes('round32-figures/av1-setup.png'));assert(figureHTML.includes('SYNTHETIC caption text'));
const calcHTML=R.calculatorCards();assert(calcHTML.includes('Recorded exact values; not a live computation.'));assert(calcHTML.includes('1/8'));assert(calcHTML.includes('costs.state'));

for(const edit of [
  data=>{data.loops[0].gate_sha256='not-a-hash';},
  data=>{data.loops.pop();},
  data=>{data.loops[0].verdict='pending';},
  data=>{data.loops[0].gate_path='../unbound';},
  data=>{data.loops[0].sequence=3;},
  data=>{data.progress.cycle_complete=false;},
  data=>{data.progress.completed=9;},
]){
  const broken=structuredClone(fixture);edit(broken);broken.summary='UNREVIEWED_SECRET';broken.loops[0].accepted='UNREVIEWED_SECRET';broken.loops[0].title='UNREVIEWED_SECRET';
  const B=environment(broken).R;assert.equal(B.complete(),false);
  for(const route of routes){const html=B.render(route);assert(!html.includes('UNREVIEWED_SECRET'),route);assert(html.includes('No Round32 scientific findings are displayed.'),route);}
}

const hostile=structuredClone(fixture);
hostile.author='<img src=x onerror=alert(1)>';hostile.summary='<script>evil</script>';
hostile.loops[0].title='<script>evil</script>';hostile.loops[0].accepted='</p><script>evil</script>';
hostile.survey[0].url='javascript:evil';hostile.survey[0].title='<img src=x onerror=evil>';
hostile.addendum.url='../private.pdf';hostile.network.nodes[0].id='" onmouseover="evil';
hostile.registry.contributions[0].summary='<script>evil</script>';
hostile.figures[0].path='../escape.png';hostile.figures[0].title='<script>evil</script>';hostile.figures[0].caption='<img src=x onerror=evil>';
hostile.calculators[0].record.certified_datum='<script>evil</script>';
hostile.panel.deliberation[0].summary='<script>evil</script>';
const H=environment(hostile).R;
for(const route of routes){const html=H.render(route);assert(!html.includes('<script>')&&!html.includes('<img src=x'),route);assert(!html.includes('href="javascript:')&&!html.includes('src="../private.pdf')&&!html.includes('src="../escape.png'),route);}
for(const value of ['javascript:evil','https://user@example.test/','https://a.test\\evil','http://a.test/','data:text/html,hi'])assert.equal(R.safeURL(value),'');
for(const value of ['../private','a/../private','/absolute','a\\b','%2e%2e/file','a//b','a?x=1'])assert.equal(R.safePath(value),'');
assert.equal(R.safePath('research/round32/skeptic/av1.md'),'research/round32/skeptic/av1.md');
const absent={window:{ResearchObservatory:{render:()=> 'PRIOR'}}};vm.createContext(absent);vm.runInContext(renderer,absent);assert.equal(absent.window.ResearchObservatory.render(),'PRIOR');assert.equal(absent.window.ResearchRound32,undefined);

// Exercise actual event handlers, including resets and network relation selection.
const sourceIds=['r32-source-search','r32-source-area','r32-source-cards','r32-source-count','r32-source-reset'];
const S=environment(fixture,sourceIds);S.context.location.hash='#research/round32-sources';S.R.afterRender();S.elements['r32-source-search'].value='unread';S.elements['r32-source-search'].listeners.input();assert(S.elements['r32-source-count'].textContent.startsWith('1 of 2'));S.elements['r32-source-reset'].listeners.click();assert.equal(S.elements['r32-source-search'].value,'');assert(S.elements['r32-source-count'].textContent.startsWith('2 of 2'));
const findingIds=['r32-finding-search','r32-finding-round','r32-finding-cards','r32-finding-count','r32-finding-reset'];
const F=environment(fixture,findingIds);F.context.location.hash='#research/hnm-findings?finding=HNM-C-AV1';F.R.afterRender();assert.equal(F.elements['r32-finding-search'].value,'HNM-C-AV1');assert(F.elements['r32-finding-count'].textContent.startsWith('1 of 11'));F.elements['r32-finding-reset'].listeners.click();assert(F.elements['r32-finding-count'].textContent.startsWith('11 of 11'));
const netIds=['r32-network-search','r32-network-catalog','r32-network-details','r32-network-count','r32-network-reset','r32-network-selected'];
const N=environment(fixture,netIds);N.context.location.hash='#research/research-network?node=synthetic-av1';N.R.afterRender();assert(N.elements['r32-network-details'].innerHTML.includes('Outgoing to'));N.elements['r32-network-details'].listeners.click({target:{closest(){return {getAttribute(){return 'synthetic-av2';}}}}});assert(N.elements['r32-network-details'].innerHTML.includes('Incoming from'));N.elements['r32-network-search'].value='not-a-node';N.elements['r32-network-search'].listeners.input();assert(N.elements['r32-network-count'].textContent.startsWith('0 of 10'));N.elements['r32-network-reset'].listeners.click();assert(N.elements['r32-network-count'].textContent.startsWith('10 of 10'));
const A=environment();A.context.location.hash='#research/round31-results';A.R.afterRender();assert.equal(A.archiveCalls(),1);

// Admission failures only: synthetic incomplete findings never reach gate loading.
const admission=spawnSync('python3',['-B','-c',`
import importlib.util,json,pathlib,tempfile
spec=importlib.util.spec_from_file_location('r32site','research/round32/presentation/build_site.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as d:
 p=pathlib.Path(d);a=p/'research/round32/advisor';a.mkdir(parents=True)
 (a/'findings.json').write_text(json.dumps({'human_author':'Hruday N M (BUNZEEY)','requested':10,'completed':5,'loops':[{},{},{},{},{}]}))
 try: m.build(p)
 except ValueError as e: assert 'exactly ten' in str(e) or 'allow-incomplete' in str(e), str(e)
 else: raise AssertionError('incomplete findings admitted without --allow-incomplete')
 assert not (p/'dist/research-round32-data.js').exists()
 try: m.build(p, allow_incomplete=True)
 except ValueError as e: assert 'mismatch' in str(e) or 'missing' in str(e) or 'invalid' in str(e), str(e)
 else: raise AssertionError('malformed loop rows admitted even with --allow-incomplete')
 for bad in ['../escape','/absolute','a/../b','a\\\\b','a%2fb']:
  try: m.local(p, bad)
  except ValueError: pass
  else: raise AssertionError('unsafe path admitted '+bad)
print('incomplete and unsafe source inputs rejected')
`],{cwd:root,encoding:'utf8'});
assert.equal(admission.status,0,admission.stderr||admission.stdout);

let release='not built; only synthetic in-memory renderer and rejection tests executed';
const bundleExists=fs.existsSync(path('dist/research-round32-data.js'));
const bundleData=bundleExists?(()=>{const raw={window:{}};vm.createContext(raw);vm.runInContext(read('dist/research-round32-data.js'),raw);return raw.window.ROUND32_DATA;})():null;
if(bundleExists&&bundleData?.progress?.cycle_complete!==true&&!process.argv.includes('--require-release')){
  // An in-progress placeholder bundle must display no scientific findings at all.
  const placeholder=environment(bundleData).R;assert.equal(placeholder.complete(),false);
  for(const route of routes)assert(placeholder.render(route).includes('No Round32 scientific findings are displayed.'),'placeholder route '+route);
  release='in-progress placeholder bundle: no scientific findings displayed';
} else if(bundleExists){
  const data=bundleData;
  assert.equal(data.schema,'hnm-round32-presentation-v1');assert.equal(data.author,'Hruday N M (BUNZEEY)');
  assert.equal(data.loops.length,10);assert.equal(data.progress.completed,10);assert.equal(data.progress.cycle_complete,true);
  for(const [name,expected] of Object.entries(data.input_bindings))assert.equal(hash(name),expected,'changed presentation input '+name);
  for(const loop of data.loops){const gate=JSON.parse(read(loop.gate_path));assert.equal(hash(loop.gate_path),loop.gate_sha256);assert.equal(loop.accepted,gate.accepted);assert.equal(loop.title,gate.title);assert.equal(loop.verdict,gate.verdict);assert(gate.bindings[gate.reviewer_path]);for(const [name,expected] of Object.entries(gate.bindings))assert.equal(hash(name),expected,'changed gate input '+name);}
  const inherited=JSON.parse(read(data.registry_source));assert.equal(JSON.stringify(data.registry.contributions.slice(0,inherited.contributions.length)),JSON.stringify(inherited.contributions));assert.equal(data.registry.contributions.length,inherited.contributions.length+10);
  const actual=environment(data).R;assert(actual.complete());for(const route of routes)assert.equal((actual.render(route).match(/<h1(?:\s|>)/g)||[]).length,1,'real route '+route);
  for(const loop of data.loops)assert(actual.findingCards(loop.contribution_id).includes(loop.contribution_id));
  const before=hash('dist/research-round32-data.js');const replay=spawnSync('python3',['-B','research/round32/presentation/build_site.py','--check'],{cwd:root,encoding:'utf8'});assert.equal(replay.status,0,replay.stderr||replay.stdout);assert.equal(hash('dist/research-round32-data.js'),before,'--check mutated the bundle');
  release='actual gate hashes, catalog preservation and exact nonmutating rebuild passed';
} else if(process.argv.includes('--require-release')) {
  throw new Error('The real Round32 release bundle is required. Synthetic renderer tests are not publication verification.');
}
console.log(JSON.stringify({status:'passed',renderer_fixture:'explicitly synthetic; in memory only',routes:routes.length,checks:'navigation, archive fallback, review suppression, escaping, source/figure/calculator paths, provenance display, catalog additions, sub-round grouping, panel deliberation/updates, source/catalog/network interactions, incomplete-build rejection',release}));
