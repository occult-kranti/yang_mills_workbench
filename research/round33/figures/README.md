# Round33 presentation figures

Five deterministic matplotlib figures illustrating Round33 experiment setups
and recorded values. **Every figure here is presentation only and carries no
admission weight.** None of them computes, replays or certifies an admitted
result; each footer and each caption says so explicitly.

Unlike the Round32 figures, no number is typed into the script. Every plotted
or printed value is read at run time from a file bound by the corresponding
Round33 gate, and the script first checks that the file's sha256 equals the
gate's binding. Where two bound records state the same value, the script
requires them to agree and stops otherwise: forward against reverse
producers, producer against skeptic review, and record against the gate's
accepted text. The one computation is a float preview of the BB2 item-5
bracket, evaluated in log10 space from the recorded exact constants and
formula so it can be drawn as a curve. The script requires that preview to
reproduce the recorded first exceedance of 2 (N=14419) and the recorded N=5
and N=10 bracket previews to relative 1e-5.

## Generate

```bash
python3 -B research/round33/figures/make_figures.py
```

This writes five `.png` (200 dpi) + `.svg` pairs into
`research/round33/figures/` and byte-copies each `.png` into `dist/` under
the same filename, which is where `research/round33/presentation/build_site.py`
expects the paths named in `research/round33/advisor/figures.json`. The script
also writes `research/round33/advisor/figures.json` (path, title, caption,
source_path, as in Round32), with each caption assembled from the same record
values and beginning "Presentation only; no admission weight.". No arguments,
no network access, and no packages beyond `matplotlib` and the standard
library. The script prints a `sha256  path` line for every file it writes.

## Files and sources

| File | Shows | Read from (all gate-bound) |
|---|---|---|
| `r33-boundary-sources.png/svg` | (a) An x–z slice (y=0) of the centered coarse cube Λ_N at N=3: the cover R={0,e_z}, the outer layer max\|b_i\|=N (source set of the F1-versus-F2 comparison) and the shell Λ_{N+1}∖Λ_N (source set of both nested comparisons), with the recorded l∞ distances from e_z (N−1 to the layer, N to the shell). (b) The exact source enumerations for N=2,3,4: F1 nested new faces (with new-star counts), F2 nested new faces, and the 28N(5N+1) extra F2 faces. | `forward/ba1/output/results.json` (checks `boundary_sources_enumerated`, `boundary_distance_exact`; `headline.comparisons`), `forward/ba2/output/results.json` (`headline.extra_faces`, cross-checked); BA1 and BA2 gates |
| `r33-rate-curves.png/svg` | (a) Against N (log x): the BB1 rate C q^(N−1), the BB2 whole-sequence bound C′ q^(N−1) and the BB2 item-5 bracket, with the certified O(1/N) range 5≤N≤14000 and the vacuous region from N=14419 shaded. (b) A zoom on 14388≤N≤14431 showing the region term overtaking the dynamics term, with the parity sawtooth of r_N=⌊(N−1)/2⌋. | `skeptic/bb1.json` and `skeptic/bb2.json` (`recommended_bound`), cross-checked against `forward/bb2/output/results.json` and against the BB1/BB2 gate text (exact constants, `r_N` rule, `5<=N<=14000`, `N=14418`, `N=14419`) |
| `r33-gauge-group-ledger.png/svg` | A table figure for G ∈ {SU(2), SU(3), SU(4), SU(5), U(1), Z2, SO(3)}: the central element acting as −1 on the Wilson representation, E[W²], E[W³], the exact first-order coefficient of ω(W)/τ, and the status of the link-flip lemma and the first-order parity theorem (✓ transfers / ✕ obstruction, with the exact nonzero obstruction coefficient). | `forward/bd1/output/results.json` (`transfer_ledger`, `headline.moment_table`), cross-checked against `reverse/bd1/output/results.json` (`centre`, `moment_table`, `first_order_coefficients`); the group list and coefficient order are parsed from the BD1 gate text |
| `r33-route-incidence.png/svg` | (a) The cover R with the seven whole stars that meet it and, in route B only, the two single-factor groups at the factors of R. (b) Faces meeting R and faces inside R per group at N=2: route A 82 meeting and 10 inside; route B 88 meeting and 16 inside (10 omitted + 6 selected). | `forward/bc2/output/results.json` (checks `route_b_incidence_on_R`, `route_b_first_order_R_marginal`; `cover`); BC2 gate text (cover, 21 omitted faces, 3 selected faces) |
| `r33-two-plaquette-couplings.png/svg` | (a) The Round11 two-square patch with independent couplings l₁, l₂ on its two faces, the shared link vM (C_shared) and the 1×2 loop z around both faces. (b) The exact coefficients of ⟨W₁⟩, ⟨z⟩ and ⟨C_shared⟩ through total order 4 with their parities. | Graph (vertices, links, squares) parsed from `forward/bd2/report.md`; coefficients and parities from `forward/bd2/output/results.json` (`headline`); BD2 gate text |

Paths in the table are relative to `research/round33/`.

## Determinism

The script pins the font family (bundled DejaVu Sans; SVG text as paths),
sets a fixed `svg.hashsalt`, passes `metadata={'Date': None}` to every
`savefig` call, and seeds `random` defensively (nothing stochastic is used).
Each PNG in `dist/` is a byte copy of the PNG under
`research/round33/figures/`, not a second render. Running the script twice in
the same checkout produced byte-identical output: the sha256 digests of all
sixteen written files (five PNGs, five SVGs, five `dist/` copies and
`advisor/figures.json`) matched.

## Palette

Colours follow the dataviz reference palette in light mode (categorical slots
1–5 on surface `#fcfcfb`). The palette validator passes every check. It warns
on contrast for the aqua, yellow and magenta slots, so every mark in these
figures also carries a visible text label or legend entry. Status colours
(good/critical, plus warning for the below-2 band) are used only for status
and always come with an icon or text label.

## Presentation-only statement

No figure in this directory computes an admission, replays a `check.py`, or
carries any evidentiary weight under `AGENTS.md`. Every figure's footer states
"Presentation only; no admission weight." and names the bound record it reads.
The rate-curve figure also labels its curves as float previews, not
certificates.
