# M1 reverse reconstruction: from local residuals to strong dynamics

## Verdict and premises

The desired strong-topology conclusion follows in the fixed A2 incomplete
tensor-product representation. This is a model-specific application of bounded
perturbation and strong-convergence arguments. Scientific priority is unverified.
No forward M1 source, report or output was inspected before this report froze.

Use the full-link selected-strip/free reference `H0=H_ref`, its product vacuum
`Omega`, and the admitted A2/H2/G2 premises. Keep `E_star>0`, `alpha/E_star>0`,
`hbar>0` and the lattice spacing fixed. Fix `0<eta<1`, let `q` increase to 1,
and take

\[
 P(q)=2+5q+5q^2+6q^3+3q^4,\qquad
 B(q)=\frac{P(q)}{24(1-q)^3(1+q)^2(1+q^2)},\qquad
 \tau_q=\frac{\eta}{8B(q)}.
\]

Here `q,eta,tau_q` are dimensionless action-profile parameters, not measured
physical constants or time calibrations. `V_q=-alpha tau_q sum_f w_f(q)x_f`
uses only omitted positive-orientation faces, with `w_f=q^(x+y+z)/24` and
`||x_f||<=1`. H2 supplies

\[
 \|V_q\|=\alpha\eta/8=:M>0,\qquad
 \sigma_q^2:=\|V_q\Omega\|^2
 =\alpha^2\tau_q^2B(q^2)/96,
 \quad -\sigma_q^2/\bar g\le e_q\le0,
 \quad\bar g=\alpha(1-\eta)/8.
\]

These premises are inherited mathematical results, not independent physical
observations. J2's fixed dyadic physical-sector result is not silently extended
here to new profile parameters; this loop proves a theorem on the full A2 space.

## 1. Reconstruct the local condition actually needed

To prove `V_q -> 0` strongly it is enough to prove convergence on a dense set
and a uniform operator bound. Vacuum convergence alone is insufficient.
For a bounded operator `A` on finitely many **complete** reference factors `F`,
the additional requirement on this route is `[V_q,A]Omega -> 0`:

\[
 V_qA\Omega=A V_q\Omega+[V_q,A]\Omega.
\]

Conversely, if both strong convergence on `A Omega` and vacuum convergence
hold, that commutator applied to the vacuum necessarily tends to zero. The
operator-norm commutator estimate below is sufficient, stronger than this
necessary vector condition. It is not asserted to be necessary for every
conceivable strong-dynamics limit.

Let `E(F)` be the union of **all links** in factors F. A selected strip anchored
at `(4i,2j,k)` has six x-links with tails `(4i+r,2j+s,k)`, `r=0,1,2`, `s=0,1`,
and four y-links with tails `(4i+r,2j,k)`, `r=0,1,2,3`. Every other link is a
single free factor. Each link has one owner; a strip has ten links. A bounded
operator on a dressed strip need not be supported only on its displayed Wilson
edges. A face disjoint from `E(F)` acts on tensor factors disjoint from A and
therefore commutes with A.

Define `N(F)` to be all omitted faces whose edge set meets `E(F)`, and

\[
 D_F(q)=\sum_{f\in N(F)}w_f(q).
\]

For a link of axis a and tail v, every incident positive-oriented face has
axis pair `{a,b}` for a transverse b and base either `v` or `v-e_b`. Omit the
second base when its coordinates would be negative. Thus a link in the
nonnegative-octant lattice meets at most four elementary faces; boundary links
meet fewer, and retaining only omitted faces cannot increase the count.
This exhausts incident faces without any finite-box clipping convention.
Consequently `|N(F)|<=4|E(F)|`, and every weight is at most `1/24`, giving

\[
 D_F(q)\le |E(F)|/6,\qquad
 \|[V_q,A]\|\le 2\alpha\tau_q\|A\|D_F(q).
\]

The infinite defining series of V converges in operator norm for each q<1.
Taking its commutator termwise is legitimate; all terms outside the finite
set N(F) vanish exactly. Therefore

\[
 \boxed{\|V_qA\Omega\|\le
 \|A\|[\sigma_q+2\alpha\tau_qD_F(q)]
 \le\|A\|[\sigma_q+\alpha\tau_q|E(F)|/3].}
\]

The checker builds strips explicitly, verifies a complete cover against an
independent ownership formula, and compares incident-face reconstruction with
direct face enumeration. It includes a selected Wilson face whose four edges
miss omitted faces touching other links in the same ten-link strip. This
rejects the smaller Wilson-edge-only commutator budget for arbitrary dressed A.
The finite checks discriminate mistakes; the incidence argument supplies the
universal bound.

## 2. Close the density argument without a hidden domain assumption

Exact algebra gives

\[
 \frac{\tau_q}{(1-q)^3}
 =\frac{3\eta(1+q)^2(1+q^2)}{P(q)}\longrightarrow\frac{8\eta}{7},
\qquad
 \frac{\sigma_q^2}{\alpha^2\eta^2(1-q)^3}
 =\frac{P(q^2)(1+q)}{256P(q)^2(1+q^4)}
 \longrightarrow\frac1{5376}.
\]

Thus the boxed bound tends to zero for every fixed A and F, with upper-bound
rate `O((1-q)^(3/2))`. These are bounds for fixed local vectors, not a uniform
rate over the unit sphere or a claimed nonzero leading error coefficient.

