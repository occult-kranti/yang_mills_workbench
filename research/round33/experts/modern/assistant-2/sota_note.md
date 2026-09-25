# BB1/BB2 relative to the literature this lens already reads (advisory note)

Round33 sub-round 2, modern (Penrose/Feynman) lens, research assistant/coder
"assistant-2". **This file is advisory. It counts zero research loops,
admits nothing, and is not a contract, a premise or a gate.** Every source
cited below is already recorded in
`research/round33/experts/modern/sources.json` (with its own
`reading_depth`, honestly stated) or is the committed excerpt
`research/round33/sources/nachtergaele-sims-1410.8174v1.md`; nothing new was
fetched to write this note, per instruction. No claim of scientific
priority is made anywhere in this file, matching every BB1/BB2 report's own
exclusion list.

## 1. Marginal locality (BB1) against boundary-decay-of-perturbed-ground-states results

BB1 proves, by two independent routes (polymer/Kotecky-Preiss and an
iterated product-ordering split with per-site charging), that the reduced
density of the finite-box ground vector on the fixed cover `R={0,e_z}`
depends on the choice between two *named* boundary prescriptions (F1, F2,
and their nested/nested-and-translated volumes) by at most `C q^(N-1)`,
`q=1/64`, `C<=1/250000` — both routes independently reproduce headline
values around `8.90e-7`, roughly `4.49x` inside that target (this folder's
`bb1_arb.py`). This is exactly the shape of a **boundary-condition-decay**
result for a weakly perturbed reference state, which is the closest
external theorem this lens has on file:

- **`r33-yarotsky-jsp2005`** (D. A. Yarotsky, *Uniqueness of the Ground
  State in Weak Perturbations of Non-Interacting Gapped Quantum Lattice
  Systems*, J. Stat. Phys. 118 (2005)): "In finite volume the dependence of
  the ground state of a weak perturbation of a non-interacting gapped
  system on the boundary condition decays exponentially with the distance
  to the boundary, implying uniqueness of the infinite-volume ground
  state." Recorded `reading_depth: search summary only` — the full text was
  never read (a login gate; see `access_failures` in `sources.json`), so no
  hypothesis-by-hypothesis comparison is possible here. Two things are
  nonetheless clear from the summary alone: (a) BB1's target quantity
  (trace-norm distance of *reduced densities on a fixed finite region*
  between two named finite-box constructions, at a fixed lattice spacing)
  is the same *kind* of object as Yarotsky's boundary-decay statement; (b)
  BB1's conclusion is deliberately narrower — locality of two *named*
  construction families, never "every boundary condition" and never
  "uniqueness of the infinite-volume ground state" (both explicitly
  excluded by the BB1 contract's `claim_exclusions` and by the
  `named_construction_not_uniqueness` control). Whether AM2's unbounded
  on-site Casimir terms even fall inside Yarotsky's stated hypotheses
  (bounded on-site dimension is typical in this literature) is exactly the
  `unresolved` note already recorded against this source in `sources.json`
  and remains unresolved here; **this is a reading request, not a claim**
  (Section 3 below).

