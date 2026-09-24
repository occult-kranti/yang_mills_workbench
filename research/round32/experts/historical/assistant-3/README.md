# Historical lens (Newton/Tesla) assistant scripts -- Round32 sub-round 3

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted assistant scripts for the
Newton/Tesla historical lens, delivering the five tests requested in
`research/round32/experts/historical/update-2.md` section 5. These
scripts and this note count **zero research loops**: they are tests and
planning material for the lens, not a producer, skeptic or advisor
artifact. Nothing here reads or imports `research/round32/forward/ax1/
check.py` or `research/round32/reverse/ax1/check.py`; every geometric
and arithmetic construction is re-derived from the frozen contract,
gate and report text plus the two producers' exported `output/
results.json` (data, never code). `research/round32/contracts/ax2.json`
is `frozen_before_production` -- it is treated throughout as a
**provisional premise**, never as an admitted result, and script 5's
output is explicitly labelled a planning preview.

Everything numeric is `fractions.Fraction`; no floats appear in any
pass/fail comparison (decimal previews are for readability only).

Read before writing: `update-2.md` section 5, `research/round32/advisor/
ax1-gate.json`, `research/round32/forward/ax1/report.md` + `output/
results.json`, `research/round32/reverse/ax1/output/results.json` (and
the corresponding sections of `reverse/ax1/report.md`), `research/
round32/skeptic/ax1.md`, `research/round32/contracts/ax2.json`, and
this lens's `assistant-1/` (`am2_tiers_exact.py`, `haar_parity_exact.py`,
`window_kernel_budget.py`) and `assistant-2/` (`wrong_face_replay.py`,
`sign_margin_replay.py`) work, reused throughout per the assignment's
own instruction (reuse assistant-1/-2; no producer imports).

Run every script with `python3 -B <script>.py` (also confirmed
byte-identical under `python3 -B -O <script>.py` for all five scripts).

## What passed

All five scripts pass (`overall_pass: true` in each, and in the combined
`results.json`). Every numeric quantity below was cross-checked
bit-for-bit, as an exact `Fraction`, against **both** the forward and
the reverse AX1 producers' exported `output/results.json`, not just
against the contract or gate text.

**T1 `j0_contraction_replay.py`.** `exp(1/8)<8/7` is re-proved from
scratch (a 10-term Taylor truncation plus an exact geometric tail
bound, independent of the report's own truncation degree), and fed
through the same arithmetic chain the AX1 report states to reproduce
`G(1/64)<148/7` and `G'(1/64)<352` literally. Route B's `J'=29|tau|`
is independently re-derived from its additive structure (4 stars x
7|tau| + 1 single-factor group x |tau|). The re-frozen `J_0'=29/10^8`
is shown to equal `J'` at the cap, and the two named contraction
rationals `1073/175000000<1/64` and `319/1562500<1` are reproduced
exactly, matching both producers' `j0_resolution` blocks in every
field. The old `J_0=7/25000000=28/10^8<29/10^8=J_0'` confirms the
re-freeze is upward (R1), not a loosening.

