# Q1 independent preparation and acceptance challenges

Prepared from the frozen Q1 contract, methods/v4 and admitted C1/P2 evidence
without reading either current producer. These comparators are frozen before
review, not an admission or selection of Q2. The model adds the explicitly
dimensionless magnetic lambda>=0 to the actual fixed finite graph.

## Exact face moments: independent comparator

The checker rebuilds all 20 original signed faces and deletes only the
genuine tree edges 0 through 15 and 26 when writing their traces in chord
coordinates. All 16 chord variables remain in the full map. Face 8 alone is
fully selected: W8=t=Tr(VW^-1)/2. Every other face has an omitted chord
appearing once and hence zero conditional mean.

For two distinct faces, an omitted chord appearing exactly once across both
words kills their Haar product. Exhaustive support enumeration gives 187
vanishing pairs and just three survivors, all sharing chord G=L25:

| Faces | Functions involving G | Conditional product |
|---|---|---|
| 9,14 | Tr(UG^-1)/2, Tr(GW^-1)/2 | r/4, r=Tr(UW^-1)/2 |
| 9,15 | Tr(UG^-1)/2, Tr(G^-1)/2 | x/4 |
| 14,15 | Tr(GW^-1)/2, Tr(G^-1)/2 | z/4 |

In unit-quaternion coordinates these are u.G, w.G and e0.G, with
E[G_a G_b]=delta_ab/4. Each of the 19 random faces has conditional second
moment 1/4. Thus, for the complete V=sum_p(1-Wp),

    E[V|U,V,W] = mu = 20-t,
    E[V^2|U,V,W] = (20-t)^2 + k,
    k = 19/4 + (r+x+z)/2 = 4 + |u+w+e0|^2/4.

The factor two for distinct cross terms is essential. The function k is
neither a constant nor its Haar mean. It has exact range [4,25/4]: the lower
endpoint is realized by u+w+e0=0 and the upper by u=w=e0; continuity gives
the same essential endpoints. Its Haar mean is 19/4. Distinct original
physical faces are unconditionally orthogonal by a singly occurring full
link, so E[V]=20 and Var(V)=5, consistently with Var(mu)=1/4.

Consequently

    J* V(1-P)V J = M_k,
    2||f|| <= ||(1-P)VJ f|| <= (5/2)||f||,
    ||(1-P)VJ||=5/2.

This is a multiplication-operator statement on the invariant selected L2
space, not only a scalar reference-vector calculation. Conditional face
independence, terminal-inverse omission and evaluation of omitted chords at
identity all give explicitly wrong controls. The checker verifies all 190
distinct face pairs and a noncommuting rational quaternion fixture; the
universal moment proof is the displayed Haar-linear argument.

## Operators, leakage and scalar/state distinctions

V is a real smooth bounded invariant multiplication operator with 0<=V<=40.
Hence H_lambda=H_E+alpha lambda V is self-adjoint on D(H_E), has the same
graph core and is nonnegative. Its closed form has the inherited H1 domain.
The full J16 unitary still transports this operator exactly; that statement
does not establish a selected reducing image.

The actual selected compression is

    A_lambda = H_eff + alpha lambda M_(20-t)

on the inherited invariant H2 domain, with H1 form domain. It is
nonnegative. Its off-diagonal block is B=alpha lambda(1-P)VJ and
B*B=alpha^2 lambda^2 M_k. For lambda>0 the selected image cannot reduce
H_lambda; indeed every nonzero selected vector has nonzero leakage.
Lambda=0 must recover the exact P2 electric reduction.

The normalized Haar vector is a reference only. H_lambda 1=alpha lambda V
is nonconstant for lambda>0; its energy variance is 5 alpha^2 lambda^2.
It is not an interacting eigenvector or ground. Neither compressed-reference
matrix elements nor their derivatives can be relabeled stationary interacting
correlations. A common scalar shift multiplies both semigroups by the same
factor and leaves B, k and the leading discrepancy unchanged. A scalar added
only to the proposed compression changes the first derivative and cannot
repair the second-order defect while preserving that derivative.

