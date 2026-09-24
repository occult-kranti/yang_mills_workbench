# AZ2 independent derivation (skeptic, before comparison)

**Standing.** I wrote this after the AZ2 contract froze (`frozen_at` 2026-09-24T04:29:40Z, sha256 `2861d5c5…61c3`). AZ2 has a single forward producer, so this package is a required admission input (`single_direction_independent_replay`).

**Sources.** I worked from:
- the frozen contract, `selection-az2.md` and `panel-update-4.md`;
- Round11 `README.md`, `advisor/advisor.md` (§1, §5–7), `solver/README.md` and `solver/two_plaquette.py`, read for their conventions (`basis`, `moment`, `kinetic`, `free_energy`, `free_gap`, `tail_lower`, `inertia`, `exact_bracket`, `certificate`);
- the AW1 gate and AW1 forward report, for the I1.5 sign, `+tau/144` and the one-plaquette fixture;
- modern `update-4.md` and the rehearsals `assistant-3/az2_dictionary_calc.py` and `assistant-4/finite_graph_rehearsal_d8.py` with their READMEs, read as previews only;
- `methods/paired-physics-research/references/complete-residual-and-error-scope.md`;
- my own `triage.md`, `prospective-controls.json`, `loop2-response.md`, `ay2.md` and AX2 package;
- AGENTS.md.

**Isolation.**
- I did not open or read anything under `research/round32/forward/az2/` except `inputs/`. There I listed the file names with `find`: 28 files, equal to AGENTS.md, the contract and the 26 shared premises. I hashed them against their repository paths, and all are byte-identical. The checker repeats this hash comparison and does nothing else under `forward/az2/`.
- I did not open `forward/az1/`.
- **Incidental exposure.** A listing of `skeptic/` showed that an `az1-independent/` directory exists. I did not read it.
- While this package was being written, `git status` showed no untracked producer paths.
- The `git status` run after the final replays showed the names, and only the names, of untracked producer paths: `forward/az2/arb_preview.py`, `check.py`, `report.md`, `output/` and `preview/`. The producer was therefore working in parallel. I opened none of them. Nothing in this package changed in response, apart from this disclosure and the matching line in the contract review.

**Scratch.** All scratch work stayed in `/tmp/claude-0/skeptic-az2-private/`: prototypes, timing, the source-edit harness and its mirror tree built from repository paths, and the replays. I read nothing in other agents' scratch folders.

**Correlated ancestry.** I am a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and the producer. My loop-2 response set the two-plaquette placement and the not-fitted rule. This is re-derivation, not independent discovery or human review.

**Exactness.** Exact values come from `az2_check.py`, which uses the standard library and `Fraction` only, with no numpy, no python-flint and no import of the Round11 solver. It records 81 checks and 23 controls (the 20 contract ids plus 3 extra), with 75 rejected mutations, 71 of them inside the contract controls. Every decimal below is a preview. Human project author: Hruday N M (BUNZEEY).

## 1. Model and conventions

**The graph (Round11 §1).**
- Six vertices and seven links: `h1, h2, h3, h4, vL, vM, vR`.
- Six Gauss constraints; the physical space is the gauge-invariant `L^2`.
- The squares are `U = vM h3^-1 vL^-1 h1` and `V = h2 vR h4^-1 vM^-1`. They share `vM`.

**The coordinates.** `x=(1/2)Tr U`, `y=(1/2)Tr V` and `z=(1/2)Tr(UV)`. Here `x` and `y` have independent semicircle laws, and `z = xy - sqrt(1-x^2)sqrt(1-y^2)u` with `u` uniform on `[-1,1]`.

**The model as I read the contract.**
- `H_FG = K - tau_FG·x`.
- `K = sum_e C_e` is the Casimir sum over the seven links, with `alpha_FG=1` and `rho=1`.
- The second face is uncoupled (`lambda2=0`).
- The observable is `<W> = <x>` in the ground state of the gauge-invariant sector. That ground state is unique (Round11 Theorem F).
- This equals Round11's `K + lambda1(1-x)` at `lambda1=tau_FG`, up to the constant `tau_FG`.

