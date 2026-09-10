import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const base=new URL('../dist/',import.meta.url),records=new URL('../research/round15/',import.meta.url);
const nodes=new Map(),events={},checks=[];
const node=id=>{if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',open:false,style:{},value:'',dataset:{},addEventListener(){},querySelector(){return {focus(){}}},focus(){},showModal(){this.open=true},close(){this.open=false},setAttribute(){},classList:{toggle(){}}});return nodes.get(id)};
const ctx={console,URL,Blob,setTimeout:()=>0,clearTimeout(){},location:{hash:'#research'},localStorage:{getItem(){return null},setItem(){}},document:{querySelector:node,getElementById:id=>node('#'+id),addEventListener:(e,f)=>(events[e]??=[]).push(f)},addEventListener(){}};
ctx.window=ctx;vm.createContext(ctx);
const files=[...fs.readFileSync(new URL('index.html',base),'utf8').matchAll(/<script src="(research[^\"]*\.js)"/g)].map(m=>m[1]);
for(const file of files)vm.runInContext(fs.readFileSync(new URL(file,base),'utf8'),ctx,{filename:file});
const D=ctx.OBSERVATORY_CYCLES,T=ctx.ResearchObservatory;
const read=p=>JSON.parse(fs.readFileSync(new URL(p,records),'utf8'));
const plain=v=>JSON.parse(JSON.stringify(v));
const routes=['home','cycle-map','range-cover','cube-graph','cube-certificate','spectral-audit','cycle-roadmap','cycle-review'];
function check(name,fn){fn();checks.push({name,passed:true});}
function csv(name){const lines=fs.readFileSync(new URL(name,base),'utf8').trimEnd().split(/\r?\n/);const h=lines.shift().split(',');return lines.map(l=>Object.fromEntries(l.split(',').map((x,i)=>[h[i],x])));}
function rational(s){const [a,b='1']=s.split('/');return [BigInt(a),BigInt(b)];}
function number(s){const [a,b='1']=s.split('/');return Number(a)/Number(b);}
function decimal(s){const [a,b='']=s.split('.');return [BigInt(a+b),10n**BigInt(b.length)];}
function less(a,b){return a[0]*b[1]<=b[0]*a[1];}
function nearPoints(a,b){assert.equal(a.length,b.length);for(let i=0;i<a.length;i++)for(let j=0;j<2;j++){assert(Number.isFinite(a[i][j])&&Number.isFinite(b[i][j]));assert(Math.abs(a[i][j]-b[i][j])<=4*Number.EPSILON*Math.max(Math.abs(a[i][j]),Math.abs(b[i][j]),Number.MIN_VALUE),`plot rounding mismatch at${i},${j}`);}}
check('Eight new pages and historical routes resolve in actual script order',()=>{
 assert(files.indexOf('research-cycles.js')>files.indexOf('research-team.js'));
 for(const r of routes){ctx.location.hash='#research/'+r;const h=T.render(r);assert.equal((h.match(/<h1>/g)||[]).length,1);assert(h.includes('aria-current="page"'));T.afterRender();assert(ctx.document.title.includes('Yang–Mills'));
  for(const m of h.matchAll(/href="#research\/([^\"]+)"/g))assert(!T.render(m[1]).includes('Research page not found'),m[1]);}
 assert(T.render('review14-home').includes('Historical round14'));
 for(const r of ['constructor','__proto__','missing'])assert(T.render(r).includes('Research page not found'));
});
check('Planning review and six loops retain exactly three roles and original goals',()=>{
 assert.equal(D.team_size,3);assert.equal(D.planning_loops,1);assert.equal(D.research_loops,6);assert.equal(D.loops_per_goal,2);
 assert.deepEqual(plain(D.loops.map(r=>r.id)),['A1','A2','B1','B2','C1','C2']);assert.equal(D.goals.length,3);
 assert(D.goals.find(r=>r.id==='C').status.includes('Original goal open'));assert(D.feedback.some(r=>r.transition==='C1 → C2'));
 const n=new Map(D.network.nodes.map(r=>[r.id,r]));for(const edge of D.network.edges){assert(n.has(edge.from));assert(n.has(edge.to));}
 assert(D.network.edges.some(r=>r.from==='B1'&&r.to==='C2'));for(const r of D.network.nodes)assert(T.render('cycle-map').includes(ctx.ResearchHub.escape(r.label)));
});
check('Every accepted loop binds complete actual source bytes',()=>{
 const gates=JSON.parse(D.documents.gates);assert.deepEqual(Object.keys(gates),['A1','A2','B1','B2','C1','C2']);
 for(const [phase,g] of Object.entries(gates)){assert.deepEqual(g,read('advisor/loop-gates/'+phase+'.json'));assert(g.status.startsWith('accepted'));assert(Object.keys(g.source_sha256).length>5);
  for(const [p,h] of Object.entries(g.source_sha256))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(new URL(p,records))).digest('hex'),h,p);}
});
check('Published exact certificates match accepted evidence byte for byte',()=>{
 for(const [original,asset] of [['forward/A2/output/final_cover.json','research-round15-cover.json'],['forward/B2/output/certificates.json','research-round15-cube.json']])assert.deepEqual(fs.readFileSync(new URL(original,records)),fs.readFileSync(new URL(asset,base)));
 const a=read('forward/A2/output/final_cover.json');assert.equal(a.cell_count,21);assert.deepEqual(a.target,['1/8','1/4']);assert.equal(a.status,'certified-positive-cover');assert(rational(a.minimum_lower)[0]>0n);
 assert.deepEqual(read('forward/A2/output/refinement.json').levels.map(r=>r.cell_count),[8,16,21]);
});
check('Outward displayed cube decimals contain the exact rational enclosure',()=>{
 const b=read('forward/B2/output/certificates.json').certificates.at(-1),bounds=D.metrics.B_equation.match(/\d+\.\d+/g);assert.equal(bounds.length,2);
 assert(less(decimal(bounds[0]),rational(b.enclosures.expectation[0])));assert(less(rational(b.enclosures.expectation[1]),decimal(bounds[1])));
 assert(less(rational(b.expectation_width),[1n,10n**12n]));assert(rational(b.enclosures.partition_excess[0])[0]>0n);
});
check('A plots preserve rational point versus complete-cell endpoints',()=>{
 for(const [key,name] of [['A_coarse','cycles-a-coarse.csv'],['A_refined','cycles-a-refined.csv']]){
  const rows=csv(name);for(const [i,field] of ['point_lower','transported_lower'].entries())nearPoints(plain(D.plots[key].series[i].points),rows.map(r=>[number(r.center),number(r[field])]));
  assert(rows.every(r=>number(r.left)<number(r.center)&&number(r.center)<number(r.right)));
 }
 assert(csv('cycles-a-coarse.csv').every(r=>number(r.point_lower)>0&&number(r.transported_lower)<0));assert(csv('cycles-a-refined.csv').every(r=>number(r.transported_lower)>0));
});
check('B degree-refinement graph keeps all failed precision targets',()=>{
 const rows=csv('cycles-b-refinement.csv');assert.deepEqual(plain(D.plots.B_refinement.series[0].points),rows.map(r=>[Number(r.degree),Number(r.log10_width)]));
 const certs=read('forward/B2/output/certificates.json').certificates;
 for(const [i,r] of rows.entries()){assert.equal(r.width_exact,certs[i].expectation_width);assert.equal(r.status,certs[i].expectation_status);}
 assert(rows.slice(0,3).every(r=>r.status==='insufficient-width'));assert(rows.slice(3).every(r=>r.status==='target-certified'));
});
check('C charts show sufficient bounds and volume deterioration, not actual eigenvalues',()=>{
 const rows=csv('cycles-c-coupling.csv');for(const [i,key] of ['c1_lower','c2_lower'].entries())nearPoints(plain(D.plots.C_coupling.series[i].points),rows.map(r=>[number(r.ratio),number(r[key])]));
 assert.equal(rows.find(r=>r.ratio==='1/2').c1_lower,'0');assert(number(rows.find(r=>r.ratio==='1/2').c2_lower)>0);
 assert.equal(rows.find(r=>r.ratio==='12/23').c2_lower,'0');assert(D.plots.C_coupling.caption.includes('not computed eigenvalues'));
 assert(T.render('spectral-audit').includes('its upper endpoint is not an upper bound on the physical gap'));
 const vol=csv('cycles-c-volume.csv');nearPoints(plain(D.plots.C_volume.series[0].points),vol.map(r=>[Number(r.plaquettes),number(r.positive_threshold_lambda_over_alpha)]));assert(D.plots.C_volume.caption.includes('only been proved for the single cube'));
});
check('All document dialogs contain actual evidence and escape text',()=>{
 for(const r of routes)for(const m of T.render(r).matchAll(/data-r-doc="([^\"]+)"/g))assert(ctx.OBSERVATORY_RESEARCH.documents[m[1]]?.length>50,m[1]);
 const button={dataset:{rDoc:'round15/A2'},hasAttribute:()=>false};const fire=()=>{for(const f of events.click||[])f({target:{closest:s=>s.includes('[data-r-doc]')?button:null}});};fire();assert(node('#research-dialog').open);
 const old=ctx.OBSERVATORY_RESEARCH.documents['round15/A2'];ctx.OBSERVATORY_RESEARCH.documents['round15/A2']='<script>injected</script>';fire();assert(node('#research-body').innerHTML.includes('&lt;script&gt;'));assert(!node('#research-body').innerHTML.includes('<script>'));ctx.OBSERVATORY_RESEARCH.documents['round15/A2']=old;
});
check('New downloads and recorded figure files exist',()=>{for(const r of routes)for(const m of T.render(r).matchAll(/href="\/([^\"]+)" download/g))assert(fs.existsSync(new URL(m[1],base)),m[1]);for(const key of Object.keys(D.plots))assert(fs.existsSync(new URL('figures/'+key+'.png',records)));});
check('Actual proof routes and saved roadmap match displayed statuses',()=>{
 const p=read('proof_results.json');assert.equal(D.routes.length,Object.keys(p.routes).length);for(const r of D.routes){const s=p.routes[r.name].result;assert.equal(r.status,s.status);assert.equal(r.steps,s.certified_cost??null);if(r.status==='proved'){assert(s.first_meeting_candidate.passed);assert(s.independent_ordered_replay.passed);}}
 assert.equal(D.routes.filter(r=>r.status==='proved').length,3);assert.equal(p.routes.original_uniform_goal.result.status,'not_derivable');assert.equal(p.routes.four_dimensional_yang_mills.result.status,'not_derivable');
 assert.deepEqual(plain(D.goals),read('current_roadmap.json').goals);assert.deepEqual(plain(D.next),read('current_roadmap.json').next);
});
check('Malformed data yields unavailable states and dynamic strings are escaped',()=>{
 const old=D.plots.B_refinement;for(const series of [null,[],[null],[{points:[[0,NaN]]}],[{points:[[Infinity,1]]}],[{points:[[1,2,3]]}]]){D.plots.B_refinement={series};assert(ctx.ResearchCycles.plot('B_refinement').includes('No valid recorded data'));}D.plots.B_refinement=old;
 const saved=D.network.nodes;D.network.nodes=[{id:'x',x:NaN,y:0}];assert(ctx.ResearchCycles.network().includes('unavailable'));D.network.nodes=saved;
 for(const [list,field,route] of [[D.network.nodes,'label','cycle-map'],[D.goals,'status','cycle-roadmap'],[D.reviews,'name','cycle-review']]){const prev=list[0][field];list[0][field]='<img src=x onerror=alert(1)>';assert(!T.render(route).includes('<img'));list[0][field]=prev;}
 const url=D.sources[0].url;D.sources[0].url='javascript:alert(1)';assert(!T.render('cycle-review').includes('href="javascript:'));D.sources[0].url=url;
});
check('Acceptance counts remain producer versus independent, and browser limits remain visible',()=>{
 assert.equal(D.reviews.filter(r=>r.name.endsWith(' producer')).length,6);assert.equal(D.reviews.filter(r=>r.name.endsWith(' independent reviewer')).length,6);
 assert(D.reviews.every(r=>!r.scope.includes('two independent optimized reviews')));assert(T.render('cycle-review').includes('keyboard interaction have not been audited'));
 assert(T.render('cycle-review').includes('missing')||D.failures.some(r=>r.finding.includes('deletion')));assert(fs.statSync(new URL('research-cycles-data.js',base)).size<2000000);
});
const report={status:'passed',count:checks.length,checks,scope:'Actual-script Node VM routes, modal documents, source/data bindings, exact decimal containment, recorded graphs and unavailable states. No real-browser visual or keyboard audit.'};
fs.writeFileSync(new URL('site-validation.json',records),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
