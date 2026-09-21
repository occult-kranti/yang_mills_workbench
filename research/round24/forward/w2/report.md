# W2 forward — repeated filters at the fixed initial diagonal

Independent forward derivation before current reverse W2. W1's uniform moment refinement is attributed to the reverse researcher and independent skeptic; it is inherited here, not rediscovered. Newton's synthesis requires a convergent target with its topology; Tesla's complete-system condition keeps the exterior identity. The actual vacuum-column iteration converges with explicit uniform rates. Full-source and later-diagonal closure remain limited.

## Finite-step full-source identity

Fix the actual initial homogeneous S/W1 G, source A, r=||A|| and 0<Theta≤1/16. Define the bounded maps R=R_Theta and L=L_Theta from S2, then

    A_n=R^n(A), A_0=A,
    K_n=sum_(j=0)^(n-1) L(A_j), K_0=0.               (W2.1)

The averages are over the **actual** full G. Every A_j is self-adjoint, every K_n skew-adjoint, and the original source remains identity-extended on the exterior. Conjugation averages are contractions, so ||A_n||≤r and ||K_n||≤nTheta r/2. Applying S2's domain theorem to each bounded A_j gives, on D(G),

    [K_n,G]=-A+A_n,
    ||[K_n,G]||≤2r.                                 (W2.2)

Thus K_n preserves D(G), is bounded in its graph norm by nTheta r/2+2r, and exp(±K_n) preserves that domain at every finite n. This is an actual all-step regulated identity; no residual is dropped. It neither asserts a uniform norm bound on K_n nor defines its infinite exponential.

The maps commute because they integrate the same one-parameter automorphisms. R^n is averaging alpha_s(A) against the n-fold convolution of the uniform measure on [-Theta,Theta]. Its time support is [-nTheta,nTheta]. In a spectral matrix element of Bohr frequency omega the exact multipliers are

    A_n: sinc(Theta omega)^n,
    K_n: [1-sinc(Theta omega)^n]/omega,              (W2.3)

with continuous zero-frequency values 1 and 0, respectively. The finite geometric sum, including negative sinc values, proves (W2.3). Every equal-energy source block remains unchanged for every n.

## Actual vacuum-column convergence with an explicit rate

Let Omega be the actual product ground of initial G, xi=A Omega, r=||xi||. The inherited complete-star form comparison gives

    G≥g H0≥g(I-|Omega><Omega|),
    g=1-4M, M=7|tau|, g≥381/416>0.

S1 proves xi perpendicular to Omega; W1 reverse proves its finite form moment ≤24(1+4M)r² and nonvanishing r≥sigma³/432 for tau≠0. Only the actual positive gap and orthogonality are needed for the decay theorem.

For a=Theta g≤1/16 and every x≥a,

    |sinc x|≤rho:=1-a²/10<1.                       (W2.4)

A self-contained scalar proof: on [0,1], the alternating sine bound gives 0≤sinc x≤1-x²/6+x⁴/120≤1-x²/10. On [1,2], sin x is positive and that same polynomial is decreasing, so sinc x≤101/120<9/10. On [2,infinity), |sinc x|≤1/2. These intervals imply (W2.4); no scalar bound on a general double-operator multiplier is inferred.

The vacuum column is an ordinary spectral-calculus vector:

    A_n Omega=sinc(Theta G)^n xi,
    K_n Omega=G_Q^-1[I-sinc(Theta G)^n]xi.          (W2.5)

Therefore on every containing finite volume and on the admitted infinite reference representation,

    ||A_n Omega||≤rho^n r,
    ||K_n Omega-G_Q^-1 xi||≤rho^n r/g,
    ||K_n Omega-G_Q^-1 xi||_(graph G)
       ≤(1+1/g)rho^n r.                            (W2.6)

The graph statement uses ||G(K_n Omega-G_Q^-1xi)||≤rho^n r. It is convergence of one vector column; the target G_Q^-1xi is the global-vacuum inverse column, not an identity-extended all-exterior inverse operator. Constants are uniform in volume and in the allowed tau interval at fixed positive Theta. As Theta decreases the certified rate worsens, consistent with W1's residual persistence. This is no uniform n-rate over Theta→0.

For Theta=1/16 and the worst allowed g=381/416, put d=(381/6656)²/10. Since (1-d)^n≤exp(-nd), n=ceil(7/d) suffices for rho^n<10^-3; exp(7)>1000 is verified by a positive finite Taylor sum. The checker calculates n exactly. This yields an actual source-column error below r/1000 and graph inverse error below (1+1/g)r/1000. It does not bound the full residual by those numbers.

