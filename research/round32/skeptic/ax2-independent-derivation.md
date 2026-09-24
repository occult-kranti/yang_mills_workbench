# AX2 independent derivation (skeptic replay, before comparison)

**Standing.** I wrote this after the AX2 contract froze (`frozen_at` 2026-09-24T01:30:56Z, sha256 `da72afe3…992b`) and before reading anything under `research/round32/forward/ax2/`. My sources were: the frozen contract and `selection-ax2.md`; `advisor/ax1-gate.json` (sha256 `1b8fb152…d177`, pinned) and `advisor/av2-gate.json`; my own `ax1.md`, `av2.md`, `av2-independent-derivation.md` and `av2_check.py`; the admitted `forward/av2/calculator.py`, as a hash-pinned comparator only.

**Incidental exposure.** Listings showed that `forward/ax2` and `/tmp/claude-0/ax2-private` exist, and `git status` shows an untracked `forward/ax2/calculator.py`. I opened none of them.

AX2 has a single producer, so this replay is a required admission input. I am a model-agent skeptic with correlated ancestry: I share the model family of the advisor and the producer. My AX1 review already printed the feasibility value 1.9123e-7. This is not human review.

Exact values come from `ax2_check.py`. Its output, `ax2-independent/results.json`, has 72 checks, including all 25 contract controls. Decimals are previews. Human project author: Hruday N M (BUNZEEY).

## 1. The transfer: only `k'` and `D'` change
**The lemma.** The AV2 lemma needs two premises: (a) the spectral measure `eta` of `chi=(pi(W)-m)Omega` for `G=H/alpha` is positive, has mass at most 1 and is carried by `[0,inf)`; (b) `|c-c_0|<=k|theta|+D+D^2` holds for every real `theta`.

It then gives `C(s)=int ghat c` and `|C-C_0|<=M_0(D+D^2)+kM_1`. AX1 item 3 re-applies AQ1 nonnegativity, GNS and stationarity verbatim. No gap is used.

**Window constants.** Recomputed by the annihilator–jump route (`[g''']_0=-8s^3`) and Wallis, they are unchanged: `ghat=4s^3/(pi(s-i theta)^3(s+i theta))`, `M_0=2`, `M_1=4s/pi`, `M_2=2s^2`.

**Reference and free correlation.** `h_b=8 sum_e C_e` does not depend on `tau`, so `P_R` stays the Haar product, and the selected xy faces enter only `V`, as `psi_b=-(tau/3) sum W_g`. The Wilson face has the free z links `(0,z)` and `(e_x,z)`, and no selected face contains a z link. So the face holonomy is Haar: `W=q_0` on `S^3`, with `E[W]=0`, `E[W^2]=1/4` and `E[W^4]=1/8`. `W Omega_0` has `G_0`-eigenvalue `8·4·(3/4)/8=3`.

Hence `c_0=e^{3i theta}/4` and `C_0(s)=e^{-3s}/4`, the contract's `exp(-3)/4`.

**Slope `k'`.** Seven whole stars (anchors `R-S`) and exactly two single-factor groups (anchors `0` and `e_z`, support `{b}`) meet `R={0,e_z}`. The enumeration is identical on N=2, 3 and 4. Faces meeting `R` number 21, 21, 16, 8, 8, 4, 4 in the stars and 3, 3 in the groups: 153 faces charged, 88 meeting `R`, 16 inside `R` and 6 selected.

A star has norm `7|tau|/8` and a group `|tau|/8` (in `G` units), so `||B_N||<=51|tau|/8`. The relative-unitary Duhamel bound (AT4 F10–F11) then gives `k'=51|tau|/4` for every real `theta`, uniformly in the box. The extensive norm grows with N, so it is rejected.

**How `D'` enters.** `W alpha^0_theta(W)` lives on `R` and has norm at most 1, so trace duality gives `D'`. It does not give `D'/2`, because the operator is not an effect (toy: `|Tr(Delta A)|=4||Delta||_1/5`). The uniform first-order mean is `+tau/144≠0`, so `m^2<=D'^2` is charged.

**Where `D'` comes from.** It is read from the AX1 gate decision ("Bind the forward D'_ii = …") and equals the contract string. I recomputed it at both signs from `t_1'=13/3600000000`, `T'=13/3599632512`, `rho'=4147/11248851600000000`; `eps=2T'+T'^2` and `D'=2eps(1+eps)/(1+eps^2)`.

The same code identifies the values that are **not** substituted: the reverse refinement (≈1.22237e-8), the AX1 target `1/2500000`, the zero-selected `D` (≈1.36125e-8) and tier (i) (≈2.4526e-5). The formula increases in `|tau|`, so the gate value bounds every `|tau|<=10^-8`.

## 2. Radius at tau=+10^-8, s=1
`E'=2D'+2D'^2+51|tau|s/pi+arithmetic`.

| Term | Exact | Preview |
|---|---|---|
| state `2D'` | `4850738250398209588526485202500/167893028420061547330293754713793182097` | 2.8891838429e-8 |
| mean square `2D'^2` | exact (140 chars) | 4.1736916389e-16 |
| kernel `51·10^-8/pi_lo` | `15937500000000000000000000000000000000000000000000000/98174770424681038701957605727484465131161543730472056905467` | 1.6233804195e-7 |
| arithmetic (half-width of `e^{-3}/4`) | `1/(8·10^60)` | 1.25e-61 |

