import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';

const root=new URL('../',import.meta.url);
const read=p=>fs.readFileSync(new URL(p,root),'utf8');
const exists=p=>fs.existsSync(new URL(p,root));
function environment(data, code=read('dist/research-round26.js')) {
  const elements=new Map();
  let archivedHandlers=0;
  const element=(id,value='')=>{
    const e={value,textContent:'',innerHTML:'',hidden:false,listeners:{},attributes:{},focused:false,
      addEventListener(k,f){this.listeners[k]=f;},setAttribute(k,v){this.attributes[k]=v;},
      getAttribute(k){return this.attributes[k];},focus(){this.focused=true;}};
    elements.set(id,e);return e;
  };
  const context={window:{ROUND26_DATA:data,ResearchObservatory:{render:r=>'archive:'+r,afterRender(){archivedHandlers++;}}},location:{hash:'#research'},document:{title:'',getElementById:id=>elements.get(id),querySelectorAll:()=>[]}};
  vm.createContext(context);vm.runInContext(code,context);
  return {context,elements,element,R:context.window.ResearchRound26,archivedHandlers:()=>archivedHandlers};
}
const fixture={
  title:'Evidence <and> limits',scope:'Model evidence only.',
  loops:[{loop:'ab1',goal:'AB',title:'Initial calculation',status:'limited',accepted:'Bound within finite scope.',bullets:['A < B'],limitations:['No continuum transfer.'],equations:[{label:'Equation <1>',expression:'x < y && z > 0'}],sources:[{path:'README.md',label:'Research source'}],gate_sha256:'fixture'},
    {loop:'ab2',goal:'AB',title:'Reviewed continuation',status:'conditional',accepted:'Given an explicit premise.',bullets:['Conditional conclusion.'],limitations:['Premise remains open.']}],
  roadmap:{next_goals:[{id:'AG',title:'Future target',first_target:'First check',second_loop:'Select from the first result.'}]},
  network:{nodes:[
    {id:'history-1',title:'Earlier calculation',kind:'history',status:'proved-in-model',summary:'A preserved result.',sources:['README.md']},
    {id:'premise-1',title:'Volume-uniform input',kind:'premise',status:'conditional',summary:'An explicit premise.'},
    {id:'equation-1',title:'Equation & constraint',kind:'equation',status:'proved-in-model',equation:'a < b && c > 0',summary:'Fixed units.'},
    {id:'ab1',title:'Initial calculation',kind:'loop',status:'limited',summary:'Finite model only.',route:'round26-ab1',model:'restricted model'},
    {id:'ab2',title:'Reviewed continuation',kind:'loop',status:'conditional',summary:'Conditional estimate.',route:'round26-ab2'},
    {id:'open-1',title:'Continuum target',kind:'open',status:'planned',summary:'Construction remains open.'}],
    edges:[{from:'history-1',to:'ab1',type:'proven-dependency',label:'Inherited exact input.'},
      {from:'premise-1',to:'ab2',type:'proposed-transfer',label:'Assumption is unproved.'},
      {from:'equation-1',to:'ab2',type:'proven-dependency',label:'Specified identity.'},
      {from:'ab1',to:'ab2',type:'review-selection',label:'Selected after review.'},
      {from:'ab2',to:'open-1',type:'proposed-transfer',label:'No transfer theorem.'}]}
};
const E=environment(structuredClone(fixture)),{R,context,element,elements}=E;
assert.equal(R.status({verdict:'accepted_within_scope'}),'proved-in-model');
assert.equal(R.status({status:'limited',verdict:'accepted_within_scope'}),'limited');
assert.equal(R.status({verdict:'insufficient'}),'limited');
for(const route of ['home','round26-results','research-network','round26-roadmap','round26-ab1','round26-ab2']){
  const html=R.render(route);assert(html.includes('Research navigation'),route);assert(!html.includes('undefined'),route);assert(!html.includes('NaN'),route);
}
assert(R.render('home').includes('Evidence &lt;and&gt; limits'));
assert(R.render('round26-ab1').includes('x &lt; y &amp;&amp; z &gt; 0'));
assert(R.render('round26-ab1').includes('fixture'));
assert(R.render('round26-roadmap').includes('planning only'));
assert(R.render('all-results').includes('archive:all-results'));
assert(R.render('contributions').includes('archive:contributions'));
assert(R.render('round25-home').includes('archive:home'));
assert.equal(R.render('round24-home'),'archive:round24-home');
assert.equal(R.render('resonance-methods'),'archive:resonance-methods');
assert.equal(R.render('newton'),'archive:newton');
assert.equal(R.filteredNodes('VOLUME').length,1);
assert.equal(R.filteredNodes('','limited').length,1);
assert.equal(R.filteredNodes('','all','loop').length,2);
assert.equal(R.filteredNodes('no such result').length,0);
assert(R.catalog('no such result').includes('No entries match'));
assert.equal(R.neighborhood('ab2').nodes.length,5);
assert.equal(R.neighborhood('ab2','proven-dependency').nodes.length,2);
assert.equal(R.neighborhood('ab2','review-selection').edges.length,1);
assert.equal(R.neighborhood('missing').nodes.length,0);
assert(R.graphMap('ab2').includes('<svg'));
assert(R.graphMap('ab2').includes('type="button"'));
assert(R.graphMap('ab2').includes('aria-pressed="true"'));
assert(R.graphMap('ab2').includes('r26-edge-proposed-transfer'));
assert(!R.graphMap('ab2','proven-dependency').includes('class="r26-edge r26-edge-proposed-transfer"'));
assert(R.nodeDetails('ab2').includes('No transfer theorem.'));
assert(R.nodeDetails('equation-1').includes('a &lt; b &amp;&amp; c &gt; 0'));
assert(R.safeSource({url:'javascript:alert(1)',label:'Bad source'}).includes('<span>'));
assert(!R.safeSource({path:'javascript:alert(1)',label:'Bad source'}).includes('href='));
assert(R.safeSource({url:'https://example.org/a?x=1&y=2',label:'A < B'}).includes('A &lt; B'));
assert(R.safeSource({url:'https://example.org/source'}).includes('>https://example.org/source '));
R.data.network.nodes[0].title='<img src=x onerror=alert(1)>';
R.data.network.nodes[0].summary='"<script>bad()</script>';
assert(!R.catalog().includes('<img'));
assert(!R.nodeDetails('history-1').includes('<script>'));
assert(!R.graphMap('ab1').includes('<img'));
R.data.network.edges.push({from:'missing',to:'ab1',type:'proven-dependency'});
assert.equal(R.validEdges().length,5);

