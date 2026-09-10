// Actual recorded payload and script-order integration; not a browser layout audit.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const root=new URL('../',import.meta.url),base=new URL('dist/',root),records=new URL('research/round13/',root);
const nodes=new Map(),events={},checks=[];
function node(id){if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',open:false,value:'',focus(){},showModal(){this.open=true},close(){this.open=false},querySelector(){return node('close')},addEventListener(){}});return nodes.get(id);}
const ctx={console,URL,Blob,setTimeout:()=>0,location:{hash:'#research'},localStorage:{getItem(){return null},setItem(){}},document:{querySelector:node,getElementById:id=>node('#'+id),addEventListener:(e,f)=>(events[e]??=[]).push(f)},addEventListener(){}};
ctx.window=ctx;vm.createContext(ctx);
const html=fs.readFileSync(new URL('index.html',base),'utf8');
const files=[...html.matchAll(/<script src="(research[^"]*\.js)"/g)].map(m=>m[1]);
for(const file of files.filter(name=>!name.startsWith('research-shared')&&!name.startsWith('research-team')&&!name.startsWith('research-cycles')))vm.runInContext(fs.readFileSync(new URL(file,base),'utf8'),ctx,{filename:file});
const D=ctx.OBSERVATORY_EXCEPTIONS,T=ctx.ResearchObservatory;
const read=name=>JSON.parse(fs.readFileSync(new URL(name,records),'utf8'));
const text=name=>fs.readFileSync(new URL(name,records),'utf8');
const plain=value=>JSON.parse(JSON.stringify(value));
function check(name,fn){fn();checks.push({name,passed:true});}
function csv(name){const lines=fs.readFileSync(new URL(name,base),'utf8').trimEnd().split(/\r?\n/);const heads=lines.shift().split(',');return lines.map(line=>Object.fromEntries(line.split(',').map((s,i)=>[heads[i],s])));}
function logInteger(s){const t=String(s);return Math.log10(Number(t.slice(0,15)))+t.length-Math.min(15,t.length);}
function logRational(s){const [a,b='1']=s.split('/');return logInteger(a)-logInteger(b);}
function near(a,b,tol=1e-12){assert(Number.isFinite(a)&&Number.isFinite(b));assert(Math.abs(a-b)<=tol,`${a} versus ${b}`);}
const routes=['home','exceptions','local-dynamics','strong-coupling','moment-bounds','full-hierarchy','scalar-response','exception-roadmap','exception-review'];

check('Nine current pages, links and titles resolve through actual script order',()=>{
 assert(files.indexOf('research-exceptions.js')>files.indexOf('research-bridges.js'));
 for(const route of routes){ctx.location.hash='#research/'+route;const h=T.render(route);assert.equal((h.match(/<h1>/g)||[]).length,1,route);assert(h.includes('aria-current="page"'));T.afterRender();assert(ctx.document.title.includes('Yang–Mills'));
  for(const match of h.matchAll(/href="#research\/([^"]+)"/g))assert(!T.render(match[1]).includes('Research page not found'),match[1]);}
});
check('Historical evidence and unknown/prototype routes retain correct delegation',()=>{
 assert(T.render('review12-home').includes('Historical round 12'));
 assert(T.render('exact-evolution').includes('27/80000'));
 for(const route of ['variables','two-model','plaquette','volume-bridge'])assert(!T.render(route).includes('Research page not found'));
 for(const route of ['constructor','__proto__','missing-page'])assert(T.render(route).includes('Research page not found'));
});
check('Published documents are the actual reviewed source text',()=>{
 for(const [key,path] of Object.entries({advisor:'advisor/advisor.md',stability:'advisor/weak-coupling-stability.md',moments:'moments/README.md',locality:'locality/locality.md',response:'response/response.md',skeptic:'skeptic/REVIEW.md',readme:'README.md',experiments:'next-experiments.md'}))assert.equal(D.documents[key],text(path));
 assert.deepEqual(JSON.parse(D.documents.proof),read('proof_results.json'));
 const acceptance=read('skeptic/acceptance.json');for(const [path,sha] of Object.entries(acceptance.reviewed_source_hashes))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(new URL(path,records))).digest('hex'),sha,path);
});
check('Every new document opens via the shared escaped dialog handler',()=>{
 for(const route of routes)for(const m of T.render(route).matchAll(/data-r-doc="([^"]+)"/g))assert(ctx.OBSERVATORY_RESEARCH.documents[m[1]]?.length>50,m[1]);
 const button={dataset:{rDoc:'round13/stability'},hasAttribute:()=>false};
 const fire=()=>{for(const f of events.click||[])f({target:{closest:s=>s.includes('[data-r-doc]')?button:null}});};fire();assert(node('#research-dialog').open);assert(node('#research-body').innerHTML.includes('Yarotsky'));
 const saved=ctx.OBSERVATORY_RESEARCH.documents['round13/stability'];ctx.OBSERVATORY_RESEARCH.documents['round13/stability']='<script>injection</script>';fire();assert(!node('#research-body').innerHTML.includes('<script>'));assert(node('#research-body').innerHTML.includes('&lt;script&gt;'));ctx.OBSERVATORY_RESEARCH.documents['round13/stability']=saved;
});
check('All current downloads exist and exact certificate bytes match the reviewed source',()=>{
 for(const route of routes)for(const m of T.render(route).matchAll(/href="\/([^"?]+)" download/g))assert(fs.existsSync(new URL(m[1],base)),m[1]);
 assert.equal(fs.readFileSync(new URL('research-round13-certificates.json',base),'utf8'),text('moments/output/certificates.json'));
 assert.equal(read('moments/output/certificates.json').certificates.length,28);
});
check('Moment graph binds to recorded exact widths and omits the zero-width logarithm',()=>{
 const data=csv('exception-moments.csv');assert.equal(data.length,28);
 for(const [i,k] of ['1','5','20'].entries()){const expected=data.filter(r=>r.kappa===k).map(r=>[Number(r.level),Number(r.log10_mean_width)]);assert.deepEqual(plain(D.plots.moment_width.series[i].points),expected);}
 const zero=data.find(r=>r.kappa==='0');assert.equal(zero.mean_width,'0');assert.equal(zero.log10_mean_width,'');
 for(const r of data.filter(r=>r.mean_width!=='0'))near(Number(r.log10_mean_width),logRational(r.mean_width));
 assert(D.metrics.moment_width_k1_r6.includes('1.40631e-13'));
});
check('Locality graph displays bounds with actual chain radius and no simulation claim',()=>{
 const data=csv('exception-locality.csv'),points=D.plots.locality_radius.series[0].points;assert.equal(data.length,points.length);
 data.forEach((r,i)=>{assert.equal(points[i][0],Number(r.radius));near(points[i][1],logRational(r.bound_rational));});
 assert.equal(data.at(-1).radius,'48');assert.equal(data.at(-1).z,'8');assert(D.plots.locality_radius.caption.includes('not measured'));
 assert(T.render('local-dynamics').includes('identical electric terms'));assert(T.render('local-dynamics').includes('not an observed error'));
});
check('Scalar mean and variance plots retain every signed and zero-coupling datum',()=>{
 const data=csv('exception-response.csv');
 for(const [i,key] of ['mean_ode_reflected','mean_quad','mean_zero_variance_root','mean_wrong_coefficient_reflected'].entries())assert.deepEqual(plain(D.plots.scalar_mean.series[i].points),data.map(r=>[Number(r.kappa),Number(r[key])]));
 assert.deepEqual(plain(D.plots.scalar_variance.series[0].points),data.map(r=>[Number(r.kappa),Number(r.susceptibility_quad)]));
 const zero=data.find(r=>Number(r.kappa)===0);assert.equal(Number(zero.mean_ode_reflected),0);assert.equal(Number(zero.mean_bessel),0);near(Number(zero.mean_quad),0,1e-14);near(Number(zero.susceptibility_quad),.25,1e-14);assert(data.some(r=>Number(r.kappa)<0));
});
check('Scalar and gap pages retain the acceptance boundaries',()=>{
 const scalar=T.render('scalar-response'),gap=T.render('strong-coupling');assert(scalar.includes('not time'));assert(scalar.includes('singular at zero'));assert(scalar.includes('not an additional physical mass'));
 assert(gap.includes('existential'));assert(gap.includes('3α/8'));assert(gap.includes('4/g_H'));assert(gap.includes('No simulation at a specified positive coupling'));assert(T.render('home').includes('four-dimensional target remains open'));
});
check('Malformed plot input is visible and never silently treated as an empty success',()=>{
 const old=D.plots.moment_width;for(const series of [null,[],[null],[{points:[]}],[{points:[[0,NaN]]}],[{points:[[Infinity,1]]}],[{points:[[1,2,3]]}]]){D.plots.moment_width={series};assert(ctx.ResearchExceptions.plot('moment_width').includes('No valid recorded data'));}D.plots.moment_width=old;
});
check('Case, review and source text escape markup and unsafe source URLs',()=>{
 for(const [list,field,route] of [[D.cases,'title','exceptions'],[D.roadmap,'title','exception-roadmap'],[D.reviews,'name','exception-review'],[D.sources,'title','exception-review']]){const old=list[0][field];list[0][field]='<img src=x onerror=alert(1)>';assert(!T.render(route).includes('<img'));list[0][field]=old;}
 const old=D.sources[0].url;D.sources[0].url='javascript:alert(1)';assert(!T.render('exception-review').includes('href="javascript:'));D.sources[0].url=old;
});
check('All 24 search outcomes and costs match the actual replay',()=>{
 const proof=read('proof_results.json');assert.equal(D.routes.length,24);for(const route of D.routes){const source=proof.routes[route.name].result;assert.equal(route.status,source.status);assert.equal(route.cost,source.certified_cost??null);}
 assert.equal(D.routes.filter(r=>r.status==='proved').length,11);
 for(const name of ['stability_without_smallness','canonical_gap_without_smallness','finite_constraints_not_all_orders','finite_optimizer_slack_not_asymptotic','four_dimensional_mass_gap'])assert.equal(proof.routes[name].result.status,'not_derivable');
});
check('Current roadmap reflects completed science and keeps next obligations distinct',()=>{
 assert.deepEqual(plain(D.roadmap),read('current_roadmap.json').items);assert.equal(D.cases.length,16);
 assert(D.roadmap.find(r=>r.id==='R13-Y').status.includes('accepted'));assert.equal(D.roadmap.find(r=>r.id==='NEXT-CONTINUUM').status,'open');
 assert(T.render('exception-roadmap').includes('continuous residual'));assert(D.documents.experiments.includes('existential'));
});
check('Theory inventory retains every source node and its declared status',()=>{
 assert.equal(D.nodes.length,46);assert.deepEqual(plain(D.nodes),read('advisor/theorem_inventory.json').claims);
 const inventory=JSON.parse(D.documents.inventory);assert.deepEqual(inventory.reviewed_implications,read('advisor/inference_rules.json'));
 const h=T.render('exception-roadmap');for(const n of D.nodes)assert(h.includes(ctx.ResearchHub.escape(n.id)),n.id);
 assert(h.includes('not a certificate'));
});
check('Review counts are source-bound and execution modes are not double counted',()=>{
 const a=read('skeptic/acceptance.json');assert.equal(a.independent_gate_count,532);assert.equal(a.reports.reduce((s,r)=>s+r.count,0),532);
 for(const r of a.reports)assert(D.reviews.some(v=>v.name===r.name&&v.status.startsWith(String(r.count))));
 assert(fs.statSync(new URL('research-exceptions-data.js',base)).size<2000000);
});
const result={status:'passed',count:checks.length,checks,scope:'Node VM actual-script routes, dialog events, data/certificate bindings and malformed-input controls. No real-browser layout or keyboard audit.'};
fs.writeFileSync(new URL('site-validation.json',records),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
