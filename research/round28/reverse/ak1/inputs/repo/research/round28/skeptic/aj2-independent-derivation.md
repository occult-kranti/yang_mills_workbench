# AJ2 independent skeptical derivation

This report was written after the advisor's 67-input preflight and before any current AJ2 producer mathematics was read. The level-set strategy is the shared frozen contract's proposal, not an independently invented premise. All instructions and the seven-loop manuscript/network are snapshotted. The accepted I1/AJ1 local normality, physical completion and centered generator are inherited; no external stability theorem is reproved here.

## 1. Actual observable and complete support

Keep the actual nonsummable homogeneous omitted interaction and selected-strip reference, the specified whole-star positive-orthant limit, fixed positive `alpha,hbar,E_star,a`, and real

`|tau|<tau_* = min(c1(S),1/(2c2(S)))/7`.

The positive source constants remain unevaluated. The selected coefficients remain fixed in their inherited ranges. No numerical coupling interval, alternate boundary state, dyadic state or finite AH model is substituted.

Write `o=(0,0,0)`, `x=(1,0,0)`, `z=(0,0,1)`. The frozen face has ordered links

`(o,x,+), (x,z,+), (z,x,-), (o,z,-)`.

Here a direction label denotes the original positive link with the displayed tail. The path is `o -> x -> x+z -> z -> o`. The first, second and fourth tails belong to coarse owner `o`; the third belongs to owner `z`. The minimal complete coarse-factor region is therefore `R={o,z}`, containing 48 original links, twenty selected-strip links and twenty-eight free links. It has 36 endpoint vertices, including twenty vertices outside its sixteen tail vertices. All endpoint actions are retained. This local observable region is not asserted to be a two-block finite-volume Hamiltonian with a complete retained interaction star.

With actual original link matrices `A=U_x(o), B=U_z(x), C=U_x(z), D=U_z(o)`,

`V= A B C^{-1} D^{-1}`, `W=Tr(V)/2`.

Full left/right endpoint actions telescope to conjugation of `V` at `o`. Thus `W` is in the full bounded local gauge-invariant algebra used in AJ1. Every SU(2) matrix has eigenvalues `exp(+-i theta)`, so `W` is real and lies in `[-1,1]`. Multiplication by it is bounded and self-adjoint. Its essential norm is one because neighborhoods of identity holonomy have positive product Haar measure. No charged open word or independent plaquette coordinate is substituted.

## 2. Every level set is Haar null

The local Hilbert space is the original `L2(SU(2)^48, product Haar)` before imposing the physical completion. Fix every variable except the actual link `A`. For these fixed values, `A -> A B C^{-1}D^{-1}` is right translation by a fixed SU(2) element and preserves normalized Haar measure. Consequently the conditional distribution of `W` with respect to original product Haar is exactly the half-trace distribution of one Haar SU(2) matrix.

Identify SU(2) with the unit sphere `S^3` of quaternions `(w,v)`. Normalized Haar is the rotation-invariant sphere measure. Writing `w=cos(theta)` gives its marginal

`dnu(w)=(2/pi) sqrt(1-w^2) 1_{[-1,1]}(w) dw`.

The factor follows from the sphere element `sin^2(theta) dtheta dOmega_2` and `integral_0^pi sin^2(theta)dtheta=pi/2`. This is an absolutely continuous probability measure. For every real `c`, including zero, both endpoints and values outside `[-1,1]`, `nu({c})=0`. Fubini over the other three actual face links and the 44 spectator link factors proves

`Haar_48({W=c})=0` for every real `c`.

In particular the full local multiplication spectral projection `1_{ {c} }(W)` is the zero operator, or equivalently `ker(W-cI)={0}`. This is a measure statement on the full local space, not an inference from nonconstancy, a finite character cutoff or a sampled group.

## 3. Normality supplies nonzero actual variance

AJ1 supplies a positive trace-class density `rho_R` of trace one representing the actual homogeneous state on this complete factor. Let `m=omega(W)` and `v=omega((W-mI)^2)`. Boundedness gives finite real `m` and finite `v>=0`. By trace cyclicity for a bounded operator and trace-class density,

`v=||(W-mI) rho_R^{1/2}||_HS^2`.

If this were zero, every vector in the range of `rho_R^{1/2}` would lie in `ker(W-mI)={0}`. Hence `rho_R^{1/2}=0`, contradicting trace one. Therefore `v>0` throughout the same inherited symbolic coupling regime. This uses neither faithfulness nor a lower bound on the density. In particular it establishes no uniform numerical variance margin.

In the physical GNS null left ideal, `A=W-mI` has `omega(A*A)=v>0`, so its equivalence class is nonzero. The quotient isometry inherited from AJ1 identifies it with

`chi=(pi(W)-mI)Omega`.

Because `W` is a bounded local physical operator and the identity is physical, `chi` lies in `H_cyc`. Centering gives `<Omega,chi>=0`, and `||chi||^2=v>0`. Thus this same actual physical space has a nonvacuum vector. Normality is not silently upgraded to faithfulness or global trace-class representability.

## 4. Precise imaginary-time conclusion without energy moments

Let `H=H_phys=(alpha/8)G_phys` be AJ1's actual centered nonnegative self-adjoint restriction, with unique zero-energy vacuum and `spec(H) subset {0} union [g,infinity)`, `g=alpha/16`. Its spectral measure on `chi` is

`mu_chi(B)=||1_B(H)chi||^2`.

It is positive and finite, with total mass `v>0`, no vacuum mass, and support in `[g,infinity)`. For every finite real physical imaginary time `t>=0`, bounded spectral calculus defines

