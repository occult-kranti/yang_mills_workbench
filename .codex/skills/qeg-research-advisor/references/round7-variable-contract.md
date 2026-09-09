# R7 variable and conservation contract

Advisor derivation, 9 September 2026; contract version 1.1. This document defines two new, distinct mathematical models. They are linked by their variational gauge-kinetic coupling and work identity; they are **not** a closed semiclassical Einstein–QED system. Numerical outcomes belong to the separately executed experiment records. The equations below are a calculation contract, not a claim that its simulations have already passed. Version 1.1 makes the finite scalar's canonical rescaling explicit; it changes none of the differential equations.

## 1. What is allowed to vary

| Symbol | Type | What changes | What it cannot establish alone |
|---|---|---|---|
| `N,K` | Ultraviolet regulator labels | Which Landau modes and canonical longitudinal momenta are retained | Physical time evolution or charge running |
| `chi_(N,K)` | Regulator-dependent matching coefficient | A member of a family of finite actions | Renormalized current/stress convergence |
| `mu_RG` | Renormalization scale | The bookkeeping scale of renormalized parameters, with compensated observable dependence | A new spacetime degree of freedom |
| `chi(t)` | Prescribed time-dependent coefficient | A driven kinetic sector and an additional work exchange | Conservation without a support sector |
| `phi(t)` | Dynamical scalar | A new state variable with an equation, energy and stress | A QED ultraviolet completion or observed new particle |
| `f(phi)` | Positive gauge-kinetic function | A specified interaction in a specified action | Permission to retune the coupling after a failed run |

The symbol `mu` in the gravity scaling below is a fixed reference frequency, not `mu_RG`.

### 1.1 Reference subtraction is valid algebra, with an unclosed physical interpretation

For the round-6 exact longitudinal integral, fix a positive target `z_ref` and define, at each finite regulator pair,

`chi_(N,K) = z_ref - 1 + e^2 C_(N,K)(0)`.

Then

`Z_(N,K)(a) = z_ref + e^2 [C_(N,K)(0)-C_(N,K)(a)] >= z_ref`.

The inequality follows from the proved continuous-integral maximum at `a=0`. It does not automatically hold for a finite arbitrary quadrature, and it is not a theorem about a common renormalized quantum current. The finite matching coefficient diverges along the joint cutoff family. A physical interpretation needs one regulated action, a physical charge normalization, the associated common subtraction in current and stress, and estimates on the state-dependent terms. Across this family `N,K` are labels; no `d chi/dt` term arises unless a separate time-dependent prescription is introduced.

Conversely, if a proposed replacement only adds a uniformly bounded amount to the kinetic coefficient, it cannot cancel the established cofinal divergence. For `|a_(N,K)| <= A`, the shifted window contains `[-K+A,K-A]` when `K>A`, so

`C_(N,K)(a_(N,K)) >= C_(N,K-A)(0) -> infinity`.

Thus bounded `f(phi)+chi` cannot produce a uniform positive denominator. A common compact scalar range and continuous f are sufficient for that boundedness. Allowing the scalar state to diverge with the regulator changes the question and does not supply a physical matching condition.

### 1.2 Two different time-dependent substitutions have different work defects

Keep the original finite-mode definitions and replace only `chi` by `chi(t)`. If the old divided Maxwell equation is otherwise left unchanged, the previously defined electromagnetic/mode energy obeys

`W' = x F + (chi'/2) x^2`.

If instead the time-dependent coefficient is derived from a kinetic term in an action, the Maxwell numerator gains `-chi' x`, and the same sector energy obeys

`W' = x F - (chi'/2) x^2`.

These are different equations. Neither supports a claim of a conserved closed system until the driving sector and its energy exchange are specified. The sign cannot be selected after inspecting a plot. The dynamical model below supplies that missing sector explicitly.

## 2. Model F: a finite variational scalar–Maxwell–Bloch extension

### F1. Domain and definitions

