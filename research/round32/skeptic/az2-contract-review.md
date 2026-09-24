# AZ2 contract review (skeptic, pre-comparison)

**Standing.** I wrote this from the frozen `contracts/az2.json` (sha256 `2861d5c5…61c3`, frozen 2026-09-24T04:29:40Z) before reading anything of the AZ2 producer.
- From `research/round32/forward/az2/` I only listed the file names in `inputs/` (28) and hashed those files against their repository paths. All 28 are byte-identical and equal AGENTS.md, the contract and the 26 shared premises. I opened none of them there; I read the same files at their repository paths.
- I did not open `forward/az1/`. A directory listing of `skeptic/` showed that an `az1-independent/` output exists; I did not read it.
- The `git status` run after my final replays showed the names, and only the names, of untracked producer paths `forward/az2/arb_preview.py`, `check.py`, `report.md`, `output/` and `preview/`. I opened none of them, and nothing here changed in response apart from this disclosure.
- My scratch folder is `/tmp/claude-0/skeptic-az2-private/`.

I am a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and the producer. My loop-2 response set the conditions "the Round11 two-plaquette graph, or smaller" and "coefficients computed algebraically, never fitted", and my triage wrote the finite-graph labelling. This is not human review. Human author: Hruday N M (BUNZEEY).

**Verdict: executable as written, with the readings below.** Nothing blocks production.
- `az2_check.py` records 81 checks and 23 controls: the 20 contract ids plus 3 extra.
- 75 mutations are rejected, 71 of them inside the 20 contract controls.
- The control mirror matches: `controls` = `preregistration.controls_required.ids`, 20 = 20.

The checker computes:

| Item | Value (exact; decimals are previews) |
|---|---|
| Basis dimension `C(D+3,3)` | 84 (D=6), 165 (D=8) |
| `tail_lower(D)` = `m_{D+1}` | 45 and 69. Both minima fall in the shared-link channel, at `(a,b,c)=(3,4,0)` and `(4,5,0)` |
| `d<W>/dtau_FG` at 0 | exactly `1/6` at D=6, at D=8 and on the untruncated graph |
| `<W>` at `tau_FG=+1/1000, +1/100, +1/10` | 1.6666666087963e-4, 1.6666608796645e-3, 1.6660883111522e-2. The negative sign gives the exact negatives |
| Certified half-widths, D=6 | 3.59e-31, 3.60e-24, 3.71e-17 |
| Certified half-widths, D=8 | 1.78e-41, 1.79e-32, 1.84e-23 |
| Coefficients of `<W>` | `1/6`, `0` (second order, exactly), `-5/864`, `0`, `289/829440` |
| Coefficients of `E_0` | `-1/12` and `5/3456` |

## Readings

1. **In its ground sector the model is AW1's one-plaquette fixture. The second square is a spectator.**
   - **Why `s` is conserved.** With `H_FG = K - tau_FG x` and only face U coupled, the spin `s` carried by `h2, vR, h4` is conserved: `x` acts only on the four links of U, and `K` is diagonal in spin-network labels.
   - **The ground sector.** The ground state lies in the `s=0` sector. Every other sector has `H >= 3-|tau_FG|`, while `E_0 <= 0`. That sector is the closed span of class functions of `U`, i.e. of functions of `x` alone, and in it `K = 4C`. In the orthonormal characters `U_k(x)`, `H` is the Jacobi matrix `diag(k(k+2)) - (tau_FG/2)(shift up + shift down)`.
   - **Identity with AW1.** Under `tau_FG = tau/24`, `8 H_FG = 32C - (tau/3)x`. This is exactly the one-plaquette fixture of AW1 forward (report line 282), and the third-order coefficients agree: `-5/864 · 24^-3 = -5/11943936`.
   - **Consequences.**
     - The dictionary's `1/6 <-> 1/144` is an algebraic identity of two first-order formulas that share the energy denominator 3 and `E[W^2]=1/4`. It is not an independent observation.
     - "A different finite model" is true of the Hilbert space. It is not true of the part that determines `<W>`.
   - **What the producer must do.** Disclose this; I added the extra control `ground_sector_spectator_disclosed`.
   - **When the second square would matter.** Only if its face were coupled. With both faces coupled at `tau_FG` (not the contract model), the third-order coefficient becomes `-187/33696`.
