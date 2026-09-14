# Scrolling research journey: presentation validation

Scientific source release: `b96c1dc26a9860a27565d0e6d0668789d4244353` (approved PR #3).

The journey is a presentation of existing results. It creates no research gates and changes no files under `research/`. Its primary-source links bind the source release, while research route links lead to the full recorded reviews. Historical evidence inventories continue to describe their original releases.

`equation-and-route-checks.json` compares all 25 previously admitted forward M2 rational time/profile fixtures against the calculator in both `dist` and `docs` (50 comparisons, each checking all four terms, total, and the sufficient-window flag). Invalid endpoints and parameter values are rejected. Chapter targets, evidence boundaries, source/copy identity, and historical route delegation are checked. These calculations evaluate the published sufficient bound; they do not measure the actual correlation error.

`site-regression.json` records the existing static/local route, manifest, download, and capability tests. Both commands were also executed from a clean Git archive of the staged presentation tree. Rebuilding that archive left its published asset hashes unchanged.

The browser cannot reach this runtime's localhost (`ERR_BLOCKED_BY_CLIENT`); visual and interaction review therefore follows on the deployed public page. These automated JSON records do not claim browser or mobile visual coverage.

Reproduce:

```bash
npm run build
node tests/test_workbench.mjs
node tests/test_journey.mjs
```
