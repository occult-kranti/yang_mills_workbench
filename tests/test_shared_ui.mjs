import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const base=new URL('../dist/',import.meta.url),records=new URL('../research/round16/',import.meta.url);
const nodes=new Map(),events={},checks=[];
const node=id=>{if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',open:false,style:{},value:'',dataset:{},addEventListener(){},querySelector(){return {focus(){}}},focus(){},showModal(){this.open=true},close(){this.open=false},setAttribute(){},classList:{toggle(){}}});return nodes.get(id)};
const ctx={console,URL,Blob,setTimeout:()=>0,clearTimeout(){},location:{hash:'#research'},localStorage:{getItem(){return null},setItem(){}},document:{querySelector:node,getElementById:id=>node('#'+id),addEventListener:(e,f)=>(events[e]??=[]).push(f)},addEventListener(){}};
ctx.window=ctx;vm.createContext(ctx);
const files=[...fs.readFileSync(new URL('index.html',base),'utf8').matchAll(/<script src="(research[^\"]*\.js)"/g)].map(m=>m[1]);
for(const file of files)vm.runInContext(fs.readFileSync(new URL(file,base),'utf8'),ctx,{filename:file});
const D=ctx.OBSERVATORY_SHARED,T=ctx.ResearchObservatory,read=p=>JSON.parse(fs.readFileSync(new URL(p,records),'utf8')),plain=v=>JSON.parse(JSON.stringify(v));
const routes=['home','shared-graph','shared-haar','shared-integral','physical-scale','shared-team','shared-roadmap','shared-review'];
function check(name,fn){fn();checks.push({name,passed:true});}
check('Eight new pages, historical routes and actual script order',()=>{
 assert(files.indexOf('research-shared.js')>files.indexOf('research-cycles.js'));
 for(const r of routes){ctx.location.hash='#research/'+r;const h=T.render(r);assert.equal((h.match(/<h1>/g)||[]).length,1);assert(h.includes('aria-current="page"'));T.afterRender();assert(ctx.document.title.includes('Yang–Mills'));
  for(const m of h.matchAll(/href="#research\/([^\"]+)"/g))assert(!T.render(m[1]).includes('Research page not found'),m[1]);}
 assert(T.render('review15-home').includes('Historical round15'));
 for(const r of ['__proto__','constructor','no-such-route'])assert(T.render(r).includes('Research page not found'));
});
check('Both source-bound decisions match actual evidence',()=>{
 assert.equal(D.gates.length,2);
 for(const g of D.gates){assert.equal(g.status,'accepted');const saved=read('advisor/'+g.loop+'-gate.json');assert.deepEqual(plain(g),saved);
 for(const [p,sha] of Object.entries(saved.files))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(new URL(p,records))).digest('hex'),sha,p);}
});
check('Certificates and graph downloads preserve accepted bytes',()=>{
 for(const [web,local] of [['research-round16-certificates.json','forward/loop2/output/collection.json'],['research-round16-graph.json','forward/loop1/graph.json']])assert(fs.readFileSync(new URL(web,base)).equals(fs.readFileSync(new URL(local,records))),web);
});
check('Displayed outward decimals enclose the exact primary difference',()=>{
 const primary=read('forward/loop2/output/collection.json').refinement.at(-1);
 const range=D.metrics.integralEquation.match(/D∈\[([0-9.]+), ([0-9.]+)\]/);assert(range);
 const q=s=>{const [a,b='1']=s.split('/');return [BigInt(a),BigInt(b)]};
 const dec=s=>{const [a,b='']=s.split('.');return [BigInt(a+b),10n**BigInt(b.length)]};
 const le=(a,b)=>a[0]*b[1]<=b[0]*a[1];
 assert(le(dec(range[1]),q(primary.difference_interval[0])));assert(le(q(primary.difference_interval[1]),dec(range[2])));
 assert(dec(range[1])[0]>0n);assert.equal(primary.status,'target-met');
});
check('All original document dialogs are registered and handled',()=>{
 for(const r of routes)for(const m of T.render(r).matchAll(/data-r-doc="([^\"]+)"/g))assert(ctx.OBSERVATORY_RESEARCH.documents[m[1]]?.length>40,m[1]);
 const button={dataset:{rDoc:'round16/contract'},hasAttribute:()=>false};
 const fire=()=>{for(const fn of events.click??[])fn({target:{closest:s=>s.includes('[data-r-doc]')?button:null},preventDefault(){}});};
 fire();assert(node('#research-dialog').open);assert(node('#research-body').innerHTML.includes('Round16 contract'));
 const previous=ctx.OBSERVATORY_RESEARCH.documents['round16/contract'];ctx.OBSERVATORY_RESEARCH.documents['round16/contract']='<script>injected</script>';fire();
 assert(node('#research-body').innerHTML.includes('&lt;script&gt;'));assert(!node('#research-body').innerHTML.includes('<script>'));ctx.OBSERVATORY_RESEARCH.documents['round16/contract']=previous;
});
check('Every recorded plot has finite data and a byte-bound CSV',()=>{
 assert.equal(Object.keys(D.plots).length,4);
 for(const [key,p] of Object.entries(D.plots)){
  assert(p.series.length>0);assert(p.series.every(s=>s.points.length&&s.points.every(q=>q.length===2&&q.every(Number.isFinite))));
  assert(ctx.ResearchShared.plot(key).includes('<svg'));const name=p.csv.slice(1);const bytes=fs.readFileSync(new URL(name,base));assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),D.csv_sha256[name]);
  assert(fs.existsSync(new URL('figures/'+key+'.png',records)));
 }
 assert(fs.existsSync(new URL('shared-two-cubes.svg',base)));
});
check('Plot data reproduce saved exact endpoint conversions',()=>{
 const expected=read('site-data.json');assert.deepEqual(plain(D.plots),expected.plots);
 const report=read('data-checks.json');assert.equal(report.status,'passed');assert.equal(report.plot_series_checked,8);
});
check('Proof route display matches actual two-front results',()=>{
 const p=read('proof_results.json');assert.equal(D.routes.length,Object.keys(p.routes).length);
 for(const r of D.routes){const s=p.routes[r.name].result;assert.equal(r.status,s.status);assert.equal(r.steps,s.certified_cost??null);if(r.status==='proved'){assert(s.first_meeting_candidate.passed);assert(s.independent_ordered_replay.passed);}}
 assert.equal(p.routes.original_uniform_goal.result.status,'not_derivable');assert.equal(p.routes.four_dimensional_yang_mills.result.status,'not_derivable');
});
check('Malformed and unsafe data never produce a plotted success',()=>{
 const saved=D.plots.refinement;
 for(const series of [null,[],[null],[{points:[[0,NaN]]}],[{points:[[Infinity,1]]}],[{points:[[1,2,3]]}]]){D.plots.refinement={series};assert(ctx.ResearchShared.plot('refinement').includes('No valid recorded data'));}
 D.plots.refinement=saved;
 const n=D.network.nodes;D.network.nodes=[{id:'x',x:NaN,y:0}];assert(ctx.ResearchShared.network().includes('unavailable'));D.network.nodes=n;
 for(const [list,field,route] of [[D.network.nodes,'label','shared-team'],[D.reviews,'name','shared-review'],[D.next,'goal','shared-roadmap']]){const v=list[0][field];list[0][field]='<img src=x onerror=alert(1)>';assert(!T.render(route).includes('<img src=x'));list[0][field]=v;}
 const u=D.sources[0].url;D.sources[0].url='javascript:alert(1)';assert(!T.render('shared-review').includes('href="javascript:'));D.sources[0].url=u;
});
check('All downloads exist; finite scope and browser limits remain visible',()=>{
 for(const r of routes)for(const m of T.render(r).matchAll(/href="\/([^\"]+)" download/g))assert(fs.existsSync(new URL(m[1],base)),m[1]);
 assert(T.render('home').includes('volume-uniform physical stability threshold remains open'));
 assert(T.render('shared-review').includes('Real-browser visual layout and keyboard testing remain unverified'));
 assert(T.render('physical-scale').includes('not a universal classification'));
 assert.equal(D.loops_completed,2);assert.equal(D.scientific_roles,3);
});
const report={status:'passed',count:checks.length,checks,scope:'Actual-script VM routing, document behavior, downloads, source/data bindings and unavailable states. No real-browser visual or keyboard audit.'};
fs.writeFileSync(new URL('site-validation.json',records),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
