# AZ1 independent derivation (skeptic, before comparison)

**Standing.** I wrote this after the AZ1 contract froze (`frozen_at` 2026-09-24T04:29:40Z, sha256 `91c828a7…7078`). AZ1 has a single forward producer, so this package is a required admission input (`single_direction_independent_replay`).

**Sources.** I worked from:
- the frozen contract, `selection-az1.md`, `panel-update-4.md` and `plan.json`;
- the AX1 gate (sha256 `1b8fb152…d177`, pinned), the AX1 forward and reverse reports and my `ax1.md`;
- the AL1 forward report and gate, and the AM2 gate and forward report (the cap sentence);
- the AQ2 forward report (the gap passage) and `skeptic/am2.md`;
- the modern lens's `memo.md`, `sota-table.md` and `update-4.md`, and the historical lens's `update-4.md`;
- my `triage.md`, `prospective-controls.json`, `loop2-response.md`, `ay2.md` and AY2 package (format);
- AGENTS.md.

Background only, not premises: the AL2 gate (common rescaling), the modern `sources.json` record for Faizal–Shabir, and the Round31 roadmap goal 5.

**Isolation.**
- I did not open, list or read anything under `research/round32/forward/az1/` except `inputs/`. There I listed the file names with `find`: 29 files, equal to AGENTS.md, the contract and the 27 shared premises. I hashed them against their repository sources, and all are byte-identical. I opened none of them. I read the same premises at their repository paths.
- I did not open `research/round32/forward/az2/`.
- One whole-tree `git status` at the start of this package showed no untracked or modified path. Every later `git status` was restricted to `research/round32/skeptic`.
- No producer file name has come into view.

**Scratch.** All scratch work (the arithmetic previews, the source-edit harness and the replays) stayed in `/tmp/claude-0/skeptic-az1-private/`. I read nothing in other agents' scratch folders or in the shared scratchpad root.

**Correlated ancestry.** I am a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and the producer.
- My triage goal-5 note and my prospective `continuum` controls are the origin of five AZ1 control ids.
- My `ax1.md` is a shared premise.
- The selection note and the modern lens's `update-4.md`, both premises, already print the statement, the three identities and the rehearsal indices 4 and 421.

The producer can therefore copy the headline. My replay is independent in code and route only: rational-function identities by polynomial cross-multiplication, crossovers by exact integer roots with a brute-force cross-check, and a negation-aware phrase validator. This is re-derivation, not independent discovery or human review.

**Exactness.** Exact values come from `az1_check.py`: 82 checks and 28 controls (the 21 contract ids plus 7 extra), with 122 rejected mutations, 101 of them inside the contract controls. Every decimal below is a preview. Human project author: Hruday N M (BUNZEEY).

## 1. What AZ1 must state

**Model.** The uniform Kogut–Susskind SU(2) Hamiltonian at fixed spacing and strong bare coupling (AX1):
- every elementary face has coefficient `nu=alpha*tau/24`;
- route B, with the Haar reference;
- whole stars plus single-factor groups;
- both signs of `|tau|<=10^-8`, where `-tau` is the `U_E` mirror.

The contract names a trajectory `(a_n,g_n)` with `g_n->0` as `a_n->0`, stated as a hypothesis of asymptotic-freedom form. `E_star` and `hbar` are fixed, and there is no plateau fit.

**Template (contract `mandatory_sentence_template`, verbatim):**

> Along the named trajectory (a_n,g_n), the fixed-spacing family supplies exactly one uniform estimate, the volume-uniform gap alpha/16=g^2/(32a) for g^4>=9.6x10^9, and fails to supply any estimate uniform along a_n->0; this is not a statement that the continuum limit exists, that any estimate is uniform in a, that the coupling is weak, or that any fraction of the continuum problem is thereby resolved.

**Readings** (contract review items 5, 6 and 9):
- "exactly one" means the one necessary gap estimate identified, not the only volume-uniform bound AX1 admits;
- the estimate holds "at fixed a";
- the failure concerns the named trajectory, on which `g_n->0`.

## 2. The dictionary as rational-function identities

AL1 (HNM-AL1.1–2, Bauer et al. convention, `W_p=Tr U_p/2`, raw magnetic term `lambda sum_p(1-W_p)`) gives:

