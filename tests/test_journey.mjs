import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const root = new URL('../', import.meta.url);
const read = path => fs.readFileSync(new URL(path, root), 'utf8');
const rational = text => { const [a,b='1'] = String(text).split('/'); return Number(a)/Number(b); };
const fixture = JSON.parse(read('research/round21/forward/m2/output/results.json'));
let count = 0;
for (const folder of ['dist','docs']) {
  const context = {window:{ResearchObservatory:{render:route=>`<article>${route}</article>`}}};
  vm.createContext(context);
  vm.runInContext(read(`${folder}/research-journey.js`), context);
  const {evaluateBound,render} = context.window.ResearchJourney;
  // Compare the user-facing calculator with already admitted independent rational
  // fixtures, including each separate error term and both endpoint controls.
  for (const row of fixture.profile_time_fixtures.rows) for (const window of row.windows) {
    const actual = evaluateBound(rational(row.profile.q),rational(window.gamma));
    for (const part of ['state','energy','residual','support','total']) {
      const expected = rational(part==='total'?window.total_upper:window.terms_upper[part]);
      assert(Math.abs(actual[part]-expected) <= Math.abs(expected)*2e-10+1e-15, `${folder}: q=${row.profile.q}, gamma=${window.gamma}, ${part}`);
    }
    assert.equal(actual.certified, window.sufficiency_in_scope);
    count++;
  }
  for (const [q,gamma] of [[0,0],[1,0],[NaN,0],[.9,-1],[.9,Infinity],[true,0]]) assert.throws(()=>evaluateBound(q,gamma), {name:'RangeError'});
  const html = render();
  assert.equal((html.match(/data-j-chapter=/g)||[]).length,7);
  for (const phrase of ['continuum mass-gap problem remains open','scientific priority remains unverified','actual nonconvergence has not been proved','It has not been executed','Reading progress, not scientific completion']) assert(html.includes(phrase),phrase);
  for (const target of [...html.matchAll(/data-j-go="(\d+)"/g)].map(m=>m[1])) assert(html.includes(`id="j-chapter-${target}"`));
  assert(context.window.ResearchObservatory.render('home').includes('#research/journey'));
  assert.equal(context.window.ResearchObservatory.render('round21-m2'),'<article>round21-m2</article>');
  assert(!/https?:\/\/[^" ]+\.(?:js|css)[" ]/.test(html));
}
assert.equal(read('dist/research-journey.js'),read('docs/research-journey.js'));
assert.equal(read('dist/research-journey.css'),read('docs/research-journey.css'));
const hashes = {};
for (const file of ['dist/research-journey.js','dist/research-journey.css','dist/index.html','docs/index.html','docs/build-manifest.json','research/round21/advisor/m2-gate.json','research/round21/forward/m2/output/results.json','research/round21/reverse/m2/output/results.json']) hashes[file]=crypto.createHash('sha256').update(read(file)).digest('hex');
console.log(JSON.stringify({status:'passed',scientific_release:'b96c1dc26a9860a27565d0e6d0668789d4244353',fixture_comparisons:count,checks:['All M2 rational time-window fixtures match the displayed majorant in dist and docs','Endpoint and invalid-parameter controls','Seven chapter targets, scientific scope and legacy-route delegation','Identical source and Pages journey assets'],source_sha256:hashes,scope:'Presentation checks against frozen scientific evidence; no new research loops.'},null,2));
