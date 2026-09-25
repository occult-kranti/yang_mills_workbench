# AQ2 forward: HNM numerical-cap physical gap and Wilson witness

Human project author: **Hruday N M (BUNZEEY)**. This is the independent forward execution of the frozen tenth contract; no current reverse or skeptic solution was read. The compact-group averaging and Fourier gap-passage strategy is explicitly present in Gauvin arXiv:2503.15539v3 Supplement A.10, pp.S7–S8. We apply that established strategy with the actual SU(2) selected-reference dictionary and AM2 constants. Scientific priority is unverified.

**Result:** for the actual AQ1 subsequential state at either sign of `|tau|<=10^-8`, the full original-endpoint gauge-fixed space equals the physical local cyclic completion and reduces the physical generator. Its vacuum is simple and its spectral gap is at least `alpha/16`. Using the separately reviewed **full-Hilbert** AM2 strengthening gives this gap and vacuum simplicity also on the full AQ1 GNS representation. The original xz Wilson has variance at least `61999/250000>1/5` in this same state. There is no identification with the earlier orthant state and no moment or operator-domain assertion for this Wilson vector.

## 1. The actual state, algebra and compact endpoint group

Keep exactly AQ1's chosen subsequence of centered boxes `Lambda_N=[-N,N]^3`, actual whole-star Hamiltonians, complete 24-link factors and locally normal limit `omega_num`. Set `delta=alpha/8`, and let its GNS data be `(pi,H_num_space,Omega)`. AQ1 constructs the strongly continuous time group `U_t=exp(it H_num/hbar)` with `H_num>=0` and `H_num Omega=0`. Every physical scale including `alpha/E_star`, spacing and hbar is fixed.

Let V be the countable set of **all original fine-lattice vertices**, and `G=product_(v in V)SU(2)`, with its compact product topology and product normalized Haar measure. For every original positively stored link `(x,j)`,

`U_(x,j) -> g_x U_(x,j) g_(x+e_j)^(-1)`.

This is the original tail-and-head action. A bounded operator A in a finite complete-factor algebra depends under conjugation on only the finite endpoint set V(F). The representation on its finite link Hilbert space is strongly continuous, so `g -> beta_g(A)` is bounded and strong-star continuous in those endpoint coordinates. This does not imply operator-norm continuity for arbitrary A in B(H_F).

Each such action agrees locally with a gauge transformation supported on finitely many vertices. AQ1 state invariance consequently extends to all G. Define

\[
V_g\pi(A)\Omega=\pi(\beta_g(A))\Omega.\tag{HNM-AQ2.1}
\]

State invariance makes this well-defined and isometric; the inverse action makes it unitary. For local A, normality of the local density gives continuity of `omega_num(A* beta_g(A))` under bounded strong-star convergence. The norm-square identity used in AQ1 then proves strong continuity of V_g on local cyclic vectors, and unitarity extends it by density to the full GNS space. This also proves continuity for the compact product topology, since a local vector needs only finitely many endpoint coordinates. No physical tensor factorization is assumed.

## 2. Haar projection and complete physical density

Strong vector integration defines `P_G xi=int_G V_g xi dg`. Strong continuity makes the orbit of each vector compact and separable; its bounded vector integral exists. Haar invariance and inversion give `P_G^2=P_G=P_G*`, with range the joint fixed-vector space. Finitely supported gauge transformations are dense in G, so their joint fixed space is the same range.

For local A define instead the **ultraweak** operator integral

\[
\mathcal E_F(A)=\int_{SU(2)^{V(F)}}\beta_g(A)\,dg\ \in B(H_F).
\tag{HNM-AQ2.2}
\]

It exists by pairing with trace-class functionals, is contractive and positive, and is invariant under every endpoint action. We do not use a norm-Bochner integral of the full-B operator orbit. To identify its GNS vector, pair with any local cyclic vector `pi(B)Omega`. Both operators lie in a larger finite complete-factor region D. The functional `X -> omega_num(B* X)` is normal on that region, since its density is trace class and B is bounded. It therefore commutes with this ultraweak integral. The scalar equality, followed by density, proves

\[
P_G\pi(A)\Omega=\pi(\mathcal E_F(A))\Omega.\tag{HNM-AQ2.3}
\]

Every local invariant cyclic vector is fixed. Conversely apply P_G to a sequence of local cyclic vectors approaching any fixed vector and use (HNM-AQ2.3). Hence

