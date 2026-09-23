# AV1 skeptical review (post-comparison)

**Verdict: accepted_within_scope.** Both routes of the Hruday first-order local state lemma are proved for the zero-selected AQ subfamily. Tier (ii) meets the preregistered target `D_ii<=4/10^7` at both signs in both producers. The cutoff-vector and passage steps are complete in both. Every one of the 25 contract controls rejects a damaging mutation in the reverse checker and in the skeptic's checkers; the forward checker covers 22 of the 25 with mutations and the other three with positive exact checks (finding N1). There are no blocking issues. Tier (i) fails both targets and is retained as a limited-tier value.

**Standing.** I am a model-agent skeptic with correlated ancestry (same model family as the advisor, the lenses and both producers, and my triage seeded the contract's mechanism). This is not human peer review or formal verification. My pre-comparison package (`av1-independent-derivation.md`, `av1_check.py`, 71 checks, hash-recorded in `av1-independent-freeze.json`) was written before either producer was opened and is unchanged. This review adds `av1_postreview_check.py` (39 exact checks, including 12 source-mutation replays), `replay_loop.py` and the receipts in `av1-replays.json`. Human project author: Hruday N M (BUNZEEY).

## What is proved, with quantifiers

**Model.** AM2/AQ1 zero-selected patterned family:
- SU(2) Kogut–Susskind form on Z^3 at fixed spacing, with coarse 24-link factors;
- selected triple exactly `(0,0,0)`, so the reference `P_R` is the Haar product;
- 21 omitted anchored faces per factor, grouped into whole stars `phi_b=-(tau/3) sum W_f` (normalized units `delta=alpha/8`);
- either sign of `tau` with `|tau|<=10^-8`.

Every bound is increasing in `|tau|`, so the values at the cap bound every smaller `|tau|`. The `-10^-8` evaluation is a replay of the same `|tau|` formula, not a second confirmation.

**Finite volume.** Let `Lambda_N` be a centered whole-star box with `N>=2`, and let `R={0,e_z}` be the complete cover of the original xz Wilson loop (48 links, 36 endpoints, seven incident anchors). For every such box, the reduced density of the unique untruncated ground state satisfies `||rho_{N,R}-P_R||_1<=D`, uniformly in `N`.

**Shared split.** Both routes rest on the same product-ordering split:
- `psi=psi_out+delta`, with `psi_out=Omega_R (x) phi_out`;
- `(P_R (x) 1)psi=psi_out` and `<psi_out,delta>=0`;
- `||delta||<=eps||psi_out||`, where `eps` contains every support meeting `R` (straddling supports included) and the two-creation term.

**The two inequalities.**
- Forward (explicit reduced density, including `|Omega_R><xi|`, its adjoint and `Tr_out|delta><delta|`): `2eps(1+eps)/(1+eps^2)`.
- Reverse (`Tr(rho P_R)=1/(1+e^2)` exactly, plus the AT4-F08 mixture inequality): `2eps/sqrt(1+eps^2)`.

Both are correct. I re-derived the reverse inequality by a third route in my pre-comparison package: purification plus partial-trace contractivity.

**Cutoff removal.** For each fixed `N`, the bound holds for the untruncated ground vector, not only for its eigenvalue.
- Forward: an Eckart inequality with the untruncated gap `E_1-E_0>=1/2`, plus a form-core Rayleigh upper limit.
- Reverse: a Rayleigh quotient with the uniform cutoff gap `1/2`, plus `E<=E_n`.

AM2 §6 supplies both gaps (it states the cutoff-uniform gap and derives the untruncated one), so both arguments are valid.

**Passage to AQ1.** The bound passes to every subsequential limit of AQ1's centered whole-star construction, AQ1's chosen state included, by local trace-norm convergence. AQ1 §2 proves that its diagonal extraction converges in trace norm on every finite region, and its finite states are AM2's full-Hilbert grounds. Two such limits are within `2D` of each other on `R`. This is uniform local closeness, not uniqueness, whole-sequence convergence or a rate in `N`.

**Consequences.** `|omega(W)|<=D`; `|omega(W^2)-1/4|<=D/2` (by the trace-zero effect bound, since `0<=W^2<=1`); and the mean square `m^2<=D^2` is charged.

## Exact numbers re-derived (my own Fraction code; `av1-postreview/results.json`)

**Constants.** `J_0=7/25000000`, `e^{1/8}<8/7`, `G(R)<148/7`, `G'(R)<352`.

**Tier (i).** `t_i=J_0 G(R)=37/6250000` and `eps_i=462501369/39062500000000`.
- Forward: `D_i=36133347268157653748322/1525878906463907516326874161 ~ 2.36803505e-5` (exact).
- Reverse: `D_i<=236800700911401877571290493559933441/10^40 ~ 2.36800701e-5`. I verified it is an upper bound of `2eps_i/sqrt(1+eps_i^2)` by squaring, and tight to `10^-40`.

**Tier (ii) inputs.** `t_1=49|tau|/144=49/14400000000`; `T=t_1/(1-352J_0)=49/14398580736`; `rho=352J_0T=3773/11248891200000000`, which is charged and never zero.

**Tier (ii), forward.** `eps_fwd=2T+T^2=1411060914529/207319127211110301696`, giving `D_ii(fwd)=585079838465912592144137406066050/42981220507576537932303142777593983768257 ~ 1.36124529e-8`. This equals my pre-comparison value to the last digit.

**Tier (ii), reverse.** `a_1=82|tau|/144=41/7200000000` and `eps_rev=a_1+2rho+T^2=461213409663624001/80984034066839961600000000`, giving `D_ii(rev)<=113902305553947264976096174312887/10^40 ~ 1.13902306e-8`. This is a directed upper bound (checked by squaring) and is the labelled 82-face value predicted in item 6 of my pre-comparison checklist.

**Margins and scaling.** Against `4/10^7`, the margins are 29.38 (forward) and 35.12 (reverse). The exact ratios `D(tau)/D(tau/100)` are 100.0098 (forward, tier ii), 100.0015 (forward, tier i) and `[100.01166, 100.01166]` (reverse, tier ii, bracket), all in `[99,101]`. The AT4 square-root bound has ratio exactly 10.

**AV2 arithmetic.** `2(D+D^2)+49*10^-8/pi` (Machin bracket):
- `<=1.8320e-7` with `D_ii(fwd)`;
- `<=1.7876e-7` with `D_ii(rev)`;
- feasible at `4/10^7` and at `4.22*10^-7`, infeasible at `4.23*10^-7` and at `D_i`.

**Counts.** 49 / 15 / 82 / 10, plus 16 faces containing `R`, 72 straddling faces and 27 owner sets meeting `R`. I re-derived them from the I1 §3 table parsed from the report. That table equals the I1.1/I1.4 geometry and **both** producers' encoded `I1_TABLE` literals.

## Why the two tier-(ii) numbers differ, and why both are valid

The formulas differ only negligibly at this `eps`, since `f(eps)-g(eps)~2eps^2`. The real difference is `eps`:
- The forward uses the contract's global form `eps<=2t+t^2`. The two-site sum is bounded by `2*49` face units, which double-counts the 16 faces whose owner set contains both `0` and `e_z`.
- The reverse bounds the first-order `R`-sum directly by the 82 faces meeting `R`, and charges the remainder at both sites (`2rho`). This is exactly the labelled refinement that items 4 and 6 of my contract review accepted, provided it was labelled and charged `2*352J t`; it was.

Exactly, `a_1<2t_1` and `2t_1+2rho=2T`, so `eps_rev<eps_fwd`; the ratio is 1.19510. Hence `D_ii(rev)<D_ii(fwd)`.

The two numbers do not have the same backing:
- `D_ii(fwd)` is certified by **both** inequalities, because `g(eps_fwd)<=f(eps_fwd)`.
- `D_ii(rev)` needs the fidelity inequality, or my purification route: the forward formula evaluated at `eps_rev` exceeds it.

Both are valid upper bounds on the same quantity and agree as upper bounds. Neither is a lower bound, and neither says anything about the value or sign of `omega(W)`.

## Review checklist (my 14 pre-registered failure points), both producers

1. **Normalization.** Exact in both, with no `1+O(tau^2)` shortcut. The unnormalized weights grow (forward `145/144, 5365/5184, ...`; reverse `2,4,8,16`, with the global vacuum overlap decaying) while `rho_R` stays fixed.
2. **Straddling.** `c_I psi_out` is written with the partial vacuum bra in both reports, and all supports meeting `R` are counted.
   - Forward fixture: straddling creations enter `e` at first order but the W-like element only at second order.
   - Reverse fixture C: an inside-only budget of 0 against `e^2=361/1800`.
3. **Two-creation term.** Forward (F08) enumerates the disjoint pairs; reverse uses `C_R^3=0` and `delta=-C_R psi_out+C_R^2 psi_out/2`.
4. **Orthogonality.** `e` is relative to `||psi_out||` in both. Orthogonality is derived from `c_I in (x)Q_xH_x`, and the forward exhibits the vacuum-component failure (overlap `-5/16`).
5. **Monotonicity.** Proved: `f'` is proportional to `1+2e-e^2` on `[0,1+sqrt2]`, and `g` is increasing. `e<=eps` follows by the triangle inequality.
6. **`49|tau|/144`.** Labelled as a triangle bound in both. The grouped square-root forms are directed rationals and labelled; 84 is used only as a labelled bound.
7. **Self-consistent remainder.** Both use the a-priori ball `t<=R` and the convexity of `G`. `t<=t_1/(1-352J)`, the remainder is never zero, and tier mixing is rejected by explicit mutations in both. The forward's sharper `G(t)-16<=288t/(1-8t)` is valid coefficientwise (I rechecked it).
8. **Counts.** Taken over all sites by translation covariance, with box enumeration (`N=1..3` forward, `N=2,3` reverse). Source-mutation replays confirm the counts are derived, not copied: dropping one face, copying a 48, or dropping a table row each aborts the run.
9. **Cutoff.** `Q_L c^(1)=c^(1)` for `L>=24`, and counts only decrease below that. `E_n>=E` holds, and a gap is used in both. Neither report cites AM2 §6 eigenvalues alone, and both show a gapless counterexample.
10. **Passage.** "Every subsequential limit" in both, with no uniqueness, whole-sequence or rate statement. The reverse adds the weak-* mass-escape counterexample.
11. **Signs.** Only `|tau|` enters, in both.
12. **Arithmetic.** The irrational reverse constant is exported as a directed rational (ceiling at `10^-40`). No float reaches an admission Boolean. Scaling ratios are exact rationals or brackets.
13. **Units.** Face energy 24 (normalized) = 3 (`alpha` units); the amplitude is `tau/72` in both unit systems; `J=28|tau|` counts all four incoming stars.
14. **Scope.** Neither report claims a sign or the 1/144 coefficient. The reverse `inputs/` inventory equals AGENTS.md + contract + `shared_premises` exactly (19 files; enforced by `freeze.py`). See N3 for one remark that is not admitted.

## Replays, closures and controls

**Replays.** `replay_loop.py av1` replays forward and reverse, each under normal and `-O` Python, into fresh external directories. All four runs reproduce `output/` byte for byte:

| Output | sha256 |
|---|---|
| forward `results.json` | `3f998a14...` |
| reverse `results.json` | `2dd6c18d...` |

**Freeze and closures.** `freeze.py verify` passes for both. The closures have 30 (forward) and 23 (reverse) files, and every premise snapshot equals its repository source.

**Contract reading.** Both checkers read the target `1/2500000`, the secondary `10^-6` and the reference moments `0, 1/4` from the hash-checked contract snapshot. Neither source contains the target as a literal.

**Mutation harness.** An unmutated copy of each closure reproduces the frozen `results.json` exactly. Each of 12 damaging source edits aborts its run:
- contract byte change;
- claim flag set to true;
- remainder set to zero;
- undeclared or forbidden input;
- count or table edits.

## Blocking issues

None.

## Non-blocking findings (the gate should not repeat the quoted sentences)

**N1. Forward control coverage.** The forward report says: "Every control is a damaging mutation that must raise an explicit exception." That is inaccurate for three ids:
- `no_priority_or_continuum_claim`;
- `first_order_face_enumeration`;
- `av2_feasibility_threshold`.

In `forward/av1/check.py` these are exact positive checks with no `rejected(...)` mutation. They do match their prospective semantics: the flags are false; the energy is 24, the norm is 1/2 and `49<=84`; and `F(4.22e-7+10^-9)` and `F(D_i)` are infeasible. My claim-flag source mutation shows the forward run aborts when a flag is set true. The other 22 forward controls, all 25 reverse controls and all of mine reject explicit mutations. This is a wording and coverage defect, not a mathematical one.

**N2. Reverse error ledger.** The reverse exports no six-name error ledger (`preregistration.error_terms_itemized`). Every term is charged in its text. The mapping for the gate is:

| Term | Tier (ii) | Tier (i) |
|---|---|---|
| `am2_remainder` | `2rho=3773/5624445600000000` | not applicable (bounds the whole `c`) |
| `two_creation` | `T^2` | `t_i^2` |
| `straddling` | inside `a_1` (72 of the 82 faces, `|tau|/2`) and `2rho` | inside `eps` |

The remaining terms:
- `density`: not applicable to the fidelity route, since the mixture inequality bounds the whole distance;
- `onsite_cutoff_vector`: zero, by an exact per-box limit (R20–R21);
- `arithmetic`: outward rounding of at most `10^-40` on `D`.

**N3. Reverse first-order remark.** The reverse says: "no parity argument removes a first-order mean". This is an unproved remark that borders the AW1 exclusion. It is not admitted: no statement about the first-order mean, its coefficient or its sign follows from AV1.

**N4. Forward cutoff attribution.** The forward attributes a "2(E_{0,L}-E_0)/gap form" to the contract. No such form appears in the contract or its premises. The Eckart inequality itself is correct.

**N5. Undeclared reads.** Both producers disclose reads outside `inputs/`: `tools/README.md`, `tools/freeze.py`, AM2 `check.py` and AT5 `check.py`. They were used for protocol and code style, and the forward also re-ran AM2's four-qubit fixture as an audit. None carries premise weight, and none is a forbidden Round32 panel file.

**N6. Reverse labels and flags.** The reverse labels its per-face `a_1=82|tau|/144` "exact_first_order" although it is a triangle bound; the report correctly calls it conservative. The reverse also lacks the three top-level passage flags I recommended in item 11 of my contract review; its passage control rejects all three claims.

## Limitations

- **Scope.** Only this family, cover `R` and fixed spacing. Nothing transfers to nonzero selected triples (where `P_R` is not Haar), uniform Wilson theory, weak coupling or the continuum.
- **Upper certificates only.** There is no lower bound on `||rho_R-P_R||_1`, and the value and sign of `omega(W)` remain open.
- **Inherited without re-proof:**
  - AM2's fixed point, multilinear majorant and both gaps;
  - AQ1's trace-norm compactness and diagonal extraction;
  - I1's dictionary.
- **Independence.** The product-ordering split and the location of the normalization trap are shared panel premises. Independence covers only the inequality, the constants, the enumeration, and the cutoff and passage steps, and all three agents are correlated model agents.
- **Priority.** Scientific priority is unverified.

## Next-decision advice (AV2 only; nothing here is executed)

**Which tier to use.** AV2's window certificate should use tier (ii). I recommend binding `D_ii(fwd)` (exact rational above, `~1.3612e-8`) as `av1_tier_bound`, because both AV1 inequalities certify it. `D_ii(rev)` is also admissible, with the fidelity-route label. With either, the contract's state term `2(D+D^2)` is about `2.7e-8`, and `F(D)<=1.84e-7` leaves a factor of more than 5 below `10^-6`. Tier (i) and AT4's square-root bound must not be used.

**What AV2 must prove itself.** AV1 does not supply:
- the window lemma and its dynamics term;
- how `D` enters the Euclidean readout, through the admitted consequences only;
- the bound for each AQ1 subsequential limit separately, with no uniqueness.

AV2 must also bind AV1's evidence by hash. The first-order coefficient and the sign of the shift stay with AW1.
