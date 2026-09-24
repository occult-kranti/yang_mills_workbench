# AW2 independent replay before producer comparison

**Timing.** I wrote this after the AW2 contract froze (`frozen_at` 2026-09-24T00:01:24Z, sha256 `aa559b18…68f9`). I have not opened, listed or read `research/round32/forward/aw2/`. AW2 is a single-direction certificate, and the contract (item 6) makes this package a required admission input.

**Inputs:** the contract, `selection-aw2.md`, the AW1 gate (sha256 `647dc337…41ae`), the AW1 contract (rule text), the AV1 gate (`D_ii`), I1.5 in `round21/forward/i1/report.md`, the admitted AW1 forward and reverse reports, and my own `aw1.md`, `aw1.json`, `aw1-independent-derivation.md`, `aw1-postreview/results.json` and `loop2-response.md`. Scratch work stayed in a private subfolder; I read nothing else in the shared scratchpad.

**Standing:** I am a model-agent skeptic with correlated ancestry (the same model family as the advisor and the producer), and the bound `K_2^+` is my own AW1 itemization. This replays an admitted formula; it is not human review and not an independent discovery.

Human project author: Hruday N M (BUNZEEY).

Exact values come from `aw2_check.py` (75 checks, all 23 controls). Normal and `-O` runs are byte-identical, `results.json` sha256 `ecff2cfc…4e6f`. Decimals are widened outward unless marked as a preview.

## 1. Bound inputs
- **`K_2^+`** `= 81108864767825329926713064490531229475390625/24176936535511801466930759024724079017984` (≈3354.80322946).
  - It is parsed from both the decision text and the accepted text of the AW1 gate, and it equals the contract's `K_2_plus` string.
  - The ceiling `3354803229461691/10^12` is the exact `10^-12` ceiling of that value.
  - Cross-check only: `[rho+T·T+T^2+eps^2+(|tau|/144)eps^2]/tau^2` reproduces it exactly, with `T=(49|tau|/144)/(1-352J)`, `rho=352JT`, `J=28|tau|`, `eps=2T+T^2`.
  - It dominates the forward (3354.63832966) and reverse (3354.49942587) AW1 values. Both are valid bounds, but AW2 must use the gate binding.
- **From the contract and I1:** target `exclusion_margin >= 2` (`preregistration.target`); reference `0` (centering `none`, Haar route); I1.5 parsed from the snapshot as `phi_b=-(tau/3) sum_{f in O_b} W_f`.

## 2. The frozen rule
The rule text is in `contracts/aw1.json`: the largest element of `{10^-8,10^-9,...}` with `K_2^+ tau <= 1/288`, where `1/288` is half the derived `1/144`.
- **At `k=8`:** `K_2^+·10^-8 = 207638693805632844612385445095759947457/6189295753091021175534274310329364228603904` (≈3.354803e-5), at most `1/288` (≈3.472222e-3). The slack is `21282971559982635125992733687992310290751/6189295753091021175534274310329364228603904`; the ratio of threshold to `K_2^+ tau` is ≈103.50003.
- **Result:** the first grid element passes, so **`tau_AW2=10^-8`**, the cap (the grid has no larger element). The contract's literal `1/100000000` was compared only afterwards; it is never an input.

## 3. First-order coefficient (re-derived)
The sign chain:
1. `V_b=phi_b/8=-(tau/24) sum W_f` in alpha units.
2. `W_f Omega_0` has energy 3 in alpha units (four spin-1/2 links), or 24 in normalized units.
3. So `c^(1)=-(tau/72) sum W_f Omega_0` in both unit systems.
4. `psi=Omega_0-c^(1)+O(tau^2)`.
5. `omega=-2Re<W Omega_0,c^(1)>=(tau/36)E[W^2]=+tau/144`.

**Only `f=W` pairs with `W`.** The other 81 faces meeting `R` give zero by the per-link `Z_2` centre grading. My I1.4 enumeration gives 49 faces per site, 82 meeting `R`, 10 with owner set `R`, 16 touching both sites and 21 anchored, and the star has 4 sites.

