# AG2 post-freeze comparison and prospective AG3 target

This additive review was written after the advisor confirmed both AG2 freezes
and opened exchange. The current reverse report and skeptic independent
derivation were then read. No frozen producer was edited, and no AG3 checker,
contract or production was executed by this reviewer. This is contemporary
model-agent review, not Newton's participation, external human review or a
formal proof-assistant verification.

## Agreement and valid differences

The reverse and skeptic derivations agree with the forward report on the
mathematical object and every essential implication:

- The exact original transform is `G+R_O1`, and `E=R_O1-A3` includes the
  quadratic words, compressed same-anchor cubic words, all other cubic words,
  and the entire higher tail. All ordered repetitions and complete supports
  remain. The actual fixed-volume quadratic vacuum coefficient excludes a
  fourth-order assignment to E, without calculating the complete quadratic
  mixing.
- `C_b-A3_b=P_b C_b P_b+Q_b C_b Q_b` is contractive block compression. The
  scalar is retained with the centered complement, so there is no duplicated
  scalar or fictitious omitted same-anchor mixing.
- The full AG1 transform retains `exp(ad_S)E` and the nonlinear coefficients
  `ad_S^n(n A3+R_A3)/(n+1)!`. The original and correction generators are distinct,
  and each is justified on the actual graph domain before expansion.
- The resulting complete output K has a weight-two bound. Splitting every
  indexed term gives a bounded mixing family and a locally vacuum-annihilating
  centered diagonal. Because assigned supports contain at least four blocks,
  its relative diagonal cost is `||K||_2/8`. This proves a new reference-only
  gap, while retaining the full Hamiltonian's mixing.

The different positive bounds are compatible. Forward counts the entire finite
low-order relative geometry exactly and uses a rooted all-order tail. Its
depth-two counts `(1,36,24,192)` at sizes `(4,7,9,10)` total253, agreeing with
the skeptic's independently recorded total. Reverse and skeptic use the valid
looser `13^n n!` count, separating the one repeated-anchor cubic word from the
at-most337 others. Reverse additionally uses the tighter rational linear bound
`M/9`, while forward and skeptic use `4M/35`; reverse's separate cubic bound
also differs from `M^3/567`. These choices explain unequal sufficient constants
without implying unequal physical measurements.

Forward proves a scalar energy density `k/64`. Reverse independently obtains
the same factor by dividing the scalar root-incidence sum by the minimum
support size. The skeptic's displayed `k/16` scalar bound is weaker and valid;
its relative diagonal `k/8` agrees. No mathematical correction to the frozen
reports is needed on these points. A shared conservative consequence is
`||K||_2<0.007` on the main interval, with `||D_next||_2<=64M+2||K||_2` and
`G_next` gap at least `1-4M-||K||_2/8`.

## Recommended bounded AG3 question

**Make one complete bare-reference elimination of the actual full mixing B,
using an explicitly lower output weight, while retaining the entire current
diagonal and scalar.** A changed-reference inverse is not essential for this
single step. It remains a possible strategy for a future iteration; the old
O2 certificate's retained-diagonal obstruction is a warning about that complete
iteration, not a prohibition on one controlled update.

Start from the complete AG2 identity
`H_corrected=C I+H0+D_next+B`. Freeze the actual indexed B decomposition and
let `r=||B||_2`, not its upper certificate. Each B_Y is exactly the local
vacuum/complement mixing block, so

```
v_Y=B_Y Omega_Y,
u_Y=(H0,Y|Q_Y)^(-1)v_Y,
Y_Y=|u_Y><Omega_Y|-adjoint, Y=sum_Y Y_Y.
```

The bare gap one gives `||Y||_2<=r`, `[Y,H0]=-B`, and the familiar graph-domain
proof works on arbitrary generated supports. The exterior identity is retained.
It is not an inverse of the full commutator with D_next. Instead retain its
entire contribution in the exact proposed identity