Keep the exact finite regulator, fixed `b>0`, fixed canonical nodes `k_i`, positive weights `w_i`, positive masses `M_i`, fixed coupling `e^2>0` and fixed matched `chi_b`. The round-6 certificate applies at `b=10,K=20` to every finite inclusive Landau cutoff and exact positive per-level quadrature weights summing to `2K`. It does not certify rounded arbitrary inputs or a continuum limit.

Use the existing electron-scaled time and electromagnetic variables `s=mt`, `a=e A_z/m`, `x=e E_z/m^2`, `b=|eB|/m^2`, with `e=sqrt(e^2)>0`. A canonical physical scalar `Phi` can be assigned by `phi=e Phi/m`; the natural reduced energy-density unit is `m^4/e^2`. Then `nu=m_Phi/m`, and `f(Phi)=1+(g e Phi/m)^2`. This rescaling derives the scalar kinetic and magnetic energy prefactors below; it does not derive the entire regulated quantum action from a covariant theory. The gravity branch instead uses a Planck-scaled scalar.

For each retained mode set

`p_i=k_i-a`, `h_i=(M_i,0,p_i)`, `omega_i=sqrt(M_i^2+p_i^2)`.

`S=sum_i w_i (r_iz+p_i/omega_i)`.

`C=sum_i w_i M_i^2/(4 omega_i^5)`.

`D=sum_i w_i 5 M_i^2 p_i/(8 omega_i^7)`.

`U=sum_i w_i (h_i dot r_i+omega_i)`.

Choose constant parameters `g` and `nu>=0`, define

`f(phi)=1+g^2 phi^2`, `f_phi=2g^2 phi`, `V(phi)=nu^2 phi^2/2`,

`Z(a,phi)=f(phi)+chi_b-e^2 C(a)`.

The scalar gauge coupling is additional model physics. It is not the regulator-dependent matching coefficient of section 1 and is held fixed under a regulator comparison.

### F2. Complete coupled system

`a'=-x`.

`r_i'=2 h_i cross r_i`.

`phi'=y`.

`y'=-nu^2 phi + (f_phi/2)(x^2-b^2)`.

`Z x'=F(s)-e^2(S+D x^2)-f_phi y x`.

The background magnetic field is held fixed in this homogeneous, nonexpanding reduction. There is no evolving metric or horizon. No external electric source is hidden: `F(s)` is the same explicitly supplied smooth drive used by the finite reference model.

### F3. Variational check

For normalized two-component mode spinors `z_i` with `r_i=z_i^dagger sigma z_i`, use the finite action with Lagrangian

`L = Z(a,phi) a'^2/2 + phi'^2/2 - V(phi) - f(phi)b^2/2`

`    + e^2 sum_i w_i [ i(z_i^dagger z_i' - z_i'^dagger z_i)/2 - z_i^dagger(h_i dot sigma)z_i - omega_i ] - a F(s)`.

The symmetrized Berry term differs from the usual first-order expression by a boundary term. The equations for the mode spinors reproduce Bloch precession. The source sign is fixed: the term is `-a F`, because `a'=-x`.

The identities `C_a=2D`, `Z_a=-2e^2D` and

`partial_a sum_i w_i[-z_i^dagger(h_i dot sigma)z_i-omega_i]=S`

give the Maxwell equation in F2 by the Euler–Lagrange equation for a. The scalar equation is its own Euler–Lagrange equation. This establishes internal consistency of a declared finite hybrid action. It does not derive this action as the complete truncation of covariant quantum QED in an evolving geometry.

### F4. Exact energy/work identity and continuation statement

The full source-free Hamiltonian is

`W = Z x^2/2 + e^2 U + y^2/2 + V(phi) + f(phi)b^2/2`.

Subtract the constant magnetic baseline `b^2/2` when measuring changes:

`Wtilde = Z x^2/2 + e^2 U + y^2/2 + Omega^2 phi^2/2`,

where `Omega^2=nu^2+g^2b^2`.

The complete cancellation can be checked without a solver:

1. Precession gives `(|r_i|^2)'=0` and `U'=xS`.
2. `C'=-2Dx`, so `Z'=f_phi y+2e^2Dx`.
3. `(Zx^2/2+e^2U)'=xF-(f_phi y/2)x^2`.
4. `(y^2/2+Omega^2 phi^2/2)'=(f_phi y/2)x^2`.
5. Therefore `Wtilde'=W'=xF`.

