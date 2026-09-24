# AZ1 contract review (skeptic, pre-comparison)

**Standing.** I wrote this from the frozen `contracts/az1.json` (sha256 `91c828a7…7078`, frozen 2026-09-24T04:29:40Z) before reading anything of the AZ1 producer.

From `research/round32/forward/az1/` I saw only file names: the 29 files in `inputs/`, listed with `find` and hashed against their repository sources (all byte-identical). I opened none of them. One whole-tree `git status` at the start of this package showed no untracked or modified path. Later `git status` runs were restricted to `research/round32/skeptic`. I did not open `research/round32/forward/az2/`.

I am a model-agent skeptic with correlated ancestry, and this is not human review. Two of my own files shaped AZ1:
- My triage goal-5 note and the `continuum` group of `prospective-controls.json` are the origin of five of the 21 controls: `trajectory_named`, `bridge_obstruction_retained`, `one_uniform_estimate_identified`, `e_star_fixed_no_plateau` and `loop_count_not_fraction`.
- My `ax1.md` is a shared premise.

Human author: Hruday N M (BUNZEEY).

**Verdict: executable as written, with the readings below.** Nothing blocks production.
- **Checker.** `az1_check.py` has 82 checks and 28 controls: the 21 contract ids plus 7 extra. It rejects 122 mutations, 101 of them inside the 21 contract controls.
- **Control mirror.** `controls` equals `preregistration.controls_required.ids`, 21 = 21. All three new ids are present: `uniform_in_N_not_in_a`, `dictionary_arithmetic_exact` and `toy_trajectory_crossover_exact`.
- **Inventory.** The declared inventory is 29 files: AGENTS.md, the contract and 27 shared premises. It equals the `inputs/` listing.

The checker confirms:

| Item | Value (exact unless marked) |
|---|---|
| Dictionary identities | `alpha/16=g^2/(32a)`, `tau=24 lambda/alpha=96/g^4`, `alpha*lambda*a^2=1`, `r=4/g^4`, `nu=lambda`, `nu/delta=tau/3`, `7|tau|=672/g^4`, `g^4=4 alpha/lambda`: nine identities of rational functions in `(g^2, a)`, each proved by cross-multiplication to the zero polynomial |
| Admitted regime | `tau<=10^-8` iff `g^4>=9600000000` (AX1 gate) |
| AL1 bridge | `r<=1/8` iff `tau<=3` iff `g^4>=32` |
| Toy trajectory `g_n=g_0/n`, declared `g_0^4=9.6x10^9` | `n*=2` (cap), `n*=132` (bridge): `g_131^4=9600000000/294499921` ≈ 32.598, `g_132^4=12500000/395307` ≈ 31.621 |
| Panel rehearsal `g_0=1000` | `n*=4` (cap), `n*=421` (bridge): `g_3^4` ≈ 1.2346e10, `g_4^4=3906250000`, `g_420^4` ≈ 32.137, `g_421^4` ≈ 31.833 |
| Lattice-units gap floor in the admitted regime | `(a*alpha/16)^2=g^4/1024>=9375000=(1250 sqrt 6)^2`, so `a*Delta>=1250 sqrt 6` ≈ 3061.862 |
| Route radii (printed in AX1 forward; **not admitted**) | self-map `|tau|<=7/274688` (≈ 2548.3 × cap, `g^4>=26370048/7` ≈ 3.767e6); exclusion `|tau|<1/20416` |

**Is the target well-posed as a feasibility check?** Yes, and it is met by construction.
- **What the target is.** `preregistration.target` reads ">= 1" on "dictionary identities verified exactly and the toy-trajectory crossover indices computed", and says it is a feasibility/format check, not a blind threshold. I read it as a Boolean: every identity holds exactly and both crossover indices are computed by exact comparison.
- **What it can catch.** It catches arithmetic errors:
  - `alpha=g^2/a` makes `alpha*lambda*a^2=2`;
  - `tau=24/g^4`;
  - a crossover off by one or computed non-strictly;
  - `g_n=g_0/n` read as `g_n^2=g_0^2/n`, which gives bridge index 17321.
- **What it cannot catch.** It cannot test anything substantive: the failure statement, the scope of "uniform", the requirements table or the verdict. Those rest on the controls and on my post-comparison reading. The target is well-posed but not informative.

## Readings and wording defects

All are non-blocking.

1. **The preregistered selected triple is the patterned family's, not the uniform model's.**
   - `preregistration.selected_triple_alpha_units` is `["0","0","0"]`, but `model_id` is `AQ_uniform_routeB along (a_n,g_n)`.
   - The uniform route-B model has every face at `alpha*tau/24`. Its AX1 contract carries the symbolic triple `["tau/24","tau/24","tau/24"]` (plan.json vocabulary extension). AX1's own `changed_model_relabelled` control rejects the zero triple under the uniform label.
   - The block looks copied from AY2 (patterned family).
   - My validator requires the uniform triple. If the producer copies the zero triple, I will record it as this contract defect, not as a model change, because no AZ1 quantity depends on the triple.
