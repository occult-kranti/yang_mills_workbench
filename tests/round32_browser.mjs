/* Real browser QA against the Round32 site layer. Mirrors tests/round31_browser.mjs.
 * Round32 is a five-sub-round, ten-investigation cycle; while fewer than ten
 * investigations are reviewed the bundle is a placeholder and the renderer shows
 * no scientific findings on any Round32-owned route (see incomplete() in
 * dist/research-round32.js). --allow-incomplete permits running against such a
 * placeholder bundle ("smoke mode"): only home and the preserved Round31 archive
 * routes are navigated, and every Round32-owned route (including all ten planned
 * loop ids) is checked in-page for the incomplete-cycle sentence instead. Without
 * --allow-incomplete the bundle must report ten completed investigations. --final
 * marks the receipt as the authoritative source-render verification and requires
 * every listed source file to exist (a smoke run tolerates and records 'missing').
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';

const require = createRequire(import.meta.url);
const {chromium} = require(process.env.YM_PLAYWRIGHT_MODULE || '/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = fileURLToPath(new URL('../', import.meta.url));
const site = process.env.YM_SITE_FOLDER || 'docs';
const port = Number(process.env.YM_SITE_PORT || 8032);
const output = process.env.YM_QA_OUTPUT || '/tmp/yang-mills-round32-site-qa';
fs.mkdirSync(output, {recursive: true});

const allowIncomplete = process.argv.includes('--allow-incomplete');
const finalRun = process.argv.includes('--final');

// Fixed loop id order the renderer itself uses (dist/research-round32.js: const IDS = [...]).
const IDS = ['av1', 'av2', 'aw1', 'aw2', 'ax1', 'ax2', 'ay1', 'ay2', 'az1', 'az2'];
const OWNED_ROUTES = ['home', 'round32-results', 'round32-subrounds', 'round32-roadmap',
  'round32-sources', 'round32-panel', 'round32-calculators', 'round32-figures',
  'drafts', 'research-network', 'hnm-findings', ...IDS.map(id => 'round32-' + id)];

const serverArgs = site === 'docs'
  ? ['scripts/preview_pages.py', '--port', String(port)]
  : ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', path.join(root, site)];
const server = spawn('python3', serverArgs, {cwd: root, stdio: 'ignore'});

function fileSha256(absPath) {
  return crypto.createHash('sha256').update(fs.readFileSync(absPath)).digest('hex');
}

function sourceHash(relPath) {
  const abs = path.join(root, relPath);
  if (!fs.existsSync(abs)) {
    if (finalRun) throw new Error('required source file is missing for --final verification: ' + relPath);
    return 'missing';
  }
  return fileSha256(abs);
}

let browser;
try {
  await new Promise(resolve => setTimeout(resolve, 500));
  browser = await chromium.launch({
    headless: true,
    executablePath: process.env.YM_CHROMIUM_EXECUTABLE || '/tmp/chromium',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--use-gl=angle',
      '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--disable-vulkan',
      '--no-zygote', '--single-process'],
  });
  const page = await browser.newPage({viewport: {width: 1440, height: 1100}, deviceScaleFactor: 1});
  const errors = [], checks = [];
  page.on('pageerror', error => errors.push(String(error)));

  const prefix = site === 'docs'
    ? JSON.parse(fs.readFileSync(path.join(root, 'docs/build-manifest.json'), 'utf8')).base
    : '/';
  const base = 'http://127.0.0.1:' + port + prefix;
  await page.goto(base);

  const snapshot = await page.evaluate(() => {
    const data = window.ROUND32_DATA;
    const nodes = data?.network?.nodes ?? [];
    return {
      completed: data?.progress?.completed,
      loops: (data?.loops ?? []).map(row => ({
        id: row.id, title: row.title, contribution_id: row.contribution_id,
        node_id: nodes.find(node => node.route === 'round32-' + row.id)?.id ?? null,
      })),
      sources: (data?.survey ?? []).length,
      calculators: (data?.calculators ?? []).length,
      figures: (data?.figures ?? []).length,
    };
  });
  assert.equal(typeof snapshot.completed, 'number', 'window.ROUND32_DATA.progress.completed must be a number');

  const bundleIncomplete = snapshot.completed < 10;
  if (bundleIncomplete && !allowIncomplete) {
    throw new Error('Round32 bundle reports ' + snapshot.completed +
      ' of 10 completed investigations; pass --allow-incomplete to run the smoke check.');
  }

  async function checkRoute(route) {
    await page.goto(base + '#research/' + route);
    assert.equal(await page.locator('h1').count(), 1, route);
    const heading = await page.locator('h1').textContent();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    assert(heading.trim(), route);
    assert(!overflow, 'mobile overflow ' + route);
    checks.push({route, heading: heading.trim(), mobileOverflow: overflow, method: 'navigated'});
  }

  assert.equal(await page.locator('h1').count(), 1);
  await page.screenshot({path: path.join(output, 'home-desktop.png'), fullPage: true});
  await page.setViewportSize({width: 390, height: 844});
  await page.screenshot({path: path.join(output, 'home-mobile.png'), fullPage: true});

  await checkRoute('home');

  if (bundleIncomplete) {
    // Smoke mode: only visit home (done above) and the preserved Round31 archive routes.
    await checkRoute('round31-results');
    await checkRoute('round31-at6');

    // Every Round32-owned route must show the incomplete-cycle sentence; checked
    // in-page via the exported render() function rather than by navigating to each.
    const rendered = await page.evaluate(routes =>
      routes.map(route => ({route, html: window.ResearchRound32.render(route)})), OWNED_ROUTES);
    for (const {route, html} of rendered) {
      assert(html.includes('No Round32 scientific findings are displayed.'),
        'incomplete-cycle sentence missing for ' + route);
      checks.push({route, sentencePresent: true, method: 'evaluated'});
    }
  } else {
    // Final mode: the cycle is complete; visit every route and exercise the interactions.
    const routes = ['drafts', 'round32-results', 'round32-subrounds', 'round32-roadmap',
      'round32-sources', 'round32-panel', 'round32-calculators', 'round32-figures',
      'hnm-findings', 'research-network', 'round31-results', 'round31-at6',
      ...snapshot.loops.map(row => 'round32-' + row.id)];
    for (const route of routes) await checkRoute(route);

    // Sources: search, area filter to a non-matching area, reset.
    await page.goto(base + '#research/round32-sources');
    await page.locator('#r32-source-search').fill('Newton');
    assert(await page.locator('.r32-source').count() > 0, 'source search for Newton must match at least one card');
    const nonMatchingArea = await page.evaluate(() => {
      const areas = [...document.querySelectorAll('#r32-source-area option')].map(o => o.value).filter(v => v !== 'all');
      return areas.find(area => window.ResearchRound32.filterSources('Newton', area).length === 0) ?? null;
    });
    assert(nonMatchingArea, 'no research lens without a Newton match was found');
    await page.locator('#r32-source-area').selectOption(nonMatchingArea);
    assert.equal(await page.locator('.r32-source').count(), 0);
    await page.locator('#r32-source-reset').click();
    assert.equal(await page.locator('.r32-source').count(), snapshot.sources);
    await page.screenshot({path: path.join(output, 'sources-mobile.png'), fullPage: true});

    // Findings: search by the first loop's contribution id, round filter, reset.
    await page.goto(base + '#research/hnm-findings');
    await page.locator('#r32-finding-search').fill(snapshot.loops[0].contribution_id);
    assert.equal(await page.locator('#r32-finding-cards article').count(), 1);
    await page.locator('#r32-finding-cards').screenshot({path: path.join(output, 'catalog-mobile.png')});
    await page.locator('#r32-finding-reset').click();
    await page.locator('#r32-finding-round').selectOption('32');
    assert.equal(await page.locator('#r32-finding-cards article').count(), snapshot.loops.length);

    // Network: search for a Round32 node id, select it, details become visible.
    await page.goto(base + '#research/research-network');
    const nodeId = snapshot.loops[0].node_id;
    assert(nodeId, 'no network node was found for the first Round32 loop');
    await page.locator('#r32-network-search').fill(nodeId);
    await page.locator(`#r32-network-catalog [data-r32-node="${nodeId}"]`).click();
    assert(await page.locator('#r32-network-details').isVisible());
    assert((await page.locator('#r32-network-details').textContent()).includes('Direct relations'));
    await page.locator('#r32-network-details').screenshot({path: path.join(output, 'network-mobile.png')});

    // First loop page.
    await page.goto(base + '#research/round32-' + snapshot.loops[0].id);
    await page.screenshot({path: path.join(output, 'result-mobile.png'), fullPage: true});

    // Sub-rounds page.
    await page.goto(base + '#research/round32-subrounds');
    await page.screenshot({path: path.join(output, 'subrounds-mobile.png'), fullPage: true});

    // Figures page: every image must actually load (non-empty naturalWidth).
    await page.goto(base + '#research/round32-figures');
    await page.evaluate(() => document.querySelectorAll('img[loading="lazy"]').forEach(img => { img.loading = 'eager'; }));
    await page.waitForFunction(() => [...document.images].every(img => img.complete));
    const widths = await page.locator('img').evaluateAll(imgs => imgs.map(img => img.naturalWidth));
    assert(widths.length > 0, 'the figures page has no images');
    assert(widths.every(width => width > 0), 'every figure image must report a non-empty naturalWidth');
    await page.screenshot({path: path.join(output, 'figures-mobile.png'), fullPage: true});

    // Calculators page: the recorded-values label when calculators exist.
    await page.goto(base + '#research/round32-calculators');
    if (snapshot.calculators > 0) {
      assert((await page.locator('body').textContent()).includes('Recorded exact values; not a live computation.'));
    }
  }

  assert.equal(errors.length, 0, errors.join('\n'));

  const sourcePaths = [
    'research/round32/presentation/build_site.py',
    'research/round32/advisor/findings.json',
    'research/round32/network.json',
    'research/round32/advisor/roadmap.json',
    'papers/round32-addendum/main.pdf',
    'tests/round32_browser.mjs',
    'tests/round32_site.mjs',
    'scripts/build_pages.py',
    'scripts/preview_pages.py',
  ];
  const perFolder = ['index.html', 'research-round32.js', 'research-round32.css',
    'research-round32-data.js', 'ym-round32-addendum.pdf', 'ym-round31-addendum.pdf', 'ym-draft-03.pdf'];
  for (const folder of ['dist', 'docs']) for (const name of perFolder) sourcePaths.push(folder + '/' + name);
  const source_sha256 = {};
  for (const relPath of sourcePaths) source_sha256[relPath] = sourceHash(relPath);

  const screenshot_sha256 = {};
  for (const name of fs.readdirSync(output)) {
    if (name.endsWith('.png')) screenshot_sha256[name] = fileSha256(path.join(output, name));
  }

  const receipt = {
    status: 'passed',
    mode: finalRun ? 'final_source_render' : 'smoke',
    date: new Date().toISOString(),
    site, port,
    viewports: [{width: 1440, height: 1100}, {width: 390, height: 844}],
    checkpoint: {completed: snapshot.completed},
    checks, pageErrors: errors,
    source_sha256, screenshot_sha256,
    visual_review: {status: 'pending_manual_inspection', screenshots_inspected: []},
    scope: bundleIncomplete
      ? 'Smoke check: home and the preserved Round31 archive routes render (one h1, no mobile overflow); every Round32-owned route, including all ten planned loop ids, was confirmed in-page to show the incomplete-cycle sentence. Interactions and loop pages are skipped until the bundle reports ten completed investigations.'
      : 'Real browser current/archive routes, mobile overflow, source/finding/network filter interactions, figure image loading and the calculator recorded-values label. Visual inspection of screenshots is recorded separately.',
  };
  fs.writeFileSync(path.join(output, 'site-qa.json'), JSON.stringify(receipt, null, 2) + '\n');
  console.log(JSON.stringify(receipt));
} finally {
  if (browser) await browser.close();
  server.kill();
}
