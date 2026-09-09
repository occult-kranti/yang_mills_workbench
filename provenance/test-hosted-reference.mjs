import assert from 'node:assert/strict';
import worker,{parseFeed} from '../dist/server/index.js';
const feed=`<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom"><entry><id>http://arxiv.org/abs/2609.12345v2</id><title>Quantum &amp; gravitational tests</title><published>2026-09-02T00:00:00Z</published><updated>2026-09-04T00:00:00Z</updated><author><name>A. Author</name></author><arxiv:doi>10.1234/example</arxiv:doi><arxiv:journal_ref>A journal reference</arxiv:journal_ref></entry></feed>`;
const papers=parseFeed(feed,'quant-ph');assert.equal(papers.length,1);assert.equal(papers[0].title,'Quantum & gravitational tests');assert.equal(papers[0].doi,'https://doi.org/10.1234/example');assert.equal(papers[0].updated,'2026-09-04');assert.match(papers[0].status,/reference supplied/);
for(const bad of ['<html>Unavailable</html>',feed.replace('2026-09-02','2026-02-30'),feed.replace('http://arxiv.org/abs/','https://example.com/abs/'),feed.replace('</feed>','')])assert.throws(()=>parseFeed(bad,'quant-ph'));
assert.deepEqual(parseFeed('<feed xmlns="http://www.w3.org/2005/Atom"/>','quant-ph'),[]);
const origin='https://example.test';
for(const asset of ['/','/content.js','/calculators.js','/expansion-tools.js','/patents.js','/patents.css','/app.js','/style.css','/research.js','/research.css','/research-data.js']){const r=await worker.fetch(new Request(origin+asset));assert.equal(r.status,200,asset);assert((await r.text()).length>500,asset)}
const shipped=await (await worker.fetch(new Request(origin+'/content.json'))).json();assert.equal(shipped.specialisms.length,7);assert.equal(shipped.feeds.length,33);assert.equal(shipped.resources.length,164);
const pdf=await worker.fetch(new Request(origin+'/advisor-and-research-guide.pdf'));assert.equal(pdf.status,200);assert.equal(pdf.headers.get('Content-Type'),'application/pdf');assert.equal(new TextDecoder().decode((await pdf.arrayBuffer()).slice(0,5)),'%PDF-');assert.equal((await worker.fetch(new Request(origin+'/advisor-and-research-guide.pdf',{method:'HEAD'}))).body,null);
assert.equal(shipped.patents.inventory.length,311);assert.equal(shipped.patents.cases.length,28);assert.equal(shipped.patents.newton.records.length,12);
const index=await (await worker.fetch(new Request(origin+'/'))).text();assert(index.indexOf('expansion-tools.js')>index.indexOf('calculators.js'));assert(index.indexOf('expansion-tools.js')<index.indexOf('app.js'));assert(index.indexOf('patents.js')<index.indexOf('app.js'));assert(index.includes('patents.css'));assert(index.indexOf('research-data.js')<index.indexOf('research.js'));assert(index.indexOf('research.js')<index.indexOf('app.js'));
assert.equal((await worker.fetch(new Request(origin+'/worker/vendor/sax.js'))).status,404);
for(const asset of ['/research-hub.js','/research-hub-data.js','/research-hub.css','/research-map.json','/quadrature_refinement.csv','/tail_behavior.csv','/code_fix_convergence.csv']){
 const r=await worker.fetch(new Request(origin+asset));assert.equal(r.status,200,asset);assert((await r.text()).length>100,asset);
}
const review=await worker.fetch(new Request(origin+'/research-review.zip'));
assert.equal(review.status,200);assert.equal(review.headers.get('Content-Type'),'application/zip');
assert.equal(new TextDecoder().decode((await review.arrayBuffer()).slice(0,2)),'PK');
assert.equal((await worker.fetch(new Request(origin+'/research-review.zip',{method:'HEAD'}))).body,null);
for(const asset of ['/research-closures.js','/research-closures-data.js','/closure-proof-map.json','/finite_correct.csv','/finite_wrong.csv','/finite_delayed.csv','/finite_refinement.csv','/finite_matrix.csv','/gravity_constraints.csv','/gravity_case_summary.csv']){
 const r=await worker.fetch(new Request(origin+asset));assert.equal(r.status,200,asset);assert((await r.text()).length>100,asset);
 assert.equal((await worker.fetch(new Request(origin+asset,{method:'HEAD'}))).body,null,asset);
}
const closurePDF=await worker.fetch(new Request(origin+'/einstein-qed-variable-study.pdf'));
assert.equal(closurePDF.status,200);assert.equal(closurePDF.headers.get('Content-Type'),'application/pdf');
assert.equal(new TextDecoder().decode((await closurePDF.arrayBuffer()).slice(0,5)),'%PDF-');
const closureMap=await (await worker.fetch(new Request(origin+'/closure-proof-map.json'))).json();
assert.equal(Object.keys(closureMap.libraries).length,6);
assert.equal(closureMap.results.common_quantum_closure.status,'not_derivable');
assert.equal(closureMap.results.finite_continuation.certified_cost,17);
assert(index.indexOf('research-closures-data.js')<index.indexOf('research-closures.js'));
assert(index.indexOf('research-closures.js')<index.indexOf('app.js'));
const map=await (await worker.fetch(new Request(origin+'/research-map.json'))).json();assert.equal(map.nodes.length,44);
assert(index.includes('research-hub.css'));assert(index.indexOf('research-hub-data.js')<index.indexOf('research-hub.js'));assert(index.indexOf('research-hub.js')<index.indexOf('app.js'));
assert.equal((await worker.fetch(new Request(origin+'/api/papers?category=bad'))).status,400);
assert.equal((await worker.fetch(new Request(origin+'/api/papers?category=quant-ph',{headers:{Origin:'https://other.test'}}))).status,403);
const originalFetch=globalThis.fetch,originalNow=Date.now;let calls=0,now=Date.parse('2026-09-07T12:00:00Z');Date.now=()=>now;
try{
 globalThis.fetch=async url=>{calls++;assert.equal(url.hostname,'export.arxiv.org');assert.equal(url.searchParams.get('max_results'),'8');return new Response(feed)};
 const request=()=>new Request(origin+'/api/papers?category=quant-ph');
 const fresh=await (await worker.fetch(request())).json();assert.equal(fresh.cached,false);assert.equal(fresh.papers.length,1);
 // A fresh cache avoids a second upstream call.
 const cached=await (await worker.fetch(request())).json();assert.equal(cached.cached,true);assert.equal(calls,1);
 for(const category of ['physics.class-ph','eess.AS','math.MG','math.DG','math.HO']){now+=10000;const r=await worker.fetch(new Request(origin+'/api/papers?category='+category));assert.equal(r.status,200);const x=await r.json();assert.equal(x.category,category);assert.equal(x.papers.length,1);}
 now=Date.parse(fresh.fetchedAt)+901000;
 globalThis.fetch=async()=>{calls++;throw Error('offline')};
 const stale=await (await worker.fetch(request())).json();assert.equal(stale.cached,true);assert.equal(stale.fetchedAt,fresh.fetchedAt);assert.equal(stale.papers[0].id,fresh.papers[0].id);assert.match(stale.error,/previously retrieved/);
 now+=10000;
 const unavailable=await (await worker.fetch(new Request(origin+'/api/papers?category=gr-qc'))).json();assert.equal(unavailable.fetchedAt,null);assert.match(unavailable.error,/unavailable/);
}finally{globalThis.fetch=originalFetch;Date.now=originalNow}
console.log('PASS: hosted assets, namespace-aware Atom parsing, validation, category/origin controls, cached metadata, and stale/unavailable states.');
