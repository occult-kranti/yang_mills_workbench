# Six-loop Yang–Mills study

[Open the published research home](https://occult-kranti.github.io/yang_mills_workbench/#research) · [GitHub source repository](https://github.com/occult-kranti/yang_mills_workbench)

This cycle uses three scientific roles: an advisor–skeptic, a forward researcher and an independent backward researcher. There are six scientific loops, A1/A2/B1/B2/C1/C2, plus two advisory decisions. The second decision revises B and C after both A loops. Each second scientific loop is selected after its first accepted gate. The actual decision chain, conventional derivations, exact computations, rejected shortcuts and source-bound evidence remain available.

The work concerns restricted lattice and conditional integration problems. It does not solve four-dimensional quantum Yang–Mills existence and the mass gap. No mathematical novelty relative to the wider literature is claimed for these applications of representation theory, min–max and finite tensor methods.

## Physical and static contracts

The Hamiltonian branch uses the untruncated gauge-invariant SU(2) link Hilbert space on finite open cubic graphs, normalized link Haar measure, Casimir j(j+1), Gauss law at every vertex and no external charges:

\[
H=\alpha\sum_e C_e-\sum_p\lambda_p x_p,
\qquad x_p=\tfrac12\operatorname{Tr}U_p,\quad\alpha>0.
\]

The coefficients α and λ have physical energy units. A common dimensionless lower bound yields a common physical bound under the additional family condition α≥α_min>0. Static Euclidean coefficients κ enter a different measure and are not identified with λ/α without a matching theorem.

A1 derives the diagonal local estimate but refutes extending its pure relative form bound to the vacuum-offdiagonal magnetic term. A2 establishes

\[
\Delta_{\rm physical}\ge\alpha_{\min}(3/4-\rho)>0
\]

for pairwise link-disjoint nonzero plaquette supports and max|λ_p|/α≤ρ<3/4. Shared vertices are allowed. The full link space factors; the physical space is not presumed to factor. The proof first includes the unique product ground in the Gauss sector. The dense overlapping family remains outside this result.

B1 studies the dense eleven-face two-cube graph. Withδ=3α, L=Σ|λ_p| and Q=Σλ_p², the twelve-state trial gives

\[
\Delta_{\rm physical}\ge\frac{\delta+\sqrt{\delta^2+Q}}2-L.
\]

For equal coupling magnitudes this is positive for |λ|/α<12/43. The bound at3/11 exceeds0.0666989α. B2 keeps λ_p/α=12/43 fixed and adds the shared-face ordinary adjoint character to the trial. Its exact rational amplitudeη=3/3817 yields

\[
\Delta_{\rm physical}\ge\alpha\frac{1388}{284767457}>0.
\]

The full positive trial-amplitude interval is0<η<6/3817. The selected amplitude maximizes the quadratic numerator, not the entire quotient. Both B results combine an actual Rayleigh upper bound for E₀ with a separate full-operator lower bound for E₁. A trial-matrix gap is never used as a full-gap lower bound.

C1 separates the18-vertex/33-link/20-face four-cube complex from its18-vertex/32-link/16-face outer boundary. The full central four-adjoint Haar tensor has rank three; its tetrahedral conditional contraction is−1/405, while omitting cross-channel terms incorrectly gives+2/405.

C2 introduces the action vectorb=Σκ_i a_i and keeps its explicit zero branch. Atκ_i=1/8, tetrahedral and commuting boundaries have the sameb=(1/4,0,0,0) and partition function, but their joint expectations differ. The rigorous difference lies within the outward-rounded display interval

\[
D\in[0.013207249650566427,\ 0.013207249650566428].
\]

The exact fraction endpoints in `forward/c2/output/collection.json` define a much narrower enclosure, width approximately6.63×10⁻²⁵. Degrees0,4,8 are retained as insufficient for the requested10⁻¹² precision;12 and16 pass. The explicit nonzero-coefficientb=0 fixture reduces to the exact Haar result. Relative observable directions are necessary in addition tob. Their surrounding marginal integration is a separate bulk obligation.

## Launch the current website

From the full repository root:

```bash
python3 start.py --no-browser
```

Visit [localhost:8001](http://127.0.0.1:8001/#research). Windows: `py -3 start.py`. Use `--port 8002` if needed. The website and recorded plots need no API key. GitHub Pages serves the saved research; Python simulations and exact experiments run locally. Progress and notes are stored in your browser.

The research ZIP contains this round's reproducible evidence. Obtain the full website launcher and historical tools by cloning or downloading the GitHub repository. The ZIP does not duplicate the entire historical site.

## Reproduce the six loops

Use Python3.11 or newer. Exact calculations use standard-library rational arithmetic; any optional matrix or plotting dependency is stated in the corresponding source. For figures install Matplotlib. The C1 raw complex-matrix diagnostic also uses standard Python floating arithmetic; its last-bit residual can be platform-sensitive even when the exact tensor is unchanged. Exact semantic replay is intentionally strict and reports such differences for inspection. The full repository's `requirements.txt` covers the wider historical simulation tools.

From the repository root:

```bash
python3 research/round17/reproduce.py --output /absolute/path/to/new-results
python3 research/round17/reproduce.py --optimized --output /absolute/path/to/another-new-results
```

From an extracted research ZIP, use `python3 round17/reproduce.py` with the same output arguments. Output directories must be new and outside the accepted Round17 tree. The runner checks the six source-bound gates, copies the frozen sources, executes all six producer programs, six independent programs and six focused comparisons, then compares the semantic outputs with the accepted records. Normal and optimized Python repeat the same checks and are counted once.

Each loop can also be run directly:

```bash
python3 research/round17/forward/a2/check.py --output /absolute/path/to/new-a2-results
python3 research/round17/backward/a2/check.py --output /absolute/path/to/new-independent-a2
```

The same pattern applies to a1, b1, b2, c1 and c2. Read the loop report before choosing new parameters; implementation caps and unsupported cases are explicit. Uncomputed or insufficient cases must not appear as successful zero residuals.

## Replay the bidirectional proof dependencies

```bash
python3 research/round17/proof_routes.py --output /absolute/path/to/new-proof.json
```

The adapter freezes the reviewed bytes, reruns the independent scientific programs and their producer comparisons in fresh processes, and performs a real two-front search through the reviewed finite implications. A separate ordered replay checks every proved route. Withdrawal cases remove required support, physical scale, operator, trial or tensor evidence. Dense overlap, full bulk integration and continuum prerequisites remain unseeded. A backward requirement is not evidence that its premise is true.

This is an auditable conventional proof planner, not a formal proof-assistant kernel. A successful search validates the dependency route only under its declared mathematical contracts and reviewed derivations.

## Review and source records

`advisor/revised-plan.md` records the initial three-goal contract. `advisor/post-a-roadmap.md` is the actual second advisory decision. `advisor/*-contract.md` fixes each loop; `advisor/*-gate.json` binds its complete accepted evidence and the preceding gate. `advisor/feedback-log.md` retains decisions and defects. The forward and backward folders contain separate derivations and implementations. `next-roadmap.md` preserves the original unsolved obligations.

The graph-coordinate Boolean alias, unbounded mask-materialization issue, nested cache aliases and direct scalar-helper validation omissions are preserved with the original sources and recorded outcomes. Review scope covers new scientific files, their mathematical domains, required comparisons and affected website/proof integration. It is not a claim that every line of every historical project was newly audited. Agent reviews are not credentialed human peer review.

The primary-source audit is in `advisor/source-audit.md`. It distinguishes an explicit qubit/two-site stability constant from a broader rotor-relevant theorem with numerical constants not reconstructed here. The [Clay problem statement](https://www.claymath.org/millennium/yang-mills-the-maths-gap/) remains the boundary for the continuum target.

## Rebuild the evidence dashboard

After all scientific and independent integration gates pass, from the repository root:

```bash
python3 research/round17/build_report.py
python3 research/round17/build_site_data.py
python3 research/round17/plot_figures.py
python3 research/round17/package_review.py
python3 scripts/build_pages.py
node tests/test_six_ui.mjs
node tests/test_workbench.mjs
python3 tests/test_local_launch.py
```

The six scientific gates contain255 producer checks,243 independent checks and106 separate comparison checks. The repeated optimized runs are not counted again. The independent integration review passes62 additional named gates across18 dependency routes: six proved, nine required-premise withdrawals and three open targets. Its ordinary/optimized records are under `backward/integration/`. Reproduce that bounded audit with `python3 research/round17/backward/integration/check.py --round-dir research/round17 --output /absolute/path/to/new-integration-review`.

The proof adapter also records a corrected future implication: a local estimate must be paired with an applicable stability theorem and a satisfied smallness condition.

Charts use saved exact data converted only for display, with downloadable CSV files and standalone figures. The pages provide plain and technical explanations, the three-role roadmap, derivations and review documents. Routing, document behavior, data binding and local HTTP checks are separate from scientific acceptance. Real-browser visual layout and keyboard testing remain unverified.