2. **Unpinned parameters.**
   - **What is implicit.** The contract fixes `alpha_FG=1`, `rho=1` and `lambda2=0` only implicitly: through Round11's `parameters()` defaults and the words "multiplies one face".
   - **Why they matter.** The first-order slope is `2E[x^2]/(alpha·eps_100) = 2/(alpha(9+3rho))`, which equals `1/6` only at `alpha=rho=1`.
   - **Negative couplings.** Round11's API rejects `lambda1<0`. So `-tau_FG` needs either the centre-flip mirror or the producer's own code.
3. **The five ledger parts are well defined for the degree basis. Read them this way.**
   - **The spin-network picture.** Round11 (E2) identifies `P_D` with the span of spin networks `(j,s,l)` with `j+s+l <= D`:
     - `j` sits on `h1, vL, h3`, `s` on `h2, vR, h4` and `l` on `vM`;
     - so every link spin in `P_D` is at most `D/2`.
   - **(a) Per-link tail of link `e`.** The omitted spin networks whose spin on `e` exceeds `D/2`.
     - The seven links carry only three labels, so the seven tails are three distinct subspaces, and they overlap.
     - Floors at D=6: 123/2 (A links), 123/2 (B links), 45 (`vM`). At D=8: 96, 96, 69.
   - **(b) Joint product channel.** All seven spins are at most `D/2`, but `j+s+l >= D+1`.
     - It is non-empty for `D >= 2`, and (a) does not imply it.
     - Floors: 48 at D=6 (at `(a,b,c)=(3,3,1)`) and 145/2 at D=8 (at `(4,4,1)`).
   - **The floor covers both.** The union of (a) and (b) is the whole omitted space `Q`. `tail_lower` is a minimum over the entire first omitted shell, and `eps_abc` increases strictly in each exponent. So `QKQ >= m_{D+1}` on all channels at once, and with the potential `QHQ >= m_{D+1}-|tau_FG|`.
   - **The leak of the ground vector.** `x` raises exactly one shell. For the ground (x-only) vector, the omitted component is the single vector `U_{D+1}(x)`, the spin network `((D+1)/2, 0, (D+1)/2)`.
     - That one vector lies in the tails of `h1`, `vL`, `h3` and `vM` together.
     - The B-link tails and the joint channel receive exactly 0.
   - **To satisfy (a) and (b) honestly, the producer must:**
     - give the floor and the leak for all seven links (three distinct values), and state the overlap;
     - derive the zero B-link leak from `s`-conservation, not assume it;
     - give the joint floor and its zero leak, with the reason;
     - compute the leak as one vector in the full space, not as per-link pieces added as if orthogonal;
     - not use the single element `<D+1|x|D>=1/2` as a bound without the three-term argument.
   - **(c) Gauge projection.** It is 0, i.e. `not_applicable` with the reason stated:
     - trace monomials are gauge invariant;
     - `H` commutes with the six Gauss generators;
     - completeness holds by Stone–Weierstrass (Round11 §5).

     It would be a numerical term only for a non-invariant per-link basis.
   - **(d) Ritz/eigenvector residual. Either of two routes is valid.**
     - **Exact shell residual.** The Galerkin condition removes the `P_D` part, so the residual of the truncated ground vector is `-(tau_FG/2)v_D U_{D+1}`. Convert it by Davis–Kahan with the full-space separation `3-|tau_FG|` (Weyl, from the free gap 3). The finite-matrix gap is not a substitute. A rational approximation of the Ritz vector adds a P-part residual; mine is at most 5e-93.
     - **HF concavity.** Use Hellmann–Feynman plus concavity, with Round11's Feshbach lower energies built on the floor `m_{D+1}-|tau_FG|`.

     A truncated-matrix bracket alone is not valid for either.
   - **(e) Arithmetic.** Directed rounding. Mine is at most 1e-60 (outward rounding of the endpoints).
4. **update-4 §3 "certified-tail method" is wrong on both points.**
   - **Point (i).** It says each `exact_bracket` of the rehearsal "is already a certified two-sided enclosure" with `tail_lower` as the floor. But `exact_bracket(H,G,…)` brackets an eigenvalue of the **truncated** matrix and never reads `tail_lower`; only Round11's `certificate()` does, through its `B` brackets. assistant-4's "Ritz values for `<W>`" therefore enclose the truncated `<W>_D`, not the graph's `<W>`.
   - **Point (ii).** The "heuristic" `tau_FG^2/(tail-3)` has exponent 2. The certified truncation effect has order `tau_FG^(2D+1)` in `<W>`, and the leak has order `tau_FG^(D+1)`. The heuristic overstates the error by 13 to 33 orders of magnitude (for example 1.5e-4 against 1.8e-23 at D=8, `tau_FG=1/10`).
   - **Consequence.** A packet that follows either reading is retained as `insufficient`. Controls: `insufficient_verdict_retained` and the extra `truncated_bracket_not_full_graph`.
