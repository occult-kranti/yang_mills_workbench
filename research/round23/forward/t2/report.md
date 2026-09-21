# T2: separately ground-centered magnetic heat evolution

**Result.** On the actual T1 finite physical graph, with its entire infinite-dimensional physical and selected spaces, fixed positive a, E_star, alpha/E_star and hbar, and constant 0 <= lambda <= 1/100,

    sup_(t>=0) ||J* exp[-t(H_lambda-e_lambda)/hbar] J
                 - J* exp[-t(Htilde_lambda-etilde_lambda)/hbar] J||
       <= 60 lambda^2.                                      (1)

Both ground eigenvalues are simple and isolated. In physical units both excitation gaps are at least 103 alpha/40. Further,

    0 <= e_lambda-etilde_lambda <= (6250/169) alpha lambda^3,
    ||G_lambda-Gtilde_lambda|| <= (20000/1339) lambda^2.       (2)

These are conservative analytic bounds, not estimates of the actual optimal constants. They apply at all heat times, including infinity through the ground projections. They do not prove a relative operator ratio, a finite numerical implementation, real-time accuracy, a homogeneous gap, physical calibration or a continuum theory.

**Authorship:** one agent derived, implemented and critically reviewed this loop under the explicit user amendment in `methods/t2-solo-override.md`. The reverse report is a correlated obligation audit. No independent-agent review is claimed. Scientific priority is unverified.

## 1. Fixed model and a comparison path

Use the inherited 18-vertex, 33-edge, 20-face physical SU(2) graph, all vertex Gauss constraints, the P2 isometry J, P=JJ*, Q=I-P and the T1 blocks. Divide energies by alpha and set sigma=alpha t/hbar. Let

    L_s = Htilde/alpha + s lambda D,       0<=s<=1,
    D = Q Vmag Q,                         0<=D<=40 Q,
    L_s = [[A/alpha, B*/alpha], [B/alpha, C0/alpha+s lambda D]].

The symbol D here is the bounded complementary magnetic block, not the retained diagonal in the distinct homogeneous model. The path s is a proof interpolation, not an added physical field or a time-dependent coupling. All operators have the common domain D(H_E), and B is bounded with norm b=5lambda/2 in these dimensionless units. P reduces H_E, and C0/alpha>=3 on Q. No spin cutoff, two-channel autonomous approximation or change of clock is introduced.

The inherited graph Laplacian has compact resolvent: the product SU(2) manifold is compact and elliptic, its gauge-invariant subspace reduces the Laplacian, and restriction of the resolvent to that closed reducing subspace remains compact. The inherited selected/complementary decomposition also reduces H_E. Each L_s is a bounded self-adjoint perturbation on the same domain; its resolvent remains compact by the resolvent identity. Its form domain is unchanged. This justifies discrete eigenvalues with multiplicity on the actual restricted realization.

## 2. Ground construction, isolation and separation

The electric ground Omega is unique and lies in P; the next physical electric energy is at least 3. The diagonal magnetic blocks in L_s-H_E/alpha are nonnegative. The offdiagonal block has norm b, hence

    L_s >= H_E/alpha - b I.

The variational principle gives the second eigenvalue E_1(s)>=3-b. The ground Rayleigh quotient on Omega is <=40lambda (a deliberately loose bound from ||Vmag||<=40). Therefore

    epsilon_s = inf spec L_s <=40lambda,
    E_1(s)-epsilon_s >= g(lambda)=3-(85/2)lambda >=103/40.

The strict separation proves a simple isolated ground, rather than presupposing one. T1's positive lower form applies throughout this path because L_s>=L_0: epsilon_s>=18lambda. At lambda=0 the whole path equals H_E/alpha. There is no inference of heat-operator order from form order.

Construct G_s by the spectral projection onto this isolated lowest eigenvalue (equivalently a local Riesz contour), and epsilon_s as its eigenvalue. No exact numerical ground energy is assumed or fitted. The bounded differentiable perturbation and local resolvent Neumann series make the rank-one projection and eigenvalue differentiable in s. A finite cover of [0,1] patches these local constructions. Choose a normalized ground vector psi_s in the parallel gauge <psi_s,psi'_s>=0. Differentiating the eigenvalue equation yields

    epsilon'_s=lambda <psi_s,D psi_s>,
    psi'_s=-(L_s-epsilon_s)^(-1)_(G_s-perp)
                    (I-G_s) lambda D psi_s.                (3)

These formulas hold on the common operator domain; the reduced inverse maps the Hilbert space into that domain. They also follow directly by differentiating the bounded contour resolvent. Phase choices do not affect G_s.

## 3. Complementary ground leakage and spectral shifts

