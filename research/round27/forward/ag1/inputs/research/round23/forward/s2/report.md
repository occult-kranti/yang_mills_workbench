# S2 forward — a full-source filtered identity with an explicit residual

The frozen triangular filter defines a bounded skew-adjoint operator on the actual full source and preserves the full initial-G graph domain. It satisfies an exact commutator identity with a retained sinc frequency residual. Its ordered connected Dyson expansion has a positive weight2 certificate throughout the frozen coupling and time range. The same single-source filter is identified in the R2 infinite product-reference representation by a form-limit argument. These regulated statements are proved; removal of the residual, an unregulated inverse and a homogeneous gap remain open.

Current S2 reverse/skeptic solutions were not read before freezing this report and its checker. S1 evidence and its reviewed limitations are inherited. The filter is a proof construction, not a change of Hamiltonian.

## 1. Frozen model and source

Keep the actual complete24-link homogeneous block model, complete four-site stars Z_b, all21 omitted faces per star and D_b=Q_b phi_b Q_b with ||D_b||<=M=7|tau|. In a finite retained-star cuboid, G=H0+sum_b D_b is self-adjoint on D(H0). The source A=A_b^gen is S1's identity-extended local mixing of the n=2 repeated-anchor O1 word. With S1 variables,

    w_b=-a_b u_b-(||u_b||²/3)v_b,
    A_b=|w_b><Ω_b|+adjoint,
    0<||A_b||=||w_b||<=r_*=(4/3)(sqrt(7/12)|tau|)^3  (tau≠0). (1)

The definition also permits r_*=sup_b||A_b|| with this same upper bound. The declared support is Z_b, not an exterior vacuum projector. Positive E_star, alpha/E_star, hbar and a remain fixed. G,A are dimensionless; physical energies multiply them by delta=alpha/8. The integration parameter s equals delta times physical real time divided by hbar. Theta in(0,1/16] is a dimensionless proof-filter duration, with resolution energy delta/Theta; it changes neither action nor measured clock.

## 2. Exact strong-integral identity and its domains

For an arbitrary bounded self-adjoint A on the same Hilbert space define alpha_s(A)=exp(isG) A exp(-isG),

    L_Theta(A)=-(i/2) integral_-Theta^Theta
                   sign(s)(1-|s|/Theta) alpha_s(A) ds,
    R_Theta(A)=(1/(2Theta)) integral_-Theta^Theta alpha_s(A) ds. (2)

These vectorwise strong integrals exist: the integrands applied to each vector are continuous except the harmless jump at s=0, uniformly bounded and supported on a compact interval. Their bounded-operator extensions satisfy

    L_Theta*=-L_Theta, R_Theta*=R_Theta,
    ||L_Theta||<=Theta||A||/2,  ||R_Theta||<=||A||.             (3)

No operator-norm continuity of the unitary group or its conjugation is assumed. To compute a commutator, first pair with phi,psi in D(G). The scalar function <phi,alpha_s(A)psi> is differentiable by moving the two G derivatives to the domain vectors; A need not preserve D(G). Its weak derivative corresponds to i[G,alpha_s(A)]. Let f(s)=sign(s)(1-|s|/Theta) on its support. It has vanishing endpoint values and distributional derivative 2delta_0-(1/Theta)1_[-Theta,Theta]. Integration by parts therefore gives the weak identity

    [L_Theta,G]=-A+R_Theta.                                  (4)

This identity proves the missing domain fact, rather than presupposing it. For fixed psi in D(G), it expresses <G phi,L_Theta psi> as <phi,L_Theta G psi+(A-R_Theta)psi> for every phi in D(G). Self-adjointness of G then implies L_Theta psi in D(G), with G L_Theta psi=L_Theta G psi+(A-R_Theta)psi. Consequently

    ||[L_Theta,G]||<=2||A||,
    ||L_Theta||_(graph G)<=Theta||A||/2+2||A||.                (5)

The graph norm is ||psi||+||Gpsi||. The exponential series and its inverse converge in this Banach norm, proving exp(±theta L_Theta)D(G)=D(G) for every finite real theta. This is an exact full-exterior-sector result. It applies equally to any self-adjoint G for which (2) is defined; locality is a separate argument below.

## 3. Frequency action and the regulator limitation