for(const [id,value] of [['r26-search',''],['r26-status','all'],['r26-kind','all'],['r26-edge-type','all'],['r26-reset',''],['r26-map-toggle',''],['r26-map',''],['r26-catalog',''],['r26-details',''],['r26-match-count',''],['r26-selected-title','']]) element(id,value);
context.location.hash='#research/research-network?node=ab1';R.afterRender();
assert(elements.get('r26-details').innerHTML.includes('Finite model only.'));
const click=(host,id)=>elements.get(host).listeners.click({target:{closest:()=>({getAttribute:()=>id})}});
click('r26-catalog','ab2');assert(elements.get('r26-details').innerHTML.includes('Conditional estimate.'));
assert(elements.get('r26-selected-title').focused);
click('r26-map','equation-1');assert(elements.get('r26-details').innerHTML.includes('a &lt; b'));
click('r26-details','ab2');assert(elements.get('r26-details').innerHTML.includes('No transfer theorem.'));
elements.get('r26-edge-type').value='proven-dependency';elements.get('r26-edge-type').listeners.change();
assert(!elements.get('r26-details').innerHTML.includes('No transfer theorem.'));
elements.get('r26-search').value='volume';elements.get('r26-search').listeners.input();
assert(elements.get('r26-match-count').textContent.startsWith('1 of 6'));
assert(elements.get('r26-details').innerHTML.includes('An explicit premise.'));
elements.get('r26-search').value='unfindable';elements.get('r26-search').listeners.input();
assert(elements.get('r26-catalog').innerHTML.includes('No entries match'));
assert(elements.get('r26-match-count').textContent.startsWith('0 of 6'));
elements.get('r26-reset').listeners.click();assert.equal(elements.get('r26-search').value,'');assert.equal(elements.get('r26-edge-type').value,'all');
elements.get('r26-kind').value='open';elements.get('r26-kind').listeners.change();assert(elements.get('r26-details').innerHTML.includes('Construction remains open.'));
elements.get('r26-kind').value='all';elements.get('r26-status').value='limited';elements.get('r26-status').listeners.change();assert(elements.get('r26-details').innerHTML.includes('Finite model only.'));
elements.get('r26-map-toggle').listeners.click();assert(elements.get('r26-map').hidden);assert.equal(elements.get('r26-map-toggle').attributes['aria-expanded'],'false');
elements.get('r26-map-toggle').listeners.click();assert(!elements.get('r26-map').hidden);
const before=elements.get('r26-details').innerHTML;click('r26-catalog','invalid');assert.equal(elements.get('r26-details').innerHTML,before);
context.location.hash='#research/research-network?node=%';assert.doesNotThrow(()=>R.afterRender());
context.location.hash='#research/all-results';R.afterRender();assert.equal(E.archivedHandlers(),1);
// The explicit Round25 home archive retains its original endpoint control.
context.window.ResearchRound25={endpoint:z=>({realMinusOne:-z*z,imag:z/84,linearRadius:z*z/3528})};
const archivedSlider=element('r25-z','1');element('r25-z-value');const archivedEndpoint=element('r25-endpoint');
context.location.hash='#research/round25-home';R.afterRender();
assert(archivedEndpoint.innerHTML.includes('1.19048e-8'));
archivedSlider.value='.5';archivedSlider.listeners.input();assert(archivedEndpoint.innerHTML.includes('5.95238e-9'));


