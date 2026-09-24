# Historical lens (Newton/Tesla), deliberation loop 2 response

2026-09-23. Inputs: `advisor/deliberation-1.md`, `skeptic/triage.md` and `prospective-controls.json`, the Jung and modern memos and recommendations. Same standing as loop 1: contemporary method lenses, no endorsement, no invented quotation, all decimals are scratch previews (`r32loop2.py`, not evidence). Nothing outside this directory was modified.

## 1. The window kernel for AV2: accepted

I accept the skeptic's rational window `ghat = 4s^3/(pi (s-i theta)^3 (s+i theta))`, `|ghat| = (4s^3/pi)(s^2+theta^2)^-2`, `||ghat||_1 = 2`, first moment `4s/pi`, second moment `2s^2`, as the AV2 transfer. Reasons: it needs only the first-order state tier and the admitted seven-star slope `k = 49|tau|/4`; it removes the cutoff `L` and the whole tail; its constants are closed forms with directed `pi`; and it does not depend on the vanishing-first-order structure, so AV2 cannot fail through a parity slip. Reproduced budget at the cap, `s = 1`, exact first-order tier `D = 2.333e-8`: `2(D+D^2) + 49|tau|/pi = 2.03e-7`; crude tiers give `3.6e-5` (`||c||_a <= 448|tau|`) or `4.75e-5` (`592|tau|`), both "limited". The first-order window budget crosses `10^-6` at `s ~ 6.1`, so no cap-level `[0,128]` grid may be promised under AV2.

My second-order Duhamel route becomes an **unexecuted, named refinement of AV2**, not a competitor: keep the window kernel and replace the first-order dynamics term `k * 4s/pi` (`1.56e-7`, 77% of the AV2 budget) by the Dyson second-order term `k^2 M_2/2 + c_{R+} k |tau| M_1` (preview `1.5e-14 + 7.3e-14`, with `c_{R+} ~ 47` the exact-tier constant for the 20-site enlarged cover). The budget then becomes state-dominated (`~4.7e-8` at the first-order state tier, `s`-independent up to `M_0`), which is what a cap-level AT6-type grid would need. Its two hypotheses stay on record: (H3) the second relative-unitary Duhamel step over the 40 stars meeting `R+`, and the identity `T_1(theta) = 0` (first-order Duhamel term has zero Haar expectation). `T_1 = 0` is moved to the assistant tests (script S1) because it is also the skeptic's control `first_order_shift_of_C_vanishes`. The Euclidean-side variant stays dropped (`e^{~27 s}` cost, loop-1 memo 5.3).

## 2. Reconciling K_2: 1.9e4 (skeptic), 1.5e7 (modern), 1.6e8 (mine)

All three count the same leading term, `4 * ||c - c^(1)||_a`, and differ only in which tier of `||c||_a` feeds it and in one over-count of mine:

| term | skeptic | modern | mine (loop 1) |
|---|---|---|---|
| `t = ||c||_a` used | exact `7|tau|/12` (84 faces per site at `tau/144`) | crude `16 J = 448|tau|` | crude `J G(R) = 592|tau|` |
| `||c - c^(1)||_a` | `J (G(t)-16) ~ 288 J t = 4704 tau^2` | `288 J t = 3.61e6 tau^2` | `J G'(R) t = 28*352*592 = 5.83e6 tau^2` (Lipschitz at the ball edge, not at `t`) |
| multiplier (2 Re x 2 sites) | 4 -> `1.9e4` | 4 -> `1.45e7` | 4 -> `2.33e7` |
| pair/density/normalization terms | "small, to be bounded" | not itemized | `(20 * 592)^2 = 1.40e8` over the 20-site `R+` |
| straddling supports | flagged, not bounded | not itemized | inside the `R+` square |

My `1.6e8 = 4*28*352*592 + (20*592)^2` exactly. The `R+` square is the over-count: in the skeptic's ordering every creation disjoint from `R` (including those adjacent to it) sits inside `psi_out` and cancels with the normalization, so pair terms are `(2||c||_a)^2` over the two sites of `R`, not `(20||c||_a)^2`. With the exact tier the itemized second-order terms are `4 J(G(t)-16) = 1.88e4`, two-creation `2t^2 = 0.68`, density `Tr_out|delta><delta|` `<= (2t)^2 = 1.36`, normalization `<= |omega_0(X)| (2t)^2 <= 0.34`, straddling pairing `<= 2 * (2t) * t = 1.4` (a straddling `c_I` meets an outside excitation amplitude of order `||c||_a`): **`K_2 ~ 1.88e4 + O(4)`**, sign margin at the cap `(tau/144)/(K_2 tau^2) ~ 37`. If only the crude tier is proved, `K_2 ~ 1.5e7-2.2e7` and the sign fails at the cap by `~20x`; both are honest outcomes. AW1 must therefore enumerate, as exact rationals and with the tier named per term: (i) the 84 omitted faces per site / 168 for `R` with owner sets and `H_0` eigenvalue 24 (control `first_order_face_enumeration`), giving `||c^(1)||_a = 7|tau|/12` and `||c^(1)_R|| = (tau/72) sqrt(10)/2`; (ii) the self-consistent `t <= 7|tau|/12 + J(G(t)-16)`; (iii) each of the five second-order terms above separately, none set to zero (control `second_order_remainder_itemized`); (iv) the `tau -> tau/100` scaling of every term.