**Haar moments.** `E[W^2]=1/4` from the `chi` recursion.

**The AW1 literal display** `2<W Omega_0,c^(1)>` gives `-1/144` and is rejected.

**One-plaquette fixture** (finite graph, `transfers_to_aq:false`):
- `<W>=tau/144-5tau^3/11943936+289tau^5/6604518850560+…`, identical at the truncations `j<=3` and `j<=5/2`.
- The exact two-level ground state gives `<W>` in `[6.944444444444444e-11, 6.944444444444445e-11]` at `+10^-8`, and exactly the negated interval at `-10^-8`. So `sign(<W>)=sign(tau)`.
- Flipping `phi_b` gives `-1/144` and is rejected.

## 4. Enclosures (exact endpoints; decimals widened outward)
Denominator `Q=618929575309102117553427431032936422860390400000000`.
- **`tau=+10^-8`:** first-order value `1/14400000000`, radius `K_2^+/10^16` (≈3.354803e-13).
  - `lo=42773581813770903096597852821080380528959/Q >= 6.910896412149827e-11`.
  - `hi=43188859201382168785822623711271900423873/Q <= 6.977992476739062e-11`.
- **`tau=-10^-8`:** `[-hi,-lo]`, within `[-6.977992476739062e-11, -6.910896412149827e-11]`. It is the flip image and the same `|tau|` formula: **a replay, not a second confirmation.**
- **Checks:** the outward-ceiling variant gives the same 16-digit decimals and margin floors; the AV1 bound `D_ii` (≈1.3612e-8) contains both enclosures (`hi/D_ii` ≈5.13e-3).

## 5. Strict exclusion and margins
- **Strict exclusion:** `lo(+tau)>0` and `hi(-tau)<0`, so the free reference 0 is strictly excluded at both signs.
- **Exclusion margin** `m=(|tau|/144-K_2^+tau^2)/(K_2^+tau^2)=42773581813770903096597852821080380528959/207638693805632844612385445095759947457`, about **206.0000524**. Its floor on the `10^-9` grid is `41200010489/200000000`. Target `>=2`: **met**.
- **Sign margin** `s=1/(144K_2^+|tau|)=42981220507576535941210238266176140476416/207638693805632844612385445095759947457`, about **207.0000524**. Its floor on the `10^-9` grid is `41400010489/200000000`.
- **Relations:** `m=s-1` exactly. `m>=2` ⇔ `s>=3` ⇔ `K|tau|<=1/432`, whereas the AW1 rule `K|tau|<=1/288` ⇔ `s>=2` ⇔ `m>=1`; so the rule guarantees only `m>=1`, and the target is tested separately.
- **Scaling** (`tau -> tau/10`): the first-order term changes by exactly 10 (exponent 1) and the remainder by exactly 100 (exponent 2).
- **Corollary** (labelled, not the headline): `K_2^+` bounds every `|tau|<=10^-8`. The sampled itemized coefficients (3354.5056, 3354.4758 and 3354.4728 at `10^-9`, `10^-10` and `10^-11`) lie below it and decrease with `|tau|`. Therefore `s(|tau|)>=207` and `sign(omega_tau(W))=sign(tau)` for every `0<|tau|<=10^-8`.

## 6. Scope (exact statement)
**Model.** The AM2/AQ1 zero-selected patterned family: selected triple exactly `(0,0,0)` with the Haar reference, whole stars under I1.5, the original xz loop `W` with cover `R={0,e_z}`, fixed spacing and fixed positive physical scales.

**Statement.** At `tau=+-10^-8`, every state in the **whole set of AQ1 subsequential limits** `S(tau)` satisfies `omega_tau(W) in [tau/144-K_2^+tau^2, tau/144+K_2^+tau^2]`, and so does every centered whole-star box `N>=2` at every cutoff. The bound is uniform in the box and passes to the limits by local trace-norm convergence, because `W` is local on `R`. Hence `sign(omega_tau(W))=sign(tau)`, and 0 is strictly excluded.

