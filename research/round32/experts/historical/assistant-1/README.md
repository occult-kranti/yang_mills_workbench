# Historical lens (Newton/Tesla) assistant scripts -- Round32 sub-round 1

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted assistant scripts for the
Newton/Tesla historical lens, run after AV1/AV2's sub-round 1 per
`research/round32/experts/historical/loop3-signoff.md` section 3. These
scripts and this note count **zero research loops**: they are tests and
planning material for the lens, not a producer, skeptic or advisor
artifact. Nothing here reads `research/round32/forward/av1/check.py` or
`research/round32/reverse/av1/check.py`, and nothing here is read by, or
feeds back into, AV1's admitted evidence.

Read before writing: `loop3-signoff.md` section 3, `research/round32/advisor/av1-gate.json`,
`research/round32/forward/av1/report.md` + `output/results.json`,
`research/round32/reverse/av1/report.md` + `output/results.json`,
`research/round32/skeptic/av1.md`, `research/round32/contracts/av2.json`,
`research/round21/forward/i1/report.md` sections 3-4, and (for the
retained Poisson controls in S3) `research/round31/forward/at4/report.md`
+ `output/results.json`.

Run every script with `python3 -B <script>.py`.

## What passed

All three scripts pass (`overall_pass: true` in each, and in
`results.json`).

**S1 `haar_parity_exact.py`.** Two independent exact routes (SU(2)
Clebsch-Gordan / Catalan-number trivial-multiplicity counting, and the
Weyl-integration Beta-function/Wallis-integral reduction, with pi
cancelling symbolically -- no floats, no sympy) agree on every one of
`E[w^0..4] = 1, 0, 1/4, 0, 1/8`, reproducing AV1's `reference_moments`
(`omega_0(W)=0`, `omega_0(W^2)=1/4`) exactly. The original xz Wilson
face `W = (1/2)Tr[U_{0,x}U_{e_x,z}U_{e_z,x}^{-1}U_{0,z}^{-1}]` (AT4-F04)
is reconstructed explicitly from the I1.4 tail rule and shown to consist
of four distinct, independent fine links, so `W` is itself Haar
distributed exactly like a single link -- giving `E[W]=0`, `E[W^2]=1/4`
without any separate character computation. All 21 omitted I1 classes at
`W`'s own anchor star (research/round21/forward/i1/report.md section 3)
are reconstructed the same way; `E[W^2 * W_f]` is shown to vanish for
every one of them, including `f=W` itself (`E[W^3]=0`), by exhibiting an
odd total link-multiplicity in every case. Independently confirmed along
the way: two *distinct* omitted faces of this star share at most one
link (matches AV1's own `first_order_face_enumeration` check,
`max_links_shared_by_distinct_faces: 1`).

**S2 `am2_tiers_exact.py`.** The 49 omitted faces per factor, their 15
owner sets and multiplicities `[1,1,1,1,1,2,2,2,3,3,4,4,4,10,10]`, and
the 82 faces meeting `R={0,e_z}` (16 of the 49+49 touching both `0` and
`e_z`) are all independently re-derived from the I1 table by translation
covariance -- not imported, not hard-coded, not read from either
producer's `check.py`. From this enumeration, `t1 = 49|tau|/144` and
`J = 28|tau|` are derived from first principles (21 omitted faces per
star / |S|=4 stars per site), and the self-consistent
`T = t1/(1-352J)` is evaluated exactly. The forward formula
`D = 2*eps*(1+eps)/(1+eps^2)`, `eps=2T+T^2`, reproduces
`585079838465912592144137406066050/42981220507576537932303142777593983768257`
(`~1.36124528702e-8`) **bit-for-bit** against
`research/round32/forward/av1/output/results.json`'s exported
`headline.D_ii_plus`. The reverse formula
`D = 2*eps/sqrt(1+eps^2)`, using the crude 82-face sum
`a1=82|tau|/144` and the directed bound `sqrt(1+eps^2)>=1`, gives a
valid directed rational upper bound `~1.13902e-8`, consistent with (and
slightly more conservative than) the reverse producer's own exported
`1.1390230555394726e-8`. Both `D_ii<=4/10^7` at both signs, and both the
forward and the (bound on the) reverse `D_ii(tau)/D_ii(tau/100)` ratios
land at `~100.01`, inside `[99,101]`.

**S3 `window_kernel_budget.py`.** With a directed rational (Machin)
enclosure of pi (width `<10^-30`) and the AV1-admitted forward tier-(ii)
`D` (cross-read from both `research/round32/advisor/av1-gate.json` and
`research/round32/contracts/av2.json`, and cross-checked against S2's
own independent re-derivation), `E = M_0(D+D^2) + kM_1` gives
`E ~ 1.832e-7 < 10^-6` at tier (ii) and `E ~ 3.600e-5` (once-iterated
tier i) to `~4.752e-5` (crude tier i), both `> 10^-6`, at tier (i) --
matching the signoff's expected `1.7-2.0e-7` and `3.6-4.7e-5` windows
exactly (the range's two ends are the iterated and crude tier-i values
respectively). The crossover `s*` (directed bracket) is
`[6.236863446033457, 6.236863446033457]` (a single float value once
rounded, degenerate at this pi precision), inside `[6.1,6.3]`. The AT4
`L=10^4` Poisson certificate radius is reproduced **exactly** by summing
AT4's own four frozen exact-rational cost terms
(`research/round31/forward/at4/output/results.json`): total
`0.0008415187043862666`, matching AT4's exported `absolute_error_upper`
bit-for-bit and confirmed `>10^-6` (rejected). The "optimized Poisson
floor" is reproduced as a labelled **float preview only** (per this
project's floating-point-is-a-preview convention, and because
`research/round32/advisor/selection-av2.md` itself calls it a preview):
minimizing `(k/pi)ln(1+L^2)+1/(pi L)` over integration cutoff `L` gives
a floor of `~1.265088e-6` at `L* ~ 4.0816e6`, matching the expected
`~1.2651e-6` at `L~4.08e6`, and still `>10^-6` (rejected).

