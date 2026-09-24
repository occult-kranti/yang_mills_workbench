# Historical lens (Newton/Tesla) assistant scripts -- Round32 sub-round 2

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted assistant scripts for the
Newton/Tesla historical lens, delivering the five tests requested in
`research/round32/experts/historical/update-1.md` section 5. These
scripts and this note count **zero research loops**: they are tests and
planning material for the lens, not a producer, skeptic or advisor
artifact. Nothing here reads `research/round32/forward/aw1/check.py`,
`research/round32/reverse/aw1/check.py` or `research/round32/forward/aw2/check.py`;
the geometry helpers reimplement the I1.4 face-link rule fresh (the same
convention already independently used, and disclosed, by
`research/round32/experts/historical/assistant-1/haar_parity_exact.py`
and `am2_tiers_exact.py`, reused here by copy per the assignment's own
instruction). Everything numeric is `fractions.Fraction`; no floats
appear in any pass/fail comparison (decimal previews are for readability
only).

Read before writing: `update-1.md` section 5, `research/round32/advisor/aw1-gate.json`,
`research/round32/forward/aw1/output/results.json` + `report.md`,
`research/round32/reverse/aw1/output/results.json`, `research/round32/skeptic/aw1.md`
+ `aw1.json` + `aw1-independent/results.json`, `research/round32/contracts/aw2.json`,
`research/round32/forward/aw2/output/results.json` (AW2 is frozen; its
review is pending -- treated here as provisional data, not as an
admitted result), and `research/round32/experts/historical/assistant-1/`'s
README and scripts.

Run every script with `python3 -B <script>.py` (also confirmed
byte-behaviourally under `python3 -B -O <script>.py`: every `overall_pass`
is `true` under both interpreters; the few `assert` sanity checks that
`-O` strips are internal geometry sanity checks, never the pass/fail
gate itself, which is always a plain boolean).

## What passed

All five scripts pass (`overall_pass: true` in each, and in the combined
`results.json`).

**T1 `flip_full_enumeration.py`.** Every one of the 1536 plaquettes of an
independent 8x8x8 fine block (3 orientations x 512 base points) meets
the AW1 flip set `E={(p,x):p_y even} u {(p,y):p_z even} u {(p,z):p_x even}`
in an ODD number of links: zero even intersections, split exactly
768/768 between "1 link" and "3 links". A translation-covariance
cross-check independently confirms the expected 24 (orientation, parity)
classes, all odd. A damaging mutation (dropping one link from `E`) is
confirmed to turn `W`'s own face intersection even (3 -> 2), showing the
odd-intersection property is not vacuous.

**T2 `k2_reassembly.py`.** The AM2-remainder term `rho = 352 J T`
(`J=28|tau|`, `t_1=49|tau|/144`, `T=t_1/(1-352J)`) is reassembled from
scratch as a Fraction and found to equal, bit-for-bit, the value
independently exported by all three of the forward AW1 producer, the
reverse AW1 producer and the skeptic's pre-comparison itemization
(`3773/11248891200000000` at `tau=10^-8`). Reassembling the remaining
exact-tier terms (`straddling=T(6a+rho)`, `two_creation=(33a+rho)^2`,
`density=min(eps_F,eps_R)^2` with `eps_F=2T+T^2` the AV1/forward form and
`eps_R=82a+2rho+(33a+rho)^2` the reverse's 82-face refinement,
`normalization_order=a*eps_min^2`, overlap multiplier folded in as 1)
gives a minimal `K_2` whose coefficient, `3354.4994258651045`, matches
the skeptic's own exported `K2_exact_tier_minimal_accepted` **bit-for-bit**
-- an independent confirmation that the skeptic's accepted minimal form
is correctly reconstructible from the report's stated formulas alone.
Every one of the four exported/admitted `K_2` values dominates it: the
forward's own headline (`~3354.638`), the reverse's headline
(`~3354.499`, barely above the minimal), the skeptic's admitted/gate
bound (`~3354.803`), and the task's literal gate-bound number (identical
to the skeptic's).

