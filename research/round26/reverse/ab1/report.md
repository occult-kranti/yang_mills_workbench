# AB1 reverse: an actual-source bound on every near-resonant block

This independent reverse reconstruction is frozen before reading current forward work. The model is the S/W homogeneous initial diagonal, with fixed positive a, E_star, alpha/E_star and hbar and energy unit delta=alpha/8. Newton's reverse test asks what vanishing must be proved; Tesla's loading test retains all exterior states and crossing stars. No historical assertion or new action parameter enters the proof.

Choose the finite coarse cuboid Lambda={0,1,2}^3. It contains 27 complete 24-link reference factors and all eight stars with anchors in {0,1}^3. Y={0,e_x,e_y,e_z}. The same statement holds for every larger containing cuboid. H0 is the inherited tensor sum with product vacuum, gap at least one, and selected bounded strip potentials. G=H0+sum_b D_b, D_b=Q_b phi_b Q_b, phi_b=-(tau/3)sum of all 21 omitted Wilson faces, M=7|tau|, |tau|<=5/1664. G and H0 have the same operator domain in each finite volume. Compactness is inherited from finite-link Casimirs plus bounded perturbations, not from a finite Hilbert-space truncation.

The actual indexed source is A=(|w><o|+|o><w|) tensor I_ext, where v=phi_0 o, u=H0,Y,Q^-1 v, a=<u,v>, beta=||u||², w=-a u-(beta/3)v and r=||w||. Inherited actual Haar identities give sigma²=7tau²/12, sigma³/432<=r<=(4/3)sigma³ for nonzero tau. This is one indexed cubic source, not a sum of all cubic words. A bounded rank-two local operator tensored with identity has norm r regardless of exterior excitation. The source vanishes exactly at tau=0.

## Reverse reconstruction of the missing spectral requirement

If a bounded graph-preserving K satisfies [K,G]=-A, then P_E A P_E=0 for every actual energy projection. Vanishing blocks alone are not sufficient: division by all nonzero Bohr differences must define a bounded graph-preserving operator, and a useful interaction result also requires weighted connected support. A vacuum-column inverse meets none of those full-operator obligations automatically.

A quantitative source-specific conclusion is nevertheless available. Let G_Y=H0,Y+D_0, g_Y=1-M>0 and k=G_Y,Q^-1 w. Define

    K_Y=|k><o|-|o><k|, K=K_Y tensor I_ext.
    ||K||=||k||<=r/g_Y, [K,G_Y]=-A_Y.              (AB1.R1)

The local inverse gives k in D(G_Y)=D(H0,Y). Finite-rank operators built from k and o preserve this domain. Their identity extension preserves D(H0,Lambda): it commutes with exterior spectral cutoffs and has bounded local H0 commutator. Thus it preserves D(G), and all identities below hold on that domain.

Only the three anchors e_x,e_y,e_z cross Y; each retained crossing star meets Y in one site and has union size seven. Every other star is either the interior origin or disjoint. Retaining both Q factors and all 21 faces in each crossing D_c gives the exact identity

    [K,G]=-A+F, F=sum_(c=e_x,e_y,e_z) [K,D_c],
    ||F||<=6 M r/(1-M).                           (AB1.R2)

The identity extends as a bounded commutator. This is the complete actual cuboid defect; no exterior vacuum projector, single-link cover, or omitted crossing is used.

For an exact energy projection, P_E[K,G]P_E=0 and therefore

    P_E A P_E=P_E F P_E,
    ||P_E A P_E|| <= 6 M r/(1-M).                 (AB1.R3)

The bound simultaneously controls the entire diagonal map A_diag=sum_E P_E A P_E, because its blocks act on mutually orthogonal subspaces. Hence ||A_diag||<=6Mr/(1-M). This is a full-source fixed-volume norm bound on the previously unevaluated surviving map; it is not just a tested vacuum column. Combined with r=O(|tau|³), every exact resonant block and the complete diagonal map are O(|tau|⁴), uniformly in containing finite cuboids. At the frozen cap the bound is (210/1629)r<0.129r. It excludes an order-cubic equal-energy contribution with a coupling-independent coefficient. It does not prove the blocks vanish for nonzero tau.

More generally take the actual spectral interval P=1_[E-epsilon,E+epsilon](G), epsilon>=0. Since ||(G-E)P||<=epsilon,

    ||P A P|| <= 2 epsilon ||K||+||F||
               <= (2epsilon+6M)r/(1-M).          (AB1.R4)

Here epsilon is a spectral resolution, physically delta epsilon, not a clock or action deformation. Equation (AB1.R4) relates the source's complete same-window matrix to its omitted loading. It supplies a source-specific near-resonance exclusion estimate without inventing a spectrum. The exact zero-width result has the usual interpretation for an eigenvalue; interval estimates remain valid for any bounded energy interval.

The three crossing supports also yield, for the single-source declared decomposition, sum exp(mu|support|)||F_c||<=6Mr exp(7mu)/(1-M). This does not provide all translated-source root sums, convergence of an infinite inverse, a later-diagonal induction, or a homogeneous numerical gap. The diagonal spectral projection need not preserve locality, so no weighted bound on A_diag follows from its operator-norm bound.

## Scope and checks

The checker enumerates the actual cuboid stars and connected seven-site unions, verifies the cap arithmetic and both signs including tau=0, and binds this report, checker, methods and inherited sources. These are actual geometry and rational estimate checks; no generic spectral fixture is called an SU(2) calculation. Domain and spectral statements are analytic proofs. Full excited blocks remain unevaluated, and nonzero versus zero resonant blocks remains open. Scientific priority and continuum consequences are not claimed.
