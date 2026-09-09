import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const root=new URL('../',import.meta.url),checks=[];
function check(name,fn){fn();checks.push({name,passed:true});}
function load(folder){
 const base=new URL(folder+'/',root),nodes=new Map(),events={};
 const node=id=>{if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',style:{},dataset:{},value:'',open:false,addEventListener(){},focus(){},showModal(){this.open=true},close(){this.open=false},classList:{toggle(){},contains(){return false}},setAttribute(){}});return nodes.get(id);};
 const context={console,URL,Blob,setTimeout:()=>0,clearTimeout(){},location:{hash:'#research'},localStorage:{getItem(){return null},setItem(){}},document:{querySelector:node,querySelectorAll:()=>[],getElementById:id=>node('#'+id),addEventListener:(n,f)=>(events[n]??=[]).push(f),title:''},confirm:()=>true};context.window=context;context.addEventListener=()=>{};vm.createContext(context);
 const html=fs.readFileSync(new URL('index.html',base),'utf8'),files=[...html.matchAll(/<script src="([^"]+)"/g)].map(x=>x[1]);
 for(const file of files)vm.runInContext(fs.readFileSync(new URL(file,base),'utf8'),context,{filename:folder+'/'+file});
 return {base,context,node,files,run:code=>vm.runInContext(code,context)};
}
const local=load('dist'),pages=load('docs');
check('Local and Pages capability flags differ intentionally',()=>{assert.equal(local.context.WorkbenchRuntime.staticOnly,false);assert.equal(pages.context.WorkbenchRuntime.staticOnly,true);});
check('Pages build manifest binds every published file',()=>{const m=JSON.parse(fs.readFileSync(new URL('docs/build-manifest.json',root),'utf8'));assert.equal(m.base,'/yang_mills_workbench/');for(const [file,hash] of Object.entries(m.files))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(new URL('docs/'+file,root))).digest('hex'),hash,file);assert(fs.existsSync(new URL('docs/.nojekyll',root)));assert(!fs.existsSync(new URL('docs/server',root)));});
const routes=['home','dynamic-proof','exact-evolution','dynamic-experiments','volume-bridge','closure-audit','bridge-variables','bridge-roadmap','bridge-review','review11-home','two-model','two-spectrum','two-gap','two-certificates','two-dynamics','two-roadmap','two-review','review10-home','plaquette','plaquette-proof','plaquette-certificates','plaquette-drive','plaquette-next','plaquette-map','plaquette-review','review9-home','review8-home','finite','gravity','proofs','ym-transfer','evidence'];
check('All recorded download links stay under the project prefix',()=>{let count=0;for(const route of routes){const html=pages.context.ResearchObservatory.render(route);assert(!html.includes('Research page not found'),route);for(const m of html.matchAll(/href="([^"]+)" download/g)){const url=new URL(m[1],'https://occult-kranti.github.io/yang_mills_workbench/');assert.equal(url.origin,'https://occult-kranti.github.io');assert(url.pathname.startsWith('/yang_mills_workbench/'),m[1]);const file=url.pathname.slice('/yang_mills_workbench/'.length);assert(fs.existsSync(new URL('docs/'+file,root)),file);count++;}}assert(count>20);});
check('Scientific certificate payloads survive the Pages transport unchanged',()=>{for(const key of ['certificates','range','drive'])assert.deepEqual(JSON.parse(JSON.stringify(pages.context.OBSERVATORY_PLAQUETTE[key])),JSON.parse(JSON.stringify(local.context.OBSERVATORY_PLAQUETTE[key])));});
check('Source URLs remain external and unmodified',()=>{assert.deepEqual(JSON.parse(JSON.stringify(pages.context.OBSERVATORY_PLAQUETTE.sources)),JSON.parse(JSON.stringify(local.context.OBSERVATORY_PLAQUETTE.sources)));});
check('Core application views remain available on Pages',()=>{for(const view of ['study','laboratory','papers','patents/dossiers','sound','astronomy']){pages.context.location.hash='#'+view;pages.run('render()');assert(pages.node('#main').innerHTML.includes('<h1>'),view);}});
let calls=0;pages.context.fetch=async()=>{calls++;throw Error('Static host must not request local API');};pages.context.location.hash='#papers';await pages.run('refreshPapers()');
check('Static metadata action makes no unavailable API request',()=>{assert.equal(calls,0);assert(pages.node('#main').innerHTML.includes('local Python server'));assert(pages.node('#main').innerHTML.includes('Browse the category at arXiv'));});
let localCalls=0;local.context.fetch=async url=>{localCalls++;assert(String(url).startsWith('/api/papers'));return {ok:true,json:async()=>({papers:[],fetchedAt:'2026-09-09T00:00:00Z',category:'quant-ph'})};};local.context.location.hash='#papers';await local.run('refreshPapers()');
check('Local metadata endpoint remains functional through its mocked contract',()=>assert.equal(localCalls,1));
check('Unsafe source URLs remain rejected',()=>{for(const url of ['javascript:alert(1)','https://user:password@example.org','//evil.example/x'])assert.equal(pages.context.ResearchHub.safeURL(url),'#');});
console.log(JSON.stringify({status:'passed',count:checks.length,checks,scope:'Static/local execution and transport checks in a Node VM; no browser visual audit.'}));
