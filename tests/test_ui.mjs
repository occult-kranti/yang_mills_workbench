// Function and event-handler integration checks using a minimal DOM stand-in.
// This is not a browser layout, accessibility, or end-to-end test.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const base=new URL('../dist/',import.meta.url);
const nodes=new Map(),events={},saved=new Map();let inputs=[];
function node(id){if(!nodes.has(id))nodes.set(id,{id:id.replace(/^#/,''),innerHTML:'',textContent:'',style:{},dataset:{},value:'',open:false,addEventListener(){},focus(){},setSelectionRange(){},showModal(){if(this.open)throw Error('already open');this.open=true},close(){this.open=false},classList:{toggle(){},contains(){return false}},setAttribute(){}});return nodes.get(id)}
const ctx={console,URL,Blob,setTimeout:()=>0,clearTimeout(){},location:{hash:'#study'},localStorage:{getItem:k=>saved.get(k)||null,setItem:(k,v)=>saved.set(k,v)},document:{querySelector:node,querySelectorAll:()=>inputs,getElementById:id=>node('#'+id),addEventListener:(name,fn)=>events[name]=fn,title:''},confirm:()=>true};
ctx.window=ctx;ctx.addEventListener=()=>{};vm.createContext(ctx);
for(const file of ['content.js','calculators.js','expansion-tools.js','patents.js','research-data.js','research.js','research-hub-data.js','research-hub.js','research-closures-data.js','research-closures.js','app.js'])vm.runInContext(fs.readFileSync(new URL(file,base),'utf8'),ctx,{filename:file});
const run=code=>vm.runInContext(code,ctx);
const D=ctx.PHYSICS,T=ctx.PhysicsTools;
for(const page of ['home','variables','finite','gravity','cutoff','proofs','solutions','audit','proof-map','next',...ctx.OBSERVATORY_HUB.claims.map(c=>'solution/'+c.id)]){
 ctx.location.hash='#research/'+page;run('render()');assert(node('#main').innerHTML.includes('hub-nav'));assert.match(node('#main').innerHTML,/<h1>/);
}
const escape=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const view of ['study','paths','explore','laboratory','papers','pioneers','projects','resources','advisor',...D.specialisms.map(s=>s.id)]){
 ctx.location.hash='#'+view;run('render()');assert(node('#main').innerHTML.length>1500,view);assert.match(node('#main').innerHTML,/<h1>/);
}
for(const s of D.specialisms){
 ctx.location.hash='#'+s.id;run('render()');const html=node('#main').innerHTML;
 assert.equal((html.match(/data-topic-done=/g)||[]).length,6);
 assert.equal((html.match(/data-lesson=/g)||[]).length,18);
 for(const m of s.modules){assert(html.includes(escape(m.gate)));for(const l of m.lessons)assert(html.includes(escape(l.practice)));}
 for(const id of s.tools)assert(T.catalogue.some(t=>t.id===id),s.id+' missing tool '+id);
 for(const p of s.projects)assert(html.includes(escape(p.deliver)));
 for(const c of s.claims)assert(html.includes(escape(c.assessment)));
}
const topic=D.specialisms[0],module=topic.modules[0];
await events.change({target:{dataset:{topicDone:module.id,topic:topic.id},checked:true}});
assert(run(`state.topicDone.includes(${JSON.stringify(module.id)})`));assert.equal(node('#subject-progress').textContent,'1 of 6 module gates complete');
events.input({target:{id:'subject-note',dataset:{topicNote:topic.id},value:'Evidence: </textarea><img src=x onerror=alert(1)>'}});
ctx.location.hash='#'+topic.id;run('render()');assert(!node('#main').innerHTML.includes('<img'));
await events.change({target:{dataset:{lesson:module.id+'-0'},checked:true}});
const roundtrip=run('clean(JSON.parse(JSON.stringify(state)))');assert(roundtrip.topicDone.includes(module.id));assert(roundtrip.lessons.includes(module.id+'-0'));assert(roundtrip.topicNotes[topic.id].includes('Evidence:'));
const old=run("clean({version:1,path:'combined',hours:8,done:['P001'],lessons:['P001-0'],notes:{P001:'Keep me'},paperNotes:{a:'paper'}})");assert.equal(old.topicDone.length,0);assert.equal(Object.keys(old.topicNotes).length,0);assert.equal(old.notes.P001,'Keep me');
const invalidTopic=run("clean({version:1,topicDone:['bad'],topicNotes:{bad:'discard'},lessons:['bad-0']})");assert.equal(invalidTopic.topicDone.length,0);assert.equal(Object.keys(invalidTopic.topicNotes).length,0);
const feedTarget={closest(sel){return sel==='[data-feed]'?{dataset:{feed:'math.MG'}}:null}};events.click({target:feedTarget});assert.equal(ctx.location.hash,'papers');assert.equal(run('paperCategory'),'math.MG');ctx.location.hash='#papers';run('render()');assert(node('#main').innerHTML.includes('value="math.MG" selected'));
const polygonPlot=run("svgPlot(T.compute('regular_polygon',{n:4,R:1}).plot)");const coords=polygonPlot.match(/<polyline[^>]*points="([^"]+)"/)[1].split(' ').map(p=>p.split(',').map(Number));assert(Math.abs((coords[0][0]-coords[2][0])-(coords[3][1]-coords[1][1]))<.01,'Geometry plot has equal physical scale on both axes');
for(const c of D.chapters){
 run(`openChapter(${JSON.stringify(c.id)})`);const html=node('#chapter-content').innerHTML;
 for(const key of ['derive','exercise','gate','misconception'])assert(html.includes(escape(c[key])),c.id+' '+key);
 for(const id of c.tools)assert(T.catalogue.some(t=>t.id===id),'missing tool '+id);
 assert.equal((html.match(/data-lesson=/g)||[]).length,5);
}
for(const p of D.papers){run(`openPaper(${JSON.stringify(p.id)})`);const html=node('#paper-content').innerHTML;for(const key of ['status','summary','method','limits'])assert(html.includes(escape(p[key])),p.id+' '+key);}
const history=run('pioneers()');for(const p of D.pioneers)for(const t of p.reading)assert(history.includes(escape(t)));
const projectHTML=run('projects()');for(const p of D.projects)assert(projectHTML.includes(escape(p.tool)));
assert(run('resourcesPage()').includes('Direct retrieval returned 403'));
run("domainFilter='quantum';query='';state.path='combined'");const quantum=run('study()');assert(!quantum.includes('data-chapter="P001"'));assert(quantum.includes('data-chapter="P061"'));
run("state.done=['P001'];state.hours=8;domainFilter='';query=''");assert(run('paths()').includes('1 complete'));
for(const t of T.catalogue){inputs=t.fields.map(f=>({dataset:{field:f.key},value:String(f.value)}));run(`activeTool=${JSON.stringify(t.id)};renderCalc()`);assert(!node('#calc-output').innerHTML.includes('role="alert"'),t.id);}
inputs=[{dataset:{field:'V'},value:''},{dataset:{field:'R'},value:'1'}];run("activeTool='circuit';renderCalc()");assert.match(node('#calc-output').innerHTML,/role="alert"/);
const malicious='</textarea><img src=x onerror=alert(1)>';
run(`state.notes.P001=${JSON.stringify(malicious)};openChapter('P001')`);assert(!node('#chapter-content').innerHTML.includes('<img'));
const worksheet='Question:\nDoes this model fit?\n\nLimits:\nSmall sample.';node('[data-paper-note]').value=worksheet;
const target={closest(sel){return sel==='[data-save-paper]'?{dataset:{savePaper:D.papers[0].id}}:null}};
events.click({target});run(`openPaper(${JSON.stringify(D.papers[0].id)})`);assert(node('#paper-content').innerHTML.includes(worksheet));assert(saved.has('physics-observatory-v1'));
const toolTarget={closest(sel){return sel==='[data-tool]'?{dataset:{tool:'quantum_well'}}:null}};events.click({target:toolTarget});assert.equal(ctx.location.hash,'laboratory');assert.equal(node('#chapter-dialog').open,false);
ctx.fetch=async()=>({ok:true,json:async()=>({papers:[{id:'2601.12345',title:'<script>bad</script>',authors:['A'],date:'2026-01-01',status:'unverified',category:'quant-ph',url:'https://arxiv.org/abs/2601.12345'}],cached:true,fetchedAt:'2026-09-01T00:00:00Z',category:'quant-ph',error:'showing cached data'})});
ctx.location.hash='#papers';await run('refreshPapers()');assert(node('#main').innerHTML.includes('&lt;script&gt;'));assert(node('#main').innerHTML.includes('showing cached data'));assert(node('#main').innerHTML.includes('2026-09-01T00:00:00Z'));
ctx.fetch=async()=>{throw Error('offline')};await run('refreshPapers()');assert(node('#main').innerHTML.includes('&lt;script&gt;'));assert(node('#main').innerHTML.includes('offline'));
assert.equal(run("safeURL('javascript:alert(1)')"),'#');
const cleaned=run("clean({version:1,path:'missing',hours:999,done:['P001','bad','P001'],lessons:['P001-0','bad'],notes:{P001:'x',bad:'y'},paperNotes:{}})");assert.equal(cleaned.hours,80);assert.equal(cleaned.done.length,1);assert.equal(cleaned.path,'combined');
// Patent room: source integrity, tab-specific filters, links and notebook state.
const P=D.patents, PR=ctx.PatentRoom;
for(const tab of ['dossiers','catalogue','newton','plan','evidence']){
 ctx.location.hash='#patents/'+tab;run('render()');assert.match(node('#main').innerHTML,/<h1>Patent research room<\/h1>/);assert(node('#navigation').innerHTML.includes('href="#patents"'));
}
assert.equal(PR.filterInventory(P.inventory,{section:'US'}).length,112);
assert.equal(PR.filterInventory(P.inventory,{section:'Foreign',group:'Tesla',theme:'Orgone'}).length,199,'Hidden dossier filters must not erase catalogue results');
assert.equal(PR.filterInventory(P.inventory,{country:'New South Wales'}).length,4);
assert.equal(PR.filterInventory(P.inventory,{country:'France'}).length,30);
assert.equal(PR.filterCases(P.cases,{group:'Tesla',country:'France',section:'Foreign'}).length,12,'Hidden catalogue filters must not erase dossiers');
assert.equal(PR.filterCases(P.cases,{theme:'Orgone'}).length,3);
assert(PR.filterCases(P.cases,{search:'us685957a'}).some(c=>c.id==='US685957A')); // Also finds the companion document's explicit reference.
const reissue=P.inventory.find(r=>r.id==='US-097');assert.equal(reissue.url,'https://patents.google.com/patent/USRE11865E/en');assert(reissue.correction.includes('21 September 1900'));
assert.equal(P.inventory.filter(r=>!r.granted).length,2);
const catalogue1=PR.render(D,{}, {page:1},'catalogue'),catalogue2=PR.render(D,{}, {page:2},'catalogue');
assert.equal((catalogue1.match(/<tr>/g)||[]).length,26);assert(catalogue1.includes('US-001'));assert(catalogue2.includes('US-026'));assert(!catalogue2.includes('US-001'));
assert(PR.render(D,{}, {page:999},'catalogue').includes('page 13 of 13'));
assert(PR.render(D,{}, {search:'no-matching-record-xyz'},'catalogue').includes('No catalogue records match'));
const newtonSearch=PR.render(D,{}, {search:'N11'},'newton');assert(newtonSearch.includes('MINT00054'));assert(!newtonSearch.includes('NATP00007'));
const planHTML=PR.render({...D,tools:T.catalogue},{patentDone:[]}, {},'plan');
assert.equal((planHTML.match(/data-patent-done=/g)||[]).length,10);
for(const m of P.modules){assert(planHTML.includes(escape(m.gate)));for(const l of m.lessons)assert(planHTML.includes(escape(l.practice)));for(const id of m.tools)assert(T.catalogue.some(t=>t.id===id));}
for(const p of P.projects)assert(planHTML.includes(escape(p.deliver)));
const dossierHTML=PR.render(D,{}, {},'dossiers');for(const c of P.cases)for(const field of ['claim','inputs','assessment','test'])assert(dossierHTML.includes(escape(c[field])),c.id+' '+field);
const evidenceHTML=PR.render(D,{}, {},'evidence');for(const c of P.coverage)assert(evidenceHTML.includes(escape(c)));for(const c of P.connections){assert(evidenceHTML.includes(escape(c.from)));assert(evidenceHTML.includes(escape(c.to)));}
await events.change({target:{id:'',dataset:{patentDone:'PA02'},checked:true}});assert(run("state.patentDone.includes('PA02')"));assert.equal(node('#patent-progress').textContent,'1 of 10 module gates complete');
events.input({target:{id:'',dataset:{patentNote:'US685957A'},value:malicious}});
ctx.location.hash='#patents/dossiers';run('render()');assert(!node('#main').innerHTML.includes('<img'));assert(node('#main').innerHTML.includes('&lt;/textarea&gt;'));
const patentBackup=run('clean(JSON.parse(JSON.stringify(state)))');assert(patentBackup.patentDone.includes('PA02'));assert.equal(patentBackup.patentNotes.US685957A,malicious);
assert.equal(old.patentDone.length,0);assert.equal(Object.keys(old.patentNotes).length,0);
const invalidPatent=run("clean({version:1,patentDone:['PA02','bad','PA02'],patentNotes:{N11:'retain',bad:'remove'}})");assert.equal(invalidPatent.patentDone.length,1);assert.equal(Object.keys(invalidPatent.patentNotes).length,1);
run("patentFilters.country='France';patentFilters.theme='Orgone';patentFilters.page=10");
const recordTarget={closest(sel){return sel==='[data-patent-find]'?{dataset:{patentFind:'N11'}}:null}};events.click({target:recordTarget});assert.equal(ctx.location.hash,'patents/newton');assert.equal(run('patentFilters.search'),'N11');assert.equal(run('patentFilters.country'),'');
ctx.location.hash='#patents/catalogue';await events.change({target:{id:'patent-country',value:'France',dataset:{}}});assert.equal(run('patentFilters.page'),1);
events.click({target:{closest:sel=>sel==='[data-patent-reset]'?{}:null}});assert.equal(run('patentFilters.search'),'');assert.equal(run('patentFilters.country'),'');
let prevented=false;events.submit({target:{matches:()=>true},preventDefault(){prevented=true}});assert(prevented,'Search Enter must not reload the application');
const untrusted={...D,patents:{...P,cases:[{...P.cases[0],date:'<img src=x>',url:'javascript:alert(1)',resources:[]}]}};
const safePatent=PR.render(untrusted,{}, {},'dossiers');assert(!safePatent.includes('<img'));assert(!safePatent.includes('href="javascript:'));
console.log(`PASS: existing Observatory views and tools; five patent tabs, 311 catalogue rows, 28 claim dossiers, 12 Newton records, ten gates, filters/pagination, source corrections, note escaping, compatible backups and mocked research refresh.`);
