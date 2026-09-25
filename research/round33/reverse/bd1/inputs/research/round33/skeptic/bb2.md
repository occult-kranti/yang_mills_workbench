# BB2 skeptical review (post-comparison, with the BB1 discharge)

**Verdict: `accepted_within_scope`, sub-label `convergence_of_named_constructions`, secondary `common_limit_of_named_constructions`.** There are no blocking issues for the loop.

One piece of producer wording is rejected: the forward report's unqualified item-5 rate paragraph ("The rate in `N` is `O(1/N)` … while the state terms decay geometrically in `N`"). It is false from `N=14419` on and enters no gate text (item 3 below). The item-5 inequality and its constants are correct in both packets.

The contract's own item-5 rate clause can be met only on a certified range. I missed this in my pre-freeze and pre-comparison reviews, and I record it against myself as **D12**.

Human project author: Hruday N M (BUNZEEY). Reviewer: a model-agent skeptic with correlated ancestry. The frozen BB2 targets, brackets and conditional semantics came from my own BB pre-freeze review. This is not external human peer review or formal verification.

## What the packets prove

Both routes prove items 1–5 from the BB1 frozen targets, which serve as explicit hypotheses:
- the R form, `||rho^box1_R - rho^box2_R||_1 <= C_h q^(N-1)`;
- the region form, `||rho^box1_Y - rho^box2_Y||_1 <= c_h |Y| e^{|Y|/10^8} q^{d_Y}`;
- with `q=1/64`, `C_h=1/250000` and `c_h=1/500000`.

The hypotheses are taken for the BB1 comparisons each route uses, both signs, each on-site cutoff space uniformly in `L`, and at fixed `N` for the untruncated ground vectors. The dynamics constants are those admitted by BA2.

The routes:
- **Forward (`nested_telescoping`).** It sums the nested comparisons c1 (F1, `N` versus `N+1`) and c2 (F2) with the full geometric tail, so the constant is `C'=C_h/(1-q)`. It adds c3 for the common limit and c5 (direct, through `Lambda_{N-|v|}`) for coarse translations. It binds a single `C_dyn = 2K_F1 + K_cmp/4` for both families.
- **Reverse (`union_comparison`).** It makes one direct comparison of the nested pair (c4, or c5 for nested one-prescription volumes), so `C'=C_h`. It uses c3 for the common limit, and c5 direct on `(Lambda_N+v, Lambda_N)` for translations. It gives one `C_dyn` per family: `2K_F1` and `2K'_F2`.

**Discharge.** The BB1 gate exists: `research/round33/advisor/bb1-gate.json`, sha256 `18141fea672e5bae09024a5fddc56ea7102aae56ecca16fbb30d67a1354a3827`, commit eef57b4, verdict `accepted_within_scope`. For each of the five comparisons c1–c5, both signs, each on-site cutoff space and the untruncated vectors at fixed `N`, it admits:

| BB1 constant | value | route | hypothesis | margin |
|---|---|---|---|---|
| `C` | ≈ 8.9051e-7 | polymer_kp | `C_h=1/250000` | 4.49 |
| `c_site` | ≈ 8.7681e-7 | polymer_kp | `c_h=1/500000` | 2.28 |
| `C_2` (labelled secondary) | ≈ 9.689e-6 | iterated_split | `C_2h=1/20000` | 5.16 |
| `c_site,2` (labelled secondary) | ≈ 9.674e-6 | iterated_split | `c_2h=1/40000` | 2.58 |

Each admitted bound has the hypothesis shape exactly (the same `q`, exponent and `|Y|` factors), and each constant is below its hypothesis value. So **every item is discharged**, for both producers' hypothesis maps, cell by cell (section "The discharge").

## What is proved, with quantifiers

**Model** (`AQ_patterned_zero_selected`):
- SU(2) in Kogut–Susskind form on Z^3 at fixed spacing, with coarse 24-link factors;
- selected triple exactly (0,0,0), with the Haar product reference;
- 21 omitted faces per anchor, entering as `-(tau/3)W_f` in normalized units `delta=alpha/8`;
- both signs, `|tau|<=10^-8`;
- the AM2 creation expansion in each on-site cutoff space;
- the cover `R={0,e_z}`;
- the coarse l∞ metric with star diameter 1 for states, and l1 on the coarse factor lattice with `F(r)=(1+r)^-4` for dynamics;
- the trace norm on `B(H_Y)`;
- the clock `theta=alpha t/hbar`.

