# O2 independent preparation — current producers unread

This freezes a skeptical comparator, not an O2 admission. Contract
86895d53f2e0944ab4c0a93eb969018dd213d9a2a5c27d1107d10e10338e15a6
and the admitted O1 statement are the scientific inputs. The v2 instruction
snapshots have been read. Quantities remain dimensionless homogeneous ones;
support weights are proof parameters, and no canonical q is present.

## Splitting and domains

For each bounded self-adjoint residual term, with r_Y=||R_Y||, the declared
splitting is exactly R_Y=c_Y I+A_Y+Z_Y, with bounds
|c_Y|<=r_Y, ||A_Y||<=r_Y and ||Z_Y||<=2r_Y. Scalar subtraction must occur
inside the Q block as specified. Merely removing c_Y leaves A_Y.

Set v_Y=Q_Y R_Y Omega_Y, u_Y=(H0_Y|Q_Y)^(-1)v_Y and
S_Y=|u_Y><Omega_Y|-|Omega_Y><u_Y|. The bare reference inverse has norm at
most one for every nonempty finite Y, without a new interacting-gap premise.
Then ||S_Y||<=r_Y, u_Y is in D(H0_Y), and [S_Y,H0]=-A_Y on D(H0).
The O1 graph-domain proof extends to this support. The operator maps preserve
the full domain; they do not regularize arbitrary exterior vectors.

A finite physical volume can still have infinitely many indexed words.
Either group their absolutely convergent sums by its finitely many supports,
or prove summability in the graph norm using the bounds for S_Y and A_Y.
Do not confuse finite volume with a finite word expansion. Arbitrary bounded
D need not preserve D(H0); that is unnecessary for the bounded commutators
with D after the first H0 commutator has been integrated.

If r=||R||_mu, the weighted bounds for A,S,Z are r,r,2r. The new diagonal
budget can obey d'=d+2r and the relative coefficient can obey
kappa'=kappa+2 exp(-mu)r <= kappa+2r, since every support is nonempty.
The extracted scalar energy changes by at most |Lambda|r in absolute value.
It must be retained even though it cancels from further commutators.

## Generated-support bracket and a same-weight challenge

For mu'>=0 and loss delta=mu-mu'>0, splitting the root between the two
overlapping supports gives the valid comparator

    ||[S,B]||_(mu') <= 4/(e delta) ||S||_mu ||B||_mu.

Each side of the root split contains a factor |Y| from the intersection
sum. The estimate |Y| exp(-delta |Y|)<=1/(e delta) absorbs it. All indexed
occurrences must be summed; declared union supports and their multiplicity
cannot be reset to initial stars.

A universal equal-weight bound without size dependence is false. Let Y be
a connected union of m consecutive O1 stars, with N=3m+1 sites, each a qubit.
Use S_Y=exp(-mu N)(|1...1><0...0|-|0...0><1...1|), and singleton diagonal
terms D_x=exp(-mu)|1><1|_x for x in Y. Both interaction norms equal one.
Their grouped commutator has weighted norm N exp(-mu), which is unbounded
with N. D is vacuum-annihilating, and S is rank two. This rejects a universal
bracket inequality even for those structures.

However, on this fixture the bare-reference inverse acting on the all-excited
vector contributes a factor 1/N. Therefore the universal bracket failure
alone does NOT rule out a sharper bound on the *specific homological map*.
Likewise it does not disprove every same-weight algorithm. This distinction
is a required challenge to any claimed obstruction.

## One complete step and the retained-D comparator

With E separated, the exact rotated remainder is

    R' = sum_(k>=1) [ad_X^k(D+R)/k! - ad_X^k(A)/(k+1)!],
    D' = D+Z,  E' = E+sum_Y c_Y.

In particular [X,D] remains. Removing it would falsely turn the leading
remainder estimate from linear-in-r times d into a purely quadratic one.

Divide the total weight loss delta equally among k nested commutators.
The bracket comparator and k!>=(k/e)^k give

    ||ad_X^k B||_(mu-delta)/k! <= (4r/delta)^k ||B||_mu.

Consequently, for xi=4r/delta<1, a complete sufficient majorant is

    r' <= (d+3r/2) xi/(1-xi),   d' <= d+2r.

Different sharper valid estimates are acceptable. The inequality above is a
reference comparator, not a demand that either producer match these constants.

For the frozen schedule,
delta_n=log(2)/(2(n+1)(n+2)), with positive limiting mu=log(2)/2.
Define positive upper budgets by equality in this recurrence, starting from
r0=(25460736/25)tau^2 and d0=448|tau|. As long as it is defined,

    r_(n+1) >= (4d0/delta_n) r_n.

For tau!=0 the factor eventually exceeds two. If the series condition held
forever, the positive budget would then grow geometrically, contradicting
r_n<delta_n/4 and delta_n tending to zero. Thus this stated budget cannot
certify all steps for any nonzero tau. The same argument applies to this
same recurrence under every decreasing positive-limit weight schedule with
strictly positive losses. It is failure of this majorant, not a lower bound
on the actual residual, algorithm failure or homogeneous gap failure.

An exact-arithmetic example uses tau=2^(-22), the rigorous lower enclosure
log(2)>69/100 and upward rounding to a 10^(-100) grid after each residual
update. It starts at r0=777/13421772800 and d0=7/65536, shrinks dramatically,
then first violates xi<1 at step 75. The retained script and compact output
specify this conservative recurrence exactly. This step index belongs to
that enclosure/rounding choice; it is not asserted for every sharper bound.

## Acceptance and rejection conditions

- Require exact scalar/A/Z splitting, support-independent bare inverse bounds,
  bounded first commutators, and the common unbounded domain at each step.
- Check the full bracket sum, support-size factor, all-order factorials and
  positive weight remaining after the entire schedule, not a finite prefix.
- Require scalar energy bookkeeping and relative diagonal updates along with
  residual budgets. The initial diagonal terms are order |tau| and remain.
- A finite prefix of shrinking residuals does not certify the infinite
  recurrence. Locate the failed inequality or prove summability and every
  inverse-gap condition. Fixed-volume limit-domain preservation also requires
  an argument; it does not follow merely from preservation at each step.
- If a successful alternative is proposed, declare its changed inverse,
  diagonal reference and norms explicitly, and prove its new assumptions.
  A source's interacting inverse cannot silently replace the frozen bare one.
- Keep actual-model claims separate from qubit controls and worst-case
  interaction estimates. Failed upper budgets prove no physical gap failure.
  No infinite global unitary, representation transfer or continuum conclusion
  follows from local interaction norms alone.
- Fresh ordinary/optimized producer replay, strict source closure and useful
  rejecting controls are required. No current producer has been inspected.

## Targeted primary check

The O1 primary map is reused at its recorded depth. I rechecked Yarotsky's
[Lemma 1 and equations 8, 14–15](https://arxiv.org/pdf/math-ph/0411042)
(v1, PDF pp.7–9): its contraction uses excitation collections and a different
relative norm, with constants still unspecified. It does not validate the
bare-reference recurrence above.

I additionally read the inverse construction and estimate in
[Del Vecchio–Froehlich–Pizzo](https://arxiv.org/pdf/2108.13907)
(v1, Lemma 4.1, equations 4.241–4.252, PDF pp.37–38), and checked the
stated prerequisites of Appendix A, Lemma A.3, equations A.8–A.10 (PDF p.50).
That inverse uses an interacting local G-E, a prior gap and a prior relative
energy comparison. It is not the bare H0 inverse. The complete support
induction and Appendix A prerequisite proofs have not been reconstructed;
no numerical threshold is imported.
