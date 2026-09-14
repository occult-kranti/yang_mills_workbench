# Q2 forward: exact projected memory and controlled graph-specific leading matrices

The actual complementary electric gap is 3alpha. The exact projected
Volterra and Schur relations below have bounded memory/self-energy terms
on their closed domains. For the fixed channels f0=1, f1=2x, their leading
weak-magnetic matrices have seven explicitly derived electric energies
and a nonzero off-diagonal entry. The full selected-Hilbert remainders
are bounded by order lambda³, uniformly in delay and at small positive
resolvent energy. No current opposing Q2 solution was read before freeze.

## 1. Fixed model, domains, and actual complementary gap

Keep precisely Q1's 18-vertex, 33-link, 20-face graph, all vertex Gauss
actions, positive fixed alpha/E_star and hbar, and the admitted P2 map J.
H=H_lambda=H_E+alpha lambda Vmag, lambda>=0, P=JJ*, Q=1-P.
Let A=A_lambda=H_eff+alpha lambda(20-b), B=B_lambda=alpha lambda B1,
B1=QVmag J, and C=C_lambda=C0+alpha lambda QVmag Q on QHphys,
where C0=H_E restricted to Q. Q1 gives

    ||Vmag||=40,  0<=Vmag<=40,
    B1*B1=M_k,  4<=k<=25/4,  ||B1||=5/2.

P reduces H_E. Thus the full block realization of H has diagonal A,C
and off-diagonal B*,B on

    J D(A) direct-sum D(C)=D(H_E),
    D(A)=H2(SU2^3)∩H3,  D(C)=QD(H_E),
    form domains H1∩H3 and QD(H_E^(1/2)).

These are the bounded real-multiplier perturbations of the admitted
electric operators; they are self-adjoint and nonnegative. Smooth
invariant Peter-Weyl polynomials are cores. B is bounded between the
sectors, so the block matrix does not require an additional off-diagonal
domain assumption. All bounds below hold for every lambda>=0, in
particular throughout the required 0<=lambda<=1/100.

Here the needed complementary gap follows directly from the physical
graph, not from an inherited stability threshold. In the full product
Peter-Weyl decomposition, assign an SU2 spin j_e to each edge. H_E has
energy alpha sum_e j_e(j_e+1). Gauge averaging preserves each such finite
label block. A nonzero invariant tensor cannot have a vertex incident
to precisely one nontrivial edge representation: that irreducible
representation has no invariant vector. Hence every nonempty active
edge support has no degree-one vertex and contains a cycle. The actual
graph is simple and bipartite, with girth four. Such a support contains
at least four active edges, each costing at least 3/4. The only zero
label block is the constant. By the complete orthogonal decomposition,

    H_E >= 3alpha on 1-perp.

Since 1 belongs to ran(J), QHphys is contained in 1-perp. The physical
face W0 has energy 3alpha and zero conditional mean, so 2W0 is a unit
vector in Q attaining the bound. Thus inf spectrum(C0)=3alpha exactly,
and positivity of the magnetic compression gives C_lambda>=3alpha.
This argument controls all representations, with no spin cutoff.

## 2. Exact memory and Schur relations

Define K_lambda(s)=B*exp(-sC/hbar)B (units energy²) and
Sigma_lambda(z)=B*(C+z)^-1 B (units energy), s>=0,z>0.
Set T(t)=J*exp(-tH/hbar)J and R(t)=Qexp(-tH/hbar)J. For initial selected
vectors in D(A), the common-domain block equations are

    hbar T'=-A T-B*R,   hbar R'=-C R-BT,   T(0)=I, R(0)=0.

Solving the second equation in its mild sense gives
R(t)=-hbar^-1 integral_0^t exp(-(t-u)C/hbar) B T(u) du. Consequently

    hbar T'(t)=-A T(t)+hbar^-1 integral_0^t K_lambda(t-u)T(u)du,

and the all-vector exact integrated identity is

    T(t)=exp(-tA/hbar)+hbar^-2 integral_(0<=u<=s<=t)
          exp(-(t-s)A/hbar) K_lambda(s-u) T(u) du ds.

All integrals are strongly continuous vector-valued integrals, extended
from the core by bounded B and semigroup bounds. The derivative equation
is understood on its stated initial operator domain; the integrated
equation holds on all H3. The last factor must remain T(u): replacing
it by exp(-uA/hbar) drops returns through the complementary sector.
This is a different exact formula from Q1's symmetric double-Duhamel
identity, whose middle factor used the full H semigroup.