```
exp(Y)(C I+H0+D_next+B)exp(-Y)=C I+H0+D_next+R_next,
R_next=sum_(n>=1) [ad_Y^n(D_next)/n!
                  +n ad_Y^n(B)/(n+1)!].
```

The scalar C commutes and is still present. Afterward split R_next again into
scalar, mixing and centered diagonal on every generated support. No term of
the current D_next is discarded or silently absorbed into the bare inverse.

## Advisor's sharper prospective weight estimate

I checked the advisor's proposed improvement to the generic O2 loss constant.
For `a>b>1`, a nonzero commutator has intersecting supports. Therefore
`b^|X union Z|<=b^|X| b^|Z|/b`. The commutator contributes factor2. Splitting
the root between the two supports, and using
`m(b/a)^m<=1/[e log(a/b)]`, gives

```
||[U,V]||_b<=4/[b e log(a/b)] ||U||_a ||V||_a.
```

No incoming-root or overlap cost is missing: each of the two root assignments
costs `2/[b e log(a/b)]`. Allocate `log(4/3)` equally across n nested brackets
from input weight2 to output weight3/2. Every intermediate weight is at least
3/2. The factorial inequality `n!>=(n/e)^n` cancels the factors n and e, giving
the prospective constant

```
c=(8/3)/log(4/3)<=288/31,
||ad_Y^n V||_(3/2)/n! <= (c r)^n ||V||_2.
```

Here `log(4/3)>=31/108` is the four-term alternating-log lower bound. Hence
the desired one-step conclusion can use

```
||R_next||_(3/2)<= (d+r) c r/(1-c r), d=||D_next||_2.
```

Only the coefficient may replace r and d by proved upper bounds. The actual
r remains the final multiplicative input norm. Using the common AG2 main-cap
certificates `r<=0.007`, `d<=0.064+0.014=0.078` suggests the explicit target

```
||R_next||_(3/2)<=q ||B||_2,
q<=3060/3623<17/20.
```

This is a proposed contract target, not an admitted AG3 result. At r=0 the
generator and new remainder vanish; there is no denominator division. The
bound would compare different support weights. It is neither same-weight
contraction nor a proof that repeated updates retain a positive limiting weight.
This refined main-interval target is more useful than the earlier coarse
`12/loss` estimate, which suggested contraction only on the narrow interval.

The frozen AG3 acceptance should require the domain argument, complete
nonlinear identity, every scalar/diagonal update, continuous interval bounds,
actual-r multiplicative estimate and exact controls rejecting dropped D and
reused weight. A new reference-only gap may be established after the final split,
but must again be separated from the full Hamiltonian. The original homogeneous
gap, all-stage convergence and continuum claims remain outside this one step.

## Inspected frozen records

Hashes identify the reports read and output/freeze metadata inspected; this
review does not claim a new replay of the producer implementations.

| Record | SHA-256 |
|---|---|
| `forward/ag2/report.md` | `5fe9c6e404838945455a2dc0fb5b03d12d6b685db3147eeb6f607e0607f283b2` |
| `reverse/ag2/report.md` | `a65de31a483640c5131b2afee906b0486cd455d665f3417ec7e015a872ca0456` |
| `reverse/ag2/freeze.json` | `35c1427363b85461346d3d1354f2bd963de35e1011da720eee40d0c28c9b988a` |
| `reverse/ag2/output/results.json` | `3d1971ab4f614f7732783f2ec7003fc62c7b9bd43f3429dccb31835fe204383b` |
| `skeptic/ag2-independent-derivation.md` | `b6a6f2eb2a06957bb4eba0e9790f1d2cef972d5686fb4f2a138cdf948e002872` |
| `skeptic/ag2-independent-freeze.json` | `daa9c037851b556d06d022b729a499e424d7ed6f8a5e34e0a2f06e23ddc20da2` |
| `skeptic/ag2-independent.json` | `90c014903d199e941b6643406cfe1bccbc3a256f85e756d400d6467e91f584ae` |

Paths in this table are relative to `research/round28/`.
