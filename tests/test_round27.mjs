import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const root = new URL('../', import.meta.url);
const read = path => fs.readFileSync(new URL(path, root), 'utf8');
const exists = path => fs.existsSync(new URL(path, root));
const code = read('dist/research-round27.js');
function environment(data, renderer = code) {
  const calls = {render:[], after:0, cleanup:0};
  const context = {
    URL, location:{hash:'#research'}, document:{title:''},
    window:{ROUND27_DATA:data, ResearchJourney:{cleanup(){calls.cleanup++;}}, ResearchObservatory:{
      render(route){calls.render.push(route); return `<section data-archive="true">archive:${route}</section>`;},
      afterRender(){calls.after++;}, inheritedMethod:'retained'
    }}
  };
  vm.createContext(context); vm.runInContext(renderer, context);
  return {R:context.window.ResearchRound27, context, calls};
}
const fixture = {
  title:'Source <bound> research', summary:'A question & its scope.',
  loops:[
    {id:'ai1',title:'First reviewed result',accepted:'Finite estimate only.',verdict:'accepted_within_scope',bullets:['x < y'],limitations:['No infinite-volume transfer.'],equations:[{label:'A < B',expression:'a < b && c > 0',scope:'Finite support only.'}],sources:['research/round27/ai1/report.md']},
    {id:'ai2',title:'Second result',accepted:'Premise still missing.',verdict:'limited',limitations:['Missing uniform estimate.'],sources:['research/round27/ai2/report.md']},
    {id:'reselected3',title:'Dynamically selected third question',accepted:'Given the recorded premise.',verdict:'conditional',limitations:['Uniform premise is not proved.'],sources:['research/round27/third/report.md']}
  ],
  experts:[{id:'newton',name:'Newton research perspective',summary:'Analysis and exact limits.',sources:[{title:'Historical notes',url:'https://example.org/notes?q=1&b=2',depth:'Full text',status:'Historical source'},{title:'Discussion lead',url:'https://www.reddit.com/r/test/comments/example',depth:'Excerpt only',status:'Unverified conversation'}]}],
  progress:{requested:3,completed:2,percentage_statement:'No defensible numeric percentage; <scope> remains open.',obligations:[{name:'Construction',status:'Open',missing:'A nontrivial continuum theory.'},{name:'Uniform control',status:'Conditional',missing:['Uniform constants.','Matching at a fixed scale.']}]},
  roadmap:{next_goals:[{id:'AJ',title:'Next selected target',target:'Prove the named uniform input.'}]},
  addendum:{url:'ym-round27-addendum.html',title:'Round27 <addendum>'}
};
const E = environment(structuredClone(fixture)), {R, context, calls} = E;
assert.equal(context.window.ResearchObservatory.inheritedMethod, 'retained');
for (const route of ['home','round27','round27-results','round27-experts','round27-proof','round27-roadmap','round27-ai1','round27-ai2','round27-reselected3']) {
  const html = R.render(route);
  assert(html.includes('Research navigation'), route);
  assert(!html.includes('undefined'), route);
  assert(!html.includes('NaN'), route);
}
assert(R.render('home').includes('Source &lt;bound&gt; research'));
assert(R.render('home').includes('A question &amp; its scope.'));
assert(R.render('home').includes('3 recorded investigations'));
assert(R.render('home').includes('>2<small> / 3</small>'));
assert(!R.render('home').includes('66.67%'));
assert(R.render('home').includes('No defensible numeric percentage; &lt;scope&gt; remains open.'));
assert(R.render('home').includes('not a percentage of the mathematical problem solved'));
assert(R.render('home').includes('model-agent reviews'));
assert(R.render('round27-ai1').includes('a &lt; b &amp;&amp; c &gt; 0'));
assert(R.render('round27-ai1').includes('No infinite-volume transfer.'));
assert(R.render('round27-ai1').includes('Finite support only.'));
assert(R.render('round27-ai1').includes('accepted within scope'));
assert(R.render('round27-reselected3').includes('Dynamically selected third question'));
assert.equal(R.verdictClass({verdict:'accepted_within_scope'}), 'accepted');
assert.equal(R.verdictClass({verdict:'accepted_with_limitations_limited'}), 'limited');
assert.equal(R.verdictClass({verdict:'conditional'}), 'conditional');
assert.equal(R.verdictClass({verdict:'planned'}), 'planned');
assert.equal(R.verdictClass({verdict:'unclassified'}), 'neutral');
assert(R.render('round27-roadmap').includes('planning only'));
assert(R.render('round27-roadmap').includes('Prove the named uniform input.'));
assert(R.render('round27-proof').includes('<caption>Proof obligations'));
assert.equal((R.render('round27-proof').match(/<th scope="row">/g) ?? []).length, 2);
assert(R.render('round27-proof').includes('Matching at a fixed scale.'));
assert(R.render('round27-experts').includes('Full text'));
assert(R.render('round27-experts').includes('Excerpt only'));
assert(R.render('round27-experts').includes('Unverified conversation'));
assert.equal((R.render('round27-experts').match(/rel="noopener noreferrer"/g) ?? []).length, 2);
assert(R.render('round27-experts').includes('notes?q=1&amp;b=2'));
assert(R.render('drafts').includes('Round27 &lt;addendum&gt;'));
assert(R.render('drafts').includes('href="ym-round27-addendum.html"'));
assert(R.render('drafts').endsWith('<section data-archive="true">archive:drafts</section>'));
assert(R.render('drafts?version=1').endsWith('<section data-archive="true">archive:drafts?version=1</section>'));
assert(R.render('round26-home').includes('archive:home'));
for (const route of ['research-network?node=ai1','round26-ai1','round25-home','newton','resonance-methods','all-results','contributions']) {
  assert(R.render(route).includes('archive:' + route), route);
}
context.location.hash = '#research/round27-proof'; R.afterRender();
assert.equal(context.document.title, 'Proof obligations · Yang–Mills Workbench');
assert.equal(calls.after, 0);
context.location.hash = '#research/round27-reselected3'; R.afterRender();
assert.equal(context.document.title, 'Dynamically selected third question · Yang–Mills Workbench');
context.location.hash = '#research/round26-home'; R.afterRender();
assert.equal(context.document.title, 'Round26 archive · Yang–Mills Workbench');
context.location.hash = '#research/research-network?node=ai1'; R.afterRender();
assert.equal(calls.after, 1);
context.location.hash = '#research/drafts'; R.afterRender();
assert.equal(calls.after, 2);
assert.equal(calls.cleanup, 3);

