# S1 independent contract-specific preparation

Read only frozen S1 contract and inherited reports. Current producers remain unread. This preparation follows the shared cubic definition; it is independent of their derivations.

Let `m=<u,u>`, `c=<u,v>=<u,H0 u>>0` for nonzero tau, and `d=<u,phi u>`. The source is nonzero because the actual SU2 inherited norm is `||v||^2=7tau^2/12`, H0 has an injective reduced inverse, and hence u is nonzero. With `S=|u><Omega|-adjoint`, direct rank-two algebra gives

`ad_S^2(phi)Omega=-3c u-m v+2d Omega`,
`ad_S^2(A)Omega=-3c u-m v`.

Therefore the frozen cubic source is exactly

`w=Q C Omega=-c u-(m/3)v`,
`<u,w>=-(4/3)mc<0`.

This proves nonzero without knowing the full selected-strip spectrum or substituting a spin fixture. A useful bound is `||w||<=(4/3)||v||^3` because `||u||<=||v||` and `c<=||v||^2`. Coefficients are dimensionless and w is cubic in tau at fixed onsite reference. The scalar d disappears under Q; omitting either nested term changes the coefficient.

On `Y=Z_0`, only anchor zero is interior. The actual initial `G_Y=H0_Y+D_0` has domain D(H0_Y), ground Omega and gap at least `1-28|tau|`; the sharper local bound `1-7|tau|` is also available but must be stated as such. The local inverse `z=(G_Y|Q)^-1 w` gives the graph-preserving rank-two L and `[L,G_Y]=-A_gen`. Its extension by identity leaves the actual full-volume commutator defect from the three possible crossing anchors `e_x,e_y,e_z` (when retained). Their union supports with Y have seven sites. This is a uniform finite number for this source, not an all-stage connected expansion.

For an exterior free-Haar excitation at a coarse site outside Y, the local A_gen acts with norm ||w||, whereas its global vacuum-projected version vanishes. This control needs no formula for w in individual links because product-factor orthogonality and the exact nonzero proof already supply it.

Acceptance requires honest limits. The local inverse and full-volume boundary identity do not establish an all-exterior inverse for G_Lambda. The initial ground gap does not control excited energy differences, and the generic trace obstruction in preparation.md is not an actual SU2 obstruction. A connected decomposition for three defects cannot be iterated without all later source, inverse, weight and domain estimates.