**The I1.5 sign.** The Z^3 face term is `-(tau/3)W_f` in `delta=alpha/8` units, which is `-(tau/24)W_f` in `alpha` units. So `V = -tau_FG W`, and `<W>` has the sign of `tau_FG`.

## 2. Basis, moments and dimension

**The basis.** `P_D` is spanned by the monomials `x^a y^b z^c` with `a+b+c <= D`. By stars and bars the count is `C(D+3,3)`: **84 at D=6** and **165 at D=8**.

**The spin-network picture (Round11 (E2)).** Put `j=(a+c)/2` on `h1, vL, h3`, `s=(b+c)/2` on `h2, vR, h4` and `l=(a+b)/2` on `vM`.
- Admissible triples correspond one to one to the monomials, and `a+b+c = j+s+l`.
- `P_D` is the span of the spin networks with `j+s+l <= D`.
- Every link spin in `P_D` is at most `D/2`.

**Moments.** I computed the Haar moments by a Beta-function route: `E[x^p(1-x^2)^k] = (2/pi)B((p+1)/2, k+3/2)`, and the `z` average over isotropic axes. A separately written copy of the Round11 route (Catalan moments with a binomial expansion) agrees on all 1330 triples of degree at most 18. The fixtures `E[x^2]=E[y^2]=E[z^2]=1/4`, `E[xyz]=1/16` and `E[x^4]=1/8` hold.

**The kinetic operator.** I reimplemented it in Round11 coordinates from the solver README. The checks:
- it is triangular in degree, with diagonal `eps_abc = 3j(j+1)+3s(s+1)+l(l+1)`, which is Round11 (E1) = (E2), checked to degree 9;
- the low-level table holds: `1:0`, `x,y:3`, `z:9/2`, `xy-z/4:13/2`, `x^2-1/4:8`;
- its Galerkin forms are symmetric at D=6 and D=8.

## 3. Free spectrum, gap and tails

**The shells.** The shell eigenvalues of `K` are `eps_abc`. The shell minimum is `m_d = (5/8)d^2 + 2d + (3/8)(d mod 2)` (Round11 (E3)), checked by enumeration for `d <= 60` and strictly increasing.

**The free gap.** It is `m_1 = 3`, on the eigenspace `span{x,y}`. The free ground state is the constant, with energy 0.

**Monotonicity.** `eps_abc` increases strictly in each exponent (checked for `a+b+c <= 30`). So lowering a positive exponent of any omitted monomial lowers its energy, and no later shell can undercut the first omitted shell. This gives `QKQ >= m_{D+1}Q` on the **whole** omitted space.

**The certified tails.** `tail_lower(6)=m_7=`**45** and `tail_lower(8)=m_9=`**69**.

**Per-channel floors.** All four channel minima lie in shell `D+1` (checked over shells up to `D+40`):

| Channel | D=6 | D=8 |
|---|---|---|
| (a) A links `h1,vL,h3` (spin `j > D/2`) | 123/2 | 96 |
| (a) B links `h2,vR,h4` (spin `s > D/2`) | 123/2 | 96 |
| (a) shared `vM` (spin `l > D/2`) | **45**, at `(3,4,0)` | **69**, at `(4,5,0)` |
| (b) joint (all spins `<= D/2`, `j+s+l >= D+1`) | 48, at `(3,3,1)` | 145/2, at `(4,4,1)` |
| `x`-only sector, `(D+1)(D+3)` | 63 | 99 |

**What 45 and 69 certify.** With the potential, `QHQ >= (m_{D+1} - |tau_FG|)Q` for `H = K - tau_FG x`, over every per-link and joint channel. Plugged into Round11's Feshbach/Young bound (T4)–(T5), this gives a certified **lower** bound on the full-graph ground energy. Together with the Ritz upper bound and Hellmann–Feynman concavity, that yields a full-graph enclosure of `<W>`.

**What they do not certify.**
- They do not enclose `<W>` by themselves.
- The residual route (§6, route C) does not need them: it uses the exact leak and the separation `3-|tau_FG|`.
- The sharper `x`-only floor `(D+1)(D+3)` holds only after the sector reduction of §4.

## 4. Exact reduction: the second square is a spectator

**The invariant sector.** `x` acts only on the four links of U, and `K` is diagonal in spin-network labels. So `s` is conserved, and the closed span of functions of `x` alone (class functions of U) is invariant under `K` and under `x`.

