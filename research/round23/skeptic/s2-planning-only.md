# Prospective S2 filter question — planning only

Requested by the advisor while S1 producers were still working. No S2 contract is selected here, no S2 production run is executed, and this note adds zero loops.

A candidate regularized all-sector map for self-adjoint dimensionless G and bounded self-adjoint A is

`L_rho=-(i/2) integral_R sign(r) exp(-rho|r|) alpha_r(A) dr`,
`alpha_r(A)=exp(irG) A exp(-irG)`.

At the formal integration-by-parts level it obeys `[L_rho,G]=-A+R_rho`, where `R_rho=(rho/2) integral_R exp(-rho|r|)alpha_r(A)dr`. Its residual spectral multiplier is `rho^2/(rho^2+omega^2)`. Thus same-energy source blocks survive at every rho. Rho is a retained proof resolution in delta energy units, not a new physical clock or action coefficient.

A production contract would need to prove: vectorwise integrability; the weak commutator identity on D(G); boundedness of the resulting commutator; and the implication that L_rho maps D(G) into itself. It must not assume A itself preserves D(G). Finite-volume bounded interactions make an interaction-picture route possible despite unbounded onsite generators.

For useful connected-support sums, every Dyson word must retain its actual growing union, ordered multiplicity and root-containing translations. The naive positive Dyson majorant generally has a finite time radius because available intersecting anchors grow with support. Exponential damping over all times does not automatically make termwise integration of this positive majorant summable. A proof that merely integrates the Hilbert operator bound misses the requested weighted interaction topology.

A possible compact-time fallback is the triangular filter

`L_T=-(i/2) integral_{-T}^T sign(r)(1-|r|/T) alpha_r(A)dr`.

The candidate identity is `[L_T,G]=-A+R_T`, with `R_T=(1/(2T))integral_{-T}^T alpha_r(A)dr`, and its direct norm budget is `||L_T||<=T||A||/2`. On a time interval below the explicitly proved connected Dyson radius, the relevant positive support sum may be certifiable. This retains a finite resolution and residual; their removal would still require the missing actual spectral information. The advisor alone selects a contract after S1 review.
