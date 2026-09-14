# F1 forward: a static law does not determine an energy or clock

Use exactly C1's gauge-fixed space `M=SU(2)^3`, product Haar probability m,
shared-middle variables U,V,W, and action `S=3x+y+z+w+t`. Fix the product
Casimir metric with fundamental eigenvalue 3/4. For every finite real κ,
let `ρ_κ=e^(κS)/Z_κ`, `dμ_κ=ρ_κ dm`. This is a smooth strictly positive
probability density on a compact connected manifold. In particular all C2
static expectations, including its signed-κ inequality, refer to this same law.

## An explicitly added reversible family

Define on smooth functions the quadratic form

\[
q_\kappa[f]=\int_M|\nabla f|^2\,d\mu_\kappa.
\]

Since the density is bounded above and below by positive constants, its
closure has exactly the weighted H1 Sobolev domain, equal as a set to H1(M,m).
The closed, densely defined nonnegative form determines a unique nonnegative
self-adjoint operator A_κ. Integration by parts without boundary gives its
smooth-core expression

\[
A_\kappa=-\rho_\kappa^{-1}\operatorname{div}(\rho_\kappa\nabla)
=-\Delta-\kappa\nabla S\cdot\nabla.
\]

On this compact smooth manifold its operator domain is H2, with the weighted
norm equivalent to the usual one. Its Dirichlet form is Markovian, so
`exp(−s A_κ)` is a reversible Markov semigroup preserving μ_κ. Constants
have zero form energy; conversely zero energy forces zero weak gradient,
hence a constant by connectedness. The zero mode is unique. The state space
is the gauge-fixed C1 space; no further Gauss-sector statement is inferred.

Choose an independent positive physical energy c and define

\[
H_{\kappa,c}=cA_\kappa,\qquad
T_t=\exp[-tH_{\kappa,c}/\hbar].
\]

Here κ is dimensionless, c/E_star is externally supplied, hbar has action
units, t has time units, and lattice length a is independently fixed.
Every c has the same μ_κ, the same normalized constant ground in L2(μ_κ),
and identical static expectations. All nonzero energies are multiplied by c,
and every time correlation is correspondingly reparameterized. This is an
added family of reversible dynamics, not a derivation of the Yang–Mills
transfer Hamiltonian from the static measure.

## Exact nonidentifiability and a uniform positive gap

At κ=0, product Haar has exact first Casimir excitation 3/4, from a
fundamental representation on one factor and constants on the others.
Thus c=E_star and c=2E_star give gaps `3E_star/4` and `3E_star/2`
with identical static law. A centered fundamental matrix coordinate has
autocorrelation proportional to `exp(−3ct/(4hbar))`. Static moments contain
no information choosing between these two physical clocks.

Positivity is not restricted to κ=0. Write ρ_min and ρ_max for the density
extrema. Using the variational characterization of variance,

\[
\operatorname{Var}_{\mu_\kappa}(f)
\le\rho_{max}\operatorname{Var}_m(f)
\le\frac{4\rho_{max}}3\int|\nabla f|^2dm
\le\frac{4\rho_{max}}{3\rho_{min}}q_\kappa[f].
\]

Because `|S|≤7`, the ratio is at most `e^(14|κ|)`. Consequently

\[
\operatorname{gap}(H_{\kappa,c})
\ge\frac{3c}{4}e^{-14|\kappa|}>0.
\]

This is a standard bounded-density comparison applied to the stated model.
It does not identify c or make the dynamics unique. The checker supplies
rational exponential upper bounds for signed κ fixtures rather than treating
floating-point exponentials as certificates.

## Controls and limits

For the actual product metric,
`ΔS=−(3/4)(3x+y+z+2w+2t)`. At U=V=W=I, its value is −27/4
and `|∇S|²=0`. The correct formal adjoint annihilates ρ_κ. Reversing the
drift sign leaves an exact adjoint residual `27κ/2` after division by ρ_κ.
Using bare Haar as the invariant law for nonzero κ instead leaves
`κΔS=−27κ/4`. Both wrong models are rejected at positive and negative κ.

The checker also rejects c=0 in a positive-gap claim, a zero E_star, and
assertions that c=κ or c=α or a Fibonacci label follows from notation alone.
α belongs to the earlier lattice Hamiltonian and has not been matched to this
new generator. A measured dynamic quantity or independent normalization is
required even within this one-parameter family; broader diffusion families
would require more information. No temporal reflection-positivity,
Yang–Mills identification, homogeneous limit or continuum reconstruction
is established by constructing a reversible diffusion here.