`alpha = g^2/(2a)`, `lambda = 2/(g^2 a)`, `tau = 24 lambda/alpha`, `delta = alpha/8`, normalized gap `1/2`.

Take `G=g^2>0` and `a>0` as independent indeterminates. Represent each quantity as a quotient of polynomials in `(G,a)` with rational coefficients, and prove each identity by showing that `num1*den2-num2*den1` is the **zero polynomial**. This is a literal identity, not a sampled check.

| # | Identity | One-line reason |
|---|---|---|
| 1 | `alpha/16 = G/(32a)` | `(G/(2a))/16` |
| 2 | `delta*(1/2) = alpha/16` | the physical gap is the normalized gap `1/2` in units `delta=alpha/8` (AX1 F09, AL1 `H_KS=(alpha/8)H_tilde+...`) |
| 3 | `tau = 96/G^2` | `24*(2/(Ga))*(2a/G)` |
| 4 | **`alpha*lambda*a^2 = 1`** | `(G/(2a))*(2/(Ga))*a^2`; the product of the electric and magnetic scales is `1/a^2` whatever the coupling |
| 5 | `r = lambda/alpha = 4/G^2` | |
| 6 | `nu = alpha*tau/24 = lambda` | the uniform face coefficient equals the magnetic coupling |
| 7 | `nu/delta = tau/3` | route-B normalized face coefficient `-(tau/3)W_f` |
| 8 | `7|tau| = 672/G^2` | AL1 local norm |
| 9 | `lambda*G^2 = 4 alpha` | inverse map, with (4): `a^2=1/(alpha lambda)`, `g^4=4 alpha/lambda` |

So `(a,g^2) -> (alpha,lambda)` is a bijection of the open positive quadrant, and `tau` depends on the ratio `lambda/alpha` alone. The same identities are rechecked at six exact sample points.

**Discrimination.** The cross-identity (4) catches the commonest slip: `alpha=g^2/a` makes `alpha*lambda*a^2=2` identically.

**At the cap.**
- `tau*g^4=96`, so `0<tau<=10^-8` iff `g^4>=96*10^8=9600000000`.
- `g^2=40000 sqrt 6` ≈ 97979.59 is irrational, so every numeric value at the cap below uses a directed `sqrt 6` bracket (`10^-40`).

**The AL1 conditions:**
- bridge `r<=1/8` iff `tau<=3` iff `g^4>=32`;
- ends `r<=1/2` iff `g^4>=8`.

## 3. The admitted regime and why it is bounded below in g

**Route-B contraction** (AX1 gate (1)–(2)), recomputed:
- `J'=4*7|tau|+|tau|=29|tau|`, which is `2784/g^4` in the dictionary;
- `exp(1/8)<8/7`, by a Taylor sum plus a geometric tail;
- `G(1/64)=16e^{1/8}(1+10/64)<148/7` and `G'(1/64)=16e^{1/8}(18+80/64)<352`;
- with the frozen `J_0'=29/10^8`: `J_0'G(R)<1073/175000000<1/64` and `2J_0'G'(R)<319/1562500<1`;
- `J_0'/29=10^-8`, which is the cap.

**Route radii, labelled and not admitted.** The same inequalities would allow:
- `29|tau|*148/7<=1/64`, i.e. `|tau|<=7/274688` (≈ 2548.3 times the cap), `g^4>=26370048/7` ≈ 3.767e6;
- the exclusion `58*352|tau|<1`, i.e. `|tau|<1/20416`.

The AX1 forward report prints these radii, but no gate froze or reviewed them.