let checkedData=0;
for(const folder of ['dist','docs']){
  if(process.argv.includes('--fixture'))continue;
  if(!exists(`${folder}/research-round26-data.js`))continue;
  const C={window:{}};vm.createContext(C);vm.runInContext(read(`${folder}/research-round26-data.js`),C);
  const A=environment(C.window.ROUND26_DATA,read(`${folder}/research-round26.js`)).R;
  assert.equal(A.data.loops.length,10,`${folder}: exactly ten loop records required`);
  const ns=A.data.network?.nodes??A.data.nodes,es=A.data.network?.edges??A.data.edges;
  const ids=new Set(ns.map(n=>n.id));assert.equal(ids.size,ns.length,'Duplicate graph node IDs');
  for(const node of ns){assert(['history','premise','equation','loop','open'].includes(node.kind));assert(node.title);}
  for(const edge of es){assert(ids.has(edge.from),`Missing edge source ${edge.from}`);assert(ids.has(edge.to),`Missing edge target ${edge.to}`);assert(['proven-dependency','proposed-transfer','review-selection'].includes(edge.type));}
  assert.equal(A.validEdges().length,es.length);
  for(const loop of A.data.loops){
    const id=loop.loop??loop.id;const html=A.render('round26-'+id);assert(html.includes('Round26'),id);assert(!html.includes('undefined'),id);
    for(const s of loop.sources??[]){const path=typeof s==='string'?s:s.path;if(path)assert(exists(path),`Missing source: ${path}`);}
    if(loop.gate_sha256){
      const source=(loop.sources??[]).map(s=>typeof s==='string'?s:s.path).find(p=>p?.endsWith(`${id}-gate.json`));
      if(source)assert.equal(loop.gate_sha256,createHash('sha256').update(read(source)).digest('hex'));
    }
  }
  const scripts=[...read(`${folder}/index.html`).matchAll(/<script\s+src="([^"]+)"/g)].map(x=>x[1].split('/').pop());
  assert(scripts.indexOf('research-round26.js')>scripts.indexOf('research-round25.js'));
  assert(scripts.indexOf('research-round26.js')<scripts.indexOf('app.js'));
  assert.equal(scripts.filter(x=>x==='research-round26.js').length,1);
  assert(scripts.indexOf('research-round26-data.js')<scripts.indexOf('research-round26.js'));
  checkedData++;
}
if(!process.argv.includes('--fixture'))assert.equal(checkedData,2,'Both dist and docs must be built');
console.log(JSON.stringify({status:'passed',integratedDataBundles:checkedData,scope:'actual search, status/kind/edge/reset/map/native-selection handlers; graph edge integrity; source protocol and text escaping; historical delegation; routes, gate hashes and script order when built'}));
