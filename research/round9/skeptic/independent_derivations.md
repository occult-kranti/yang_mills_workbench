# Independent skeptic contract: round 9

This record supplies independent reference calculations. It is a mathematical/code review, not formal proof-kernel verification. Source inspection, executed tests, statistical consistency and continuum theorems are separate evidence classes.

## Wilson action and local link identity

On a periodic four-dimensional hypercubic lattice with every extent at least two, use

\[
U_{\mu\nu}(x)=U_\mu(x)U_\nu(x+\hat\mu)
 U_\mu(x+\hat\nu)^\dagger U_\nu(x)^\dagger,
\qquad S=\beta\sum_{x,\mu<\nu}[1-\tfrac12\operatorname{Re}\operatorname{Tr}U_{\mu\nu}(x)].
\]

The identity configuration has zero action. There are six positive-orientation plaquettes per site, and each link occurs in six plaquettes. Omitting the dagger on either reverse-oriented segment destroys generic local gauge invariance. An extent-one lattice requires different local-action handling because one nominal plaquette can depend on the same link more than once; it should be rejected by a simple single-link/staple algorithm unless separately implemented.

Freeze every link but one and write the sum of its six adjacent normalized traces as a real linear function \(f(q)=s\cdot q\) on \(q\in S^3\). The portion of the Boltzmann density depending on that link is \(e^{\beta f}\). The unit-sphere Laplacian and gradient satisfy

\[
\Delta_{S^3}f=-3f,\qquad |\nabla_{S^3}f|^2=|s|^2-f^2.
\]

Haar integration by parts therefore gives the exact finite-lattice identity

\[
\boxed{\left\langle3f-\beta(|s|^2-f^2)\right\rangle=0.}
\]

Using generators \(\sigma_a/2\) multiplies both derivative terms by \(1/4\) and does not alter the displayed identity. Normalizing the six-plaquette sum to an average changes its coefficients and must be tracked. A Monte Carlo Ward residual statistically compatible with zero is not a deterministic proof and a nonempty correlated sample requires a declared uncertainty treatment.

For the matrix oracle, compute the complete global action before and after replacing a link. This avoids using the production staple formula or quaternion multiplication. Matrix gauge transformations are \(U_\mu(x)\mapsto G(x)U_\mu(x)G(x+\hat\mu)^\dagger\). Matrix Lie perturbations are \(U\mapsto e^{i\epsilon\sigma_a}U\). Centered finite differences independently reconstruct \(f\), its Laplacian and gradient.

## Exact SU(2) convolution

For the class angle \(0\le\theta\le\pi\), normalized Haar integration uses \((2/\pi)\sin^2\theta\,d\theta\). Let \(n=2j+1\), \(\chi_j(\theta)=\sin(n\theta)/\sin\theta\), and \(k_\beta(U)=e^{\beta\cos\theta}/Z_\beta\). Then

\[
Z_\beta=\frac{2I_1(\beta)}{\beta},\quad
\int e^{\beta\cos\theta}\chi_j\,dU
=I_{n-1}(\beta)-I_{n+1}(\beta)
=\frac{2nI_n(\beta)}{\beta}.
\]

Convolution acts on each representation matrix element by

\[
\boxed{r_j(\beta)=\frac{1}{n}\int k_\beta\chi_j\,dU
=\frac{I_n(\beta)}{I_1(\beta)}}.
\]

The full \(L^2(SU(2))\) multiplicity is \(n^2\), and the class-function subspace has one character for each \(j\). At \(\beta=0\), the operator is projection onto constants: \(r_0=1\), \(r_{j>0}=0\). At fixed \(\beta>0\), all eigenvalues are positive. The largest nonconstant one is \(I_2/I_1\); the transfer-operator gap is \(1-I_2/I_1\) while the dimensionless Hamiltonian gap is \(-\log(I_2/I_1)\). These are distinct observables.

At fixed representation and large \(\beta\),

\[
-\log r_j=\frac{n^2-1}{2\beta}+O(\beta^{-2}).
\]

Thus positive finite-regulator gaps need not have a positive common lower bound. The physical energy also requires specifying the time spacing: \(E_j=-a_t^{-1}\log r_j\). At negative \(\beta\), the pointwise kernel remains positive but \(r_j(\beta)=(-1)^{n-1}r_j(|\beta|)\), so the fundamental eigenvalue is negative. This is a discriminating counterexample to inferring operator positivity from positive function values alone.

## Scope

Neither a one-group convolution operator nor a finite four-dimensional lattice supplies the reconstructed infinite-volume continuum four-dimensional pure Yang–Mills Hilbert space, a dense physical operator family, or a common positive mass bound in fixed physical units. A finite-lattice Ward identity is exact at its regulator and does not prove the continuum limit exists. A small set of reflection-positivity matrix tests is a necessary finite check only.
