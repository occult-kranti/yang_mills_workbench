# O2 reverse: generated-support homological iteration

## Verdict and reconstructed closure conditions

The arbitrary-support homological step is valid, and an explicit exponential
weight-loss estimate gives a complete one-step majorant. The resulting
baseline scalar recurrence cannot certify infinitely many stages for any
nonzero tau. Its retained diagonal term supplies a nonvanishing linear
coefficient while the available weight loss tends to zero. This is a proved
obstruction to the stated majorant, **not** failure of the actual rotation
algorithm, the homogeneous gap, or every possible weight-sensitive estimate.
The numerical stability target remains limited. No current forward O2 or
skeptic O2 finding was read; no subsequent loop is selected here.

Start from the admitted common O1 certificate, not the smaller reverse-only
constant: `r0=(25460736/25)tau^2`, `b0=448|tau|`, `a0=28|tau|`, with
`|tau|<=5/1664`. Here r bounds residual interaction norm, b the retained
diagonal interaction norm, and a its form-relative coefficient. A successful
route would require residuals tending to zero, summable scalar/diagonal and
generator corrections, a positive limiting support weight, and `a_infinity<1`.
The calculations below test all of these obligations together.

## 1. Arbitrary-support scalar, diagonal and homological splitting

At a stage in a finite cuboid write

`H=E I+H0+D+R`, `R=sum_Y R_Y`,

with self-adjoint bounded R_Y and explicit indexed finite supports Y. Generated
supports are retained; they are not reset to stars. D is a sum of self-adjoint
local terms annihilating their local product vacua. Empty-support scalar terms
are accumulated in E separately. On each nonempty Y let

\[
 P=|\Omega_Y\rangle\langle\Omega_Y|,\quad Q=I-P,\quad
 c=\langle\Omega_Y,R_Y\Omega_Y\rangle,\quad v=Q R_Y\Omega_Y,
\]
\[
 A_Y=|v\rangle\langle\Omega_Y|+|\Omega_Y\rangle\langle v|,
 \quad Z_Y=Q(R_Y-cI)Q.
\]

Then exactly `R_Y=cI+A_Y+Z_Y`. In particular cI replaces cP only because
the subtraction `-cQ` is included in Z. The explicit bounds are

`|c|<=||R_Y||`, `||A_Y||=||v||<=||R_Y||`, `||Z_Y||<=2||R_Y||`.

The bare product reference satisfies `H0_Y|Q>=1` for every nonempty finite Y.
Thus `u=(H0_Y|Q)^(-1)v` lies in its operator domain and obeys
`||u||<=||v||`, `H0_Y u=v`. Define
`S_Y=|u><Omega_Y|-|Omega_Y><u|`. It is skew-adjoint, with
`||S_Y||=||u||<=||R_Y||`, and `[S_Y,H0]=-A_Y` on D(H0).

The inverse-gap premise is exactly the unchanged *bare* gap one. This inverse
does not contain D, so no actual local gap of H0+D is needed merely to define
the step. Such positivity is needed later for a spectral certificate.

The O1 domain proof extends to any finite Y: both local products with H0_Y
are bounded, exterior spectral projections commute, and nonnegative sums
identify the full domain with the local/exterior domain intersection. For a
summable indexed decomposition in a finite cuboid, both S=sum S_Y and the
bounded commutator A=sum A_Y converge in the graph-operator estimates.
Hence S is bounded in the H0 graph norm and `exp(+/-S)D(H0)=D(H0)`.
This proves the common unbounded operator-domain statement without assuming
arbitrary bounded observables preserve it.

For `||R||_mu<=r`, all of S and A have norm at most r, Z has norm at most 2r.
The scalar sum obeys `|sum_Y c_Y|<=|Lambda|r`; it is an extensive energy
bookkeeping term, not a local observable with empty support assigned positive
weight. No scalar is deleted from the Hamiltonian identity.

## 2. Weight loss for all supports and all orders

Let `mu'>=0`, `delta=mu-mu'>0`. Define the commutator interaction by every
ordered intersecting pair `(X,Y)` with declared support X union Y. Splitting
the site-root sum into roots in X and roots in Y gives