Eliminating the complementary component in (H+z)psi=Jf gives

    J*(H+z)^-1 J = [A+z-Sigma_lambda(z)]^-1.

Indeed the complementary component is -(C+z)^-1 B u, which fixes the
minus sign. Sigma is bounded, so the Schur operator is self-adjoint on
D(A). Minimizing the positive quadratic form of H+z over the complement
shows this operator is >=zI, hence invertible. This also justifies the
domain of the reconstructed complementary vector. The spectral theorem
gives Sigma(z)=hbar^-1 integral_0^infinity exp(-zs/hbar)K_lambda(s)ds,
with the strong integral absolutely norm-bounded. No finite-dimensional
projection is used in these exact identities.

## 3. Full-Hilbert leading approximations and remainders

Define K^(2)(s)=(alpha lambda)² B1*exp(-sC0/hbar)B1 and
Sigma^(2)(z)=(alpha lambda)² B1*(C0+z)^-1 B1. These are operators on
the entire infinite-dimensional H3, not just on the two test channels.
Let sigma=alpha s/hbar. The exact gap gives

    ||K_lambda(s)||, ||K^(2)(s)|| <= (25/4)alpha² lambda² exp(-3sigma),
    ||Sigma_lambda(z)||, ||Sigma^(2)(z)||
       <= (25/4)alpha² lambda²/(3alpha+z).

Bounded-perturbation Duhamel on the common domain of C,C0, using both
semigroup decays and ||QVmag Q||<=40, gives

    ||K_lambda(s)-K^(2)(s)||
       <=250 alpha² lambda³ sigma exp(-3sigma).

The estimate is zero at s=0 and uniform for all delays:
sup_s remainder <=250 alpha² lambda³/(3e). This is absolute uniform
control. Its displayed ratio to the leading norm envelope is 40lambda
sigma, which is not a uniform long-delay relative bound. No operator-norm
time Taylor expansion is claimed.

The second resolvent identity similarly gives

    ||Sigma_lambda(z)-Sigma^(2)(z)||
       <=250 alpha³ lambda³/(3alpha+z)²
       <=(250/9)alpha lambda³,  z>0.

Thus the absolute error is uniform as z decreases to zero. The
self-energy itself extends to z=0 using C_lambda>=3alpha; the compressed
full resolvent assertion above remains stated for z>0. Positivity also
implies 0<=Sigma_lambda(z)<=Sigma^(2)(z) by resolvent order. No analogous
operator ordering of the heat kernels is assumed. The constants 250
arise explicitly as (25/4)*40. These controlled lambda² leading operators
and lambda³ remainders require neither a fitted clock nor a small-denominator
assumption beyond the proved physical complementary gap.

## 4. Analytically closed electric spectral sector for the fixed channels

The fixed orthonormal selected vectors are f0=1 and f1=2x=Tr U.
The physical x completion is P2's six-link loop
L=(14-,2+,28+,3-,15+,26-), never P1's four-link F9.
By Q1, writing F_p=W_p and I={0,...,19} minus {8},

    g0=B1 f0=-sum_(p in I) F_p,
    g1=B1 f1=-sum_(p in I) phi_p,  phi_p=2x F_p.

These are actual physical invariant polynomials in Q. Every F_p has
energy 3alpha and squared norm 1/4. Distinct faces are orthogonal by
their distinct central-edge parities.

Independently enumerating the actual intersection of L and each face
gives the following complete classification:

| Shared-edge count k | Face IDs (face8 excluded) | Count |
|---|---|---:|
| 0 | 4,5,6,7,11,13,14,18,19 | 9 |
| 1 | 0,1,10,12,16,17 | 6 |
| 2 | 2,3 | 2 |
| 3 | 9,15 | 2 |

For every k>0 the shared edges form one connected path, with no branching.
The two remaining paths are nonempty and edge-disjoint. Their holonomies
and the shared path holonomy are independent Haar variables. Reverse a
whole loop if necessary (its SU2 trace is unchanged) to write

    phi=2 t(GA)t(G^-1 B),  t(M)=Tr(M)/2.

