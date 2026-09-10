import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const base=new URL('../dist/',import.meta.url),records=new URL('../research/round17/',import.meta.url);
const nodes=new Map(),events={},checks=[];
const node=id=>{if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',open:false,style:{},value:'',dataset:{},addEventListener(){},querySelector(){return {focus(){}}},focus(){},showModal(){this.open=true},close(){this.open=false},setAttribute(){},classList:{toggle(){}}});return nodes.get(id)};
const ctx={console,URL,Blob,setTimeout:()=>0,clearTimeout(){},location:{hash:'#research'},localStorage:{getItem(){return null},setItem(){}},document:{querySelector:node,getElementById:id=>node('#'+id),addEventListener:(e,f)=>(events[e]??=[]).push(f)},addEventListener(){}};
ctx.window=ctx;vm.createContext(ctx);
const files=[...fs.readFileSync(new URL('index.html',base),'utf8').matchAll(/<script src="(research[^\"]*\.js)"/g)].map(m=>m[1]);
for(const file of files)vm.runInContext(fs.readFileSync(new URL(file,base),'utf8'),ctx,{filename:file});
const D=ctx.OBSERVATORY_SIX,T=ctx.ResearchObservatory,read=p=>JSON.parse(fs.readFileSync(new URL(p,records),'utf8')),plain=v=>JSON.parse(JSON.stringify(v));
const routes=['home','six-local','six-sparse','six-trial','six-adjoint','six-graph','six-kernel','six-team','six-review'];
function check(name,fn){fn();checks.push({name,passed:true});}
check('Nine actual-script pages and all linked research routes render',()=>{
 assert(files.indexOf('research-six.js')>files.indexOf('research-shared.js'));
 for(const r of routes){ctx.location.hash='#research/'+r;const h=T.render(r);assert.equal((h.match(/<h1>/g)||[]).length,1);assert(h.includes('aria-current="page"'));T.afterRender();assert(ctx.document.title.includes('Yang–Mills'));
 for(const m of h.matchAll(/href="#research\/([^\"]+)"/g))assert(!T.render(m[1]).includes('Research page not found'),m[1]);}
 assert(T.render('review16-home').includes('Historical Round16'));
 for(const r of ['__proto__','constructor','no-such-route'])assert(T.render(r).includes('Research page not found'));
});
check('All six gates and their preceding decision inventories match bytes',()=>{
 assert.deepEqual(plain(D.solutions.map(s=>s.id)),['A1','A2','B1','B2','C1','C2']);assert.equal(D.gates.length,6);
 for(const g of D.gates){assert.equal(g.status,'accepted');assert.deepEqual(plain(g),read('advisor/'+g.loop+'-gate.json'));
 for(const [p,sha] of Object.entries(g.files))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(new URL(p,records))).digest('hex'),sha,p);}
});
check('Completed counts require complete accepted evidence',()=>{
 assert.equal(D.loops_completed,6);assert.equal(D.scientific_roles,3);assert.equal(D.advisory_decisions,2);assert.equal(D.stages.length,8);
 const status=D.status;D.status='pending';assert(T.render('home').includes('evidence unavailable'));assert(!T.render('six-adjoint').includes('1388'));D.status=status;
 const gates=D.gates;D.gates=gates.slice(0,5);assert(T.render('home').includes('evidence unavailable'));D.gates=gates;
});
check('All registered document buttons open escaped original dialogs',()=>{
 for(const r of routes)for(const m of T.render(r).matchAll(/data-r-doc="([^\"]+)"/g))assert(ctx.OBSERVATORY_RESEARCH.documents[m[1]]?.length>40,m[1]);
 const button={dataset:{rDoc:'round17/c2-contract'},hasAttribute:()=>false};
 const fire=()=>{for(const fn of events.click??[])fn({target:{closest:s=>s.includes('[data-r-doc]')?button:null},preventDefault(){}});};
 fire();assert(node('#research-dialog').open);assert(node('#research-body').innerHTML.includes('equal action variable'));
 const original=ctx.OBSERVATORY_RESEARCH.documents[button.dataset.rDoc];ctx.OBSERVATORY_RESEARCH.documents[button.dataset.rDoc]='<script>injected</script>';fire();assert(node('#research-body').innerHTML.includes('&lt;script&gt;'));assert(!node('#research-body').innerHTML.includes('<script>'));ctx.OBSERVATORY_RESEARCH.documents[button.dataset.rDoc]=original;
});
check('Every plot has finite saved data and a byte-bound CSV',()=>{
 assert(Object.keys(D.plots).length>=6);
 for(const [key,p] of Object.entries(D.plots)){
  assert(p.series.length);assert(p.series.every(s=>s.points.length&&s.points.every(q=>q.length===2&&q.every(Number.isFinite))));
  assert(ctx.ResearchSix.plot(key).includes('<svg'));const name=p.csv.slice(1);assert.equal(crypto.createHash('sha256').update(fs.readFileSync(new URL(name,base))).digest('hex'),D.csv_sha256[name]);assert(fs.existsSync(new URL('figures/'+key+'.png',records)));
 }
 assert.deepEqual(plain(D.plots),read('site-data.json').plots);assert.equal(read('data-checks.json').status,'passed');
});
check('Displayed finite-action interval rounds outward from exact accepted fractions',()=>{
 const interval=read('forward/c2/output/collection.json').refinements.at(-1).contrast.interval;
 const match=D.solutions.find(s=>s.id==='C2').equation.match(/D∈\[([0-9.]+), ([0-9.]+)\]/);assert(match);
 const q=s=>{const [a,b='1']=s.split('/');return [BigInt(a),BigInt(b)]};
 const decimal=s=>{const [a,b='']=s.split('.');return [BigInt(a+b),10n**BigInt(b.length)]};
 const le=(a,b)=>a[0]*b[1]<=b[0]*a[1];
 assert(le(decimal(match[1]),q(interval[0])));assert(le(q(interval[1]),decimal(match[2])));assert(decimal(match[1])[0]>0n);
});
check('Missing and malformed plots cannot show recorded success',()=>{
 const original=D.plots['finite-coupling'];
 for(const series of [null,[],[null],[{points:[[0,NaN]]}],[{points:[[Infinity,1]]}],[{points:[[1,2,3]]}]]){D.plots['finite-coupling']={series};assert(ctx.ResearchSix.plot('finite-coupling').includes('unavailable'));}
 D.plots['finite-coupling']=original;assert(ctx.ResearchSix.plot('unknown').includes('unavailable'));
});
check('Unsafe data are escaped in solution, feedback and roadmap content',()=>{
 for(const [array,key,route] of [[D.solutions,'plain','home'],[D.feedback,'finding','six-review'],[D.next,'goal','six-team']]){const saved=array[0][key];array[0][key]='<img src=x onerror=alert(1)>';assert(!T.render(route).includes('<img src=x'));assert(T.render(route).includes('&lt;img'));array[0][key]=saved;}
 const p=D.plots['finite-coupling'],saved=p.csv;p.csv='javascript:alert(1)';assert(!ctx.ResearchSix.plot('finite-coupling').includes('href="javascript:'));p.csv=saved;
});
check('Actual proof routes include separate meetings and ordered replay',()=>{
 const proof=read('proof_results.json');assert.equal(D.routes.length,18);assert.equal(D.routes.filter(r=>r.status==='proved').length,6);
 for(const r of D.routes){const s=proof.routes[r.target].result;assert.equal(r.status,s.status);assert.equal(r.steps,s.certified_cost??null);if(r.status==='proved'){assert(s.first_meeting_candidate.passed);assert(s.independent_ordered_replay.passed);}}
 for(const key of ['missing_scale','missing_endpoint','overlapping_support','original_dense_uniform_goal','full_bulk_integral','four_dimensional_yang_mills'])assert.equal(proof.routes[key].result.status,'not_derivable');
});
check('Scientific limits and actual added variables are visible',()=>{
 assert(T.render('six-adjoint').includes('1388/284767457'));assert(T.render('six-adjoint').includes('not a new field'));
 assert(T.render('six-sparse').includes('Shared vertices'));assert(T.render('six-graph').includes('−1/405'));assert(T.render('six-kernel').includes('normalization'));assert(T.render('home').includes('continuum'));
 assert(T.render('six-review').includes('Real-browser visual layout and keyboard testing remain unverified'));
});
check('All local downloads and figure references exist',()=>{
 for(const r of routes){const h=T.render(r);for(const m of h.matchAll(/href="\/([^\"]+)" download/g))assert(fs.existsSync(new URL(m[1],base)),m[1]);for(const m of h.matchAll(/<img src="\/([^\"]+)"/g))assert(fs.existsSync(new URL(m[1],base)),m[1]);}
});
const report={status:'passed',count:checks.length,checks,scope:'Actual-script VM routing, document behavior, data/source bindings, scope and unavailable-state checks. No real-browser visual or keyboard audit.'};
fs.writeFileSync(new URL('site-validation.json',records),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