`C(t)=<chi,exp(-tH/hbar)chi> = integral_[g,infinity) exp(-tE/hbar) dmu_chi(E)`.

The integrand is strictly positive everywhere on this real spectral interval, while the measure has positive finite mass. Hence

`0<C(t)<=v exp[-alpha t/(16 hbar)]`, `C(0)=v`.

For example positivity can be proved by choosing a finite `L` with `mu_chi([g,L])>0`; this gives a state-dependent positive bound at that time. It is not a universal lower exponential estimate derived from `g`. The displayed upper bound also implies `C(t)->0` as `t->infinity`. Bounded semigroup calculus and finite spectral mass suffice; neither `chi in D(H)` nor `chi in D(sqrt(H))` is needed. No energy moment or derivative at zero is claimed.

The lower support threshold need not be an atom, an attained lowest overlapping energy or the true gap. The argument does not determine the measure, an observed mass or a real-time magnitude decay law. The connected single-observable expression equals the displayed centered quadratic form; an uncentered vector would retain its vacuum component.

## 5. Controls and why stronger assertions fail

All controls below concern analytic implications or explicit alternative normal states. They are not alternative evaluations of the actual I1 ground state.

* A constant multiplier `f=3/7` has zero variance in every state. A nonconstant step multiplier `f=1_[0,1]` on `L2([-1,1],dx/2)` also has zero variance in the normal rank-one state of the normalized vector `sqrt(2) 1_[0,1]`. Its level set of value one has positive measure. Nonconstancy alone does not prove the level-set premise.
* The rank-one state of the constant Haar vector on the actual local configuration space is normal but not faithful on its full bounded operator algebra. It nonetheless has positive Wilson variance. A projection onto any orthogonal vector has expectation zero, so no faithfulness assertion is available.
* Normalized vectors supported in `0<W<a`, `0<a<1`, define normal rank-one states because this band has strictly positive Haar measure. The proved level-set lemma gives positive variance, while `Var(W)<=E[(W-a/2)^2]<=a^2/4`. As `a` decreases these positive variances can be arbitrarily small. This disproves a uniform variance floor over all normal states, not a model-specific bound that might require new estimates.
* Normalized vectors supported in `|W|<1/n` give normal states with `omega_n(W^2)<=1/n^2`. Any weak-star cluster state on the full bounded algebra has zero Wilson variance at level zero. It must be singular by the normality argument above. No ordinary pointwise limit on every bounded operator is asserted. Thus absence of multiplication eigenvectors alone does not rule out singular-state concentration.
* Haar reference moments are `E(W)=0`, `E(W^2)=1/4`, `E(W^4)=1/8`, by fundamental character orthogonality/fusion or the marginal integral. The actual `tau=0` selected reference also has these particular moments because the original z-link at `x` is a free Haar factor and conditional integration there makes the holonomy Haar. At nonzero coupling this conditional state factorization is not inherited. The normal pure state with configuration density `1+kappa W`, `|kappa|<=1`, instead has mean `kappa/4`, second moment `1/4` and variance `1/4-kappa^2/16`; `kappa=1` gives `3/16`. Therefore local normality and the Haar level-set property do not assign interacting Haar variance.
* In the abstract two-level energy model `H=diag(0,2g)`, take `Omega=e0` and `W=[[1/2,1/4],[1/4,0]]`, a bounded self-adjoint operator of norm below one. Its raw vector has squared vacuum component `1/4`; its centered vector has norm squared `1/16`. At `t=hbar log(2)/g`, the centered correlation is `1/64`, while the raw one is `17/64` and violates the claimed gap decay for its full norm. This is an exact centering control, not a physical Hamiltonian truncation.
* A vacuum-only reducing physical restriction can satisfy the same exclusion while every centered physical vector is zero. AJ2 removes that logical possibility here only through the actual `v>0` proof.
* Spectral mass one concentrated at `E=2g` gives correlation `1/4` at `t=hbar log(2)/g`, below the proposed lower decay factor `1/2`. It also has no atom at `g`, and its real-time correlation has constant modulus one. The gap yields an upper imaginary-time ceiling, not these stronger claims.
* On an abstract vacuum-plus-ell2 space, let `H e_n=g n^2 e_n` and `chi_n=1/(2n)`. Then `||chi||^2<1/2`, but the form energy diverges. The bounded self-adjoint operator `|chi><Omega|+|Omega><chi|` creates it from the vacuum and has norm below one. Its exact finite prefixes test the divergence; the analytic series proves failure of the general bounded-local-domain implication. This does not assert the actual Wilson vector is outside either domain.

The checker uses only the prescribed face, complete two-site geometry, rational quaternion covariance and targeted exact diagnostics. Fundamental tensor fusion is a reference moment check, not an interacting-state computation or a discretized Haar proof. No nondiscriminating candidate or failed scientific run has been concealed; any later development correction must be recorded separately.

## 6. Scope and contribution

This is a qualitative nonvacuity consequence of AJ1's local normality for one explicitly fixed non-atomic Wilson multiplication observable, plus its bounded-semigroup spectral consequence. The level-set argument is an elementary conditional Haar calculation; the trace-class and spectral-measure implications are standard functional analysis applied to this source-bound model. No priority comparison or new general theorem is claimed.

No quantitative variance margin, energy moment, evaluated stability radius, threshold eigenvalue, mass measurement, alternative boundary identification, global faithfulness, Wilson-only algebra completion, lattice-spacing limit, physical model matching or continuum Yang-Mills result is established. The fifth goal pair remains unselected. This report executes AJ2 only.