As a function of G, the product of two fundamentals contains only spin
0 and spin1. Haar projection gives phi_s=t(AB)/2, and phi_t=phi-phi_s.
Equivalently on unit quaternion coordinates the Casimir identity
C(q_i q_j)=2q_i q_j-delta_ij/2 makes every trace-free quadratic an
exact energy-2 function, while its constant part has energy zero.
Every shared original edge has the same spin because it occurs only
through the path product G. Each remaining edge is fundamental. Thus
these are exact electric eigenvectors with dimensionless energies

    e_s=(3/4)(10-2k)=15/2-3k/2,
    e_t=e_s+2k=15/2+k/2.

Integration over independent A,B,G gives ||phi||²=1/4,
||phi_s||²=1/16 and ||phi_t||²=3/16, with orthogonality. For k=0,
phi itself has energy 15alpha/2 and squared norm 1/4. This proves
finite spectral closure of these specific vectors without truncating
the physical Hilbert space. The checker verifies singlet projection and
the actual 33-link Casimir action on noncommuting fixtures for all faces.

Different phi_p have different edge-center parity sets L symmetric-difference
boundary(p), so their entire electric spectral sectors are orthogonal.
A cross term between F_p and phi_q can survive only if
boundary(p)=L symmetric-difference boundary(q). Exact graph enumeration
leaves (p,q)=(9,15),(15,9). Their singlet pieces are respectively
F9/2 and F15/2, giving cross inner product 1/8 each. Thus the total
off-diagonal spectral weight is +1/4 at energy 3alpha. The sign is
also checked directly from Q1: <f0,M_k f1>=2 E[xk]=1/4.

## 5. Exact leading two-channel matrices for all delay and energy

Let W_e be the following real symmetric spectral-weight matrices; omitted
entries in the table are zero:

| e=energy/alpha | (W_e)00 | (W_e)01=(W_e)10 | (W_e)11 |
|---|---:|---:|---:|
| 3 | 19/4 | 1/4 | 1/8 |
| 9/2 | 0 | 0 | 1/8 |
| 6 | 0 | 0 | 3/8 |
| 15/2 | 0 | 0 | 9/4 |
| 8 | 0 | 0 | 9/8 |
| 17/2 | 0 | 0 | 3/8 |
| 9 | 0 | 0 | 3/8 |

With the fixed orthonormal channel inclusion F:C²->H3, the complete
answers are

    F* K^(2)(s) F=(alpha lambda)² sum_e exp(-e alpha s/hbar) W_e,
    F* Sigma^(2)(z) F=(alpha lambda)² sum_e W_e/(e alpha+z).

The full-Hilbert remainder bounds in section 3 apply to these matrices
without any extra factor. Each weight matrix is positive semidefinite.
At s=0 their sum is [[19/4,1/4],[1/4,19/4]], matching the exact leakage
multiplier's channel compression. Equality of its two diagonal entries
alone would be a nondiscriminating test. The off-diagonal entry and the
nonconstant channel's spectral energies reject a scalar/reference shortcut:

    M00(s)=(19/4)exp(-3sigma),  M01(s)=exp(-3sigma)/4,
    -dM00/dsigma(0)=57/4,  -dM11/dsigma(0)=285/8.

For example at z=alpha, the dimensionless self-energy matrix divided by
alpha lambda² has entries 19/16, 1/16, 2285061/3979360 in positions
00,01,11 respectively. These are exact rational evaluations of the
displayed spectral sum, not fitted or measured data. The leading
two-channel kernel is not the generator of a closed two-dimensional
selected semigroup; the exact Volterra equation still acts on all H3.

## 6. Scalar shifts, controls, and scope

A common energy shift d changes H,A,C to H+d,A+d,C+d while leaving B
unchanged. Then K_d(s)=exp(-ds/hbar)K(s), T_d(t)=exp(-dt/hbar)T(t),
and Sigma_d(z)=Sigma(z+d). For an unchanged physical resolvent use the
compensating spectral shift z->z-d, wherever the resolvents exist. One
must not shift C while leaving its spectral energy unadjusted. The
Schur minus sign and memory-return factor are tested on an exact
noncommuting finite block; that fixture is an algebra control only.
At lambda=0, K=Sigma=0 and P2 electric reduction is recovered exactly.

Primary-source reading and the actual hypothesis match are in source notes.
The proof, independent exact graph/representation controls, and all source
closures are separately recorded. The reference f0 is Haar/electric,
not the interacting ground. The complete H_lambda remains Q1's fixed
finite-graph magnetic deformation; neither an interacting ground theorem,
homogeneous stability, physical calibration, autonomous finite closure,
nor a continuum result is inferred. No R1 work is selected or executed
by this producer. Scientific priority remains unverified.
