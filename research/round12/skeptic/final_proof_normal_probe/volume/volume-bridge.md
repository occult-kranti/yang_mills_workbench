# Finite-graph gaps, volume uniformity, and the continuum bridge

The two-square Hamiltonian has a genuine positive physical gap at every fixed finite coupling. Its global heat-kernel proof does not produce a useful lower bound uniform in a growing graph. The statements below quantify that loss, exhibit a pure-gauge tensor counterbenchmark where the actual gap stays positive, and identify additional hypotheses needed to connect lattice results to a continuum mass gap. They make no mathematical novelty claim and no claim to solve the four-dimensional Yang–Mills problem.

The existing two-square graph has **two spatial dimensions and continuous time**. Its natural spacetime interpretation is a finite regulator in \(2+1\) dimensions. Increasing its polynomial cutoff improves a Hilbert-space approximation; that operation neither adds spatial cells nor changes the physical dimension.

## 1. Variables and three different gaps

Use \(\hbar=c=1\), with physical time calibration an explicit assumption where continuum comparisons are made.

| Symbol | Meaning | Units or limit |
|---|---|---|
| \(d_s\) | Spatial lattice directions | Existing graph: 2; four-dimensional target: 3 |
| \(D=d_s+1\) | Euclidean spacetime dimension of the corresponding relativistic target | Distinct from stochastic time |
| \(N_c\) | Color parameter in \(SU(N_c)\) or \(SO(N_c)\) | Hamiltonian here: \(SU(2)\) |
| \(n\) | Cells per side of an open box | Vertices per side: \(n+1\) |
| \(a,L=na\) | Spatial spacing and physical side length | Length |
| \(E,P\) | Independent oriented links and geometric plaquettes | Finite integers |
| \(\alpha,\lambda_p\) | Electric and magnetic Hamiltonian coefficients | Energy |
| \(\kappa_p=\lambda_p/\alpha\) | Magnetic/electric ratio | Dimensionless |
| \(\Delta_{a,n}\) | First Hamiltonian gap after local Gauss constraints | Energy |
| \(\delta_{a,n}=a\Delta_{a,n}\) | Same gap in spatial lattice units | Dimensionless |
| \(m_{\rm phys}\) | Continuum physical mass gap, if reconstructed | Inverse length |
| \(c_{\rm lat}\) | Exponential rate per Euclidean lattice step | Dimensionless |
| \(K_S\) | Poincaré lower bound for a specified Langevin generator | Inverse stochastic time in its normalization |

Never use the same \(N\) for color and box side. Shen–Zhu–Zhu call their color parameter \(N\), lattice side \(L\), and Euclidean dimension \(d\). Here those become \(N_c,n,D\).

A stochastic-time gap controls relaxation of an auxiliary Markov process to a Gibbs measure. Euclidean exponential clustering controls separation in the original lattice coordinates. A Hamiltonian gap controls physical time evolution in the physical Hilbert space. The last two can be connected through a suitable positive transfer operator or Osterwalder–Schrader reconstruction; the first does not supply that identification by notation alone.

## 2. Finite-graph assumptions and volume loss

**A1. Graph.** \(\Gamma=(V,E)\) is a finite, connected, simple subgraph of an open hypercubic spatial lattice, with at least one complete elementary square. Every magnetic plaquette is such a square. There are no periodic identifications, parallel edges, loop edges, external charges, or relaxed boundary Gauss laws.

**A2. Physical realization.** Start from \(L^2(SU(2)^E,d\mu)\), with normalized product Haar measure, and impose invariance under the independent gauge transformation at every vertex. The link Casimir is \(C_e=-\sum_{a=1}^3(L_e^a)^2\) for \(T_a=\sigma_a/2\), with spin-\(j\) eigenvalue \(j(j+1)\). Operators use the inherited compact-group domain.

**A3. Hamiltonian.**

\[
H_\Gamma=\alpha K_\Gamma+V_\Gamma,\qquad
K_\Gamma=\sum_e C_e,\qquad
V_\Gamma=\sum_p\lambda_p(1-x_p),\quad
x_p=\tfrac12\operatorname{Tr}U_p,\quad
\alpha>0,\ \lambda_p\ge0.
\tag{2.1}
\]

The bounded gauge-invariant potential preserves compact resolvent. Positivity improvement of the full compact-group Schrödinger semigroup gives a unique positive ground state; gauge symmetry makes it physical. This retains the original pure-gauge theory. No scalar field or tunable mass term is introduced.

