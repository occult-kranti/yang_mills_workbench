# Round32 presentation figures

Six deterministic matplotlib figures illustrating Round32 setups (geometry,
kernel comparison, and a planning-notes error-budget preview). **Every figure
here is presentation only and carries no admission weight.** None of them
computes, replays, or certifies an admitted result; each caption/footer says
so explicitly. They are built directly from fixed integer geometry (link and
face enumerations already frozen in the cited reports) and from decimal
previews already written into the Round32 advisor/skeptic record — nothing
here recomputes those previews or checks them against `fractions.Fraction`.

## Generate

```bash
python3 -B research/round32/figures/make_figures.py
```

This writes six `.png` (200 dpi) + `.svg` pairs into
`research/round32/figures/`, and byte-copies each `.png` into `dist/` under
the same filename. No arguments, no network access, no packages beyond
`matplotlib` and the standard library. The script prints a `sha256  path`
line for every file it writes; running it twice reproduces the same digests
(checked as part of this task — see below).

## Files

| File | Shows |
|---|---|
| `r32-coarse-factor.png/svg` | One coarse factor's 4×2×1 tail block (eight tail vertices `(4b_x+r, 2b_y+q, b_z)`, `r=0..3`, `q=0,1`), all 24 owned positive links, the ten selected-strip links (six x-links at `r=0,1,2` both `q`, four y-links at `q=0` all `r`) highlighted, and the three selected xy faces (`r=0,1,2` at `q=0..1`) shaded. Geometry: `research/round21/forward/i1/report.md` §1–2. |
| `r32-wilson-cover-stars.png/svg` | The cover `R={0,e_z}` (two coarse factors, drawn as translucent cubes), the four links of the original xz Wilson loop `W` at the fine origin drawn thick, and the seven incident anchor stars `b+S` (`S={0,e_x,e_y,e_z}`) drawn as translucent tetrahedra, with the anchor set `R−S={0,−e_x,−e_y,−e_z,e_z,e_z−e_x,e_z−e_y}` listed. Coarse-block positions are schematic (unit spacing), not fine-lattice scale. Geometry: `research/round32/skeptic/triage.md` (a). |
| `r32-window-vs-poisson.png/svg` | (a) The Poisson kernel `s/(π(s²+θ²))` and the window transform modulus `\|ĝ(θ)\| = (4s³/π)(s²+θ²)⁻²` at `s=1`, log-log. (b) The first-moment integrands `\|θ\|·kernel`: the Poisson tail `~1/θ` (log-divergent integral) versus the window's `~θ⁻³` decay (finite), annotated with `M₀=2`, `M₁=4s/π`. Kernel and window definitions: `research/round32/advisor/deliberation-2.md`. |
| `r32-error-budget.png/svg` | A horizontal dot chart (log x-axis) comparing four Round32 error-budget previews at `τ=1×10⁻⁸`, `s=1`: AT4 Poisson `L=10⁴` (state, centering, dynamics, tail), the optimized Poisson floor (dynamics+tail only, state suppressed to isolate the floor), window+crude tier (`D=2.37×10⁻⁵`), and window+exact tier (`D≈1.4×10⁻⁸`), each against the `10⁻⁶` target line. All values are explicitly labelled previews from the planning notes, not certified results. Source: `research/round32/advisor/deliberation-2.md`, `research/round32/skeptic/triage.md` (c)2. |
| `r32-link-flip-set.png/svg` | A 2×2×2 block of the fine lattice with the twelve unit links colored by membership in the link-flip set `E = {(p,x): p_y even} ∪ {(p,y): p_z even} ∪ {(p,z): p_x even}`, and the three faces (one per orientation) meeting at the origin vertex outlined and annotated with their `E`-count (3, odd — the sign-flip control). Source: `research/round32/advisor/deliberation-2.md`. |
| `r32-two-plaquette-graph.png/svg` | The Round11 two-plaquette graph: six vertices (`TL,TM,TR,BL,BM,BR`), seven links (`h1,h2,h3,h4,vL,vM,vR`) with the shared link `vM` highlighted. Captioned "a different finite model (AZ2), not the Z³ AQ family." Source: `research/round11/advisor/advisor.md` §1. |

## Determinism

The script pins the font family (bundled DejaVu Sans), sets a fixed
`svg.hashsalt` so SVG clip-path ids hash on content rather than Python object
identity, passes `metadata={'Date': None}` to every `savefig` call (PNG and
SVG), and seeds `random` defensively even though no figure uses a stochastic
element (every geometry is enumerated integer combinatorics; every kernel
curve is a closed-form evaluation). Each PNG that lands in `dist/` is a byte
copy of the PNG written under `research/round32/figures/`, not a second
render, so the two copies are identical by construction.

Verified for this task: running
`python3 -B research/round32/figures/make_figures.py` twice in the same
checkout produced byte-identical PNG and SVG output on both runs (sha256
digests matched for all eighteen files — six PNGs, six SVGs, and their six
`dist/` copies).

## Presentation-only statement

No figure in this directory computes an admission, replays a `check.py`, or
carries any evidentiary weight under `AGENTS.md`. Every figure's footer
states "Presentation only; no admission weight." and names its geometric or
numerical source in the Round32 or Round11/Round21 record. The error-budget
figure additionally labels its four rows as previews from the planning notes.
