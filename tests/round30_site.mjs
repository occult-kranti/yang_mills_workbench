/* Real final data only: bindings, current/archive integration and hostile text. */
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root = fileURLToPath(new URL('../',import.meta.url));
const read = name => fs.readFileSync(new URL('../' + name,import.meta.url),'utf8');
const digest = name => crypto.createHash('sha256').update(fs.readFileSync(new URL('../'+name,import.meta.url))).digest('hex');
const raw = {window:{}}; vm.createContext(raw);
vm.runInContext(read('dist/research-round29-data.js'),raw);
const old = structuredClone(raw.window.ROUND29_DATA);
vm.runInContext(read('dist/research-round30-data.js'),raw);
const data = raw.window.ROUND30_DATA;
assert.equal(data.author,'Hruday N M (BUNZEEY)');
assert.equal(data.progress.requested,3); assert.equal(data.progress.completed,3);
assert.equal(data.loops.length,3); assert.equal(new Set(data.loops.map(row=>row.id)).size,3);
assert.equal(raw.window.ROUND29_DATA.registry,data.registry,'current registry must load before Round29 renderer');
assert.equal(raw.window.ROUND29_DATA.network,data.network);
assert.equal(JSON.stringify(raw.window.ROUND29_DATA.loops),JSON.stringify(old.loops),'historical loops must remain intact');
for(const [name,hash] of Object.entries(data.input_bindings)) assert.equal(digest(name),hash,'changed source '+name);
for(const loop of data.loops){
  assert.equal(digest(loop.gate_path),loop.gate_sha256);
  const gate=JSON.parse(read(loop.gate_path));
  assert.equal(loop.accepted,gate.accepted); assert.equal(loop.verdict,gate.verdict);
  assert.equal(JSON.stringify(loop.limitations),JSON.stringify(gate.limitations));
  assert(data.registry.contributions.some(row=>row.id===loop.contribution_id));
}
assert.equal(read('dist/hnm-registry-r30.json'),read(data.registry_source));
function environment(payload=data){
  const historical=structuredClone(old); historical.registry=payload.registry; historical.network=payload.network;
  const context={window:{ROUND29_DATA:historical,ROUND30_DATA:payload,ResearchObservatory:{render:route=>'ARCHIVE:'+route,afterRender(){}},ResearchJourney:{cleanup(){}}},URL,location:{hash:'#research'},document:{title:'',getElementById(){return null}}};
  vm.createContext(context); vm.runInContext(read('dist/research-round29.js'),context); vm.runInContext(read('dist/research-round30.js'),context);
  return context;
}
const context=environment(),R=context.window.ResearchRound30,observatory=context.window.ResearchObservatory;
assert.equal(R.counts().completed,3);
const routes=['home','round30','drafts','round30-results','round30-roadmap','round30-sources','round30-proof','round30-calculator','hnm-findings','hnm-priorities','research-network',...data.loops.map(row=>'round30-'+row.id)];
for(const route of routes){
  const html=observatory.render(route);
  assert(html.includes('Research navigation'),route); assert(html.includes('Hruday N M (BUNZEEY)'),route);
  assert(!html.includes('undefined')&&!html.includes('NaN'),route);
  assert.equal((html.match(/<h1(?:\s|>)/g)||[]).length,1,'one page heading '+route);
  assert(html.includes('#research/round30-results'),'current navigation '+route);
}
assert(R.render('home').includes('not a percentage'));
assert(R.render('drafts').includes('ym-draft-03.pdf')&&R.render('drafts').includes('ym-draft-02.pdf'));
for(const route of ['round29','round29-results','round29-aq2']) assert(observatory.render(route).includes('Round29'),route);
assert(observatory.render('round26-home').includes('ARCHIVE:round26-home'));
for(const loop of data.loops){
  const html=R.render('round30-'+loop.id); assert(html.includes(loop.gate_sha256));
  assert(context.window.ResearchRound29.findingCards(loop.contribution_id).includes(loop.contribution_id));
}
assert(R.filterSources('', 'historical').length>0&&R.filterSources('', 'modern').length>0);
assert.equal(R.filterSources('nonexistent_zz_query').length,0);
assert(R.calculatorAdmitted());
for(const [alpha,tau] of [['1','1e-8'],['2','-1/100000000'],['1/2','0'],['0.001','1e-9']]){
  const js=R.spectralCertificate(alpha,tau),py=spawnSync('python3',['research/round30/calculators/spectral_certificate.py','--alpha='+alpha,'--tau='+tau],{cwd:root,encoding:'utf8'});
  assert.equal(py.status,0,py.stderr);const expected=JSON.parse(py.stdout);
  for(const key of Object.keys(js))assert.equal(JSON.stringify(js[key]),JSON.stringify(expected[key]),`calculator ${alpha},${tau}: ${key}`);
}
assert.equal(R.spectralCertificate('.5','0').alpha,'1/2');
for(const [alpha,tau] of [['0','0'],['-1','0'],['1','1.00000001e-8'],['Infinity','0'],['1','0/0']])assert.throws(()=>R.spectralCertificate(alpha,tau));
assert(R.render('round30-calculator').includes('not normalized probability'));
assert(R.render('round30-calculator').includes('not an established static susceptibility'));
const broken=structuredClone(data); broken.loops[0].gate_sha256='not-a-hash'; broken.loops[0].accepted='UNREVIEWED_SECRET_CLAIM'; broken.loops[0].summary='UNREVIEWED_SECRET_CLAIM';
const rejected=environment(broken).window.ResearchRound30;
assert.equal(rejected.counts().completed,2); assert(!rejected.render('home').includes('UNREVIEWED_SECRET_CLAIM'));
assert(!rejected.render('round30-'+broken.loops[0].id).includes('UNREVIEWED_SECRET_CLAIM'));
const hostile=structuredClone(data); hostile.author='<img src=x onerror=alert(1)>'; hostile.summary='<script>alert(1)</script>';
hostile.loops[0].title='<img src=x onerror=alert(1)>'; hostile.loops[0].equations=[{label:'<script>',expression:'</code><script>evil</script>'}];
hostile.survey[0].title='<script>evil</script>'; hostile.survey[0].url='javascript:alert(1)'; hostile.draft.url='../private.pdf';
const H=environment(hostile).window.ResearchRound30;
for(const route of ['home','drafts','round30-sources','round30-'+hostile.loops[0].id]){
  const html=H.render(route); assert(!html.includes('<script>')&&!html.includes('<img src=x'),route); assert(!html.includes('href="javascript:')&&!html.includes('src="../private.pdf'),route);
}
for(const input of ['javascript:alert(1)','https://a.test@b.test/','https://a.test\\evil','data:text/html,hi']) assert.equal(R.safeURL(input),'');
for(const input of ['../secret','a/../secret','/absolute','a\\b','%2e%2e/x']) assert.equal(R.safePath(input),'');
const html=read('dist/index.html'),scripts=[...html.matchAll(/<script src="([^"]+)"/g)].map(row=>row[1]);
for(const [before,after] of [['research-round29-data.js','research-round30-data.js'],['research-round30-data.js','research-round29.js'],['research-round29.js','research-round30.js'],['research-round30.js','app.js']]){
  assert(scripts.includes(before)&&scripts.includes(after)&&scripts.indexOf(before)<scripts.indexOf(after),before+' before '+after);
}
const replay=spawnSync('python3',['research/round30/presentation/build_site.py','--check'],{cwd:root,encoding:'utf8'});
assert.equal(replay.status,0,replay.stderr||replay.stdout);
console.log(JSON.stringify({status:'passed',completed:3,routes:routes.length,sourceRecords:data.survey.length,scope:'Real gate bindings, exact rebuild, current registry/network integration, archive routes, source filtering, unreviewed-claim suppression and HTML/URL controls.'}));