### Theorem V1. The free physical gap is exactly \(3\alpha\)

Under A1–A3 with all \(\lambda_p=0\), the ground state is constant and the first physical excitation has energy \(3\alpha\).

**Proof.** Peter–Weyl expansion and vertex invariant projection give a complete spin-network basis with electric eigenvalue \(\sum_e j_e(j_e+1)\). In the support of nonzero spins, no vertex has degree one: a single nontrivial irreducible representation has no invariant vector. Any nonempty finite support without degree-one vertices contains a cycle. A simple open hypercubic graph has no cycles shorter than four. Thus at least four nontrivial edges contribute at least \(4(3/4)=3\). A fundamental Wilson trace around an elementary square is physical, orthogonal to constants, and attains exactly 3. QED.

The full kinematical gap is \(3\alpha/4\), not \(3\alpha\). A tree has only constant charge-free physical functions and is excluded rather than assigned a nonexistent first excitation.

### Theorem V2. Explicit global comparison bound

Under A1–A3,

\[
\boxed{\Delta_\Gamma\ge
3\alpha\left(\frac35\right)^{2E}
\exp\left[-16\sum_p\frac{\lambda_p}{\alpha}\right].}
\tag{2.2}
\]

**Proof.** Divide \(H\) by \(\alpha\); write \(W=V/\alpha\), \(S_\kappa=\sum_p\kappa_p\). Then \(0\le W\le2S_\kappa\). The one-link normalized heat kernel obeys

\[
p_4(g)=1+\sum_{r\ge1}(r+1)e^{-r(r+2)}\chi_{r/2}(g),
\qquad
|p_4(g)-1|\le\sum_{r\ge1}(r+1)^2e^{-r(r+2)}<\frac14.
\tag{2.3}
\]

The first summand is \(4e^{-3}<1/5\). For \(r\ge2\), use \((r+1)^2\le4^r\), \(r(r+2)\ge4r\), and \(e^4>50\). The tail is at most \(\sum_{r\ge2}(2/25)^r=4/575\). Their sum is below \(1/4\); the exponential inequalities follow from finite positive Taylor lower sums.

The product kernel of \(e^{-4K_\Gamma}\) is between \(m=(3/4)^E\) and \(M=(5/4)^E\). Feynman–Kac yields pointwise kernel inequalities

\[
e^{-8S_\kappa}e^{-4K_\Gamma}
\le e^{-4(K_\Gamma+W)}\le e^{-4K_\Gamma}.
\tag{2.4}
\]

Apply these to the positive ground state \(\phi\). Cancel its common eigenvalue factor and integral to obtain

\[
R:=\frac{\sup\phi}{\inf\phi}
\le(5/3)^E e^{8S_\kappa}.
\tag{2.5}
\]

Normalize \(\phi\) in \(L^2(\mu)\) and set \(d\nu=\phi^2d\mu\). The exact ground-state transform is

\[
\langle\phi f,(K_\Gamma+W-e_0)\phi f\rangle
=\int\Gamma_K(f)d\nu.
\tag{2.6}
\]

For physical \(f\), V1 and comparison of variances give

\[
\operatorname{Var}_\nu f
=\inf_c\int|f-c|^2\phi^2d\mu
\le(\sup\phi)^2\operatorname{Var}_\mu f
\le\frac{R^2}{3}\int\Gamma_K(f)d\nu.
\tag{2.7}
\]

Using an infimum over constants correctly handles the different means of the measures. Thus \(\Delta_\Gamma/\alpha\ge3/R^2\), proving (2.2). QED.

For an open \(n^{d_s}\)-cell box,

\[
E=d_s n(n+1)^{d_s-1},\qquad
P=\binom{d_s}{2}n^2(n+1)^{d_s-2}.
\tag{2.8}
\]

At fixed equal \(\kappa\), the logarithm of (2.2), divided by \(3\alpha\), is

\[
-2E\log(5/3)-16\kappa P=-\Theta(n^{d_s}).
\tag{2.9}
\]

The losses are a product of pointwise heat-kernel extrema and an extensive potential-oscillation bound. Gauge reduction can improve constants, as in the two-square proof, but this full-link comparison does not retain locality.