**T2 `uniform_face_count.py`.** Extends assistant-1's translation-
covariant owner-set method (`am2_tiers_exact.py`'s `OMITTED_CLASSES`,
imported, not copied) with route B's 3 new selected classes (support
`{0}` each). A sanity gate first reproduces the 21-class, omitted-only
case's `49`/`15`/`82`/`16` numbers exactly against assistant-1's own
function before trusting the extension. The full 24-class route-B
enumeration then gives, independently: **52** faces per factor (16
owner sets, multiplicities `[1,1,1,1,1,2,2,2,3,3,3,4,4,4,10,10]`,
matching the forward producer's exported multiplicities bit-for-bit),
**88** faces meeting `R={0,e_z}`, **16** faces inside `R`, and **6**
selected faces meeting `R`. The contract's candidates `96=4x24` and
`168=7x24` are confirmed to be naive per-anchor overcounts, strictly
above the derived exact counts (52 and 88 respectively), matching both
producers' `face_enumeration` blocks and their own labelled bounds.

**T3 `route_b_incidence_table.py`.** Generalizes assistant-1's/
assistant-2's anchor-0 face-link builder (`face_links`, `owner_factor`,
imported from `haar_parity_exact.py`) to an arbitrary anchor `b`, via
the AX1 report's own tail rule `(4b_x+r,2b_y+s,b_z)`; a sanity gate
confirms the generalized builder reduces to assistant-1's own anchor-0
build exactly at `b=0`. The 7 star anchors and 2 single-factor anchors
that meet `R` are independently derived (as `R-S` and `R`, `S={0,e_x,
e_y,e_z}`) rather than asserted, and match the reverse producer's
exported incidence-table anchors exactly, including the anchor **list**
(`(-1,0,0),(-1,0,1),(0,-1,0),(0,-1,1),(0,0,-1),(0,0,0),(0,0,1)`
for the stars; `(0,0,0),(0,0,1)` for the single-factor groups). Every
one of the resulting **153** faces is built as an actual fine-link
object and keyed by its exact link set: zero duplicates are found
(`no_face_charged_twice: true`), and of these 153, exactly 88 meet `R`
and 16 lie inside it, agreeing with T2's abstract owner-set count from
an entirely independent (concrete link-level) construction. The norm
bound `||B_N||<=(7x7+2x1)|tau|/8=51|tau|/8` is reproduced exactly and
matches both producers' exported `B_N_over_abs_tau`.

**T4 `uniform_state_tiers.py`.** From `t_1'=52|tau|/144` and
`T'=t_1'/(1-352J')`, `eps=2T'+T'^2` reproduces the forward's admitted
`D'_ii=2425369125199104794263242601250/
167893028420061547330293754713793182097` (`~1.44459e-8`) bit-for-bit,
matching every intermediate the forward exports (`t1`, `T'`, `eps`, the
pair term, `J`). The reverse's labelled "88-face" variant
(`a1=88|tau|/144` in place of the forward's implicit `2x52`-face
double-count, `rho'=352J'T'`, `eps=a1+2rho'+T'^2`, `D=2eps`) reproduces
`~1.22237e-8` bit-for-bit against the reverse's exported
`D_exact_2eps`, and the skeptic's own exact identity
`eps_fwd-eps_rev=16|tau|/144=|tau|/9` is confirmed directly as a
`Fraction` equality. The tau-scaling ratios `D(tau=10^-8)/D(tau=10^-10)`
land at `100.0101` (forward) and `100.0119` (reverse variant) --
matching the skeptic's own independently reported ratios to four
significant figures -- both comfortably inside `[99,101]`.

**T5 `ax2_budget_preview.py`.** `D'` is read and cross-checked
bit-for-bit across **four** independent sources (the AX2 contract's own
`parameters.D_prime`, the AX1 gate's `decision` text, the forward AX1
producer's export, and this sub-round's own T4 re-derivation) before
being used. With `k'=51|tau|/4`, `M0=2`, `M1=4s/pi` and a directed
Machin-formula rational enclosure of pi (imported from assistant-1's
`window_kernel_budget.py`, exactly the AV2-window template the AX2
contract says to apply verbatim), `E'=M0(D'+D'^2)+k'M1` at `tau=10^-8`,
`s=1` encloses (as exact rationals, decimal preview `~1.9123e-7`) well
below the `10^-6` target (a margin of `>=5.229`, matching the skeptic's
own independently stated `~5.23`). The crossover `s*` (where `E'`
would reach `10^-6`) is enclosed to width `<10^-20`, decimal preview
`~5.982`. Every output is explicitly labelled a **planning preview**
(`claim_flags.ax2_gate_status`): AX2 is `frozen_before_production` and
has not been produced or gated, so nothing here is an admission.

## What failed

Nothing failed. All five scripts, and every one of their cross-checks
against the forward and reverse AX1 producers' exports, pass.

## Three planning notes for the lens, sub-round 4

`research/round32/advisor/plan.json` and `selection-ay1.md` name AY1 as
sub-round 4's investigation: "uniform local closeness of all AQ-type
subsequential states and the boundary-independent first-order density
(paired)," with **two named construction families** (the AQ1 centered
whole-star boxes and the I1 all-contained-face boxes with padding) and
a common clock; AY2 then states what remains unproved.

