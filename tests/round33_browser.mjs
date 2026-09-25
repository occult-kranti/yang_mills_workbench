/* Real browser QA against the Round33 site layer. Mirrors tests/round32_browser.mjs.
 * Round33 is a four-sub-round, eight-investigation cycle (three research sub-rounds
 * and an applications stage); while fewer than eight investigations are reviewed
 * the bundle is a placeholder and the renderer shows no scientific findings on any
 * Round33-owned route (see incomplete() in dist/research-round33.js).
 * --allow-incomplete permits running against such a bundle ("smoke mode"): only
 * home and the preserved Round32 archive routes (round32-results, round32-az2) are
 * navigated, and every Round33-owned route (including round33-applications and all
 * eight planned loop ids) is checked in-page for the incomplete-cycle sentence
 * instead. Without --allow-incomplete the bundle must report eight completed
 * investigations. --final marks the receipt as the authoritative source-render
 * verification and requires every listed source file to exist (a smoke run
 * tolerates and records 'missing').
 * Environment: YM_PLAYWRIGHT_MODULE, YM_CHROMIUM_EXECUTABLE, YM_QA_OUTPUT,
 * YM_SITE_FOLDER (docs or dist), YM_SITE_PORT.
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
const port = Number(process.env.YM_SITE_PORT || 8033);
const output = process.env.YM_QA_OUTPUT || '/tmp/yang-mills-round33-site-qa';
fs.mkdirSync(output, {recursive: true});

const allowIncomplete = process.argv.includes('--allow-incomplete');
const finalRun = process.argv.includes('--final');
if (finalRun && allowIncomplete) throw new Error('--final and --allow-incomplete are mutually exclusive');

// Fixed loop id order the renderer itself uses (dist/research-round33.js: const IDS = [...]).
const IDS = ['ba1', 'ba2', 'bb1', 'bb2', 'bc1', 'bc2', 'bd1', 'bd2'];
const REQUESTED = IDS.length;
const OWNED_ROUTES = ['home', 'round33-results', 'round33-subrounds', 'round33-roadmap',
  'round33-sources', 'round33-panel', 'round33-calculators', 'round33-figures', 'round33-applications',
  'drafts', 'research-network', 'hnm-findings', ...IDS.map(id => 'round33-' + id)];
const ARCHIVE_ROUTES = ['round32-results', 'round32-az2'];

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
  let sourceQueryUsed = null;
  page.on('pageerror', error => errors.push(String(error)));

  const prefix = site === 'docs'
    ? JSON.parse(fs.readFileSync(path.join(root, 'docs/build-manifest.json'), 'utf8')).base
    : '/';
  const base = 'http://127.0.0.1:' + port + prefix;
  await page.goto(base);

  const snapshot = await page.evaluate(() => {
    const data = window.ROUND33_DATA;
    const nodes = data?.network?.nodes ?? [];
    return {
      completed: data?.progress?.completed,
      placeholder: data?.placeholder === true,
      loops: (data?.loops ?? []).map(row => ({
        id: row.id, title: row.title, contribution_id: row.contribution_id,
        node_id: nodes.find(node => node.route === 'round33-' + row.id)?.id ?? null,
      })),
      sources: (data?.survey ?? []).length,
      calculators: (data?.calculators ?? []).length,
      figures: (data?.figures ?? []).length,
      applications: (data?.applications ?? []).length,
      round32Complete: window.ROUND32_DATA?.progress?.cycle_complete === true,
    };
  });
  assert.equal(typeof snapshot.completed, 'number', 'window.ROUND33_DATA.progress.completed must be a number');
  assert(snapshot.round32Complete, 'the preserved Round32 bundle must remain complete');

  const bundleIncomplete = snapshot.completed < REQUESTED;
  if (bundleIncomplete && !allowIncomplete) {
    throw new Error('Round33 bundle reports ' + snapshot.completed +
      ' of ' + REQUESTED + ' completed investigations; pass --allow-incomplete to run the smoke check.');
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

  async function checkArchive(route) {
    await checkRoute(route);
    const banner = await page.locator('.r33-current-banner').count();
    assert.equal(banner, 1, 'archived Round32 route must carry the Round33 archive banner: ' + route);
    const body = await page.locator('body').textContent();
    assert(!body.includes('No Round32 scientific findings are displayed.'), 'Round32 archive must remain complete: ' + route);
    checks[checks.length - 1].archiveBanner = true;
  }

  assert.equal(await page.locator('h1').count(), 1);
  await page.screenshot({path: path.join(output, 'home-desktop.png'), fullPage: true});
  await page.setViewportSize({width: 390, height: 844});
  await page.screenshot({path: path.join(output, 'home-mobile.png'), fullPage: true});

  await checkRoute('home');
  const navigation = await page.locator('nav[aria-label="Research navigation"] a[href$="#research/round32-results"]').count();
  assert.equal(navigation, 1, 'the Round33 navigation must link the Round32 archive');

  if (bundleIncomplete) {
    // Smoke mode: only visit home (done above) and the preserved Round32 archive routes.
    for (const route of ARCHIVE_ROUTES) await checkArchive(route);

    // Every Round33-owned route must show the incomplete-cycle sentence; checked
    // in-page via the exported render() function rather than by navigating to each.
    const rendered = await page.evaluate(routes =>
      routes.map(route => ({route, html: window.ResearchRound33.render(route)})), OWNED_ROUTES);
    for (const {route, html} of rendered) {
      assert(html.includes('No Round33 scientific findings are displayed.'),
        'incomplete-cycle sentence missing for ' + route);
      checks.push({route, sentencePresent: true, method: 'evaluated'});
    }
  } else {
    // Final mode: the cycle is complete; visit every route and exercise the interactions.
    const routes = ['drafts', 'round33-results', 'round33-subrounds', 'round33-roadmap',
      'round33-sources', 'round33-panel', 'round33-calculators', 'round33-figures', 'round33-applications',
      'hnm-findings', 'research-network', ...snapshot.loops.map(row => 'round33-' + row.id)];
    for (const route of routes) await checkRoute(route);
    for (const route of ARCHIVE_ROUTES) await checkArchive(route);

    // Sources: search, area filter to a non-matching area, reset. "Newton" is preferred
    // (as in Round32); when no Round33 source record mentions it, the query is a
    // recorded source id, which matches exactly one card, so another lens has none.
    await page.goto(base + '#research/round33-sources');
    const sourceQuery = await page.evaluate(() => {
      const R = window.ResearchRound33;
      const areas = [...document.querySelectorAll('#r33-source-area option')].map(o => o.value).filter(v => v !== 'all');
      const usable = term => R.filterSources(term).length > 0 && areas.some(area => R.filterSources(term, area).length === 0);
      return ['Newton', ...(window.ROUND33_DATA?.survey ?? []).map(row => String(row.id))].find(usable) ?? null;
    });
    assert(sourceQuery, 'no source search term matches a card while leaving a research lens empty');
    sourceQueryUsed = sourceQuery;
    await page.locator('#r33-source-search').fill(sourceQuery);
    assert(await page.locator('.r33-source').count() > 0, 'source search for ' + sourceQuery + ' must match at least one card');
    const nonMatchingArea = await page.evaluate(query => {
      const areas = [...document.querySelectorAll('#r33-source-area option')].map(o => o.value).filter(v => v !== 'all');
      return areas.find(area => window.ResearchRound33.filterSources(query, area).length === 0) ?? null;
    }, sourceQuery);
    assert(nonMatchingArea, 'no research lens without a match for ' + sourceQuery + ' was found');
    await page.locator('#r33-source-area').selectOption(nonMatchingArea);
    assert.equal(await page.locator('.r33-source').count(), 0);
    await page.locator('#r33-source-reset').click();
    assert.equal(await page.locator('.r33-source').count(), snapshot.sources);
    await page.screenshot({path: path.join(output, 'sources-mobile.png'), fullPage: true});

    // Findings: search by the first loop's contribution id, round filter, reset.
    await page.goto(base + '#research/hnm-findings');
    await page.locator('#r33-finding-search').fill(snapshot.loops[0].contribution_id);
    assert.equal(await page.locator('#r33-finding-cards article').count(), 1);
    await page.locator('#r33-finding-cards').screenshot({path: path.join(output, 'catalog-mobile.png')});
    await page.locator('#r33-finding-reset').click();
    await page.locator('#r33-finding-round').selectOption('33');
    assert.equal(await page.locator('#r33-finding-cards article').count(), snapshot.loops.length);

    // Network: search for a Round33 node id, select it, details become visible.
    await page.goto(base + '#research/research-network');
    const nodeId = snapshot.loops[0].node_id;
    assert(nodeId, 'no network node was found for the first Round33 loop');
    await page.locator('#r33-network-search').fill(nodeId);
    await page.locator(`#r33-network-catalog [data-r33-node="${nodeId}"]`).click();
    assert(await page.locator('#r33-network-details').isVisible());
    assert((await page.locator('#r33-network-details').textContent()).includes('Direct relations'));
    await page.locator('#r33-network-details').screenshot({path: path.join(output, 'network-mobile.png')});

    // First loop page.
    await page.goto(base + '#research/round33-' + snapshot.loops[0].id);
    await page.screenshot({path: path.join(output, 'result-mobile.png'), fullPage: true});

    // Sub-rounds page.
    await page.goto(base + '#research/round33-subrounds');
    await page.screenshot({path: path.join(output, 'subrounds-mobile.png'), fullPage: true});

    // Applications page: one card per recorded application, or the empty notice.
    await page.goto(base + '#research/round33-applications');
    const applicationCards = await page.locator('.r33-application-card').count();
    assert.equal(applicationCards, snapshot.applications, 'every recorded application must render a card');
    if (snapshot.applications === 0) {
      assert((await page.locator('body').textContent()).includes('No applications are recorded.'));
    }
    await page.screenshot({path: path.join(output, 'applications-mobile.png'), fullPage: true});

    // Figures page: every image must actually load (non-empty naturalWidth).
    await page.goto(base + '#research/round33-figures');
    await page.evaluate(() => document.querySelectorAll('img[loading="lazy"]').forEach(img => { img.loading = 'eager'; }));
    await page.waitForFunction(() => [...document.images].every(img => img.complete));
    const widths = await page.locator('img').evaluateAll(imgs => imgs.map(img => img.naturalWidth));
    if (snapshot.figures > 0) {
      assert(widths.length > 0, 'the figures page has no images');
      assert(widths.every(width => width > 0), 'every figure image must report a non-empty naturalWidth');
    }
    await page.screenshot({path: path.join(output, 'figures-mobile.png'), fullPage: true});

    // Calculators page: the recorded-values label when calculators exist.
    await page.goto(base + '#research/round33-calculators');
    if (snapshot.calculators > 0) {
      assert((await page.locator('body').textContent()).includes('Recorded exact values; not a live computation.'));
    }
  }

  assert.equal(errors.length, 0, errors.join('\n'));

  const sourcePaths = [
    'research/round33/presentation/build_site.py',
    'research/round33/advisor/findings.json',
    'research/round33/network.json',
    'research/round33/advisor/roadmap.json',
    'papers/round33-addendum/main.pdf',
    'tests/round33_browser.mjs',
    'tests/round33_site.mjs',
    'scripts/build_pages.py',
    'scripts/preview_pages.py',
  ];
  const perFolder = ['index.html', 'research-round33.js', 'research-round33.css',
    'research-round33-data.js', 'research-round32.js', 'research-round32-data.js',
    'ym-round33-addendum.pdf', 'ym-round32-addendum.pdf', 'ym-round31-addendum.pdf', 'ym-draft-03.pdf'];
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
    checkpoint: {completed: snapshot.completed, placeholder: snapshot.placeholder},
    checks, pageErrors: errors,
    ...(bundleIncomplete ? {} : {source_search_query: sourceQueryUsed}),
    source_sha256, screenshot_sha256,
    visual_review: {status: 'pending_manual_inspection', screenshots_inspected: []},
    scope: bundleIncomplete
      ? 'Smoke check: home and the preserved Round32 archive routes (round32-results, round32-az2) render (one h1, no mobile overflow, Round33 archive banner); every Round33-owned route, including round33-applications and all eight planned loop ids, was confirmed in-page to show the incomplete-cycle sentence. Interactions and loop pages are skipped until the bundle reports eight completed investigations.'
      : 'Real browser current/archive routes, mobile overflow, source/finding/network filter interactions, the applications page, figure image loading and the calculator recorded-values label. Visual inspection of screenshots is recorded separately.',
  };
  fs.writeFileSync(path.join(output, 'site-qa.json'), JSON.stringify(receipt, null, 2) + '\n');
  console.log(JSON.stringify(receipt));
} finally {
  if (browser) await browser.close();
  server.kill();
}