// Reject executable schemes, credentials, protocol-relative targets and paths escaping the repository.
for (const url of ['javascript:alert(1)','data:text/html,<script>','http://example.org/','//example.org/','https://name:pass@example.org/','https://example.org/\" onclick=alert(1)','https:\\example.org/a','https://example.org/\nnext']) {
  assert.equal(R.safeURL(url), '', url);
  assert(!R.safeSource({url,title:'Unsafe source'}).includes('href='), url);
}
for (const path of ['../secret','/absolute','ok/../secret','ok/./file','ok//file','javascript:alert(1)','//example.org','file%2fsecret','file#anchor','file?x=y','x\\y']) {
  assert.equal(R.safePath(path), '', path);
  assert(!R.safeSource({path,title:'Unsafe source'}).includes('href='), path);
}
assert(R.safeSource('research/round27/ai1/report.md').includes('/blob/main/research/round27/ai1/report.md'));
assert(R.safeSource({url:'https://example.org/a',title:'A < B & C'}).includes('A &lt; B &amp; C'));
assert.equal(R.safeURL('ym-round27-addendum.html', true), 'ym-round27-addendum.html');
const attack = '<img src=x onerror="alert(1)"><script>bad()</script>';
const hostile = structuredClone(fixture);
hostile.title = attack;
hostile.loops[0].title = attack; hostile.loops[0].accepted = attack; hostile.loops[0].verdict = attack;
hostile.loops[0].equations = [{label:attack,expression:attack,scope:attack}];
hostile.loops[0].limitations = [attack]; hostile.loops[0].bullets = [attack];
hostile.loops[0].sources = [{url:'javascript:alert(1)',title:attack}];
hostile.experts = [{id:attack,name:attack,summary:attack,sources:[{title:attack,url:'https://example.org/source',depth:attack,status:attack}]}];
hostile.progress.percentage_statement = attack;
hostile.progress.obligations = [{name:attack,status:attack,missing:attack}];
hostile.roadmap.next_goals = [{id:attack,title:attack,target:attack}];
hostile.addendum = {url:'javascript:alert(1)',title:attack};
const H = environment(hostile).R;
for (const route of ['home','round27-ai1','round27-experts','round27-proof','round27-roadmap','drafts']) {
  const html = H.render(route);
  assert(!html.includes('<img'), route);
  assert(!html.includes('<script>'), route);
  assert(!html.includes('href="javascript:'), route);
}
assert(!H.render('drafts').includes('aria-label="Round27 manuscript addendum"'));
const missing = environment({loops:[{id:'only',title:'Unreviewed'}]}).R;
assert(missing.render('home').includes('Execution count has not been recorded.'));
assert(missing.render('round27-only').includes('Review not recorded'));
assert(missing.render('round27-only').includes('No limitation statement is attached'));
assert(missing.render('round27-proof').includes('No obligation inventory'));
assert.equal(missing.executionCounts().completed, null);
assert.equal(environment({...fixture,progress:{completed:-1,requested:NaN}}).R.executionCounts().requested, null);
assert.equal(environment(undefined).R, undefined);
const noPrior = {window:{ROUND27_DATA:fixture}};
vm.createContext(noPrior); vm.runInContext(code, noPrior);
assert.equal(noPrior.window.ResearchRound27, undefined);