**Sub-label** `static_not_dynamic`. This is a **static equal-time mean**. It is not a dynamical correction, mass shift, susceptibility or mass-gap statement.

**What remains unresolved.** The shift of the centered correlation (`C(s)`, `c(theta)`) is still unresolved: AV2 carries `reference_unresolved`, and AW1 made it second order.

**Not claimed:** AQ uniqueness (`S(tau)` may have many states; `S(-tau)=S(tau)∘alpha_E` holds as sets), a rate in `N` or whole-sequence convergence, uniform Wilson, weak coupling, continuum or scientific priority. `sign_certified_below_cap` does not apply at the cap.

## 7. Retained crude-tier failure
With `t_c=592|tau|`, `K_2=1937877026146766159414097129/244140625000000000000` (≈7937544.299, equal to the AW1 crude value). At the cap its enclosure `[-7.243099854652710e-10, 8.631988743541599e-10]` **contains 0**: sign margin ≈0.0874886 (<1), exclusion margin ≈-0.91251. It is retained as a limited-tier control. The rule would give it `10^-10`; that is a comparison only, and using it would be tier mixing.

## 8. Controls and receipts
All 23 contract ids are executed, in contract order, as damaging mutations. Each raises an explicit `Rejected` with the expected reason. Item 4's controls without their own ids are mapped as follows:
- **sign convention:** a flipped `phi_b` string and a flipped fixture series, both under `wilson_mean_first_order_coefficient`;
- **boundary/state:** `N=2` and `N=7` give the same enclosure, and `N=1` is rejected;
- **centring artifact:** the vector and scalar identities as a synthetic fixture, plus rejection of any `m_hat` in the `omega(W)` path;
- **coherent tampering:** the gate snapshot removed with the manifest rebound, and the gate's `K` edited with its hash rebound. Both are rejected.

**Source-edit receipts.** Ten edits to a scratch copy of the checker all abort: sign flip, rule start shifted, `K` scaled, contract pin, static flag, margin denominator, reference `1/4`, crude `K` as headline, sign-blind `-tau`, and inward decimals.

## 9. Producer-error checklist (to hold the forward to)
1. **Literal coupling.** `tau_AW2` is parsed from the contract's `1/100000000`, or typed in. It must come from the rule applied to the gate's `K_2^+` inside `check.py`. The coupling must not be `10^-9`, off-grid or above the cap.
2. **Wrong `K_2` value.** Any of these is wrong:
   - the forward's 3354.638 or the reverse's 3354.499 (valid, but not the binding);
   - a recomputed or reduced `K`;
   - the crude `7.94e6`;
   - `K` unverified against the gate's hash;
   - the ceiling used without its label.
3. **Using the `-tau` replay as confirmation**, or counting it as a second certificate. Also wrong: a sign-blind `-tau` interval, or pointwise `-tau` states taken along independent subsequences.
4. **Claiming a dynamical effect.** This includes a mass shift, a susceptibility, a correlation or `C(s)` shift, a spectral statement, or omitting `static_not_dynamic`.
5. **Sign convention.** The literal `2<W Omega_0,c^(1)>` gives `-tau/144`; a flipped `phi_b` does the same; mixed units give `tau/18` or `tau/1152`. A `+1/144` reached through two compensating sign errors must be caught by the fixture.
6. **A margin defined against the wrong denominator:**
   - `(|tau|/144-Ktau^2)/(|tau|/144)≈0.99517`, which would wrongly *fail* the target;
   - the ratio to `1/288` (≈103.5);
   - the sign margin 207 reported as the exclusion margin (it is 206.00005);
   - the rule threshold `1/288` used as the AW2 target, when the target is `m>=2`.
7. **Arithmetic slips.** Decimals rounded inward, floats in admission Booleans, or an endpoint that is not an exact rational.
8. **Labels.** `sign_certified_below_cap:true` at the cap, a missing `producers=[forward]` statement, a fabricated reverse package, reverse isolation claimed, or the crude tier dropped instead of retained.
