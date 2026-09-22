# AE1 forward: all-time locality of the actual Gaussian residual

Independent first-loop work after the AB/AC/AD gates, before reading reverse AE1. The homogeneous initial model and identity-extended indexed source A remain unchanged. Write r=||A||, Y={0,e1,e2,e3}, M=7|tau|<=35/1664 and G=H0+sum_c D_c, with every retained complete star Z_c=c+Y and ||D_c||<=M. No finite local Hilbert dimension, norm for H0 or physical clock fit is introduced.

## Unbounded onsite dynamics and an all-time comparison

The product onsite evolution exp(itH0) preserves every complete-factor support. It makes each bounded D_c into a strongly continuous bounded interaction of the same norm and support. Finite-volume cocycles therefore satisfy strong bounded-generator integral equations. This handles the unbounded electric terms; it does not replace them by a bounded matrix or use norm differentiability of their unitary group.

For explicit geometry let C_R={x in N_0^3:|x|_1<=2R+1}, R>=0, intersected with the containing finite volume if necessary. It contains Y. Keep all onsite terms and exactly the interaction stars wholly contained in C_R; call the resulting operator G_R. Its evolved A is supported in C_R, with exterior identity. Every coarse site belongs to at most four stars, hence every four-site star meets at most sixteen stars (a safe overcount; the interior deduplicated count is thirteen). A chain of m interacting stars beginning at Y has at most16^m choices and stays within distance2m of Y. Thus no chain of m<=R can contain a star omitted from G_R.

The interaction-picture commutator iteration gives, for a bounded B supported on Z,

    ||[alpha_t(A),B]||
      <=2r||B|| sum_(n>=0) (2M|t|)^n/n!
          * number of star chains of length n from Y meeting Z.

Here n=0 is the actual initial overlap, and each later star meets the preceding star. Internal unitary evolutions are removed in the commutator recursion, so this is a path count, not the growing-support Dyson majorant that failed at finite radius. This recursion is valid for every time. One direct way to establish it is the strong interaction-picture Jacobi/integral inequality of Nachtergaele–Sims, Eq.71, followed by iteration of the nonnegative terms. The finite coordination bounds the remainder by the tail of an exponential, so iteration converges at every fixed t.

Apply exact Duhamel comparison to G and G_R and sum over every omitted final interaction star. An n-step commutator followed by that final star has m=n+1 steps. Its norm factor after time integration is r(2M)^m|t|^m/m!, and the summed chain count is at most16^m. All terms of length m<=R vanish geometrically. Consequently

    ||alpha_t^G(A)-alpha_t^(G_R)(A)||
      <=r sum_(m>=R+1) (32M|t|)^m/m!
      <=r 2^[-(R+1)] exp(64M|t|).                 (AE1.1)

The trivial2r bound can always replace a larger right side. Every omitted boundary star is included; disjoint outside stars have zero commutator. No total interaction norm proportional to volume is used. Equation(AE1.1) is uniform in all finite containing volumes. Finite-volume bounded perturbation preserves D(H0); the comparison is proved first in domain pairings and then by bounded strong integrals on all vectors.

## Actual Gaussian residual approximation

Let R_s^G(A)=integral p_s(t)alpha_t^G(A)dt be AB2's actual residual, with the same normalized Gaussian. Let R_s^(G_R)(A) be its local approximation. This is an actual bounded operator on all states, not only a vacuum expectation. For v>=0, completing the square gives E exp(v|T|)<=2exp(v²s²/2), T normal with variance s². Integrating(AE1.1) over the full Gaussian, including its unbounded time support, therefore gives

    ||R_s^G(A)-R_s^(G_R)(A)||/r
      <=2^-R exp[(64Ms)²/2].                      (AE1.2)

Unlike a short-time power-series integration, this estimate controls the entire time tail. Fixing s and M, the error tends to zero in operator norm as R grows, uniformly in containing volumes. It also makes the local approximations norm-Cauchy as volume grows; this concerns the single residual operator, not a global generator or norm convergence of full unitaries.

At the actual cap M=35/1664 and s=4, the exponent is2450/169. Since exp(2/3)<2 and2450/169<44/3, exp(2450/169)<2^22. Thus

    R=64: residual approximation error <2^-42 r.

The collar has |C_R|=binomial(2R+4,3), so C_64 contains374660 complete onsite factors. This deliberately conservative certificate is costly and is not a claim of a practical full-Hilbert computation. It specifies the finite regional operator and a rigorous error, without claiming its spectral matrix has been evaluated. Combined with AB2, its local residual norm is below(626/1629+2^-42)r. No norm error for the corresponding Gaussian inverse is asserted in this loop; its AB2 graph-domain identity remains valid separately.

At tau=0 the actual source and both residuals vanish; ratios are not used. If the containing finite volume has no interactions outside C_R the comparison error is exactly zero. Positive-octant boundary omissions only reduce chain counts. Both nonzero signs of tau are covered through M. Physical s is a proof duration with energy resolution(alpha/8)/s; a,E_star,alpha,hbar remain fixed.

## What locality norm has actually been proved

For fixed s,M, define T_0=R_s^(G_0)(A) and T_R=R_s^(G_R)(A)-R_s^(G_(R-1))(A). The series sum_R T_R converges in operator norm to the actual residual, and(AE1.2) gives ||T_R||<=3r exp[(64Ms)²/2]2^-R for R>=1. Each T_R has support C_R and diameter4R+2 in coarse l1 distance. Thus this particular decomposition has summable exponential diameter weights whenever

    0<nu<log(2)/4.

This is a single-source diameter-weighted decomposition. A translation-family root sum requires counting how many translated collars contain the root; polynomial R³ overcounts preserve the same strict diameter exponent. It is not the old exp(mu*support cardinality) norm. In fact the available cardinality-weighted majorant contains exp[mu binomial(2R+4,3)]2^-R, whose terms grow for every mu>0. Hence this certificate cannot establish that required norm. Failure of the upper majorant does not prove actual residual divergence or impossibility of another connected-support decomposition.

The distinction matters for the next nonlinear stage: operator-norm contraction plus spatial diameter decay does not by itself control all ordered generated supports in the frozen cardinality-weighted stability scheme. No later-diagonal, homogeneous gap or continuum construction follows.

## Source reading and evidence

Primary source inspected in this loop: Nachtergaele and Sims, *On the Dynamics of Lattice Systems with Unbounded On-Site Terms in the Hamiltonian*, arXiv:1410.8174, https://arxiv.org/pdf/1410.8174. Reading depth: Theorem3.1 and its proof, especially Eq.71-73, and the finite-volume interaction-picture comparison in the proof of Theorem4.1. They justify strong calculus and commutator iteration with unbounded onsite terms. The geometry-specific constants32,64, collar formula and Gaussian bound above are derived here, not quoted from that paper. No finite-qudit cluster theorem is used.

The standard-library checker verifies actual star incidences, collar counts and diameter, path containment, Gaussian cap arithmetic, the rational exponential inequality and the cardinality/diameter distinction. Source inventories bind inherited reports and this proof; numeric algebra controls do not substitute for the all-time argument. Newton's inverse discipline motivates auditing the exact norm obtained, and Tesla's loading discipline keeps every boundary interaction. Scientific priority is unverified.
