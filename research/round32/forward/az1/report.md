# Hruday continuum-trajectory statement: the one estimate the fixed-spacing family supplies and its failure point — AZ1 forward (single producer)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production (a Claude model agent) under the frozen AZ1 contract (`research/round32/contracts/az1.json`, sha256 `91c828a7aa6ef9bd4d3dbf762363b7558faa6922c23e1aff476cd098d4177078`). AZ1 is a `statement+skeptic` loop: this is the only producer, and admission also needs the skeptic's independent derivation and replays (`single_direction_independent_replay`). This is correlated model-agent work, not independent human review and not formal verification.

**What this producer read.**
- **The contract snapshot first.** `check.py` verifies its sha256 before any evaluation. After that, only files under `inputs/`:
  - **read in full:** `AGENTS.md`; the contract; `selection-az1.md`; the AX1 gate (every field, including `bindings`); the AL1 forward report and the AL1 gate (including `bindings`); the AM2 gate (every field except `bindings`) and `skeptic/am2.md`; the I1 forward report; the AQ1 forward report; the modern lens `update-4.md`, `memo.md` and `sota-table.md`; the historical lens `update-4.md`;
  - **read in part:** the AX1 forward report (lines 1–165 and 490–547, plus a keyword scan); the AX1 reverse report (keyword-search lines only); `skeptic/ax1.md` (its first 100 lines, long lines cut at 700 characters, plus a keyword scan); the AM2 forward report (keyword lines and lines 96–110); the AM2 reverse report (keyword lines and lines 96–98); the AT4 forward report (keyword lines, lines 50–64 and 166–167); the AQ2 forward report (its first 20 lines); the paired-physics, Newton, Tesla and historical-panel SKILL files and the complete-residual reference (read with long lines cut at 400–600 characters);
  - **not opened:** the Newton and Tesla `references/research.md` notes and the historical-panel `lenses-and-evidence.md`. The checker hashes all 29 snapshots.
- **Outside `inputs/`, for protocol and code style only:** `research/round32/tools/README.md`, `research/round32/tools/freeze.py`, the AY2 forward checker `research/round32/forward/ay2/check.py` (helpers, contract parsing, the control sections, the packet assembly and `main`) and `research/round32/forward/ay2/report.md` (lines 1–140 and 300–417). None of these carries premise weight. The project's `CLAUDE.md` was shown to me as session context.
- **Not read:** nothing under `research/round32/skeptic/`, `research/round32/experts/` or `research/round32/advisor/` other than the snapshots in `inputs/`; no `advisor/deliberation-*.md` or `panel*.md`; nothing under `research/round32/forward/az2/`; no other agent's scratch folder.
- **Scratchpad disclosure (sub-round 2 rule).** My scratch work is in `/tmp/claude-0/az1-forward-private/`: a geometry and crossover preview (`prelim.py`), a value printer, a debugging importer and a report-scan printer that import `check.py` without writing bytecode (`values.py`, `dbg.py`, `scan.py`), development runs, the source-edit audit driver (`audit.py`) with its mirrored copies, and the production run `run1`. **None of it is evidence.** I created the folder directly with `mkdir -p` and did not list `/tmp/claude-0/` or the shared session scratchpad root, so I saw no other agent's folder names. **I opened no file in any other agent's scratchpad folder.** The Claude harness saved copies of two of my own long reads (the tail of the AY2 checker and the modern `update-4.md`) to its tool-results cache; I read the saved AY2 copy. Those are my own reads, not another agent's files.

