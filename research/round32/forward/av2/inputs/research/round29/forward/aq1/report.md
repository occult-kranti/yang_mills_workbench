# AQ1 forward: HNM numerical-cap thermodynamic construction

Human project author: **Hruday N M (BUNZEEY)**. Independent forward execution of the frozen AQ1 contract, without current reverse or skeptic work. The compactness/dynamics/GNS/Fourier strategy has direct prior overlap with Gauvin arXiv:2503.15539v3 Supplement A.10. The dynamics theorem is Nachtergaele–Sims arXiv:1410.8174v1 Section3/Theorem4.1 (also cross-checked by the source panel against NSY). This is a model-specific SU(2) application, not invention of that strategy; scientific priority is unverified.

**Result:** at either sign of `|tau|<=10^-8`, centered complete-factor whole-star boxes have a subsequence defining a locally normal stationary state on the full coarse Z³ algebra. Its GNS evolution is strongly continuous, with a nonnegative self-adjoint physical energy generator and an invariant physical cyclic restriction. No tau_* or HTW smallness is used. Whole-sequence convergence, state uniqueness, translation invariance and a physical spectral gap are not claimed in this loop.

## 1. Actual full-lattice factor model

For any integer fine coordinates, set `pi(x,y,z)=(floor(x/4),floor(y/2),z)`. Euclidean division, including negative x,y, gives unique residues `r=0..3,s=0..1`. Each coarse factor owns the three positive links at its eight tail vertices, giving 24 untruncated SU(2) Haar factors. Its ten selected-strip links and fourteen free links are unchanged. The same selected coefficient triple, within the inherited ranges, repeats at every coarse site. All original endpoint gauge actions are retained, including heads outside tail blocks.

For Lambda_N=[-N,N]³, the normalized finite operator is

`Hhat_N=sum_(b in Lambda_N)h_b + sum_(b+S subset Lambda_N)phi_b`,

where `h_b>=I-P_b`, P_b is the actual selected-reference vacuum projection, `S={0,e_x,e_y,e_z}`, and `||phi_b||=M=7|tau|`. The raw physical operator differs from delta Hhat_N by the selected ground scalar, with delta=alpha/8. Actual centered physical energy is `K_N=delta(Hhat_N-Ehat_N)`. AM2 supplies the finite full-Hilbert construction at the numerical cap, but a finite gap by itself is not the state construction below.

## 2. Reset energy and trace-norm compactness

Let F be any fixed finite complete-factor region contained in Lambda_N. Reset the ground density on F to `P_F=tensor_(b in F)P_b`, keeping its exterior marginal. The mixed trial state has finite reference form energy; nonnegative spectral truncations justify cancellation of unchanged unbounded exterior energy. Every incident retained star changes its expectation by at most 2M. Its anchor lies in F-S, whose size is at most 4|F|. The ground variational principle therefore gives

\[
\operatorname{Tr}(\rho_{N,F}h_F)\le2M N_{F,N}\le8M|F|=56|\tau||F|=:C_F,
\quad h_F=\sum_{b\in F}h_b.\tag{HNM-AQ1.1}
\]

All incoming stars are included. This is actual selected-reference energy, not an assumed Haar/pure-electric energy bound. At tau=0 it forces the product reference locally.

Each h_b is a compact-manifold elliptic Casimir sum plus bounded selected potential and its actual ground shift, hence has compact resolvent. So does the finite tensor sum h_F. Its spectral projection Q_(F,L)=1_[0,L](h_F) is finite rank. For L>0,

\[
\operatorname{Tr}\rho_{N,F}(I-Q_{F,L})\le C_F/L,\qquad
\|\rho_{N,F}-Q_{F,L}\rho_{N,F}Q_{F,L}\|_1\le2\sqrt{C_F/L}.\tag{HNM-AQ1.2}
\]

The second inequality follows by purifying the density, bounding the projected rank-one difference by 2sqrt(tail), and contracting under partial trace. For fixed L the compressed positive trace-at-most-one matrices form a compact finite-dimensional set. Equation(HNM-AQ1.2) makes the full family trace-norm precompact.

Diagonal extraction over the countable nested coarse cubes produces a subsequence N_k whose densities converge in trace norm on every finite F. Limits are positive and trace one. Partial-trace contractivity passes compatibility. Thus `omega_num(A)=Tr rho_F A` defines a normalized positive functional on the full local algebra and extends by norm continuity to its C*-closure. Every local restriction is normal. No compactness of an extensive global density, Haar replacement, or uniqueness of the selected subsequence is asserted.

## 3. Exact placement in the unbounded-onsite dynamics theorem

Use the l1 metric on Z³ and `F(r)=(1+r)^-4`. The shell at integer r>=1 contains `4r²+2` sites. Since this is at most `6(r+1)²`, and `sum_(r>=1)(r+1)^-2<=1`,

`||F||<=7`.

In the convolution sum, either d(x,z)>=d(x,y)/2 or d(z,y)>=d(x,y)/2. On that half, the corresponding F factor is at most 16F(d(x,y)); summing both halves gives convolution constant `C<=32||F||<=224`.