5. **"Second-order coefficients".**
   - **The exact values.** `<W>` is exactly odd in `tau_FG`: the centre flip on one U link sends `x -> -x` and `z -> -z` and fixes `y`. The checker verified `S K S = K`, `S G S = G` and `S MX S = -MX` on both Round11 pencils. So the `tau_FG^2` coefficient of `<W>` is exactly 0 at every D, and the leading correction is cubic, `-5/864`. The second-order energy coefficient is `-1/12`.
   - **"The tail residual bounding the truncation error."** For the coefficients there is no truncation error to bound: `<W>_D` equals the untruncated series through `tau_FG^(2D)` and first differs at order `2D+1` (checked for D=6 and D=8). The tail matters for the finite-`tau_FG` enclosures, not for the coefficients.
   - **How the coefficients must be obtained.** By Rayleigh–Schrödinger algebra, never by fitting. For example, a divided difference from one enclosure gives `-5.7835e-3`, not `-5/864`.
   - **What the zero does not say.** It says nothing about `K_2` or about the AQ remainder. The AW1 gate itself records "no O(tau^3) from oddness" for AQ limits.
6. **Target.**
   - `{"value":"1","comparator":">="}` is ill-typed for "widths reported at every point; first-order enclosure contains 1/6". I read it as a 0/1 indicator; it equals 1.
   - The first-order value is exact (`1/6`), so "enclosure contains 1/6" is degenerate.
   - As the note says, the target is a feasibility check and does not discriminate.
7. **`error_terms_itemized`.**
   - It lists three legacy items (`truncation_jmax`, `eigenvector_residual`, `arithmetic`), while required item 1 has five parts. Map them as `truncation_jmax` → (a)+(b), `eigenvector_residual` → (d), `arithmetic` → (e), and add (c) as `not_applicable` with its reason.
   - Irony worth recording: in the ground sector the degree cutoff **is** a per-link cutoff, `j <= D/2` on the four U links. "No per-link `j_max` is well-posed" is true of the basis, not of the sector that carries `<W>`.
8. **`selected_after`.** It names `advisor/az1-gate.json`. AZ1 and AZ2 were frozen in the same commit, and that gate did not exist at freeze (I checked by listing). It should name `ay2-gate.json`, or say "in parallel with AZ1".
9. **Copied preregistration fields.**
   - **`state_provenance`.** It reads "AQ1_centered_whole_star_subsequence via finite_volume uniform bound", copied from the Z^3 loops. The AZ2 state is the unique ground state of the gauge-invariant sector of a finite graph (Round11 Theorem F); no subsequence is involved.
   - **`clock`.** It does not apply to a static ground-state mean.
   - **The free-reference exclusion.** The claim exclusion "free reference inside enclosure => no interaction claim" is not triggered: the own free value 0 lies outside every enclosure.
   - **The sub-label.** The expected sub-label is `sign_certified_finite_graph`, which is allowed.
10. **Legacy control ids, as I read them for a finite graph.**

    | Legacy id | Finite-graph reading |
    |---|---|
    | `missing_incoming_stars` | every coupling from `P_D` into the omitted space (the leak) enters both the residual and the Feshbach term |
    | `full_original_wilson_cover` | `W` is the whole four-link square U, including the shared `vM` |
    | `wrong_delta_alpha_hbar_clock` | units: `alpha_FG=1` and `tau_FG=tau/24` from `delta=alpha/8`; no clock |
    | `vector_versus_scalar_centering` | the preregistered uncentred `<W>` |
    | `first_order_mean_charged` | the slope `1/6≠0`, and every enclosure excludes 0 with the sign of `tau_FG` |
    | `root_n_misuse` | ledger items add linearly; Pythagoras is used only across orthogonal components of one residual vector |
    | `tau_scaling_exponent` | the remainder has exponent 3: the exact ratio per decade lies in [999.404346208695, 999.404346208696], against about 100 for a `tau^2` remainder |

    The executed semantics are in the table below.
