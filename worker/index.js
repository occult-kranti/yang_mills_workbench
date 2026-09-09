// ASSETS, CATEGORIES, and the unmodified SAX parser are bundled by build-hosted.mjs.
const TTL=900000,MAX_BYTES=2*1024*1024;
const memoryCache=new Map();
let requestQueue=Promise.resolve(),nextRequestAt=0;
const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
function normalizeDate(raw){const day=raw.slice(0,10);if(!/^\d{4}-\d{2}-\d{2}$/.test(day)||!Number.isFinite(Date.parse(day))||new Date(day).toISOString().slice(0,10)!==day)throw Error('Invalid date in arXiv response');return day}
function normalizeId(raw){let id=raw.trim();if(/^https?:\/\//i.test(id)){const u=new URL(id);if(!['arxiv.org','www.arxiv.org'].includes(u.hostname)||u.port||u.username||u.password||u.search||u.hash||!u.pathname.startsWith('/abs/'))throw Error('Invalid arXiv identifier');id=u.pathname.slice(5)}if(!/^(?:[a-z-]+(?:\.[A-Z-]+)?\/\d{7}|\d{4}\.\d{4,5})(?:v\d+)?$/i.test(id))throw Error('Invalid arXiv identifier');return id}
export function parseFeed(xml,category){
 if(new TextEncoder().encode(xml).byteLength>MAX_BYTES)throw Error('arXiv response too large');
 const parser=SAX.parser(true,{xmlns:true,strictEntities:true}),stack=[],papers=[];
 let entry=null,rootSeen=false;
 parser.onerror=e=>{throw Error('Malformed arXiv XML: '+e.message.split('\n')[0])};
 parser.ondoctype=()=>{throw Error('Unexpected document type in arXiv response')};
 parser.onopentag=tag=>{
  if(!rootSeen){rootSeen=true;if(tag.local!=='feed'||tag.uri!=='http://www.w3.org/2005/Atom')throw Error('Response is not an arXiv Atom feed')}
  stack.push({name:tag.local,text:''});
  if(tag.local==='entry'){if(entry)throw Error('Nested arXiv entry');entry={authors:[]}}
 };
 const text=t=>{if(stack.length)stack.at(-1).text+=t};parser.ontext=text;parser.oncdata=text;
 parser.onclosetag=()=>{
  const tag=stack.pop(),parent=stack.at(-1);
  if(entry){
   const value=tag.text.trim();
   if(parent?.name==='entry'&&['id','title','published','updated','doi','journal_ref'].includes(tag.name))entry[tag.name]=value;
   if(tag.name==='name'&&parent?.name==='author'&&value)entry.authors.push(value);
   if(tag.name==='error')throw Error('arXiv returned an error');
   if(tag.name==='entry'){
    if(!entry.title||entry.title.toLowerCase()==='error'||!entry.id||!entry.published||!entry.updated||!entry.authors.length)throw Error('Incomplete arXiv entry');
    const id=normalizeId(entry.id),doi=(entry.doi||'').replace(/^https:\/\/doi.org\//i,'').replace(/^doi:\s*/i,'');
    papers.push({id,title:entry.title.replace(/\s+/g,' '),authors:entry.authors,date:normalizeDate(entry.published),updated:normalizeDate(entry.updated),status:entry.journal_ref?'arXiv record; journal reference supplied':'arXiv preprint; publication not verified',url:'https://arxiv.org/abs/'+id,doi:/^10\.\d{4,9}\/[-._;()/:A-Z0-9]+$/i.test(doi)?'https://doi.org/'+doi:null,journal:entry.journal_ref||null,category});entry=null;
   }
  }
  if(parent)parent.text+=tag.text;
 };
 parser.write(xml).close();if(!rootSeen)throw Error('Empty arXiv response');return papers.slice(0,8);
}
async function limitedText(response){
 if(!response.body)throw Error('Empty arXiv response');const reader=response.body.getReader(),decoder=new TextDecoder();let bytes=0,text='';
 try{while(true){const {value,done}=await reader.read();if(done)break;bytes+=value.byteLength;if(bytes>MAX_BYTES)throw Error('arXiv response too large');text+=decoder.decode(value,{stream:true})}return text+decoder.decode()}finally{await reader.cancel().catch(()=>{});reader.releaseLock()}
}
async function retrieve(category){
 const pause=nextRequestAt-Date.now();if(pause>0)await new Promise(r=>setTimeout(r,pause));nextRequestAt=Date.now()+3000;
 const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),12000);
 try{
  const url=new URL('https://export.arxiv.org/api/query');url.search=new URLSearchParams({search_query:'cat:'+category,max_results:'8',sortBy:'submittedDate',sortOrder:'descending'});
  const response=await fetch(url,{signal:controller.signal,redirect:'error',headers:{Accept:'application/atom+xml','User-Agent':'PhysicsObservatory/1.0'}});
  if(!response.ok)throw Error('arXiv returned HTTP '+response.status);
  return parseFeed(await limitedText(response),category);
 }finally{clearTimeout(timer)}
}
async function getPapers(category,requestURL){
 const key=new Request(new URL('/__paper-cache/'+encodeURIComponent(category),requestURL).href);
 let previous=memoryCache.get(category),edge=globalThis.caches?.default;
 if(!previous&&edge){try{const hit=await edge.match(key);if(hit)previous=await hit.json()}catch{}}
 const age=previous?Date.now()-Date.parse(previous.fetchedAt):Infinity;
 if(previous&&Array.isArray(previous.papers)&&age>=0&&age<TTL)return {...previous,cached:true,category};
 try{
  const papers=await retrieve(category),record={papers,fetchedAt:new Date(Date.now()).toISOString()};memoryCache.set(category,record);
  if(edge){try{await edge.put(key,new Response(JSON.stringify(record),{headers:{'Content-Type':'application/json','Cache-Control':'public, max-age=86400'}}))}catch{}}
  return {...record,cached:false,category};
 }catch(e){
  if(previous&&Array.isArray(previous.papers))return {...previous,cached:true,category,error:'Refresh unavailable; showing previously retrieved records.'};
  return {papers:[],fetchedAt:null,cached:false,category,error:'arXiv discovery is temporarily unavailable. Use the category link or the curated papers. '+(e.name==='AbortError'?'Request timed out.':e.message)};
 }
}
export default {async fetch(request){
 const url=new URL(request.url);
 if(!['GET','HEAD'].includes(request.method))return json({error:'Method not allowed'},405);
 if(url.pathname==='/api/papers'){
  const origin=request.headers.get('Origin');if(origin&&origin!==url.origin)return json({error:'Same-origin requests required'},403);
  const category=url.searchParams.get('category');if(!CATEGORIES.has(category))return json({error:'Unsupported category'},400);
  if(request.method==='HEAD')return new Response(null,{status:200});
  const task=requestQueue.then(()=>getPapers(category,url));requestQueue=task.catch(()=>{});
  return json(await task);
 }
 const asset=Object.hasOwn(ASSETS,url.pathname)?ASSETS[url.pathname]:null;
 if(!asset)return new Response('Not found',{status:404,headers:{'Content-Type':'text/plain; charset=utf-8'}});
 const body=request.method==='HEAD'?null:asset.binary?Uint8Array.from(atob(asset.body),c=>c.charCodeAt(0)):asset.body;
 return new Response(body,{headers:{'Content-Type':asset.type,'Cache-Control':'private, no-cache','X-Content-Type-Options':'nosniff'}});
}};