**Families:**
- F1: the AQ1 centered whole-star boxes `Lambda_N=[-N,N]^3`;
- F2: the I1 §6 all-contained-face boxes with padding, on the same `Lambda_N`;
- `N>=2`, with `N>=5` for item 5.

**Statement.** The mandatory template holds verbatim, with the hypotheses now discharged. The items are:
1. **Whole-sequence Cauchy bound, for F1 and F2:**
   - `sup_{M>N} ||rho^{F,M}_R - rho^{F,N}_R||_1 <= C' q^(N-1)`;
   - `sup_{M>N} ||rho^{F,M}_Y - rho^{F,N}_Y||_1 <= c'_site |Y| e^{|Y|/10^8} q^{d_Y}`, for every finite complete-factor region `Y ⊂ Lambda_N`.

   The limit exists on every finite region, by trace-class completeness and without compactness.
2. **Common limit.** The F1 and F2 limits coincide on every finite region. This uses c3, the fixed-`N` comparison of the two prescriptions.
3. **Identification.** The limit equals every AQ1 subsequential limit (F1) and every F2 subsequential limit on every finite region. It inherits exactly:
   - AQ1 stationarity under `T_theta`;
   - strong continuity of the GNS evolution;
   - a nonnegative generator (for F2 limits through BA2's rerun of AQ1 §§4–5);
   - the AQ2 statement for the actual AQ1 centered subsequential state: `H_phys >= (alpha/16)(I-P_Omega)` with a simple vacuum on the invariant-local cyclic completion, and the full-GNS strengthening only as qualified in the AQ2 gate.
4. **Coarse translations.** For every coarse translation `v` (fine translation `(4v_x,2v_y,v_z)`, which preserves residues and face classes) and `N >= |v|_inf+2`:
   - `||rho^{Lambda_N+v}_R - rho^{Lambda_N}_R||_1 <= C_h q^(N-|v|_inf-1)`, from the direct c5 comparison;
   - the limit is invariant on every finite region, from the region form of c5;
   - non-coarse translations are rejected.
5. **Correlation functions.** For `N>=5`, `r_N=floor((N-1)/2)`, `|theta|<=8` and `A` in `B(H_R)`:

   `|c^{F,N}_A(theta) - c^inf_A(theta)| <= ||A||^2 [C_dyn/(r_N-1) + c'_site |Lambda_{r_N}| e^{|Lambda_{r_N}|/10^8} q^(N-r_N) + 2C' q^(N-1)]`.

   The correlations use complex-mean centering.

The item-5 inequality holds for every `N>=5`. It gives an explicit rate only on `5<=N<=14000`, and it is vacuous from `N=14419` (section "Item 5").

**Gate fields.** All 15 contract fields hold as required, produced by the discharge engine. `whole_sequence_claimed`, `common_limit_claimed`, `state_convergence_claimed`, `translation_invariance_claimed` and `rate_in_N_claimed` are true, with the contract scopes, and `dynamics_level` is `correlation_functions_compact_window`. Every exclusion field is false.

`rate_in_N_claimed` refers to the state rate `q^(N-1)` of item 1, which holds for every `N`. The correlation rate is limited to the certified range.

## The discharge

**Admission record.** `bb2-bb1-admission.json` (sha256 `6eb6e3be…946f6`) is my transcription of the gate. The checker pins it, and refuses any entry that is not a verbatim substring of the gate's accepted, decision and limitations text (whitespace-normalized). This covers:
- every constant;
- every bound shape (`differ by at most C q^(N-1) in trace norm`; `<= c_site |Y| e^{|Y|/10^8} q^{d_Y} with d_Y=N-max_{y in Y}|y|_inf`);
- `q=1/64`;
- every comparison label (`c1 F1 on Lambda_N versus Lambda_(N+1)`, …);
- the signs (`both signs`) and the regimes (`in each on-site cutoff space with constants independent of the cutoff, and at fixed N for the untruncated ground vectors`).

Each constant anchor must end with `=<the exact constant>`, and each comparison label must also equal the BB1 contract's list entry. Beyond those anchors:
- **40 cells** (5 comparisons × 2 forms × 2 regimes × 2 signs) equal the BB1 review's `admitted_values` table (`bb1.json`, pinned), including the route, the iterated_split value and the secondary pair;
- the recommended bounds are equal;
- the record has 30 anchored entries: 10 bound values, 10 iterated_split values and 10 secondary cells.

**Protocol** (pre-registered in `bb2_check.py`, committed at 8921539 before either producer or the gate was read). An item is unconditional only when, at both signs, some route proves it from comparisons admitted with a bound dominated pointwise by the hypothesis form and a constant at most the hypothesis value.

| item | what it needs | `+` | `-` | status |
|---|---|---|---|---|
| 1 | c1 and c2 (forward) or c4 (reverse), R and region forms, both families | full | full | **full** |
| 2 | item 1 and c3 | full | full | **full** |
| 3 | item 2 | full | full | **full** |
| 4 | c5 in R and region forms, and item 1 | full | full | **full** |
| 5 | items 1–2 (R form, region form at `Lambda_{r_N}`) and BA2 | full | full | **full** |

Verdict from the discharge: `accepted_within_scope`. Both routes are available at `+` for every family and form.

**The producers' own maps, cell by cell.** Each cell is a (comparison, form, regime, sign) tuple the producer says it uses. The rule is conservative: every listed comparison must be admitted, even where the reverse lists alternatives ("B4 … equivalently B5").

Forward (from `hypotheses_used` H1–H4, each comparison text equal to a BB1 contract entry: H1→c1, H2→c2, H3→c3, H4→c5):

| item | hypotheses | comparisons | cells | discharged |
|---|---|---|---|---|
| 1 | H1, H2 | c1, c2 | 16 | 16 |
| 2 | H1, H2, H3 | c1, c2, c3 | 24 | 24 |
| 3 | H1, H2, H3 | c1, c2, c3 | 24 | 24 |
| 4 | H1, H4 | c1, c5 | 16 | 16 |
| 5 | H1, H2, H3 | c1, c2, c3 | 24 | 24 |
| secondary | H1s–H3s (as H1–H3) | c1, c2, c3 at `q_2` | 24 | 24 |

Reverse (B-labels parsed from each item, with its item references closed: "plus item 1", "through items 1-2", "as items 1-2"):

| item | literal | closure | regimes | cells | discharged |
|---|---|---|---|---|---|
| 1 | c4, c5 | c4, c5 | Q_L, untruncated | 16 | 16 |
| 2 | c3 | c3, c4, c5 | Q_L, untruncated | 24 | 24 |
| 3 | c3, c4, c5 | c3, c4, c5 | untruncated | 12 | 12 |
| 4 | c5 | c5 | Q_L, untruncated | 8 | 8 |
| 5 | c4, c5 | c4, c5 | untruncated | 8 | 8 |
| secondary | — | c3, c4, c5 at `q_2` | none listed; both used | 24 | 24 |

Totals:
- forward: 104 primary cells and 24 secondary;
- reverse: 68 primary cells and 24 secondary.

All are discharged.
- The literal maps equal the Jung assistant-2 table (pinned) item for item.
- The reverse item-5 row lists only item 1. Its F2 part also needs the F2 limit identified with the common limit (item 2, hence c3). I ran that reading as well: 12 cells, all discharged.

**Labelled runs.**
- The secondary pair discharges every item at `q_2=592/390625`.
- The self-contained iterated_split values discharge every item as well. So the discharge does not depend on the post-hoc Kotecký–Preiss repair of the BB1 forward route.

**Discharge controls (18, in memory).** Each is an edit of the gate and/or the admission record, with the hash rebound unless stated. The engine must refuse the record, or return the stated verdict.
- **Downgraded (8):**
  - R constant raised above `C_h`: `insufficient`;
  - `q` retuned to 1/32: `insufficient`;
  - region form dropped: `limited`, with `R_only`/`R_marginals`/`R_translate_covariance`/`dropped`;
  - c5 dropped: `limited`, item 4 dropped;
  - c3 dropped: `limited`, items 3 and 5 `per_family`;
  - c1, c2 and c4 dropped: `insufficient`;
  - the `-` sign not admitted: `limited`, all conditional;
  - gate verdict `insufficient`: `insufficient`.
- **Accepted (1):** c4 alone dropped gives `accepted_within_scope`, because the forward route suffices.
- **Refused (9):**
  - both signs claimed beyond an edited gate;
  - a smaller (iterated_split) constant substituted without its anchor;
  - a region shape claimed without the exponential;
  - an R shape text on a region entry;
  - the gate edited without rebinding the sha;
  - a comparison label swapped;
  - a BB1 contract comparison text changed;
  - the secondary `q` off the cap;
  - a regime claimed beyond the gate.

## Constants: hypothesis values (bound) and admitted values (labelled)

The contract target fixes the BB2 state constants at the hypothesis values. Each is nondecreasing in the BB1 constants, so the hypothesis-value constants remain valid under the discharge.

| quantity | bound (hypothesis values) | re-evaluated at the admitted BB1 values (labelled) | target | margin |
|---|---|---|---|---|
| `C'` forward (nested_telescoping) | `4/984375` ≈ 4.0635e-6 | ≈ 9.0465e-7 | `1/100000` | 315/128 |
| `c'_site` forward | `2/984375` ≈ 2.0317e-6 | ≈ 8.9073e-7 | `1/200000` | 315/128 |
| `C'` reverse (union_comparison), labelled | `1/250000` | ≈ 8.9051e-7 | `1/100000` | 5/2 |
| `c'_site` reverse, labelled | `1/500000` | ≈ 8.7681e-7 | `1/200000` | 5/2 |
| item 4 constant | `C_h=1/250000` in `C_h q^(N-|v|_inf-1)` | ≈ 8.9051e-7 | — | — |
| `C_dyn` forward (duhamel_inner_f1, both families) | `78057/622883200000000` ≈ 1.2532e-10 | unchanged (BA2) | `1/2000000000` | ≈ 3.99 |
| `C_dyn` reverse F1 (duhamel_inner_f1), labelled | `9261/77860400000000` ≈ 1.1894e-10 | unchanged | same | ≈ 4.20 |
| `C_dyn` reverse F2 (duhamel_inner_f2), labelled | `1055961408185869563/15240701171875000000000000000` ≈ 6.9286e-11 | unchanged | same | ≈ 7.22 |
| `C'_2` forward, labelled secondary | `625/12481056` ≈ 5.0076e-5 | ≈ 9.7038e-6 | `1/8000` | 390033/156250 |
| `c'_site,2` forward, labelled secondary | `625/24962112` ≈ 2.5038e-5 | ≈ 9.6891e-6 | none (D5) | — |
| secondary reverse, labelled | `1/20000`, `1/40000` | ≈ 9.6891e-6, 9.6744e-6 | — | — |

The exact re-evaluated rationals are in `bb2-postreview/results.json` → `discharge.constants`.

τ → τ/100 ratios:
- `C'` and `c'_site`: exactly 1 at the hypothesis values, which is non-discriminating (see limitations);
- `C_dyn` forward and reverse F1: `1953058850/194651` ≈ 10033.64;
- reverse F2: ≈ 10019.59;
- `C'_2`: `1085053/1083425` ≈ 1.0015;
- `q_2`: exactly 100.

All are inside their brackets.

## Item 5: range, vacuity and whole-sequence convergence

- **The inequality holds for every `N>=5`**, in both packets, with the three separate constants. I re-derived it, and my pre-comparison package predicted the same form.
- **Certified range `5<=N<=14000`.** The region term is at most `c'_site g(N)` with `g(x) = x^4 e^{x^3/10^8} 8^{-(x+1)}`.
  - `phi = (ln g)' = 4/x + 3x^2/10^8 - ln 8` is convex and `phi(5)<0`. So `g` decreases and then increases on `[5,14000]`, and `g(14000) <= g(5)` exactly.
  - Together with `N <= 10(r_N-1)`, this gives `N·bracket <= K5 = 10 C_dyn + c'_site g(5) + 10 C' q^4`.

  | constant set | `K5` at the hypothesis values | `K5` at the admitted values (labelled) |
  |---|---|---|
  | forward | ≈ 6.0996e-9 | ≈ 3.3774e-9 |
  | reverse F1 | ≈ 5.9602e-9 | ≈ 3.2805e-9 |
  | reverse F2 | ≈ 5.4636e-9 | ≈ 2.7839e-9 |

  The reverse's own block certificate gives ≈ 1.4154e-8 and 1.3657e-8: valid but looser, because it uses `E_UP` where `e^{1.25e-6}` suffices. The historical assistant-2 finds the smallest `K5` ≈ 5.1e-9 to 5.5e-9 at the hypothesis values, consistent with both.
- **Below 2 on `14001<=N<=14418`.** I certified this with fine logarithms: an atanh-series enclosure of `ln` with the geometric remainder, and a 140-term series enclosure of `ln 2`. The dynamics and mean terms together are below `10^-6`.
  - The tightest point is `N=14417`: log margin ≈ 0.741 at the hypothesis values, ≈ 1.566 at the admitted values.
- **At least 2 from `N=14419`.** I certified this at 14419 and 14420 by logarithms, and for every `N>=14421` by the monotone lower envelope `h(x) = c'(x-1)^3 e^{(x-1)^3/10^8} 64^{-(x/2+1)}`, which increases once `(x-1)^2 >= 10^8 ln 2`.
  - This holds for all six constant sets (forward, reverse F1 and reverse F2, at the hypothesis and at the admitted values).
  - The first exceedance is `N=14419` in every case. The historical assistant-2 found the same first exceedance independently at the hypothesis values (scan 14400–14425).
- **Why.** `|Lambda_{r_N}| ≈ N^3` sits inside `e^{|Lambda_{r_N}|/10^8}` and eventually beats `q^(N-r_N)`. At odd `N` the cube grows by a shell of about `6N^2` sites, which adds about 12.5 to the log at `N≈14400`.
- **Whole-sequence convergence without a rate.** The finite-box correlation functions converge to `c^inf_A(theta)` along the whole sequence, for every local `A` and `|theta|<=8`. Two arguments give this:
  - applying the inequality with any fixed `r>=2` in place of `r_N` gives `limsup_N |c^{F,N}_A - c^inf_A| <= C_dyn/(r-1) ||A||^2`, and `r` is arbitrary (reverse Corollary 8.6);
  - equivalently, norm convergence of the evolutions (BA2), trace-norm convergence of the local densities (item 1), and norm approximation of `T_theta(A)` by local observables.

  Neither argument re-chooses `r_N` for a quantitative statement.

The supported statement therefore says:
- the inequality holds for every `N>=5`;
- the explicit rate holds only on `5<=N<=14000`;
- the bound is vacuous from `N=14419`;
- the correlation functions converge along the whole sequence without a rate.

The template claims no correlation rate. Its "at a rate in N" belongs to the reduced densities (item 1).

## Items adjudicated

1. **`C'`: forward `(64/63)C_h` versus reverse `C_h`.** Both are valid implications of the hypotheses, and both equal my pre-comparison predictions exactly. The forward values `4/984375` and `2/984375` are bound. They are valid whichever route's hypotheses are discharged, since `(64/63)C_h >= C_h`. The reverse values are labelled.
2. **`C_dyn`.**
   - The forward composite `2K_F1+K_cmp/4` uses one route (duhamel_inner_f1) for both families. Its lemma `(5N+1)(r_N-1) <= N^3/4` is correct: I re-proved it by the identity `N^3-10N^2+28N+6 = N(N-5)^2+3N+6` with `2(r_N-1) <= N-3`, and checked it exactly for `N<4000`.
   - The reverse gives single-route per-family constants: `2K_F1` and `2K'_F2`, the latter through BA2 gate item (4).
   - Neither producer mixes routes, so D3 and D10 are resolved. The forward single constant is bound, and the reverse per-family values are labelled.
3. **The item-5 rate (reverse W1; forward overclaim; D12).** See the previous section.
   - The forward report's §6 rate paragraph ("The rate in `N` is `O(1/N)`: … while the state terms decay geometrically in `N` (the cube volume grows only like `N^3`)") is **rejected**.
     - Its checker evaluates item 5 only for `N<=59`.
     - Its enclosure `e^x<=1/(1-x)` cannot be applied from `N=465`.
     - The inequality F07 itself is correct.
   - This is blocking for that wording only. It is not blocking for the loop: acceptance concerns the proved constants, and the reverse's certified-range statement (re-certified here independently) is what the gate should carry.
   - My own pre-comparison derivation (§8) made the same unqualified statement. My reviews missed that contract required item 5 ("the rate in N is O(1/N)") is attainable only on a certified range. This is **D12**, recorded against the skeptic.
4. **Item 4.**
   - Both producers use the direct c5 comparison, the reverse on `(Lambda_N+v, Lambda_N)` and the forward through `Lambda_{N-|v|}`, and both get the contract constant `C_h q^(N-|v|-1)`.
   - The reverse's labelled union fallback `2C_h q^(N-|v|-1)` is valid but looser than the available `C_h q^(N-|v|-1)(1+q^{|v|})`.
   - Both check residues face by face:
     - forward: per-face role and class plus a constant owner shift on a 16×8×3 window;
     - reverse: all 64 translations of the period window, exactly 8 coarse.

     Neither uses the per-anchor histogram, which is blind to fine shifts; my pitfall fixture and the historical assistant-2 both show this.
   - Invariance on every finite region comes from the region form of c5. The F2 volumes other than centred cubes rest on the AY1 local reading, a BB1 limitation carried along.
5. **Gate-field blocks.**
   - The reverse exports the dependent fields false before the discharge (`dynamics_level` `algebraic_heisenberg_compact_window`) and the contract values after it, which is correct under `gate_fields_rule`.
   - The forward exports the contract values labelled "proposed", with an if-undischarged block. This is a presentation difference.
   - Both after-discharge blocks equal `gate_fields_required`, and so do the fields produced by my discharge engine.
6. **Producer wording findings against my record.**

   | producer finding | my record |
   |---|---|
   | forward W1 / reverse W4 (`C_dyn` assembly, per family) | D3, D10 |
   | forward W2 (BA2 minimum mixing routes) | R9 |
   | forward W3 (item 4 needs the region form) | D1 / R4 |
   | forward W4 (BA1 accepted versus decision text) | my BB review, non-blocking |
   | forward W5 / reverse W2 (gate fields at producer time) | the `gate_fields_rule` reading |
   | forward W6 / reverse W5 ("exactly 1" brackets non-discriminating) | agree; limitation |
   | forward W7 (naive placeholder regex) | minor |
   | reverse W1 (item-5 rate) | **new; D12** |
   | reverse W3 (union versus direct) | D2 / R1 |
   | reverse W6 (two exclusion lists), W10 (observable id) | minor |
   | reverse W7 (inherited semantics) | D6 / R7 |
   | reverse W8 (region form at R) | my check `region_form_at_R_is_weaker` |
   | reverse W9 (BA2 rerun consistent) | agree |

## Review against the contract items (both producers)

- **Item 1.**
  - Forward: nested telescoping with the full tail, exact, sup over all `M>N`.
  - Reverse: one direct nested comparison.
  - Both work in each `Q_L`, with the untruncated vectors at fixed `N` via AV1 F20–F23 (AY1 for F2). The `L` and `N` limits are never exchanged.
  - Existence comes from the Cauchy bound, not compactness. The region form carries `|Y|` and `d_Y`.
- **Item 2.** Both use c3.
- **Item 3.** Both identify the limit with AQ1 and F2 subsequential limits and inherit within the admitted scope (D4, D11).
  - The reverse lists the AQ2 Wilson variance; the forward omits it.
  - The AQ2 full-GNS strengthening is carried only as qualified.
- **Item 4.** Direct c5 in both (above). Both reject non-coarse translations face by face.
- **Item 5.**
  - Three separate constants, `r_N` as frozen, complex-mean centering.
  - The rate clause is met only on the certified range (D12).
  - Neither packet claims anything uniform in time, and neither claims equality of GNS dynamics of different states.
- **Item 6.**
  - The template appears once, as one unbroken line, in each report.
  - `tools/phrase_scan.py` exits 0 on both reports, and my mirror agrees.
  - Every quoted Nachtergaele–Sims block line is a verbatim substring of the committed excerpt.
  - The τ ratios are inside their brackets.
  - All 34 controls are damaging mutations in each checker:
    - forward: 52 checks, 122 rejected mutations;
    - reverse: 59 checks, 162 rejected mutations.

## Replays, closures and isolation (`bb2-replays.json`)

- **Producer replays.** All four (forward/reverse × normal/`-O`, fresh external directories) reproduce `output/` byte for byte:
  - forward: `results.json` `b87fea90…3753a`, manifest `b7aedea8…36b1`;
  - reverse: `results.json` `51613bda…0d0bbe`, manifest `dc4da2b7…8eb02`.

  `tools/freeze.py verify` reports verified for both.
- **Closures.** Each has 42 files and verifies file by file. Each producer holds exactly the 38 declared inputs (`AGENTS.md`, the contract and 36 shared premises), equal to the inventory I recorded before production and byte-identical to the repository. Both carry the frozen BB1 contract bytes.
- **Reverse isolation.** The inventory holds no forbidden file: no BB1 producer or gate file, forward file, triage, plan, lens file or BB contract review. Both producers disclosed name-only exposures to untracked file names after their first freeze and opened none of them. The BB2 state constants are fixed by the contract, so a file name carries no numeric channel. Accepted as disclosed.
- **Commit order:**
  - contracts frozen 45a87be (09-24 23:38:22);
  - forward d05efda (00:10:26);
  - my pre-comparison package 8921539 (00:14:56);
  - reverse 17c0ecf (00:18:36);
  - my stage 1 e2a9ed2 (00:44:31);
  - BB1 gate eef57b4 (03:02:27).

  The forward could not have read my package. I read no producer before my commit, and no BB1 gate, BB1 review or lens table before eef57b4.
- **My packages.**
  - The pre-comparison package is unchanged and replays byte for byte (81 checks, 38 controls, 142 rejected mutations).
  - This review's checker, `bb2_postreview_check.py` (sha256 `f2949f2a…4475`), writes `bb2-postreview/results.json` (sha256 `be5de151…9b11`, 11 checks). It is byte-identical under `-B` and `-B -O` in fresh external directories.
  - My first `-O` run was misdirected by a shell-variable error to `/outO` at the filesystem root. Its output is identical, and it is disclosed in `bb2-replays.json`. Removing it is left to the operator.

## Mutation harness

- **Validator weakenings (68).** One per contract control per producer, on temporary copies outside the checkout. Each run must abort with `damaging mutation accepted: <label>`, a recorded mutation of the same control.
- **Must-abort edits (13), all caught:**
  - forward (7): the `C'` function coefficient changed, lemma F08's `1/4` replaced by `1/8`, `K_cmp/8` in `C_dyn`, contract bytes edited without rehash, the BB1 forward report added as an undeclared input, an affirmative forbidden phrase appended to the report, the template removed;
  - reverse (6): the dynamics ratio `10` replaced by `2`, a vacuity witness moved to `N=14415`, contract bytes edited, a skeptic triage added to the inputs, an affirmative forbidden phrase appended, the template removed.
- **Unmutated copies (2)** reproduce the frozen results byte for byte.
- **Silent edits (6)**, which the producer checkers do not pin:
  - 3 are caught only by my value validator: the forward item-5 F1 sums computed with the F2 constant, the forward secondary `c'_2` factor doubled, and the reverse union fallback factor 3;
  - 3 are caught by the reverse checker itself: `K_R` coefficient 5, `K_reg` without the `e` factor, and `C'` doubled.
- **Discharge controls (18).** In memory (above).

## Blocking issues

None for the loop. The forward's unqualified item-5 rate wording is rejected: it must not enter the gate text, and it is recorded as a limitation.

## Non-blocking findings

- **N1. Forward rate overclaim** (above). The frozen forward files stay as retained evidence.
- **N2. Jung assistant-2 vocabulary finding.** The forward's `gate_fields_if_undischarged.dynamics_level` value `not_set (conditional_on_bb1_targets)` is outside `plan.json`'s closed vocabulary. It sits in the conditional block, which the discharge supersedes, and it is not exported to the gate.
- **N3. Forward gate-field presentation** differs from `gate_fields_rule` (proposed values plus an if-undischarged block). Presentation only.
- **N4. The reverse item-5 map lists "through item 1" only.** Its F2 part also needs item 2 (c3), which is admitted. The reading was discharged in 12 cells.
- **N5. The reverse's labelled item-4 union fallback `2C_h`** is looser than `C_h(1+q^{|v|})`.
- **N6. The reverse secondary row lists no signs or regimes** (Jung assistant-2). I read it as "as items 1–2", with both signs and both regimes, and it is discharged.
- **N7. The reverse item-1 row lists alternatives** ("B4 … equivalently B5"). The map-level discharge required both, and both are admitted.
- **N8. The forward's `e^x<=1/(1-x)` enclosure** is unusable from `N=465`. Its checker uses it only for `N<=59`.
- **N9. The reverse `K5` certificate** (≈ 1.415e-8 for F1, ≈ 1.366e-8 for F2) is valid but about 2.3 to 2.7 times looser than my envelope values and the historical assistant-2's scan values.
- **N10. Name-only exposures** of both producers were accepted as disclosed.
- **N11. The "exactly 1" τ brackets** for `C'` and `c'_site` cannot discriminate at the hypothesis values. This is a contract design choice. The BB1 constants' linear τ-scaling (≈ 100.648) is recorded by BB1.

## Contract defects

- **D1.** `acceptance.limited` did not say what happens to item 4 without the region form. Moot: the region form is admitted.
- **D2.** A literal union route cannot meet `C_h q^(N-|v|-1)`. Both producers use c5 directly.
- **D3, D10.** Composite `C_dyn` and the unspecified assembly. Resolved: each producer states a single-route assembly.
- **D4, D11.** The scope of the item-3 inheritance. Both producers stay within the admitted scope.
- **D5.** `c'_site,2` has no target. Labelled.
- **D6.** Inherited control texts written for BA2/BB1. Read as in my contract review.
- **D7.** `d_Y` is defined only in BB1. Both producers define it.
- **D8.** Plan history freeze record. Repaired in 43eb922.
- **D9.** No frame for limited outcomes. Moot at this verdict.
- **D12 (new, against the skeptic).** Contract required item 5's "the rate in N is O(1/N)" is attainable only on a certified range with the frozen `r_N` and region form. My BB pre-freeze and pre-comparison reviews missed it, and my derivation §8 repeated it. The reverse producer found it (W1).

## Which constants the gate binds

The rule: bind the larger valid constant per quantity, which is valid under either discharge route; label the other route's value. Constants are evaluated at the hypothesis values, as the contract target specifies. The values at the admitted constants are labelled only.
- **Item 1:** `C'=4/984375` and `c'_site=2/984375` (forward, nested_telescoping, exact_first_order, hypothesis source `bb1_frozen_targets`, BB1 route `polymer_kp`). The reverse's `1/250000` and `1/500000` are labelled.
- **Item 4:** `C_h q^(N-|v|_inf-1)` with `C_h=1/250000` (direct c5, both routes). The union two-step is labelled.
- **Item 5:** `C_dyn=78057/622883200000000` (forward, polynomial_lieb_robinson, duhamel_inner_f1, both families). The reverse per-family values are labelled.
  - `K5` ≈ 6.0996e-9 on `5<=N<=14000` only.
  - The bound is vacuous from `N=14419`.
- **Labelled secondary:** `C'_2=625/12481056` and `c'_site,2=625/24962112` at `q_2=151552|tau|`.
- **BB1 route of the discharging constant:** polymer_kp for `C` and `c_site`; iterated_split for the secondary pair.

## Limitations

1. **Scope.** Only the zero-selected patterned family, with fixed spacing and `|tau|<=10^-8`. F1 and F2 on centered cubes (`N>=2`) and the limit of the named constructions; the cover `R` and finite complete-factor regions; coarse translations; `|theta|<=8`. Nothing transfers to other boundary conditions, states outside the named constructions, nonzero selected triples, literal vertex boxes, weak coupling or the continuum. The constants are uniform in N and in the cutoff, never in the lattice spacing.
2. **Convergence of the named constructions only.** This is no uniqueness of any ground state, and no statement about any other infinite-volume state. The limit inherits only the listed admitted properties. There is no equality of GNS dynamics of different states and no uniform-in-time statement.
3. **Discharge as recorded above.** The bound constants are evaluated at the hypothesis values. The values re-evaluated at the admitted constants are labelled.
4. **The BB1 limitations are carried along.** The polymer_kp bound values rest on the Kotecký–Preiss citation, checked post hoc and covered; the iterated_split values discharge as well. Non-centred F2 volumes in c5 rest on the AY1 local reading.
5. **Item-5 rate** (D12, reverse W1). The explicit rate holds only on `5<=N<=14000`, and the bound is vacuous from `N=14419`.
6. **The rejected forward overclaim.** Recorded and excluded from the gate text.
7. **Upper bounds only.** The minus-sign values replay `|tau|`. The "exactly 1" brackets are non-discriminating. The correlation bound holds per fixed local `A` on `|theta|<=8`.
8. **Contract readings:** D2/R1, D3/D10, D5, D7, D9, D6, D4/D11.
9. **Independence** is limited to derivations, constants and code. All agents are correlated model agents. The targets and semantics came from my BB pre-freeze review. My package was committed between the two producer commits. Isolation is verified for repository inputs only.
10. **Scientific priority is unverified.**

## Advice (planning only)

- **Carry the certified-range rule into later contracts.** A contract that asks for a rate from a frozen bracket should require the producer to certify the range on which the bracket stays below its trivial bound, and should state the rate only there. Here the obstruction is `e^{|Lambda_{r_N}|/10^8}` in the frozen region form. A region form without the exponential (the BB1 iterated_split route proves `c_site sum_{y in Y} q^(N-|y|_inf)`) would give a rate for every `N`. That is a candidate goal, not a result.
- **Boundary independence of the dynamics** and **uniqueness** remain open. The limit here is the limit of the named constructions only.
