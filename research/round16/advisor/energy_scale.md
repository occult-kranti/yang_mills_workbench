# Common physical energy: an exact conditional bridge and counterexample

Let K_N be a self-adjoint physical Hamiltonian on its declared gauge-invariant domain and H_N=α_N K_N with α_N>0. Positive scalar multiplication rescales the spectrum: spec(H_N)=α_N spec(K_N). Ground and first excitation therefore satisfy Δ(H_N)=α_N Δ(K_N), with the same statement for an isolated ground and the infimum of its complementary spectrum. No finite matrix truncation is needed.

Consequently, the TWO premises inf_N Δ(K_N)>=d>0 and inf_N α_N>=α_min>0 imply inf_N Δ(H_N)>=α_min d. A physical lower bound cannot be inferred merely by assigning the same dimensionless coupling ratio to every volume.

The exact counterexample uses open cubic vertex boxes n>=2, SU(2), and Gauss law at every vertex with no external charges. At zero magnetic coupling every nonconstant physical spin network has a support containing a cycle. The shortest cycle uses four edges, each nontrivial Casimir is at least3/4, and a fundamental plaquette loop attains3. Thus the dimensionless electric gap is exactly3 for every box. Set α_n=1/n in a fixed energy unit: the physical gaps3/n tend to zero even though all dimensionless coupling ratios are identically zero. This is an analytic sequence proof; the CSV samples illustrate it and are not its justification.

The common-scale condition is necessary for an inference from a common LOWER dimensionless bound alone. It is not a universal theorem that every uniformly gapped family must have inf α_N>0: a dimensionless gap that grows fast enough could compensate a decreasing prefactor. Such compensation is absent in the exact free-box counterexample, whose dimensionless gap stays3. This qualifier prevents the new roadmap from overstating its own necessary condition.

At fixed α=1 the free gaps remain3. In the interacting norm estimate, P(n)=3n(n−1)^2 and Δ>=α[3−P(n)|λ/α|]. Its negative values at fixed nonzero ratio mean this sufficient estimate is inconclusive; they do not prove the interacting gap vanishes. A volume-independent local bound and matched boundary/Gauss assumptions are still missing. κ_f in the Euclidean cube measure is not λ_f/α without a separately derived state/time-generator relation.

`energy_scale.py` uses exact rationals, rejects nonpositive scales and Boolean/float substitutions, preserves negative sufficient bounds, and records the actual energy convention. No guessed running function has been added to the Yang–Mills action.