Finite-excitation elementary tensors are dense by the definition of the A2
incomplete tensor product. Any vector `v_F tensor Omega_out` can be obtained by
the bounded local rank-one operator `A_F=|v_F><Omega_F|` applied to Omega.
Finite sums can be represented on the union of their supports. This uses the
full bounded-factor algebra and requires no strict positivity or division by a
reference wavefunction.

For arbitrary fixed psi and a finite excitation phi,

\[
 \limsup_{q\uparrow1}\|V_q\psi\|
 \le M\|\psi-\phi\|
 +\limsup_{q\uparrow1}\|V_q\phi\|
 =M\|\psi-\phi\|.
\]

Let phi approach psi to obtain `V_q -> 0` strongly. Arbitrary bounded local
operators need not map Omega into `D(H0)` or its form domain. None of this
bounded-V density proof asserts that they do.

## 3. Recover the resolvents on their actual domains

A2 constructs H0 as a self-adjoint nonnegative operator. Each Vq is bounded
self-adjoint, so `H_q=H0+V_q` is self-adjoint on exactly `D(H0)` and has the
same form domain. Fix a complex energy z with `Im z != 0`. For every psi,

\[
 (R_q(z)-R_0(z))\psi=-R_q(z)V_qR_0(z)\psi,
 \qquad
 \|(R_q-R_0)\psi\|
 \le |\operatorname{Im}z|^{-1}\|V_qR_0\psi\|\longrightarrow0.
\]

The argument of Vq is the fixed vector R0 psi; no q-dependent vector is
substituted into a strong-limit statement. This proves strong-resolvent
convergence. The same conclusion holds for `H_q-e_q`, because `e_q -> 0`.

## 4. Obtain a bound uniform on each finite time interval

Write `U_q(t)=exp(-itH_q/hbar)` and `U0(t)=exp(-itH0/hbar)`.
For psi in `D(H0)`, differentiation of `U_q(t-s)U0(s)psi` is justified by the
common operator domain and the graph-norm continuous reference orbit. It gives
the Duhamel identity. Boundedness of Vq and density extend that identity to
every psi as a strong vector integral:

\[
 (U_q(t)-U_0(t))\psi
 =-\frac{i}{\hbar}\int_0^t U_q(t-s)V_qU_0(s)\psi\,ds.
\]

The formula with its oriented integral covers negative t as well. For fixed
psi and finite T, `K={U0(s)psi: |s|<=T}` is norm compact, since the reference
group is strongly continuous. Uniformly bounded operators converging strongly
to zero converge uniformly on a compact set: use a finite epsilon-net of K,
pointwise convergence at its centers and the uniform bound M. Hence

\[
 \boxed{\sup_{|t|\le T}\|(U_q(t)-U_0(t))\psi\|
 \le\frac{T}{\hbar}\sup_{|s|\le T}\|V_qU_0(s)\psi\|
 \longrightarrow0.}
\]

For the canonical ground-energy shift, an extra error is at most
`T |e_q| ||psi||/hbar <= T sigma_q^2 ||psi||/(hbar gbar)`, which also vanishes.
The compactness proof gives convergence for every fixed vector and finite T;
it does not provide a uniform local rate for all evolved vectors, nor an
unbounded-time limit.

For the established general framework, the checked primary source is
[Teschl, Mathematical Methods in Quantum Mechanics, section 6.6](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf),
printed pp. 154–155 (PDF pp. 165–166): Theorem 6.31, Corollary 6.33 and Lemma
6.36. The model support estimate and the compact-time Duhamel argument above
are written out, rather than inferred from a pointwise-time citation.

## 5. Discriminating topology and interpretation controls

On `ell^2(N_0)`, take `V_n=c|e_n><e_n|` for n>=1 and fixed c>0. Its norm is
c, its vacuum residual on e0 is zero, and it converges strongly to zero. For
the fixed unit vector with entries `sqrt(3)2^-k`, k>=1, the squared error is
`3c^2/4^n`, whereas the moving unit vector e_n has squared error c^2. This
discriminates fixed-vector convergence from operator-norm convergence.

Two reference Hamiltonians demonstrate that constant perturbation norm alone
decides neither norm-resolvent question. At z=i E_star:

* For `H0 e0=0`, `H0 e_k=E_star e_k` for k>=1, the squared resolvent-difference
  norm is `c^2/[2 E_star^2 ((E_star+c)^2+E_star^2)]`, independent of n.
* For `H0 e_k=k E_star e_k`, it is
  `c^2/[((n E_star)^2+E_star^2)((n E_star+c)^2+E_star^2)]`, which tends to zero.

Both preserve a simple vacuum and positive reference gap. In either example,
at `t=pi hbar/c`, the moving component acquires phase -1 and the propagator
difference norm is 2. These are counterexamples to automatic norm conclusions,
not calculations of the lattice model's norm resolvent or propagator norm.

The canonical tau tends to zero. Each fixed omitted-face coefficient tends to
zero, while the global norm remains M; the limiting Hamiltonian is the
selected-strip reference, which still has its selected interactions. A fixed
nonzero homogeneous omitted coupling is not obtained. This loop neither
proves nor disproves norm-resolvent convergence for the actual lattice family,
and does not identify the K/L conditional diffusion, establish a continuum
theory or measure a physical mass. M2 awaits the advisor's M1 gate.

## Executed evidence

Run `python3 -B research/round21/reverse/m1/check.py --output FRESH_DIRECTORY`.
The standard-library checker uses exact rational profiles, deterministic full
support geometry, exact squared topology controls and portable source hashes.
It records the theorem's scoped verdict separately from arithmetic checks;
the output is not a machine-formalized proof of the infinite-dimensional steps.