Sign check from `research/round21/forward/i1/report.md` eq. I1.5: `phi_b = -(tau/3) sum_{f in O_b} W_f`, `W_f = (1/2) Tr U_f`, in units `delta = alpha/8`; with `V_b = phi_b/8` (AT4 F03) the `G = H/alpha` interaction is `-(tau/24) sum_f W_f`. First-order ground correction `+(tau/24) R_0 sum_f W_f Omega_0`; the `W Omega_0` component (eigenvalue 3) is `(tau/72) W Omega_0`; `omega(W) = 2 (tau/72)(1/4) = +tau/144` for `tau > 0`. AL1's `lambda sum_p (1 - W_p)` differs by a scalar and gives the same sign; the skeptic's and the modern lens's signs agree. Frozen convention: I1.5 governs.

## 3. Polymer/monotone reading versus `psi = psi_out + delta`: same mechanism, not the same argument

Shared mechanism: commuting nilpotent creators give the ground vector as an explicit product; the `R`-vacuum part and the `R`-excited part are exactly orthogonal; the outside factor multiplies every term, so normalization cancels without any adjoint exponential. Different bookkeeping: the skeptic groups by *creations meeting R* (`e^{-C} = prod(1 - chat_I)` with those factors last), which needs no connectivity and no cluster bound; my reading groups by *excited-set components*, which forces star-connectivity (A1) and a Kotecky-Preiss step (A3) and over-counts `R+`. For AV1 the skeptic's route dominates; I retire the polymer reading to (a) the fixture generator for the controls `deleted_normalization` and `outside_creations_do_not_cancel_naively` (sign-changing weights break the monotonicity `Z_{a u a'} <= Z`, which is exactly the failure those controls must exhibit), and (b) the weighted-norm machinery for AY1, where a size weight is unavoidable.

Direction for AV1 (genuinely different routes to the same inequality):
- **Forward: product-ordering / reduced-density route** (skeptic sketch): `psi = psi_out + delta`, explicit `rho_R = [||psi_out||^2 P_R + |Omega_R><xi| + h.c. + Tr_out|delta><delta|]/(||psi_out||^2 (1+eps^2))`, `||rho_R - P_R||_1 <= 2 eps (1+eps)/(1+eps^2)`. It also yields the first-order density `rho^(1)_R` that AY1 needs.
- **Reverse: fidelity / vacuum-overlap route.** Compute only `Tr(rho_R P_R) = ||(P_R (x) 1) psi||^2/||psi||^2 = 1/(1+eps'^2)` (because `(P_R (x) 1) delta = 0`), then apply AT4's own pure-state-mixture inequality (HNM-AT4-F08) `||rho - P||_1 <= 2 sqrt(1 - Tr(rho P))`, giving `2 eps'/sqrt(1+eps'^2)`: no cross or adjoint terms, a slightly sharper constant, and it displays the mechanism (infidelity `O(tau^2)` from the expansion versus `O(tau)` from the energy, hence no square root). Shared premises to declare: AM2 fixed point, the product ordering, `eps <= 2||c||_a + ||c||_a^2`. The reverse must find on its own the cutoff-vector removal and the straddling term.
- The modern lens's Riesz/left-eigenvector identity is a statement-level cross-check, not a producer route (its `l`-bound is unproved and unnecessary).

## 4. Ranking of the ten loops in plan v1 (no replacement insisted on)

1. AV1 — everything else needs the state lemma; it must deliver the exact first-order tier, else AV2 is limited.
2. AW1 — parity theorem plus the itemized `K_2`; shares 90% of its enumeration with AV1's exact tier, so schedule it immediately after.
3. AV2 — window certificate at the cap; expected `2.0e-7`; carries the second-order refinement as a named unexecuted item.
4. AW2 — sign of `omega(W)` at the cap with both signs; expected margin `~37` if the exact tier holds.
5. AX1 — route-B uniform re-derivation; must re-freeze `J_0 >= 29e-8` as an exact rational (slack is `~5000x`) rather than lower the cap to `9.655e-9`.
6. AX2 — uniform datum by the window route; conditional on AX1's `J_0` decision and the six-face incidence.
7. AZ2 — finite graph; I would move it before AY, since `d<x>/dkappa` at `kappa = 0` and the empirical second-order size are the cheapest independent check on `K_2` and `1/144`; acceptable as planned if the assistants run the preview after sub-round 2.
8. AY1 — `||rho_R - rho'_R||_1 <= 2 D` is a corollary of AV1; the loop's content is the boundary-independent `rho^(1)_R` and the weighted-norm decay, which is a real derivation.
9. AY2 — statement; must say "uniform local closeness, not uniqueness".
10. AZ1 — statement; the one uniform estimate (`g^2/(32 a)` for `g^4 >= 9.6e9`) and the AL1 failure on every `g -> 0` path; no number.

Disagreement retained: the Jung lens's rank-1 finite graph is a different model and should not precede the AQ lemma; its labelling rules R1-R8 should be adopted verbatim. Jung G4 (negotiated `2e-6`) is unnecessary given the window kernel.

## 5. Three assistant scripts after sub-round 1 (pass/fail)

S1 `haar_parity_exact.py` (sympy, exact SU(2) characters): `E[W^n] = 0, 1/4, 0, 1/8` for `n = 1..4`; `E[W^2 W_g] = 0` for a face sharing one link; `E[W_f chi_1(U_W)] = 0` for every omitted `f`; `E[W W_f] = 1/4` iff `f` is the Wilson face; intermediate free energies of `W_f W Omega_0` over all `7 x 21` incident faces contain no `3`; `T_1(theta) = 0` assembled from these. Pass iff every value is the stated exact rational and `m_1 = +1/144` under I1.5's sign; fail if any step uses Monte Carlo.

S2 `am2_tiers_exact.py` (Fraction): enumerate 84 faces per site and the 10 faces with owners inside `R`; compute `||c^(1)||_a = 7|tau|/12`, `||c^(1)_R|| = (tau/72) sqrt(10)/2` (as a squared rational), the self-consistent `t` with outward rounding, and the five second-order terms of Section 2 as exact rationals. Pass iff `K_2 tau^2 < tau/144` at `tau = 10^-8` with margin `>= 10` at the exact tier and iff the crude tier is reported failing (`K_2 > 6.9e5`); also pass iff `D` scales by 100 and `K_2 tau^2` by `10^4` under `tau -> tau/100`.

S3 `window_kernel_budget.py` (Fraction with directed `pi`, `exp`; Arb cross-check): derive `ghat` from `g = e^{-sx}` (`x >= 0`), `e^{sx}(1 - 2sx + 2s^2 x^2)` (`x < 0`) symbolically; verify `|ghat| = (4s^3/pi)(s^2+theta^2)^-2`, `||ghat||_1 = 2`, moments `4s/pi`, `2s^2`, `g(3) = e^{-3s}`, and the negative-atom misread `g(-1) != e^{s}`; assemble the AV2 budget at `s = 1`, `tau = 10^-8` with `D` from S2. Pass iff total `< 10^-6` at the exact tier (expected `2.03e-7`), `> 10^-6` at the crude tier (reported "limited"), crossover `s ~ 6.1`, and the Poisson floor `1.2651e-6` reproduced as the rejected control.

## 6. Method notes to freeze into `research/round32/methods/` for the AV contracts

Newton (analysis before synthesis): before charging any first-order error budget, compute the first-order coefficient of the target observable exactly from the frozen Hamiltonian's representation content; if it vanishes, write the budget at second order and make the vanishing a required control, never an assumption. State the kernel of every inverse: a local trace-norm bound identifies neither the AQ state nor the sign of a second-order remainder. Failed certificates (AT4 `8.4e-4`, the Poisson floor `1.265e-6`) are retained data, not lower bounds.

Tesla (whole device, load, phase): name the source (seven stars; 40 stars for any second-order step), the load (the 48-link, 36-endpoint cover), the clock (`s = alpha t_E/hbar`) and the transfer element (window kernel with exact `||ghat||_1` and first moment) before evaluating; charge every omitted channel (straddling supports, cross and adjoint terms, normalization) in the same anchored norm and name the tier used for each term. A per-site maximum summed over the volume is extensive and rejected; a size-weighted norm is required for multi-polymer or boundary-decay statements (AY), not for AV. The pair `(+tau, -tau)` is the phase-reversal control: the mean is odd, the centered correlation even to `O(tau^2)`.

Provenance line for the snapshot: these rules are modern abstractions from documented practice (General Scholium 1729 p. 392; US 787,412 and US 1,119,732; Colorado Springs Notes p. 60; 1891 AIEE lecture; Keynes MS. 28 as interpretation only); no historical figure endorses any contract, and no occult material supplies a premise.
