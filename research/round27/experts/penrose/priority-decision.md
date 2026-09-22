# Prospective decision after the identification audit

Status: conditional proposal for advisor selection, written before a third-loop contract or production experiment. AI1 is selected by the advisor; AI2 and third-loop conclusions are not assumed here.

If AI1/AI2 establish only within-model identification or an explicit obstruction to homogeneous matching, keep **AG** as the highest-priority mathematical branch. A useful third loop can target the first actual homogeneous BCH update and its support-weight loss. Do not replace an unavailable cross-model map with a clock fit.

## Inherited formulas and a candidate stronger norm

The relevant accepted source is `research/round26/reverse/ae2/report.md`, equations AE2.R6–R8, checked against the forward report. Its contract fixes T=3 and M=7|tau|<=1/1000. It obtains finite original weight-2 rooted interaction norms, but no contraction in that norm. The support of an n-th ordered word has at most 4+3n sites, with the complete translated-word count retained.

For prospective testing only, let

\[
\|\Phi\|_\rho=\sup_x\sum_{X\ni x}\rho^{|X|}\|\Phi_X\|,
\qquad \rho>2.
\]

Repeating the **same** reverse majorant with rho in place of 2 suggests the orbital order-n bound

\[
\rho^4 r_*(4+3n)(26M\rho^3|t|)^n.
\]

At rho=9/4 and the accepted endpoint, the prospective geometric ratio is

\[
26M\rho^3T=\frac{28431}{32000}<1.
\]

This is an analytic selection calculation, not an admitted Round27 theorem or production validation. It suggests that the AE2 construction has spare cardinality decay available for a new proof. The stronger norm is an auxiliary estimate; the conclusion must still return to the declared original norm.

## Why spare weight matters

For the ordinary finite-volume interaction commutator, terms are indexed by intersecting supports X,Y and assigned support X union Y. Since nonempty intersection gives 2^|X union Y|<=2^|X|2^|Y|/2, and an operator commutator costs at most twice the norm product, rooted counting gives

\[
\|[\Phi,\Psi]\|_2
\le \|\Phi\|_{2,1}\|\Psi\|_2
 +\|\Phi\|_2\|\Psi\|_{2,1},
\quad
\|\Phi\|_{2,1}=\sup_x\sum_{X\ni x}|X|2^{|X|}\|\Phi_X\|.
\]

All displayed operations require the actual indexed supports and absolutely convergent sums. Finite weight-2 norms alone do not control these first-cardinality moments. For rho>2, the elementary bound

\[
\|\Phi\|_{2,1}\le
\left(\sup_{n\ge1}n(2/\rho)^n\right)\|\Phi\|_\rho
\]

provides the missing moment at a loss of support weight. One commutator is not the full BCH series; repeated commutators require their own complete count or an integral remainder estimate with a proved interaction norm bound.

## Contract needed before execution

Freeze the actual finite-volume sum J of AE2 filtered generators, its anti-self-adjointness and common domain, and C=[J,G]=-A+R with full translated families. Prove, on the inherited domain,

\[
e^JGe^{-J}=G+C+
\int_0^1(1-s)e^{sJ}[J,C]e^{-sJ}\,ds.
\]

Then estimate that exact remainder in the original norm uniformly in the containing finite volumes. Scalar, diagonal and generated-source components must be defined and retained. A finite-volume operator bound using exp(2||J||) may grow with volume and cannot pass a volume-uniform gate by itself.

Required negative controls: missing incoming overlaps; origin's three crossings substituted for the family's twelve; discarded equal-energy residual; unsupported claim that weight-2 finiteness closes commutators; finite-volume norm mislabeled uniform. Success would control one actual update. It would still leave weighted contraction, changed-diagonal induction and continuum matching unproved.

This priority decision is contingent on the preceding loops' review, and authorizes no experiment by itself.