On a matrix element between energies E_m,E_n put omega=E_m-E_n. Direct integration, with the continuous zero-frequency extension, gives

    ell_Theta(omega) = [1-sinc(omega Theta)]/omega,
    L_Theta(A)_(mn)=ell_Theta(omega) A_(mn),
    R_Theta(A)_(mn)=sinc(omega Theta) A_(mn),                 (6)
    sinc(x)=sin(x)/x, sinc(0)=1, ell_Theta(0)=0.

Thus multiplication by E_n-E_m in [L,G] gives exactly -(1-sinc(omegaTheta)). In every equal-energy block the residual is the entire original source. At small x, sinc(x)=1-x²/6+O(x^4), so decreasing Theta makes this filter remove less, not more, of the source. Formula(6) is the spectral interpretation; the proof of (4) does not require pure point spectrum or bounded double-operator-integral assertions.

For a fixed nonzero scalar frequency, sinc(omegaTheta) tends to0 as Theta tends to infinity. This pointwise observation neither removes an actual resonant source block nor proves operator-norm convergence over arbitrary source frequencies. It also leaves the frozen positive connected-support certificate's finite radius. The elementary G=diag(0,1,1), A=|1><2|+adjoint fixture has R_Theta=A and L_Theta=0 at every Theta. It rejects a universal residual-free inference, not proves an actual SU2 resonance obstruction. Actual low-frequency source control remains missing.

## 4. All-order connected Dyson expansion at weight2

The unbounded onsite evolution alpha_s^0 preserves the support of every bounded local operator: it is conjugation by the local onsite tensor-sum unitary, extended by identity. Its norm is unchanged. To make the interaction-picture ordering explicit, let V(s)=exp(-isH0)exp(isG), so V'(s)=i D_I(s)V(s), D_I(s)=alpha_-s^0(D). The bounded finite-volume interaction yields

    gamma_s(A)=V(s) A V(s)*,
    gamma_s'=i[D_I(s),gamma_s], gamma_0=A,
    alpha_s^G(A)=alpha_s^0(gamma_s(A)).                        (7)

Equation(7) gives the time-ordered Dyson nested-commutator series. For negative s use reversed simplex orientation; its norm is bounded by |s|^n/n!. Every term is an ordered word with a source star and n interaction stars; repetitions remain distinct. If a new star is disjoint from the previously generated union the commutator vanishes. Each surviving union is connected and has at most4+3n sites. The outer onsite conjugation changes neither support nor norm. The finite-volume bounded-interaction Dyson series converges strongly with its standard norm majorant; it never puts unbounded H0 into a norm BCH series.

Here is the full root-sum certificate, not just a support-size assertion. Let N_n bound the indexed root sum of 2^|Y| times the norm of depth-n integrands, before time integration, uniformly in all time labels. Starting from a translated family of sources, at most4 source stars contain a root, so N_0<=64r_*. Inserting a star contributes a commutator factor2M and at most3 new sites, giving a factor16M. At a fixed new root, split into the root lying in the old union or in the inserted star. There are at most4|Y| stars meeting the old union, and at most4 stars containing the root with4 sites through which to meet earlier unions. Thus

    N_(n+1)<=64M(8+3n)N_n,
    N_n<=64r_* (192M)^n (8/3)_n.                             (8)

This counts incoming anchors, ordered repetitions and connected supports meeting only previous additions. Double counting the root in the intersection only increases the upper bound. Finite cuboid deletions reduce it. The rising factorial is determined by the displayed recurrence at every order, not guessed from a finite enumeration. With c=192M and p=8/3, the generalized-binomial series gives

    ||alpha_s^G(A_family)||_weight2
       <=64r_* sum_n (p)_n(c|s|)^n/n!
       =64r_*(1-c|s|)^(-p), c|s|<1.                          (9)

The equality of the positive scalar series follows by its differential equation (1-x)F'=pF, F(0)=1. It establishes an explicit all-order coefficient sum. Strong integrals of each bounded-support word remain in that local bounded-operator algebra, so support labels are unchanged by integration.

The precise time-simplex/filter coefficients are

    integral_0^Theta (1-s/Theta)s^n/n! ds=Theta^(n+1)/(n+2)!,
    (1/Theta)integral_0^Theta s^n/n! ds=Theta^n/(n+1)!.       (10)

Using the factor1/2 and both signs of s in (2), (8)–(10) imply

    ||L_Theta(A_family)||_weight2
      <=64r_* sum_n (p)_n c^n Theta^(n+1)/(n+2)!
      <=32Theta r_* (1-cTheta)^(-p),
    ||R_Theta(A_family)||_weight2
      <=64r_* sum_n (p)_n(cTheta)^n/(n+1)!
      <=64r_* (1-cTheta)^(-p).                               (11)

