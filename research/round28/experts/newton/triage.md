# Newton-method triage for Round28

This is pre-contract selection advice, not a new physics execution. The lens is a contemporary analysis/synthesis method, not Newton's participation or endorsement. Baseline: `a7f4b8dd42ce0f31f2442c068815f6d1f75ade1a`. No new physics checker has been run. Reading and proposed bounds below must be independently derived and checked under the advisor's frozen contract before admission.

## Recommended AG2 target

**Account for every term of the original O1 transform at the actual AG1 input weight, transport that complete inventory through the accepted AG1 update, and extract a fully budgeted next reference and its remaining mixing.** This closes AG1's conditional-E premise. It should not promise contraction of the complete remainder or a second correction before learning what the inventory contains.

Write the original O1 generator as `X=sum_b S_b^(1)` and its first-order source as `A^(1)=sum_b A_b^(1)` to avoid confusing either with AG1's cubic source or filtered generator. The exact inherited identity is

```
exp(X)(H0+Phi)exp(-X) = G + R_O1,
G = H0 + D,
R_O1 = sum_(n>=1) [ad_X^n(Phi)/n! - ad_X^n(A^(1))/(n+1)!].
```

Let `C_b` be S1's repeated-anchor cubic word and `A_b^(3)` its vacuum off-diagonal projection. With `A_selected=sum_b A_b^(3)`, the actual object left outside AG1 is exactly

```
E_original = R_O1 - A_selected.
```

The declared indexed inventory should contain four parts:

| Part | Exact content | Lowest degree in tau | Declared support |
|---|---|---:|---|
| E2 | `[X,Phi]-[X,A^(1)]/2 = [X,D]+[X,A^(1)]/2`, with every ordered seed/generator pair | 2 | Union of two intersecting stars; up to 7 sites |
| E3,other | Every depth-two ordered word except `(b0,b1,b2)=(b,b,b)` | 3 | Connected union of three stars; up to 10 sites |
| E3,same | `sum_b(C_b-A_b^(3))` | 3 | Original four-site stars |
| E>=4 | Every depth `n>=3` word, retaining factorials and repeated anchors | 4 | Arbitrary connected unions, size at most `4+3n` |

This is an algebraic partition, not an assertion that every listed part is nonzero in the actual model. In particular, the quadratic term must not be assumed scalar or vacuum-annihilating. O1 already proves a nonzero quadratic vacuum expectation in each fixed nonempty volume, which prohibits treating the full E as fourth order. It does not identify the full quadratic mixing operator.

There is a useful economical partition: `C_b-A_b^(3)=P_b C_b P_b+Q_b C_b Q_b`, whose operator norm is at most `||C_b||`. Thus removing the selected source does not require adding its norm to the full cubic-word budget. For the later scalar/diagonal split this remains `c_b I+Q_b(C_b-c_b I)Q_b`; the scalar is retained. A triangle estimate `||E||<=||R_O1||+||A_selected||` is also valid but less informative. Any use of the compression bound must state the changed indexed decomposition explicitly.

## Bound questions to freeze

1. **General-weight O1 sum.** For a support weight `a>=2`, repeating O1's two root assignments suggests
   `N0(a)<=4 a^4 b`, `N_(n+1)(a)<=8 s a^3(8+3n)N_n(a)`, where `s<=sqrt(7/12)|tau|` and the seed norm is at most `b`. Hence the candidate all-order majorant is
   `4 a^4 (M+sigma/2)[(1-24 s a^3)^(-8/3)-1]`, where `M=7|tau|`, `sigma=sqrt(7/12)|tau|` and `24 s a^3<1`. Derive it again under the contract, split out degrees two and three, and bound the positive tail continuously over the chosen interval. This is a proposal, not an admitted new result.
2. **Actual input weight.** Use `rho=9/4` if retaining the frozen AG1 proof. A bound only at weight two does not satisfy its transport premise. Preserve whole-star boundary deletion, all word multiplicities, and incoming roots.
3. **Complete transport.** Apply the inherited identity
   `exp(S_AG1)(G+A_selected+E_original)exp(-S_AG1)=G+R_filtered+N_AG1+exp(ad_S_AG1)E_original`.
   Convert a proved `||E_original||rho<=e(tau)` into `e(tau)/(1-theta(tau))` at weight two, with the admitted complete nonlinear budget and every first commutator present.
