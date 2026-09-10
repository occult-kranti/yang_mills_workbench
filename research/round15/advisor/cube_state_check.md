# The shared cube variables do not identify the interacting state

This advisor audit is a side result to be independently reviewed before promotion. It uses the same cube Wilson traces as goalB, but explicitly tests a proposed Hamiltonian state rather than assuming it.

Let `S=sum_f x_f`, with six normalized Wilson traces, and use the physical Hamiltonian with its scalar magnetic offset removed:

\[
H=\alpha\sum_e C_e-\lambda S,\quad C_e=-\sum_{a=1}^3L_{e,a}^2,\quad \alpha>0.
\]

The Lie generators act by `U_e(t)=exp(i t sigma_a/2)U_e`, so the fundamental Casimir is `3/4`. Every face has four distinct links. Therefore `sum_e C_e S=3S`. For the proposed Gibbs square-root wavefunction `psi=Z^{-1/2}exp(kappa S/2)`, the product rule gives

\[
\frac{H\psi}{\psi}=\left(\frac{3\alpha\kappa}{2}-\lambda\right)S
-\frac{\alpha\kappa^2}{4}\sum_{e,a}(L_{e,a}S)^2.
\]

The candidate is smooth and strictly positive on the compact configuration manifold. Its Hamiltonian image and this ratio are continuous. Hence an eigenvalue equation holding almost everywhere would hold everywhere, because product Haar has full support. An eigenstate would require this ratio to be constant on configuration space; testing isolated configurations is sufficient to refute this continuous identity. Evaluate three exact configurations: all links identity; one link minus identity; one link `diag(i,-i)` with all others identity. The respective pairs `(S, |grad S|^2)` are `(6,0)`, `(2,0)` and `(4,5/2)`. The matrix checker independently differentiates every signed factor to verify these numbers.

The first two configurations force `3 alpha kappa/2-lambda=0`. Under that match, the third differs from the first by `-5 alpha kappa^2/8`, which is nonzero for `kappa!=0`. Thus no chosen lambda makes this nonconstant Gibbs square root an eigenstate of the stated Hamiltonian. At `kappa=lambda=0`, the constant reference is valid. The remaining case `kappa=0,lambda!=0` is ruled out by the nonconstant `-lambda S` ratio as well.

This is a configuration-space counterexample to a particular state identification. It does not reject using Haar moments to evaluate trial vectors: variational trial states need not be true eigenstates. GoalC may use the free Haar vacuum and Wilson-loop trial vectors to bound the interacting ground energy without assuming the Gibbs density is that ground state. The two uses of the same trace coordinates are mathematically distinct.