**Shared premises and attribution.** Every admitted number used here is inherited: the dictionary is AL1's, the admitted regime and the supplied gap are AX1's (with AM2's cap), and the toy-trajectory design, the rehearsal `g_0=1000` and the cross-identity `alpha*lambda*a^2=1` were proposed by the modern and historical lenses (update-4). AZ1 contributes the statement itself, the exact verification of the dictionary identities by two routes, the exact crossover indices for the declared toy, the lattice-units reading of the supplied gap, and the requirement table with a missing premise for each row. The mathematics is elementary algebra. Scientific priority is unverified. HNM labels are project aliases.

## Verdict (forward, single producer)

1. **Trajectory and dictionary (item 1).** The trajectory `(a_n,g_n)` with `g_n->0` as `a_n->0` is a hypothesis of asymptotic-freedom form, not derived here (Section 1.3). The AL1 dictionary `alpha=g^2/(2a)`, `lambda=2/(g^2 a)`, `tau=24 lambda/alpha=96/g^4` places the admitted regime at `abs(tau)<=10^-8`, i.e. `g^4>=9600000000` at fixed `a` (strong bare coupling).
2. **The one estimate supplied, and its failure point (item 2).** Cited from the AX1 gate, not re-derived: the volume-uniform gap `alpha/16=g^2/(32a)` for `g^4>=9.6x10^9` at fixed `a`. Along any trajectory with `g_n->0` the admitted regime is left at a finite index, and the AL1 bridge `g^4>=32` is also violated from a finite index on; no estimate uniform along a_n->0 is supplied (Section 2).
3. **Toy trajectory (item 3).** For `g_n=g_0/n`, `a_n=a_0/n` at fixed `E_star`: with the declared `g_0^4=9.6x10^9`, `n*=2` (cap) and `n*=132` (bridge); with the panel rehearsal `g_0=1000`, `n*=4` and `n*=421`. All four are exact integer results, each found by two routes (Section 3).
4. **Obstruction and requirements (item 4).** The AL1 bridge obstruction is retained, the failure of common rescaling is derived from the dictionary, and the three continuum requirements are tabulated with a missing premise each (Section 4).
5. **Checker (item 5).** `check.py` runs **42 exact checks**. All **21 contract controls** reject explicit damaging mutations (**107** rejections inside the control checks, **121** in the whole checker), and none is deferred. The `-B` and `-B -O` outputs are byte-identical.

**Proposed forward verdict: `accepted_within_scope`** (forward half; no sub-label proposed). The contract's acceptance ("verified by the skeptic with the dictionary arithmetic exact") needs the skeptic's independent derivation and replays, which are outside this producer's work.

## 1. The named trajectory, the dictionary and the admitted regime

### 1.1 Model and scales

**Model label:** `uniform Kogut–Susskind SU(2) at fixed spacing, strong bare coupling`.
- This is the AX1 model: every elementary face of the SU(2) Kogut–Susskind Hamiltonian on `Z^3` carries the same coefficient `nu=alpha*tau/24`; route B with the Haar reference; centered whole-star boxes; cover `R={0,e_z}` (preregistered `model_id`: `AQ_uniform_routeB along (a_n,g_n)`).
- `E_star>0` is a fixed positive physical energy reference; it is never a regulator and never zero. No plateau fit is made.
- Units: the dictionary is written with `hbar=c=1`. Restoring units, `alpha=hbar c g^2/(2a)` and the gap bound is `hbar c g^2/(32a)`. The common clock is `s=alpha*t_E/hbar`, `theta=alpha*t/hbar`; the statement is static and the clock only fixes that `alpha/16` is an energy in the same units as `E_star`.

### 1.2 The dictionary (AL1, applied)

With the Bauer et al. convention recorded in AL1 (raw magnetic term `lambda sum_p(1-W_p)`, `W_p=Tr U_p/2`):

| quantity | value | source |
|---|---|---|
| `alpha` (electric scale) | `g^2/(2a)` | AL1.1, contract `parameters.dictionary` |
| `lambda` (magnetic coefficient) | `2/(g^2 a)` | AL1.1 |
| `r=lambda/alpha` | `4/g^4` | AL1.1 |
| `tau=24 lambda/alpha` | `96/g^4` | AL1.2 (`nu=lambda=alpha tau/24`) |
| `epsilon=7 abs(tau)` | `672/g^4` | AL1.2 |
| normalized unit `delta` | `alpha/8` | AL1, I1 |
| supplied gap `alpha/16` | `g^2/(32a)` | AX1 gate; AX1 reverse report |
| cross-identity | `alpha*lambda*a^2=1` | contract item 5 |
| first-order Wilson mean `tau/144` | `2/(3g^4)` | AX1 gate item 7, in the dictionary |

`check.py` verifies all of these, plus `alpha*tau/24=lambda`, `(alpha/8)*(tau/3)=lambda`, `(alpha/8)/2=g^2/(32a)`, `a*alpha/16=g^2/32` and `tau*g^4=96`, as literal identities (eleven distinct identities, from the contract, the template, the AX1 reverse report and the AL1, AX1 and I1 premises) by two routes (Section 5.5): as rational functions with integer polynomial coefficients in `(g,a,c)`, compared by cross-multiplication, and by direct `Fraction` arithmetic on a 35-point grid of exact `(g^2,a)`.

### 1.3 The trajectory (hypothesis, not derived)

**Hypothesis H_AF (a hypothesis of asymptotic-freedom form).** There is a sequence `(a_n,g_n)`, `n>=1`, with `a_n->0` and `g_n->0`, of the asymptotic-freedom form `g(a)^2 ~ 1/(2 b_0 log(1/(a Lambda)))` as `a->0` for some `b_0>0` and scale `Lambda`. This is stated as a hypothesis and is not derived here: no beta function is computed, no numerical `b_0` is used or source-audited, and no sequence is claimed to be the physical renormalization trajectory. Everything below uses only `g_n->0`.

The toy trajectory of Section 3 (`g_n=g_0/n`, `a_n=a_0/n`) is a labelled algebraic example of this form of limit; it decays faster than the logarithmic form above and is not a physical trajectory.

### 1.4 The admitted regime

For real `g`, `tau=96/g^4>0`, and for any `T>0`, `tau<=T` if and only if `g^4>=96/T`. At the preregistered cap `T=10^-8` (AX1, AM2):

`abs(tau)<=10^-8`  if and only if  `g^4>=96/10^-8=9600000000` (so `g^2>=40000 sqrt(6)`, about `9.79795897113e4`), at fixed `a`.

This is strong bare coupling. `tau<0` has no real `g`; in the uniform model it is the `U_E` mirror of `+abs(tau)` (AX1 gate item 7), not a point of any trajectory. The value `9600000000` is read from the AX1 gate, the AX1 skeptic table and four places in the contract, and recomputed as `96/tau` from the preregistered `tau=1/100000000`.

### 1.5 Rescaling cannot move the regime

`tau=24 lambda/alpha` depends on `g` only. Exactly (Section 5.5): `tau(c a)=tau(a)`, `alpha(c a)=alpha(a)/c`, `lambda(c a)=lambda(a)/c`, and `r` is unchanged when `alpha` and `lambda` are rescaled by a common factor. Changing the spacing at fixed `g`, changing the energy unit, or rescaling the whole Hamiltonian therefore moves the gap `g^2/(32a)` but never moves `tau`. Only `g` decides whether a point lies in the admitted regime.

## 2. The one estimate supplied (volume-uniform at fixed a) and its failure point

### 2.1 The supplied estimate, cited

The AX1 gate (`research/round32/advisor/ax1-gate.json`, hash-bound in `inputs/`) admits, for the uniform Kogut–Susskind SU(2) Hamiltonian at fixed spacing and strong bare coupling, both signs `abs(tau)<=10^-8`:

> "every finite complete-factor route-B volume has a unique gauge-invariant ground and full-space gap >=1/2 normalized (alpha/16 physical), with a nonzero physical excited sector" — and the gap `alpha/16` passes to the AQ subsequential states ("the gap alpha/16, cutoff-vector removal and AQ passage re-apply verbatim").

In the dictionary this is the volume-uniform gap `alpha/16=g^2/(32a)` for `g^4>=9.6x10^9` at fixed `a`: one lower bound, the same for every finite complete-factor volume (uniform in N), at one fixed spacing. It is cited, not re-derived; its proof is the AM2/AX1 creation-operator contraction (`J_0'G(R)<1073/175000000<1/64`, `2J_0'G'(R)<319/1562500<1`, with the per-site sum `J'=29 abs(tau)` including the incoming stars), recorded in the gate and re-read by `check.py`.

**Why this one.** A continuum mass gap needs, at the least, a lower bound on the gap in physical units that survives along the trajectory. This is the only estimate of that kind the family supplies. The AX1 gate also admits other volume-uniform constants at fixed `a` (the state bound `D'_ii`, the reset budget `102 abs(tau)`), and none of them is uniform along a_n->0 either; they are not needed for the statement (contract wording note D2).

### 2.2 The failure point

**Lemma (elementary).** If `g_n->0`, then for every threshold `T>0` there is an index `n0` with `g_n^4<T` for every `n>=n0`. This is the definition of the limit.

Applied with `T=9.6x10^9`: every trajectory with `g_n->0` leaves the admitted regime at a finite index. From that index on, `tau_n=96/g_n^4>10^-8`, the AM2/AX1 contraction is no longer available as admitted, and the family supplies no gap estimate at the spacing `a_n` at all; in particular it does not supply any estimate uniform along a_n->0. Applied with `T=32`: the AL1 bridge condition `g^4>=32` (equivalently `r=4/g^4<=1/8`) is also violated from a finite index on. On the AL1 frozen path `a_n=a_0/n`, `g_n^2=1/n` it fails at every `n>=1`, since `g_n^4=1/n^2<32`. The I1 omitted-interaction conditions `g^4>672/c_1` and `g^4>1344 c_2` (with `c_1(S)`, `c_2(S)` unevaluated) fail from a finite index on for any fixed positive values.

This is failure of a sufficient certificate, not absence of a gap (AL1 gate limitation): nothing here says the gap closes where the certificate stops.

**Not a sharp threshold.** `10^-8` is the preregistered cap at which the AM2 and AX1 certificates are admitted; the AM2 reverse report states that it is not a sharp threshold. The AX1 forward report records contraction-only margins (`abs(tau)<=7/274688` for the self-map, `abs(tau)<1/20416` for the exclusion), which are **not admitted** regimes because the rest of the AX1 chain was evaluated only at the cap. The failure point does not depend on where a fixed cap sits: `check.py` recomputes both margins from the gate constants and finds the declared toy leaving them at `n*=8` and `n*=9` as well (Section 3.3).

### 2.3 The supplied gap in lattice units

`a*alpha/16=g^2/32` exactly. Inside the admitted regime `g^2>=sqrt(9.6x10^9)`, so for every admitted `(a,g)`:

`a*Delta >= g^2/32 >= 19595917942265424785578272597647131/6400000000000000000000000000000` (about `3.06186217847e3`),

a directed lower bound from an integer square-root bracket of `9600000000`. The certified gap is more than three thousand times the inverse spacing. A trajectory with `a_n->0` that stayed inside the admitted regime would therefore have a certified `Delta_n>=3061/a_n`, which diverges in units of the fixed `E_star`. A finite physical gap along `a_n->0` requires `a_n*Delta_n->0`, which is impossible inside the admitted regime. This is the physical-scale face of the same failure point (requirement R3).

## 3. The toy trajectory

### 3.1 Declaration

**Toy T1 (declared primary):** `g_n=g_0/n`, `a_n=a_0/n`, `n>=1`, with `g_0^4=9.6x10^9` (the cap) and `E_star` fixed. **Toy T2 (the panel rehearsal, labelled second example):** the same law with `g_0=1000` (so `g_n^4=10^12/n^4`). The contract names `g_n` and `E_star`; `a_n=a_0/n` is declared here (wording note D7). Because `tau` does not depend on `a`, the crossover indices do not depend on the choice of `a_n`.

A crossover index `n*` is the first `n>=1` with `g_n^4` strictly below the threshold. `g_n^4` equal to the cap (`abs(tau)=10^-8`) is inside the admitted regime, which is inclusive.

### 3.2 Exact crossover indices

| toy | threshold | `n*` | `g^4` at `n*-1` (inside) | `g^4` at `n*` (outside) | `tau` at `n*` |
|---|---|---|---|---|---|
| T1, `g_0^4=9600000000` | cap `9600000000` | `n*=2` | `9600000000` (n=1, exactly the cap) | `600000000` | `1/6250000` (about `1.6e-7`) |
| T1, `g_0^4=9600000000` | bridge `32` | `n*=132` | `9600000000/294499921` (about `32.5976318343`) | `12500000/395307` (about `31.6209933039`) | `1185921/390625` (about `3.03595776`) |
| T2, `g_0=1000` | cap `9600000000` | `n*=4` | `1000000000000/81` (about `1.23456790123e10`) | `3906250000` | `6/244140625` (about `2.4576e-8`) |
| T2, `g_0=1000` | bridge `32` | `n*=421` | `6250000/194481` (about `32.1368154215`) | `1000000000000/31414372081` (about `31.8325636884`) | `94243116243/31250000000` (about `3.01577971977`) |

- For T1 the first crossover is at `n=2` because `(g_0/2)^4=g_0^4/16=600000000<9600000000`, while `n=1` sits exactly on the inclusive cap.
- Two routes give each index: the exact integer fourth root, `n*=iroot4(floor(g_0^4/T))+1` with `m^4<=F<(m+1)^4` checked (for T1 and the bridge, `F=300000000`, `131^4=294499921<=F<132^4=303595776`); and an exact `Fraction` scan `n=1,2,...`.
- The panel rehearsal in the modern `update-4.md` is reproduced for every index and power it states (`n*=4`, `n*=421`, `g_4^4=3906250000`, `420^4=31116960000`, `421^4=31414372081`), with one arithmetic slip found: it writes `g_3^4=10^12/81=12345679012+34/81`, but `10^12/81=12345679012+28/81` exactly (premise note P1, Section 5.6). No index is affected, since `g_3^4` is above the cap either way.

So the declared toy keeps the admitted regime only at `n=1` and keeps the much weaker bridge condition only through `n=131`; the rehearsal keeps them through `n=3` and `n=420`.

### 3.3 What the family supplies along the toy

Along T2 with `a_0=1/10 fm` and the declared `E_star=hbar c/(1 fm)` (about 197.327 MeV, preview), the supplied estimate gives `Delta_n/E_star>=g_0^2/(32 a_0 n E_star)=312500/n` for `n=1,2,3`, i.e. `Delta_1>=312500 fm^-1` (about `6.1664681e7` MeV, preview with the truncated CODATA 2018 value `hbar c=197.3269804 MeV fm`). From `n=4` on the family supplies no certificate; this is not a statement that the gap vanishes. Along T1, with the same `a_0` and `E_star`, only `n=1` is covered, with `Delta_1/E_star>=` about `3.06186217847e4` (a directed lower bound from the `sqrt(9.6x10^9)` bracket).

**Other thresholds, labelled (not admitted).** For the contraction-only margins of Section 2.2 the crossovers are `n*=8` (self-map) and `n*=9` (exclusion) for T1, and `n*=23` and `n*=27` for T2. A slower toy `g_n^4=g_0^4/n` with `g_0=1000` crosses the cap at `n*=105` and the bridge at `n*=31250000001`. Every one is finite, as the lemma requires.

### 3.4 The plain statement

No rigorous construction of a genuine asymptotic-freedom trajectory satisfying either bound uniformly along the trajectory was found in this or any prior sub-round's source search. This rests on the searches recorded in the snapshotted lens notes (the modern memo, which records under "What it fails to supply" `any estimate uniform along a -> 0 with g(a) -> 0`; the historical `update-4.md`, whose sub-round-4 search found no rigorous result of that kind, uniform in the lattice spacing, for this or a comparable strong-coupling lattice family to import; and the modern `update-4.md`); this producer ran no source search of its own.

**The one recorded lead.** Faizal and Shabir (arXiv:2606.19362, Fortschr. Phys. 74 (2026) e70097) claim a reflection-positive construction in which the strong-coupling and asymptotically-free continuum limits coincide. The modern lens read it at abstract depth only. It is unaudited and not imported: no premise, number or conclusion of AZ1 depends on it, and no priority or correctness statement about it is made. It is recorded as a lead for a future round's skeptical diff.

## 4. The bridge obstruction, common rescaling and what a continuum construction would require

### 4.1 The AL1 bridge obstruction (retained)

AL1: `r=4/g^4<=1/8` (the selected bridge) if and only if `g^4>=32`; the ends need `r<=1/2`, i.e. `g^4>=8`. The AL1 gate records that the frozen path `a_n=a_0/n`, `g_n^2=1/n` violates the bridge for every `n>=1` (`tau_n=96 n^2`, `alpha_n=1/(2a_0)` fixed) and that every path with `g->0` eventually violates it. `check.py` re-verifies the path for `n=1..1000` and the equivalence `4/32=1/8`, and rejects the substitution of the different finite-graph bound `g^4>=32/3` (R18-B2).

### 4.2 Common rescaling fails

Section 1.5 is the exact content: `tau` and `r` are invariant under `a->c a` and under a common rescaling of `alpha` and `lambda`, so no change of spacing at fixed `g`, of energy unit or of overall scale reaches `g^4>=9.6x10^9` (or `g^4>=32`) from a point outside it. The AL1 gate selected a follow-up loop to test common scale changes, but that result is not a shared premise of AZ1; the invariance is derived here from the AL1 dictionary alone (wording note D4).

### 4.3 What a continuum construction would additionally require

| id | requirement | what the fixed-spacing family supplies | missing premise | status |
|---|---|---|---|---|
| R1 | uniform-in-a estimates | not along a_n->0: at each fixed a with g^4>=9.6x10^9 only, the volume-uniform gap alpha/16 and the AX1 state bounds, and nothing once g_n^4<9.6x10^9 | A lower bound Delta(a_n,g_n)>=m E_star with a fixed m>0 for every n along a trajectory with a_n->0 and g_n->0, with the matching control of local states and correlations; it requires a certificate valid for g^4<9.6x10^9, outside strong bare coupling, and no admitted or source-audited result supplies one | missing |
| R2 | reconstruction hypotheses | fixed-a lattice objects only, no limit object: AQ subsequential states and their GNS Hamiltonians with the gap alpha/16, on a lattice with no rotation or Lorentz covariance | Osterwalder-Schrader axioms for limiting Euclidean Schwinger functions (reflection positivity passed to the limit, restored Euclidean invariance, regularity, clustering), or the Hamiltonian analogue: a limit of the Hilbert spaces and local algebras along a_n->0 carrying a self-adjoint nonnegative Hamiltonian with a unique vacuum, local fields and Poincare covariance; no such limit is constructed in the admitted material | missing |
| R3 | physical scale control | not a physical scale: in lattice units a*Delta>=g^2/32>3061 throughout the admitted regime, so the certified gap is a cutoff-scale quantity | A relation between a_n and g_n that holds a physical quantity fixed in units of E_star (the renormalization-group trajectory, here only the hypothesis H_AF), with a proof that a_n*Delta_n->0 while Delta_n/E_star stays bounded above and below; inside the admitted regime a_n*Delta_n>3061 for every n, so the certified Delta_n/E_star diverges as a_n->0 | missing |

### 4.4 No fraction

No number in this report is a fraction of the continuum problem. AZ1 is investigation 9 of 10 of Round32; that is an index of executed investigations, not a measure of progress on the continuum problem, and no percentage or completion estimate is given.

## 5. Mandatory sentence, label, exclusions, checker and verdict

### 5.1 The mandatory sentence (contract template, verbatim)

> Along the named trajectory (a_n,g_n), the fixed-spacing family supplies exactly one uniform estimate, the volume-uniform gap alpha/16=g^2/(32a) for g^4>=9.6x10^9, and fails to supply any estimate uniform along a_n->0; this is not a statement that the continuum limit exists, that any estimate is uniform in a, that the coupling is weak, or that any fraction of the continuum problem is thereby resolved.

Reading (wording notes D1, D2): the template's "exactly one" estimate is the one necessary estimate of Section 2.1, qualified by its apposition as volume-uniform at fixed a; the template quotes a forbidden phrase only inside a negation, so the report scan removes the template before scanning.

### 5.2 Model label and scope

- **Label:** `uniform Kogut–Susskind SU(2) at fixed spacing, strong bare coupling`.
- **Scope string of the one positive claim:** `volume-uniform at fixed a, strong bare coupling` (exported as `uniform_in_N_scope` with `uniform_in_N_claimed: true`).
- **Gate fields:** `continuum_claim: false`, `uniform_in_a_claimed: false`, `weak_coupling_claim: false`, `loop_count_fraction_claimed: false`; also `uniform_wilson_claim: false`, `resolved_interaction_shift: false`, `scientific_priority_verified: false`. (The AX1 gate's `uniform_wilson_claim: true` meant only the uniform model label, which AZ1 carries in its label; AZ1 makes no Wilson-mean claim.)

### 5.3 Exclusions

- **Contract, verbatim:** `any continuum construction`; `any uniform-in-a estimate`; `weak coupling`; `scientific priority`; `the continuum limit exists (phrase)`; `fraction of the problem (phrase)`.
- **Preregistration, verbatim:** `free reference inside enclosure => no interaction claim`; `uniqueness of any subsequential limit`; `whole-sequence convergence or rate in N`; `continuum or weak coupling`; `transfer from a finite graph`; `relabelling a static shift as dynamical`; `scientific priority`.
- **Additional:**
  - nothing is said about the actual gap where the certificate does not apply;
  - no asymptotic-freedom trajectory is derived, and no numerical beta-function coefficient is used;
  - the Faizal–Shabir construction is a lead, not a premise;
  - the contraction-only margins are not admitted regimes;
  - no estimate here is claimed both volume-uniform and uniform in a; the second sense is never claimed.

### 5.4 The two senses of the word

Two senses occur and are kept apart. The N-sense is the positive claim: volume-uniform (uniform in N, every finite complete-factor volume) at one fixed spacing. The a-sense is never claimed: no estimate is uniform in a, and none is uniform along a_n->0. A third, unrelated use is the model name (uniform Kogut–Susskind: the same coefficient on every face). `check.py` enforces this on this report: every occurrence of the word is qualified in place by one of these three senses, every a-sense sentence carries a negation or requirement word, and the two senses are never conjoined (the template is checked separately and is qualified by apposition).

### 5.5 Checks and controls

`check.py` runs 42 exact checks. Binding and premises: `contract_snapshot_sha256`, `premise_inventory_bound` (29 snapshots), `gate_bindings_match_snapshots` (22 snapshots are byte-identical to what the AX1 gate binds; the AL1 report is what the AL1 gate binds), `ax1_gate_fields_and_verdict`, `al1_gate_and_report_parsed`, `am2_gate_cap_and_gap`. Content: `dictionary_identities_symbolic`, `dictionary_identities_rational_grid`, `cap_coupling_equivalence`, `gap_physical_units_example`, `admitted_regime_lattice_units_floor`, `toy_gap_along_path`, `any_g_to_zero_path_leaves_regime`, `fixed_cap_sensitivity_not_admitted`, `continuum_requirements_listed`, `unaudited_lead_not_imported`, `mandatory_sentence_and_phrasing`, `gate_fields_exported`, `error_ledger_itemized`, `contract_wording_defects_recorded`, `report_item_and_control_map`, and the 21 controls below.

| control | damaging mutations rejected |
|---|---|
| `missing_incoming_stars` | outgoing stars only (2 anchors, per-site sum `8 abs(tau)`); single-factor groups dropped (`28 abs(tau)`, the patterned value); a single star at 0. The full incidence (7 stars, 2 groups, 153 faces, 88 meeting R, 82+6, 16 inside) is recomputed from the I1 owner map and equals the AX1 gate |
| `full_original_wilson_cover` | a single-factor cover `{0}`; the four drawn links as the cover (48 links and 36 endpoints required) |
| `wrong_delta_alpha_hbar_clock` | the normalized gap `1/2` read in `alpha` units (`alpha/2`); the gap-one route (`alpha/8`); the Haar on-site gap six as the interacting gap; a normalized clock; the mixed `g^2/(16a)` |
| `vector_versus_scalar_centering` | vector or scalar centering imposed on a statement (AT4 residues `1/10000`, `-51/10000`, `1/16` recomputed); a zero reference energy for the gap (two-level exact fixture) |
| `first_order_mean_charged` | the first-order mean set to zero; the sign slip `-tau/72`; `tau/72`. The mean `tau/144=2/(3g^4)` equals `1/14400000000` at the cap |
| `tau_scaling_exponent` | `tau` labelled `96/g^2`; `tau` labelled `a`-dependent; the lattice gap `a*alpha/16` labelled physical; the dictionary with `tau=96/g^2`. Exponents are measured by exact substitution |
| `changed_model_relabelled` | the patterned zero-selected model; the toy point `n=2` (`tau=16x10^-8`) labelled admitted; an AL1-path point labelled admitted; `tau<0` as a real-`g` coupling; a finite graph; the selected-strip reference; the trajectory points relabelled as one model |
| `coherent_evidence_tampering` | with the packet hash rebound: a control flipped; the T1 bridge index 131; the T1 cap index 1; the cap decade; `uniform_in_a_claimed` true; the scope string changed; the AX1 gate hash replaced; the AL1 gate snapshot removed; the mandatory sentence altered; the gap example doubled; a second estimate added; the trajectory marked derived; a requirement marked supplied; the verdict changed; `continuum_claim` true; a retained failure dropped |
| `insufficient_verdict_retained` | a missing citation relabelled accepted; an overclaim relabelled limited; inexact arithmetic relabelled accepted; the AL1 path failure dropped; the failure point relabelled resolved |
| `exact_arithmetic_admission` | float, bool, NaN and zero-denominator inputs; a decimal preview as an admission value; a float coupling in a crossover; a non-integer polynomial coefficient |
| `root_n_misuse` | a square-root crossover index (11 for T2); `g_n^4` read as `g_0^4/n^2`; the gap divided by a root of the volume |
| `no_priority_or_continuum_claim` | continuum, priority, weak-coupling, Wilson-mean, shift or a-sense flag set true |
| `trajectory_named` | the trajectory claimed derived; `a_n` unnamed; `g_n` constant; a claimed physical renormalization trajectory |
| `bridge_obstruction_retained` | the bridge dropped; the R18-B2 bound `32/3` substituted; common rescaling claimed to reach the cap; an `a`-dependent `tau` |
| `one_uniform_estimate_identified` | no estimate; a second estimate added; the patterned-model gate cited; the estimate read along a_n; the estimate re-derived instead of cited |
| `e_star_fixed_no_plateau` | `E_star=0`; `E_star` varying as `1/a_n`; a plateau fit; post-hoc node selection |
| `loop_count_not_fraction` | the loop-count flag set true; an investigation index exported as a fraction field; a fraction sentence appended to the report |
| `uniform_label_strong_coupling` | a weak-coupling label; a continuum label; "fixed spacing" missing; "strong bare coupling" missing |
| `uniform_in_N_not_in_a` | the appended sentences `The gap is uniform.`, `The gap is uniform in a.`, `The gap is uniform in N and in a.` and `The estimate holds uniformly along the trajectory.` |
| `dictionary_arithmetic_exact` | `alpha=g^2/a`; `lambda=1/(g^2 a)`; `tau=12 lambda/alpha`; the gap as `g^2/(16a)`; `alpha*lambda*a^2=2`; the grid with `alpha` denominator 1; a float grid coupling; a shifted cap decade |
| `toy_trajectory_crossover_exact` | the boundary `n=1` of T1 counted as a crossover; bridge indices 131 and 133 for T1; 3 and 420 for T2; the threshold `32/3`; the cap decade `9.6x10^8` |

### 5.6 Contract wording defects (non-blocking; each a verified fact about the frozen text)

- **D1** (`mandatory_sentence_template`): it contains the forbidden phrase listed first in `forbidden_phrasings`, inside a negation. The report scan removes the template's verbatim occurrence before scanning.
- **D2** (`mandatory_sentence_template`): `supplies exactly one uniform estimate` — the AX1 gate also admits other volume-uniform constants at fixed a (`D'_ii`, the reset `102 abs(tau)`). Read with item 2 as "exactly one necessary estimate"; none of them is uniform along a_n->0.
- **D3** (`parameters.failed`): `the AM2 contraction needs tau<=10^-8` — `10^-8` is the admitted preregistered cap, not a sharp threshold (AM2 reverse report; AX1 forward margins, not admitted). The failure point holds for every fixed cap.
- **D4** (`required[3]`): `the failure of common rescaling` refers to work after AL1 that is not a shared premise; the invariance is derived here from the AL1 dictionary.
- **D5** (`parameters.failed`): `the AL1 bridge condition g^4>=32 also fails` — along a trajectory with `g_n->0` it fails from a finite index on (T1: `n*=132`), not at every `n`; only on the AL1 frozen path does it fail at every `n`.
- **D6** (`preregistration.selected_triple_alpha_units`): `["0","0","0"]` is read as the route-B Haar reference; in the uniform model every selected face carries `tau/24` in `alpha` units, held in `psi_b` (AX1).
- **D7** (`parameters.toy_trajectory`): names `g_n` and `E_star` but not `a_n`; `a_n=a_0/n` is declared here, and the crossovers do not depend on it.
- **D8** (`preregistration.tau.signs_evaluated`): a real-`g` trajectory has `tau>0`; `tau<0` is the `U_E` mirror (AX1), not a trajectory point.
- **D9** (`preregistration.state_provenance`): `finite_volume uniform bound` carries an unqualified word; read as volume-uniform at fixed a.

Premise arithmetic note (lens text, not contract text): **P1** (`experts/modern/update-4.md`, section 3): the rehearsal's `g_3^4=10^12/81=12345679012+34/81` should read `12345679012+28/81` (`81 x 12345679012 = 999999999972`, remainder 28). The crossover indices it states are correct.

Relayed-instruction notes (not contract text): R1, `uniform_wilson_claim` is exported false as instructed (see Section 5.2); R2, the relayed freeze command omits `--verdict`, which `freeze.py` requires, so the proposed forward verdict text is passed.

### 5.7 Proposed verdict

**`accepted_within_scope` (forward half), no sub-label proposed** (none of the five preregistered sub-labels describes a dictionary statement). The rule in `check.py` follows the contract acceptance:
- `insufficient` on any overclaim flag;
- `limited` if the failure point is stated without the supplied estimate's proof citation (and, as this producer's reading, if the dictionary arithmetic were inexact);
- otherwise `accepted_within_scope`, which the skeptic's independent derivation and replays must still confirm.

Retained failures (exported): T1 leaves the admitted regime at `n*=2` and the bridge at `n*=132`; T2 at `n*=4` and `n*=421`; the AL1 frozen path fails the bridge at every `n`; the I1 omitted conditions stay unevaluated; no estimate along a_n->0 is supplied.

### 5.8 Limitations and audit

1. **Scope.** Only the uniform Kogut–Susskind SU(2) model at fixed spacing and strong bare coupling, as admitted by AX1, and the dictionary of AL1. The trajectory is a hypothesis; the toy is algebraic.
2. **Inherited without re-proof.** The AX1 gap (AM2 contraction, cutoff removal, AQ passage), the AL1 dictionary and bridge, the I1 geometry. `check.py` re-reads their recorded constants and recomputes the incidence, but it does not re-prove any theorem.
3. **The error ledger** has one entry, `not_applicable` with the stated reason: exact integer and rational arithmetic only; the one irrational quantity, `sqrt(9.6x10^9)`, is bracketed by integer square roots of width `10^-30` and enters only as a lower bound.
4. **Correlation.** Single producer; all agents are correlated model agents; the lens notes proposed the toy, the rehearsal and the cross-identity. The skeptic's independent derivation is the second admission input.
5. **Priority.** Scientific priority is unverified.

**Source-edit audit (private scratch, not evidence).** I ran thirteen damaging edits, each on a mirrored copy of this directory in `/tmp/claude-0/az1-forward-private/audit/`, plus one unmutated copy, which reproduces the development run byte-for-byte. Every damaging edit aborts `check.py`:
- **Contract:** a byte edit, and `alpha=g^2/(2a)` changed to `g^2/(4a)` in the snapshot, both abort at the sha256 check.
- **Arithmetic and geometry:** the crossover route changed to `isqrt(F)+1` aborts at the crossover bracket; the `tau` coefficient 24 changed to 25 aborts at `tau=96/g^4`; outgoing-only anchors abort at the AX1 incidence; `continuum_claim` set true aborts at `gate_fields_exported`.
- **Discrimination:** the crossover test weakened from `<` to `<=` aborts, because the control mutation that counts `n=1` of T1 as a crossover is then accepted.
- **Report:** the mandatory sentence altered, a forbidden phrase appended, an unqualified sentence with the word appended, row R3 removed from Section 4.3, one control row removed from the Section 5.9 map, and `n*=132` replaced by `n*=131` each abort at the report scans.

**Methodological lenses** (modern use of the snapshotted skills):
- **Newton, analysis before synthesis.** The statement first separates what the fixed-spacing certificates determine (a lower bound on the gap at each admitted `(a,g)`) from what they cannot (anything once `g_n^4<9.6x10^9`), and never turns a failed sufficient condition into a bound on the actual gap.
- **Tesla, whole-device accounting.** The clock, `E_star`, the incoming stars and the complete cover are carried through the dictionary unchanged, and every threshold is shown with its own crossover.

No historical figure endorses anything here, and no historical or occult material supplies a premise.

### 5.9 Map of required items and controls to statements and checks

| item / control | where stated | `check.py` check id(s) |
|---|---|---|
| item 1 (trajectory hypothesis, dictionary, admitted regime) | §§1.1–1.5 | `al1_gate_and_report_parsed`, `ax1_gate_fields_and_verdict`, `cap_coupling_equivalence`, `trajectory_named`, `dictionary_identities_symbolic` |
| item 2 (the one estimate, cited; failure point) | §§2.1–2.3 | `one_uniform_estimate_identified`, `am2_gate_cap_and_gap`, `any_g_to_zero_path_leaves_regime`, `admitted_regime_lattice_units_floor`, `fixed_cap_sensitivity_not_admitted` |
| item 3 (toy trajectory, crossovers, plain statement) | §§3.1–3.4 | `toy_trajectory_crossover_exact`, `toy_gap_along_path`, `gap_physical_units_example`, `unaudited_lead_not_imported` |
| item 4 (bridge, rescaling, requirements, no fraction) | §§4.1–4.4 | `bridge_obstruction_retained`, `continuum_requirements_listed`, `loop_count_not_fraction` |
| item 5 (exact checker, controls, sentence, gate fields) | §§1.2, 5.1–5.5 | `dictionary_arithmetic_exact`, `dictionary_identities_rational_grid`, `mandatory_sentence_and_phrasing`, `gate_fields_exported`, the 21 control ids, `error_ledger_itemized`, `contract_wording_defects_recorded`, `report_item_and_control_map` |
| item 6 (skeptic; phrasings; two senses) | §§5.1, 5.4 | `mandatory_sentence_and_phrasing`, `uniform_in_N_not_in_a` (the skeptic's derivation and replays are outside this producer) |
| contract and premise binding | header | `contract_snapshot_sha256`, `premise_inventory_bound`, `gate_bindings_match_snapshots` |
| `missing_incoming_stars` | §§2.1, 5.5 | `missing_incoming_stars` |
| `full_original_wilson_cover` | §§1.1, 5.5 | `full_original_wilson_cover` |
| `wrong_delta_alpha_hbar_clock` | §§1.1, 1.2 | `wrong_delta_alpha_hbar_clock` |
| `vector_versus_scalar_centering` | §5.5 | `vector_versus_scalar_centering` |
| `first_order_mean_charged` | §§1.2, 5.5 | `first_order_mean_charged` |
| `tau_scaling_exponent` | §§1.5, 5.5 | `tau_scaling_exponent` |
| `changed_model_relabelled` | §§1.1, 1.4 | `changed_model_relabelled` |
| `coherent_evidence_tampering` | §5.5 | `coherent_evidence_tampering` |
| `insufficient_verdict_retained` | §5.7 | `insufficient_verdict_retained` |
| `exact_arithmetic_admission` | §§1.2, 5.8 | `exact_arithmetic_admission` |
| `root_n_misuse` | §§3.2, 5.5 | `root_n_misuse` |
| `no_priority_or_continuum_claim` | header, §5.2 | `no_priority_or_continuum_claim` |
| `trajectory_named` | §§1.3, 3.1 | `trajectory_named` |
| `bridge_obstruction_retained` | §§2.2, 4.1, 4.2 | `bridge_obstruction_retained` |
| `one_uniform_estimate_identified` | §2.1 | `one_uniform_estimate_identified` |
| `e_star_fixed_no_plateau` | §§1.1, 3.3 | `e_star_fixed_no_plateau` |
| `loop_count_not_fraction` | §4.4 | `loop_count_not_fraction` |
| `uniform_label_strong_coupling` | §§1.1, 5.2 | `uniform_label_strong_coupling` |
| `uniform_in_N_not_in_a` | §§2.1, 5.4 | `uniform_in_N_not_in_a` |
| `dictionary_arithmetic_exact` | §§1.2, 5.5 | `dictionary_arithmetic_exact` |
| `toy_trajectory_crossover_exact` | §3.2 | `toy_trajectory_crossover_exact` |

### 5.10 Reproduction

```bash
python3 -B research/round32/forward/az1/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/forward/az1/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round32/tools/freeze.py verify research/round32/forward/az1
```

`check.py` verifies the contract sha256 before any evaluation and records its own sha256 before evaluation. It writes `results.json` and `source-manifest.json`; the manifest records the sha256 of `check.py`, `report.md`, every `inputs/` file and `results.json`. AZ1 is investigation 9 of 10 in Round32. This producer executed only the forward statement of AZ1.
