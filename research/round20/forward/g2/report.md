# G2 forward: the limiting state's GNS generator in the declared algebra

Use the full local factor algebra A_loc of G1, its A2 incomplete product
Hilbert space H_ref, and the normalized perturbed ground vector Ψ. Restore
the condition `β=α|τ|107/135<δ=α/8`; G1's broader arbitrary-finite-τ
dynamics statement alone did not imply ground isolation. The E2 limit state
is `ω(A)=<Ψ,AΨ>`. α, E_star and hbar retain their original lattice meanings;
the unmatched F diffusion energy c does not enter.

## Irreducibility from the actual infinite tensor representation

Let Ω be the reference product vacuum. For each finite set F of complete
reference factors, the operator
`p_F=(tensor_(i in F)|Ω_i><Ω_i|) tensor I_(outside F)` belongs to A_loc.
These projections converge strongly, as F exhausts all factors, to the
global rank-one projection `p_Ω=|Ω><Ω|`. Indeed, on a finite-excitation
vector, every sufficiently large F projects each excited factor to its
vacuum, leaving exactly its inner product with Ω times Ω. Such vectors
are dense, and the projections are uniformly bounded by one, proving strong
convergence on the whole Hilbert space.

If a bounded T commutes with A_loc, it commutes with every p_F and hence
with their strong limit p_Ω. Therefore `TΩ=aΩ` for a scalar a. Finite
local rank-one operators applied to Ω produce the dense finite-excitation
core. Commutation now gives `TAΩ=aAΩ` on that dense set, so T=aI.
The representation is irreducible. This is an infinite core argument,
not a consequence of finite matrix ranks.

For every nonzero vector Ψ, the closure of A_loc Ψ is a reducing subspace:
it is invariant under A_loc and its adjoints. Its orthogonal projection
commutes with A_loc, so irreducibility forces that nonzero projection to
be I. In particular the actual perturbed ground Ψ is cyclic.

## The null quotient identifies the GNS Hilbert space

The GNS pre-Hilbert space quotients A_loc by
`N_ω={A:ω(A* A)=0}`. Define

\[
W:[A]\longmapsto A\Psi.
\]

The null condition is precisely `AΨ=0`, making W well-defined and
injective on the quotient. Its inner product is exactly preserved:
`<[A],[B]>_ω=ω(A*B)=<AΨ,BΨ>`. Cyclicity makes its range dense,
so its completion is a unitary from the GNS Hilbert space onto the declared
A2 product representation. It intertwines GNS left multiplication by B
with the actual local operator B. In particular this full-algebra limit
state has an irreducible GNS representation and is pure.

## Dynamics and the energy subtraction that cannot be omitted

Let e be the actual eigenvalue of H on Ψ, with e≤0. G1 supplies the
Heisenberg automorphisms `α_t(A)=e^(itH/hbar)Ae^(−itH/hbar)`; their
point-norm continuity on all of A_loc was explicitly disproved. The state
is invariant because Ψ is an H eigenvector. On cyclic vectors,

\[
W[\alpha_t(A)]
=\alpha_t(A)\Psi
=e^{it(H-e)/\hbar}A\Psi.
\]

Hence the GNS implementation is strongly continuous and, under W, exactly
`U_t=e^(it(H−e)/hbar)`. Its nonnegative physical energy generator is
`K=H−e`, with the factor 1/hbar converting energy to inverse time. The
e subtraction makes the cyclic ground invariant, U_tΨ=Ψ, rather than
merely a vector with a changing phase. The shift cancels in observable
conjugation, but is required for this normalized GNS implementation.

The A2 spectral theorem gives a unique ground and excited H spectrum at
or above δ−β. Thus K has a one-dimensional zero eigenspace and

\[
\operatorname{gap}(K)\ge\delta-\beta-e\ge\delta-\beta.
\]

At `|τ|=1/64`, the inherited lower bound is `973α/8640`. This identifies
the generator and transfers an already proved gap; it is not an additional
larger gap theorem. The absolute excited threshold δ−β is not asserted
equal to the actual eigenvalue gap.

## Discriminators and scope

Exact M2 matrix-unit Gram examples have GNS rank two for a pure state and
rank four for the maximally mixed state. A diagonal subalgebra acting on C2
has a nonzero vector e0 whose cyclic space is only one-dimensional. These
controls prevent silently applying full-factor irreducibility to a mixed
state or a restricted algebra. Another exact example `H=diag(−1,2)`
requires subtracting e=−1 to obtain the correct positive generator
`diag(0,3)` and an invariant cyclic ground. Strict β<δ and positive
physical-reference controls are also executed.

The identified state is precisely E2's local weak-star limit in the chosen
product representation of the **full bounded local-factor algebra**. The
GNS representation of a Gauss-invariant subalgebra is a separate question;
it is not asserted equal to this one. No representation-independent,
homogeneous or continuum Yang–Mills conclusion follows. The F research used
a conditional three-link space with its exterior fixed, not a demonstrated
gauge-fixing equivalence, and plays no role in this GNS identification.