**The structural point.** The contraction's smallness parameter is `J'` ∝ `|tau|` ∝ `1/g^4`. Any finite radius R therefore bounds `g^4` from below, and every sequence `g_n->0` eventually leaves the region: there is some `n_0` beyond which every `n` is outside it. This holds for the admitted cap, for the route radius, and for any other finite radius.

**Sufficient, not necessary.** The AM2 report says "It does not interpret rejection beyond the chosen cap as actual gap failure". The AL1 gate says the obstruction is "failure of a specified sufficient certificate, not a no-gap or continuum-impossibility theorem". The failure is the certificate's, not the gap's.

## 4. The one uniform estimate supplied (cited, not re-derived)

**The estimate.** AX1 gate (2): every finite complete-factor route-B volume at `|tau|<=10^-8` has a unique gauge-invariant ground and a full-space gap `>=1/2` normalized, that is **`alpha/16=g^2/(32a)` physical**. AX1 gate (3) and AQ2: the gap `alpha/16` re-applies to the GNS representation of every AQ1 subsequential limit. The estimate is therefore **uniform in N (volume-uniform) at fixed a**, for strong bare coupling `g^4>=9.6x10^9`. Its proof citation is AX1 gate (2)–(3) (AM2 with `J_0'`; AQ2).

**In lattice units** the bound reads `a*Delta>=g^2/32`. On the admitted regime:

`(a*Delta)^2 >= g^4/1024 >= 9600000000/1024 = 9375000 = (1250 sqrt 6)^2`, so `a*Delta >= 1250 sqrt 6` ≈ **3061.862**.

The correlation length allowed by the bound is below `a/3061`. This is the ultra-local strong-coupling regime. For comparison, even a hypothetical gap bound `alpha/16` on the whole bridge region `g^4>=32` would still give `(a*Delta)^2>=1/32`.

**Physical units** (illustration only; no scale setting identifies any `a` with any `g`):
- At `g^2=10^5` (`g^4=10^10`, `tau=3/312500000<=10^-8`, admitted) and `a=0.1 fm`, with `hbar c=197.3269804 MeV fm`: `Delta>=g^2 hbar c/(32a)=31250*197.3269804 MeV = 493317451/80 MeV` ≈ **6.166 TeV**.
- At the cap, with the same `a`: `Delta>=12500 sqrt 6*197.3269804 MeV` ∈ [6041880.18, 6041880.19] MeV, ≈ 6.04 TeV.
- In units of the fixed reference: `Delta/E_star >= g^2/(32 a E_star)`.

**The clock.** In `theta=alpha t/hbar` units the gap is `1/16` at every `(a,g)`, and in `G=H/delta` units it is `1/2`. Those numbers are constant only because the unit `alpha` moves with `(a,g)`. Uniformity along a trajectory must be stated in units of the fixed `E_star` with fixed `hbar`. Non-unit fixture: with `alpha=5` and `hbar=7`, the physical frequency is `alpha/(16 hbar)=5/112`, against the normalized misread `1/14`.

## 5. The failure, stated exactly

**(a) On the named trajectory.** Since `g_n->0`, there is an `n_0` such that `g_n^4<9.6x10^9` for every `n>=n_0`. From then on the AX1/AM2 certificate is not available, and the family supplies no estimate uniform along `a_n->0` on that trajectory. The same holds for the bridge `g^4>=32` and for any finite contraction radius.

**(b) The failure needs the scope `g_n->0`.**
- At fixed `g^2=10^5` (admitted) with `a_n=1/n`, the bound `g^2/(32a_n)=3125n` holds at every n and increases.
- So "no estimate uniform along a_n->0" is **false** as a free-standing sentence.
- The fixed-g sequence is common rescaling: `a_n*Delta>=3125` is fixed. The bound in units of `E_star` diverges like `1/a_n`, so there is no finite-mass limit.

**(c) The admitted regime cannot host a scaling trajectory.**
- A continuum limit at a fixed positive physical gap `m` needs `a_n*Delta_n->0`.
- The admitted regime forces `a*Delta>=1250 sqrt 6`.
- Hence any trajectory with `a_n->0` and `a_n*Delta_n->0` stays in the regime for only finitely many n. This is the exact content of "physical scale control fails in the admitted regime".
- Equivalently, `(alpha a)^2=g^4/4>=2.4x10^9`: the electric scale is at least `20000 sqrt 6/a`.

**(d) The *form* of the estimate cannot survive the hypothesized trajectory.** This is conditional on the hypothesis, and it is not a premise.
- Suppose `Delta_n->m<infinity` and `g_n^2/a_n->infinity`. The second holds on any trajectory of asymptotic-freedom form, where `g^2` falls like `1/ln(1/a)`. Then `Delta_n>=g_n^2/(32a_n)` must fail for all large n.
- So the supplied estimate is not merely unproved along such a trajectory: its form is incompatible with the trajectory's hypothesized limit.
- A uniform-in-a estimate has to be of a different form, a gap in units of `E_star` bounded below. In lattice units such a bound tends to 0 faster than any power of `g^2` if dimensional transmutation holds.