The bounded family notation denotes its indexed interaction decomposition, not a bounded extensive operator sum in infinite volume. Its support weight is exactly2^|Y|. No radius-to-volume replacement occurs and no weight loss is hidden.

For all frozen parameters,

    cTheta<=192*7*(5/1664)*(1/16)=105/416<1,
    (1-cTheta)^(-8/3)<=(416/311)^3.                           (12)

Equations(11)–(12) are numerical positive-volume-weight certificates covering the entire contract. They give no all-time integration or convergent unfiltered inverse. At cTheta>=1 the displayed positive series loses its radius; failure of this upper certificate is not actual dynamics divergence. At tau=0 the actual source and interaction vanish, a valid exact exception.

## 5. Identification in the R2 infinite representation

This paragraph supplies the additional form-limit premise instead of assuming it. Work in exactly R2's incomplete product-reference Hilbert space, with closed H0 form h0, common form domain F and G associated with h0+d. Its absolute form estimate is |d[phi,psi]|<=kappa h0[phi]^(1/2)h0[psi]^(1/2), kappa=4M<1. Extend finite-volume G_Lambda by the unaltered H0 on exterior factors; equivalently G_Lambda=H0+D_Lambda on the full representation. Their forms obey the same lower coercivity g=1-kappa.

Let u=(G+1)^-1 f and u_Lambda=(G_Lambda+1)^-1 f. For e=u_Lambda-u, the resolvent form equations give

    (h0+d_Lambda+1)[e,e]=(d-d_Lambda)[e,u].

Absolute Cauchy–Schwarz over omitted stars yields

    |(d-d_Lambda)[e,u]|
       <=sqrt(kappa h0[e]) * sqrt(M sum_omitted ||Q_b u||²).

Since sum_all ||Q_b u||²<=4h0[u]<infinity, the omitted tail tends to0 along a complete-star cuboid exhaustion. Coercivity therefore gives

    ||u_Lambda-u||_F
       <=sqrt(kappa)/g * sqrt(M sum_omitted ||Q_b u||²) ->0,  (13)

where ||x||_F²=||x||²+h0[x]. Thus G_Lambda converges in strong resolvent sense to the actual R2 G. Spectral calculus then gives strong convergence of their unitary groups, uniformly on compact time intervals. This standard consequence can be seen by first restricting to a bounded spectral window, approximating its continuous functions by resolvent functions and then controlling the vector spectral tails. Hence alpha_s^(G_Lambda)(A) tends strongly to alpha_s^G(A) for every bounded A and fixed s; dominated vector integration identifies the limits of (2).

For a *single fixed local source*, the connected Dyson expansions give a stronger volume comparison in the short-time interval: every fixed word occurs in all sufficiently large cuboids, while the uniform summable all-order tail in (8)–(12) tends to0. All word supports contain the source's fixed root, so its total operator-norm sum is controlled by the root certificate. Therefore the finite-volume local-source expansions converge in operator norm, uniformly for |s|<=Theta, to the same strongly identified R2 evolution. This also identifies norm limits of the single-source L_Theta and R_Theta. The arbitrary self-adjoint domain proof in Section2 applies directly to this G and proves (4) on D(G). It does not claim D(G)=D(H0) for arbitrary vectors or construct a bounded sum of all translated filters.

## Evidence, source comparison and remaining target

The checker uses exact rational time integrals, commutator algebra and finite connected-word enumeration only as controls. The all-order bound and infinite-domain/representation arguments are the written proofs above. A bounded-frequency sine series is enclosed by exact alternating rational bounds; equal-energy residual retention is exact. Controls reject the opposite sign, missing residual, lost ordered multiplicity, wrong simplex/filter factors and integration of the positive majorant outside its radius. Neither a finite matrix nor a convergent scalar upper bound proves actual SU2 spectral completeness.

Filtered spectral-flow generators are established operator methods; the targeted source comparison and reading depth appear in source-notes.md. The precise triangular residual, model-specific connected coefficients and identification here are project derivations; scientific priority remains unverified. This closes the selected *regulated* S2 construction only. The original unregularized all-sector inverse, source low-frequency control, later-diagonal induction, full homogeneous numerical gap, physical calibration and four-dimensional continuum construction remain open.

    python3 -B research/round23/forward/s2/check.py --output /absolute/new/s2-forward
    python3 -B -O research/round23/forward/s2/check.py --output /absolute/new/s2-forward-O