For physical Bloch norms `|r_i|<=1`, every term `h_i dot r_i+omega_i` is nonnegative. If the original finite denominator is globally at least `mu_gap>0`, then `f>=1` retains that lower bound. For the round-6 exact-coefficient family, `mu_gap=3/4` is available.

For continuous drive, epsilon-regularizing the square root at zero energy gives

`sqrt(Wtilde(s)) <= sqrt(Wtilde(0)) + (1/sqrt(2 mu_gap)) integral_0^s |F(u)| du`.

Consequently

`|x(s)| <= sqrt(2 Wtilde(0)/mu_gap) + (1/mu_gap) integral_0^s |F(u)| du`.

Also `|y|<=sqrt(2Wtilde)` and, when `Omega>0`, `|phi|<=sqrt(2Wtilde)/Omega`. The potential a is bounded on any finite interval by integrating `a'=-x`. The finite mode norms remain bounded. Smoothness of the vector field on `Z>=mu_gap` and the standard finite-dimensional ODE continuation criterion then prove a unique global forward solution for this finite model. If `Omega=0`, necessarily `nu=g=0` at fixed b>0; the scalar is decoupled and affine in time, so the same finite-time continuation conclusion holds separately.

This does not bound the current uniformly over regulator removal, prove continuum convergence, or supply quantum directional stress. It is a genuinely stronger finite-model theorem under explicitly changed equations.

### F5. Analytic fixtures and discriminating falsifier

- **Zero source, stationary modes:** set `x=0`, fixed a and `r_i=-h_i/omega_i`. Then `phi''+Omega^2 phi=0` exactly. This fixture tests changing f with a closed analytic scalar trajectory while the electromagnetic vacuum remains stationary.
- **Decoupling:** `g=0` returns the previous driven finite Maxwell–Bloch equations plus an independent oscillator. With matching initial data and source, electromagnetic histories must agree.
- **Degenerate scalar preparation:** `phi(0)=y(0)=0` leaves the scalar identically zero for any g. This must not be counted as evidence that nonzero scalar exchange was tested.
- **Nontrivial exchange:** use a compact smooth drive, nonzero scalar preparation, for example `g=0.05,nu=0.5,b=10,phi(0)=0.2,y(0)=0.1`. These are illustrative reduced-model inputs, not measured physical constants.
- **Wrong-model control:** remove only `-f_phi y x` from the Maxwell numerator, while retaining the scalar equation and all energy terms. The exact defect is then `Wtilde'-xF=f_phi y x^2`. Integrating this nonzero defect must explain the broken energy balance. A test which passes the wrong system with the original zero-defect criterion is invalid.

For numerical checks, compare a primary Bloch system with independent complex spinors on the same finite modes and source. Do not share a copied energy-derivative routine as the only independent evidence. Separately refine time tolerance and momentum quadrature; label any cutoff comparisons as different finite systems. Check source hash, finite diagnostics, mode norms, minimum Z, full sampled histories, and the independently integrated work. Do not clip or project energy or norms.

## 3. Model G: a classical scalar–Maxwell–Einstein conservation bridge

### G1. Covariant action and domain

Use natural units, signature `(-,+,+,+)`, reduced Planck mass `Mpl^2=1/(8 pi G)`, and the curvature convention yielding the Einstein equation `G_mu_nu+Lambda g_mu_nu=Mpl^-2 T_mu_nu`. The action is

`S=integral sqrt(-g) [Mpl^2(R-2Lambda)/2 -(partial phi)^2/2 -V(phi) -f(phi)F_mu_nu F^mu_nu/4] d^4x`.

