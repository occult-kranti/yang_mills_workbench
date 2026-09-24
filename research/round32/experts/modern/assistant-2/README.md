# Round32 sub-round 2 -- modern (Penrose/Feynman) lens, assistant-2

Status: assistant/coder cross-check tools, per `loop3-signoff.md` section 3
and `update-1.md` section 7 (this sub-round's proposed tests). **These
outputs count zero research loops.** They are previews and cross-checks
only: python-flint 0.9 (Arb) and mpmath (via assistant-1's
`flint_harness.py`) are independent open-source rigorous/high-precision
libraries used here for comparison, never for admission. Every number this
repository actually admits is decided by exact `fractions.Fraction`
arithmetic in a frozen `check.py` inside `forward/`, `reverse/` or
`skeptic/`; nothing in this directory is imported by any of those, and
nothing here changes a verdict.

Human project author: Hruday N M (BUNZEEY). Run everything with `python3 -B`.

## Files

- `parity_theorem_exact.py` -- an exact-`Fraction` re-derivation of AW1's
  parity theorem item 1 (`report.md` equations F04/F05/F06 and item 3),
  using SU(2) tensor-power trivial multiplicities (three independent exact
  routes: Clebsch-Gordan recursion, a Catalan/binomial closed form, and a
  free-link Haar cross-check via the S^3 moment formula
  `E[q_0^{2m}]=prod(2i+1)/(2i+4)`), plus a general combinatorial proof
  (algebraic + exhaustive brute force) of the "two/three distinct plaquettes
  never conspire to make every link even" lemma behind F06. Self-test: PASS.
- `k2_bracket.py` -- brackets the AW1-gate-admitted
  `K_2^+ = 81108864767825329926713064490531229475390625/24176936535511801466930759024724079017984`
  (read live from `advisor/aw1-gate.json` and `forward/aw1/output/results.json`,
  never retyped except as an independent literal cross-check) against
  assistant-1's three S2 preview tiers (crude/skeptic-84-face/enumerated-49-face)
  and the forward/reverse exact-tier values. Self-test: PASS.
- `rayleigh_rehearsal.py` -- rehearses `flint_harness.py`'s exact
  Rayleigh-quotient/residual/Arb pipeline on three matrices of size >= 84:
  a plain 90x90 rational tridiagonal fixture (harness calls used verbatim),
  and the real Round11 two-plaquette interacting Hamiltonian at D=6 (84x84)
  and D=8 (165x165), via a generalized (non-identity-Gram) extension of the
  same bound, built from `two_plaquette.solve_exact` and
  `flint_harness.rational_sqrt_bracket`. Self-test: PASS. Full timings
  recorded (D=8's 256-bit Arb eig is the slowest single step, ~17s).
- `az2_spec_check.md` -- a concrete AZ2 producer recipe: basis/matrix
  assembly, D=6 primary / D=8 refinement cutoffs, the exact tail bound
  (`tail_lower`: 45 at D=6, 69 at D=8), the residual method rehearsed above,
  an explicit `tau_FG` normalization-dictionary proposal, an exact
  zero-point-derivative method (regularized singular solve; numerically
  sanity-checked, not admitted), required labels/controls, and a runtime
  estimate.
- `results.json` -- combined machine-readable output of the three scripts'
  self-tests plus planning notes.

```
python3 -B research/round32/experts/modern/assistant-2/parity_theorem_exact.py
python3 -B research/round32/experts/modern/assistant-2/k2_bracket.py
python3 -B research/round32/experts/modern/assistant-2/rayleigh_rehearsal.py
```

All three exit 0 (PASS) as of this writing; each prints its own JSON report
and exits 1 on any failed sub-check. `rayleigh_rehearsal.py` takes about
30 seconds (dominated by the D=8 256-bit Arb eigenvalue call).

## parity_theorem_exact.py results

- Three independent routes to the SU(2) single-plaquette moments agree for
  `n=0..12`: the Clebsch-Gordan recursion's own character-count sequence
  `1,0,1,0,2,0,5,0,14,0,42` for `k=0..10` matches `forward/aw1/report.md`
  line 95 exactly; the Catalan closed form `m_0(2k)=C(2k,k)/(k+1)`; and the
  free-link Haar cross-check `E[q_0^{2m}]=prod_{i<m}(2i+1)/(2i+4)` (report.md
  line 117's own "AQ2 S5" route) -- all three give identical `Fraction`
  values at every even `n` checked.
- The reference moments `E[W]=E[W^3]=0`, `E[W^2]=1/4`, `E[W^4]=1/8`
  reproduce exactly.
- Every first-order term of `report.md` equation F05 (the state term of
  `omega(W^2)`, the state term of `C_N`/`c_N`, the vector-centring term,
  the Duhamel term, and the energy term `E_1`) evaluates to exactly
  `Fraction(0)`, at both `tau=+1e-8` and `tau=-1e-8`, over a representative
  sample of omitted faces (5 sharing a link with `W`, 5 disjoint) plus the
  `f=W` branch.
- F06 (`P_24 V W Omega_0 = 0`): the off-multiplet overlaps vanish by the
  same pairwise argument, and the underlying three-plaquette lemma ("`g xor
  h` is never a single face", report.md line 106) is reproduced as a general
  combinatorial theorem (any three 4-element sets with pairwise
  intersection `<=1` cannot have every element occur an even number of
  times -- proved algebraically here, and confirmed by an exhaustive
  brute-force search over 2960 abstract triples with zero counterexamples),
  independent of the actual Z^3 face geometry.
- Item 3's nonzero first-order Wilson mean reproduces exactly:
  `omega_tau(W) = tau/144`, giving `+1/14400000000` at `tau=+1e-8` and
  `-1/14400000000` at `tau=-1e-8`.
- Scope note: the *geometric* facts used (every plaquette has 4 links, two
  distinct plaquettes share at most one link, the specific set of "omitted"
  faces) are cited from the admitted `forward/aw1/report.md` and
  corroborated by assistant-1's S2 brute-force enumeration; they are not
  re-derived here. What this script contributes independently is the
  *group-theoretic* content (the SU(2) trivial-multiplicity engine and its
  application to F04/F05/F06), plus the general 4-element-set combinatorial
  lemma behind F06, from scratch.

## k2_bracket.py results

- The gate's literal `K_2^+` string is found verbatim in
  `advisor/aw1-gate.json`, and confirmed to equal
  `forward/aw1/output/results.json`'s `k2.variants.unpinned_t_bounds.K2`
  field exactly (bit-for-bit `Fraction` equality) -- reproducing the gate's
  own claim that the admitted value "is... identical to the forward's
  labelled unpinned_t_bounds variant".
- `K_2^+ (~3354.80323)` is `>=` all three exported exact-tier values:
  itself (trivially), the forward headline exact tier (`~3354.63833`), and
  the reverse exact tier (`~3354.49943`) -- reproducing "dominating the
  forward... and reverse... exact-tier values" exactly.
- `K_2^+` is strictly less than assistant-1's S2 crude
  (`AM2`-majorant-only) preview tier (`1.65e7`, reconstructed from S2's own
  source and cross-checked against S2's live float preview output, bit for
  bit) -- i.e. the admitted bound sits far below the crude preview, as
  expected since the crude tier is a much looser, geometry-free majorant.
- Informational (not gated): `K_2^+` is also below S2's sharper 84-face
  (`1.88e4`) and 49-face-triangle (`1.10e4`) preview tiers, by factors of
  `~5.6x` and `~3.3x` respectively -- consistent with the admitted value
  coming from a tighter, fully itemized route than either S2 preview.

## rayleigh_rehearsal.py results

- Fixture 0 (90x90 rational tridiagonal, `flint_harness.rayleigh_bounds`/
  `arb_eig_preview` called verbatim, no extension): exact Rayleigh quotient
  `~1.00238`, residual bound `~1.69e-7`; `mu >= Arb lower ball` and the
  residual enclosure contains the Arb ball. PASS.
- Fixture 1 (Round11 two-plaquette Hamiltonian, `alpha=1,lambda1=lambda2=1`,
  `D=6`, 84x84, `G != I`): the generalized Rayleigh/residual extension
  (built from `two_plaquette.solve_exact` + `flint_harness.rational_sqrt_bracket`,
  reused, not reimplemented) gives `mu ~ 1.8360110023644876`, residual bound
  `~4.12e-7`; the Arb comparison uses the exact rational matrix
  `M = solve_exact(G,H)` fed unmodified into `flint_harness.arb_eig_preview`
  (no symmetry required by that call). PASS.
- Fixture 2 (same construction, `D=8`, 165x165): `mu ~ 1.836011002364485`,
  residual bound `~3.82e-7`. PASS.
- Timings: matrix build 0.5s/2.0s (D=6/D=8), exact generalized
  Rayleigh+residual 0.12s/0.69s, `solve_exact(G,H)` 0.88s/6.5s, 256-bit Arb
  eig 1.2s/17.0s. **No scaling blocker found up to 165x165**; the slowest
  single step (D=8 Arb eig, ~17s) still leaves an ample budget for a full
  AZ2 grid (see `az2_spec_check.md` section 9).

## Three planning notes for sub-round 3

See `results.json`'s `planning_notes` for the full text; in short:

1. **For AW2 (selected next by the AW1 gate):** `k2_bracket.py`'s
   live-read-never-retyped pattern for the 46-digit `K_2^+` numerator is
   directly reusable by AW2's own `check.py` to bind its coupling-rule
   input without transcription risk; the sign-margin arithmetic
   (`K_2^+ * tau <= 1/288`, margin `~207`) is a one-line extension not built
   here since it was outside this sub-round's assigned scope.
2. **For sub-round 3 (AX1/AX2, uniform Wilson theory):** the trivial-
   multiplicity engine and the pairwise/triple combinatorial lemmas of
   `parity_theorem_exact.py` do not depend on the selected triple being
   zero, only on the Z^3 lattice's own link-sharing geometry, so they carry
   over to the uniform case directly.
3. **For sub-round 5 (AZ1/AZ2, finite graph):** the generalized-Rayleigh/
   residual/Arb pipeline is now exercised and timed on the *real* D=6/D=8
   two-plaquette matrices (not a toy fixture), and `az2_spec_check.md`
   turns that into a concrete, close-to-implementable recipe, leaving only
   the `tau_FG`-to-`1/144` unit-conversion convention as an open judgment
   call for that sub-round's own producer.
