# O1 independent preparation — frozen before producer inspection

This is a prospective acceptance checklist and independent derivation, not an
admission. Only the frozen O1 contract, inherited I1/I2 evidence and admitted N2
material have been used. No current O1 producer has been inspected. All quantities
below are dimensionless homogeneous quantities; there is no profile parameter q.

## Domain and exact identity

Write Phi=sum_b phi_b and A=sum_b A_b over complete retained stars. The local
rank-two generator satisfies S_b D(H0_Lambda) subset D(H0_Lambda), and
[H0_Lambda,S_b]=A_b there. A necessary distinction: after tensoring by identity,
S_b need not send the entire global Hilbert space into D(H0_Lambda), because
it does not regularize spectator blocks. A proof claiming that stronger property
would be defective.

On a finite tensor core, the local inverse gives u_b in D(H0_S), and the
commutator identity follows. Nonnegative commuting site Hamiltonians identify
the local sum domain with the intersection of site domains. Core approximation
and closedness extend the identity to the full operator domain. Thus finite X
is bounded in the H0 graph norm as well as in Hilbert norm; its exponential and
inverse preserve the domain. Volume growth of these graph-norm constants is
allowed here, but must not become the local interaction estimate.

For U=exp X, first integrate the bounded commutator:

    U H0 U* = H0 - integral_0^1 exp(tX) A exp(-tX) dt.

Only then use norm series for bounded Phi and A. The exact remainder is

    R = sum_{n>=1} (ad_X^n(Phi)/n! - ad_X^n(A)/(n+1)!).

The sign and the unequal factorials matter. The term of order zero is
Phi-A=sum_b Q_S phi_b Q_S. An unqualified norm BCH expansion of unbounded H0
does not establish the identity on its domain.

## All orders, overlap, and an independently available majorant

For S={0,e_x,e_y,e_z}, |S-S|=13 and each site belongs to at most four translates
of S. A nonzero ordered nested word with base star b0 and n generators must
have each new star overlap the union of previous stars. Its union Y is connected
and has |Y|<=4+3n. For fixed b0, the j-th new star has at most 13j choices,
so the number of words is at most 13^n n!. Repeated anchors are included.

The weighted norm is rooted at a site, not at b0. For each relative word there
are at most |Y| translations for which a fixed site belongs to Y. Counting all
translations in Z^3 bounds the retained positive-octant cuboid words from above.
This supplies the often-missing factor 4+3n. Bounds for connected unordered
clusters alone do not count the ordered words.

Let s=sqrt(7/12)|tau|, M=7|tau| and r=208s. Since ||S_b||<=s and ||A_b||=s,
the indexed-word decomposition gives, for r<1,

    ||R||_w <= 16 sum_{n>=1} (4+3n) r^n [M+s/(n+1)].

Here 16 is the initial weight, 8^n is support growth, 2^n is the nested
commutator bound, and 13^n is the overlap count. The factorial from counting
cancels the exponential factorial. This covers every finite volume and includes
all cross-star terms; grouping identical supports can only improve the bound.

An explicit conservative choice is |tau|<=1/1024. Using s<=(4/5)|tau| gives
r<=13/80, and summing the geometric series gives

    ||R||_w <= C tau^2,
    C = 16*(37/5)*(832/5)*[4/(1-13/80)+3/(1-13/80)^2]
      = 4003397632/22445 < 178365.

The rational constant and overlap counts were independently computed with
Python Fraction arithmetic and direct set enumeration. This is a comparator,
not a demand that producers obtain these constants. A sharper or different
valid indexed decomposition is acceptable. Conversely, a naive assertion that
the fixed weighted norm is a bounded Lie algebra norm for arbitrary growing
supports needs proof: commutator overlap introduces support-size factors.

For each finite volume, the bounded-operator exponential series already
converges. The small interval above specifically gives a volume-uniform bound
in the declared interaction norm, not a threshold for a spectral gap.

## Relative part and the missing gap inference

The retained diagonal D satisfies D Omega=0 and

    |<psi,D psi>| <= 7|tau| sum_b <psi,Q_(b+S) psi>
                   <= 28|tau| <psi,H0 psi>.