let integratedBundles = 0;
if (!process.argv.includes('--fixture')) {
  for (const folder of ['dist','docs']) {
    assert(exists(`${folder}/research-round27-data.js`), `${folder}: data bundle is required`);
    const C = {window:{}}; vm.createContext(C); vm.runInContext(read(`${folder}/research-round27-data.js`), C);
    const data = C.window.ROUND27_DATA;
    const A = environment(data, read(`${folder}/research-round27.js`)).R;
    assert.equal(data.loops.length, 3, `${folder}: three actual investigations required`);
    assert.equal(new Set(data.loops.map(loop => loop.id ?? loop.loop)).size, data.loops.length);
    assert.equal(data.progress.requested, 3);
    assert.equal(data.progress.completed, 3);
    assert(data.progress.percentage_statement, 'The expert progress assessment must be explicit');
    assert(data.progress.obligations.length > 0, 'Proof obligations must be recorded');
    for (const loop of data.loops) {
      assert(loop.verdict, 'Every loop requires its reviewed verdict');
      assert(loop.accepted, 'Every loop requires a scope statement');
      assert(loop.limitations?.length, 'Every loop requires limitations');
      assert(loop.sources?.length, 'Every loop requires evidence');
      assert(A.render('round27-' + String(loop.id ?? loop.loop).toLowerCase()).includes(loop.title.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;')));
      for (const source of loop.sources) {
        const path = typeof source === 'string' ? source : source.path;
        if (path) assert(exists(path), `Evidence is missing: ${path}`);
      }
    }
    assert(data.experts.length >= 5, 'All requested historical perspectives must be represented');
    for (const expert of data.experts) {
      assert(expert.name && expert.summary && expert.sources.length);
      for (const source of expert.sources) {
        assert(A.safeURL(source.url), `Invalid expert source URL: ${source.url}`);
        assert(source.depth && source.status, 'Source depth and evidential status must travel together');
      }
    }
    const scripts = [...read(`${folder}/index.html`).matchAll(/<script\s+src="([^"]+)"/g)].map(match => match[1].split('/').pop());
    assert.equal(scripts.filter(script => script === 'research-round27.js').length, 1);
    assert(scripts.indexOf('research-round27-data.js') < scripts.indexOf('research-round27.js'));
    assert(scripts.indexOf('research-round27.js') > scripts.indexOf('research-drafts.js'));
    assert(scripts.indexOf('research-round27.js') < scripts.indexOf('app.js'));
    assert(read(`${folder}/index.html`).includes('research-round27.css'));
    integratedBundles++;
  }
}
console.log(JSON.stringify({status:'passed',integratedBundles,scope:'Dynamic loop routes, inherited routes and lifecycle, authoritative execution counts, source and addendum URL validation, HTML escaping, explicit limitation and proof-obligation rendering; actual evidence paths and load order when integrated.'}));