**One-loop heuristic** (preview only, not a premise; `1/g^2=2b_0 ln(1/(a Lambda))`, `b_0=11/(24 pi^2)` for SU(2)):
- the cap corresponds to `a Lambda` ≈ 0.99989;
- the bridge corresponds to `a Lambda` ≈ 0.149.

The admitted regime therefore sits where `a` is of order `1/Lambda`, nowhere near a continuum. The scheme dependence of `Lambda` is not addressed.

## 6. The toy trajectory, exact

**Definition.** `n* = min{n>=1 : g_0^4/n^4 < threshold}` (strict). It is computed by an exact integer fourth root and a monotone correction, and cross-checked by a brute-force scan.

| `g_0` | threshold | `n*` | `g^4` at `n*-1` | `g^4` at `n*` |
|---|---|---:|---|---|
| declared `g_0^4=9.6x10^9` | cap `9.6x10^9` | **2** | `9600000000` (n=1, exactly on the cap, admitted) | `600000000` |
| declared | bridge `32` | **132** | `9600000000/294499921` ≈ 32.598 | `12500000/395307` ≈ 31.621 |
| rehearsal `g_0=1000` | cap | **4** | `10^12/81` ≈ 1.2346e10 | `3906250000` |
| rehearsal `g_0=1000` | bridge | **421** | `6250000/194481` ≈ 32.137 | `10^12/31414372081` ≈ 31.833 |

**The integer facts behind the table:**
- `131^4=294499921<3x10^8<132^4=303595776`;
- `420^4=31116960000<3.125x10^10<421^4=31414372081`;
- `3^4<625/6<4^4`.

The rehearsal values agree with the modern lens (4 and 421).

**Labelled extras** (not required):

| Condition | declared | `g_0=1000` |
|---|---:|---:|
| ends `g^4<8` | 187 | 595 |
| non-admitted route radius `g^4<26370048/7` | 8 | 23 |
| `tau/144=2/(3g^4)` exceeds the bound `|omega(W)|<=1` (`g^4<2/3`) | 347 | 1107 |

**Misreadings the controls reject:**
- a non-strict cap comparison gives `n*=1`;
- `g_n=g_0/n` read as `g_n^2=g_0^2/n` gives bridge indices 17321 and 176777;
- comparing `g_n^2` with 32 at `g_0=1000` gives 177.

**What the toy trajectory is not.** It declares no `a_n`, so the crossover indices are a-independent. It is a power law in n, not asymptotic-freedom running. It illustrates the crossover only.

If one declares the AL1 path shape `a_n=a_0/n` (illustration), then `alpha_n=g_0^2/(2a_0 n)`. With `g_0=1000`, for `n<=3`, the gap bound in physical units is `31250/(a_0 n)` and in lattice units `a_n Delta>=31250/n^2`.

**The AL1 frozen path** `a_n=a_0/n`, `g_n^2=1/n` has `tau_n=96n^2>3` for every `n>=1`, so the bridge fails at every n (retained, AL1 gate).

## 7. The AL1 bridge obstruction and common rescaling

**The bridge is retained.** The bridge condition is `g^4>=32`, not R18-B2's `32/3`, which belongs to a different finite-graph box.

**Common rescaling.** Multiplying both couplings, `(alpha,lambda)->(s alpha, s lambda)`, is exactly `a->a/s` at fixed g:
- every admission ratio (`r=4/g^4`, `tau=96/g^4`, `7|tau|`) is unchanged;
- the gap bound is multiplied by s relative to fixed `E_star`;
- checked on the fixture `g^2=10^5`, `a=1`, `s=7`.

So common rescaling can neither repair nor break the bridge or the cap.

**An independent magnetic multiplier** `lambda->s lambda` at fixed `alpha`:
- changes `g^4` to `g^4/s`, which changes the model and the action;
- the bridge needs `s<=g^4/32`;
- on the declared toy trajectory `s_max<1` from `n=132` on (≈ 0.98816 at n=132), and `s_max->0` as `g->0`.

