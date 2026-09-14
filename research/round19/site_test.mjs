import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const root = new URL('../../', import.meta.url);
const dist = new URL('../../dist/', import.meta.url);
const events = {};
const nodes = new Map();
function node(selector){
  if(!nodes.has(selector)){
    nodes.set(selector,{innerHTML:'',textContent:'',open:false,showModal(){this.open=true},close(){this.open=false},addEventListener(){},querySelector(){return node(selector+' child')}});
  }
  return nodes.get(selector);
}
const ctx = {
  console,
  URL,
  Blob,
  Math,
  location:{hash:'#research'},
  localStorage:{getItem(){return null},setItem(){}},
  document:{title:'',querySelector:node,getElementById:id=>node('#'+id),addEventListener:(e,f)=>(events[e]??=[]).push(f)},
  addEventListener(){}
};
ctx.window = ctx;
vm.createContext(ctx);
const index = fs.readFileSync(new URL('index.html', dist), 'utf8');
const researchScripts = [...index.matchAll(/<script src="(research[^"]*\.js)"/g)].map(m=>m[1]).filter(file=>file!=='research-contributions.js');
for (const file of researchScripts) vm.runInContext(fs.readFileSync(new URL(file, dist), 'utf8'), ctx, {filename:file});
vm.runInContext(fs.readFileSync(new URL('research-paired.js', dist), 'utf8'), ctx, {filename:'research-paired.js'});

