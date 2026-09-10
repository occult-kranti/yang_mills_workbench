import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const base=new URL('../dist/',import.meta.url),records=new URL('../research/round14/',import.meta.url);
const nodes=new Map(),events={},checks=[];
const node=id=>{if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',open:false,style:{},value:'',dataset:{},addEventListener(){},querySelector(){return {focus(){}}},focus(){},showModal(){this.open=true},close(){this.open=false},setAttribute(){},classList:{toggle(){}}});return nodes.get(id)};
const ctx={console,URL,Blob,setTimeout:()=>0,clearTimeout(){},location:{hash:'#research'},localStorage:{getItem(){return null},setItem(){}},document:{querySelector:node,getElementById:id=>node('#'+id),addEventListener:(e,f)=>(events[e]??=[]).push(f)},addEventListener(){}};
ctx.window=ctx;vm.createContext(ctx);
const files=[...fs.readFileSync(new URL('index.html',base),'utf8').matchAll(/<script src="(research[^"]*\.js)"/g)].map(m=>m[1]).filter(f=>!f.startsWith('research-next'));
for(const file of files.filter(name=>!name.startsWith('research-six')&&!name.startsWith('research-shared')&&!name.startsWith('research-cycles')))vm.runInContext(fs.readFileSync(new URL(file,base),'utf8'),ctx,{filename:file});
const D=ctx.OBSERVATORY_TEAM,T=ctx.ResearchObservatory;
const read=p=>JSON.parse(fs.readFileSync(new URL(p,records),'utf8'));
const plain=v=>JSON.parse(JSON.stringify(v));
const routes=['home','team-map','team-loop1','team-loop2','team-roadmap','team-review'];
function check(name,fn){fn();checks.push({name,passed:true});}
function csv(name){const lines=fs.readFileSync(new URL(name,base),'utf8').trimEnd().split(/\r?\n/);const h=lines.shift().split(',');return lines.map(l=>Object.fromEntries(l.split(',').map((x,i)=>[h[i],x])));}
function rational(s){const [a,b='1']=s.split('/');return [BigInt(a),BigInt(b)];}
function decimal(s){const [a,b='']=s.split('.');return [BigInt(a+b),10n**BigInt(b.length)];}
function less(a,b){return a[0]*b[1]<=b[0]*a[1];}
check('Six current pages resolve in actual script order; historical pages remain reachable',()=>{
 assert(files.indexOf('research-team.js')>files.indexOf('research-exceptions.js'));
 for(const r of routes){ctx.location.hash='#research/'+r;const h=T.render(r);assert.equal((h.match(/<h1>/g)||[]).length,1);assert(h.includes('aria-current="page"'));T.afterRender();assert(ctx.document.title.includes('Yang–Mills'));
  for(const m of h.matchAll(/href="#research\/([^"]+)"/g))assert(!T.render(m[1]).includes('Research page not found'),m[1]);}
 assert(T.render('review13-home').includes('Historical round 13'));assert(T.render('strong-coupling').includes('3α/8'));
 for(const r of ['constructor','__proto__','missing'])assert(T.render(r).includes('Research page not found'));
});
check('Collaboration graph is backed by exactly three roles and two completed gates',()=>{
 assert.equal(D.team_size,3);assert.equal(D.completed_loops,2);assert.equal(D.collaboration.nodes.length,8);
 const byid=new Map(D.collaboration.nodes.map(n=>[n.id,n]));for(const e of D.collaboration.edges){assert(byid.has(e.from));assert(byid.has(e.to));}
 assert(byid.get('gate1').status.includes('accepted'));assert(byid.get('gate2').status.includes('accepted'));assert(byid.get('next').status.includes('not executed'));
 const h=T.render('team-map');assert(h.includes('marker-end'));assert(h.includes('marker-start'));for(const n of D.collaboration.nodes)assert(h.includes(ctx.ResearchHub.escape(n.label)));
 assert(D.feedback.some(f=>f.decision.includes('bound7')));assert(D.feedback.some(f=>f.challenge.includes('Forged')));
});
check('Every exact gate source hash still matches the reviewed bytes',()=>{
 for(const name of ['advisor/loop1_gate.json','advisor/loop2_gate.json'])for(const [p,h] of Object.entries(read(name).source_sha256))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(new URL(p,records))).digest('hex'),h,p);
});
check('Outward displayed central decimals contain the actual rational certificate',()=>{
 const c=read('central-certificate.json'),bounds=D.metrics.central_equation.match(/\d+\.\d+/g);assert.equal(bounds.length,2);
 assert(less(decimal(bounds[0]),rational(c.enclosures.covariance[0])));assert(less(rational(c.enclosures.covariance[1]),decimal(bounds[1])));
 assert(rational(c.enclosures.covariance[0])[0]>0n);assert(less(rational(c.width),[1n,10n**12n]));assert.equal(c.degree,32);
});
check('All23 published certificate bytes match the independently reviewed collection',()=>{
 const p='forward/loop2_output/certificates.json',raw=fs.readFileSync(new URL(p,records));assert.equal(raw.toString(),fs.readFileSync(new URL('research-round14-certificates.json',base),'utf8'));
 assert.equal(read(p).certificates.length,23);assert.equal(crypto.createHash('sha256').update(raw).digest('hex'),read('backward/loop2_output/independent_certificate_review.json').collection_sha256);
});
check('Current dialogs contain original derivations and preserve escaping',()=>{
 for(const [key,p] of Object.entries({protocol:'advisor/two-loop-protocol.md',forward1:'forward/loop1.md',forward2:'forward/loop2.md',backward2:'backward/loop2.md',readme:'README.md',roadmap:'next-roadmap.md'}))assert.equal(D.documents[key],fs.readFileSync(new URL(p,records),'utf8'));
 for(const r of routes)for(const m of T.render(r).matchAll(/data-r-doc="([^"]+)"/g))assert(ctx.OBSERVATORY_RESEARCH.documents[m[1]]?.length>50);
 const button={dataset:{rDoc:'round14/forward2'},hasAttribute:()=>false};const fire=()=>{for(const f of events.click||[])f({target:{closest:s=>s.includes('[data-r-doc]')?button:null}});};fire();assert(node('#research-dialog').open);
 const old=ctx.OBSERVATORY_RESEARCH.documents['round14/forward2'];ctx.OBSERVATORY_RESEARCH.documents['round14/forward2']='<script>injected</script>';fire();assert(node('#research-body').innerHTML.includes('&lt;script&gt;'));assert(!node('#research-body').innerHTML.includes('<script>'));ctx.OBSERVATORY_RESEARCH.documents['round14/forward2']=old;
});
check('All new downloads resolve to saved assets',()=>{for(const r of routes)for(const m of T.render(r).matchAll(/href="\/([^"]+)" download/g))assert(fs.existsSync(new URL(m[1],base)),m[1]);});
check('Covariance graph preserves every recorded signed fixture and its legend',()=>{
 const data=csv('team-covariance.csv');for(const [i,key] of ['covariance_1_2','covariance_0_0','tangent_1_2','false_factorization'].entries())assert.deepEqual(plain(D.plots.covariance.series[i].points),data.map(r=>[Number(r.eta),Number(r[key])]));
 for(const s of D.plots.covariance.series)assert(s.name?.length);assert(T.render('team-loop1').includes('False factorization'));
});
check('Certificate refinement plots rational widths and retains failed degree4',()=>{
 const data=csv('team-certificate.csv');assert.deepEqual(plain(D.plots.certificate.series[0].points),data.map(r=>[Number(r.degree),Number(r.log10_width)]));
 const certs=read('forward/loop2_output/certificates.json').certificates;for(const r of data){const c=certs.find(c=>c.id==='central_N'+r.degree).certificate;assert.equal(r.width,c.width);assert.equal(r.status,c.status);}
 assert(data[0].status.includes('inconclusive'));assert.equal(data[0].degree,'4');assert.equal(data.at(-1).degree,'32');
});
check('Quadrature plot keeps strong-field coarse failures and numeric interpretation',()=>{
 assert(D.plots.quadrature.series[0].points[0][1]>-2);assert(D.plots.quadrature.series[1].points[0][1]>-2);assert(D.plots.quadrature.caption.includes('not a rigorous'));
 assert.equal(fs.readFileSync(new URL('team-quadrature.csv',base),'utf8'),fs.readFileSync(new URL('forward/output/quadrature_refinement.csv',records),'utf8'));
});
check('Actual proof routes and costs match recorded meetings and ordered replay',()=>{
 const p=read('proof_results.json');assert.equal(D.routes.length,11);for(const r of D.routes){const s=p.routes[r.name].result;assert.equal(r.status,s.status);assert.equal(r.cost,s.certified_cost??null);if(r.status==='proved'){assert(s.first_meeting_candidate.passed);assert(s.independent_ordered_replay.passed);}}
 assert.equal(D.routes.filter(r=>r.status==='proved').length,2);assert.equal(p.routes.four_dimensional_yang_mills.result.status,'not_derivable');
 const compact=JSON.parse(D.documents.proof);for(const [name,r] of Object.entries(p.routes)){assert.deepEqual(compact.routes[name].library,r.library);assert.deepEqual(compact.routes[name].result.first_meeting_candidate,r.result.first_meeting_candidate);}
});
check('Roadmap separates completed loops, unexecuted interval cover and open physical target',()=>{
 assert.deepEqual(plain(D.roadmap),read('current_roadmap.json').items);assert.equal(D.roadmap.filter(r=>r.status==='completed').length,2);assert.equal(D.roadmap.find(r=>r.id==='NEXT-A').status,'planned');assert.equal(D.roadmap.find(r=>r.id==='CONTINUUM').status,'open');
 assert(T.render('team-roadmap').includes('complete orthonormal basis'));assert(T.render('team-loop2').includes('implementation cap of48'));assert(T.render('home').includes('four-dimensional Yang–Mills problem remains open'));
});
check('Malformed plot and graph input gives an explicit unavailable state',()=>{
 const old=D.plots.certificate;for(const series of [null,[],[null],[{points:[[0,NaN]]}],[{points:[[Infinity,1]]}],[{points:[[1,2,3]]}]]){D.plots.certificate={series};assert(ctx.ResearchTeam.plot('certificate').includes('No valid recorded data'));}D.plots.certificate=old;
 const saved=D.collaboration.nodes;D.collaboration.nodes=[{id:'x',x:NaN,y:0}];assert(ctx.ResearchTeam.graph().includes('unavailable'));D.collaboration.nodes=saved;
});
check('Dynamic labels and source URLs are escaped',()=>{
 for(const [list,field,route] of [[D.collaboration.nodes,'label','team-map'],[D.roadmap,'forward','team-roadmap'],[D.reviews,'name','team-review'],[D.sources,'title','team-review']]){const old=list[0][field];list[0][field]='<img src=x onerror=alert(1)>';assert(!T.render(route).includes('<img'));list[0][field]=old;}
 const old=D.sources[0].url;D.sources[0].url='javascript:alert(1)';assert(!T.render('team-review').includes('href="javascript:'));D.sources[0].url=old;
});
check('Normal/optimized modes are not described as separate independent reviews',()=>{
 assert(T.render('team-review').includes('not counted as separate'));assert(D.reviews.some(r=>r.name==='Independent proof admission review'&&r.status.startsWith('36')));assert(D.reviews.some(r=>r.name==='Independent exact certificate review'&&r.status.startsWith('59')));
 assert(T.render('team-review').includes('keyboard interaction have not been audited'));assert(fs.statSync(new URL('research-team-data.js',base)).size<1500000);
});
const report={status:'passed',count:checks.length,checks,scope:'Actual-script Node VM routes, graph/data/doc bindings, exact decimal containment and failure states. No real-browser visual or keyboard audit.'};
fs.writeFileSync(new URL('site-validation.json',records),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
