# AE2 forward: a restricted-coupling filter with the original cardinality norm

Independent second-loop work after AE1 review; no reverse AE2 solution was read. The compact triangular averaging kernel at T=3 proves simultaneous per-source full-operator contraction and finite original rooted weight-2 interaction norms throughout the continuously restricted range M=7|tau|<=1/1000. It does not prove contraction in that interaction norm or close a nonlinear iteration. The original larger cap fails this particular joint certificate.

## Exact kernel, residual and graph domain

Freeze p_T(t)=(1-|t|/T)_+/T. Its integral is one. Its odd integrated primitive is h_T(t)=sgn(t)(1-|t|/T)^2/2 for0<|t|<T, zero outside. Its jump is one and h_T'=delta_0-p_T. Direct integration gives

    integral |h_T|=T/3,  integral |p_T'|=2/T.

For the actual homogeneous initial G define

    R_T(A)=integral p_T(t)alpha_t^G(A)dt,
    L_T(A)=-i integral h_T(t)alpha_t^G(A)dt.

Strong integrals and weak integration by parts give

    [L_T(A),G]=-A+R_T(A),  ||L_T(A)||<=Tr/3.

The actual commutator is bounded, so the self-adjoint adjoint-domain characterization proves L_T(A)D(G) subset D(G), without presupposing domain preservation by A. Its graph bound is Tr/3+2r, and its exponential preserves that domain. The Fourier residual is sinc²(omega T/2); its zero-frequency value is exactly one. The inverse multiplier is[1-sinc²(omega T/2)]/omega, with value zero at omega=0. Thus the residual is retained, not erased by naming this map an inverse.

## Complete translated-source contraction

For each indexed translated source A_b on Z_b, define the actual interior inverse K_b using G_(Z_b)=H0_(Z_b)+D_b. Its norm is at most r_b/(1-M). In the full retained-star volume

    [K_b,G]=-A_b+F_b,
    F_b=sum_(c crossing Z_b)[K_b,D_c].

The possible relative anchors are S-S, S={0,e1,e2,e3}: thirteen in total including zero. Thus an interior source has up to twelve crossing stars, each with seven-site connected union. The positive-octant origin has only three, but that smaller number cannot be used for the family. Complete support and both Q factors remain in every D_c. Consequently ||F_b||<=24M r_b/(1-M).

As in AB2, differentiating alpha_t(K_b) and integrating p_T' gives the exact boundary-retaining identity

    R_T(A_b)=R_T(F_b)+i integral p_T'(t)alpha_t(K_b)dt.

Therefore, uniformly in all translated sources and containing finite volumes,

    ||R_T(A_b)||/r_b <=min(1,[24M+2/T]/(1-M)).     (AE2.1)

At the frozen T=3 and every0<M<=1/1000 the right side is at most2072/2997<7/10. This is a full operator statement on each identity-extended source, including all exterior sectors. It is not just a vacuum-column bound. At the origin one can replace24M by6M; at a no-crossing boundary F_b=0. At tau=0 every actual indexed source and filtered operator is exactly zero, so ratios are omitted. Both nonzero signs are covered without equating their spectra.

## Original rooted weight-2 cardinality decomposition

Here the norm is exactly ||Phi||_2=sup_x sum_(X contains x)2^|X| ||Phi_X||, with declared connected supports, not a diameter substitute. Let r_*=sup_b r_b. Removing unbounded onsite evolution preserves complete-factor supports. At Dyson depth n every surviving ordered word is one source star plus n interactions, including repeated anchors, with connected union at most4+3n sites.

For completeness, repeat the actual rooted positive count from S2. At depth zero at most four source stars contain a fixed root, so N_0<=64r_*. Adding a star costs2M in commutator norm and at most2^3 in support weight. If the root lies in the previous union, at most4(4+3n) stars can meet it; if it lies in the new star, at most four root-containing stars with four possible overlap sites bring in the old rooted sums. These alternatives give

    N_(n+1)<=64M(8+3n)N_n,
    N_n<=64r_*(192M)^n(8/3)_n.                  (AE2.2)

All translated anchors, repetitions and incoming overlaps are counted. The bounded time-ordered simplex gives |t|^n/n!, and its exact filter integrals are

    integral p_T(t)|t|^n/n! dt=2T^n/(n+2)!,
    integral |h_T(t)||t|^n/n! dt=2T^(n+1)/(n+3)!.

Writing c=192M and p=8/3, the actual indexed decompositions consequently obey

    ||R_T(A_family)||_2
      <=128r_* sum_(n>=0)(p)_n(cT)^n/(n+2)!,
    ||L_T(A_family)||_2
      <=128T r_* sum_(n>=0)(p)_n(cT)^n/(n+3)!.
                                                        (AE2.3)

At M<=1/1000,T=3, cT<=72/125<1. The simpler explicit continuous bound for both quantities is

    64(125/53)^3 r_*.

It follows by integrating the uniform orbital bound64r_*(1-cT)^(-8/3), using unit mass for p_T, T/3=1 for |h_T| and8/3<3. Every term keeps its connected support before integration. No unbounded extensive family sum is claimed as a Hilbert-space operator. A single-source infinite-volume limit can be identified by the inherited common-form/strong-resolvent argument and the summable word tail; no equality of all infinite-volume operator domains is asserted.

The displayed weighted upper bound is larger than the starting64r_* upper budget. It proves finiteness, not weighted contraction. Combining it with(AE2.1) cannot silently make a repeated residual iteration converge in ||.||_2. Future steps would have larger supports and new root-count budgets, and a later diagonal would change the source, scalar and reference operator.

## Original-cap feasibility audit

For this complete translated-family boundary estimate, strict full-source contraction requires

    T>2/(1-25M),  M<1/25.

The positive residual cardinality certificate requires cT<1, i.e. T<1/(192M). There is a simultaneous open interval precisely when409M<1. At the original cap M=35/1664, this fails:409M=14315/1664>1. Explicitly the contraction lower duration is3328/789, while the cardinality upper duration is26/105. The intervals are disjoint. Even the origin's smaller crossing count would not repair this cap mismatch.

At cT=1, the distinction between the two filters is relevant: near its endpoint, the residual's positive integral behaves as(T-t)*(T-t)^(-8/3), which diverges, while the inverse has the additional vanishing factor and its corresponding integral is locally integrable. Thus endpoint inverse finiteness alone cannot supply the joint residual certificate. For cT>1 the positive coefficient series fails its radius. These are failed upper certificates, not proofs that the actual filtered operators diverge or that a stronger method is impossible.

## Scope and verification

The restriction |tau|<=1/7000 is a narrower theorem range inside the same physical Hamiltonian family; it is not a changed action or clock. T is a proof duration with physical energy resolution(alpha/8)/T. All fixed positive physical scales remain unchanged. Newton's inverse discipline separates the norms required by the next inference; Tesla's loading discipline enforces twelve family crossings instead of importing the origin's three. Scientific priority is unverified.

The exact checker enumerates both geometries, verifies kernel moments at multiple orders against their analytic formulas, checks every displayed rational threshold and binds the inherited S2 proof. Explicit wrong-count and missing-residual controls remain active under optimized Python. The all-order rooted recurrence, rather than a finite sample, establishes(AE2.3). Accepted scope is restricted initial-G contraction per source plus finite original weighted norms. Weighted contraction, later-diagonal closure, a homogeneous numerical gap and continuum construction remain open.
