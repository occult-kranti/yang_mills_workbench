# O1 reverse: one simultaneous homogeneous rotation

## Verdict

A finite-volume, domain-preserving simultaneous rotation has the declared
decomposition and an explicit volume-independent weighted interaction bound:

\[
 \|R_\Lambda\|_w\le\frac{1970176}{5}\tau^2,
 \qquad |\tau|\le\tau_0:=\frac5{1664}.
 \tag{1}
\]

The all-order scalar majorant below converges on the larger open interval
`|tau|<5/832`. These are series/remainder thresholds, not numerical ground-state
stability thresholds. The numerical homogeneous gap target remains **limited**:
one step does not close an iteration, and the residual cannot be discarded or
automatically treated as purely relative. Current forward/skeptic O1 work was
not read. O2 is not selected here.

## 1. Sufficient premises and exact finite-volume domain

Return to homogeneous I1/I2; there is no q or canonical summable profile.
Let G=`{0,e_x,e_y,e_z}` and retain precisely anchors b with `b+G subset Lambda`
in a finite coarse cuboid. All 21 anchored omitted faces are retained. The
onsite spaces are the actual separable 24-link blocks, with possibly unbounded
nonnegative `h_x>=I-P_x` and unique zero vacua. Let

`H0=sum_(x in Lambda) h_x`, `Phi=sum_b phi_b`, `A=sum_b A_b`, `X=sum_b S_b`.

Inherited I2 supplies the local definitions, `v_b=phi_b Omega_G`,
`u_b=(H0_G|Q_G)^(-1)v_b`, `H0_G u_b=v_b`, and

\[
 \|\phi_b\|\le v:=7|\tau|,\quad
 \|S_b\|\le s:=\sqrt{7/12}|\tau|,\quad
 \|A_b\|\le a:=\sqrt{7/12}|\tau|,
\]
\[
 S_b=|u_b\rangle\langle\Omega_G|-|\Omega_G\rangle\langle u_b|,
 \quad A_b=|v_b\rangle\langle\Omega_G|+|\Omega_G\rangle\langle v_b|,
 \quad\phi_b=A_b+Q_G\phi_bQ_G.
\]

On the local domain, `H0_G S_b=|v_b><Omega_G|` and
`S_b H0_G=-|Omega_G><v_b|` have bounded extensions. Tensoring with the identity
outside the star does not map every vector into the full operator domain;
instead it preserves that domain. Indeed `S_b` preserves `D(H0_G)`, commutes
with exterior spectral projections, and preserves `D(H0_ext)`. Nonnegativity
and the joint spectral calculus give
`D(H0)=D(H0_G) intersect D(H0_ext)`. Therefore

\[
 [S_b,H0]=-A_b,\qquad [X,H0]=-A
 \quad\hbox{on }D(H0).
 \tag{2}
\]

X is bounded skew-adjoint in each finite volume. Equation (2) gives
`||H0 X psi||<=||X||||H0 psi||+||A||||psi||`, so X is also bounded on the
Banach space D(H0) equipped with its graph norm. Its exponential power series
converges there. Thus `U=e^X` and its inverse preserve D(H0) exactly.
All conjugated Hamiltonians are self-adjoint on this same domain. No
volume-independent bound on `||X||` or an infinite global U is asserted.

Differentiate on this graph domain first, then integrate the bounded
commutator (2):

\[
 e^X H0e^{-X}=H0-\int_0^1e^{rX}Ae^{-rX}\,dr.
\]

The integrand is a norm-continuous bounded operator. Expanding only its
bounded conjugation, and separately that of Phi, proves

\[
 U(H0+\Phi)U^*=H0+D+R,\qquad D=\sum_b Q_{b+G}\phi_bQ_{b+G},
\]
\[
 R=\sum_{n\ge1}\left\{\frac{\operatorname{ad}_X^n\Phi}{n!}
             -\frac{\operatorname{ad}_X^n A}{(n+1)!}\right\}.
 \tag{3}
\]

These are ordinary norm-convergent bounded series in each fixed finite volume.
Unbounded H0 was never placed in an operator-norm power series.

## 2. Count every ordered generated support