\[
\mathcal H_{\rm phys}=\overline{\pi(\mathcal A_{\rm loc}^{G})\Omega}
=\{\xi:V_g\xi=\xi\text{ for all }g\in G\}.\tag{HNM-AQ2.4}
\]

This is the full bounded local invariant completion, not only Wilson polynomials or a tensor product of blockwise physical spaces. Shared original vertices act on incoming and outgoing links across factor boundaries.

Every finite Hamiltonian is invariant under its complete original endpoint group. Its evolution commutes with beta_g; the AQ1 norm limit retains that identity. Thus V_g commutes with U_t, as does P_G. The physical space reduces H_num: `P_G D(H_num) subset D(H_num)` and `H_num P_G=P_G H_num` there, by the spectral theorem. Its restriction is self-adjoint and nonnegative.

## 3. Centered spectral measures, including zero

Write the actual raw finite Hamiltonian as Hraw_N, its ground energy as Eraw_N, and

`K_N=Hraw_N-Eraw_N=delta(Hhat_N-Ehat_N)`.

No ground scalar is omitted. Put `m_gap=delta/2=alpha/16`. For any bounded local **gauge-invariant** A, its finite centered vector

`chi_(N,A)=(A-omega_N(A))Omega_N`

is physical, orthogonal to the unique finite vacuum, and has spectral measure supported on `[m_gap,infinity)` by AM2's finite physical theorem. For arbitrary bounded local A the identical support statement uses the **separately reviewed full-Hilbert AM2 strengthening**; it does not follow merely from a physical finite gap.

For either allowed class, let `a_N=omega_N(A)` and `a=omega_num(A)`. Local trace-norm convergence gives `a_N -> a` and

\[
\nu_{N,A}(\mathbb R)=\omega_N(A^*A)-|a_N|^2
\longrightarrow\omega_{\rm num}(A^*A)-|a|^2.\tag{HNM-AQ2.5}
\]

Complex means require the absolute square. The centered correlations are exactly

\[
c_{N,A}(t)=\omega_N(A^*\mathcal T_t^N(A))-|a_N|^2
\longrightarrow c_A(t)=\omega_{\rm num}(A^*\mathcal T_t(A))-|a|^2.
\tag{HNM-AQ2.6}
\]

The convergence follows along the actual AQ1 subsequence by a fixed finite-region dynamical approximation and local trace-norm convergence, uniformly on compact times. The limiting function is the actual Stone spectral correlation of `chi_A=(pi(A)-a)Omega`; it is continuous at zero. All correlations are bounded in magnitude by `||A||^2`. Thus mass and Fourier transforms converge to the same actual spectral measure, without any assumed unbounded moment convergence.

For a nonnegative `f in C_c^infinity((-infinity,m_gap))`, use the physical Fourier pair

`f(E)=int_R fhat_hbar(t) exp(it E/hbar) dt`,

whose inverse-transform coefficient is integrable. Finite support exclusion gives `int f dnu_(N,A)=0`. Dominated convergence in (HNM-AQ2.6) gives `int f dnu_A=0`. Such functions exhaust the entire interval below m_gap, **including neighborhoods of E=0**. Consequently `nu_A((-infinity,m_gap))=0`. Testing only `(0,m_gap)` would leave a spurious centered zero atom undetected.

By (HNM-AQ2.4), the centered local invariant vectors are dense in `H_phys intersect Omega-perp`. Therefore the physical spectral projection below m_gap vanishes on that orthogonal complement. The physical restriction obeys

\[
H_{\rm num,phys}\ge {\alpha\over16}(I-|\Omega\rangle\langle\Omega|)
\quad\text{as a quadratic-form inequality}.\tag{HNM-AQ2.7}
\]

The vacuum is simple there. Applying the same argument to **all** local A with the reviewed full-Hilbert finite gap makes the centered vectors dense in the whole `Omega-perp` and gives (HNM-AQ2.7) on the full GNS space as well. Equivalently, in either space `1_[0,alpha/16)(H)=|Omega><Omega|`. The energy threshold is alpha/16; the corresponding frequency is alpha/(16 hbar).

## 4. Original Wilson cover and seven-star reset

Take the original xz face at the fine origin:

`W=(1/2)Tr(U_(0,x) U_(e_x,z) U_(e_z,x)^(-1) U_(0,z)^(-1))`.

