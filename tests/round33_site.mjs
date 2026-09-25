/* Renderer fixtures are explicitly synthetic and remain in memory.
 * Real bundle and gate checks run when the complete release bundle exists, or are
 * required by --require-release. An in-progress placeholder bundle (0 of 8 reviewed
 * investigations) is accepted without --require-release and must display no
 * scientific findings. No fake completed research bundle is written or built.
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
const renderer=read('dist/research-round33.js');
const IDS=['ba1','ba2','bb1','bb2','bc1','bc2','bd1','bd2'];
const DIRECTIONS=['paired','single+skeptic','statement+skeptic','statement-only'];
const fixture={
  schema:'hnm-round33-presentation-v1',author:'Hruday N M (BUNZEEY)',
  summary:'SYNTHETIC RENDERER FIXTURE: not scientific results.',
  scope_statement:'SYNTHETIC scope text.',
  progress:{requested:8,completed:8,cycle_complete:true,subrounds_completed:4},
  subrounds:[1,2,3,4].map(id=>({id,title:`SYNTHETIC sub-round ${id} title`,goal_id:`goal-${id}`,
    loops:IDS.slice((id-1)*2,id*2),
    selection_note_path:`research/round33/advisor/selection-subround${id}.md`,
    panel_update_path:`research/round33/advisor/panel-update-${id}.md`})),
  loops:IDS.map((id,index)=>({id,sequence:index+1,subround:Math.floor(index/2)+1,
    title:`SYNTHETIC ${id} title`,stage:'reviewed',verdict:index===7?'limited':'accepted_within_scope',
    accepted:`SYNTHETIC ${id} accepted text`,summary:`SYNTHETIC ${id} summary`,model:'SYNTHETIC model',
    limitations:['SYNTHETIC limitation'],contribution_id:`HNM-C-${id.toUpperCase()}`,
    derivation_steps:['SYNTHETIC step'],applications:['SYNTHETIC application'],
    producers:index%4===0?['forward','reverse']:['forward'],
    direction:DIRECTIONS[index%4],
    gate_path:`research/round33/advisor/${id}-gate.json`,gate_sha256:'a'.repeat(64),
    reviewer_path:`research/round33/skeptic/${id}.md`,
    sources:[`research/round33/advisor/${id}-gate.json`],
    all_sources:[`research/round33/advisor/${id}-gate.json`,`research/round33/skeptic/${id}.md`]})),
  applications:[
    {loop_id:'bd1',problem:'SYNTHETIC related problem one',equation:'SYNTHETIC omega(W) = tau/144 + O(tau^2)',outcome:'SYNTHETIC transfers with its own exact checks',model:'SYNTHETIC target model',kind:'transfer',detail:'SYNTHETIC detail',sources:['research/round33/skeptic/bd1.md'],gate_path:'research/round33/advisor/bd1-gate.json',gate_sha256:'a'.repeat(64),route:'round33-bd1'},
    {loop_id:'bd2',problem:'SYNTHETIC related problem two',equation:'SYNTHETIC flip lemma',outcome:'SYNTHETIC obstruction: -1 is not central',model:'SYNTHETIC SU(3) model',kind:'obstruction',detail:'',sources:[],gate_path:'research/round33/advisor/bd2-gate.json',gate_sha256:'a'.repeat(64),route:'round33-bd2'},
  ],
  roadmap:{goals:[{id:'future',title:'SYNTHETIC future target',status:'planned_not_executed',target:'SYNTHETIC target'}]},
  survey:[{id:'synthetic-jung',area:'jung',title:'SYNTHETIC unread source',url:'https://example.test/primary',reading_depth:'Unread synthetic fixture',provenance:'SYNTHETIC record',use:'SYNTHETIC use',limits:'Inaccessible synthetic record',ledger:'research/round33/experts/jung/sources.json',passages:['SYNTHETIC section']},{id:'synthetic-modern',area:'modern',title:'SYNTHETIC modern source',url:'https://example.test/paper',reading_depth:'Selected synthetic passages',ledger:'research/round33/experts/modern/sources.json'}],
  network:{nodes:IDS.map(id=>({id:'synthetic-'+id,title:'SYNTHETIC '+id,kind:'result',status:'accepted',route:'round33-'+id,summary:'SYNTHETIC node summary',sources:[`research/round33/advisor/${id}-gate.json`]})),edges:[{from:'synthetic-ba1',to:'synthetic-ba2',type:'proven-dependency',label:'SYNTHETIC relation'}]},
  panel:{deliberation:[1,2].map(loop=>({loop,path:`research/round33/advisor/deliberation-${loop}.md`,summary:`SYNTHETIC deliberation ${loop} summary`})),
    updates:[1,2,3,4].map(subround=>({subround,lens:'historical, jung',lenses:[`research/round33/experts/historical/update-${subround}.md`],assistants:[`research/round33/experts/historical/assistant-${subround}.md`],path:`research/round33/advisor/panel-update-${subround}.md`,goal_changes:'SYNTHETIC goal change'}))},
  calculators:[{loop_id:'ba2',title:'SYNTHETIC calculator',gate_path:'research/round33/advisor/ba2-gate.json',gate_sha256:'a'.repeat(64),formula_id:'synthetic-formula',preview_only:true,source:'research/round33/forward/ba2/calculator.py',result_path:'research/round33/forward/ba2/output/results.json',record:{certified_datum:'1/8',certified_absolute_error:'1/100',costs:{state:'1/100',centering:'0'},parameters:{tau:'1/100000000000000'}}}],
  figures:[{path:'r33-setup.png',title:'SYNTHETIC figure',caption:'SYNTHETIC caption text',source_path:'research/round33/figures/make_figures.py'}],
  addendum:{path:'papers/round33-addendum/main.pdf',url:'ym-round33-addendum.pdf',title:'SYNTHETIC addendum',available:true},
  round32_addendum:{path:'papers/round32-addendum/main.pdf',url:'ym-round32-addendum.pdf',title:'SYNTHETIC round32 addendum'},
  round31_addendum:{path:'papers/round31-addendum/main.pdf',url:'ym-round31-addendum.pdf',title:'SYNTHETIC round31 addendum'},
  previous_draft:{path:'papers/draft-03/main.pdf',url:'ym-draft-03.pdf',title:'SYNTHETIC preserved draft'},
  registry:{contributions:[{id:'HNM-C-OLD',display_name:'SYNTHETIC old contribution',round:30,summary:'SYNTHETIC preserved summary',source_paths:['papers/draft-03/registry/hnm-registry.json']},{id:'HNM-C-AZ2',display_name:'SYNTHETIC round32 alias',round:32,summary:'SYNTHETIC inherited alias',route:'round32-az2',source_paths:['research/round32/advisor/az2-gate.json']},...IDS.map(id=>({id:'HNM-C-'+id.toUpperCase(),display_name:'SYNTHETIC '+id,round:33,summary:'SYNTHETIC contribution',route:'round33-'+id,source_paths:[`research/round33/advisor/${id}-gate.json`]}))]},
};
function environment(data=fixture,elementIds=[]) {
  let archiveCalls=0;
  const elements=Object.fromEntries(elementIds.map(id=>[id,{value:id.endsWith('-area')||id.endsWith('-round')?'all':'',innerHTML:'',textContent:'',listeners:{},focused:false,addEventListener(type,fn){this.listeners[type]=fn;},focus(){this.focused=true;},setAttribute(){}}]));
  const prior={marker:'preserved prior',render:route=>`<aside class="r32-current-banner">Current research: Round32.</aside><main>ARCHIVE:${route}</main>`,afterRender(){archiveCalls++;}};
  const context={window:{ROUND33_DATA:structuredClone(data),ResearchObservatory:prior,ResearchJourney:{cleanup(){}}},URL,location:{hash:'#research/home'},document:{title:'',getElementById:id=>elements[id]??null}};
  vm.createContext(context);vm.runInContext(renderer,context);
  return {context,R:context.window.ResearchRound33,prior,elements,archiveCalls:()=>archiveCalls};
}
const {context,R}=environment();
const routes=['home','round33','round33-results','round33-subrounds','round33-roadmap','round33-sources','round33-panel','round33-calculators','round33-figures','round33-applications',...IDS.map(id=>'round33-'+id),'drafts','research-network','hnm-findings'];
assert.equal(R.complete(),true);assert.equal(R.counts().completed,8);assert.equal(R.counts().requested,8);
assert.equal(context.window.ResearchObservatory.marker,'preserved prior');
for(const route of routes){const html=R.render(route);assert(html.includes('Research navigation'),route);assert(html.includes('Hruday N M (BUNZEEY)'),route);assert.equal((html.match(/<h1(?:\s|>)/g)||[]).length,1,route);assert(!html.includes('undefined')&&!html.includes('NaN'),route);assert(html.includes('href="#research/round32-results">Round32 archive</a>'),'Round32 archive link '+route);}
assert(R.render('home').includes('not a percentage'));
assert(R.render('home').includes('8<span> / 8</span>'));
assert(R.render('drafts').includes('ym-round33-addendum.pdf')&&R.render('drafts').includes('ym-round32-addendum.pdf')&&R.render('drafts').includes('ym-round31-addendum.pdf')&&R.render('drafts').includes('ym-draft-03.pdf'));
assert(R.render('round33-subrounds').includes('Applications stage'));
assert(R.render('round33-subrounds').includes('selection-subround1.md'));
assert(R.render('round33-panel').includes('deliberation-2.md')&&R.render('round33-panel').includes('Assistant package'));
assert(R.render('round33-calculators').includes('Recorded exact values; not a live computation.'));
assert(R.render('round33-figures').includes('<img'));
const appHTML=R.render('round33-applications');
assert(appHTML.includes('SYNTHETIC related problem one')&&appHTML.includes('SYNTHETIC related problem two'));
assert(appHTML.includes('Recorded obstruction')&&appHTML.includes('>Transfer<'));
assert(appHTML.includes('SYNTHETIC omega(W) = tau/144 + O(tau^2)'));
assert(appHTML.includes('href="#research/round33-bd1"')&&appHTML.includes('research/round33/skeptic/bd1.md'));
assert(R.render('round33-bd1').includes('Recorded transfers and obstructions'));
assert(!R.render('round33-ba2').includes('Recorded transfers and obstructions'));
for(const [index,id] of IDS.entries())assert(R.render('round33-'+id).includes('<strong>Direction:</strong> '+DIRECTIONS[index%4]),id);
assert.equal(R.normalizeRoute('round33/ba1'),'round33-ba1');
assert.equal(R.normalizeRoute('round33/results'),'round33-results');
assert.equal(R.normalizeRoute('round33/subrounds'),'round33-subrounds');
assert.equal(R.normalizeRoute('round33/applications'),'round33-applications');
for(const route of ['round32-results','round32-az2','round31-results','round30-results','round29-aq2']){const html=R.render(route);assert(html.includes('ARCHIVE:'+route),route);assert(html.includes('Archived research view'),route);assert(!html.includes('Current research: Round32.'),route);assert(html.includes('Current Round33 results'),route);}
assert.equal(R.filterSources('unread').length,1);assert.equal(R.filterSources('','jung').length,1);assert.equal(R.filterSources('no-such-title').length,0);
assert(R.sourceCards('unread').includes('Unread synthetic fixture'));
assert(R.sourceCards('unread').includes('research/round33/experts/jung/sources.json'));
assert.equal(R.filterNodes('ba1').length,1);assert.equal(R.validEdges().length,1);
assert(R.networkDetails('synthetic-ba1').includes('Outgoing to'));
assert(R.networkDetails('synthetic-ba2').includes('Incoming from'));
assert(R.networkDetails('synthetic-ba1').includes('SYNTHETIC relation'));
assert.equal(R.filterFindings('HNM-C-BA1').length,1);assert.equal(R.filterFindings('','33').length,8);assert.equal(R.filterFindings('','32').length,1);
assert(R.findingCards('HNM-C-OLD').includes('papers/draft-03/registry/hnm-registry.json'));
assert(R.findingCards('HNM-C-AZ2').includes('href="#research/round32-az2"'));
const subroundHTML=R.subroundCards();assert(subroundHTML.includes('SYNTHETIC sub-round 1 title'));assert(subroundHTML.includes('2 of 2 investigations reviewed.'));
const figureHTML=R.figureCards();assert(figureHTML.includes('r33-setup.png'));assert(figureHTML.includes('SYNTHETIC caption text'));
const calcHTML=R.calculatorCards();assert(calcHTML.includes('Recorded exact values; not a live computation.'));assert(calcHTML.includes('1/8'));assert(calcHTML.includes('costs.state'));
const emptyApps=structuredClone(fixture);emptyApps.applications=[];assert(environment(emptyApps).R.applicationCards().includes('No applications are recorded.'));
const noApps=structuredClone(fixture);delete noApps.applications;assert(environment(noApps).R.render('round33-applications').includes('No applications are recorded.'));

for(const edit of [
  data=>{data.loops[0].gate_sha256='not-a-hash';},
  data=>{data.loops.pop();},
  data=>{data.loops[0].verdict='pending';},
  data=>{data.loops[0].gate_path='../unbound';},
  data=>{data.loops[0].sequence=3;},
  data=>{data.loops[0].id='av1';},
  data=>{data.progress.cycle_complete=false;},
  data=>{data.progress.completed=7;},
  data=>{data.progress.requested=10;},
  data=>{data.placeholder=true;},
  data=>{data.schema='hnm-round32-presentation-v1';},
]){
  const broken=structuredClone(fixture);edit(broken);broken.summary='UNREVIEWED_SECRET';broken.loops[0].accepted='UNREVIEWED_SECRET';broken.loops[0].title='UNREVIEWED_SECRET';broken.applications[0].problem='UNREVIEWED_SECRET';
  const B=environment(broken).R;assert.equal(B.complete(),false);
  for(const route of routes){const html=B.render(route);assert(!html.includes('UNREVIEWED_SECRET'),route);assert(html.includes('No Round33 scientific findings are displayed.'),route);}
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
hostile.applications[0].equation='</code></pre><script>evil</script>';hostile.applications[0].problem='<img src=x onerror=evil>';hostile.applications[0].loop_id='" onclick="evil';hostile.applications[1].sources=['javascript:evil','../escape'];
const H=environment(hostile).R;
for(const route of routes){const html=H.render(route);assert(!html.includes('<script>')&&!html.includes('<img src=x'),route);assert(!html.includes('href="javascript:')&&!html.includes('src="../private.pdf')&&!html.includes('src="../escape.png')&&!html.includes('onclick="evil'),route);}
for(const value of ['javascript:evil','https://user@example.test/','https://a.test\\evil','http://a.test/','data:text/html,hi'])assert.equal(R.safeURL(value),'');
for(const value of ['../private','a/../private','/absolute','a\\b','%2e%2e/file','a//b','a?x=1'])assert.equal(R.safePath(value),'');
assert.equal(R.safePath('research/round33/skeptic/ba1.md'),'research/round33/skeptic/ba1.md');
const absent={window:{ResearchObservatory:{render:()=> 'PRIOR'}}};vm.createContext(absent);vm.runInContext(renderer,absent);assert.equal(absent.window.ResearchObservatory.render(),'PRIOR');assert.equal(absent.window.ResearchRound33,undefined);

// Exercise actual event handlers, including resets and network relation selection.
const sourceIds=['r33-source-search','r33-source-area','r33-source-cards','r33-source-count','r33-source-reset'];
const S=environment(fixture,sourceIds);S.context.location.hash='#research/round33-sources';S.R.afterRender();S.elements['r33-source-search'].value='unread';S.elements['r33-source-search'].listeners.input();assert(S.elements['r33-source-count'].textContent.startsWith('1 of 2'));S.elements['r33-source-reset'].listeners.click();assert.equal(S.elements['r33-source-search'].value,'');assert(S.elements['r33-source-count'].textContent.startsWith('2 of 2'));
const findingIds=['r33-finding-search','r33-finding-round','r33-finding-cards','r33-finding-count','r33-finding-reset'];
const F=environment(fixture,findingIds);F.context.location.hash='#research/hnm-findings?finding=HNM-C-BA1';F.R.afterRender();assert.equal(F.elements['r33-finding-search'].value,'HNM-C-BA1');assert(F.elements['r33-finding-count'].textContent.startsWith('1 of 10'));F.elements['r33-finding-reset'].listeners.click();assert(F.elements['r33-finding-count'].textContent.startsWith('10 of 10'));
const netIds=['r33-network-search','r33-network-catalog','r33-network-details','r33-network-count','r33-network-reset','r33-network-selected'];
const N=environment(fixture,netIds);N.context.location.hash='#research/research-network?node=synthetic-ba1';N.R.afterRender();assert(N.elements['r33-network-details'].innerHTML.includes('Outgoing to'));N.elements['r33-network-details'].listeners.click({target:{closest(){return {getAttribute(){return 'synthetic-ba2';}}}}});assert(N.elements['r33-network-details'].innerHTML.includes('Incoming from'));N.elements['r33-network-search'].value='not-a-node';N.elements['r33-network-search'].listeners.input();assert(N.elements['r33-network-count'].textContent.startsWith('0 of 8'));N.elements['r33-network-reset'].listeners.click();assert(N.elements['r33-network-count'].textContent.startsWith('8 of 8'));
const A=environment();A.context.location.hash='#research/round32-results';A.R.afterRender();assert.equal(A.archiveCalls(),1);
const T=environment();T.context.location.hash='#research/round33-applications';T.R.afterRender();assert.equal(T.context.document.title,'Round33 applications · Yang–Mills Workbench');

// Admission failures and the placeholder build. Synthetic incomplete findings never reach gate loading.
const admission=spawnSync('python3',['-B','-c',`
import importlib.util,json,pathlib,tempfile
spec=importlib.util.spec_from_file_location('r33site','research/round33/presentation/build_site.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
base={'human_author':'Hruday N M (BUNZEEY)','requested':8}
with tempfile.TemporaryDirectory() as d:
 p=pathlib.Path(d);a=p/'research/round33/advisor';a.mkdir(parents=True)
 (a/'findings.json').write_text(json.dumps({**base,'completed':4,'loops':[{},{},{},{}]}))
 try: m.build(p)
 except ValueError as e: assert 'exactly eight' in str(e) or 'allow-incomplete' in str(e), str(e)
 else: raise AssertionError('incomplete findings admitted without --allow-incomplete')
 assert not (p/'dist/research-round33-data.js').exists()
 try: m.build(p, allow_incomplete=True)
 except ValueError as e: assert 'mismatch' in str(e) or 'missing' in str(e) or 'invalid' in str(e), str(e)
 else: raise AssertionError('malformed loop rows admitted even with --allow-incomplete')
 (a/'findings.json').write_text(json.dumps({**base,'requested':10,'completed':0,'loops':[]}))
 try: m.build(p, allow_incomplete=True, allow_missing_addendum=True)
 except ValueError as e: assert 'eight' in str(e), str(e)
 else: raise AssertionError('wrong requested count admitted')
 (a/'findings.json').write_text(json.dumps({**base,'completed':0,'loops':[],'summary':'S','scope_statement':'T'}))
 try: m.build(p)
 except ValueError as e: assert 'allow-incomplete' in str(e), str(e)
 else: raise AssertionError('placeholder admitted without --allow-incomplete')
 try: m.build(p, allow_incomplete=True)
 except ValueError as e: assert 'allow-missing-addendum' in str(e), str(e)
 else: raise AssertionError('missing addendum admitted without --allow-missing-addendum')
 data=m.build(p, allow_incomplete=True, allow_missing_addendum=True)
 assert data['placeholder'] is True and data['progress']['completed']==0 and data['loops']==[] and data['progress']['cycle_complete'] is False
 assert list(data['input_bindings'])==['research/round33/advisor/findings.json']
 assert 'window.ROUND33_DATA = ' in m.bundle(data) and 'Placeholder' in m.bundle(data)
 for bad in ['../escape','/absolute','a/../b','a\\\\b','a%2fb']:
  try: m.local(p, bad)
  except ValueError: pass
  else: raise AssertionError('unsafe path admitted '+bad)
print('incomplete, placeholder and unsafe source inputs handled')
`],{cwd:root,encoding:'utf8'});
assert.equal(admission.status,0,admission.stderr||admission.stdout);

let release='not built; only synthetic in-memory renderer and rejection tests executed';
const bundleExists=fs.existsSync(path('dist/research-round33-data.js'));
const bundleData=bundleExists?(()=>{const raw={window:{}};vm.createContext(raw);vm.runInContext(read('dist/research-round33-data.js'),raw);return raw.window.ROUND33_DATA;})():null;
if(bundleExists&&bundleData?.progress?.cycle_complete!==true&&!process.argv.includes('--require-release')){
  // An in-progress placeholder bundle must display no scientific findings at all.
  assert.equal(bundleData.schema,'hnm-round33-presentation-v1');assert.equal(bundleData.author,'Hruday N M (BUNZEEY)');
  assert.equal(bundleData.progress.requested,8);assert(bundleData.progress.completed<8);
  const placeholder=environment(bundleData).R;assert.equal(placeholder.complete(),false);
  for(const route of routes)assert(placeholder.render(route).includes('No Round33 scientific findings are displayed.'),'placeholder route '+route);
  release=`in-progress bundle (${bundleData.progress.completed} of 8 reviewed): no scientific findings displayed`;
} else if(bundleExists){
  const data=bundleData;
  assert.equal(data.schema,'hnm-round33-presentation-v1');assert.equal(data.author,'Hruday N M (BUNZEEY)');
  assert.equal(data.loops.length,8,'the Round33 release requires eight reviewed investigations');assert.equal(data.progress.completed,8);assert.equal(data.progress.cycle_complete,true);assert.notEqual(data.placeholder,true);
  for(const [name,expected] of Object.entries(data.input_bindings))assert.equal(hash(name),expected,'changed presentation input '+name);
  for(const loop of data.loops){const gate=JSON.parse(read(loop.gate_path));assert.equal(hash(loop.gate_path),loop.gate_sha256);assert.equal(loop.accepted,gate.accepted);assert.equal(loop.title,gate.title);assert.equal(loop.verdict,gate.verdict);assert(gate.bindings[gate.reviewer_path]);for(const [name,expected] of Object.entries(gate.bindings))assert.equal(hash(name),expected,'changed gate input '+name);const contract=JSON.parse(read(`research/round33/contracts/${loop.id}.json`));assert.equal(loop.direction,contract.direction,'direction '+loop.id);}
  const inherited=JSON.parse(read(data.registry_source));assert.equal(JSON.stringify(data.registry.contributions.slice(0,inherited.contributions.length)),JSON.stringify(inherited.contributions));
  const earlier=data.inherited_alias_sources.reduce((sum,name)=>sum+JSON.parse(read(name)).loops.length,0);
  assert.equal(data.registry.contributions.length,inherited.contributions.length+earlier+8);assert.equal(data.registry.contributions.filter(row=>row.round===33).length,8);
  for(const row of data.applications??[])assert(data.loops.some(loop=>loop.id===row.loop_id),'application loop '+row.loop_id);
  const actual=environment(data).R;assert(actual.complete());for(const route of routes)assert.equal((actual.render(route).match(/<h1(?:\s|>)/g)||[]).length,1,'real route '+route);
  for(const loop of data.loops)assert(actual.findingCards(loop.contribution_id).includes(loop.contribution_id));
  // Before the addendum PDF exists the complete bundle records it as unavailable;
  // --require-release demands the published PDF, so the replay flag is never needed there.
  const preAddendum=data.addendum?.available===false;
  if(process.argv.includes('--require-release'))assert.equal(data.addendum?.available,true,'the Round33 release requires the published addendum PDF');
  const replayArgs=['-B','research/round33/presentation/build_site.py','--check',...(preAddendum?['--allow-missing-addendum']:[])];
  const before=hash('dist/research-round33-data.js');const replay=spawnSync('python3',replayArgs,{cwd:root,encoding:'utf8'});assert.equal(replay.status,0,replay.stderr||replay.stdout);assert.equal(hash('dist/research-round33-data.js'),before,'--check mutated the bundle');
  release=`actual gate hashes, contract directions, catalog preservation and exact nonmutating rebuild passed${preAddendum?' (addendum PDF not yet published; replayed with --allow-missing-addendum)':''}`;
} else if(process.argv.includes('--require-release')) {
  throw new Error('The real Round33 release bundle is required. Synthetic renderer tests are not publication verification.');
}
console.log(JSON.stringify({status:'passed',renderer_fixture:'explicitly synthetic; in memory only',routes:routes.length,checks:'navigation incl. Round32 archive link, archive fallback, review suppression, escaping, source/figure/calculator paths, applications (transfers and obstructions), provenance display, catalog additions incl. inherited aliases, sub-round grouping incl. applications stage, panel deliberation/updates, direction vocabulary, source/catalog/network interactions, incomplete and placeholder builds',release}));