The retained W1 moment also gives a finite-step lower certificate. For real y with |y|≤1, |1-y^n|≤n|1-y|; and 0≤1-sinc x≤x/2 for x≥0. Thus

    <xi,A_n Omega>≥[1-12nTheta(1+4M)]r².             (W2.7)

Whenever its right side is positive, ||A_n|| is at least that coefficient times r. A negative lower estimate is merely inconclusive. This estimate does not contradict eventual column decay or establish a cubic obstruction to every n-dependent procedure.

## Full source: precisely what follows in finite volume

Every fixed finite complete-block volume has compact resolvent. The finite sum of link Casimirs has discrete spin spectrum with finite multiplicity below each energy, hence compact resolvent; the selected potentials, shifts and finite D sum are bounded perturbations. The resolvent identity preserves compactness. Thus G has a complete discrete energy decomposition with possibly degenerate finite-rank eigenspaces P_E.

For a vector supported in one P_F, orthogonality gives

    A_n v=sum_E sinc(Theta(E-F))^n P_E A v.

The squared terms have summable majorant ||P_E A v||². Dominated convergence kills each nonzero energy difference and retains E=F. Finite sums of energy vectors are dense, and ||A_n||≤r uniformly. Hence in this fixed finite volume

    A_n -> A_diag:=sum_E P_E A P_E strongly.       (W2.8)

The diagonal sum defines a bounded operator of norm ≤r because its output blocks are orthogonal. This is a full-source **strong** limit; it is zero if and only if all actual equal-energy blocks vanish. Their actual values for this cubic source are still uncomputed. The actual vacuum diagonal block is zero and is consistent with (W2.6).

No pure-point hypothesis is established for the full infinite-volume G in this loop. Therefore (W2.8) is not exported to that representation. Nor does fixed-volume compact resolvent force a positive lower bound on excited energy differences, operator-norm decay of A_n, convergence of K_n, or uniformity in volume.

A precise logical counterexample explains the missing norm premise. On l² paired levels set E_(k,0)=2k, E_(k,1)=2k+1/(k+1), and let A swap each pair. G has compact resolvent and A has zero equal-energy blocks. For each fixed n, sinc(Theta/(k+1))^n→1 as k→infinity; consequently ||R^n(A)||=1 although R^n(A)→0 strongly. The formal inverse pair amplitude is k+1 and unbounded. This is **not** an actual SU2 spectrum and proves no actual obstruction there; it shows why compactness and strong convergence alone cannot close the required norm theorem.

## Connected supports and later diagonals

Finite convolution times make each iterated map well-defined as a bounded operator. To reuse the existing S2 positive weight-2 expansion directly, however, one needs c nTheta<1 with c=192M. Then the entire convolution lies in the interval on which the displayed all-order coefficient sum is controlled, giving

    ||A_n,family||_weight2≤64r_*(1-c nTheta)^(-8/3).

At the frozen cap cTheta=105/416, this particular bound covers only n≤3. Its loss at n=4 does not prove that A_4 or the physical dynamics diverges. Reapplying a single-star bound to A_j as though it still had one four-site support would discard generated supports and ordered multiplicities. A long-time interaction-norm theorem with a stated weight loss, or a different all-sector inverse construction, is required for the tens-of-thousands-step column estimate to imply useful interaction control.

The present iteration holds G fixed. An actual successive diagonalization changes G, its scalar and diagonal terms, the source, reference projection, form domain and support budgets. The original C=bI+A_gen+Q(C-bI)Q is retained; (W2.1) does not update those terms or prove later-diagonal induction. All new n,Theta,rho,d quantities are counts, proof durations or derived dimensionless estimates. Physical a,E_star,alpha/E_star,hbar and delta_energy=alpha/8 are unchanged.

## Evidence and scope

The checker verifies telescoping in nonresonant and exactly resonant rational spectral fixtures, the explicit iteration count, a decreasing-gap wrong-topology control and the existing weighted radius. These fixtures are labeled logical/algebraic controls. The actual convergence statements rely on the full source/domain and spectral proofs above. No original paper is newly invoked beyond the inherited S2 framework; compactness and scalar inequalities are proved here. Scientific priority is unverified. Full-source norm/weighted convergence, actual excited-sector blocks, later-diagonal closure, homogeneous gap and continuum construction remain open.