**The characters.** In the Chebyshev characters `U_k(x) = chi_{k/2}(U)`, the checker verifies exactly, at D=6 and D=8, in the Round11 conventions:
- `<U_j,U_k> = delta_jk`;
- `K U_k = k(k+2) U_k`, which is `4C`: four links at spin `k/2`;
- `x U_k = (U_{k+1}+U_{k-1})/2`;
- **`U_{D+1}` is orthogonal to every monomial of degree `<= D`.**

**The ground state lies in the sector.** The complement of the sector contains no constants, so `H >= 3-|tau_FG|` there, while `E_0 <= 0` in the sector.

**The Jacobi matrix.** On the `x`-only monomials the truncated problem is exactly
`J_D(tau_FG) = diag(k(k+2))_{k=0..D} - (tau_FG/2)(shift up + shift down)`.
Its omitted coupling is the single element `-(tau_FG/2)` from `k=D` to `k=D+1`.

**Identity with AW1.** Multiplying by 8 at `tau_FG = tau/24` gives `32C - (tau/3)x`, which is **AW1's admitted one-plaquette fixture** (`H_0=32j(j+1)`, `V=-(tau/3)W`). The ground-sector physics of AZ2 is therefore that fixture.

**Centre-flip mirror.** Let `S = (-1)^(a+c)` (a centre flip on one U link). The checker verifies `S K S = K`, `S G S = G` and `S MX S = -MX` on both Round11 pencils. So `-tau_FG` is an exact mirror, and `<W>` is odd in `tau_FG`.

**Both faces coupled (side value).** This is not the contract model. With `V = -tau_FG(x+y)`, untruncated RS gives `<x> = tau_FG/6 - (187/33696)tau_FG^3 + …` and `E_2 = -1/6`. The second square enters only if its face is coupled.

## 5. The derivative at zero, and why it does not depend on D

**The value.** First-order perturbation theory around the constant `Omega` (with `E_0(0)=0`) gives:
- `x·Omega = x`;
- `x` is an exact eigenvector of `K` with eigenvalue 3 (`K x = 3x` as a polynomial identity), so the first-order vector is `psi^(1) = (tau_FG/3)x`;
- `d<W>/dtau_FG|_0 = 2<Omega, x psi^(1)>/tau_FG = 2E[x^2]/3 = (2·1/4)/3 =` **`1/6`**.

**D-independence.** `psi^(1)` lies in `P_1`, which is contained in every `P_D` with `D>=1`. So the truncated first-order problem has the same solution as the untruncated one. The truncation enters only through the top shell, which the first-order vector never reaches.

**The check in the producer's basis.** At D=6 and D=8 the checker verifies:
- the Galerkin identity `K_form(e_x/3) = MX e_1` entrywise;
- `inertia(K_form) = (0,1,n-1)`, so the kernel is the constants and the solution is unique;
- and hence the derivative `2·MX[const][x]/3 = 2E[x^2]/3 = 1/6` exactly.

**The graph's own free reference, in the same routines.** `<W>(0)=0` and `E_0(0)=0`, with gap 3 and `E[W^2]=1/4`. `route_c(D,0)` returns `[0,0]`. In the 84-dimensional Round11 pencil, `E_0(0)` lies in `(-10^-25, 10^-25)`.

## 6. Certified enclosures at the grid

**Route C (primary): exact full-space residual.**
- **The trial vector.** Bracket the Jacobi ground eigenvalue by exact Sturm counts to width `10^-90`. Build `v` by the three-term recurrence from the top at the bracket midpoint.
- **Its residual.** `r = (H-rho)v` has two parts:
  - a Galerkin part in `P_D`, from the rational approximation, at most 5e-93;
  - the **exact one-component leak** `-(tau_FG/2)v_D U_{D+1}` into shell `D+1`.
- **The spectral bound.** With the full-space separation `b = 3-|tau_FG|` (Weyl, from the free gap 3), the spectral-measure bound (complete-residual note) gives `sin theta <= ||r||/(b-rho)`. Then `|<W> - <v,xv>/<v,v>| <= 2 sin theta`, because `||x|| <= 1`.
- **Rounding.** Square roots are rounded up at `10^-100`, and the endpoints are rounded outward at `10^-60`.

