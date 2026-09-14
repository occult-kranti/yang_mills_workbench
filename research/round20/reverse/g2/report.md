# G2 reverse reconstruction: identify the cyclic representation already constructed

Let A_loc be all bounded operators on finitely many complete reference factors,
and A its norm closure in the A2 incomplete tensor-product representation H.
The factors include the entire selected-strip link Hilbert spaces and free
links. This is the full factor algebra; no equality with a Gauss-only algebra
or its GNS representation is being asserted.

Exhaust the countably many factors by finite J. The local operators
`P_J=(tensor_(j in J)|Omega_j><Omega_j|) tensor I_out` converge strongly to
`P_Omega=|Omega><Omega|`. On every finite-excitation elementary tensor this
holds once J includes its excited factors; boundedness extends the convergence
to H. If T commutes with A, it commutes with every P_J and hence P_Omega, so
`T Omega=z Omega`. It follows that `T(A Omega)=z A Omega` on the dense
finite-excitation set. Thus the commutant is scalar and the representation is
irreducible.

For any nonzero vector Psi, the closed span of A Psi is invariant under A and
A*, hence its orthogonal projection is in the commutant. It must be I. In
particular the normalized perturbed ground Psi_H is cyclic. This argument
requires neither finite Hilbert dimension nor that Psi_H be the product vacuum.

For the E2 limiting state `omega(A)=<Psi_H,A Psi_H>`, the GNS null space is
`N={A:omega(A*A)=0}`. The map

\[
[A]\longmapsto A\Psi_H
\]

is well defined and isometric from the null quotient, since its norm squared
is omega(A*A). Cyclicity makes its completion onto H. It intertwines the GNS
representation with the existing local-factor representation. This is an exact
identification, not a second independent construction of an infinite-volume
field theory.

Restore the gap premise `beta=alpha*|tau|*107/135<delta=alpha/8`. A2 gives
unique ground e in `[-beta,0]` and excited spectrum at least `delta-beta`.
The E2 state is invariant under the G1 Heisenberg group. On the GNS dense set,

\[
[\alpha_t(A)]\longmapsto
 e^{itH/\hbar}Ae^{-itH/\hbar}\Psi_H
 =e^{it(H-e)/\hbar}A\Psi_H.
\]

Thus its state-preserving implementing group is strongly continuous and fixes
the cyclic ground vector. Its energy generator is H-e, with nonnegative
spectrum, simple zero mode and gap at least `delta-beta`. The Stone frequency
generator is `(H-e)/hbar`. Point-norm continuity of alpha_t on the full algebra
is not required and remains false in the G1 counterexample. A scalar shift
cancels in conjugation, but subtracting actual e is essential when choosing the
canonical GNS implementer that fixes the cyclic vector.

The exact finite checks use all four matrix units in M2. A pure vector state has
GNS Gram rank2, whereas the maximally mixed state has rank4; reusing the
physical vector Hilbert space for the latter would fail. The diagonal
subalgebra provides a non-scalar commuting operator and a noncyclic nonzero
vector, demonstrating why irreducibility is needed. These examples discriminate
wrong premises; they are not the proof of the infinite algebra statement.

At `alpha/E_star=2`, `tau=1/64`, the inherited energy gap floor is
`973/4320 E_star`. No F diffusion coefficient enters. This identifies the E2
state and its original lattice dynamics in the chosen representation. It does
not establish representation-independent homogeneous or continuum Yang-Mills.