**T3 `tau_aw2_rule.py`.** Reading `K_2^+` independently from both the
live `advisor/aw1-gate.json` and `contracts/aw2.json` (confirmed to
agree with each other bit-for-bit), the frozen decade-grid rule
(`K_2^+ tau <= 1/288`, largest `tau` in `{10^-8,10^-9,...}`) is
re-evaluated over the grid from scratch and returns `tau_AW2 = 1/10^8`,
matching `research/round32/forward/aw2/output/results.json`'s exported
`tau_AW2` exactly. An off-grid mutation (`10^-7`, outside the model's own
`|tau|<=10^-8` cap) is confirmed absent from the scanned grid by
construction.

**T4 `sign_margin_replay.py`.** The AW2 enclosure endpoints
`[tau/144 - K_2^+ tau^2, tau/144 + K_2^+ tau^2]` at both `tau=+10^-8` and
`tau=-10^-8`, the exclusion margin `(|tau|/144-K tau^2)/(K tau^2)`
(`~206.00`) and the sign margin `1/(144 K |tau|)` (`~207.00`) are
recomputed independently and found to equal the AW2 forward producer's
exported rationals bit-for-bit at every one of six compared quantities
(both enclosure endpoints at both signs, both margins); both margins
comfortably exceed the contract's threshold of 2, and both signs
strictly exclude 0.

**T5 `wrong_face_replay.py`.** An exact Haar computation, re-deriving the
per-face coefficient `c^(1)_f = -(tau/72) W_f Omega_0` from I1.5's
`phi_b=-(tau/3) sum W_f`, `V_b=phi_b/8` and the energy-3 eigenvalue of
`W_f Omega_0` (giving `H_0^{-1}` factor `1/3`), shows that among the 10
omitted faces with owner set `R={0,e_z}` (the 6 xz classes `r=0,1,2;
s=0,1` and the 4 yz classes `r=0,1,2,3; s=0`), only `f=W` (the xz,
`r=0,s=0` class) gives a nonzero first-order contribution to `omega(W)`,
with the exact value `tau/144` (via `E[W^2]=1/4`, independently
re-derived by the Clebsch-Gordan/Catalan and Weyl/Wallis routes). Every
other one of the 9 faces gives exactly `E[W W_f]=0`, hence contribution
0, by the odd-link-multiplicity vanishing argument (two distinct
plaquettes share at most one fine link, confirmed exhaustively over all
10x9 ordered pairs). A damaging mutation claiming a different face as
the sole contributor is rejected, and the naive sum over all 10 faces is
confirmed to equal `tau/144` only because 9 of the 10 terms are exactly
zero, not by any other cancellation.

## What failed

Nothing failed in the final scripts.

## Three planning notes for the lens, sub-round 3

`research/round32/advisor/plan.json`, `selection-ax1.md` and
`deliberation-2.md`/`-3.md` name AX1/AX2 as sub-round 3's investigation:
the uniform Kogut-Susskind SU(2) Hamiltonian at fixed spacing, via
**route B** and a re-frozen `J_0`.