The factor four counts all stars incident on a site. Consequently H0+D alone
has the reference vacuum and a gap at least 1-28|tau| when this is positive.
This says nothing sufficient by itself about H0+D+R: a local interaction norm
is not a volume-independent global operator norm, nor a pure relative bound.

The actual one-retained-star cuboid already tests deletion of R. Write
phi=tau phi_1, v=tau v_1 and u=tau u_1. The analytic order-two coefficient is

    <Omega,R Omega> = -tau^2 <v_1,(H0_S|Q)^-1 v_1> + O(tau^3),

which is strictly negative to leading order since ||v_1||^2=7/12. Thus the
uncentered R is not identically vacuum-annihilating or pure relative. This
does not prove that a scalar-centered actual-model R has residual mixing;
that stronger claim needs its own witness.

A two-level lemma fixture can separately reject any universal inference that
scalar centering removes mixing: take H0=diag(0,1), phi=tau[[0,1],[1,c]] and
the inherited rank-two generator. The transformed off-diagonal remainder is
tau cos(2tau)-(1+c tau) sin(tau)cos(tau), generally nonzero. Scalar shifts
cannot remove it, and testing Omega+z e1 gives a linear form contribution
against a quadratic H0 form. This fixture is not an SU(2) simulation.

To accept a numerical gap, require a proved volume-independent method that
controls this residual vacuum mixing, scalar energy, diagonal relative terms,
growing supports and repeated inverses/domains. Neither C tau^2 being small
nor a theorem saying 'sufficiently small' supplies that method's evaluated
constants. A valid one-step bound with this precise remaining premise is an
acceptable limited O1 outcome. No O2 selection is made here.

## Discriminating acceptance and rejection checks

- Verify the actual frozen contract and inherited I1/I2 bindings. Retain all
  21 omitted faces at each admissible anchor and the full four-block star.
- Require the domain argument, exact first commutator, all-order coefficients,
  support unions, ordered multiplicity and site-root conversion above or valid
  replacements. Empty anchor sets and boundary removal must behave correctly.
- Compute the submitted scalar interval/constant directly; convergence must
  hold throughout the claimed closed interval and uniformly in cuboid size.
- Demand a nonzero cross-star or enlarged-support control. Two overlapping
  stars can be tested with local rank-two and Pauli fixtures; zero commutators
  for disjoint stars alone do not test omitted overlap terms.
- Reject summing isolated I2 remainders as the simultaneous remainder, deleting
  R, replacing an interaction norm by a global norm, or transferring the
  diagonal-only gap to the full transformed operator without a new premise.
- Separate actual-model statements, abstract fixtures, analytic proofs and
  finite enumerations. Ordinary/optimized producer replay is evidential
  verification, not formalization of unbounded-domain arguments.
- No homogeneous infinite-volume U, canonical-profile transfer, clock change,
  continuum conclusion, or numerical source constant may be inferred here.

## Primary proof checks and limits

Yarotsky's [v1 paper](https://arxiv.org/pdf/math-ph/0411042) permits the present
separable, unbounded on-site reference and bounded finite-range interaction;
its empty-boundary convention matches complete retained stars. Definitions and
Theorems 1–3 (PDF pp.2–4), Lemma 1 and the contraction/resolvent outline
(PDF pp.6–9, equations 8–15) were read. The contraction is in a ground-state
excitation collection norm, not the O1 interaction norm. Constants c1, c2 and
the contraction constant remain unevaluated; this supplies no numerical gap
threshold here.

Del Vecchio–Fröhlich–Pizzo's [v1 paper](https://arxiv.org/pdf/2108.13907)
was checked at its setup, Lemma 2.8 and its proof, Theorem 2.10, conditional
gap argument 2.51–2.53, and Theorem 3.3 with its closing proof (PDF
pp.3–5, 11–12 and 36). Their form-domain lemma depends on later inductive
estimates; it does not automatically establish O1's common operator domain.
Their iterative rectangle norm and smallness parameter require an explicit
dictionary to our star interaction. Theorem 3.1's complete induction was not
replayed. No numerical t_d, contraction or gap is imported from this source.