Whole stars have l1 diameter two. Each site belongs to four anchor stars. Therefore the actual normalized interaction satisfies

\[
J\le4M=28|\tau|,\qquad
\|\Phi\|_F\le3^4J=81J\le2268|\tau|.\tag{HNM-AQ1.3}
\]

This is a finite interaction norm, not the extensive total norm. The countable lattice, separable onsite Hilbert spaces, self-adjoint unbounded h_b, and bounded self-adjoint finite-range Phi(X) now satisfy Nachtergaele–Sims Section3 and Theorem4.1. Its native restriction `sum_(X subset Lambda)Phi(X)` is exactly the retained whole-star prescription here. The theorem gives, for each bounded local A, the norm limit of its finite evolutions, uniform on compact **normalized** time intervals. It extends to a group of isometric star automorphisms of the quasi-local algebra.

Restore physical time by `u=delta t/hbar`:

\[
\mathcal T_t(A)=\lim_N e^{iu\widehat H_N}A e^{-iu\widehat H_N}
=\lim_N e^{itK_N/\hbar}A e^{-itK_N/\hbar}.\tag{HNM-AQ1.4}
\]

All raw/reference ground scalars cancel in this conjugation. A physical compact time window corresponds to a fixed compact u window. The theorem does **not** assert norm continuity in time for every operator of the full local B(H) algebra. Its proof handles strongly continuous interaction-picture operators; no unjustified norm differentiability is added here.

## 4. Stationarity and separate GNS continuity

Local density convergence extends along the same subsequence to every fixed quasi-local observable by norm approximation. Finite ground invariance and the norm volume limit imply

`omega_num(T_t(A))=omega_num(A)`.

Indeed replace T_t(A) by a fixed finite-region approximation, pass the local state limit, then use the uniform norm errors to compare with each finite-volume invariant expectation. The construction yields well-defined unitaries

`U_t pi(A)Omega=pi(T_t(A))Omega`, with U_t Omega=Omega.

Strong time continuity requires a separate argument. For a fixed finite containing region D, its finite unitary evolution is strong-* continuous on every bounded A. The normal density rho_D makes `omega_num(A* T_t^D(A))` continuous by bounded dominated convergence in its trace-class decomposition. Uniform-on-compact-time norm volume approximation then makes `omega_num(A* T_t(A))` continuous. Consequently

`||(U_t-I)pi(A)Omega||²=2omega_num(A*A)-2Re omega_num(A*T_t(A)) ->0`.

Local cyclic vectors are dense; unitarity extends this to the full GNS Hilbert space. Stone's theorem gives a self-adjoint physical energy H_num such that `U_t=exp(it H_num/hbar)` and H_num Omega=0. There is no implicit reset of the physical clock.

## 5. Nonnegative spectral support

For fixed bounded local A, the finite correlation

`c_(N,A)(t)=omega_N(A* T_t^N(A))=<A Omega_N,e^(itK_N/hbar)A Omega_N>`

has a positive spectral measure supported on [0,infinity). Along the selected subsequence, local state and norm dynamical convergence give its limit `c_A(t)=<pi(A)Omega,e^(itH_num/hbar)pi(A)Omega>`. All correlations are bounded by ||A||².

Take any nonnegative smooth compactly supported energy test f inside (-infinity,0). Its hbar-scaled Fourier transform is integrable. Fourier inversion and dominated convergence pass `int f dnu_(N,A)=0` to the actual Stone spectral measure nu_A. Such tests exhaust the negative half-line. Therefore the negative spectral projection annihilates every local cyclic vector and, by density, is zero. Thus H_num>=0. No finite positive gap is passed in this loop.

Finite ground densities are gauge invariant under every original finite endpoint group, so omega_num is gauge invariant. Each finite evolution takes a bounded local gauge-invariant operator to another such operator, and its norm limit lies in their norm-closed algebra A_phys. Both signs of time preserve A_phys; hence the physical cyclic space `closure(pi(A_phys)Omega)` reduces U_t and H_num. Its restriction is a nonnegative self-adjoint physical generator. Equality with the full joint fixed-vector sector and a nonzero excited physical signal remain for AQ2.

## 6. Controls and limitations

The checker audits negative-coordinate ownership, actual endpoint counts, complete incoming-star incidence, exact shell/convolution estimates and physical units. The densities |e_n><e_n| show how local trace mass can escape without an energy-tightness bound. Inconsistent finite marginals are rejected.

On l2(N), `U(t)e_j=e^(ijt)e_j` is strongly continuous, while `A e_j=e_(2j)` obeys `||U(pi/n)A U(pi/n)*-A||=2` for every n, witnessed by e_n. This preserves the distinction between norm volume convergence and full-B norm time continuity.

The prior strategy credit is explicit. No SU(3) coefficient, old tau_* interval, HTW constant, prior orthant-state identity, whole-sequence limit, translation invariance or boundary uniqueness is imported. The state is a constructed full-lattice subsequential state at a fully numerical coupling cap. Subsequent physical-gap claims require the next reviewed loop.

Reproduce: `python -B research/round29/forward/aq1/check.py --output /absolute/new/output`.