\[
 \|[\Phi,\Psi]\|_{\mu'}
 \le\frac4{e\delta}\|\Phi\|_\mu\|\Psi\|_\mu.
 \tag{1}
\]

For example, in the root-in-X part, sum the Y interactions by one of their
intersection sites in X. This costs |X|; use
`e^(mu'|X union Y|)<=e^(mu'|X|)e^(mu'|Y|)` and
`|X|e^(-delta|X|)<=1/(e delta)`. The commutator norm costs two and the
other root placement another factor two. Ordered multiplicities and every
support union remain in the interaction decomposition.

For n nested commutators, spend delta/n at each of the n steps. The generator
norm at every intermediate weight is at most its initial norm s. Applying
(1) repeatedly and using `n!>=(n/e)^n` gives

\[
 \frac1{n!}\|\operatorname{ad}_S^n K\|_{\mu'}
 \le\left(\frac{4s}{\delta}\right)^n\|K\|_\mu.
 \tag{2}
\]

The factorial inequality follows by integrating log on [1,n]. This estimate
covers arbitrary generated supports, without a fixed support-size cutoff.

An equal-weight universal bilinear bound is false. On a union Y of N adjacent
stars, m=`3N+1` sites, use qubits, H0=sum_i N_i, and
`K_Y=2^(-m)(|1^m><0^m|+adjoint)`. At mu=log 2 its interaction norm is one.
Let `D_i=N_i/64` for i in Y, each declared on its containing four-site star
inside a larger cuboid. At most four such stars meet a site, so `||D||_mu<=1`.
Every D_i annihilates its local vacuum, yet

`exp(mu*m)||[D,K_Y]||=m/64`,

which is unbounded as N grows. Retaining larger declared commutator supports
can only increase this lower benchmark. This rules out an equal-weight
constant valid for all bounded interactions. It does **not** prove weight loss
is unavoidable for the more structured homological pair: its inverse here
divides the all-excited vector by m, and `[D,S_Y]` instead has weighted norm
1/64. That valid cancellation is retained as an exception/control.

## 3. Complete one-step recurrence, including D

With C=sum c_Y, A=sum A_Y and Z=sum Z_Y, graph-domain integration of the first
bounded commutator gives the exact finite-volume identity

\[
 e^SHe^{-S}=(E+C)I+H0+(D+Z)+R',
\]
\[
 R'=\sum_{n\ge1}\left\{
 \frac{\operatorname{ad}_S^n(D+R)}{n!}
 -\frac{\operatorname{ad}_S^n A}{(n+1)!}\right\}.
 \tag{3}
\]

The scalar pieces of R commute automatically. Neither `[S,D]` nor any higher
commutator involving D is discarded. As in O1, unbounded H0 is integrated
first and only bounded operators enter these norm series.

Let `||D||_mu<=b`, `||R||_mu<=r`, and set `u=4r/delta`. For u<1, (2)-(3) imply

\[
 \boxed{r'\le F(r,b;\delta)
 :=\frac{u}{1-u}(b+3r/2).}
 \tag{4}
\]

Indeed `s<=r`, `||D+R||<=b+r`, and A's extra factorial costs at most r/2
for every n>=1. This majorant is conservative but fully explicit.

For the retained diagonal update at the new weight,

`b'<=b+2r`, `a'<=a+2r`.

The relative estimate follows from `Q_Y<=sum_(x in Y)(I-P_x)`: the unweighted
per-site sum of `||Z_Y||` is at most 2r. The scalar density increment is at
most r. These bounds include all site overlap multiplicities automatically.

If these bounds held through all stages with `sum r_n<infinity`, `r_n->0`
and `a0+2sum r_n<1`, then in every fixed finite volume the cumulative scalar,
diagonal and generators would converge. Generator sums also converge in the
graph estimates because `||S_n||,||[H0,S_n]||<=|Lambda|r_n`. The products of
unitaries and their inverses consequently converge in both Hilbert and graph
operator norms. The limiting transformed Hamiltonian is H0+D_infinity plus
its retained scalar, and has gap at least `1-a0-2sum r_n`, uniformly in volume.
This is a conditional finite-volume spectral implication; it constructs no
infinite global unitary or representation identification.

## 4. Evaluate the baseline and locate its precise obstruction

Use the contract's schedule

`mu_n=log(2)/2+log(2)/(2(n+1))`,
`delta_n=log(2)/(2(n+1)(n+2))`.

It spends a total log(2)/2 and has positive limit log(2)/2. Define the explicit
scalar upper iteration by equality in (4), with
`b_(n+1)=b_n+2r_n`, `a_(n+1)=a_n+2r_n`, and the common O1 initial bounds.
Its step is admitted only if `4r_n<delta_n`.

For r_n>0, an actual decrease of this chosen scalar majorant requires exactly

\[
 F(r_n,b_n;\delta_n)<r_n
 \quad\Longleftrightarrow\quad
 \delta_n>4b_n+10r_n.
 \tag{5}
\]

Since `b_n>=b0=448|tau|>0` and delta_n tends to zero, (5) cannot hold
eventually at any fixed nonzero tau. More strongly, if all steps remained
admissible then

\[
 \frac{r_{n+1}}{r_n}
 =\frac{4(b_n+3r_n/2)}{\delta_n-4r_n}
 \ge\frac{4b0}{\delta_n}.
\]

After delta_n<=2b0 this ratio is at least two forever. The positive r_n would
then grow geometrically, contradicting admissibility `r_n<delta_n/4->0`.
Thus every positive-tau scalar trajectory either fails a step earlier or
necessarily leaves this majorant's radius after finitely many stages. This is
a proof about the scalar bounds, not an assumed lower bound on actual residuals.
Tau=0 is the exact trivial exception.

For the explicit example `tau=10^-8`, initially
`b0=0.00000448`, `a0=0.00000028`, and
`r0=0.000000000101842944`. Controlled rational logarithm bounds and exact
arithmetic verify the first four shrinking stages. Nevertheless `log 2<7/10`
implies delta_n<=2b0 for every n>=197, since
`(n+1)(n+2)>=7/(40b0)` there. Conditional on reaching those stages, the
same majorant then doubles at every step and cannot remain admissible forever.
The checker does not pretend that early shrinkage proves closure or sample
the tiny residual numerically through all 197 stages.

The same obstruction applies to this *same loss-only majorant* under any
decreasing positive-limit schedule: positive summable losses tend to zero
while its b_n remains at least b0. It does not exclude a sharper treatment of
the structured D-homological commutator, a gap-dressed inverse, or an applicable
source induction with different norms. A meaningful next missing estimate is
one controlling `[S(R),D]` using D's vacuum structure and relative coefficient
without paying a vanishing support-loss denominator at every stage. Its
inverse/domain and generated-support hypotheses would require a new proof.

## 5. Controls, sources and limits

An exact three-level fixture checks the complete scalar/diagonal split and
bare inverse, rejecting the double-counted `cQ` alternative. A growing union
of stars gives the equal-weight failure and its homological cancellation
exception above. A separate one-qubit fixture has `D=dN`, residual rX and
bare generator r times the real skew flip. Its new offdiagonal residual is

`r cos(2r)-(1+d)sin(2r)/2=-dr+O(r^3)`.

At `d=1/100,r=1/1000000`, Taylor remainder bounds enclose it strictly below
zero and within a controlled error of -dr. It rejects deleting D or asserting
a universal purely quadratic recurrence in r at fixed D. These are operator
lemma controls, not physical SU(2) simulations or measured gap failures.

The actual source closure binds every v2 instruction snapshot and accepted
dependency. The primary comparison reuses the actual O1 reading: Yarotsky's
Section 2, Lemma 1 and equations (8),(14)-(15) employ a structured fixed-point
and spectral representation, with constants not numerically extracted here.
The multidimensional Lie-Schwinger source's domain lemma and induction setup
likewise require more than a one-step generic commutator norm. No unseen
source proof or numerical threshold is claimed.
[Yarotsky](https://arxiv.org/pdf/math-ph/0411042),
[unbounded-interaction Lie-Schwinger methods](https://arxiv.org/pdf/2108.13907).

This loop proves the explicit homological/loss estimates and failure of their
stated scalar certificate. It does not prove actual algorithm failure,
homogeneous gap failure, an infinite global unitary, or continuum Yang-Mills.
The model is homogeneous I1/I2/O1, with no q and no canonical-profile transfer.
Weights and their schedule are proof devices. Physical energies multiply
these dimensionless operators by delta=alpha/8; fixed a,E_star>0,
alpha/E_star>0 and hbar remain unchanged. Scientific priority is unverified.

Run `python3 -B research/round22/reverse/o2/check.py --output NEW_DIR` and
`python3 -O -B` into another fresh directory. A compact optimized summary
records all matching output hashes. Finite exact controls accompany the
written all-support proof; they do not formalize the unbounded-domain theorem.
