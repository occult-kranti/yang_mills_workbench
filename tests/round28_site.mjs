import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';

const root = new URL('../', import.meta.url);
const read = path => fs.readFileSync(new URL(path, root), 'utf8');
const exists = path => fs.existsSync(new URL(path, root));
const code = read('dist/research-round28.js');
function environment(data, script = code) {
  const elements = new Map(), calls = {render:[],after:0,cleanup:0};
  const element = (name, value = '') => {
    const item = {value,innerHTML:'',textContent:'',listeners:{},attributes:{},hidden:false,focused:false,addEventListener(type,handler){this.listeners[type]=handler;},setAttribute(name,value){this.attributes[name]=value;},focus(){this.focused=true;}};
    elements.set(name,item);return item;
  };
  const context = {URL,location:{hash:'#research'},document:{title:'',getElementById:name=>elements.get(name)},window:{ROUND28_DATA:data,ResearchJourney:{cleanup(){calls.cleanup++;}},ResearchObservatory:{inherited:'retained',render(route){calls.render.push(route);return 'archive:'+route;},afterRender(){calls.after++;}}}};
  vm.createContext(context);vm.runInContext(script,context);
  return {R:context.window.ResearchRound28,context,elements,element,calls};
}
const gate = 'a'.repeat(64);
const fixture = {
  title:'A result <with> conditions',summary:'Check the model & scale.',
  loops:[
    {id:'ag2',goal:'AG',title:'Reviewed first step',stage:'reviewed',verdict:'accepted_with_limits',accepted:'A bound at the stated model.',gate_sha256:gate,model:'Finite source model',bullets:['x < y'],limitations:['The full mixing source is still present.'],equations:[{label:'Estimate <1>',expression:'x < y && z > 0',scope:'Only at the fixed reference scale.'}],derivation_steps:['Inventory all supports.'],applications:['A scoped comparison.'],sources:['research/round28/forward/ag2/report.md']},
    {id:'ag3',goal:'AG',title:'Reviewed second step',stage:'reviewed',verdict:'limited',accepted:'A limitation established.',gate_sha256:gate,limitations:['No continuum transfer.'],equations:[],sources:['research/round28/reverse/ag3/report.md']},
    {id:'new-step',goal:'AI',title:'Next selected question',stage:'in-progress',verdict:'accepted',accepted:'UNREVIEWED_RESULT_MUST_NOT_RENDER',bullets:['UNREVIEWED_BULLET'],equations:[{label:'UNREVIEWED_EQUATION',expression:'x=y'}],limitations:['UNREVIEWED_LIMIT'],sources:['research/round28/contracts/new-step.json']}
  ],
  goal_pairs:[{id:'AG',target:'A complete first correction',loops:['ag2','ag3']},{id:'AI',target:'Probe the physical readout',loops:['new-step','ai4']}],
  progress:{requested:10,completed:10,selected:10,percentage_statement:'No defensible percentage of a continuum proof.',obligations:[{name:'Construction',status:'Open',missing:['Nontrivial continuum theory.','Axioms and scale matching.']}]},
  roadmap:{next_goals:[{id:'AJ',title:'Future question',target:'Supply the missing input.'}]},
  addendum:{title:'Round28 addendum',url:'ym-round28-addendum.pdf'},
  survey:{records:[
    {id:'n1',lens:'newton',title:'Fluxions <notes>',category:'historical_primary',depth:'Selected passages only.',urls:['https://example.org/notes?a=1&b=2'],use:'Comparison of hypotheses.',limits:'Historical inspiration only.',change_status:'deepened_prior_source',change_basis:'Additional passages were read.',ledger:'research/round28/experts/newton/sources.json'},
    {id:'t1',lens:'tesla',title:'Noise cancellation',category:'technical_primary',depth:'Abstract only.',urls:['https://example.org/notes?a=1&b=2','https://example.org/research'],use:'Candidate receiver comparison.',limits:'No theorem imported.',change_status:'new_round28_lens_reading_record'},
    {id:'j1',lens:'jung',title:'A conversation about patterns',category:'forum_discourse',depth:'Thread excerpt.',urls:['https://www.reddit.com/r/test/comments/example'],use:'A lead to test.',limits:'Unverified discourse.'}
  ],screening:[{id:'screen-1',url:'https://example.org/screen',reading_depth:'Metadata only.',use:'Not a technical premise.'}],interpretation_limits:['Source counts are not physics-loop counts.'],government_context:{scope:'No new government-document reading recorded.'},discrepancies:[{record_id:'n1',issue:'Date differs.',resolution:'Use the inspected edition.'}],sources:['research/round28/experts/sources.json']}
};
const E = environment(structuredClone(fixture)), {R,context,calls,element,elements} = E;
assert.equal(context.window.ResearchObservatory.inherited,'retained');
assert.equal(R.counts().completed,2,'Claimed progress must not replace actual reviewed records');
assert.equal(R.counts().selected,3);
assert.equal(R.counts().remaining,8);
assert.equal(R.reviewed(fixture.loops[2]),false);
assert.equal(R.reviewed({...fixture.loops[0],gate_sha256:'bad'}),false);
assert.equal(R.reviewed({...fixture.loops[0],verdict:'planned'}),false);
for (const route of ['home','round28','round28-results','round28-sources','round28-roadmap','round28-proof','round28-addendum','round28-ag2','round28-ag3','round28-new-step','round28/home','round28/loops','round28/sources']) {
  const html = R.render(route);
  assert(html.includes('Research navigation'),route);
  assert(!html.includes('undefined'),route);
  assert(!html.includes('NaN'),route);
  assert(!html.includes('UNREVIEWED_'),route);
}
assert(R.render('home').includes('>2<small> / 10</small>'));
assert(R.render('home').includes('not a percentage of Yang–Mills solved'));
assert(!R.render('home').includes('This requested cycle is complete.'));
assert(R.render('home').includes('3 later goals remain to be selected'));
assert(!R.render('home').includes('href="#research/round28-ai4"'),'Unselected future loops are not promoted to routes');
assert(R.render('round28-ag2').includes('x &lt; y &amp;&amp; z &gt; 0'));
assert(R.render('round28-ag2').includes('The full mixing source is still present.'));
assert(R.render('round28-ag2').includes('Only at the fixed reference scale.'));
assert(R.render('round28-new-step').includes('No reviewed finding is recorded'));
assert(R.render('round28-proof').includes('Nontrivial continuum theory.'));
assert.equal((R.render('round28-proof').match(/<th scope="row">/g)??[]).length,1);
assert(R.render('round28-roadmap').includes('Supply the missing input.'));
assert(R.render('round28-addendum').includes('href="ym-round28-addendum.pdf"'));
assert(R.render('drafts').endsWith('archive:drafts'));
assert(R.render('drafts').includes('Round28 addendum'));
assert(R.render('round27-home').includes('archive:home'));
for (const route of ['research-network?node=r27-ai1','round27-proof','round26-home','resonance-methods','all-results','contributions','drafts?version=1']) assert(R.render(route).includes('archive:'+route),route);
context.location.hash='#research/round28/home';assert(R.render('round28').includes('A result &lt;with&gt; conditions'));
context.location.hash='#research/round28/sources';assert(R.render('round28').includes('Filter source readings'));
context.location.hash='#research/round28/ag2';assert(R.render('round28').includes('Inventory all supports.'));
context.location.hash='#research/round28-proof';R.afterRender();assert.equal(context.document.title,'Round28 proof obligations · Yang–Mills Workbench');
context.location.hash='#research/round27-home';R.afterRender();assert.equal(context.document.title,'Round27 archive · Yang–Mills Workbench');
context.location.hash='#research/research-network?node=x';R.afterRender();assert.equal(calls.after,1);
context.location.hash='#research/drafts';R.afterRender();assert.equal(calls.after,2);

