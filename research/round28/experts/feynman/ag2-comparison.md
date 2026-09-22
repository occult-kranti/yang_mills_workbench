# AG2 post-freeze comparison and bounded next proposal

The advisor opened exchange after both AG2 producers froze. This review then
read the forward report/checker/output and the skeptic's independent derivation.
It does not modify any frozen producer. The two producer derivations and the
skeptic agree on the exact operator and supported scope; no mathematical defect
was found in the inspected forward estimates.

## Agreement and attribution

All three retain the original quadratic remainder, the pinched same-anchor
cubic term, other ordered cubic words, and the full higher tail. They keep the
unbounded graph domain, every support and root, actual AG1 generator, full E
transport, scalar centering and complete remaining mixing. The negative actual
quadratic vacuum coefficient excludes a quartic-only E interpretation in fixed
nonempty volume. No calculation claims an actual lower ratio from upper budgets.

Forward improves the first two levels by exact union geometry. Re-enumeration
using the frozen reverse implementation's `star` and `meeting` functions gives
the same depth-two distribution `{4:1,7:36,9:24,10:192}`. Consequently its
polynomial `Q2(a)=4a^4+252a^7+216a^9+1920a^10` is correct. This is a review
replay of the existing geometry, not a new investigation.

The forward tail remains an all-order proof: the rooted recurrence counts roots
in both old and incoming unions, bounds new union growth by three, and retains
repeats. Replacing `(8/3)_n/n!` by `(3)_n/n!` gives a positive complete tail.
Combining that tail with exact low-order counts is legitimate. Its compression
of C-A3 is contractive and retains the separate scalar and centered diagonal.
The complete reference bound `1-4M-K2/8` correctly uses supports of at least four
blocks and only vacuum-annihilating centered diagonal terms.

| Author and estimate | Main complete output norm upper budget | Narrow complete output norm upper budget |
|---|---:|---:|
| Forward, exact first two support levels plus rooted tail | `<0.006168` | `<0.000059689` |
| Reverse, rational `s=M/9` and relative-word tail | `0.00653109394414` | `0.000062602452769` |
| Skeptic, rational `s=4M/35` and relative-word tail | `0.00673686252904` | `0.000064496293980` |

These are compatible sufficient budgets. Their inequality is not disagreement
about an evaluated observable. In particular the forward first-two-level
refinement is attributed to the forward producer; it was not silently added to
the frozen reverse proof. The skeptic retains the main selected-filter estimate
also at its narrow endpoint, another harmless conservative difference.

Forward and skeptic additionally include elementary uniform-value/derivative
countercontrols. Reverse's derivative control concerns the bounded-commutator
and unbounded-domain implication. The full report proofs, rather than either
type of finite countercontrol, establish domain preservation in this model.

## Bounded AG3 proposal, not yet a contract or result

Use the **whole generated mixing family** `B_Y=P_Y K_Y Q_Y+adjoint` from AG2,
and the actual new reference `G_next=H0+D+Z`. Keep the scalar C separate but
retain it in the full Hamiltonian identity. Freeze an explicit source
decomposition; B_Y is local vacuum mixing, even though its identity extension
is not a rank operator relative to the global vacuum.

Test one additional triangular-filter correction with two explicitly reserved
weight losses, for example `2 -> 15/8` for interacting orbit estimates and
`15/8 -> 7/4` for nonlinear conjugation. These are suggested proof weights,
not claimed feasible constants. A predeclared main interval audit may be
insufficient; retain a separately frozen narrow `M<=1/10000` audit if the
advisor selects it. Do not execute a parameter search and retrospectively
declare the winning interval.

The useful reverse question is whether a source-specific free-filter estimate,
the complete arbitrary-support diagonal interaction, exact triangular-kernel
moments and paid commutator losses give a finite full update. All additional
original E terms have already entered B and Z; none can be dropped. Any
inequality comparing actual `||B||_2` with an output norm at `7/4` must be called
a weight-changing bound. It is not contraction in one unchanged norm, and the
AG2 upper budget is not an actual denominator. Handle B=0 before division.

Require the actual changed reference's graph domain, the complete generated
support class, bounded first commutator, scalar/mixing/diagonal re-extraction and
an explicit nonzero denominator wherever a ratio is used. Even success for this
one correction would not establish all-stage convergence, the original spectral
gap, physical matching or a four-dimensional continuum theory. The advisor and
skeptic choose the final bounded target after this review. No AG3 production was
performed for this comparison.

### Preferred proposal after advisor/Newton feedback

The subsequent bare-H0 inverse proposal is simpler for one bounded next step.
For every generated B_Y, invert H0,Y on its vacuum complement to obtain a local
rank generator X_B,Y. Its norm is at most ||B_Y|| and its first commutator is
`[X_B,H0]=-B`. This retains `[X_B,D_next]` in the exact residual instead of
requiring an inverse of the changed reference.

The advisor's proposed weight loss `2 -> 3/2` is valid for the generic rooted
commutator estimate. Nonempty overlap contributes `b^-1`; two root placements
and the commutator triangle bound give `4/(b e log(a/b))`. Equal loss at each
nested order and the factorial bound yield
`c=(8/3)/log(4/3)<=288/31`. The rational logarithm lower bound follows by
integrating `1-t+t^2-t^3` on `[0,1/3]`.

With actual `r=||B||_2`, `d=||D_next||_2`, the proposed exact residual is

```
sum_(n>=1) ad_(X_B)^n[D_next/n!+n B/(n+1)!].
```

The prospective bound is `r*c(d+r)/(1-cr)` when cr<1. The inherited coarse
caps `r<=0.007` and `d<=0.078` make its ratio no greater than
`3060/3623<17/20`. This hand assessment supports freezing that bounded target;
it is not AG3 production or independent executed evidence. Prefer it over the
filter proposal above. Its bound changes weights, all D and scalar terms remain,
zero r needs a separate case, and the same step cannot be iterated unchanged.

## Reviewed source bytes

```
forward/ag2/report.md
5fe9c6e404838945455a2dc0fb5b03d12d6b685db3147eeb6f607e0607f283b2
forward/ag2/check.py
a11f048d8d7e52e7bfb78c7094d6b8555e9061e93e90ca26b02b196c056e9758
forward/ag2/output/results.json
676e69d5941ab99343132e2465a05d12f4ca1fbbd0583b88cf09f316c51f1ea1
reverse/ag2/freeze.json
35c1427363b85461346d3d1354f2bd963de35e1011da720eee40d0c28c9b988a
skeptic/ag2-independent-derivation.md
b6a6f2eb2a06957bb4eba0e9790f1d2cef972d5686fb4f2a138cdf948e002872
skeptic/ag2-independent.json
90c014903d199e941b6643406cfe1bccbc3a256f85e756d400d6467e91f584ae
```

Paths in this final list are relative to `research/round28/`.