1. **Route B's geometry is a direct extension of this sub-round's flip
   and owner-set machinery, not a new derivation from scratch.** Route B
   keeps the Haar product reference and moves the three selected xy
   faces per factor into the interaction as single-factor groups
   (`selection-ax1.md`, `deliberation-1.md` item 4): `J'=29|tau|`
   (up from AW1's `J=28|tau|`), reset `102|tau|`, exactly two selected
   groups (six faces) meeting `R`, `||B_N||<=51|tau|/8`, labelled
   "uniform Kogut-Susskind SU(2) at fixed spacing, `g^4=96/tau`"
   (`~9.6x10^9` at the cap; never "weak coupling"). `T1`'s
   `face_links`/`in_E` module and `T5`'s owner-set enumeration both
   generalize directly: the three newly-interacting xy classes change
   the 49/15/82 face-and-owner-set counts (AW1's frozen values) to a new
   49+3=52-per-factor count with a modified owner-set table, and the
   flip set `E`'s odd-intersection property (T1) is a purely
   link-geometric fact independent of which faces are "selected" vs.
   "omitted" -- so `U_E` still exists and still flips every plaquette
   under route B, but AW1's specific antisymmetry statement
   (`kappa=0` only) will need re-examination once three more per-factor
   faces carry nonzero coefficients (the AW1 report's own unreviewed
   remark on `E*` in section 3.3 is directly relevant here: a modified
   flip set that meets every *interacting* plaquette oddly and every
   *still-omitted* one evenly is exactly the kind of object route B's
   larger interacting set will need).

2. **The `J_0` re-freeze is a numeric contraction check that this
   assistant's toolchain can replay verbatim once AX1 states its
   constants.** `deliberation-1.md`/`-2.md` and `selection-ax1.md` fix
   the re-frozen coupling at `J_0'=29/10^8` with the exact contraction
   checks `1073/175000000<1/64` and `319/1562500<1` (both simple
   Fraction comparisons). `T2`'s `k2_reassembly.py` pattern -- reading
   the producer's exported terms, reassembling them independently from
   the stated formula, and checking bit-for-bit / domination -- is the
   template for a sub-round-3 `j0_refreeze_replay.py`: recompute `J_0'`
   from route B's per-factor face count and the four-incoming-stars
   argument (as `T5` did for AW1's `J=28|tau|`), confirm the two named
   contraction inequalities as exact Fractions, and confirm every
   AM2-derived downstream constant (the analogue of AV1's `T`, `eps`,
   `D_ii`) that route B needs is still self-consistent at the *new*
   `J_0'`, not silently reusing AW1's `J=28|tau|`/`352` self-consistency
   constant where AX1's `29|tau|`/route-B-specific majorant coefficient
   belongs.

3. **T4's enclosure/margin replay pattern is reusable for AX-level
   sign or enclosure claims, but only once route B produces its own
   `K_2`-analogue and coupling rule; nothing in this sub-round's five
   tests transfers a *number* to AX1/AX2.** `sign_margin_replay.py`'s
   structure (recompute `[first_order - K tau^2, first_order + K tau^2]`,
   the exclusion margin and the sign margin, all from a contract-frozen
   `K` and a contract-frozen coupling, then diff bit-for-bit against the
   producer's export) is exactly the shape any AX-level sign or
   enclosure result will need to replay, since AX1/AX2 is paired
   (`paired-physics-research`) the same way AW1/AW2 was. But route B
   changes the first-order coefficient itself (the "selected" xy faces
   moving into the interaction changes which faces are "omitted" and
   hence which `E[W W_f]` sums enter `omega(W)`'s first order), so
   `T5`'s specific `tau/144` value and its per-face table do **not**
   carry over unchanged -- only the *method* (Haar odd-multiplicity
   vanishing plus the energy-3/`H_0^{-1}` chain) does. A sub-round-3
   assistant script should re-run `T5`'s method against route B's own
   (larger) set of "omitted, non-selected" faces before assuming the
   coefficient is still `1/144`.

## Files

- `flip_full_enumeration.py` -- T1, full 8x8x8-fine-block enumeration of
  odd `|face_links(f) & E|` in all three orientations, plus a
  translation-covariance cross-check and a damaging-mutation control.
- `k2_reassembly.py` -- T2, independent Fraction reassembly of the
  exact-tier `K_2` terms (`am2_remainder=352JT`, `straddling`,
  `two_creation`, `density`, `normalization_order`, overlap multiplier
  1), diffed against the forward/reverse/skeptic exports and the
  gate-bound `K_2^+`.
- `tau_aw2_rule.py` -- T3, independent re-evaluation of the AW1-frozen
  decade-grid rule for `tau_AW2` from the gate-bound `K_2^+`.
- `sign_margin_replay.py` -- T4, independent recomputation of the AW2
  enclosure endpoints, exclusion margin and sign margin at both signs of
  `tau`, diffed bit-for-bit against the AW2 forward producer's export.
- `wrong_face_replay.py` -- T5, exact Haar computation isolating `f=W`
  as the only nonzero first-order contributor to `omega(W)`, value
  exactly `tau/144`.
- `results.json` -- combined pass/fail and full raw output from all five
  scripts.