assert.equal(R.filterSources('FLUXIONS').length,1);
assert.equal(R.filterSources('','tesla').length,1);
assert.equal(R.filterSources('','all','forum_discourse').length,1);
assert.equal(R.filterSources('noise','newton').length,0);
assert(R.sourceCards('no match').includes('No reading records match'));
assert(R.sourceCards().includes('Selected passages only.'));
assert(R.sourceCards().includes('Historical inspiration only.'));
assert(R.sourceCards().includes('Abstract only.'));
assert(R.sourceCards().includes('No theorem imported.'));
assert(R.render('round28-sources').includes('<dt>Reading records</dt><dd>3</dd>'));
assert(R.render('round28-sources').includes('<dt>Distinct recorded URLs</dt><dd>3</dd>'));
assert(R.render('round28-sources').includes('<dt>URLs including screening</dt><dd>4</dd>'));
assert(R.render('round28-sources').includes('not a count of distinct studies'));
assert(R.render('round28-sources').includes('No new government-document reading recorded.'));
for (const [name,value] of [['r28-source-search',''],['r28-source-lens','all'],['r28-source-category','all'],['r28-source-reset',''],['r28-source-cards',''],['r28-source-count','']]) element(name,value);
context.location.hash='#research/round28/sources';R.afterRender();
assert.equal(context.document.title,'Round28 source survey · Yang–Mills Workbench');
assert.equal(elements.get('r28-source-count').textContent,'3 of 3 reading records shown.');
elements.get('r28-source-search').value='noise';elements.get('r28-source-search').listeners.input();
assert.equal(elements.get('r28-source-count').textContent,'1 of 3 reading records shown.');
assert(elements.get('r28-source-cards').innerHTML.includes('Noise cancellation'));
elements.get('r28-source-lens').value='newton';elements.get('r28-source-lens').listeners.change();
assert(elements.get('r28-source-cards').innerHTML.includes('No reading records match'));
elements.get('r28-source-reset').listeners.click();
assert.equal(elements.get('r28-source-search').value,'');assert.equal(elements.get('r28-source-lens').value,'all');
assert(elements.get('r28-source-search').focused);
elements.get('r28-source-category').value='forum_discourse';elements.get('r28-source-category').listeners.change();
assert(elements.get('r28-source-cards').innerHTML.includes('A conversation about patterns'));
assert(!elements.get('r28-source-cards').innerHTML.includes('Noise cancellation'));