2. **`gate_fields_required` is partial.**
   - It lists the four false fields: `continuum_claim`, `uniform_in_a_claimed`, `weak_coupling_claim` and `loop_count_fraction_claimed`.
   - Item 5 adds `uniform_in_N_claimed: true` with the scope string `'volume-uniform at fixed a, strong bare coupling'`.
   - The producer should export all five, plus `scientific_priority_verified: false`. This is the same pattern as AY2's five-versus-ten fields.
3. **The mandatory template contains a forbidden phrase.**
   - "the continuum limit exists" occurs verbatim inside the template, negated: "this is not a statement that the continuum limit exists". A literal phrase scan rejects the mandatory sentence, so the scan must allow a negated frame.
   - My scanner accepts a forbidden phrase only after an explicit frame ("not a statement that", "not claimed that", "does not assert that" and similar) in the same clause. It rejects "It is not hard to see that the continuum limit exists".
4. **"fraction of the problem" as a literal phrase is too narrow.**
   - It misses the template's own "fraction of the continuum problem" (negated there).
   - It also misses "9/10 of the continuum problem" and "90% of the problem".
   - My scan uses a pattern. "Investigation 9 of 10" is a loop count and passes.
5. **The template omits "at fixed a".** It says "the volume-uniform gap alpha/16=g^2/(32a) for g^4>=9.6x10^9". The scope string supplies "at fixed a". The producer should put "at fixed a" in the sentence next to the template, not edit the template.
6. **"supplies exactly one uniform estimate" is a selection, not a count.**
   - AX1 also admits other volume-uniform bounds for this model:
     - `D'_ii` (|omega(W)|<=D');
     - the reset `102|tau|`;
     - `epsilon_R<=17|tau|`;
     - the Nachtergaele–Sims constants.
   - Item 2 says "identify exactly one **necessary** uniform estimate". The reading is: the one necessary gap estimate identified, not the only volume-uniform bound.
   - The producer should state this reading beside the verbatim template.
7. **Item 2, "the AM2 contraction needs tau<=10^-8", reads as "is admitted only for".**
   - The frozen cap `J_0'=29/10^8` with `J'=29|tau|` gives `|tau|<=10^-8`.
   - The AX1 forward report prints wider route radii, `|tau|<=7/274688` and `|tau|<1/20416`. These are not frozen, reviewed or admitted, and must never be used as the regime.
   - Even the route radius gives only `g^4>=26370048/7` ≈ 3.77e6, so the conclusion is unchanged. Any finite contraction radius bounds `g^4` from below, because `J'=29|tau|=2784/g^4`.
   - "Violated on every g->0 path" means *eventually* violated, not violated at every n.
8. **Failure of a sufficient certificate, not a gap.**
   - AM2 says "It does not interpret rejection beyond the chosen cap as actual gap failure". The AL1 gate limitation says "failure of a specified sufficient certificate, not a no-gap or continuum-impossibility theorem".
   - The producer must quote one of them next to the failure statement.
   - A sentence implying that the gap closes as g→0 is an overclaim.
9. **The failure must be scoped to `g_n->0`.**
   - At fixed g in the admitted regime, sending `a_n->0` keeps the estimate at every n. Example: `g^2=10^5` and `a_n=1/n` give a bound of `3125 n`.
   - This is common rescaling: `a_n*Delta>=3125` stays fixed. It is not a finite-mass limit.
   - "No estimate uniform along a_n->0" is therefore false unless it is scoped to the named trajectory or to `g_n->0`.
   - The template is scoped by "Along the named trajectory". A free-standing producer sentence may not be.
   - This is my extra control `failure_scoped_to_g_to_zero`.
10. **Item 3's "not found" sentence is a tautology, and it needs a disclosure.**
    - **Tautology.** No sequence `g_n->0` satisfies `g_n^4>=c` for all n, for any `c>0`. So "no rigorous construction of a genuine asymptotic-freedom trajectory satisfying either bound uniformly was found" is true by the shape of the regime, not because of a source search.
    - **The substantive statement** is that no premise supplies an estimate valid at weak coupling, that is, a replacement for the contraction.
    - **Disclosure.** The sub-round-4 modern search did find a *claimed* construction: Faizal–Shabir, arXiv:2606.19362, read at abstract depth and unaudited. The producer must disclose it in the same sentence or the next one, as an unaudited lead and not a premise. Omitting it misleads by omission. My validator binds the disclosure to the prose.
11. **The toy trajectory declares no `a_n`.**
    - The crossover indices depend only on `g_n^4`, so they are independent of a.
    - The gap in physical units along the toy trajectory is not determined unless `a_n` is declared. Any declared `a_n` should be labelled as an illustration.
    - `g_n=g_0/n` is a power law in n with no relation to a, so it is not of asymptotic-freedom form. The producer should label it "toy, not of asymptotic-freedom form".
12. **At n=1 the declared toy trajectory sits exactly on the cap.**
    - `g_1^4=9.6x10^9`, `tau=10^-8`, which is admitted.
    - "First drops below" is strict, so `n*=2`. A non-strict reading gives `n*=1` and is a rejected mutation.
13. **"Failure of common rescaling" is an AL2 result, and the AL2 gate is not snapshotted.**
    - The only premise mention is the AL1 gate `decision` ("Select AL2 … to test common scale changes").
    - The result can be derived in one line from the dictionary. `(alpha,lambda)->(s alpha, s lambda)` is `a->a/s` at fixed g. Every admission ratio (`r=4/g^4`, `tau=96/g^4`) is unchanged, and the gap bound scales by s relative to fixed `E_star`, so common rescaling can neither repair nor break the bridge. An independent magnetic multiplier `lambda->s lambda` changes `g^4` to `g^4/s`, needs `s<=g^4/32`, and `s->0` as `g->0`.
    - The producer should derive it this way or cite AL2 by name only.
14. **Only positive τ lies on a real-g trajectory.**
    - `signs_evaluated` is `["+","-"]` and item 1 says `|tau|<=10^-8`.
    - For real g, `tau=96/g^4>0`, so a real-g trajectory has `0<tau<=10^-8`. `-tau` is the `U_E` mirror (AX1 gate), with the same gap, not a trajectory point.
15. **`error_terms_itemized` is "not_applicable … no enclosure".**
    - That holds only if the report keeps the gap symbolic or works in `g^4`.
    - At the cap, `g^2=40000 sqrt 6` is irrational. Any printed numeric gap (about `3061.86/a`) needs a directed `sqrt 6` bracket and an arithmetic term.
16. **`direction_note`** says the lenses "kept AZ1 unchanged after sub-round 4". Panel update 4 kept the *goal* but adopted new contract requirements (identities, toy trajectory, the `uniform_in_N_not_in_a` control, template, gate fields). This is a clerical wording issue.
17. **Inherited AX1 controls have thin AZ1 meaning.**
    - `missing_incoming_stars`, `full_original_wilson_cover`, `vector_versus_scalar_centering` and `first_order_mean_charged` concern R-local constants that AZ1 only cites.
    - My semantics guard the cited quantities:
      - `missing_incoming_stars`: the regime is `J_0'/J'` with `J'=29|tau|`;
      - `full_original_wilson_cover`: the cover R has 48 links and 36 endpoints;
      - `vector_versus_scalar_centering`: the gap is measured from the actual ground, not from `lambda N_p`;
      - `first_order_mean_charged`: `tau/144=2/(3g^4)` is a fixed-a strong-coupling coefficient, never extrapolated. It exceeds the bound `|omega(W)|<=1` once `g^4<2/3`, at n=347 on the declared toy trajectory.
    - The producer may implement them the same way. They discriminate little for a dictionary statement.
18. **Premises not snapshotted.** Besides AL2, `contracts/ax1.json` and `advisor/ay2-gate.json` are not AZ1 inputs. The uniform triple and the AY2 obligations can be quoted from the AX1 gate and `selection-az1.md`.

## Control semantics for the three new ids (as executed)

- **`uniform_in_N_not_in_a`** rejects any of the following:
  - `uniform_in_a_claimed: true`;
  - a scope string without "at fixed a";
  - `uniform_in_N_claimed` dropped;
  - an estimate scope "N and a";
  - a sentence where an a-sense "uniform" (in a, along `a_n`, along the trajectory) shares the sentence with a bare "uniform" and has no N-qualifier ("volume-uniform", "uniform in N");
  - an a-sense "uniform" not preceded by a negator (the "not only … but also" trick is caught);
  - "uniform along the trajectory" asserted.

  The template passes, because its bare "uniform estimate" is resolved by the appositive "volume-uniform".
- **`dictionary_arithmetic_exact`** rejects any of the following:
  - `alpha=g^2/a`;
  - `lambda=2/(g^4 a)`;
  - `alpha/16=g^2/(16a)`;
  - `tau=24/g^4`;
  - `tau=r` (ratio coefficient 1);
  - `alpha*lambda*a^2=2`;
  - a cap `g^4` one decade off.

  Each is decided by recomputing the rational-function identities from the packet's own dictionary.
- **`toy_trajectory_crossover_exact`** rejects any of the following:
  - bridge index 131;
  - a non-strict inequality;
  - cap index 1;
  - swapped rehearsal indices;
  - the rehearsal bridge computed on `g^2` (177);
  - a changed rehearsal `g_0`;
  - a floating fourth-root method.

  Each is decided by exact integer comparison, with a brute-force cross-check.

**Deferred parts** (executed on synthetic or reference inputs, rechecked at post-comparison):
- the producer's actual freeze and 29-file inventory;
- its requirements table;
- the phrase scans of its report (forbidden phrases, the two senses of "uniform", fractions, the lead disclosure);
- the consistency between its prose numbers and its exported fields. The validator reads fields, so editing a number in a prose sentence is silent; the source-edit audit confirms this.