11. **Forbidden-phrase scan.**
    - The scan must be whole-phrase, word-bounded and case-insensitive.
    - The template itself passes: "not a prediction" and "not a confirmation of the Z^3 value" are not hits.
    - A substring scan for "predict" would flag the mandatory template.
12. **The negative sign.** `-tau_FG` is the exact centre-flip mirror: equal inertia, and endpoints that are exact negatives. It is a replay, not a second confirmation (extra control `minus_tau_mirror_replay`).
13. **Arb.** python-flint is not in the standard library. The admission `check.py` must not import it, and any Arb value is a labelled preview. My checker uses neither Arb nor numpy, and it does not import the Round11 solver, which imports numpy and scipy.
14. **Independence.**
    - The contract, `selection-az2.md`, update-4 and the assistant rehearsals already state `1/6`, the dimensions, the tails and grid previews, so the single producer can copy the headline.
    - My replay is independent in route and code only:
      - the character basis with the exact full-space residual;
      - a second certified route through HF concavity and the Feshbach tail;
      - my own moments, kinetic operator and inertia, cross-checked on the Round11 pencils.
15. **Runtime.** My checker takes about 1 min 50 s. That is dominated by nine exact 165-dimensional inertia calls: eight pencil endpoints, which place the Round11-basis Ritz energy inside my Jacobi bracket, and the kernel of `K`. The producer's estimate of about 8 minutes is plausible for the rehearsed route.

## Control semantics as executed

| Contract id | Rejected mutations (count) |
|---|---|
| `missing_incoming_stars` | leak dropped from the residual; Feshbach `CC^*=0`, i.e. a Ritz value used as a lower bound (2) |
| `full_original_wilson_cover` | three links without `vM`; outer loop `z`; other square `y` (3) |
| `wrong_delta_alpha_hbar_clock` | `tau_FG=tau/3` (delta units); `tau/8`; `alpha_FG=8`; a clock field (4) |
| `vector_versus_scalar_centering` | scalar centring; vector centring; `E[W^2]=1/4` subtracted (3) |
| `first_order_mean_charged` | slope 0 (parity misapplied); `1/12` (factor 2 lost); `1/3`; free value 0 inside an enclosure (4) |
| `tau_scaling_exponent` | remainder exponent 2; first-order exponent 1/2 (2) |
| `changed_model_relabelled` | D=4 labelled D=6; one-plaquette graph; both faces coupled; `rho=1/2`; grid point 1/20; cutoff 10 (6) |
| `coherent_evidence_tampering` | flipped Boolean with rebound digest; dropped control with rebound digest; stale digest (3) |
| `insufficient_verdict_retained` | Ritz-only row dropped; heuristic promoted; single-element row dropped (3) |
| `exact_arithmetic_admission` | float endpoint; float slope; float floor (3) |
| `root_n_misuse` | root-sum-square of items; radius below the linear sum (2) |
| `no_priority_or_continuum_claim` | continuum, priority, weak coupling and goal-2 flags; "predicts"; "confirms the Z^3 value" (6) |
| `finite_graph_model_id` | `model_is_finite_graph:false`; coupling named `tau`; Z^3 label (3) |
| `complete_residual_all_channels` | B links omitted; `vM` omitted; joint channel assumed empty; one omitted element as the bound; `vM` leak zeroed (5) |
| `certified_representation_tail` | finite-matrix gap 3 as the floor; 45 without `-|tau_FG|`; the sector floor 63 without its proof; `m_6`; D=8 tail left at 45 (5) |
| `own_free_reference` | imported `e^{-3}/4`; not the same code path; `1/4` as the reference (3) |
| `no_transfer_to_aq` | `transfers_to_aq:true`; template missing; a `K_2`/AQ sentence; dictionary as a prediction (4) |
| `fg_coefficients_not_fitted` | fitted flag; `c_3` from one enclosure; a small nonzero `c_2`; "least-squares fit" (4) |
| `sign_convention_fixture` | `V=+tau_FG W` with flipped signs; fixture `-1/6` (2) |
| `complete_residual_ledger_itemized` | (a) and (b) merged; (c) `not_applicable` without a reason; (e) missing; (d) missing (4) |

**Extra controls:**
- `ground_sector_spectator_disclosed` (2);
- `minus_tau_mirror_replay` (1);
- `truncated_bracket_not_full_graph` (1), which rejects the update-4 reading.

**Deferred to post-comparison:**
- the producer's actual ledger, freeze inventory and report text (forbidden-phrase scan and template);
- whether its enclosures intersect mine at all 12 points.