This is the AL2 form. It is derived here from the dictionary because the AL2 gate is not snapshotted.

## 8. What a continuum construction would additionally require

Each row is `not_supplied`. The first three are the contract's; the last three are my additions.

| Requirement | What is missing | Missing premise | Candidate route (status) |
|---|---|---|---|
| **Uniform-in-a estimates** | a gap lower bound in units of `E_star`, with locality and clustering bounds, at every n along `a_n->0`, `g_n->0` | an estimate whose validity region contains `g->0`. `J'=2784/g^4` is unbounded as `g->0`, so the AM2/AX1 fixed point and gap exclusion cannot be continued, and no premise supplies a weak-coupling replacement | multiscale renormalization-group control (Balaban-type ultraviolet stability, known for the Euclidean Wilson action in finite volume; not read here, not a premise), re-derived for the Kogut–Susskind family or transferred with an identification theorem (AGENTS.md: shared notation does not transfer a gap) |
| **Reconstruction hypotheses** | the axioms of the limit: Osterwalder–Schrader (regularity, Euclidean invariance, reflection positivity, symmetry, clustering) for limits of gauge-invariant Schwinger functions, or a Hamiltonian reconstruction with identification maps between the lattice Hilbert spaces | existence of the limits (tightness or convergence of renormalized smeared correlation functions); restoration of Euclidean or Poincaré invariance from cubic symmetry; a mode of convergence that keeps the vacuum simple and the gap open. Strong-resolvent convergence alone does not: the vacuum eigenvalue can disappear or change multiplicity in the limit, and on different lattice Hilbert spaces a uniform gap passes to the limit only with identification maps, convergent renormalized ground energies and a surviving vacuum vector | reflection positivity at each spacing (the transfer matrix; OS positivity survives limits); everything else needs uniform-in-a bounds; none available |
| **Physical scale control** | a trajectory along which a fixed physical quantity (the gap, or a string tension) in units of `E_star` converges to a finite positive value while `a_n->0` | a non-perturbative `a(g)` relation (asymptotic freedom is the hypothesis, not derived) with two-sided gap bounds in units of `E_star`. In the admitted regime `a*Delta>=1250 sqrt 6`, so it cannot host `a_n*Delta_n->0` (§5c) | scale setting by a non-perturbatively bounded observable; running verified, not assumed |
| State identification at fixed a | the six AY2 obligations (uniqueness, whole-sequence convergence, translation invariance, rate in N, boundary independence of dynamics, padded-family dynamics) | unproved even at fixed a (AY2 gate) | AY2 table; not an AZ1 premise |
| Nontriviality | the limit is not Gaussian | any non-Gaussian estimate that survives `a_n->0`. The only rigorous non-Abelian d>2 scaling limit in the SOTA table (Chatterjee, SU(2) Yang–Mills–Higgs) is Gaussian | none in the premises |
| Observables | which operators converge (smeared Wilson loops, a renormalized field strength) | operator renormalization with a-dependent normalization | none in the premises |

No number in this package is a fraction of the continuum problem. Investigation 9 of 10 is a loop count.

## 9. The claimed Faizal–Shabir construction (lead only)

**The record.** Faizal and Shabir, arXiv:2606.19362 (Fortsch. Phys. 74 (2026) e70097), claim a reflection-positive SU(N) construction: a uniform transfer-operator gap, an area law, multiscale clustering to the continuum, OS reconstruction with a spectral gap, and coincidence of the strong- and weak-coupling continuum limits. The modern lens read it **at abstract depth only**. I did not read it, and it is unaudited.

**It changes nothing in AZ1:**
1. AZ1 states what *this* fixed-spacing Kogut–Susskind family supplies. A different construction (a Euclidean reflection-positive lattice, SU(N)) cannot supply an estimate for this family without an identification theorem.
2. Its central claim, if correct, concerns a continuum theory. It is not a uniform-in-a estimate for this family at `g^4>=9.6x10^9`.
3. Any route "from strong coupling" to a continuum with finite mass has to cross the whole coupling range, because of §5(c): the strong-coupling regime has `a*Delta` bounded below. What would have to be audited is exactly the estimate that §8 row 1 lists as missing.
4. **Its only effect on AZ1 is the disclosure.** The item-3 sentence ("no rigorous construction … was found in this or any prior sub-round's source search") is true. No `g->0` trajectory satisfies either bound, and nothing audited supplies a weak-coupling estimate. But it must be accompanied by the statement that one *claimed* construction was found, recorded as an unaudited lead and not a premise.