for (const value of ['javascript:alert(1)','data:text/html,<script>','//example.org/','https://name:pass@example.org/','https:\\example.org/a','https://example.org/\nx','http://example.org/']) assert.equal(R.safeURL(value),'',value);
for (const value of ['../secret','/absolute','ok/../secret','ok//secret','x%2fsecret','x#fragment','x?query','x\\y']) assert.equal(R.safePath(value),'',value);
assert(R.source({url:'javascript:alert(1)',title:'bad'}).startsWith('<span>'));
assert(R.source({url:'https://example.org/a?x=1&y=2',title:'A < B'}).includes('A &lt; B'));
assert(R.source('https://example.org/read').includes('href="https://example.org/read"'));
const attack='<img src=x onerror="alert(1)"><script>bad()</script>', hostile=structuredClone(fixture);
hostile.title=attack;hostile.summary=attack;hostile.loops[0].title=attack;hostile.loops[0].accepted=attack;hostile.loops[0].limitations=[attack];hostile.loops[0].equations=[{label:attack,expression:attack,scope:attack}];
hostile.progress.percentage_statement=attack;hostile.progress.obligations=[{name:attack,status:attack,missing:attack}];
hostile.survey.records=[{lens:attack,title:attack,category:attack,depth:attack,urls:['javascript:alert(1)'],use:attack,limits:attack,change_basis:attack,ledger:'../bad'}];
hostile.addendum={url:'javascript:alert(1)',title:attack};hostile.roadmap.next_goals=[{id:attack,title:attack,target:attack}];
const H=environment(hostile).R;
for(const route of ['home','round28-ag2','round28-sources','round28-roadmap','round28-proof','round28-addendum','drafts']) {
  const html=H.render(route);assert(!html.includes('<img'),route);assert(!html.includes('<script>'),route);assert(!html.includes('href="javascript:'),route);
}
assert.equal(environment(undefined).R,undefined);
const empty=environment({}).R;
assert(empty.render('home').includes('0 selected'));
assert(empty.render('round28-proof').includes('has not been recorded'));
assert(empty.render('round28-addendum').includes('not available in this checkpoint'));
const metadataFixture=structuredClone(fixture);
metadataFixture.survey.records.push({id:'metadata',lens:'feynman',category:'bibliographic_primary',title:'Publication identity',depth:'Publication metadata only.',urls:['https://example.org/publication'],limits:'No technical validation.'});
metadataFixture.survey.sources=[{path:'research/round28/experts/source-survey.md',title:'Initial source survey'},{path:'research/round28/experts/sources.json',title:'Initial source survey · reading ledger'},{path:'research/round28/experts/source-supplement.md',title:'Supplemental source review'},{path:'research/round28/experts/source-supplement.json',title:'Supplemental source review · reading ledger'}];
metadataFixture.survey.unread_leads=[{id:'unread',url:'https://example.org/unopened',reading_depth:'Not opened in this pass.',context:'Parent-supplied lead.'}];
const M=environment(metadataFixture).R;
assert(M.render('round28-sources').includes('Bibliographic metadata'));
assert(M.sourceCards('','all','bibliographic_primary').includes('Publication metadata only.'));
assert(M.sourceCards('','all','bibliographic_primary').includes('No technical validation.'));
assert(M.render('round28-sources').includes('source-supplement.md'));
assert(M.render('round28-sources').includes('source-supplement.json'));
assert(M.render('round28-sources').includes('Unopened leads · excluded from reading and screening counts'));
assert.equal(M.filterSources('unopened').length,0);

