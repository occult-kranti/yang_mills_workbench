# Modern lens (Penrose/Feynman), deliberation loop 3 sign-off

2026-09-23. `round32_loop3_advisory`; not a contract, loop or gate. Read first: `loop2-response.md` (this lens's position), `advisor/deliberation-2.md`, `advisor/deliberation-3.md`, `advisor/plan.json`, `contracts/av1.json`, `contracts/av2.json`.

## 1. Sign-off / veto

**Plan v2: sign-off, no veto.** Five sub-rounds, direction rules, assistants-after-each-sub-round, pre-registration block and the loop-2 vetoes are unchanged and remain adequate; nothing here reopens the plan.

**AV1: sign-off, no veto.** Tier-(ii) target `D_ii<=4/10^7`, reverse premise isolation, and the 49-face/15-support enumeration match my independent count exactly; ship it.

**AV2: sign-off, C^2 accepted, no veto.** Both window members clear `1e-6` with margin ~5 at the exact tier (C^2: 2.03e-7; my C^1: 1.86e-7) — not decisive. C^2's finite `M_2=2s^2` is the only route to the unexecuted second-order Dyson refinement, so freezing C^2 and keeping C^1 as a preview control (as recorded) is the conservative, forward-compatible choice. I retract "insisted" from loop 2 on this point.

**AY2-into-AY1 decline: accepted, no veto.** I flagged this "recommended, not insisted" in loop 2; the advisor's reason (AY2 remains the named-families statement) stands. No veto anywhere in plan v2 or the two contracts.

## 2. Link-flip antisymmetry lemma for AW1

Hypotheses: zero-selected triple, centered whole-star box `Lambda_N`, finite volume. Let `E={(p,x):p_y even} U {(p,y):p_z even} U {(p,z):p_x even}`, `U_E` = the unitary multiplying every link variable in `E` by the central `-1 in SU(2)`. Statement: every plaquette of `Z^3` meets `E` in an odd (1 or 3) number of links, so `U_E W_f U_E* = -W_f` for every `f`; `U_E` fixes the Gauss-law projectors, the Casimir term and `Omega_0`, and flips only the magnetic sum, giving `U_E H(tau) U_E* = H(-tau)` exactly in every `Lambda_N`. Implies: `omega_{-tau}(W)=-omega_tau(W)` exactly and `C(s)`, `omega(W^2)` are even in `tau`, for every N and every AQ-type subsequential limit; hence the `tau^2` coefficient of `omega(W)` vanishes identically, and by the same mod-2 obstruction `<W Omega_0, L_1(c^(1))Omega_0>=0`, so the *direct* second-order remainder in `K_2` is `O(tau^3)`. Does not imply: the sign or size of that `tau^3` coefficient, nor that `K_2` itself is small — the straddling/pair/density terms (b)-(f) of my §2 still need the full enumerated tier; the lemma kills one term, not the budget.

## 3. Assistant scripts after sub-round 1

- **S1 `flint_harness.py`** (reusable python-flint `fmpq_mat`/Arb harness for all lenses: `to_fmpq`/`from_fmpq` rejecting floats, `mat`/`solve`/`det`/`inv` via `fmpq_mat`, exact `inertia` with 2x2 pivots, `ball`/`contains`/`integral` via Arb, `provenance()` pinning `flint==0.9.0`). PASS iff fmpq solve/det/inertia match stdlib-Fraction Gaussian elimination bit-for-bit on the seeded fixtures, Arb balls contain the AT5/AV1 intervals, and no `check.py` imports it; else FAIL.
- **S2 `flip_parity_k2.py`.** PASS iff every plaquette of a 9^3-factor box meets `E` oddly with zero failures, the exact `<x>(-k1,k2)=-<x>(k1,k2)` identity holds on the Round11 D=4 fixture with no `k^2` term, the 49/15/82/10/72/10 counts match AV1's frozen enumeration, and all three K_2 tiers stay below `6.9e5` with margin >=10 (crude tier reported failing); else FAIL.
- **S3 `window_budget_crosscheck.py`.** PASS iff sympy/Arb reproduce `ghat`, `M_0=4/pi or 2`, `M_1=4s/pi`, `M_2` (divergent for C^1, `2s^2` for C^2), the negative-atom values `3/e`/`5/e`, and AV2's recorded radius is reproduced to its rational bits and `<1e-6`; FAIL if `M_0=1` is used, `m^2` is dropped, or a `[0,128]` cap-level grid is claimed.

## 4. Remaining disagreements

- None that block production. I would still rather the Lambda(left-eigenvector)-locality lemma I proposed be folded into AY1's scope (it underlies both uniform analyticity and weighted boundary decay); the advisor did not adopt this, and I do not veto over it.
- I retain a quantitative preference for the C^1 window (5% tighter budget) purely as a recorded position; operationally I accept C^2 as frozen (§1).