At \(\kappa=0\), V1 is exact while (2.2) deteriorates. Even the heat-kernel factor alone loses information. V2 concerns this specified estimate, not every possible heat-kernel method or an optimized time-dependent argument.

## 3. Exact tensor counterbenchmarks

### Theorem V3. Collapse of a lower bound does not imply gap closure

Let \(h\) be an exact finite-graph physical Hamiltonian with simple ground energy \(e_0\), compact resolvent, and gap \(\Delta>0\). On \(q\) independent copies set

\[
H^{(q)}=\sum_{i=1}^q
I^{\otimes(i-1)}\otimes h\otimes I^{\otimes(q-i)}.
\tag{3.1}
\]

Then \(E_0^{(q)}=qe_0\) and \(\Delta^{(q)}=\Delta\) for every finite \(q\).

**Proof.** Tensor products of one-copy eigenvectors form a complete eigenbasis. Any excited tensor contains at least one excitation costing \(\Delta\) or more. Exactly one first excitation attains that cost. QED.

For \(q\) copies of the exact round-11 two-square block, write \(s=\kappa_1+\kappa_2\). The existing time-\(4/3\) comparison has one-block heat bounds \(9/16,25/16\). Applied globally it gives

\[
B_q=3\alpha(9/25)^{2q}e^{-16qs/3}\longrightarrow0,
\qquad \Delta^{(q)}=\Delta^{(1)}>0.
\tag{3.2}
\]

At \(q=1\), \(3(9/25)^2=243/625\), recovering the existing bound. Applying the one-block bound first and then V3 instead retains a bound independent of \(q\). This isolates the loss from applying the global density comparison after tensorization.

There is an even sharper diagnosis. At positive magnetic coupling the one-copy ground state is nonconstant, since applying its Hamiltonian to a constant gives a nonconstant potential. Write its exact extremal ratio as \(R_1>1\). The product ground state has exact ratio \(R_q=R_1^q\), so even using that exact ratio in the global Haar comparison gives only \(3\alpha R_1^{-2q}\to0\). The loss is already present in the global maximum/minimum comparison, independently of heat-kernel approximation errors.

This is a **disconnected pure-gauge counterbenchmark**, not a theorem for interacting adjacent cells in a growing connected lattice. It refutes only \(B_q\to0\Rightarrow\Delta_q\to0\). It does not justify replacing shared-link terms by independent rotors.

### One-square benchmark with an analytic uniform floor

The physical one-square space is the class-function sector of \(L^2(SU(2))\). With \(x=\operatorname{Tr}U/2\),

\[
h/\alpha=4C+\kappa(1-x),\qquad
4Cf=-(1-x^2)f''+3xf'.
\tag{3.3}
\]

The orthonormal characters \(\chi_{r/2}\), \(r=0,1,\ldots\), give the exact infinite Jacobi matrix

\[
(h/\alpha)_{rr}=r(r+2)+\kappa,\qquad
(h/\alpha)_{r,r+1}=(h/\alpha)_{r+1,r}=-\kappa/2,
\tag{3.4}
\]

because \(2x\chi_{r/2}=\chi_{(r+1)/2}+\chi_{(r-1)/2}\), with the negative-index character zero. Min–max and the constant trial state prove \(\Delta/\alpha\ge3-\kappa\). At \(\kappa=1/2\), the analytic tensor-independent floor is therefore \(2.5\), without numerical assumptions.

The computation gives \(\Delta/\alpha\approx3.0289863271\). Reduced one-square heat time one gives instead the global bound

\[
B_q^{\rm sq}=3\alpha(3/5)^{2q}e^{-4q\kappa}.
\tag{3.5}
\]

At \(q=32,\kappa=1/2\), this is of order \(10^{-42}\alpha\), while the analytic floor stays \(2.5\alpha\). The approximate eigenvalue is not interval-certified; the proof of a uniform positive gap in this benchmark is analytic.

## 4. Primary strong-coupling results and the measure distinction

**External theorem S1 — Shen, Zhu, Zhu.** For unit-spacing \(\mathbb Z^D\), their action is \(S=N_c\beta\operatorname{Re}\sum_p\operatorname{Tr}U_p\). For \(SU(N_c)\),

\[
|\beta|<\frac1{16(D-1)},\qquad
K_S=\frac{N_c}{2}-8N_c|\beta|(D-1)>0.
\tag{4.1}
\]