**A future skeptical diff should establish:**
- which estimate is uniform in a, and in which variables;
- its constants and coupling range;
- whether it applies to the Hamiltonian (`a_t->0`) limit of the Wilson action;
- an independent replay.

No priority, correctness or import statement follows.

## 10. What I will require of the producer

1. **Protocol.**
   - The contract hash checked, and the `check.py` sha256 recorded before evaluation.
   - The cap `tau`, `g_0^4` and the template read from the contract.
   - Byte-identical `-B` and `-B -O` replays.
   - An inventory of exactly 29 files.
2. **Dictionary.**
   - The three contract identities, plus the cross-identity, as literal rational-function identities (symbolic or polynomial). Evaluation at a few exact points is a supplement, not the proof.
   - Floats nowhere in admission.
3. **Regime.**
   - `0<tau<=10^-8` iff `g^4>=9600000000`, cited from AX1.
   - `-tau` as the `U_E` mirror, not a trajectory point.
   - The route radii 7/274688 and 1/20416, if mentioned, labelled as not admitted.
4. **Estimate.**
   - Exactly one necessary estimate, the volume-uniform gap `alpha/16=g^2/(32a)` at fixed a for `g^4>=9.6x10^9`.
   - Cited from the AX1 gate (2)–(3), not re-derived; without the citation the verdict is `limited`.
   - The "exactly one" reading stated beside the template.
5. **Failure.**
   - "Is admitted only for" as the reading of "needs".
   - "Eventually violated".
   - Scoped to `g_n->0` or the named trajectory.
   - Failure of a sufficient certificate, not of the gap, with the AM2 or AL1 quotation.
6. **Toy trajectory.**
   - `n*=2` and `132` (declared), and `4` and `421` (rehearsal), with the strict inequality and the neighbouring `g^4` values.
   - Exact integer comparison.
   - Labelled "toy, not of asymptotic-freedom form", with `a_n` undeclared or declared as an illustration.
7. **Item-3 sentence**, with the Faizal–Shabir disclosure (unaudited lead, not a premise). Preferably also noting that the bound failure on `g->0` paths is definitional.
8. **Bridge and rescaling.**
   - AL1 bridge `g^4>=32` retained.
   - The AL1 frozen path failing at every `n>=1` retained.
   - Common rescaling derived from the dictionary (or AL2 cited by name).
   - The magnetic multiplier `s<=g^4/32`.
9. **Requirements table**, with the three contract rows, each with its missing premise and `not_supplied`. The three extra rows are recommended.
10. **Wording.**
    - The template verbatim, with "at fixed a" added beside it.
    - The forbidden phrases only inside an explicit negating frame.
    - Every a-sense "uniform" negated, and never in a sentence with a bare "uniform" unless "volume-uniform" or "in N" is present.
    - No loop count as a fraction.
11. **Exports.**
    - `continuum_claim`, `uniform_in_a_claimed`, `weak_coupling_claim` and `loop_count_fraction_claimed`, all false.
    - `uniform_in_N_claimed: true` with scope `'volume-uniform at fixed a, strong bare coupling'`.
    - `scientific_priority_verified: false`.
    - The uniform selected triple, recording the contract's zero triple as a defect.
12. **Controls.** All 21 as damaging mutations, with stated AZ1 semantics for the inherited AX1 ids.

## 11. Predicted values (the post-comparison flags any difference)