The Q component of the ground equation is

    (C0/alpha+s lambda D-epsilon_s) Q psi_s
         = -(B/alpha) J*psi_s.

The operator on the left is >=d(lambda)=3-40lambda>=13/5. It is invertible on Q, so with ell=b/d,

    ||Q psi_s||<=ell,
    0<=epsilon'_s<=40lambda ell^2,
    ||G'_s||=||psi'_s||<=40lambda ell/g.                    (4)

The rank-one derivative equality follows by restricting
|psi'_s><psi_s|+|psi_s><psi'_s| to the orthogonal two-vector span. Integrate (4) over s. With d>=13/5 and g>=103/40, this gives exactly (2). The positive sign of the energy difference follows from D>=0. Ground equality is neither required nor asserted.

## 4. Centered leakage and the cancellation needed for uniform time

Write K_s=L_s-epsilon_s, E_s(u)=exp(-u K_s), and
F_s(u)=E_s(u)-G_s. Then ||E_s(u)||<=1 and ||F_s(u)||<=exp(-g u).
Variation of constants in the actual Q block gives, first on domain vectors and then by density,

    ||Q E_s(u)J|| <= b integral_0^u exp[-d(u-v)] dv <=ell.

These are strong vector integrals; the scalar norm bounds justify the estimates. Together with ||QG_s J||<=ell this proves

    ||Q F_s(u)J|| <= min(2ell, exp(-g u)).                  (5)

At u=0, QF_s(0)J=-QG_sJ can be nonzero. Dropping this initial projection term would give a false estimate.

Since K'_s=lambda D-epsilon'_s I is bounded, differentiating the heat evolution gives the Duhamel identity

    d_s J*E_s(sigma)J
      = -integral_0^sigma J* E_s(sigma-u)
                   (lambda D-epsilon'_s I) E_s(u) J du.   (6)

For fixed sigma this follows by the bounded perturbation identity and norm convergence of difference quotients. Expand each E_s=G_s+F_s. The ground-ground term vanishes **exactly**:

    G_s (lambda D-epsilon'_s I) G_s=0.

This cancellation removes a secular sigma term; a shared or omitted ground shift would not do so. The scalar cross terms vanish since G_s F_s=F_s G_s=0.

For each of the two remaining ground/excited terms, use one ground leakage ell and ||F_s(u)||<=exp(-g u). Its integrated bound is 40lambda ell/g. For the excited/excited D term, use (5) on one side as 2ell and on the other side as exp(-g u). Its integrated bound is 80lambda ell/g. For the scalar excited/excited term, F_s(sigma-u)F_s(u)=F_s(sigma), hence its integral is bounded by

    epsilon'_s sigma exp(-g sigma) <=40lambda ell^2/g.

Consequently, uniformly in sigma>=0 and s in [0,1],

    ||d_s J*E_s(sigma)J||
       <= (160lambda ell+40lambda ell^2)/g
       = [400/(d g)+250lambda/(d^2 g)] lambda^2
       <= [400/((13/5)(103/40))
             +(250/100)/((13/5)^2(103/40))] lambda^2
       = (1042500/17407) lambda^2 <60lambda^2.             (7)

Integrating in s gives (1). All inequalities remain valid at lambda=0, where the error is exactly zero. At t=0 both compressions equal I. As t tends to infinity the two centered semigroups converge in norm to their own ground projections at the proved excitation rate. Thus their compressed difference tends to J*(G_1-G_0)J, consistent with (2); it is not forced to vanish.

## 5. Verification and limitations

The forward checker verifies the continuous-range constants by exact rational endpoint inequalities and monotonicity of positive denominators. A two-state rational block fixture tests nonidentical grounds, centering cancellation, projection leakage and partial-shift failures. Its square roots and exponentials are bounded with rational intervals and Taylor remainders. It is an algebra fixture, **not** a spin truncation of the physical graph. The reverse checker reconstructs the proof's sufficient constants from polynomial inequalities and tests the secular cancellation by a different exact formulation. Both are written by the same agent.

The actual graph premises come from the frozen T1/Q2 contracts and source-bound reports. The written proof establishes the all-time/all-sector implication; finite checks do not establish infinite-dimensional completeness. Bounds on energy shifts are not a finite algorithm for calculating every ground eigenfunction. Relative late-time errors, finite implementation/truncation, real-time comparisons, physical matching and continuum construction remain open. No additional physical mass, fitted clock, golden-ratio coefficient or new axiom has been inserted.

The next already-selected broad goal is U, in a **different** canonical summable model. T2's gap and bounds cannot be transferred to it. U1 is not frozen or executed in this milestone, as requested.