**Route F (cross-check): Hellmann–Feynman, concavity and the Feshbach tail.**
- **The enclosure.** `E_0(tau_FG)` is concave, so `<W>(t) = -E_0'(t)` lies in `[(E_lo(t-h)-E_hi(t))/h, (E_hi(t)-E_lo(t+h))/h]`, with `h = |t|·10^-12`.
- **Upper energies.** `E_hi` is the Ritz value.
- **Lower energies.** `E_lo = lambda_min(J_D - (t/2)^2/(m_{D+1}-|t|-R) e_D e_D^T)` with `R = E_hi` (Round11 (T4)). This is where the tails 45 and 69 enter.
- **Agreement.** At all 12 points route C lies inside route F. Route F's width is about `h/6` (1.7e-14 at 1/10).

**Guards recomputed outside the routines.** Three quantities could be shrunk without breaking any value test, so the checker recomputes each independently:
- the separation `b = m_1 - |tau_FG|`, with `m_1 = 3` from the shell enumeration and never a finite-matrix level;
- the inequality `radius >= 2 sqrt(||r_P||^2 + leak^2)/(b - rho)`;
- the Feshbach term `(tau_FG/2)^2/(m_{D+1} - |tau_FG| - R)`, which must be positive at every point.

**Round11-basis cross-check.** For `tau_FG = +1/1000, +1/100, +1/10` and `-1/10`, at D=6 (84) and D=8 (165), I rounded the Jacobi bracket outward at `10^-25`. The exact inertia of `K - tau_FG MX - lambda G` is `(0,0,n)` at the lower end and `(1,0,n-1)` at the upper end. So the Ritz ground energy of the producer's basis lies inside my bracket.

**Enclosures (exact rationals in `az2-independent/results.json`).** Decimals are rounded outward (lower ends down, upper ends up) at the digits shown. Each negative point is the exact negation.

| D | `tau_FG` | lower | upper | half-width |
|---|---|---|---|---|
| 6 | 1/1000 | 0.000166666660879629978057460688201962 | 0.000166666660879629978057460688919840 | 3.59e-31 |
| 6 | 1/100 | 0.001666660879664472176328166229230208 | 0.001666660879664472176335366558520720 | 3.60e-24 |
| 6 | 1/10 | 0.016660883111521936680228504770719547 | 0.016660883111522010859108428089815832 | 3.71e-17 |
| 8 | 1/1000 | 0.000166666660879629978057460688560900923118734 | 0.000166666660879629978057460688560900923154344 | 1.78e-41 |
| 8 | 1/100 | 0.001666660879664472176331766393857606118 | 0.001666660879664472176331766393893322030 | 1.79e-32 |
| 8 | 1/10 | 0.016660883111521973769650069301187929 | 0.016660883111521973769686863559360310 | 1.84e-23 |

**Ritz energies** (identical at D=6 and D=8 to the digits shown): `E_0 ≈ -8.3333331886574131e-08`, `-8.3333188657988110e-06` and `-8.3318871544888471e-04`.

**Ledger per point.** The table shows D=6 at `tau_FG=±1/10`; every point is in the results.

| Part | Value |
|---|---|
| (a) per-link | `2·leak/(b-rho)` ≈ 3.71e-17. The leaked vector `U_{D+1}` is the spin network `((D+1)/2,0,(D+1)/2)`, so the same vector lies in the tails of `h1, vL, h3, vM`, and `h2, vR, h4` receive 0 |
| (b) joint | 0: all spins `<= D/2` but `j+s+l >= D+1`, which the ground-sector leak never reaches |
| (c) gauge projection | not applicable: an invariant basis, and `H` commutes with the six Gauss generators |
| (d) Ritz / eigenvector | 4.2e-93 (Galerkin part) |
| (e) arithmetic | at most 4.5e-61 |
| floor | 45 - 1/10 = 449/10 |
| separation | 3 - 1/10 = 29/10 |

**How the width scales.** The width is set by the leak, which is of order `tau_FG^(D+1)`: the ratio per decade of `tau_FG` is `10^7` at D=6 and `10^9` at D=8.