The four distinct stored links belong exactly to the complete factors `R={0,e_z}` under `pi(x,y,z)=(floor(x/4),floor(y/2),z)`. The complete cover contains **48 links and 36 original endpoints**. Each factor has 22 endpoints; their intersection has eight. These shared endpoints forbid replacing the joint gauge action by two unrelated blockwise physical actions.

The full-lattice incident anchors are exactly

`R-S={0,-e_x,-e_y,-e_z,e_z,e_z-e_x,e_z-e_y}`.

There are seven, all retained in every centered box with N>=2. The orthant's two-anchor count is not applicable. Resetting the ground density on R to the **actual selected-reference product** `P_R=P_0 tensor P_(e_z)` changes each incident star expectation by at most `2||phi_b||=14|tau|`. The finite ground variational principle, with unchanged exterior reference energy, gives

\[
\omega_N(h_R)\le98|\tau|.\tag{HNM-AQ2.8}
\]

The reset trial need not be physical: AM2 identifies the full ground. It has finite reference energy; bounded spectral truncation justifies cancellation of the exterior unbounded terms as in AQ1. Passing bounded positive spectral truncations of h_R through local trace-norm convergence and taking their increasing supremum yields the same inequality in the actual AQ1 state.

Since `h_R>=I-P_R`, set `epsilon=1-Tr(rho_R P_R)<=98|tau|`. The pure-reference trace distance satisfies

\[
\|\rho_R-P_R\|_1\le2\sqrt\epsilon\le {1\over500}
\quad(|\tau|\le10^{-8}).\tag{HNM-AQ2.9}
\]

For completeness, decompose rho_R into pure states. The trace distance from each pure state to P_R is `2sqrt(1-overlap)`; convexity and concavity of the square root yield the displayed bound. The numerical inequality uses `98/100000000<1/1000000`.

## 5. Reference integration and interacting variance

Every original z link is one of the fourteen free links in its reference factor. Conditional on all other original links, one z link of this face remains Haar in P_R. Left/right multiplication and inversion preserve its normalized Haar law, so the face product is Haar under this **reference** integration. For SU(2), write a Haar matrix as `q_0 I+i q.sigma` on the unit three-sphere. Symmetry gives mean q_0 zero and second moment `1/4`. Thus

`Tr(P_R W)=0`, `Tr(P_R W^2)=1/4`.

This does not assume that either the selected strip vacuum or the interacting local density is a product Haar state. Boundedness `||W||<=1`, `||W^2||<=1` and (HNM-AQ2.9) give

\[
|\omega_{\rm num}(W)|\le1/500,\qquad
\omega_{\rm num}(W^2)\ge1/4-1/500,
\]
\[
\operatorname{Var}_{\omega_{\rm num}}(W)
\ge{1\over4}-{1\over500}-{1\over250000}
={61999\over250000}>{1\over5}.\tag{HNM-AQ2.10}
\]

The vector `(pi(W)-omega_num(W))Omega` is therefore nonzero, physical and orthogonal to the vacuum in the **same** AQ1 representation. Its bounded-vector spectral measure has positive total mass and is supported on `[alpha/16,infinity)`. No operator-domain or first/second-moment identity is asserted here.

## 6. Scope, controls and stop

The executable checker independently reconstructs the complete link/endpoints, shared gauge vertices, full seven-anchor incidence and rational reset/variance constants. Actual SU(2) matrix fixtures distinguish correct tail/head actions from missing heads. A joint-invariant singlet fixture rejects an independent blockwise fixed-sector substitution. Centered measures with a zero atom reject tests only in the open positive interval; complex and moving-mean controls retain the true finite centering and ground shift. A bounded local density fixture shows why reference Haar moments cannot be assigned directly to the interacting density. Two distinct gapped representations of a direct-sum algebra reject equating a simple vacuum in one representation with uniqueness of all states. These finite diagnostics support the analytic arguments; they do not prove infinite completeness by enumeration.

The Newton-inspired check reconstructs the original graph and limiting premises before synthesizing the conclusion. The Tesla-inspired mechanism check retains the endpoint channels, source/state distinction and fixed physical clock. Neither historical figure is asserted to endorse this result.

Vacuum simplicity here is a property of the chosen GNS representation. It does not establish uniqueness of every thermodynamic ground state, whole-sequence convergence, translation invariance, boundary independence, or identity with the older symbolic-smallness state. No continuum limit or Clay mass-gap solution follows. This is investigation ten: after review, scientific production stops; further goals are advice only.

Reproduce: `python -B research/round29/forward/aq2/check.py --output /absolute/new/output`.