1. **T4's forward-vs-reverse "two valid bounds from the same
   ingredients" pattern is exactly AY1's own two-family comparison, one
   level up.** This sub-round's `D'_ii` story is not a discrepancy to
   resolve but a template: two independently-constructed exact bounds
   (forward's `2T'+T'^2` collection vs. the reverse's `88`-face
   collection) both certify the same target, differ by an exact,
   fully-itemized amount (`|tau|/9`), and the larger, more
   conservative one is the one that should be bound. AY1 will need
   precisely this discipline for its **two construction families**
   (AQ1 whole-star boxes vs. I1 all-contained-face boxes): expect two
   valid closeness bounds, not one, an exact itemized difference
   between them, and a stated reason (as the skeptic gave here: "uses
   no 88-face refinement, so stays valid even if the refinement were
   disputed") for which one AY1's gate should bind. A sub-round-4
   assistant script should be ready to reassemble both families' bounds
   from scratch and confirm any claimed difference is a named, provable
   quantity -- not an unexplained residual.

2. **T3's "no face charged twice" itemization is the right shape for
   AY1's "boundary-independent" claim, but the boundary itself changes
   family to family.** Route B's incidence table (7 stars + 2 single-
   factor groups, 153 faces, zero duplicates) worked because every
   charged group's support was checked to lie inside the box by
   construction. AY1's second family (I1 "all-contained-face boxes
   with padding") uses a genuinely different boundary rule from AQ1's
   centered whole-star boxes, so the same face could in principle be
   owned by one family's boundary convention and not the other's. A
   sub-round-4 script should build both families' charged-face sets
   independently (T3's link-set-keyed approach generalizes directly)
   and confirm they agree on every face that lies in BOTH families'
   boxes, before trusting that the "boundary-independent" first-order
   density is the same object under either convention -- not merely
   that both formulas happen to output the same rational.

3. **T5's four-source `D'` cross-check (contract, gate, producer
   export, independent re-derivation) is the minimum bar AY1's own
   state bound should clear before AY2 is allowed to compute anything
   from it, but AY1 will not have a T4-style prior sub-round's
   `D'` to just look up.** Route B's `D'` transferred cleanly into this
   sub-round because AX1 had already frozen and gated it; AY1's
   "boundary-independent first-order density" is a NEW quantity, so a
   sub-round-4 assistant script cannot simply re-read it from an
   existing gate -- it will need to reassemble it from AY1's own report
   once frozen, the way T1-T4 reassembled AX1's constants from its
   report's stated formulas rather than its final numbers, and only
   then cross-check the reassembly against AY1's export. `window_kernel_
   budget.py`'s directed-pi/AV2-window machinery (reused again in T5)
   is likely to be needed a second time once AY2 (or a later sub-round)
   asks what an AY1 closeness bound implies for a dynamical-window
   radius -- but only once AY1 itself is frozen and gated, not before.

## Files

- `j0_contraction_replay.py` -- T1, independent proof of `exp(1/8)<8/7`
  (fresh truncated-series + tail bound), reproduction of `G(R)<148/7`,
  `G'(R)<352`, `J'=29|tau|`, `J_0'=29/10^8`, and the two exact
  contraction rationals, diffed bit-for-bit against both producers.
- `uniform_face_count.py` -- T2, translation-covariant owner-set
  enumeration of the 24 anchored route-B classes (52/88/16/6), with a
  sanity gate against assistant-1's 21-class numbers and a check that
  96/168 are only naive bounds.
- `route_b_incidence_table.py` -- T3, face-by-face (fine-link-level)
  itemization of the 7 stars + 2 single-factor groups meeting `R`
  (153 faces, zero double charges), and the `||B_N||<=51|tau|/8`
  norm bound.
- `uniform_state_tiers.py` -- T4, independent reassembly of the forward
  and reverse tier-(ii) state bounds from their stated formulas, the
  exact `eps_fwd-eps_rev=|tau|/9` identity, and the tau-scaling ratio
  checks.
- `ax2_budget_preview.py` -- T5, a labelled AX2 window-radius preview
  (`E'=2(D'+D'^2)+51|tau|/pi`) and crossover `s*`, using a directed
  Machin-formula pi enclosure reused from assistant-1's
  `window_kernel_budget.py`.
- `results.json` -- combined pass/fail and full raw output from all
  five scripts.