**Sign.** At every point the enclosure excludes the own free value 0, with the sign of `tau_FG`. Sub-label: `sign_certified_finite_graph`.

**Retained `insufficient` rows.**
- **Truncated brackets only** (the update-4/assistant-4 reading). These enclose the truncated `<W>_D`. The numbers are indistinguishable at 1e-14, but the certificate is missing.
- **The heuristic `tau_FG^2/(m_{D+1}-3)`.** It is uncertified and has exponent 2. At D=8, `tau_FG=1/10` it gives 1.5e-4 against a certified 1.8e-23.
- **The single omitted element `<D+1|x|D>=1/2` as a bound.** It proves leakage but does not bound it. Here it happens to be the only omitted element in the ground sector, but that follows from the three-term structure proved in §4.

## 7. Second-order and higher coefficients (finite-model values)

**The series.** Exact Rayleigh–Schrödinger on `J_D`, and independently untruncated RS in Round11 monomials, give:
- `E_0 = -tau_FG^2/12 + 5tau_FG^4/3456 - 289tau_FG^6/4976640 + 21391tau_FG^8/7166361600 - …`
- `<W> = tau_FG/6 + 0·tau_FG^2 - (5/864)tau_FG^3 + (289/829440)tau_FG^5 - (21391/895795200)tau_FG^7 + …`

**The values.** The second-order coefficient of `<W>` is **exactly 0** at both cutoffs, by the centre flip. The second-order energy coefficient is **`-1/12`**. The first nonzero correction to `<W>` is **`-5/864`**.

**D-dependence.** `<W>_D` equals the untruncated series through `tau_FG^(2D)` and first differs at `tau_FG^(2D+1)`: at order 13 for D=6 and order 17 for D=8, both checked. So the truncation error of every coefficient the contract asks for is exactly 0. The certified tail is needed only for the finite-`tau_FG` enclosures.

**Scaling.** From the D=8 enclosures, `(<W>(1/10)-1/60)/(<W>(1/100)-1/600)` lies in `[999.404346208695, 999.404346208696]`. The remainder therefore has exponent 3; a `tau_FG^2` remainder would give about 100.

**Not fitted.** A divided difference taken from one enclosure gives `-5.7835e-3`, not `-5/864`. That is why coefficients must come from algebra.

## 8. Normalization dictionary (consistency only)

**Where it comes from.** `tau_FG = tau/24` is the unit conversion `delta=alpha/8`: `-(tau/3)W` in delta units equals `-(tau/24)W` in alpha units.

**The comparisons.**
- **First order.** `(1/6)·(1/24) = 1/144`, the AW1 value. The two first-order formulas are the same expression, `2E[W^2]/3` times the face coefficient. It holds only at `alpha_FG=rho=1`: the slope is `2/(alpha(9+3rho))` in general.
- **Third order.** `(-5/864)/24^3 = -5/11943936`, which is exactly AW1's one-plaquette fixture coefficient, as it must be by §4.

**What it is.** A consistency check on a finite model whose ground sector is AW1's fixture. It is not a prediction, a confirmation or a transfer, and it says nothing about `K_2` or the AQ remainder.

**The template.** The mandatory sentence passes a word-bounded, case-insensitive scan for "predicts" and "confirms the Z^3 value".

## 9. What I will require of the producer