## What failed

Nothing failed in the final scripts. One internal bug was caught and
fixed during development: S1's first draft flagged "faces share at most
one link" as violated, because the local anchor star's own 21 omitted
classes include `W` itself (the `xz, r=0, s=0` class) -- `W` sharing all
four links with itself is expected (it is the `f=W` / `E[W^3]` case),
not a violation of the *distinct*-faces claim. The check was corrected
to separate `f=W` from the 20 genuinely distinct faces before applying
the "at most one shared link" assertion; both the corrected distinctness
check and the `f=W` vanishing check now pass.

Two scope notes, not failures: (1) the "352" self-consistency
coefficient (`G'(R)<352`) is used exactly as AV1/AV2 state it, not
re-derived from the AM2 exponential majorant series here -- that
re-derivation is AM2/AV1's own eighth-order work, out of scope for an
assistant script. (2) the reverse `D_ii` bound uses the elementary
`sqrt(1+eps^2)>=1` estimate rather than reverse's own tighter directed
square-root machinery, so it is intentionally more conservative than
(not bit-identical to) the reverse producer's exported value; the
assignment only requires the *forward* value to match exactly.

## Three planning notes for the lens, sub-round 2 (AW1: parity theorem, flip antisymmetry, K_2)

`research/round32/advisor/plan.json` names AW1 as "Peter-Weyl parity
theorem, exact link-flip antisymmetry `omega_{-tau}(W)=-omega_tau(W)`,
exact first-order Wilson mean 1/144 and itemized second-order remainder
K_2" (`research/round32/contracts/aw1.json` items 1-4). All three items
overlap directly with what these scripts already computed:

1. **Parity theorem (AW1 item 1).** S1 already proves, exactly and by
   two independent routes, every fact AW1 item 1 asks for on the AV1
   model: `E[W]=0`, `E[W^2]=1/4`, `E[W^3]=0`, `E[W^4]=1/8`, and
   `E[W^2*W_f]=0` for every omitted face `f` of `W`'s star including
   `f=W`. AW1's contract sketches a proof via the energy-24 multiplet
   splitting under `H_0`; S1's "W is Haar-distributed because one of
   its four links is free" argument (Part B) is a genuinely different,
   shorter route to the same `E[W^2]` and `E[W^4]` values and is worth
   offering to AW1's producers as an independent cross-check, not a
   replacement -- the multiplet-splitting route additionally certifies
   "no omitted face maps the energy-24 vector back into itself except
   through the identity component," which the Haar-distribution
   shortcut does not by itself address.

2. **Flip antisymmetry (AW1 item 2).** AW1 needs, for a flip region `E`
   and the central-element unitary `U_E`, that "every elementary
   plaquette of Z^3 meets `E` in an odd number of links," enumerated by
   translation covariance across the three orientations (xy, xz, yz).
   S1's `face_links`/`owner_factor`/`DIRS` geometry already builds
   exactly this kind of object (a face's four `(tail,direction)` link
   identifiers, and multiplicity/parity counting against an arbitrary
   link set) and already enumerates all three orientations' omitted
   classes from the I1 table. A sub-round-2 assistant script could reuse
   this module directly: once AW1's producers fix a concrete region `E`
   (a half-space is the natural candidate, but that choice belongs to
   AW1, not to this note), count `|face_links(...) & E_links|` for a
   translation-covariant sample of faces in each of the three
   orientations and confirm the count is odd in every case, mirroring
   the odd-multiplicity checks S1 already runs for the parity theorem.

3. **K_2 enumeration (AW1 item 4).** S2's `am2_constants()` /
   `forward_D()` already compute, exactly, several of K_2's named
   itemized pieces on the AV1 model at `tau=10^-8`: `J=28|tau|` and the
   self-consistent remainder `T=t1/(1-352J)` (AW1's "AM2 remainder
   term"), and the two-creation term `T^2` (already split out of
   `eps=2T+T^2` in `forward_D`). S2's reverse-route `a1=82|tau|/144`
   (the crude sum over faces meeting `R`) is a ready-made ingredient for
   AW1's "straddling-support pairing with outside excitations" item.
   AW1 item 4 also names a "multiplier for the overlap with
   `W Omega_R`" and states `||W Omega_R||=1/2`; S1 computes exactly this
   quantity independently (`omega_0(W^2)=1/4`, so
   `||W Omega_R||=sqrt(1/4)=1/2`), which is a clean, already-exact
   cross-check of that stated constant. A sub-round-2 assistant script
   should extend `am2_tiers_exact.py`'s tier-labelled structure (rather
   than re-deriving `J`, `t1`, `T` from scratch) to assemble `K_2^+` at
   both the exact and the crude tier, keeping AV1/AV2's discipline of
   naming every term's tier and rejecting tier mixing.

## Files

- `haar_parity_exact.py` -- S1, exact SU(2)/Peter-Weyl Haar moments and
  link-wise odd-multiplicity vanishing.
- `am2_tiers_exact.py` -- S2, independent I1 face enumeration, AM2 tier
  constants, forward/reverse `D_ii` reproduction.
- `window_kernel_budget.py` -- S3, directed-pi window-kernel radius `E`,
  crossover `s*`, and the two retained Poisson controls.
- `results.json` -- combined pass/fail and key numbers from all three
  scripts (summary plus each script's full raw output).