Theorems 1.2 and 1.4 give a unique infinite-volume invariant measure, convergence from finite volumes, and volume-independent inequalities in their Hilbert–Schmidt metric

\[
\operatorname{Ent}_\mu(F^2)\le\frac2{K_S}\sum_e\mu(|\nabla_eF|^2),
\qquad
\operatorname{Var}_\mu F\le\frac1{K_S}\sum_e\mu(|\nabla_eF|^2).
\tag{4.2}
\]

Corollary 1.6 separately proves exponential Euclidean covariance decay for smooth cylinder functions with disjoint supports, including Wilson-loop observables. Its positive rate depends on \(K_S,N_c,D\), and prefactors on supports and observable norms. Sections 4.1 and 4.3 use local Hessian and derivative-commutator estimates. The stochastic gap \(K_S\) is not identified with that correlation rate. For \(SO(N_c)\), the threshold is \((N_c-2)/[32(D-1)N_c]\).[^1]

In the \(D=4,SU(2)\) specialization, \(|\beta|<1/48\) and \(K_S=1-48|\beta|\). These are fixed-spacing strong-coupling results, not the positive continuum Hamiltonian gap below.

The contrast between local and global estimates is elementary. A plaquette touches four links; a link belongs to at most \(2(D-1)\) plaquettes. A quadratic-form estimate that bounds each interaction by a sum over its incident links counts each link only \(2(D-1)\) times after summation. It can depend on degree instead of total plaquette count. Its applicability still depends on the **actual measure and generator** being studied.

### Theorem V4. Wilson Gibbs density is not the interacting quantum ground-state density

For (3.3), no normalized \(\phi_\theta(x)\propto e^{\theta x}\), with real \(\theta\), is an eigenfunction unless \(\kappa=\theta=0\).

**Proof.**

\[
\frac{(4C+\kappa(1-x))e^{\theta x}}{e^{\theta x}}
=\kappa-\theta^2+(3\theta-\kappa)x+\theta^2x^2.
\tag{4.3}
\]

An eigenfunction requires a constant right side on \((-1,1)\). Its quadratic coefficient forces \(\theta=0\), and its linear coefficient then forces \(\kappa=0\). QED.

The square root of an exponential Wilson Gibbs density has exactly this form. The minimal one-square test already excludes this measure identification at positive coupling; no large-volume issue is required. More generally, for \(K=-\Delta\) and \(\phi=e^{S/2}\), the equation \((K+W)\phi=e_0\phi\) requires

\[
W-e_0=\tfrac12\Delta S+\tfrac14|\nabla S|^2.
\tag{4.4}
\]

A plaquette sum \(S\) produces derivative-square interactions in (4.4). Omitting them does not give a unitarily equivalent Hamiltonian. This diagnoses the missing equality; it is not a proposal to change the theory.

### Conditional rule V5. A local estimate on the actual ground state would suffice

Add to A1–A3 a volume-independent \(c_*>0\) such that, on the full group product,

\[
\operatorname{Ric}-2\operatorname{Hess}\log\phi_\Gamma
\ge c_*g_{\rm product}
\tag{4.5}
\]

for the **actual** positive ground state, using the Casimir metric. Then \(\Delta_\Gamma\ge\alpha c_*\), including in the physical sector.

Indeed, the ground-state transform has generator \(\mathcal L=\Delta+2\nabla\log\phi\cdot\nabla\). Its iterated carré-du-champ is
\[
\Gamma_2(f)=|\operatorname{Hess}f|^2+
(\operatorname{Ric}-2\operatorname{Hess}\log\phi)(\nabla f,\nabla f).
\]
The resulting gradient estimate and its integral imply the Poincaré bound \(1/c_*\). For this \(SU(2)\) metric, the group is a round three-sphere of radius two, with \(\operatorname{Ric}=g/2\). A sufficient check is that the symmetric block matrix \(\operatorname{Hess}\log\phi\) has block-norm row sums bounded by \(\eta<1/4\), giving \(c_*=1/2-2\eta\).

No such estimate uniform in volume for this interacting ground state is established here. V5 is a sufficient missing hypothesis, not an accomplished extension of S1.

## 5. Spacing, couplings, and both directions of the bridge

Use \(g_H(a)\) for the **declared Hamiltonian convention** matched to Froland–Grabowska–Li, Eq. (1):[^2]

