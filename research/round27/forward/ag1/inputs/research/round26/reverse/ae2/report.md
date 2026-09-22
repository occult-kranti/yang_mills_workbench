# AE2 reverse: compact-time contraction with the original cardinality norm

Independent reverse derivation under AE2, without current forward AE2 access. Keep the actual homogeneous initial G and the translated indexed cubic source family {A_b}, each supported on the complete four-factor star Y_b and extended by identity. The frozen subrange is M=7|tau|<=1/1000, equivalently |tau|<=1/7000; this restricts the original coupling parameter, without deforming the action or fitting a physical clock. The filter duration is fixed at T=3.

For every indexed source in every containing finite volume, including interior translations,

    ||R_T(A_b)|| <= (2072/2997)||A_b|| <0.7||A_b||. (AE2.R1)

At the same time, both its residual family and inverse family admit finite bounds in the ORIGINAL rooted norm sup_x sum_(indexed Y containing x) 2^|Y| ||term_Y||. This is simultaneous per-source operator contraction and finite weighted summability. It is not a weighted contraction, an exact inverse or an all-stage stability theorem.

## Kernel, inverse and domain

Use p_T(t)=(1-|t|/T)_+/T and

    h_T(t)=(sign(t)/2)(1-|t|/T)_+²,
    R_T(A)=integral p_T(t)alpha_t^G(A)dt,
    J_T(A)=-i integral h_T(t)alpha_t^G(A)dt.

Direct polynomial integration gives integral p_T=1, ||p_T'||_1=2/T, ||h_T||_1=T/3, and h_T'=delta_0-p_T in distributions. The strong vector integrals define bounded operators, with J_T skew-adjoint and ||J_T(A)||<=T||A||/3. AB2's weak pairing and integration-by-parts argument therefore proves on the actual closed domain

    [J_T(A),G]=-A+R_T(A), J_T(A)D(G) subset D(G). (AE2.R2)

The bounded commutator has norm at most 2||A||, and the inverse has bounded G graph action. No finite onsite dimension or source-domain differentiation is assumed. At Bohr difference omega the residual multiplier is sinc²(Tomega/2), since p_T is the convolution of two uniform densities on [-T/2,T/2]. The inverse multiplier is [1-sinc²(Tomega/2)]/omega, continuously zero at omega=0. Equal-energy source blocks are retained exactly; the residual is never dropped.

## Complete boundary coefficient for the entire translated family

For each b, use the actual local inverse K_b for G_(Y_b)=H0,Y_b+D_b. It has ||K_b||<=r_b/(1-M), r_b=||A_b||, and

    [K_b,G]=-A_b+F_b,
    F_b=sum_(c crossing Y_b)[K_b,D_c].            (AE2.R3)

The difference set of the star contains thirteen anchors: zero, plus/minus e_i, and e_i-e_j for i!=j. Therefore an interior translated source has up to twelve crossing stars; the positive-octant origin has only three. Each crossing meets one site and its union has seven complete factors. Thus

    ||F_b||<=24M r_b/(1-M),                      (AE2.R4)

uniformly over the entire family. The origin-only coefficient 6M cannot be applied to interior sources. Every retained crossing term remains in (AE2.R3), and physical boundaries only delete terms.

Apply p_T integration by parts to A_b=F_b-[K_b,G], keeping R_T(F_b). It gives

    ||R_T(A_b)||/r_b <=min(1,(24M+2/T)/(1-M)), r_b>0. (AE2.R5)

The right side increases in M. At M=1/1000,T=3 it is exactly 2072/2997<7/10, proving (AE2.R1) continuously on the full restricted interval and for either coupling sign. With no crossings the 24M term disappears. At tau=0 the actual cubic sources, inverses and residuals are all zero; ratios by r_b are not used. A positive boundary upper budget does not establish a nonzero actual resonant block.

## All connected words in the original rooted cardinality weight

Use the bounded interaction picture around unbounded H0; onsite evolution preserves complete supports. A surviving depth-n Dyson word consists of a source star and n ordered interaction stars. Each new star must meet the accumulated union, which contains at most n+1 stars. Since one star meets at most thirteen anchor stars, there are at most 13^n n! relative ordered words. Repeated anchors and attachments to earlier generated stars remain. A word union has at most 4+3n factors, and at most 4+3n translations put a chosen root in that union.

Let r_*=sup_b r_b. Combining rooted translations, cardinality weight, ordered words, commutator factor and simplex volume gives the actual indexed order-n bound

    (4+3n) 2^(4+3n) (13^n n!) (2M)^n r_* |t|^n/n!
       =16r_*(4+3n)(208M|t|)^n.                 (AE2.R6)

Finite-volume or octant restrictions only remove terms. This is the same connected-support counting proved in reverse S2, rederived for the present filter; no cubic collar or diameter weight replaces its declared supports.

Put zeta=208MT. Exact integration with p_T and |h_T| yields

    ||R_T family||_w2 <=32r_* sum_(n>=0)
                      (4+3n)zeta^n/[(n+1)(n+2)],
    ||J_T family||_w2 <=32r_*T sum_(n>=0)
                      (4+3n)zeta^n/[(n+1)(n+2)(n+3)]. (AE2.R7)

In particular, for zeta<1 and F(zeta)=(4-zeta)/(1-zeta)²,

    ||R_T family||_w2<=16r_*F(zeta),
    ||J_T family||_w2<=16r_*(T/3)F(zeta).       (AE2.R8)

At the frozen subrange endpoint zeta=78/125, T/3=1, both upper bounds are

    (844000/2209)r_* <383r_*.

Every omitted positive-order tail is bounded explicitly by the rational geometric derivative formula for sum_(n>N)(4+3n)zeta^n, so both series converge uniformly over the restricted interval. Strong integrals of each fixed-support word retain that same local algebra. In a finite volume there can still be infinitely many indexed words; their absolute weighted convergence, not finite spatial volume alone, justifies regrouping.

The initial family has a convenient upper budget 64r_* in the same norm. The positive estimates above do not improve it: the exact integrated residual upper series already has constant term 64r_* and positive higher terms when M>0. This proves only that this positive majorant cannot establish weighted contraction, not that the actual weighted residual norm is larger. No volume-independent norm is asserted for the extensive sum of all translated sources.

## Audit at the original coupling cap

For this reverse positive residual series, zeta<1 is needed; at zeta=1 the residual terms behave as a positive constant divided by n and diverge. Hence the certificate requires T<1/(208M). The family full-operator contraction certificate requires T>2/(1-25M), assuming 25M<1. A nonempty open duration interval therefore requires M<1/441. At the original cap M=35/1664 this fails decisively: weighted convergence requires T<8/35, while source contraction requires T>3328/789. There is no duration satisfying both certificates there.

Even the inherited forward S2 majorant with improved constant 192 instead of 208 would require T<1/(192M), still incompatible with that family contraction bound at the cap. This audits known positive certificates, not all possible filters or decompositions. The no-crossing and origin-only bounds improve the contraction condition but do not rescue this radius at the original cap either. Failure of an upper certificate is not actual physical divergence or a proof that a better inverse cannot exist.

Newton's reconstruction keeps the exact norm requested; Tesla's loading audit exposes the twelve-versus-three crossing distinction. The accepted restricted construction supplies initial-G per-source contraction plus original-weight summability, while retaining the residual and complete boundary terms. Iterating a newly generated residual would change its support class; updating G would change its domain, inverse and source estimates. Those later-stage obligations, the homogeneous numerical gap, physical calibration and continuum construction remain open. Scientific priority is unverified.