1. **Model.** Declare `alpha_FG=1`, `rho=1`, `lambda2=0`, `H = K - tau_FG x` (or Round11's form plus a constant), and the I1.5 sign.
   - Handle `-tau_FG` by the centre-flip mirror or by its own code; Round11's `parameters()` rejects `lambda<0`.
   - Label the negative sign a replay.
2. **Full-graph enclosures.** They must be full-graph enclosures, not truncated brackets, at all 12 points.
   - Either use the exact shell residual with Davis–Kahan and the full-space separation `3-|tau_FG|`, or use HF concavity with the Round11 Feshbach lower bound on the floor `m_{D+1}-|tau_FG|`.
   - The finite-matrix gap is not a substitute.
   - A truncated `exact_bracket` difference quotient (assistant-4) is `insufficient` for the full graph.
3. **The five-part ledger**, per `(D, tau_FG)`:
   - (a) floors and leak for all seven links, three distinct values, with the overlap stated and the zero B-link leak derived from `s`-conservation;
   - (b) the joint floor (48 or 145/2) and its zero leak, with the reason;
   - (c) `not_applicable` with the invariance reason;
   - (d) the Ritz residual;
   - (e) the arithmetic term.

   Deterministic items add linearly. The tail floor must be the all-channel `m_{D+1}-|tau_FG|`: 45 and 69 before the shift. The `x`-only floor 63/99 is allowed only with the sector proof.
4. **Coefficients** by exact RS: `1/6`, `0`, `-5/864`, `E_2=-1/12`. Never fitted, and `fg_coefficients_fitted:false`.
5. **The free reference** computed in the same code path: `<W>(0)=0` and `E_0(0)=0`.
6. **Disclosure.** State the ground-sector spectator structure and the identity with AW1's fixture.
7. **Wording.**
   - Gate fields: `transfers_to_aq:false`, `model_is_finite_graph:true`, `fg_coefficients_fitted:false`.
   - The mandatory template, verbatim.
   - No "predicts" and no "confirms the Z^3 value".
   - No sentence about `K_2` or the AQ model's shift.
   - Arb as a labelled preview only, and not imported by `check.py`.
8. **Replay.** Byte-identical replay under `-B` and `-B -O`, with no `.pyc` in the closure.

## 10. Predicted values for the post-comparison

- **Dimensions and tails.** Dimensions 84 and 165; `tail_lower` 45 and 69; free gap 3.
- **Derivative at zero.** Exactly `1/6` at D=6 and D=8; converted, `1/144`.
- **Coefficients.** `<W>`: `c_2 = 0` and `c_3 = -5/864`. `E_0`: `-1/12`, then `5/3456`.
- **Enclosures.**
  - Every producer enclosure intersects mine at the same `(D, tau_FG)`.
  - `<W> ≈ ±1.6666666087963e-4`, `±1.6666608796645e-3` and `±1.6660883111522e-2`.
  - Producer widths will likely be far larger than mine. The rehearsal's HF widths were about 1.9e-7, 1.7e-6 and 1.7e-5.
  - D=6 and D=8 agree below 1e-16.
- **Negative sign.** `-tau_FG` gives the exact negation.
- **Ledger.** B-link and joint leaks are 0; the leak sits in the tails of `h1, vL, h3, vM` together; gauge projection is not applicable.
- **Verdict.** `accepted_within_scope` is reachable at both cutoffs. It becomes `limited` if the producer reports only truncated brackets at one cutoff, or leaves the joint channel unitemized. It becomes `insufficient` only if the residual argument fails.

## 11. Replay

```bash
python3 -B research/round32/skeptic/az2_check.py --output /absolute/fresh/dir
```

**Byte-identity.** Runs under `-B`, `-B -O` and without `-B` are byte-identical (sha256 recorded in the freeze), and no `.pyc` is written. Each run takes about 1 min 50 s on this container. Nine exact 165-dimensional inertia calls take most of that: eight pencil endpoints and the kernel of `K`.

**Source-edit mutations.** These were run on mirror copies built from repository paths, in private scratch; the results are in the next paragraph.

Of 14 edits, 12 abort for the intended reason:
- the tail taken from the last retained shell;
- the leak dropped;
- the separation 8 in place of 3 (a finite-matrix level);
- the sign of the expectation flipped;
- a wrong Beta moment;
- the kinetic cross term at `rho/4`;
- the derivative missing its factor 2;
- the Feshbach term set to zero;
- the tail floor without `-|tau_FG|`;
- the direct-expectation RS reading `y` in place of `x`;
- the Davis–Kahan factor halved;
- the contract hash.

Two do not abort:
- **Flipping the sign of `V` in the Jacobi RS is harmless.** `E_0` is even in `tau_FG`, so every energy coefficient is unchanged. The sign of `<W>` is fixed separately by route C and by the direct-expectation monomial RS.
- **Replacing the sum of ledger items by their maximum cannot be seen in the values.** The two differ by about `d^2/(2a)`, around 1e-169, far below the 1e-100 square-root rounding. This remains a proof-text item.

An unmutated mirror run exits 0.