\[
\alpha(a)=\frac{g_H^2(a)}{2a},\qquad
\lambda(a)=\frac2{g_H^2(a)a},\qquad
\kappa(a)=\frac4{g_H^4(a)}.
\tag{5.1}
\]

This coefficient dictionary does not determine the physical spacing, a renormalized running coupling, or a scale-setting observable from two cells.

For \(D=d_s+1\), dimensional consistency of a continuum action proportional to \(g_D^{-2}\int F^2\), with link phase \(aA\), requires \([g_D^2]=\mathrm{mass}^{3-d_s}\). Define the Hamiltonian bare-parameter convention \(g_H^2=a^{3-d_s}g_D^2\). Substitution then gives

\[
[g_D^2]=\mathrm{mass}^{3-d_s},\quad
g_H^2=a^{3-d_s}g_D^2,\quad
\alpha=\tfrac12g_D^2a^{2-d_s},\quad
\lambda=\frac{2a^{d_s-4}}{g_D^2}.
\tag{5.2}
\]

Finite renormalizations and physical time normalization require separate matching. In \(d_s=2\), \(g_D^2\) has mass units and \(g_H^2\sim ag_D^2\); in \(d_s=3\), \(g_D^2\) is dimensionless. A four-dimensional logarithmic running law cannot be applied to the two-spatial-dimensional toy without changing its interpretation.

For a Euclidean convention, write independently

\[
S_W=\beta_W\sum_p\left(1-\frac1{N_c}\operatorname{ReTr}U_p\right).
\tag{5.3}
\]

Comparison with S1 is algebraic: \(\beta_W=N_c^2\beta\). If \(g_E\) is defined by \(\beta_W=2N_c/g_E^2\), then \(\beta=2/(N_cg_E^2)\). Thus S1's \(D=4,SU(2)\) condition reads \(g_E^2>48\). This is a definition of \(g_E\), **not** an identification with \(g_H\).

That distinction matters in transfer matching. With temporal step \(a_t\), the split Hamiltonian kernel is

\[
e^{-a_tV/2}e^{-a_t\alpha K}e^{-a_tV/2}+o(a_t).
\tag{5.4}
\]

Its spatial plaquette coefficient is \(a_t\lambda\), while its temporal link factor is a group heat kernel. Relating it to an isotropic Wilson action requires plaquette counting, trace normalization, anisotropy, and time calibration. A finite-spacing Wilson transfer operator cannot be silently identified with the declared continuous-time Hamiltonian.

**Lattice to continuum.** In a controlled infinite-volume setting, a finite physical mass \(0<m_{\rm phys}<\infty\) would require

\[
\Delta_{a,n(a)}\longrightarrow m_{\rm phys},
\qquad a\Delta_{a,n(a)}\sim am_{\rm phys}\longrightarrow0,
\qquad n(a)a\longrightarrow\infty.
\tag{5.5}
\]

An alternative takes \(a\to0\) at fixed \(L=na\), constructs the finite-volume continuum theory, and then controls \(L\to\infty\). A fixed-\(L\) excitation can contain finite-volume shifts and is not automatically the infinite-volume mass.

A positive continuum gap is therefore compatible with a vanishing dimensionless lattice gap. An \(a\)-independent positive lower bound on \(a\Delta\) would force physical energies to at least order \(1/a\); alone, it would not give a nontrivial finite-mass continuum excitation.

For a covariance \(e^{-c_{\rm lat}r}\), physical separation is \(R=ar\) and the physical decay scale is \(c_{\rm lat}/a\). A finite mass channel needs \(c_{\rm lat}\sim am_{\rm phys}\), together with converging renormalized observables. A correlation length uniformly bounded in lattice units in a strong-coupling region does not alone supply a nontrivial continuum limit.

**Continuum to lattice.** A hypothesized continuum pure-gauge theory supplies a scale and renormalization conditions. Those would select \(g_H(a)\), observable renormalizations, and a box growth schedule. They cannot be extracted merely from positivity on one fixed graph. Conditional on \(g_H(a)\to0\), the exact ratio in (5.1) gives \(\kappa(a)\to\infty\), leaving an electric-dominated small-\(\kappa\) regime. Conditional on \(g_E(a)\to0\), \(\beta(a)\to\infty\), leaving S1's region. These implications do not presume a nonperturbative construction of either trajectory.

The equal-coupling two-square bound translates to

