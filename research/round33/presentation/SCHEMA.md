# Round33 presentation bundle schema (`hnm-round33-presentation-v1`)

`research/round33/presentation/build_site.py` builds `dist/research-round33-data.js`
(`window.ROUND33_DATA = {...}`) only from source-bound reviewed records. The renderer
`dist/research-round33.js` (plus `dist/research-round33.css`) is additive: it wraps the
existing `window.ResearchObservatory` exactly as `dist/research-round32.js` does, owns the
routes listed below, and delegates every other route to the prior renderer inside an
"Archived research view" banner. Tests: `tests/round33_site.mjs` (synthetic fixtures in
memory; real bundle/gate checks only when the bundle is complete or `--require-release`)
and `tests/round33_browser.mjs` (real browser; `--allow-incomplete` smoke mode, `--final`).

Builder flags: `--check` (validate and compare without writing), `--allow-incomplete`
(fewer than eight reviewed investigations; at zero it writes the placeholder bundle, and
while incomplete the network and roadmap may be absent), `--allow-missing-addendum`
(before `papers/round33-addendum/main.pdf` exists).

Placeholder bundle (0 reviewed investigations): `placeholder:true`, `progress.completed:0`,
empty `loops`, `subrounds`, `applications`, `network`, `survey`, `panel`, `calculators`,
`figures`, `registry.contributions`; `input_bindings` binds `advisor/findings.json` only. The
renderer shows "No Round33 scientific findings are displayed." on every Round33-owned route.

Top-level fields of a built bundle:

- `schema`: "hnm-round33-presentation-v1"; `author`: "Hruday N M (BUNZEEY)".
- `summary`, `scope_statement`: strings copied from `advisor/findings.json`.
- `progress`: {requested:8, completed:<n>, cycle_complete:<bool>, subrounds_completed:<n>}.
- `subrounds`: list of {id:1..4, title, goal_id, loops:[loop ids], selection_note_path, panel_update_path}
  (sub-rounds 1-3 are research sub-rounds; sub-round 4 is the applications stage).
- `loops`: list (in sequence order ba1, ba2, bb1, bb2, bc1, bc2, bd1, bd2) of {id, sequence, subround,
  title, stage:"reviewed", verdict, accepted, summary, model, limitations[], contribution_id,
  derivation_steps[], applications[] (text), producers:["forward","reverse"]|["forward"],
  direction:"paired"|"single+skeptic"|"statement+skeptic"|"statement-only" (must equal the frozen
  contract direction; paired iff two producers), gate_path, gate_sha256, reviewer_path, sources[], all_sources[]}.
- `applications`: optional list from `advisor/findings.json` `applications`, each
  {loop_id (a reviewed loop, normally bd1/bd2), problem, equation, outcome, model, kind?:"transfer"|"obstruction"|"partial"|"not_attempted",
  detail?, sources?[] (each that loop's gate file or a path the gate binds, i.e. an entry of the loop's all_sources)}; the builder adds gate_path, gate_sha256 and route.
  It lists the applications stage's labelled transfers, partial transfers and recorded obstructions, and, with kind "not_attempted" (rendered with a pending "Not attempted" badge), the planning candidates that no investigation ran; nothing is claimed for them.
- `roadmap`: contents of `advisor/roadmap.json` with a `goals` list (required when complete).
- `network`: contents of `research/round33/network.json` (required when complete; built by
  `research/round33/build_network.py` from Round32's 476-node network).
- `survey`: flattened expert source records (area = experts/<lens> directory name, ledger path,
  id, title, url, provenance, date, reading_depth, use, limits, passages[]).
- `panel`: {deliberation:[{loop:1..n, path, summary}] with n = 2 or 3 contiguous loops,
  updates:[{subround:1..4, lens (label), lenses[], assistants[], path, goal_changes}]}.
- `calculators`: list of recorded exact results the site may display as recorded values:
  {loop_id, title, gate_path, gate_sha256, source, result_path, formula_id, record:{...}, preview_only:true}.
  `advisor/calculators.json` entries may name `record_keys` (top-level fields of the bound result record) to select the displayed subset; the whole record stays bound by its gate.
- `figures`: list of {path (dist-relative), title, caption, source_path} for experiment-setup images (`advisor/figures.json`).
- `addendum`: {title, path, url, sha256, available}; preserved downloads `previous_draft`
  (Draft03), `round31_addendum`, `round32_addendum`: {path, url, title, sha256}.
- `registry`: inherited Draft03 registry plus additive aliases rebuilt from the gated Round31 and
  Round32 findings (round 31/32, routes to their archived pages) and the Round33 aliases (round 33).
  `registry_source` and `inherited_alias_sources` name the files.
- `input_bindings`: sha256 of every file read.

Routes owned by the Round33 renderer: home, round33, round33-results, round33-subrounds,
round33-roadmap, round33-sources, round33-panel, round33-calculators, round33-figures,
round33-applications, round33-<loop id>, drafts, research-network, hnm-findings. `round32-*`,
`round31-*` and older routes are archived views rendered by the prior renderers.