| Quantity | Prediction |
|---|---|
| Identities | `alpha/16=g^2/(32a)`, `tau=96/g^4`, `alpha*lambda*a^2=1`, all exact |
| Cap | `g^4=9600000000` at `tau=10^-8`; `g^2=40000 sqrt 6` ≈ 97979.59 |
| Bridge; ends | `g^4>=32` (`tau<=3`); `g^4>=8` |
| `n*`, declared `g_0^4=9.6x10^9` | cap **2**, bridge **132** |
| `n*`, `g_0=1000` | cap **4**, bridge **421** |
| `g^4` next to the crossovers | 32.598 / 31.621 (declared); 1.2346e10 / 3.90625e9 and 32.137 / 31.833 (`g_0=1000`) |
| Lattice-units gap floor on the regime | `a*Delta>=1250 sqrt 6` ≈ 3061.862 (`(a Delta)^2>=9375000`) |
| Route radius (not admitted) | `7/274688` (≈ 2548.3 × cap), `g^4>=26370048/7` ≈ 3.767e6 |
| Gate fields | the four false fields false; `uniform_in_N_claimed` true with the scope string |
| Verdict if all holds | `accepted_within_scope`; `limited` without the AX1 proof citation; `insufficient` on any overclaim |

## 12. Producer-error checklist

1. **Crossover errors:** bridge index 131, or cap index 1 (a non-strict comparison at n=1, where `g_1^4` equals the cap).
2. **`g_n=g_0/n` read as `g_n^2=g_0^2/n`,** giving 17321; or `g_n^2` compared with 32, giving 177 at `g_0=1000`.
3. **The route radius `7/274688` used as the admitted regime.**
4. **An unscoped failure:** "no estimate uniform along a_n->0" without `g_n->0`.
5. **"The gap closes as g->0"** or any no-gap reading of a certificate failure.
6. **"No construction exists"** instead of "not found", or Faizal–Shabir omitted.
7. **Forbidden phrases:** "the continuum limit exists" outside a negating frame; "fraction of the problem" or a percentage.
8. **A bare "uniform"** in a sentence with an a-sense "uniform" and no "volume-uniform" or "in N".
9. **Contract defects copied:** the zero selected triple, or `uniform_in_N_claimed` missing from the exported fields.
10. **The gap in `theta` or normalized units** called uniform along the trajectory, or `E_star` moving with `alpha_n`.
11. **`tau/144=2/(3g^4)` extrapolated** to weak coupling.
12. **Numeric gap values at the cap** printed without a `sqrt 6` bracket, or floats in admission.

## 13. Replay and source-edit mutations

**Command.** `python3 -B research/round32/skeptic/az1_check.py --output <abs fresh dir>`. The checker refuses a non-fresh directory and any directory inside the checkout.

**Replays.** The normal (`-B`), `-B -O` and no-`-B` runs are byte-identical: `results.json` sha256 `980c9bc3…0b8`, recorded in `az1-independent-freeze.json`. No `.pyc` is written. The run takes about 0.2 s.

**Source-edit mutations.** These ran on copies of the checker in private scratch, with only `ROOT` repointed. The unmutated copy reproduces the results apart from its own `checker_sha256`.

**Twenty-four must-abort edits all abort at the intended check or control:**
- the dictionary `alpha` coefficient, the ratio coefficient 24 and the claimed gap coefficient: all abort at `dictionary_rational_function_identities`;
- the cap one decade off and the bridge `32/3`: both abort at `admitted_regime_and_bridge_in_g`;
- a non-strict crossover in either the exact or the brute-force routine: both abort at the cross-check `crossover methods disagree`;
- `G(R)` and `J_0'`: abort at `route_b_contraction_recomputed`;
- `sqrt 5` for `sqrt 6`: aborts at `lattice_units_gap_floor`;
- `hbar c`: aborts at `physical_units_example`;
- the contract and AX1 gate pins;
- the phrase scan removed, the negating frame dropped, the "not only" handling dropped, and "fails" dropped from the negators (the template then fails its own scan);
- a bare "uniform" added to a reference statement;
- the root-N check removed (caught by reason matching);
- the digest check removed (caught by reason matching);
- the bridge reason, the scope-string check and the verdict rule;
- the uniform triple replaced by the zero triple.

**Three edits are silent, and all are accounted for:**
- an off-by-five initial guess in the integer root, which the monotone correction repairs;
- an extra exact sample point;
- **a changed number in the toy prose sentence (132 to 131).** The validator reads the exported fields, not the prose, so prose–field consistency is a post-comparison read (contract review, deferred parts).