\[
a\Delta\ge\frac{243}{1250}g_H^2
\exp\left[-\frac{128}{3g_H^4}\right].
\tag{5.6}
\]

For a connected box, V2 gives

\[
a\Delta_{a,n}\ge\frac{3g_H^2}{2}(3/5)^{2E(n)}
\exp\left[-\frac{64P(n)}{g_H^4}\right].
\tag{5.7}
\]

At fixed physical side, \(n=L/a\), and \(E,P\) grow as \(a^{-d_s}\). This displayed bound collapses under a weak-coupling refinement. By V3, that is not evidence that the actual physical gap closes. Keeping the two-square topology fixed while \(a\to0\) instead shrinks the physical region and is not fixed-volume refinement.

## 6. Reconstruction and limit rules

The official problem asks for a nontrivial four-dimensional quantum Yang–Mills theory with a positive physical mass gap and sufficiently strong axiomatic properties. Its lattice discussion separates vanishing spacing and infinite volume and emphasizes reflection positivity and construction of the physical Hilbert space. Compactness alone is not the required existence result.[^3]

### Conditional rule V6. Gap survival under controlled operator convergence

Let \(A_j\ge0\) be vacuum-subtracted physical Hamiltonians on a common Hilbert space and \(P_j\) their rank-one vacuum projections. Assume
\[
A_j\ge m_*(I-P_j),\quad m_*>0,\qquad
P_j\to P\ \text{strongly},\quad \operatorname{rank}P=1,
\]
and \(e^{-tA_j}\to e^{-tA}\) strongly for every \(t>0\), where \(A\) is a nonnegative selfadjoint operator on that common Hilbert space and its semigroup is strongly continuous at zero. Then

\[
e^{-tA}\le P+e^{-tm_*}(I-P),\qquad
\operatorname{spec}(A)\subset\{0\}\cup[m_*,\infty),
\tag{6.1}
\]

with one-dimensional vacuum.

**Proof.** Functional calculus gives the semigroup inequality for each \(j\); strong convergence passes it in quadratic forms. Also \(e^{-tA}P=P\). The limiting inequality for every \(t>0\) excludes spectral weight in \((0,m_*)\) and additional zero-energy vectors. QED.

Varying lattice Hilbert spaces require specified embeddings or another precise generalized convergence framework. No common Hilbert-space limit, vacuum convergence, or physical lower bound uniform in both volume and spacing follows from the two-square theorem.

The existence and strong continuity of the limiting semigroup are assumptions, not consequences of pointwise strong convergence at positive times. For example \(A_j=j(I-P)\) converges at the semigroup level to \(P\) for every \(t>0\), but that limit is discontinuous at zero on a Hilbert space larger than the vacuum. It does not define a densely defined Hamiltonian there.

### Conditional rule V7. Correlation decay controls only observable spectral channels

Suppose a positive reconstructed Hamiltonian \(A\) and vacuum \(\Omega\) exist. For centered \(v=F\Omega\),

\[
C_v(t)=\langle v,e^{-tA}v\rangle
=\int_{[0,\infty)}e^{-tE}d\nu_v(E).
\tag{6.2}
\]

If \(C_v(t)\le M_ve^{-m_*t}\) for all \(t\ge0\), then \(\nu_v([0,m_*))=0\). Positive weight on any interval \([0,m_*-\epsilon]\) would contradict the bound as \(t\to\infty\).

If such vectors span a dense subspace of \(\Omega^\perp\), the full gap is at least \(m_*\). Control of one observable alone cannot exclude lighter states orthogonal to its spectral channel. A lattice-to-continuum application requires convergence of renormalized correlations, reflection positivity and the other reconstruction hypotheses, a nontrivial observable algebra, and an exponential bound in **physical** separation with adequate uniform norm control. A stochastic Poincaré bound is not already (6.2).

### Conditional rule V8. A lower gap and nontriviality are separate conditions

A sequence in which every excitation escapes to infinite physical energy can satisfy an excellent lower-gap inequality while its surviving Hilbert space contains only the vacuum. A credible continuum bridge must therefore also control nonzero limiting gauge-invariant correlations or another complete nontriviality criterion. A lower bound alone does not establish a finite-mass excitation.

## 7. Current rigorous progress and its boundaries

