# Round32 presentation bundle schema (`hnm-round32-presentation-v1`)

`research/round32/presentation/build_site.py` builds `dist/research-round32-data.js`
(`window.ROUND32_DATA = {...}`) only from source-bound reviewed records. The renderer
`dist/research-round32.js` (plus `dist/research-round32.css`) is additive: it wraps the
existing `window.ResearchObservatory` exactly as `dist/research-round31.js` does, owns the
routes listed below, and delegates every other route to the prior renderer inside an
"Archived research view" banner. Tests: `tests/round32_site.mjs` (synthetic fixtures in
memory; real bundle/gate checks only when the bundle exists or `--require-release`).

Top-level fields:

- `schema`: "hnm-round32-presentation-v1"; `author`: "Hruday N M (BUNZEEY)".
- `summary`, `scope_statement`: strings copied from `advisor/findings.json`.
- `progress`: {requested:10, completed:<n>, cycle_complete:<bool>, subrounds_completed:<n>}.
- `subrounds`: list of {id:1..5, title, goal_id, loops:[loop ids], selection_note_path, panel_update_path}.
- `loops`: list (in sequence order) of {id, sequence, subround, title, stage:"reviewed", verdict,
  accepted, summary, model, limitations[], contribution_id, derivation_steps[], applications[],
  producers:["forward","reverse"]|["forward"], direction:"paired"|"single+skeptic",
  gate_path, gate_sha256, reviewer_path, sources[], all_sources[]}.
- `roadmap`: contents of `advisor/roadmap.json` with a `goals` list.
- `network`: contents of `research/round32/network.json`.
- `survey`: flattened expert source records (area = experts/<lens> directory name, ledger path,
  id, title, url, provenance, date, reading_depth, use, limits, passages[]).
- `panel`: {deliberation:[{loop:1..3, path, summary}], updates:[{subround, lens, path}]}.
- `calculators`: list of recorded exact results the site may display as recorded values:
  {loop_id, title, gate_path, gate_sha256, source, result_path, record:{...}, preview_only:true}.
  The renderer shows recorded rationals verbatim and labels any floating preview as such.
- `figures`: list of {path (dist-relative), title, caption, source_path} for experiment-setup images.
- `addendum`: {path, url, title, sha256}; `previous_draft`: {path:"papers/draft-03/main.pdf", url:"ym-draft-03.pdf", title, sha256}; `round31_addendum`: {path, url, title, sha256}.
- `registry`: inherited Draft03 registry plus additive Round32 contribution aliases (round:32).
- `input_bindings`: sha256 of every file read.

Routes owned by the Round32 renderer: home, round32, round32-results, round32-subrounds,
round32-roadmap, round32-sources, round32-panel, round32-calculators, round32-figures,
round32-<loop id>, drafts, research-network, hnm-findings. `round31-*` and older routes are
archived views rendered by the prior renderer.
