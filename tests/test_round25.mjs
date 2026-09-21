import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const root=new URL('../',import.meta.url),read=p=>fs.readFileSync(new URL(p,root),'utf8');
let entries=0;
for(const folder of ['dist','docs']){
 const elements=new Map();
 const element=(id,value='')=>{const e={value,textContent:'',innerHTML:'',listeners:{},addEventListener(k,f){this.listeners[k]=f;}};elements.set(id,e);return e;};
 const context={window:{ResearchObservatory:{render:r=>'archive:'+r,afterRender(){}}},location:{hash:'#research'},document:{title:'',getElementById:id=>elements.get(id),querySelectorAll:()=>[]}};
 vm.createContext(context);for(const f of ['research-round25-data.js','research-round25.js'])vm.runInContext(read(`${folder}/${f}`),context);
 const R=context.window.ResearchRound25;
 assert.equal(R.data.history.rounds.length,23);assert.equal(R.data.history.counts.entries,111);
 const gates=new Set();
 for(const r of R.data.history.rounds)for(const x of r.runs){
  entries++;assert(x.bullets.length>0);for(const p of x.sources)assert(fs.existsSync(new URL(p,root)),p);
  if(x.gate_sha256){const p=x.sources[0];assert(!gates.has(p));gates.add(p);assert.equal(x.gate_sha256,createHash('sha256').update(read(p)).digest('hex'));}
 }
 assert.equal(gates.size,76);
 for(const x of R.data.loops)assert(R.render('round25-'+x.loop).includes(x.gate_sha256));
 for(const r of ['home','all-results','contributions','resonance-methods','use-results','round25-roadmap']){const page=R.render(r);assert(page.includes('Research navigation'));assert(!page.includes('undefined'));}
 assert(R.render('all-results').includes('Round1/2'));assert(R.render('all-results').includes('scientific priority'));
 assert(R.render('round25-roadmap').includes('None of these goals has been executed'));
 assert.equal(R.render('newton'),'archive:newton');assert(R.render('round24-home').includes('archive:home'));
 assert(R.archiveRows('nonexistent-zzzz').includes('No recorded entries'));
 assert(R.archiveRows('','24').includes('Round 24'));assert(!R.archiveRows('','24').includes('Round 23'));
 R.data.history.rounds[0].runs[0].bullets.push('<img src=x onerror=alert(1)>');assert(!R.archiveRows('onerror').includes('<img src=x'));
 const z=element('r25-z','1');element('r25-z-value');const endpoint=element('r25-endpoint');R.afterRender();assert(endpoint.innerHTML.includes('1.19048e-8'));z.value='.5';z.listeners.input();assert(endpoint.innerHTML.includes('5.95238e-9'));
 elements.clear();element('r25-chi','1');element('r25-q','5');element('r25-chi-value');element('r25-q-value');const modes=element('r25-modes');context.location.hash='#research/resonance-methods';R.afterRender();assert(modes.innerHTML.includes('10.59'));elements.get('r25-chi').value='.75';elements.get('r25-chi').listeners.input();assert(modes.innerHTML.includes('7.94'));
 const m=R.earthModes(1,5);assert(m[0].peak<m[0].ideal);assert(Math.abs(m[1].ideal/m[0].ideal-Math.sqrt(3))<1e-14);
 elements.clear();element('r25-search','');element('r25-round','25');const ledger=element('r25-ledger');element('r25-expand');element('r25-collapse');context.location.hash='#research/all-results';R.afterRender();elements.get('r25-round').listeners.change();assert(ledger.innerHTML.includes('AA2'));assert(!ledger.innerHTML.includes('Round 24'));
 const scripts=[...read(`${folder}/index.html`).matchAll(/<script\s+src="([^"]+)"/g)].map(x=>x[1].split('/').pop());
 assert(scripts.indexOf('research-round25.js')>scripts.indexOf('research-round24.js'));assert(scripts.indexOf('research-round25.js')<scripts.indexOf('app.js'));assert.equal(scripts.filter(x=>x==='research-round25.js').length,1);
}
console.log(JSON.stringify({status:'passed',history_entries_compared:entries,scope:'source links and gate hashes, archive coverage, routes, filters, actual slider handlers, escaping, script ordering and stable mode display'}));