- **`r33-kotecky-encyclopedia-cluster-expansion`** (R. Kotecky, *Cluster
  Expansion*, Encyclopedia of Mathematical Physics, 2006): already flagged
  in this lens's own `bb-targets-proposal.md` as "the exact template" for a
  polymer-gas route to marginal locality, with its boundary-decay estimate
  (49), `|<Psi>-<Psi>_Lambda| <= |S| K^{-dist(S,Lambda^c)}` under a
  Dobrushin-type condition. The forward BB1 producer's own machinery —
  hard-core polymers built from AM2 creation vectors, an activity bound
  `|w(gamma)|<=prod||c_K||`, an exploration-tree combinatorial majorant
  (Lemma 4.1/4.2), and a Kotecky-Preiss-form convergence condition with an
  explicit `a`, `d(.)` (Proposition 6.2) — is structurally the same family
  of argument as this encyclopedia article's Section 2-3 machinery, applied
  to the AM2 creation algebra rather than a classical polymer gas. This
  transfer (classical hard-core-polymer combinatorics to a quantum creation
  expansion) is exactly what `sources.json` already flagged as needed
  ("the quantum polymer representation... must be derived for the AM2
  creation algebra; no constant transfers"); the forward report does derive
  it (report.md Sections 3-6), and `kp_condition.py` in this folder gives
  one further, freshly-coded finite-graph confirmation of the same
  exploration-tree combinatorial fact (Lemma 4.1's max-path/`sigma^2`
  bound) on an instance distinct from either producer's own fixtures.

- **`r33-kotecky-preiss-cmp1986`** and **`r33-ueltschi-math-ph-0304003`**
  are the two sources the forward report itself cites for Theorem 6.1 (the
  abstract Kotecky-Preiss cluster-expansion conclusion). Both are recorded
  here at `reading_depth: metadata only` / `abstract` respectively — no
  deeper than the forward report's own stated depth ("cited, not re-proved
  and not machine-checked; the primary sources were not re-inspected in
  this session"). `kp_condition.py` records this explicitly: the forward
  report is self-contained on **Proposition 6.2** (verifying that its own
  choice of `a(gamma)`, `d(gamma)` meets Theorem 6.1's hypothesis, proved
  in full from the report's own Lemma 4.2) but not on **Theorem 6.1**
  itself, which remains a citation with no committed excerpt anywhere in
  this round (unlike Nachtergaele-Sims, which *is* committed at
  `research/round33/sources/nachtergaele-sims-1410.8174v1.md`).

- **`r33-fernandez-procacci-math-ph-0605041`** (a tree-graph/Penrose-identity
  sharpening of Kotecky-Preiss and Dobrushin, abstract only): flagged in
  `sources.json` as a possible way to enlarge the admissible KP parameter
  range and so, in principle, reach a smaller `q` than `1/64`. Nothing in
  BB1 uses it; it remains background only, at the depth already recorded.

- **`r33-kennedy-tasaki-cmp1992`** and the two Datta-Fernandez-Froehlich
  papers (**`r33-datta-fernandez-froehlich-jsp1996`**,
  **`r33-dffrb-hpa1996`**) are recorded as `search summary only` background
  for convergent ground-state expansions around a product/diagonal
  reference — the same genre as AM2's creation expansion around the Haar
  vacuum, but not read deeply enough here to say more than that they share
  a genre.

## 2. Whole-sequence convergence and correlation functions (BB2) against Lieb-Robinson / clustering results

BB2 items 1-3 (whole-sequence Cauchy estimate without compactness, one
common limit, identification with every AQ1/F2 subsequential limit) are a
completeness-of-the-trace-class argument built entirely on BB1's own
(frozen-target, `conditional_on_bb1_targets`) locality bound — nothing
external beyond BA1/AQ1/AQ2/AY1 enters there, so there is no separate
literature comparison to make for those items beyond what BA1's own
sub-round already covers.

BB2 item 5 (correlation functions on the compact window `|theta|<=8`, rate
`O(1/N)`) inherits its dynamics constants unchanged from the BA2 gate,
which in turn rests on the **committed excerpt**
`research/round33/sources/nachtergaele-sims-1410.8174v1.md` — Theorem 3.1
(the Lieb-Robinson bound (51)-(53) with the interaction-picture proof
handling the unbounded on-site `H_x`) and Theorem 4.1 (the norm-limit
existence of `tau_t`, quoted verbatim in both BB2 reports). `bb2_constants.py`
in this folder reproduces `C_dyn` exactly from the BA2 gate's `K_F1`,
`K_cmp` and (reverse route) `K'_F2` values, and independently re-confirms
with Arb/mpmath that the reverse route's rational bound `E_up(y)` dominates
the true `E(y)=2(e^y-1-y)/y^2` at its working point (matching the ~7e-13 gap
the BA2 reverse report itself records).

The genuinely relevant literature-scope point, already on file and worth
restating here because it is the one place BB2 could be mis-read as
stronger than it is: this project's Lieb-Robinson-type function is
`F(r)=(1+r)^-4`, a **polynomial**, not an exponentially decaying kernel.
The Nachtergaele-Sims excerpt's own exponential-clustering strengthening
((53) in the committed excerpt, and separately
**`r33-nachtergaele-sims-math-ph-0506030`**'s Theorem 2, exponential
clustering from a spectral gap) requires an *exponentially weighted* norm
`F_a(r)=e^{-ar}F(r)` for some `a>0` — a hypothesis this project's admitted
`F(r)=(1+r)^-4` interaction norm does not, by itself, satisfy. BB2's own
`lieb_robinson_polynomial_tail` control exists for exactly this reason: it
rejects any claim of exponential decay in `N` with this polynomial `F`, and
both BB2 reports state the `O(1/N)` rate as the "honest" rate for a
polynomial Lieb-Robinson function. **`r33-hastings-koma-math-ph-0507008`**
(exponential decay of ground-state correlations from a spectral gap,
abstract only) and the broader survey
**`r33-nachtergaele-sims-1004.2086`** and
**`r33-nachtergaele-ogata-sims-jsp2006`** (search summary only) are the
companion results that *would* give an exponential rate under that
stronger hypothesis; none of them is used, or needed, by BB2's own
`O(1/N)` claim, and none is contradicted by it.

## 3. Reading requests (not fetched here; genuinely needed for a deeper comparison)

Per instruction, no new source was fetched for this note. If the project
wants a real hypothesis-level (not genre-level) comparison of BB1/BB2
against the closest external theorems, the following would need to be read
in full and, ideally, committed as excerpts the way the Nachtergaele-Sims
Theorem 3.1/4.1 excerpt already is:

1. **Yarotsky, J. Stat. Phys. 118 (2005), full text** (`r33-yarotsky-jsp2005`,
   currently a login-gated publisher page; `access_failures` records the
   gate). Needed to check whether its uniform-in-boundary-condition
   exponential-decay theorem's hypotheses (in particular, any bound on
   on-site Hilbert-space dimension) apply to AM2's unbounded on-site
   Casimir operators `h_b`, and to compare its rate and constant structure
   against BB1's `q=1/64`, `C<=1/250000` on the two named families.
2. **Kotecky-Preiss, Comm. Math. Phys. 103 (1986) 491-498, full text**
   (`r33-kotecky-preiss-cmp1986`, currently `metadata only`: the Project
   Euclid page displayed no abstract), and **Ueltschi, Moscow Math. J. 4
   (2004) 511-522, full text** (`r33-ueltschi-math-ph-0304003`, currently
   `abstract` only). Needed so that BB1 forward's Theorem 6.1 citation
   could eventually rest on a committed excerpt of the actual criterion and
   proof, rather than on the Kotecky encyclopedia article's later
   restatement plus "transcribed as known to this producer" (report.md's
   own words).
3. **Datta-Fernandez-Froehlich I and II, J. Stat. Phys. 84 (1996) /
   Helv. Phys. Acta 69 (1996), full text** (`r33-datta-fernandez-froehlich-jsp1996`,
   `r33-dffrb-hpa1996`, both `search summary only`), if a genuine
   contour/cluster-expansion comparison for BB2's whole-sequence-convergence
   argument (as opposed to BB2's own trace-class-completeness argument,
   which needs no such comparison to stand) were ever wanted.

None of these is fetched here; each is listed only as a concrete next
reading step, not acted on. This note carries no premise weight and
changes no verdict.
