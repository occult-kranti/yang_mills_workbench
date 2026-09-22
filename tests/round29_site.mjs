/* Current presentation integration: real registry, source-bound status, routes and hostile text. */
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const read=p=>fs.readFileSync(new URL('../'+p,import.meta.url),'utf8');
const ctx={window:{},URL,location:{hash:'#research'},document:{title:'',getElementById(){return null}}};vm.createContext(ctx);
vm.runInContext(read('dist/research-round29-data.js'),ctx);
const D=ctx.window.ROUND29_DATA;
function environment(data){
 const context={window:{ROUND29_DATA:data,ResearchObservatory:{render:route=>'ARCHIVE:'+route,afterRender(){}},ResearchJourney:{cleanup(){}}},URL,location:{hash:'#research'},document:{title:'',getElementById(){return null}}};vm.createContext(context);vm.runInContext(read('dist/research-round29.js'),context);return context;
}
const C=environment(D),R=C.window.ResearchRound29;
assert.equal(D.author,'Hruday N M (BUNZEEY)');
assert.equal(R.counts().completed,D.progress.completed);
assert.equal(D.registry.contributions.length,new Set(D.registry.contributions.map(x=>x.id)).size);
for(const route of ['home','hnm-priorities','hnm-findings','contributions','drafts','sharing','round29-results','round29-sources','round29-roadmap','round29-proof','research-network',...D.loops.map(x=>'round29-'+x.id)]){
 const html=R.render(route);assert(html.includes('Research navigation'),route);assert(!html.includes('undefined'),route);assert(!html.includes('NaN'),route);assert(html.includes('Hruday N M (BUNZEEY)'),route);
}
assert(R.render('home').includes('Still open'));
assert(R.render('home').includes('not how much of a proof'));
assert(R.render('hnm-priorities').includes('not a ranking of verified world novelty'));
assert(R.render('contributions').includes('research catalog'));
assert(R.render('sharing').includes('research/round29/sharing/substack.md'));
assert(R.render('sharing').includes('research/round29/sharing/reddit.md'));
assert(R.render('round28-home').includes('ARCHIVE:home'));
assert(R.render('round26-home').includes('ARCHIVE:round26-home'));
for(const item of D.registry.contributions){
 const html=R.findingCards(item.id);assert(html.includes(item.id));assert(html.includes('Original record:'));assert(html.includes('Limit:'));
 for(const path of item.source_paths??[])assert(fs.existsSync(new URL('../'+path,import.meta.url)),`missing ${path}`);
 for(const note of item.current_extensions??[]){
  assert(D.registry.contributions.some(row=>row.id===note.id),'missing extension target '+note.id);
  assert(html.includes('Later reviewed extensions')&&html.includes(note.id));
  for(const path of note.source_paths??[])assert(fs.existsSync(new URL('../'+path,import.meta.url)),`missing extension ${path}`);
 }
}
for(const statement of D.registry.statements??[]){
 const item=D.registry.contributions.find(row=>row.id===statement.contribution_id);assert(item,'statement join '+statement.id);
 assert(R.matchesFinding(item,statement.id));assert(R.findingCards(statement.id).includes(statement.id));
}
assert.equal(R.matchesFinding(D.registry.contributions[0],D.registry.contributions[0].id,'absent-round'),false);
assert(R.findingCards('nonexistent_zz_search').includes('No named findings'));
for(const node of D.network.nodes)assert(R.networkDetails(node.id).includes(node.id));
const H=structuredClone(D);H.registry.contributions[0].display_name='<img src=x onerror=alert(1)>';H.registry.contributions[0].application='<script>bad()</script>';H.author='<script>bad()</script>';H.addendum={url:'javascript:alert(1)'};
const hostile=environment(H).window.ResearchRound29;
for(const route of ['home','hnm-findings','hnm-priorities','drafts']){const html=hostile.render(route);assert(!html.includes('<script>'));assert(!html.includes('<img src=x'));assert(!html.includes('href="javascript:'));}
for(const folder of ['dist','docs']){
 const html=read(folder+'/index.html'),scripts=[...html.matchAll(/<script src="([^"]+)"/g)].map(x=>x[1].split('/').pop());
 assert(scripts.indexOf('research-round29-data.js')<scripts.indexOf('research-round29.js'));assert(scripts.indexOf('research-round29.js')<scripts.indexOf('app.js'));assert(html.includes('name="author" content="Hruday N M (BUNZEEY)"'));
}
console.log(JSON.stringify({status:'passed',completed:R.counts().completed,registry:D.registry.contributions.length,equationRecords:D.registry.equations.length,networkNodes:D.network.nodes.length,scope:'Real registry and sources, current and archive routes, visible limitations, search, network detail records, HTML escaping and static load order.'}));
