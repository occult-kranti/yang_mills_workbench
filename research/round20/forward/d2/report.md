# D2 forward: quantitative ground-state convergence

Fix the D1 representation, finite-factor completions, and positive physical
reference E_star. Put δ=α/8, β_L=α|τ|s_L, β=α|τ|107/135,
ε_L=β−β_L, and assume **β<δ**. Set g_L=δ−β_L and g=δ−β>0.
The same actual face coefficients and reference factors occur throughout.

## Existence, including the finite-factor operator

For H and each lifted H_L, the reference vacuum has trial energy zero because
every retained or infinite perturbing face has a free-link Haar witness.
On its orthogonal complement the quadratic forms are at least g or g_L.
The spectral subspace below that threshold is nonempty: otherwise every
trial vector would have strictly positive energy. It has dimension at most
one, because any two-dimensional subspace contains a vector orthogonal to
the reference vacuum. Hence each operator has a simple isolated ground
e or e_L≤0, and the rest of its spectrum lies at or above g or g_L.
This is a spectral-subspace argument and does not presume compact resolvent.

D1's lift splits as `K_L⊗I+I⊗H_ref,out`. On the exterior-vacuum
orthogonal sector, `H_ref,out≥δ` while `K_L≥−β_L`; the lifted operator
therefore has energy at least g_L>0. Its ground, of energy at most zero,
must lie in the exterior vacuum sector. Consequently K_L itself has a
simple ground eigenvector, and the lifted eigenvector is exactly its tensor
product with the exterior reference vacuum. Its factors remain infinite
dimensional. This supplies existence without turning K_L into a finite matrix.

## Energy, projector, and observable estimates

The bounded perturbation difference obeys `||H−H_L||≤ε_L` on the
common operator/form domain. Variational infima in both directions imply

\[
|e-e_L|\le\epsilon_L.
\]

Write P_L for the rank-one ground projection of H_L, Q_L=1−P_L,
and φ for a normalized ground vector of H. Since e≤0 and the excited
spectrum of H_L is at least g_L,

\[
Q_L(H_L-e)Q_L\ge(g_L-e)Q_L\ge g_L Q_L.
\]

The ground eigenvector is in the common domain. Projecting
`(H_L−e)φ=−(H−H_L)φ` and inverting on Q_L therefore yields

\[
\|Q_L\phi\|\le\epsilon_L/g_L.
\]

For two normalized pure states, their rank-one projector difference has
nonzero eigenvalues `±sqrt(1−|<φ_L,φ>|²)`. Thus

\[
\|P-P_L\|\le\min(1,\epsilon_L/g_L),\qquad
\|P-P_L\|_1\le2\min(1,\epsilon_L/g_L).
\]

For every bounded observable A on this representation (local or otherwise),
the trace duality inequality gives

\[
|\langle A\rangle-\langle A\rangle_L|
\le2\|A\|\min(1,\epsilon_L/g_L)\longrightarrow0.
\]

The projector and normalized-observable errors are dimensionless; energy
errors are recorded relative to the same E_star. At τ=1/64, the limiting
compression floor is `g=973α/8640`. Neither g nor g_L is an equality
for the actual ground-to-excited spectral gap; each is a rigorous lower bound.

## What the controls discriminate

The sharper denominator uses e≤0, which depends on the zero trial mean.
For `H_L=diag(1,2)` and its orthogonal rotation with eigenvector `(3/5,4/5)`,
the projector distance is 4/5 and the operator perturbation norm is 4/5.
Dividing by the absolute excited threshold 2 would incorrectly give 2/5.
The missing nonpositive-ground premise cannot be removed.

The rank-one identity also fails if ranks differ: projections onto
`span(e1,e2)` and `span(e1)` share an exact vector but have distance one.
Strong resolvent convergence alone is weaker than D1: on l2, the bounded
operators `A_n=I−2|e_n><e_n|` converge strongly (hence strongly in resolvents)
to I, while their ground eigenvalues remain −1 and their ground projections
converge strongly to zero. The moving vector escapes every fixed finite
support. These are executed finite arithmetic witnesses for the complete
counterexamples given here, not numerical proofs of infinite convergence.

The checker also rejects β≥δ, a zero physical reference, and equating a
spectral threshold with the gap. It emits exact L=0..8 energy/projector/observable
error ledgers, using the frozen D1 result as a source-bound input and independently
recalculating its tail. Standard variational, spectral and trace inequalities
are the tools; the contribution is their explicit use with this model's tail
and zero-mean structure. Literal clipped-boundary convergence remains outside D2.