const networkFixture=structuredClone(fixture);
networkFixture.network={nodes:[
  {id:'old',kind:'history',status:'proved-in-model',title:'Earlier model calculation',summary:'Preserved scope.'},
  {id:'source',kind:'literature',status:'source-reviewed',title:'Historical <source>',summary:'A method comparison.',detail:'Reading depth: selected passages only. No physical premise.',sources:['https://example.org/manuscript','research/round28/experts/newton/sources.json'],route:'round28-sources'},
  {id:'r28-ag2',kind:'loop',status:'limited',title:'AG2 reviewed loop',summary:'A limited result.',route:'round28-ag2'},
  {id:'eq',kind:'equation',status:'proved-in-model',title:'A scoped equation',equation:'a < b && c > 0'},
  {id:'open',kind:'open',status:'planned',title:'Continuum construction',summary:'Missing input.'},
  {id:'unfamiliar',kind:'new-kind',status:'unspecified',title:'Additional record',summary:'An unclassified entry.'}
],edges:[
  {from:'old',to:'r28-ag2',type:'proven-dependency',label:'Inherited exact model input'},
  {from:'source',to:'r28-ag2',type:'review-selection',label:'Methodological comparison only'},
  {from:'r28-ag2',to:'eq',type:'proven-dependency',label:'Within-model derivation'},
  {from:'r28-ag2',to:'open',type:'proposed-transfer',label:'Missing continuum transfer'},
  {from:'source',to:'unfamiliar',type:'proposed-transfer',label:'Prospective comparison'},
  {from:'missing',to:'r28-ag2',type:'proven-dependency'},
  {from:'old',to:'r28-ag2',type:'invented-type'}
]};
const N=environment(networkFixture),NR=N.R;
assert.equal(NR.validEdges().length,5);
assert.equal(NR.filterNodes('','literature').length,1);
assert.equal(NR.filterNodes('historical').length,1);
assert.equal(NR.neighborhood('source').nodes.length,3);
assert.equal(NR.neighborhood('source','review-selection').edges.length,1);
assert.equal(NR.neighborhood('missing').nodes.length,0);
assert(NR.networkCatalog().includes('Literature and historical sources'));
assert(NR.networkCatalog().includes('Additional record'));
assert(NR.networkDetails('source').includes('Source reviewed · not a physics premise'));
assert(!NR.networkDetails('source').includes('Proved within stated model'));
assert(NR.networkDetails('source').includes('Reading depth: selected passages only.'));
assert(NR.networkDetails('source').includes('href="https://example.org/manuscript"'));
assert(NR.networkDetails('source').includes('Methodological comparison only'));
assert(NR.networkDetails('eq').includes('a &lt; b &amp;&amp; c &gt; 0'));
assert(NR.networkMap('source').includes('Historical &lt;source&gt;'));
assert(NR.networkMap('source').includes('r28-map-node-source'));
assert(NR.networkMap('source').includes('r28-net-edge-review-selection'));
assert(!NR.networkMap('source','proven-dependency').includes('Methodological comparison only'));
assert(NR.render('research-network').includes('not vertices, links or states of a physical gauge graph'));
for(const [name,value] of [['r28-network-search',''],['r28-network-kind','all'],['r28-network-edge','all'],['r28-network-reset',''],['r28-network-catalog',''],['r28-network-details',''],['r28-network-map',''],['r28-network-count',''],['r28-network-map-toggle',''],['r28-network-selected','']])N.element(name,value);
N.context.location.hash='#research/research-network?node=source';NR.afterRender();
assert(N.elements.get('r28-network-details').innerHTML.includes('Historical &lt;source&gt;'));
const choose=(host,target)=>N.elements.get(host).listeners.click({target:{closest:()=>({getAttribute:()=>target})}});
choose('r28-network-map','r28-ag2');assert(N.elements.get('r28-network-details').innerHTML.includes('A limited result.'));
assert(N.elements.get('r28-network-selected').focused);
choose('r28-network-details','source');assert(N.elements.get('r28-network-details').innerHTML.includes('No physical premise.'));
N.elements.get('r28-network-edge').value='proven-dependency';N.elements.get('r28-network-edge').listeners.change();
assert(N.elements.get('r28-network-details').innerHTML.includes('No direct relations match'));
N.elements.get('r28-network-search').value='continuum';N.elements.get('r28-network-search').listeners.input();
assert(N.elements.get('r28-network-count').textContent.startsWith('1 of 6'));
assert(N.elements.get('r28-network-details').innerHTML.includes('Missing input.'));
N.elements.get('r28-network-reset').listeners.click();
assert.equal(N.elements.get('r28-network-search').value,'');assert.equal(N.elements.get('r28-network-edge').value,'all');
N.elements.get('r28-network-kind').value='literature';N.elements.get('r28-network-kind').listeners.change();
assert(N.elements.get('r28-network-catalog').innerHTML.includes('Historical &lt;source&gt;'));
assert(!N.elements.get('r28-network-catalog').innerHTML.includes('AG2 reviewed loop'));
N.elements.get('r28-network-map-toggle').listeners.click();
assert(N.elements.get('r28-network-map').hidden);assert.equal(N.elements.get('r28-network-map-toggle').attributes['aria-expanded'],'false');
N.elements.get('r28-network-map-toggle').listeners.click();assert(!N.elements.get('r28-network-map').hidden);
const before=N.elements.get('r28-network-details').innerHTML;choose('r28-network-catalog','missing');assert.equal(N.elements.get('r28-network-details').innerHTML,before);
N.context.location.hash='#research/research-network?node=%';assert.doesNotThrow(()=>NR.afterRender());
networkFixture.network.nodes[1].title=attack;networkFixture.network.nodes[1].detail=attack;
const NH=environment(networkFixture).R;
assert(!NH.networkCatalog().includes('<img'));assert(!NH.networkMap('source').includes('<script>'));assert(!NH.networkDetails('source').includes('<img'));