For K_b equal to phi_b or A_b, expand `ad_X^n K_b` over ordered anchors
`(b_1,...,b_n)`, with b_1 the innermost commutator. A nonzero term requires
each new star to meet the union of preceding stars. Disjoint factors commute.
This condition is necessary, not sufficient, so retaining all such words
overcounts safely, including repeated anchors and cancellations.

The number of star translates intersecting one fixed star is

`|G-G|=1+6+6=13`.

With j stars already inserted (including the base), the next anchor has at
most 13j choices. Holding the base at zero, there are therefore at most
`13^n n!` candidate ordered words. Every new intersecting star adds at most
three sites, so its declared support Y satisfies `|Y|<=4+3n`.

For the required per-site norm one must also sum over base anchors. For a
fixed relative word, exactly |Y| translations in the full integer lattice
put a specified site x in Y. Restriction to retained octant/cuboid anchors
can only remove translations. This is a combinatorial bound, not a transfer
of the physical boundary or Hilbert representation. Combining this factor,
the support weight, and the nested commutator norm yields

\[
 \sup_x\sum_{\substack{\text{ordered words}\\Y\ni x}}
  2^{|Y|}\|\operatorname{ad}_{S_{b_n}}\cdots
                 \operatorname{ad}_{S_{b_1}}K_b\|
 \le16(4+3n)(208s)^n n!\,\|K_b\|_{\rm sup}.
 \tag{4}
\]

Here `208=8*13*2`: support-weight growth, anchor choices and the norm
commutator factor are all present. The root multiplicity `(4+3n)` must not
be omitted. Keeping indexed words as the interaction decomposition is
permitted by the contract; combining words with the same support can only
reduce the triangle bound. All orders are counted by this argument; finite
enumeration is a check, not its proof.

## 3. Sum the majorant and evaluate an interval

Put `z=208s`. Equations (3)-(4) give, for z<1,

\[
 \|R\|_w\le16\sum_{n\ge1}(4+3n)z^n
                       \left(v+\frac a{n+1}\right)
 \le16(v+a/2)\frac{z(7-4z)}{(1-z)^2}.
 \tag{5}
\]

The positive scalar series identity is
`sum_(n>=1)(4+3n)z^n=z(7-4z)/(1-z)^2`. Weighted absolute convergence proves
that the declared interaction decomposition of R exists with this norm
uniformly in every finite cuboid. It also defines a summable local interaction
bound in the homogeneous geometry; it does not make R a globally bounded
operator in the canonical incomplete tensor product.

Using `sqrt(7/12)<4/5` gives `z<=(832/5)|tau|`. If
`|tau|<=5/1664`, then z<=1/2 and
`(7-4z)/(1-z)^2<=20`. Therefore

`16*(37/5)*20*(832/5)=1970176/5`,

which proves (1), including tau=0 and either sign of tau. The chosen interval
is approximately 0.0030048 in dimensionless homogeneous coupling; the exact
rational endpoints and constant are the certificate. No optimality is claimed.

As a first-step size comparison, `||Phi||_w<=448|tau|`, while for
`|tau|<=1/2000`, (1) is less than half that *budget*. This is an inequality
between upper budgets, not a comparison to the actual Phi norm or a repeated
contraction theorem. The unchanged diagonal part still has first order size.

## 4. Retained diagonal part and the failed gap inference

Commuting onsite projections imply
`Q_(b+G)<=sum_(x in b+G)(I-P_x)`. Each site occurs in at most four retained
stars. Hence on the form domain,

\[
 |\langle\psi,D\psi\rangle|
 \le7|\tau|\sum_b\langle\psi,Q_{b+G}\psi\rangle
 \le28|\tau|\langle\psi,H0\psi\rangle.
 \tag{6}
\]

The overlap four occurs at interior sites; using one would be incorrect.
The *truncated* H0+D has the original vacuum and gap at least `1-28|tau|`
when this number is positive. Equation (3) retains R. In general it contains
both a vacuum-energy correction and vacuum-offdiagonal terms.

An explicit two-overlapping-star seven-qubit control below has, at tau=0,

\[
 R(\tau)\Omega=\tau^2[-(3/8)\Omega-(1/16)|11 00000\rangle]+O(\tau^3).
 \tag{7}
\]