const routes = ['home','paired-a1','paired-a2','paired-b1','paired-b2','paired-c1','paired-c2','paired-roadmap','paired-review'];
for (const route of routes) {
  ctx.location.hash = '#research/' + route;
  const html = ctx.ResearchObservatory.render(route);
  assert.equal((html.match(/<h1>/g)||[]).length, 1, route);
  assert(html.includes('aria-current="page"'), route);
  assert(!html.includes('Research page not found'), route);
  ctx.ResearchObservatory.afterRender();
  assert(ctx.document.title.includes('Yang–Mills Workbench'), route);
}
const home = ctx.ResearchObservatory.render('home');
assert(home.includes('Approximate opposing golden logarithmic spirals'));
assert(home.includes('no Round19 physical test of the geometry is recorded') || home.includes('No physical test of the geometry has been performed in Round19'));
assert(home.includes('viewBox="0 0 1040 760"'));
assert.equal((home.match(/class="paired-card /g)||[]).length, 6);
assert.equal((home.match(/class="paired-node-link"/g)||[]).length, 6);
assert(home.includes('#research/paired-a1'));
assert(home.includes('A2 · Representation bridge'));
assert(home.includes('B2 · Finite spectral bound'));
assert(home.includes('C2 · Certified static integral'));
assert(!home.includes('A2 · Dense bridge'));
assert(!home.includes('C2 · Physical readout'));
assert(home.includes('Text fallback'));
assert(home.includes('C nodes are static κ integrals with physical matching open'));
assert(home.includes('Static κ; physical matching open'));
assert(home.includes('E★ and common α scale.'));
assert(home.includes('spectral checkpoint'));
assert(/accepted loop gates? recorded/.test(home));
assert(home.includes('E★ &gt; 0'));
assert(home.includes('α_min/E★ and α/E★'));
assert(home.includes('Goal B records α/E★ = 2'));
assert(home.includes('λ_f/α'));
assert(home.includes('κ'));
assert(home.includes('not a regulator, physical time matching variable or Hamiltonian energy scale'));
assert(home.includes('research/round19/advisor/contract-a1.json'));
assert(home.includes('/blob/main/research/round19/advisor/contract-a1.json'));
assert(!/\b100%\b|progress meter/i.test(home));
assert(!/solved Yang|Clay mass gap proved/i.test(home));

const data = ctx.ResearchPaired.data;
const a1State = data.loops.find(x => x.id === 'A1')?.state;
const a1 = ctx.ResearchObservatory.render('paired-a1');
if (a1State === 'accepted') {
  assert(a1.includes('For every reachable selected clipped component'));
  assert(a1.includes('Remaining open:'));
  assert(a1.includes('fresh replay reproduced saved forward outputs'));
} else {
  assert(a1.includes('Forward A1 evidence currently reports'));
  assert(a1.includes('No A1 advisor gate is accepted yet'));
}
assert(!a1.includes('stronger mutation controls before any gate'));
assert(a1.includes('alpha/8') || a1.includes('α/8'));
assert(a1.includes('boundary-classification.json'));
assert(a1.includes('backward/a1/comparison/comparison.json'));

const a2 = ctx.ResearchObservatory.render('paired-a2');
assert(a2.includes('accepted gap:'));
assert(a2.includes('not finite clipped-restriction convergence'));
assert(a2.includes('a2-source-bound-inventory.json'));
const b1 = ctx.ResearchObservatory.render('paired-b1');
const b1State = data.loops.find(x => x.id === 'B1')?.state;
assert(b1State === 'accepted' ? b1.includes('b1-gate.json') : b1.includes('B1 is frozen and running'));
assert(b1.includes('contract-b1.json'));
assert(b1.includes('strict-cutoff'));

const b2 = ctx.ResearchObservatory.render('paired-b2');
assert(b2.includes('b2-gate.json'));
assert(b2.includes('validation-b2.json'));
assert(b2.includes('26 checks'));
assert(b2.includes('R(r) = [9 − 13r − sqrt(100r² − 54r + 9)]/2'));
assert(b2.includes('(33 − 6√5)α/16'));
assert(b2.includes('19α/32'));
assert(b2.includes('(30 − 2√87)/23'));
assert(b2.includes('not a physical failure'));
assert(!b2.includes('Clay mass gap result'));
const c1 = ctx.ResearchObservatory.render('paired-c1');
assert(c1.includes('contract-c1.json'));
assert(c1.includes('c1-gate.json'));
assert(c1.includes('6054'));
assert(c1.includes('S=3x+y+z+w+t') || c1.includes('S = 3x + y + z + w + t'));
assert(c1.includes('7.9244597e-7') || c1.includes('7.924459'));
assert(c1.includes('physical matching remains open') || c1.includes('physical-scale matching remains open'));
assert(c1.includes('physical energy/time-scale matching') || c1.includes('physical matching remains open')); 

const review = ctx.ResearchObservatory.render('paired-review');
assert(review.includes('Frozen contracts and controls'));
assert(review.includes('Advisor gates'));
assert(review.includes('Exception ledger'));
assert(review.includes('boundary-clipping'));
assert(review.includes('enlarged-gram-sparsity'));
assert(review.includes('W*W=PV^2P-(PVP)^2'));
assert(review.includes('/blob/main/research/round19/exception-ledger.json'));
assert(review.includes('/blob/main/research/round19/advisor/contract-b1.json'));
assert(review.includes('No current Round19 file proves'));

const round18 = ctx.ResearchObservatory.render('review18-home');
assert(round18.includes('Historical Round18 snapshot'));
assert(round18.includes('Current Round19 paired view'));
assert(ctx.ResearchObservatory.render('review17-home').includes('Historical Round17'));
assert(ctx.ResearchObservatory.render('__proto__').includes('Research page not found'));

assert.equal(JSON.stringify(data.loops.map(x=>x.id)), JSON.stringify(['A1','A2','B1','B2','C1','C2']));
const acceptedLoopIds = data.loops.filter(x=>x.state === 'accepted').map(x=>x.id);
assert.equal(JSON.stringify(acceptedLoopIds), JSON.stringify(['A1','A2','B1','B2','C1','C2']));
assert.equal(data.meta.accepted_loop_count, 6);
assert(data.meta.summary.includes('6 of six Round19 loop gates are accepted'));
assert.equal(data.loops.find(x=>x.id === 'C2')?.state, 'accepted');
assert.equal(data.evidence.find(x=>x.key === 'gate-c2')?.hashes_ok, true);
assert(data.evidence.length >= 4);
assert(data.evidence.every(x => ['pending','running','accepted','limited','rejected'].includes(x.state)));
assert(data.exception_ledger.entries.length >= 10);
assert(data.exception_ledger.entries.filter(x => x.loop === 'B1').every(x => x.status && x.evidence.length));
assert(data.evidence.find(x => x.key === 'forward-a1-results')?.state === 'accepted');
assert.equal(data.evidence.find(x => x.key === 'gate-b2')?.state, 'accepted');
assert.equal(data.evidence.find(x => x.key === 'gate-b2')?.hashes_ok, true);
assert.equal(data.evidence.find(x => x.key === 'gate-b2')?.inventory_complete, true);
assert.equal(data.evidence.find(x => x.key === 'validation-b2')?.state, 'accepted');
assert.equal(data.evidence.find(x => x.key === 'gate-c1')?.state, 'accepted');
assert.equal(data.evidence.find(x => x.key === 'gate-c1')?.hashes_ok, true);
assert.equal(data.evidence.find(x => x.key === 'gate-c1')?.inventory_complete, true);
if (data.evidence.some(x => x.key === 'validation-c1')) assert.equal(data.evidence.find(x => x.key === 'validation-c1')?.state, 'accepted');
assert(fs.readFileSync(new URL('round19/build_site.py', new URL('../', import.meta.url)), 'utf8').includes('missing required accepted-gate inventory item'));
assert(fs.readFileSync(new URL('round19/build_site.py', new URL('../', import.meta.url)), 'utf8').includes('mathematical_result'));
assert(fs.readFileSync(new URL('round19/build_site.py', new URL('../', import.meta.url)), 'utf8').includes('position=(u,side)'));
assert(fs.readFileSync(new URL('round19/build_site.py', new URL('../', import.meta.url)), 'utf8').includes('Math.pow(phi,(theta+2.95)/(Math.PI/2))'));

const circles = [...home.matchAll(/<circle class="(?:forward|reverse)" cx="([0-9.]+)" cy="([0-9.]+)" r="18"/g)].map(m => [Number(m[1]), Number(m[2])]);
for (let i = 0; i < circles.length; i += 2) {
  const dx = circles[i][0] - circles[i+1][0], dy = circles[i][1] - circles[i+1][1];
  assert(Math.hypot(dx, dy) > 100, 'paired node spacing ' + i/2);
}
console.log(JSON.stringify({routes:routes.length,evidence:data.evidence.length,status:data.meta.status}));


// Standalone overview artifact: no legacy megabyte bundles, hash navigation across every new route.
const overviewHtml = fs.readFileSync(new URL('round19/overview.html', new URL('../', import.meta.url)), 'utf8');
assert(overviewHtml.includes('Round19 review artifact'));
assert(!overviewHtml.includes('not published on GitHub Pages'));
assert(overviewHtml.includes('/tree/main'));
assert(!overviewHtml.includes('research-next-data.js'));
assert(!overviewHtml.includes('OBSERVATORY_NEXT'));
const overviewEvents = {};
const overviewMain = {innerHTML:'',querySelector(){return {scrollIntoView(){}}}};
const overviewCtx = {
  console,
  URL,
  Math,
  location:{hash:'#research/home', href:'https://example.test/research/round19/overview.html#research/home'},
  document:{
    title:'',
    getElementById(id){return id === 'main' ? overviewMain : null},
    querySelector(){return null}
  },
  addEventListener(event, fn){(overviewEvents[event] ??= []).push(fn)}
};
overviewCtx.window = overviewCtx;
vm.createContext(overviewCtx);
for (const match of overviewHtml.matchAll(/<script>([\s\S]*?)<\/script>/g)) vm.runInContext(match[1], overviewCtx, {filename:'overview-inline.js'});
for (const route of routes) {
  overviewCtx.location.hash = '#research/' + route;
  for (const fn of overviewEvents.hashchange ?? []) fn();
  assert(overviewMain.innerHTML.includes('<h1>'), 'overview h1 ' + route);
  assert(!overviewMain.innerHTML.includes('Research page not found'), 'overview route ' + route);
  assert(overviewMain.innerHTML.includes('Branch-only review artifact') === false, 'top chrome not rerendered into main');
}
overviewCtx.location.hash = '#research/paired-review';
for (const fn of overviewEvents.hashchange ?? []) fn();
assert(overviewMain.innerHTML.includes('Exception ledger'));
assert(overviewMain.innerHTML.includes('validation-b2.json'));
assert(overviewMain.innerHTML.includes('c1-gate.json'));
assert(overviewMain.innerHTML.includes('Static κ; physical matching open') || overviewMain.innerHTML.includes('projector-dependent-cross-gram'));

overviewCtx.location.hash = '#research/review18-home';
for (const fn of overviewEvents.hashchange ?? []) fn();
assert(overviewMain.innerHTML.includes('Historical Round18 snapshot'));
assert(overviewMain.innerHTML.includes('https://occult-kranti.github.io/yang_mills_workbench/#research/next-bridge'));

// Malformed accepted gates must fail closed. Use a temp repository copy so the test does not mutate real advisor files.
const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ym19-gate-'));
fs.mkdirSync(path.join(tempRoot, 'research/round19/advisor'), {recursive:true});
fs.mkdirSync(path.join(tempRoot, 'dist'), {recursive:true});
fs.copyFileSync(new URL('round19/build_site.py', new URL('../', import.meta.url)), path.join(tempRoot, 'research/round19/build_site.py'));
fs.copyFileSync(new URL('round19/site-content.json', new URL('../', import.meta.url)), path.join(tempRoot, 'research/round19/site-content.json'));
fs.copyFileSync(new URL('research-paired.css', dist), path.join(tempRoot, 'dist/research-paired.css'));
const contractText = JSON.stringify({schema:'ym19-a1-contract-v1',status:'frozen-by-advisor',acceptance_tests:[],falsifying_controls:[]});
fs.writeFileSync(path.join(tempRoot, 'research/round19/advisor/contract-a1.json'), contractText);
const hash = await import('node:crypto').then(({createHash}) => createHash('sha256').update(contractText).digest('hex'));
fs.writeFileSync(path.join(tempRoot, 'research/round19/advisor/a1-gate.json'), JSON.stringify({
  schema:'ym19-advisor-loop-gate-v1',
  loop:'a1',
  status:'accepted',
  mathematical_result:'This accepted claim must not render because inventory is incomplete.',
  files:{'advisor/contract-a1.json':hash}
}));
execFileSync('python3', ['research/round19/build_site.py'], {cwd:tempRoot, stdio:'pipe'});
const badJs = fs.readFileSync(path.join(tempRoot, 'dist/research-paired.js'), 'utf8');
const badData = JSON.parse(badJs.match(/const EMBED=(.*?);\n const D=/s)[1]);
const badGate = badData.evidence.find(x => x.key === 'gate-a1');
assert.equal(badGate.state, 'limited');
assert.equal(badGate.hashes_ok, true);
assert.equal(badGate.inventory_complete, false);
assert(badGate.inventory_validation_errors.some(x => x.includes('forward source')));
const badA1 = badData.loops.find(x => x.id === 'A1');
assert.equal(badA1.state, 'limited');
assert(!badA1.result.includes('This accepted claim must not render'));
assert(badA1.result.includes('validation failed'));
