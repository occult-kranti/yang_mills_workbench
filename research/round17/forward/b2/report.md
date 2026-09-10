# B2: a shared-face adjoint repairs the finite B1 endpoint

This calculation keeps the actual 12-vertex, 20-link, 11-face two-cube graph, the full untruncated Gauss-invariant SU(2) link Hilbert space, and the Hamiltonian fixed. Every physical coefficient is lambda_p=(12/43) alpha, with alpha>0. Only the trial space is enlarged. The coefficient eta is a dimensionless amplitude of a legitimate state, not a new coupling, field, counterterm or change in the action. The common physical energy scale alpha is separate from the Euclidean coefficients used in earlier static Haar experiments.

## The added state and every matrix element

The shared square is identified from the actual incidence graph: its four boundary links are precisely the links incident to three distinct faces. The unique face bounded by those four links agrees with the retained shared-face metadata. The new state is a=chi_2(U_s)=4x_s^2-1, where x_s=Tr(U_s)/2. It is the ordinary spin-one character, not a normalized trace with another dimension factor.

The thirteen trial states are Omega, the eleven chi_1(U_p)=2x_p, and a. They are gauge invariant, smooth and in the electric operator domain. The Gram matrix is I_13. In particular, single-face Haar moments give

    <a^2> = 16<x_s^4> - 8<x_s^2> + 1
           = 16/8 - 8/4 + 1 = 1.

Its mean vanishes, and it is orthogonal to every fundamental face character. Odd shared powers establish the same-face orthogonality; for different faces, link integration or center parity gives zero. The code expands every polynomial before applying the accepted actual-graph Haar functional, including repeated indices. All 169 Gram entries and all 1859 individual magnetic insertions are reconstructed.

An elementary adjoint loop occupies four spin-one links, each with Casimir j(j+1)=2. Thus H0 a=8 alpha a. Every diagonal magnetic entry <a,x_f a> vanishes. The only new off-diagonal magnetic entry is

    <a,x_s chi_1(U_s)> = 8<x_s^4> - 2<x_s^2> = 1/2,
    <a,W chi_1(U_s)> = -lambda_s/2.

For a different fundamental face p or different insertion f, the actual mixed Haar moments vanish. One case needs more than parity: if p=f differs from the shared face, integrate a boundary link of p absent from s first. The conditional integral of x_p^2 is 1/4, so <x_p^2 x_s^2>=1/16 and <a,x_p chi_1(U_p)>=2(4/16-1/4)=0. The graph supplies such an exclusive link for every p other than s. The remaining cases follow from the explicit polynomial products and graph integration. They are not inferred from distinct-face subset tests alone. The copied local Haar utility retains the previous two-disk character integration and source bindings.

## A specific state and the full spectral inequality

First set alpha=1. Write e=-3/43. The independently proved full-operator bound from B1 is E1(H)>=3-sum_p|lambda_p|=e. Its proof uses the physical free gap and a bounded perturbation; it is not an eigenvalue of the trial matrix.

At the same coupling, the old twelve-state trial vector

    v0 = Omega + (1/22) sum_(p=1)^11 chi_1(U_p)

has squared norm G=45/44 and is an exact eigenvector of the old trial block at e. Its coupling to the new state is <a,H v0>=-3/473. Consequently v_eta=v0+eta a, for every real eta, has

    ||v_eta||^2 = G+eta^2 > 0,
    <v_eta,H v_eta> = eG - (6/473)eta + 8eta^2.

This is an actual physical Rayleigh quotient R(eta), so E0(H)<=R(eta). Combining the two directions, without a Galerkin lower-bound substitution,

    Delta_physical >= e-R(eta)
      = [(6/473)eta-(347/43)eta^2]/[45/44+eta^2].

The right-hand side is an exact lower bound on the full physical gap. There is no physical-gap upper bound asserted here. A positive value also separates the lowest full eigenvalue from the second one; finite-graph compact resolvent and the bounded perturbation hypotheses are inherited unchanged from B1.

## Whole interval, chosen amplitude and controls

The numerator factors as

    (347/43) eta (6/3817-eta).

Since its prefactor and the denominator are positive, the sufficient gap bound is strictly positive exactly for 0<eta<6/3817. This sign statement holds for the whole interval by an exact polynomial identity; plotted samples are illustrations rather than the proof.

The chosen eta=3/3817 gives the exact physical gap lower bound 1388/284767457, approximately 4.8741524562618824 times 10^-6 at alpha=1. It is the midpoint and maximizes the quadratic numerator. It is not labelled a maximizer of the quotient. Indeed, the numerator derivative is zero there, while the quotient derivative has negative numerator -2 eta N(eta), so the chosen point is not the stationary quotient maximum.

At eta=0 or eta=6/3817 the estimate is exactly zero. Negative amplitudes and amplitudes beyond the upper endpoint give a negative estimate. All these are valid trial states with insufficient lower bounds; none is an invalid quantum state, physical instability test or evidence that the actual gap closes. The runner retains these cases, rejects a missing cross term and normalization, and checks that a trial excited energy cannot replace the full E1 estimate.

For general alpha>0, every Hamiltonian matrix entry, Rayleigh energy and full gap lower bound scales exactly by alpha; eta and the positivity interval do not change. The two additional fixtures alpha=2 and alpha=1/2 verify this directly. Zero and negative alpha are rejected. All finite signed rational eta, including zero, define valid trials. Boolean or nonfinite inputs do not meet the exact-rational contract.

## Scope and reproduction

Run `python -B check.py --output ../b2-output` from this source directory. The output folder must be outside the frozen sources. All actual imports are local; the graph, copied Haar implementation and new source are hash bound. The normal and optimized runs must produce identical semantic evidence bytes. Exact rational CSV values are authoritative.

This is one finite dense-graph improvement obtained by an additional physical representation in a trial state. It repairs B1's actual zero margin at lambda/alpha=12/43. It does not establish a dense volume-uniform stability theorem, replace the sparse-support hypotheses, or resolve the continuum Yang-Mills mass gap. No next research loop is executed by this package.