let bundles=0;
if(!process.argv.includes('--fixture')) {
  for(const folder of ['dist','docs']) {
    if(folder==='docs'&&!exists('docs/research-round28-data.js')&&!process.argv.includes('--release'))continue;
    const C={window:{ROUND26_DATA:{},ROUND27_DATA:{network:{nodes:[],edges:[]}}}};vm.createContext(C);vm.runInContext(read(`${folder}/research-round28-data.js`),C);
    const data=C.window.ROUND28_DATA,A=environment(data,read(`${folder}/research-round28.js`)).R;
    assert.equal(A.counts().completed,data.progress.completed,'Browser count differs from built reviewed records');
    assert.equal(A.counts().requested,10);
    assert(data.progress.completed<=10);
    for(const loop of data.loops.filter(A.reviewed)) {
      const gatePath=`research/round28/advisor/${loop.id}-gate.json`;
      assert.equal(loop.gate_sha256,createHash('sha256').update(read(gatePath)).digest('hex'),'Gate changed since browser bundle build');
      for(const path of loop.sources)assert(exists(path),'Missing evidence '+path);
    }
    assert.equal(data.survey.counts.readings,data.survey.records.length);
    assert.equal(data.survey.counts.urls,new Set(data.survey.records.flatMap(item=>item.urls)).size);
    assert.equal(new Set(data.survey.records.map(item=>item.id)).size,data.survey.records.length);
    assert.equal(data.survey.counts.screening,data.survey.screening.length);
    assert.equal(data.survey.counts.urls_including_screening,new Set([...data.survey.records.flatMap(item=>item.urls),...data.survey.screening.map(item=>item.url)]).size);
    const scripts=[...read(`${folder}/index.html`).matchAll(/<script\s+src="([^"]+)"/g)].map(match=>match[1].split('/').pop());
    assert.equal(scripts.filter(name=>name==='research-round28.js').length,1);
    assert(scripts.indexOf('research-round28-data.js')>scripts.indexOf('research-round27-data.js'));
    assert(scripts.indexOf('research-round28-data.js')<scripts.indexOf('research-round26.js'));
    assert(scripts.indexOf('research-round28.js')>scripts.indexOf('research-round27.js'));
    assert(scripts.indexOf('research-round28.js')<scripts.indexOf('app.js'));
    assert(read(`${folder}/index.html`).includes('research-round28.css'));
    if(data.network){
      assert.equal(C.window.ROUND26_DATA.network.nodes.length,data.network.nodes.length);
      assert.equal(A.validEdges().length,data.network.edges.length);
      const literature=data.network.nodes.filter(node=>node.kind==='literature');
      assert.equal(A.filterNodes('','literature').length,literature.length);
      for(const node of literature){assert(A.networkDetails(node.id).includes('Source reviewed · not a physics premise'));assert(A.networkMap(node.id).includes('r28-map-node-source'));}
    }
    if(process.argv.includes('--release'))assert.equal(A.counts().completed,10);
    bundles++;
  }
}
console.log(JSON.stringify({status:'passed',bundles,scope:'Reviewed-gate counts, pending-result suppression, nested and historical routes, source and network filter/reset/selection/map handlers, literature graph semantics, reading depth, URL/HTML safety, evidence hashes and script order when integrated.'}));