| Primary work | Verified scope | Remaining distinction |
|---|---|---|
| Chevyrev–Shen, 2D invariant measure and universality; revised April 2026 | On the trivial bundle over the two-dimensional torus, for connected compact groups: invariant Yang–Mills measure and universality of approximations including Wilson, Villain, Manton.[^4] | Euclidean dimension two, not four; not a Hamiltonian mass-gap bridge. |
| Chandra–Chevyrev–Hairer–Shen, stochastic Yang–Mills–Higgs in 3D; published 2024 | State space and gauge-orbit Markov process; renormalized local stochastic-time solutions with possible finite-time blow-up.[^5] | Local stochastic dynamics with Higgs fields do not establish an infinite-volume pure-gauge continuum gap. |
| Chevyrev–Shen, gauge-covariant renormalization; revised January 2026 | Uniqueness of the Yang–Mills-field mass renormalization giving gauge-covariant local 3D stochastic Yang–Mills–Higgs solutions.[^6] | A singular-SPDE counterterm is not a freely inserted physical Proca mass or a derived glueball mass. |
| Chevyrev–Qu–Shen, submitted August 28, 2026 | Weak-coupling \(U(1)\) scaling on a discrete 3D torus, in DeTurck gauge: rescaled logarithmic field converges locally in time and in probability to a one-form stochastic heat equation.[^7] | Abelian, three-dimensional, local stochastic-time scaling; not a nonabelian four-dimensional mass gap. |
| Shen–Zhu–Zhu, lattice Yang–Mills–Higgs | Strong-coupling infinite-volume exponential correlation decay for specified Higgs target spaces.[^8] | Additional fields change the model. |

Version dates above come from arXiv submission histories. The strong-coupling paper's experimental HTML displayed an August 2026 rendering date, while its PDF and submission history identify the mathematical version as April 2022. The PDF determines the theorem numbers and constants used here.

## 8. Reproduction and raw results

Run \(\texttt{python volume_checks.py}\). The script has no network or input-file dependence and uses NumPy, SciPy, Matplotlib. Checks use explicit exceptions and remain active under \(\texttt{python -O}\).

| Output file | Contents |
|---|---|
| \(\texttt{output/volume_scaling.csv}\) | Box counts and logarithms of V2 in spatial dimensions 2 and 3 |
| \(\texttt{output/tensor_counterbenchmark.csv}\) | One-square gap diagnostic, analytic \(2.5\alpha\) floor, one- and two-square tensor bounds |
| \(\texttt{output/one_square_convergence.csv}\) | Jacobi cutoffs 8, 16, 32, 64; approximate energies and omitted-component residuals |
| \(\texttt{output/gibbs_groundstate_obstruction.csv}\) | V4 polynomial coefficients after cancellation of the linear term |
| \(\texttt{output/spacing_dictionary_diagnostic.csv}\) | Coefficient substitutions along an illustrative trajectory |
| \(\texttt{output/checks.json}\) | Thirteen checks, proof/numerical scope flags, source hashes before and after |
| \(\texttt{output/volume_counterbenchmark.png}\), \(\texttt{.svg}\) | Connected-box bound loss and disconnected tensor counterbenchmark |
| \(\texttt{output/SHA256SUMS.json}\) | Output hashes |

Graph counts are compared with direct enumeration. All nonempty edge supports are enumerated in three small boxes to test the no-degree-one premise and the four-edge minimum. Two small Kronecker sums reproduce their one-copy finite-matrix gaps. These computations do not replace the general proofs.

The numerical \(\kappa=1/2\) gap is \(3.0289863271\alpha\); cutoff drift is approximately \(6\times10^{-13}\alpha\). Omitted-component residuals exclude neither every floating-point error nor a spectral-index error and are not called certified enclosures. Underflowed exponential bounds retain logarithms and explicit flags: a numerical zero is not an exact zero.

The spacing diagnostic declares \(g_H^2(a)=1/[1+\log(1/a)]\), \(L=1,d_s=3\), in reference units. This tests substitutions; it is not a fitted or derived Yang–Mills running coupling. Its target \(am=a\) column depicts what a unit finite physical mass would mean.

## 9. Primary source ledger and reading depth

All sources were accessed September 9, 2026. “Abstract scope” means the complete proof was not independently audited.