4. **Next reference.** Split every self-adjoint output term into scalar, vacuum mixing and centered reference diagonal. Keep scalar support/density, a full mixing bound, and the diagonal relative-form update. Establish the finite-volume operator domain separately. A gap for this *reference* does not yet give a gap for the reference plus its mixing.
5. **Actual versus upper norms.** The AG1 factor below `2/3` compares its selected output with the actual selected-source norm. Comparing the complete E budget with that upper cubic certificate cannot prove whole-input contraction. A complete contraction claim requires its own actual denominator or a directly proved operator inequality; retain a limited verdict if it is unavailable.
6. **Weight available afterward.** Display the remaining support-weight schedule. The consumed `9/4 -> 2` margin cannot be reset. AG3 should be chosen after the complete E result and skeptic response, with a newly justified source class and local inverse if a changed reference is proposed.

Useful controls to freeze: exact finite-degree reconstruction through the entire cubic coefficient; deletion of the depth-one term; wrong repeated-anchor multiplicity; replacement of E by a quartic-only tail; scalar omission; use of an upper bound in a contraction denominator; use of weight-two input in the weight-`9/4` transport premise; the old O2 retained-diagonal linear-term control. Matrix fixtures test algebra and rejection semantics, not SU(2) gap completeness.

## What Round27 changes about the decision

The addendum, final panel and network now establish selected-source AG1 contraction and complete nonlinear control; their edge to AG2 remains a proposed transfer because E was conditional. AI1's limiting-map fibers and AI2's one successful coherent two-hypothesis disk test do not supply a homogeneous stability premise. O2 explains why merely iterating a bare-reference inverse with a retained diagonal and summable weight loss can fail its own certificate. S1 supplies an actual cubic source, while explicitly withholding its identification with the full remainder. These facts favor full inventory before a new correction.

## Primary reading deepened in this triage

The exact reading ledger is `sources.json`; prior Round27 reading is distinguished there.

**Newton, Of Natures obvious laws, ALCH00081.** Newly read the normalized English discussion around ff. 2r–2v, especially numbered sections 8–9 and the proposed salt/fume circulation argument. This extends Round27's opening outline. Newton connects proposed invisible mechanisms with comparative processes and replenishment arguments. Several inferences depend on assuming which products or reservoirs exhaust the alternatives. The methodological lesson here is an explicit missing-term inventory. Neither the mineral-fume claims nor the manuscript's speculative unification are modern physical premises or evidence of a Yang–Mills mechanism.

**Newton, October 1666 Tract on Fluxions, NATP00100.** Newly read the textual statement of Proposition 7, selected Proposition 8 discussion of reductions and termwise reconstruction, and the opening of Proposition 7's demonstration. Some displayed formulas are omitted by the retrieved normalized-text rendering, so this is not a complete mathematical transcription audit. The passage motivates checking a reconstruction against its originating relation and retaining each term. The modern domain, convergence and interaction-norm proofs must supply the justifications that a historical procedural analogy does not.

**Del Vecchio, Fröhlich and Pizzo, arXiv:2108.13907.** Newly inspected Section 3's three size regimes, the complete displayed Theorem 3.1 statement, its opening induction and the opening tree-reexpansion definition (PDF pages indexed 14–17). The theorem couples potential estimates with the next local reference gap and uses additional weighted quantities for the large-support regime. This deepens O1's earlier domain-lemma/final-theorem reading. The full intervening proof and auxiliary Lemma 4.3 are not audited here, and the small coupling threshold remains unspecified in these passages. The useful lead for a later AG3 is a coupled norm/gap/source-class induction, not an imported numerical threshold.

A current primary-source search was also attempted on 2026-09-22. Its recent results concerned different model classes and did not establish a new applicable theorem. This is limited retrieval, not an exhaustive SOTA review or evidence that no newer applicable result exists. Scientific priority remains unverified.