At tau=1/100 the exact tail bound in the checker is smaller than each displayed
nonzero coefficient. Thus its vacuum expectation is strictly negative and
its excited component is nonzero. The general premise `R Omega=0` is false.
The purely relative form estimate `|<psi,R psi>|<=c<psi,H0 psi>` already
fails at Omega. Subtracting the vacuum expectation cannot fix the offdiagonal
term: test `Omega+r xi` and let r tend to zero. This is a lemma control, not
an SU(2) spectrum calculation or proof of a specific SU(2) matrix element.

Using the global bounded perturbation inequality instead only gives a
volume-dependent lower certificate such as
`1-28|tau|-2|Lambda| C_R tau^2`. A fixed local interaction norm is not that
global operator norm. For example `R=-r sum_x P_x` has weighted norm 2r but
global norm `|Lambda|r`. This rejects substituting a local norm into a global
spectral perturbation inequality. It does not disprove a valid local stability
theorem or actual positive gaps in either model.

The exact missing closure premise is a quantitative scheme that removes
vacuum scalar/offdiagonal parts on the generated connected supports, maintains
their local inverse gaps and unbounded-domain conditions, and controls support
weights over every iteration. Reapplying the four-site word count unchanged
is invalid once arbitrary supports have been generated. A justified candidate
is a support-indexed block diagonalization with explicit loss-of-weight and
gap recurrences, or numerical reconstruction of a fully matched source
fixed-point estimate. No such recurrence is proved by this one-step lemma.

## 5. Discriminating controls and primary comparison

The checker enumerates relative connected ordered words through order three,
including a chain where the outer generator misses the base but meets the
already generated support. It independently reconstructs finite-cuboid site
overlap. Exact seven-qubit operators on stars
`G` and `e_x+G` test `[S_b,H0]=-A_b`, the cross-star commutator, support on all
seven sites, and the retained second-order remainder. Their local excitation
energies are 1 and 2; the other qubits have unit gap. Local phi amplitudes are
tau/2; local S amplitudes are tau/2 and tau/4. Thus their norms satisfy the
upper assumptions, while no claim of matching the SU(2) Haar variance is made.
An analytic exponential tail bound certifies (7) at a stated rational tau.
These controls reject dropping cross terms, freezing support at four sites,
reversing the cancellation, deleting R, and pure-relative/global-norm errors.

Yarotsky's definitions and Theorem 1 match unbounded gapped onsite operators,
bounded finite-range perturbations and the whole-support empty boundary.
Section 2, Lemma 1, and equations (8), (14)-(15) rely on a fixed-point estimate
and unspecified range-dependent constants; no numeric c1 or c2 was extracted.
The source itself declares changing c/epsilon conventions. Its existing
qualitative stability theorem is preserved, not replaced by (1).
[Yarotsky primary text](https://arxiv.org/pdf/math-ph/0411042).

The multidimensional unbounded-interaction Lie-Schwinger paper was checked at
Lemma 2.8 and its proof, Theorem 2.10, and the Theorem 3.1 statement/induction
setup. It explicitly treats domains and uses stronger evolving weighted
estimates; the complete induction and numerical threshold were not
reconstructed. Our bounded finite-rank generators allow the direct stronger
operator-domain proof above. No source threshold is transferred.
[Primary text](https://arxiv.org/pdf/2108.13907).

The local construction and Lie method are established tools; the explicit
word majorant and numerical one-step constants are scoped project derivations.
Scientific priority is unverified. Multiply H0, D and R by delta=alpha/8 to
restore energies; tau is a homogeneous action deformation, weight 2 a fixed
proof device. Keep spacing, E_star>0, alpha/E_star>0 and hbar fixed. No
infinite unitary, dynamics consequence, canonical-profile gap, homogeneous
representation equivalence, fitted physical clock or continuum mass gap is
proved. O2 belongs to the advisor after O1 review.

Reproduce with `python3 -B research/round22/reverse/o1/check.py --output NEW_DIR`
and `python3 -O -B` into another fresh directory. Ordinary scientific outputs
are retained; the optimized replay summary binds all identical output hashes.
The arithmetic checks complement the proof and do not formalize it.