**Enclosures.** For `pi`, Hutton's formula rounded outward to `10^-60`. It overlaps Machin and the calculator's `10^-40` interval; the lower end is used, and the rounding slack sits inside the kernel term. For `e^{-3}`, Taylor with a geometric remainder, halving, outward squaring and inversion. It lies inside the calculator's enclosure.

**Radius.** The exact rational has 388 characters. Rounded outward it is `R'=1912298807996871790146581299723633/10^40`, about **1.9122988080e-7**.

**The Boolean `E'<=10^-6` is true**, with margin at least `1307327071/250000000` (about 5.2293).

**Datum and interval.** My datum is `19914827347145577191736966260024710652679836875369286227051/(16·10^59)`, about 0.012446767091965986. The calculator datum `d=497870683678639429793424156500617766317/(4·10^40)` is the AV2 gate datum, since the reference is unchanged. With the calculator's primitives, the radius is also at most `R'`. So `C(1)` lies in `[99572606896681488461252714035083774357/(8·10^39), 497878332873871417280584742825816660849/(4·10^40)]`, about `[0.0124465758620851, 0.0124469583218468]`, and `e^{-3}/4` lies inside, so the result is `reference_unresolved`: no shift, sign or coefficient.

**Mirror.** `U_E H_N(tau)U_E^*=H_N(-tau)` (AX1 item 7) and `C` is even. So at `-10^-8` the same `|tau|` formula gives the same radius and datum exactly. This is a replay, not a second confirmation, and `-tau` has no real `g`.

**Scaling.** `E'(tau)/E'(tau/100)` lies in `[100.0015,100.0016]`. The square-root control `2sqrt(17|tau|)` gives about 10.008.

## 3. Crossover
`s*=pi(10^-6-2(D'+D'^2))/(51|tau|)` lies in **[5.982012284161, 5.982012284163]**. At the lower end the full directed radius is at most `10^-6`; at the upper end the lower radius is at least `10^-6`. For comparison, `D'->0` gives `100pi/51`, about 6.15999, and the seven-star slope gives about 6.2262.

This is the crossover of a formula, not a node certificate: only `s=1` is certified, and there is no grid claim. At `s*`, `e^{-3s*}/4<10^-8`.

## 4. Retained Poisson failures at the uniform slope
All are insufficient. **Optimized floor, `D->0`:** at least `(2k's/pi)(1+log(1/(2k's)))>=1.313477283469e-6` for every `L`, since `log(1+L^2/s^2)>=2log(L/s)`. At `L=3921569` it is at most 1.31347728347e-6. **With `D'`:** at least 1.327923202892e-6 for every `L`. **AT4 form at `L=10^4`, with the AX1 square-root control (labelled):** about 8.579e-4.

The Poisson first moment diverges (`P_1(8)>4/pi>P_1(7)`), while the window's stays finite.

## 5. Label and non-claims
**Label:** "uniform Kogut–Susskind SU(2) at fixed spacing and strong bare coupling (`g^4=96/tau=9.6×10^9` at the cap)". The result is `reference_unresolved`. There is no `K_2` rider and no uniform Wilson-mean sign rider (loop-2 veto).

**Flags.** `continuum_claim`, `weak_coupling_claim`, `resolved_interaction_shift`, `scientific_priority_verified` and `grid_claim` are false. `uniform_wilson_claim:true` is the model label only. `euclidean_node_certified:true` means only the `s=1` enclosure within `10^-6`.

The result holds for each AQ1 subsequential state separately. There is no uniqueness, rate or continuum claim.

## 6. Producer-error checklist
Every error below except tier (i) still passes the Boolean, so the formula has to be read.
1. **Seven-star slope** `49|tau|/4` instead of nine groups: 1.8486e-7. With the zero-selected `D` as well, it gives exactly AV2's 1.8320e-7.
2. **Wrong `D'`:** the reverse refinement gives 1.8679e-7; the AX1 target `4/10^7` gives 9.6234e-7, which passes with margin 1.04; tier (i) gives 4.92e-5, which fails.
3. **Zero-selected or mixed tiers:** the zero-selected `D` (1.8956e-7), a dropped `T'^2`, a non-self-consistent `T'`, or tiers mixed across terms or signs (AX1 N5).
4. **Wording:** weak coupling or continuum, a wrong `g^4`, or a missing uniform scope.
5. **Riders:** a uniform sign rider or a `K_2` rider.

Also check: `D'/2` (1.7678e-7); a dropped `m^2`; `pi_hi` in the upper bound; the `theta->-theta` free atom `25e^{-3}/4`; the AV2 calculator run with the zero triple (it refuses the uniform triple); `s*` presented as certified; `-tau` presented as a confirmation.

**Replay.** `python3 -B research/round32/skeptic/ax2_check.py --output <abs fresh dir>`. The normal, `-O` and no-`-B` runs are byte-identical (sha256 `db7e6b56…a5a1`), and no `.pyc` is written.

**Source-edit mutations.** Of nine, eight abort for the intended reason: slope 49, `T'^2` dropped, `pi` direction, `m^2` dropped, the effect half, a zero group norm, the gate hash, and energy 24. The ninth deletes the exp Taylor remainder. That remainder lies below the `10^-60` rounding, so the deletion is undetectable by value; it remains a proof-text item.