## Dynamic topology: what is possible and what is not

For a selected smooth invariant f, direct second derivatives give

    [J* exp(-tH_lambda/hbar)J - exp(-tA_lambda/hbar)] f
      = alpha^2 lambda^2 t^2 M_k f/(2 hbar^2) + o_f(t^2)

strongly. The polynomial core lies in the needed squared-operator domains;
these individual semigroup derivatives must not be asserted for arbitrary
L2 vectors. On f=1 the scalar quadratic coefficient is
19 alpha^2 lambda^2/(8 hbar^2), strictly positive for lambda>0.

There is also a compatible operator-norm upper bound. Let D be the diagonal
Q=1-P compression of H_lambda, defined on QD(H_E); it is nonnegative and
self-adjoint because H_E reduces Q and QVQ is bounded. Set
X(t)=J*exp(-tH_lambda/hbar)J. The block equations, or bounded off-diagonal
Duhamel, yield the strong double integral

    X(t)-exp(-tA/hbar)
      = hbar^-2 int_0^t ds int_0^s du
        exp(-(t-s)A/hbar) B* exp(-(s-u)D/hbar) B X(u).

Every semigroup/compression is contractive, so

    ||X(t)-exp(-tA/hbar)|| <= (25/8)(alpha lambda t/hbar)^2, t>=0.

The integral is justified vectorwise by bounded perturbation and strong
continuity. A norm estimate does not turn it into a norm-Bochner integral.
Rescaling the triangle and dominated strong convergence, or density plus
the uniform quotient bound, extends the difference quotient's strong limit
to all selected vectors. This does not give individual second derivatives
there.

**A second-order operator-norm Taylor limit is actually impossible at
lambda>0.** The finite-product electric Casimir has compact resolvent;
bounded magnetic perturbation preserves it by the resolvent identity.
The selected operator has compact resolvent by P2's comparison and its
bounded added potential. Thus both heat operators, and their compressed
difference divided by t^2, are compact for each t>0. But M_k>=4I on the
infinite-dimensional invariant H3 space is not compact. A norm limit of
compact operators cannot equal alpha^2 lambda^2 M_k/(2 hbar^2).

More explicitly, take normalized mutually orthogonal SU2 characters of U
as a weakly null invariant sequence. Any fixed compact operator sends them
to zero, while ||M_k f_n||>=4. Therefore the norm distance of the quotient
from its proposed limiting coefficient is at least
2 alpha^2 lambda^2/hbar^2 for every t>0. This distinguishes a valid O(t^2)
norm bound from an invalid norm Taylor conclusion. It does not assert that
the discrepancy is a positive operator at every finite time; that stronger
order claim would require its own proof.

## Primary-source map and review boundary

Reuse Burbano and Bauer, arXiv:2409.13812v2 (28 September 2024), the P2-read
Haar/Peter-Weyl passages and magnetic path translation in Appendix C.4.1,
Eqs.276-278. Its hypotheses are matched through the genuine tree and actual
signed graph. The conditional cross moments above are independently derived.

Targeted additional reading: Gerald Teschl,
[Mathematical Methods in Quantum Mechanics, second edition](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe2.pdf),
AMS 2014, author-hosted 370-page PDF: Theorem 6.4 and Lemma 6.5, printed
p.159 (PDF index170), for the common domain under bounded symmetric
perturbation and the resolvent identity; Section 6.2, printed pp.160-162
(PDF indices171-173), for compact-operator norm closure and weak-sequence
behavior. Bounded V has relative bound zero. Compactness here follows from
the actual finite electric spectrum, not an imported infinite-volume claim.
Reading was targeted, not a whole-book audit. The block Duhamel and
topology-specific discrepancy are independent arguments.

Accept only the proved topology and stated model. Reject clipped faces,
missing conditional cross terms, replacement of M_k by its expectation,
scalar repair, presumed interacting Haar ground, and any unsupported norm
Taylor or all-time operator-order claim. Scientific priority remains
unverified. No Q2 target is selected; await both frozen Q1 submissions and
the advisor's explicit review opening.
