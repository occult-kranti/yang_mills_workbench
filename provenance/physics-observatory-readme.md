# Physics Observatory

A separate localhost learning and research website, from arithmetic and measurement to quantum physics, relativity, electromagnetism, matter, particles, and interdisciplinary research.

## Start the website

1. Extract the ZIP.
2. Open a terminal in the extracted `physics-observatory` folder.
3. Run:

```bash
python3 start.py
```

On Windows, use:

```powershell
py -3 start.py
```

The launcher opens **http://127.0.0.1:8001/**. Keep the terminal open; press **Ctrl+C** to stop. Python **3.10 or newer** is required. The website itself needs no package installation, account, API key, build step, or paid model service. It uses a different default port from the earlier Learning Atlas.

If the browser does not open automatically, enter the address yourself. If port 8001 is occupied:

```bash
python3 start.py --port 8002
```

For a terminal-only launch: `python3 start.py --no-browser`. You can also open `dist/index.html` directly for offline reading and calculators; browser storage behavior for file URLs varies, and paper refresh requires the server.

## Included

| Component | Coverage |
|---|---|
| Curriculum | 108 chapters, 540 subchapters, 1,934 topic entries |
| Chapter detail | Prerequisites, five study steps, practice tasks, derivation, exercise, exit gate, misconception, sources, and related tools |
| Routes | 14 combined and focused study paths with prerequisite closure and adjustable study estimates |
| Historical reading | Newton, Einstein, and Tesla: contributions, primary works, archives, reading orders, access limits, and claim checks |
| Resources | 164 annotated textbooks, lecture/video courses, primary works, archives, and open-source projects |
| Projects | 28 detailed replication or learning briefs, including three runnable SciPy textbook benchmarks |
| Calculator laboratory | 29 offline tools with formulas, units, assumptions, numerical steps, and plots where useful |
| Research desk | 25 annotated papers checked on 7 September 2026; manual arXiv discovery across 33 categories |
| Patent research room | 311 Tesla catalogue entries, 28 patent dossiers, 12 Newton records, 10 modules / 30 lessons and 6 additional project briefs |
| Notebook | Chapter and subchapter completion, notes, paper and patent worksheets, subject/patent module gates, local persistence, JSON backup and restore |
| Advisor | Study sequencing, weekly planning, scientific evidence, reproducibility, and research readiness |

The chapter IDs are stable references, not a demand to finish every mathematics chapter before beginning physics. The displayed order introduces measurement and elementary mechanics early, then brings in advanced mathematics as needed. A focused route includes its required preparation; the combined route includes every chapter.

## Where to begin

- **Study:** choose “Start from the beginning,” attempt the first exit gates, and fill genuine gaps. Switch to a specialty after the foundations.
- **Paths:** compare the evidence each route asks you to produce. Hour ranges are planning estimates for selected study and practice, not guarantees of mastery.
- **Laboratory:** change an input, predict the effect, calculate, and inspect units and assumptions.
- **Projects:** select an official software tutorial or included textbook benchmark before attempting a recent-paper replication.
- **Papers:** read the method and limitation notes, check the original source, and save a worksheet in your own words.
- **Pioneers:** follow the reading order and record the edition, date, document identifier, and access status of each primary text.

## Calculator index

Kinematics; projectile motion; Newtonian gravity; circular orbit and escape scales; harmonic oscillator; Coulomb force; parallel-plate capacitor; Ohm’s law; RC charging; series RLC response; long-wire magnetic field; magnetic Lorentz force; Faraday induction; ideal transformer; thin lens; single-slit diffraction; ideal gas; thermal radiation; special relativity; Schwarzschild exterior; photon/photoelectric effect; de Broglie wavelength; infinite quantum well; radioactive decay.