There is no Dirac field, quantum expectation, pair-production current or quantum counterterm in this benchmark. The use of a scalar gauge-kinetic coupling in anisotropic gravity is established in the literature; our E-and-B extension and variable conventions are derived here. The cited inflation model writes its kinetic function as `f_lit^2`; our f denotes the complete positive multiplier, so these conventions cannot be copied without the square. [Watanabe, Kanno and Soda, equations (1)–(3)](https://arxiv.org/html/0902.2833v2).

Take axial Bianchi I

`ds^2=-dt^2+A(t)^2(dx^2+dy^2)+Cmetric(t)^2 dz^2`

with homogeneous parallel orthonormal E and B along z. Let `Hperp=A_dot/A`, `Hparallel=Cmetric_dot/Cmetric`. There is no spatial boundary or horizon. Initial data specify a homogeneous Cauchy slice with positive scale factors.

The source-free covariant equations are

`nabla_mu(f F^mu_nu)=0`, `nabla_[mu F_nu_rho]=0`,

`Box phi - V_phi - f_phi F_mu_nu F^mu_nu/4=0`.

Their stress is the sum of canonical scalar stress and

`T_EM_mu_nu=f(F_mu_alpha F_nu^alpha -g_mu_nu F^2/4)`.

No current or stress is added after varying the action.

### G2. Dimensionless variables and complete ODEs

Choose fixed frequency `mu>0`. Define

`tau=mu t`, `varphi=phi/Mpl`, `v=dvarphi/dtau`,

`hperp=Hperp/mu`, `hparallel=Hparallel/mu`,

`Ecal=E/(mu Mpl)`, `Bcal=B/(mu Mpl)`,

`lambda=Lambda/mu^2`, `U=V/(mu^2 Mpl^2)=mhat^2 varphi^2/2`,

`f=exp(2c varphi)`, `lA=log A`, `lC=log Cmetric`, `theta=2hperp+hparallel`.

All rho and p below are divided by `mu^2 Mpl^2`:

`rhoEM=f(Ecal^2+Bcal^2)/2`,

`rho=v^2/2+U+rhoEM`,

`pperp=v^2/2-U+rhoEM`, `pparallel=v^2/2-U-rhoEM`.

The complete first-order system is

`lA'=hperp`, `lC'=hparallel`, `varphi'=v`,

`v'=-theta v-mhat^2 varphi-c f(Bcal^2-Ecal^2)`,

`Ecal'=-(2hperp+2cv)Ecal`, `Bcal'=-2hperp Bcal`,

`hperp'=(lambda-pparallel-3hperp^2)/2`,

`hparallel'=lambda-pperp-hperp'-hperp^2-hparallel^2-hperp hparallel`.

The algebraic Hamiltonian constraint is

`Cg=hperp^2+2hperp hparallel-rho-lambda=0`.

For regular initial data with nonnegative rho and lambda, the initial isotropic choice `hperp=hparallel=sqrt((rho+lambda)/3)` satisfies it. An initially isotropic rate is not a claim that anisotropic magnetic/electric stress will keep it isotropic. Do not enforce the constraint by resetting hparallel during evolution: its free propagation is a test.

### G3. Exact exchange and constraint propagation

For any diagonal homogeneous sector define

`Q=rho'+2hperp(rho+pperp)+hparallel(rho+pparallel)`.

The equations give

`Q_EM=(f'/2)(Bcal^2-Ecal^2)=c f v(Bcal^2-Ecal^2)`,

`Q_scalar=-Q_EM`, hence `Q_total=0`.

The previously established geometric identity becomes

`Cg'=-theta Cg-Q_total`.

It follows that constraint-satisfying initial data retain `Cg=0` in exact arithmetic. For arbitrary initial constraint residual, `Cg(tau)=Cg(0) exp[-integral theta]`. This is an exact conservation/constraint statement for Model G, not a result about a substituted QED stress tensor.

### G4. Independent formulation, analytic fixtures and falsifier

With `A(0)=1`, the exact flux laws are

`Bcal=Bcal0 exp(-2lA)`,

`Ecal=f0 Ecal0 exp(-2lA)/f`.

An independent reduced ODE can eliminate both electromagnetic evolution equations using these laws; comparison with the full system detects wrong dilution or scalar-coupling factors. Use a distinct numerical method for that reference when practical.

Analytic fixtures:

- Vacuum de Sitter: `varphi=v=Ecal=Bcal=0`, positive lambda, `hperp=hparallel=sqrt(lambda/3)` constant, and both logarithmic scale factors linear in tau.
- Massless homogeneous scalar: `mhat=lambda=Ecal=Bcal=0`, isotropic `h0=|v0|/sqrt(6)>0`. With `d=1+3h0 tau`, `h=h0/d`, `v=v0/d`, `varphi=varphi0+(v0/(3h0))log d`, and `lA=lC=log(d)/3`.
- Constant coupling `c=0`: both electromagnetic fluxes dilute as `A^-2`, and scalar/gauge direct exchange vanishes.

The wrong-model control deletes only the scalar force `-c f(Bcal^2-Ecal^2)` while retaining the scalar energy and the varying-f Maxwell equation. It has

`Q_wrong=c f v(Bcal^2-Ecal^2)`.

Let `volume=exp(2lA+lC)` and integrate `I'=volume Q_wrong` alongside the state. Then

`volume Cg+I=Cg(0)`

must hold even for that wrong model, while `Cg=0` must fail for a nondegenerate case. This separates physical inconsistency from a numerical integration defect. Cases with zero c, v or electromagnetic invariant at all times cannot discriminate the missing force and must not be the only controls.

The declared numerical domain should include finite arguments, positive finite f, nonnegative mhat and lambda for the selected expanding fixtures, and finite scale factors. Guard exponential overflow explicitly rather than returning nonfinite stresses. f approaching zero is an ill-conditioned gauge sector; the fact that an exponential is formally positive does not certify numerical or quantum weak coupling.

## 4. Why these two models cannot yet be merged into Einstein–QED

Model F has a fixed canonical finite mode list, fixed magnetic b and no covariant directional quantum stress. Model G has a self-consistent homogeneous metric and complete classical stress but no charged quantum matter. Their matching pattern is the common action-derived exchange between a gauge kinetic coefficient and a scalar. Their scalar normalizations, regulators and state contents are different. If the same canonical scalar were later used, the units would relate by `phi=(e Mpl/m)varphi`, and `x=(e mu Mpl/m^2)Ecal`; these unit conversions alone do not identify the selected polynomial and exponential coupling functions or close the missing quantum sector.

The missing interface is still a common causal quantum action or equivalent locally covariant prescription producing all of `Jq,rhoq,pq_perp,pq_parallel` in a stated state and the applicable force Ward identity. A moving geometry changes frequencies, physical momenta, magnetic field and state preparation; differentiating fixed-b flat-space formulas after the fact does not derive those changes.

The reference literature on locally covariant Dirac fields must be read with its sectional restrictions. Its conserved-current result does not license replacing the restricted stress argument by an unrestricted strong-background stress closure. [Zahn, especially section 4](https://arxiv.org/pdf/1210.4031).

## 5. Optional local QED bridge, deliberately not the strong-field replacement

A separate controlled low-energy benchmark can use the leading spinor Euler–Heisenberg local term

`L(E,B)=(E^2-B^2)/2 + kappa[(E^2-B^2)^2+7(E dot B)^2]`,

`kappa=2 alpha^2/(45 m_e^4)`.

For a pure homogeneous magnetic field it gives

`rho=B^2/2-kappa B^4`, `pperp=B^2/2-3kappa B^4`, `pparallel=-rho`,

with `B_dot=-2Hperp B`. Inserting this stress into the same Einstein reduction conserves the homogeneous stress exactly for that truncated local action. One should independently vary the action to check these coefficients before implementation.

Its QED interpretation requires `|eB|/m_e^2 << 1`, slow variation on the electron scale and curvature components small relative to `m_e^2`. The weak-field polynomial is not authorized at `B >> B_QED`, and taking E of order the critical electric field requires treatment of real-time pair creation beyond this local real polynomial. These limitations concern the truncation written here; the full constant-field one-loop effective action has a wider field-amplitude range. [Dunne, sections on the constant-field action and its expansions](https://arxiv.org/pdf/hep-th/0406216).

The optional local branch earns a QED label only in its declared overlap regime. Neither that benchmark nor the scalar addition fills the full in-in current/stress/noise and ultraviolet completion gaps.
