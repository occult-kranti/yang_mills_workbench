# AT4 independent reconstruction before producer comparison

Written and tested after the first contract freeze and before reading either current producer report or source.

Let r=alpha*t/hbar, V/alpha be the dimensionless magnetic interaction, R={0,e_z}, and d=2 sqrt(98|tau|). In the zero-selected subfamily the onsite vacuum is Haar, h_R>=I-P_R, and the inherited reset bound yields ||rho_R-P_R||_1<=d. The reference dynamics preserve R for all r. The exact Haar Wilson correlation is c_0(r)=exp(3ir)/4, since each of the four distinct fundamental link occurrences contributes Casimir 3/4 and W has Haar squared norm 1/4.

In a finite complete box, interaction-picture bounded perturbation theory gives a strong Duhamel integral for the difference of full and onsite evolution of bounded W. It is unnecessary to assume norm differentiability of arbitrary B(H) observables under the unbounded onsite generator: its conjugation is strong-* continuous, the commutator with the finite bounded V is strong continuous, and the integral is strongly defined. Differentiation can first be justified weakly for vectors in a common core, or through the bounded interaction-picture propagator. The finite-volume generator is a bounded perturbation of the onsite self-adjoint operator, so this propagator exists. Its unitary outer conjugations preserve operator norm. Only seven whole stars meet the support of the freely evolved W. Each has physical norm/alpha at most 7|tau|/8. Hence

||T_r(W)-T^0_r(W)|| <= min(2, (49|tau|/4)|r|).

The support remains the complete two-factor R because onsite evolution is a tensor product; it is not necessary for its individual free-link factors to remain Wilson multipliers. The bound is independent of box size. The inherited actual norm thermodynamic limit for local observables passes it to the AQ dynamics at every fixed real r.

Write m=omega_tau(W), with |m|<=d because the reference mean vanishes. For c_tau(r)=omega_tau(W T_r(W))-m², insert T^0_r and compare the local density on R. Since ||W T^0_r(W)||<=1,

|c_tau(r)-c_0(r)| <= d+d²+min(2,(49|tau|/4)|r|).

This is a sufficient upper estimate only. No lower bound on the true interaction correction is implied by any of these positive allowances.

Both ground-centered spectral generators are nonnegative. Against the finite positive spectral measures the Cauchy/Poisson Fourier identity gives

C_tau(s)=integral_R [s/(pi(s²+r²))] c_tau(r) dr,

and likewise C_0(s)=exp(-3s)/4. Bounded correlations justify scalar Fubini. The constant error integrates with mass one. On |r|<=L, charge the dynamical bound by (49|tau|/4)L. On the complement charge it by 2; the kernel tail is at most 2s/(pi L). Using pi>3 gives the fully rational sufficient budget

|C_tau(s)-C_0(s)| <= d+d²+(49|tau|/4)L+4s/(3L).

This is intentionally conservative; integrating the interior linear bound exactly can sharpen it, but no such sharpening is needed to discriminate the frozen target. At s=1,L=10000,tau=10^-8, the state allowance alone is approximately 0.001980, so this sufficient budget cannot certify radius 10^-6. Directed rational brackets for d and exp(-3) yield a rigorous broad actual-state interval in the independent checker. This is a real interacting-state analytic envelope, not a finite solver result, and it does not solve the cap-level requested accuracy.

For the abstract equal-moment controls, y=exp(-1) gives C_B(1)-C_A(1)=y(1-y)^4/32. Any deterministic point output from their common moments has worst-case error at least half this gap, by the triangle inequality. The simple rigorously enclosed range 1/3<y<3/8 gives half-gap >625/786432>10^-6. This proves an insufficiency of those moments as data over the abstract admissible measure class, without asserting that both measures are AQ states.

Vector centering with W-mhat produces C(s)+(m-mhat)² because cross terms with the centered vacuum-orthogonal vector vanish. Subtracting mhat² from an uncentered scalar produces C(s)+m²-mhat². The first residue is nonnegative and quadratic in mean error; the second can have either sign and is generally linear in the error. For mhat=-m the latter cancels while the former is 4m². Correcting one protocol by the other's formula is invalid.

Independent executable: `python -B research/round31/skeptic/at4_check.py --output /absolute/new/output`. Normal and optimized Python give identical output bytes and 31 explicit checks; none depend on Python assert statements. This independent reconstruction uses the shared contract and inherited method premises, not independent empirical evidence.