Defining constants and measured constants are distinguished in the advisor. The values use the [NIST 2022 CODATA table](https://physics.nist.gov/cuu/Constants/Table/allascii.txt). Equations are linked to the relevant [OpenStax University Physics volumes](https://openstax.org/subjects/science). Floating-point output does not constitute an uncertainty estimate. These are explanatory models with stated physical domains, not professional instrument or equipment design tools.

## Run the optional scientific examples

The core website does not require NumPy, SciPy, or Matplotlib. These packages are needed only for the optional examples:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r examples/requirements.txt
python examples/reproduce.py --experiment all --output my-results
```

Windows activation uses `.venv\Scripts\Activate.ps1`; alternatively invoke `.venv\Scripts\python.exe` directly. See `examples/README.md` for each model and single-experiment commands.

The examples reuse `scipy.integrate.solve_ivp`, `scipy.linalg.eigh_tridiagonal`, and `scipy.sparse.linalg.expm_multiply`. Included `examples/verified-output/` contains CSV data, PNG figures, and recorded metrics from a successful run. These are **textbook numerical benchmarks**, not claims to reproduce the recent research papers.

## Research coverage and updates

The snapshot is a curated set of entry points. It is not every latest paper or a systematic review of all physics. It includes newer preprints and selected published anchors, with distinct submission, update, and journal dates. Annotations are based on source and abstract/metadata review; they do not certify full independent replication.

“Find recent submissions” requests up to eight records from one arXiv category, ordered by first submission date. The server caches a category for 15 minutes, spaces upstream requests by at least three seconds, and preserves cached records on refresh failure. A stale result displays its original retrieval timestamp. Changing category does not silently merge results from different categories.

arXiv is one discovery source. Coverage is incomplete across journals and fields, and a journal-reference field is not independently verified peer review. Follow the original paper, version history, publisher DOI, data, code, and corrections. No background polling or automatic refresh occurs.

The static annotations do not rewrite themselves when a paper changes. To update them, edit `research_catalogue.py`, verify the sources, update the snapshot date and advisor text, and rebuild:

```bash
python3 content.py
```

The generated data are `dist/content.js` and `dist/content.json`. The rebuild validates counts, references, prerequisites, and route closure. Restarting the server is not necessary after rebuilding; reload the page.

## Historical scope

The Newton, Einstein, and Tesla sections are guides to major works and routes into the wider surviving corpora. They do not reproduce every work. Some documents are incomplete, lost, not digitized, untranslated, restricted, or paywalled. Catalogue records are not equivalent to readable papers or inventions. The Einstein digital edition’s access arrangements were changing at the research date; the relevant note links to the current publisher and archive pages.

Full texts and third-party software are linked, not bundled. Read each resource’s access and reuse notes. A patent claim, historical proposal, modern simulation, and independently measured performance are treated as different kinds of evidence.

## Keep your work

The notebook is stored in browser local storage under `physics-observatory-v1`. Export a JSON backup regularly. Clearing site data, changing browser/profile, or moving between `localhost` and `127.0.0.1` can show a different notebook. Use the same address consistently. Import validates the file and asks before replacing the current notebook.

The server listens on `127.0.0.1`, not the local network. It serves only `dist/` and an allowlisted arXiv metadata endpoint. It makes no AI service calls and sends no study notes upstream. Its optional paper cache is `data/paper-cache.json`; deleting that cache does not delete browser notes.

## Validation and limits

Verified in this build:

- All 108 chapters, five subchapters each, resource/tool references, prerequisite ordering, and route closure.
- All sixteen view-render functions, 108 chapter dialogs, 25 paper worksheets, 29 calculator forms, filters, note persistence, escaping, and mocked refresh states using a minimal DOM stand-in.
- Calculator analytic values, unit conversion examples, singular inputs, weak-field/low-speed limits, quantum-density normalization, and plotted geometry.
- Seven server/client tests for metadata parsing, allowlisting, timestamps, cache fallback, rate spacing, and loopback-origin handling.
- All three SciPy examples, including infinite-well grid-convergence checks; generated plots were inspected.

Run the checks with Python and Node.js installed:

```bash
python3 content.py
python3 -m unittest -v test_server.py
node dist/test_calculators.mjs
node tests/test_ui.mjs
```

Browser visual/accessibility/end-to-end testing and an actual live arXiv refresh were not performed. The refresh client was verified with mocked feeds and failures. Upstream availability and machine-specific installation remain environment-dependent.

## Source layout

| Path | Purpose |
|---|---|
| `start.py` | Standard-library localhost server and arXiv client |
| `dist/` | Offline HTML, CSS, JavaScript, generated curriculum data |
| `content.py` | Resource catalogue, prerequisite sequencing, validation, and data builder |
| `curriculum/` | Detailed chapter source |
| `learning_program.py` | Routes, projects, historical guides, and advisor |
| `research_catalogue.py` | Dated paper annotations and discovery categories |
| `examples/` | Optional SciPy programs and verified outputs |
| `test_server.py`, `tests/`, `dist/test_calculators.mjs` | Reproducible verification |
| `READING_LEDGER.md` | Reusable primary-source and paper-reading template |

The interface is deliberately framework-free and works without a CDN. Substantial numerical projects point to established scientific libraries instead of embedding replacement solvers.


## Dedicated subject rooms · 7 September 2026 expansion

Open **Explore** for seven pages: `#sound`, `#geometry`, `#sacred-geometry`,
`#astrophysics`, `#astronomy`, `#newton-esoteric`, and `#tesla-esoteric`.
Each includes six modules, eighteen lessons with practice, two projects, a source
reading guide, evidence assessments, and links to relevant core chapters.

The expansion adds 42 modules, 126 lessons, 14 project briefs, 35 annotated
resources, and five calculators. Original chapters and paths retain their IDs.
Progress files remain version 1: older backups import with empty subject progress;
new backups include subject gates, lesson completion, and subject notes. Notes
remain in the browser and are not automatically synchronized between devices.

Calculator additions: acoustic beats and tube fundamentals, regular polygons,
golden rectangles, parallax/astrometry, and stellar luminosity/temperature scaling.
Geometric plots preserve equal scale on both axes. Physical assumptions and input
limits are displayed with each tool. No audio playback or new external scripts
are loaded by these calculators.

Source data lives in `specialisms.py`. Rebuild with `python content.py` and
`node scripts/build-hosted.mjs`. Additional verification: `node tests/test_expansion_tools.mjs`.
The historical pages distinguish primary transcriptions, correspondent reports,
retrospective autobiography, scholarly interpretation, and unresolved quotation
attribution. Cultural meanings are described in context; physical effects need
independent empirical evidence. These are selected guided routes, not complete
editions of all historical works or an exhaustive literature collection.


## Patent research room · reviewed 8 September 2026

Open **Patents** in the navigation, or `#patents/dossiers`. The five views cover
patent studies, the searchable Tesla catalogue, Newton archive records, a sequenced
research plan, and evidence/connection notes. Theme filters include magnetism,
electrostatics, radiant energy, resonance, scalar claims, orgone, radionics,
gravity claims, sound and perception. Catalogue results are paginated and retain
historical jurisdictions and source dates. Worksheets and module gates save in
this browser and are included in Export backup. Existing version-1 backups remain
compatible and acquire empty patent fields on import.

The inventory reproduces all **311 numbered entries in the museum-hosted 2019
catalogue**: 112 US and 199 foreign. This is not a worldwide patent census or a
count of distinct inventions. Twelve Tesla specifications receive detailed study;
other rows are metadata. Corrections, a reissue, missing dates, and a summary-count
discrepancy are visible. The museum PDF is linked rather than bundled.

No invention patent naming Isaac Newton (1642–1727) as inventor was verified in
this bounded review. The Newton archive records include royal appointment and
privilege documents called patents, as well as scientific, alchemical, geometric
and theological writings. Further historical register searches remain an explicit
research task. Later inventors, citations and thematic comparisons are identified
separately from Tesla or Newton authorship.

Patent disclosures are distinguished from independent experimental evidence.
NASA's cited 2004 capacitor tests retain their apparatus/medium limitations;
exceptional claims without independent confirmation in this review are labeled
accordingly. Projects are proposed source audits, simulations and analysis plans,
not claims of completed device replications. Existing calculators and established
open-source scientific tools supply the computational foundations.

Edit `patent_archive.py`, `patent_learning.py` and `data/tesla-patent-index.json`,
then run `python3 content.py` and the hosted build. The patent review date is
separate from the existing September 7 research-paper snapshot.