| ID | Exact primary source and date | Reading depth and use |
|---|---|---|
| S1 | Hao Shen, Rongchan Zhu, Xiangchan Zhu, [A stochastic analysis approach to lattice Yang–Mills at strong coupling](https://arxiv.org/pdf/2204.12737), v1 April 27, 2022; [publisher record](https://link.springer.com/article/10.1007/s00220-022-04609-1), online December 23, 2022; CMP 400, 805–851 (2023) | PDF definitions/main results pp. 3–8; selected Hessian/curvature/functional-inequality proof pp. 17–20; covariance argument pp. 28–30. Selected proof sections, not a complete 43-page audit. |
| S2 | Henry Froland, Dorota M. Grabowska, Zhiyao Li, [Simulating Fully Gauge-Fixed SU(2) Hamiltonian Dynamics on Digital Quantum Computers](https://arxiv.org/html/2512.22782v1), v1 December 28, 2025 | Section II, Eq. (1), and finite two-plaquette scope. Hamiltonian normalization. |
| S3 | Arthur Jaffe, Edward Witten, [Quantum Yang–Mills Theory](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf), official problem statement | Problem/mass-gap requirements and pp. 11–12 regulator discussion. Required endpoint. |
| S4 | Ilya Chevyrev, Hao Shen, [Invariant measure and universality of the 2D Yang–Mills Langevin dynamic](https://arxiv.org/abs/2302.12160v3), v3 April 6, 2026; CPAM (2026) | Abstract, comments, version history. Scoped 2D comparison. |
| S5 | Ajay Chandra, Ilya Chevyrev, Martin Hairer, Hao Shen, [Stochastic quantisation of Yang–Mills–Higgs in 3D](https://arxiv.org/abs/2201.03487v2), v2 April 15, 2024; Inventiones 237, 541–696 (2024) | Abstract/publication history. Local 3D dynamics and possible blow-up. |
| S6 | Ilya Chevyrev, Hao Shen, [Uniqueness of gauge covariant renormalisation of stochastic 3D Yang–Mills–Higgs](https://arxiv.org/abs/2503.03060v2), v2 January 21, 2026; ARMA 250, article 11 (2026) | Abstract/publication history. Renormalization scope. |
| S7 | Ilya Chevyrev, Yahui Qu, Hao Shen, [Scaling limit of the 3D abelian Yang–Mills Langevin dynamics](https://arxiv.org/abs/2608.27828v1), v1 August 28, 2026 | Abstract/submission history; incomplete experimental HTML. Latest scoped abelian result. |
| S8 | Hao Shen, Rongchan Zhu, Xiangchan Zhu, [Langevin dynamics of lattice Yang–Mills–Higgs and applications](https://arxiv.org/abs/2401.13299), submitted January 24, 2024 | Abstract scope. Distinguish a changed model. |
| D1 | [Hao Shen's author-maintained publication list](https://sites.google.com/view/haoshen) | Discovery only; followed to primary records. |
| L1 | Konrad Osterwalder, Erhard Seiler, *Gauge field theories on a lattice*, Annals of Physics 110(2), 440–471 (1978) | Located in S1 bibliography; original full text not retrieved. Historical lead only; no independently asserted theorem details. |

This targeted update does not claim exhaustive coverage of all literature. V1–V4 are derived above; V5–V8 expose additional hypotheses. External paper statements remain separate from these derivations.

[^1]: Shen, Zhu, Zhu, [arXiv:2204.12737 PDF](https://arxiv.org/pdf/2204.12737), Assumption 1.1, Theorems 1.2/1.4, Corollaries 1.6/4.11, Remark 4.12.
[^2]: Froland, Grabowska, Li, [Section II.1, Eq. (1)](https://arxiv.org/html/2512.22782v1#S2.SS1).
[^3]: Jaffe and Witten, [official problem statement](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf).
[^4]: Chevyrev and Shen, [arXiv:2302.12160v3](https://arxiv.org/abs/2302.12160v3).
[^5]: Chandra, Chevyrev, Hairer, Shen, [arXiv:2201.03487v2](https://arxiv.org/abs/2201.03487v2).
[^6]: Chevyrev and Shen, [arXiv:2503.03060v2](https://arxiv.org/abs/2503.03060v2).
[^7]: Chevyrev, Qu, Shen, [arXiv:2608.27828v1](https://arxiv.org/abs/2608.27828v1).
[^8]: Shen, Zhu, Zhu, [arXiv:2401.13299](https://arxiv.org/abs/2401.13299).
