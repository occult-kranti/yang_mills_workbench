# AJ1 reverse: local regularity and the actual homogeneous physical GNS space

Independent reverse derivation for investigation 7. Current forward AJ1 and
skeptic AJ1 science remained unread through this freeze. The advisor selected
the target and suggested the vacuum-reset route before production; neither
suggestion was an inherited local-energy theorem. The conclusion below is a
representation result for the actual I1 state, not a new numerical gap theorem.

For every fixed finite complete-factor region R, the finite-volume I1 ground
states have uniformly bounded local reference energy. Their local densities
converge in trace norm to the actual I1 limit. This proves local normality and
normality of its represented local algebras. Endpoint Haar averaging is
compatible with that GNS representation, and the full bounded physical local
algebra generates exactly the joint gauge-fixed vector space. This space
reduces the inherited closed, centered generator G. Thus its physical energy
restriction has the inherited threshold alpha/16, on I1's symbolic coupling
interval only. No nonzero physical excitation is established here.

## 1. Reconstruct the premises required by the target

The desired restriction requires three separate facts: compatible averaging
for the actual state, equality of physical cyclic and fixed vectors, and
commutation with the closed generator. Invariance of an abstract state alone
would not supply the first fact. Nor would a finite matrix compression supply
the last. Sections 3–6 establish them in that order.

Retain I1's positive coarse orthant, full link Haar factors and selected-strip
assignment. A coarse site b=(i,j,k) owns every positive-direction link whose
tail lies in

    T_b = {(4i+r,2j+s,k): 0<=r<4, 0<=s<2}.

Euclidean division gives unique ownership of every positive orthant link. Each
site has 24 links: the complete ten-link selected three-face strip and fourteen
free links. Link heads may lie beyond the site's or finite volume's boundary.
Every endpoint has its original SU(2) action. The unconstrained site spaces
factor; the Gauss-constrained space is not assumed to factor.

Let delta=alpha/8, with alpha, hbar, spacing a, E_star and alpha/E_star fixed
positive. For the fixed inherited selected coefficients,

    h_b = (H_strip,b-E_strip,b + alpha sum_free C_e)/delta,
    h_b >= I-P_b,  h_b Omega_b=0,
    S = {0,e_x,e_y,e_z},
    phi_b = -(tau/3) sum_(21 omitted anchored faces) W_f,
    M=7|tau|,   ||phi_b||=M.

The onsite vacuum is unique by the inherited A1/I1 theorem. The actual model
on a finite coarse cuboid Lambda is

    Hhat_Lambda = sum_(b in Lambda) h_b
                 + sum_(b+S subset Lambda) phi_b.                 (1)

All 21 faces of a retained star remain, even when an individual face's actual
support uses only two or three of the four sites. A face at p in axes a<c has
owners pi(p), pi(p+e_a), pi(p+e_c), where
pi(x,y,z)=(floor(x/4),floor(y/2),z). There is no diagonal-corner link tail. The
six omitted support multiplicities are 1,3,1,10,2,4, for {0,ex}, {0,ey},
{0,ex,ey}, {0,ez}, {0,ex,ez}, {0,ey,ez}, respectively. Their union is S.
The common signed Wilson sum has norm M because its modulus approaches 21
near the identity configuration on positive Haar measure sets. For N complete
anchors the homogeneous global perturbation norm is NM by the same argument;
it does not converge as a bounded global perturbation at nonzero tau.

The regime is exactly

    |tau| < tau_* = min(c1(S),1/(2c2(S)))/7,                     (2)

with positive, unevaluated source constants. Zero coupling is included. I1
already supplies unique finite grounds, the specified whole-star orthant
local-state limit omega, its centered full-algebra GNS generator G, and
Spec(G) subset {0} union [1/2,infinity), with a unique ground Omega. No
particular positive numerical tau is chosen. The current I1 gate is revision
2; the archive correction changes the planning interpretation, not these
inherited results. J2's dyadic state, representation, numerical threshold and
Wilson variance are different premises and are not imported.

## 2. Unbounded local energies and the source's actual topology

On one full site K_b=sum_(24 links) C_e has the product Peter–Weyl basis.
Writing k=2j, each link has energy k(k+2)/4 and multiplicity (k+1)^2. A bounded
electric energy permits only finitely many labels, each with finite
multiplicity. Hence K_b and every finite-site sum have compact resolvent,
operator domain the corresponding product H^2 space and form domain H^1.
The strip potential has physical norm at most 9alpha/8; its Haar vacuum
expectation is zero. Thus -9alpha/8 <= E_strip,b <= 0 and

    ||h_b-8K_b|| <= 18,           h_b >= 8K_b-9.                 (3)

Bounded self-adjoint perturbation gives the same operator/form domains and
compact resolvent. This applies to h_R=sum_(b in R) h_b and to (1), whose
finite perturbation is bounded. In particular its ground lies in D(sum h_b),
so all local positive reference-energy expectations used below are finite.

Let P_T=1_[0,T](h_R). It is finite rank and increases strongly to I. For an
explicit finite bound, min-max and (3) give

    rank P_T <= rank 1_[0,B](sum_(24|R| links) C_e),
    B=(T+9|R|)/8,
    rank P_T <= [sum_(k=0)^floor(4B/3) (k+1)^2]^(24|R|).        (4)

This is a loose rank bound, not an interacting eigenvalue calculation. It
uses k(k+2)>=3k for every integer k>=0 and retains all full link factors.

The primary source is Yarotsky, arXiv:math-ph/0411042v1. Theorems 2–3 give
pointwise ground-state limits on B(H_R) and resolvent matrix elements tested
between A Omega_Lambda and B Omega_Lambda and their GNS counterparts. Section
2 uses creation vectors with u_I in H'_I intersect D(H0,I); essential
self-adjointness is attributed to the source. These are inherited theorems,
not a same-Hilbert-space strong resolvent assertion. Here

    hat(u_I)=|u_I><Omega_I,0|,
    [H0,hat(u_I)]=|H0,I u_I><Omega_I,0|,

and only finitely many incident bounded interactions contribute to its other
commutator. The domain condition makes this bounded local commutator valid.
Arbitrary bounded local A need not put pi(A)Omega in D(G), or even its form
domain. Our generator transfer uses the tested resolvent limit, so it needs
no new assertion that all local vectors are an operator core.

For clarity, the orthant transfer used in I1 sets all outside-orthant anchors
to zero on Z^3, with gapped spectator reference sites there. The nonnegative
star offsets make the positive and negative subsystems decouple. Symmetric
cuboid grounds factor into the positive-orthant ground and negative vacua.
The limiting state is their product on local factors. For an orthant A,
its finite excitation has the spectator vacuum, so the full centered
resolvent acts as the positive-system resolvent on this vector. In the product
GNS construction the spectator-vacuum sector reduces the limiting resolvent:
finite-volume off-sector matrix elements vanish, and products of local
excitations are dense. Its restriction supplies exactly I1's orthant tested
resolvent limit. No physical Gauss reduction or summable representation is
used in that transfer. It identifies no other thermodynamic boundary family.

## 3. A local vacuum reset proves the missing regularity

Write rho_Lambda for the finite-volume ground density and R subset Lambda
for any finite complete-factor region. Define

    I_Lambda(R)={b: b+S subset Lambda, (b+S) intersect R nonempty},
    n_Lambda(R)=|I_Lambda(R)|,
    I_+(R)={r-s: r in R, s in S, r-s in the positive orthant}.

Each incident anchor must equal r-s, and conversely an allowed such anchor
meets R. Therefore

    I_Lambda(R)=I_+(R) intersect {retained anchors},
    n_Lambda(R)<=n_+(R)<=4|R|.                                 (5)

This includes incoming as well as outgoing stars. Define the normal reset
state on the original full tensor factors by

    rho'_Lambda = |Omega_R><Omega_R| tensor Tr_R rho_Lambda,
    Omega_R = tensor_(b in R) Omega_b.                          (6)

It has trace one. Its reference energy in R is zero; the energy outside R is
unchanged. To justify this with unbounded operators, first use bounded
spectral truncations of the nonnegative exterior reference sum and the
partial-trace identity, then pass by monotone convergence. The original
finite ground has finite reference energy, so the exterior energy is finite
for both states. Consequently (6) has finite reference form energy and is a
valid trial density for the semibounded variational principle. Neither
operator-domain membership of every vector in that mixed state nor a bounded
infinite-volume perturbation is needed.

The variational inequality is
Tr(rho'_Lambda Hhat_Lambda) >= E_Lambda = Tr(rho_Lambda Hhat_Lambda).
Subtract these two finite energy expressions. Every nonincident interaction has unchanged expectation by
partial trace; all exterior reference energies cancel; each incident
interaction changes by at most 2||phi_b||. Thus

    Tr(rho_Lambda,R h_R)
      <= sum_(b in I_Lambda(R)) Tr((rho'_Lambda-rho_Lambda)phi_b)
      <= 2M n_Lambda(R) <= C_R:=2M n_+(R)<=8M|R|.              (7)

The displayed first right-hand sum is necessarily nonnegative for the actual
ground; no positivity of individual interaction differences was assumed.
The actual finite ground scalar E_Lambda cancels. The onsite shifts E_strip,b
were already retained in h_b and make Omega_R have precisely zero energy.
Dropping crossing stars or substituting an approximate scalar would not
justify (7). This bound holds for either coupling sign and does not require
an evaluated stability constant, beyond the inherited existence of the
chosen ground. In terms of the physical coupling, C_R<=56|tau||R|.

By spectral order, with T>0,

    Tr(rho_Lambda,R (I-P_T)) <= C_R/T.                         (8)

For any density rho and orthogonal P, let e=Tr(rho(I-P)). The off-diagonal
blocks have trace norm at most sqrt(e) by the Hilbert–Schmidt product
inequality; the omitted positive diagonal block has trace e. Hence

    ||rho-P rho P||_1 <= 2 sqrt(e)+e.                         (9)

The finite matrix block P_T rho_Lambda,R P_T converges entrywise, hence in
trace norm, because each matrix unit is a bounded local observable and I1
supplies its pointwise state limit. Given epsilon, first choose T so that
2sqrt(C_R/T)+C_R/T is small, then choose sufficiently large volumes for the
finite block to be Cauchy. Equations (8)–(9) show the full densities are
trace-norm Cauchy. Their limit rho_R is positive with trace one, and

    omega(A)=Tr(rho_R A),  A in B(H_R),
    ||rho_Lambda,R-rho_R||_1 -> 0,
    Tr(rho_R h_R)<=C_R.                                      (10)

The last claim follows from each bounded truncated h_R and monotone
convergence. This proves actual local normality, rather than assuming it
from weak-star convergence. No rate in volume is supplied. At tau=0, (7)
forces the local vacuum density, as expected.

One needs represented regularity as well. If 0<=A_i increases to A in
B(H_R), bounded above, and B is any bounded operator in another finite
region, local normality in the union region gives

    <pi(B)Omega, pi(A-A_i)pi(B)Omega>
      = omega(B*(A-A_i)B) -> 0.

Such pi(B)Omega are dense. Uniform boundedness and positivity extend this to
all GNS vectors and give strong monotone convergence. Therefore pi restricted
to each original local von Neumann algebra is normal. More directly, for a
bounded original strong-star convergent local family X_i->0,

    ||pi(X_i)pi(B)Omega||^2=omega(B*X_i*X_i B)->0               (11)

by normality on the union region; the same dense extension applies. This
is the continuity used next. It is not point-norm continuity on B(H_R).

## 4. Gauge invariance, continuity and compatible Haar averaging

For a finite endpoint set V, let Gamma_V=product_(v in V) SU(2). On finite
link factors the actual gauge unitary is given by left/right regular
translations at both endpoints, tensoring over every owned link. On smooth
Peter–Weyl vectors it is continuous; its norm-one extension is strongly
continuous. Each Casimir commutes with both translations, and every closed
Wilson word telescopes to conjugation at its base. The trace is unchanged.
Thus the full finite Hamiltonian, including every selected and retained
omitted face, commutes with these unitaries on its domain and resolvent.
Outgoing free links retain their head transformations, including vertices
outside the tail-owned cuboid.

Uniqueness makes the finite ground transform by a continuous character of a
finite product of SU(2). Such characters are trivial: every SU(2) element is
conjugate to diag(exp(it),exp(-it)); this diagonal is a commutator of
D=diag(exp(it/2),exp(-it/2)) with the matrix interchanging the two coordinates
with determinant one, since that matrix conjugates D to D^(-1). Characters
annihilate commutators. The finite ground vector is therefore fixed, not
merely its rank-one projection. The same reasoning applies to onsite vacua.
Finite-state convergence then gives omega(beta_g(A))=omega(A) for every local
A and finite endpoint g, and by norm approximation on the full algebra.

Define on the full cyclic domain

    U_omega(g)pi(A)Omega=pi(beta_g(A))Omega.                   (12)

Invariance preserves the GNS seminorm and null ideal; the inverse g^(-1)
makes (12) a unitary. It fixes Omega and has the group law. For a local A,
conjugation by the original finite-link translations is bounded strong-star
continuous with support still inside the same complete-factor region R.
Equation (11) proves continuity of (12) on pi(A)Omega. Density and unitarity
give strong continuity on the whole homogeneous GNS space for each finite
endpoint group. This does not assert operator-norm continuity of beta on
every bounded operator.

For A in B(H_R), average over all endpoints V(R) of the complete owned links:

    E_R(A) = integral_(Gamma_V(R)) beta_g(A) dg.               (13)

In the original local algebra this is a weak operator/ultraweak integral,
with norm at most ||A||. Strong continuity on vectors gives its scalar
matrix elements and bounded sesquilinear form. The integral stays in
B(H_R), since that factor is strongly/weakly closed. Haar invariance makes
it fixed under every group at these endpoints; all other vertices act
trivially on its support. This is an element of the full local physical
algebra. No Wilson-only density assertion is needed.

The original bounded operator orbit is also ultraweakly continuous. Since
the represented local algebra is normal, (13) can be passed through pi in
all represented scalar matrix elements. Independently the represented
vector orbit is strongly continuous by (12), so its Bochner vector integral
exists. These facts identify the two objects:

    pi(E_R(A))Omega
       = integral_(Gamma_V(R)) U_omega(g)pi(A)Omega dg.         (14)

This establishes the needed compatibility in the actual homogeneous
representation; an arbitrary representation would not justify it.

## 5. Physical cyclic vectors, fixed vectors and the null quotient

Let A_phys be the norm closure of every bounded local operator invariant
under all finite endpoint transformations. Define

    H_cyc=closure(pi(A_phys)Omega),
    H_fix=intersection_g ker(U_omega(g)-I).

Equation (12) immediately gives H_cyc subset H_fix. Conversely, for xi in
H_fix, full GNS cyclicity and norm density of the local algebra give local A
with ||pi(A)Omega-xi||<epsilon. Average A over its full endpoint set. The
vector integral in (14) is an orthogonal projection onto that finite-group
fixed space, fixes xi and contracts norm. Therefore

    ||pi(E_R(A))Omega-xi|| <= ||pi(A)Omega-xi|| < epsilon.

Since E_R(A) is a local physical observable,

    H_cyc = H_fix.                                           (15)

There is no infinite-group Haar probability assumed here: each approximant
uses one finite compact endpoint product, while xi is fixed under every
finite transformation. The gauge-constrained Hilbert space does not enter
as an assumed tensor product.

For omega restricted to A_phys, the null left ideal is
N_phys={A:omega(A*A)=0}={A:pi(A)Omega=0}. On its quotient the map

    W_phys:[A] -> pi(A)Omega

is well defined and isometric, with inner product omega(A*B). Completion
makes it a unitary onto (15), intertwining left multiplication with the
restricted represented physical algebra. This is the actual physical GNS
identification. It neither claims full-space cyclicity for A_phys nor proves
that its cyclic space has any nonvacuum vector.

## 6. The actual closed generator and physical scales

Use the source topology without a domain shortcut. Let
R_Lambda(z)=(Hhat_Lambda-E_Lambda-z)^(-1), z nonreal. For sufficiently large
cuboids containing the complete supports of A, B and a fixed endpoint gauge
action g, finite gauge commutation and ground invariance give

    <R_Lambda(z) beta_g(A)Omega_Lambda,
                         beta_g(B)Omega_Lambda>
        = <R_Lambda(z) A Omega_Lambda, B Omega_Lambda>.

I1's tested matrix-element limit, with those same bounded local operators,
yields U_omega(g)^* (G-z)^(-1) U_omega(g)=(G-z)^(-1) on dense cyclic vectors,
and hence everywhere by boundedness. Both z and its conjugate are covered.
Thus every U_omega(g) commutes with the closed spectral resolution of G and
preserves its operator and form domains. One could additionally check formal
covariance on the source's restricted creation vectors; no such check can
replace the closed resolvent argument just given.

Each resolvent and its adjoint maps the joint fixed space (15) into itself.
That space therefore reduces G. Its spectral projections restrict there,
and spectral cutoffs show that the following domain is dense:

    G_phys=G|H_cyc,    D(G_phys)=D(G) intersect H_cyc,
    D(sqrt(G_phys))=D(sqrt(G)) intersect H_cyc.                (16)

This is a self-adjoint restriction, not the compression P G P on an arbitrary
subspace. Its zero eigenvector is the same Omega and is unique. The inherited
normalized spectral inequality restricts to it. In physical units,

    H_phys = (alpha/8) G_phys,
    Spec(H_phys) subset {0} union [alpha/16,infinity),
    Stone frequency generator = H_phys/hbar.                (17)

The centered implementing group fixes Omega. Physical Heisenberg evolution
may be represented by exp(it H_phys/hbar); heat uses exp(-t H_phys/hbar).
Neither statement supplies a new norm-continuous dynamics on every bounded
quasilocal observable. No bounded infinite-volume dressing unitary, chosen
numerical coupling interval, positive Wilson variance, lowest physical
excitation value, continuum construction or scientific priority follows.
Even the physical spectrum above zero could be empty on the information
proved here; a nonzero invariant excitation requires another argument.

## 7. Exact fixtures and discriminating controls

The new standard-library checker reconstructs oriented links and faces rather
than executing or importing a historical checker. All full lists are in
geometry.json. The three prescribed cuboids give:

| Coarse side counts | Sites | Owned links | Endpoint vertices | Outgoing links | Retained anchors | Omitted faces |
|---|---:|---:|---:|---:|---:|---:|
| (2,2,2) | 8 | 192 | 120 | 56 | 1 | 21 |
| (3,2,2) | 12 | 288 | 176 | 80 | 2 | 42 |
| (3,3,3) | 27 | 648 | 342 | 126 | 8 | 168 |

Boundary singleton {0}, pair {0,ex}, and singleton {(1,1,1)} appear in every
fixture. The last is an upper-boundary site in the smaller cuboids and has
no retained incident star there; in (3,3,3) all four incident anchors appear,
three of them incoming. The orthant counts are respectively 1,2,4, so the
corresponding uniform coefficients C_R/M are 2,4,8. The pair's sole
actual-support-contained omitted face is absent from its whole-star empty
boundary; the two prescriptions cannot be interchanged.

Rational unit quaternions test full endpoint covariance of every retained
oriented face, and a missing head action changes an explicit Wilson value.
The Q8 subgroup average of the fundamental representation vanishes exactly;
a center flip changes a charged open link while closed traces are invariant.
These finite tests support the implemented identities. Full SU(2) Haar
statements use invariance/telescoping in Section 4, not subgroup completeness.

The additional controls have explicit, different roles:

* A local reset on an entangled two-site density verifies normalization,
  removal of local reference energy and preservation of exterior energy.
  It is bookkeeping, not a finite surrogate for (7). Complete all-volume
  incidence and the variational proof establish that bound.
* Normal vector states escaping every finite-rank cutoff have a singular
  weak-star cluster state on B(l2). Its value on every finite-rank projection
  is zero and on I is one. The divergent local energies violate the new
  tightness premise and show why weak-star convergence alone was insufficient.
* The strongly continuous U(t)e_n=exp(int)e_n and bounded A e_n=e_(2n)
  satisfy ||beta_(pi/k)(A)-A||=2, witnessed on e_k. Thus strong unitary
  continuity does not give point-norm continuity on all bounded operators.
* For an explicit weak-average obstruction, take the compact profinite
  group product_N Z2, H=direct_sum_N C2, U(g)|n=diag(1,g_n), and
  A=direct_sum sigma_x. Its original weak operator Haar average is zero.
  A free-ultrafilter cluster of vector states on (e_(n,0)+e_(n,1))/sqrt(2)
  evaluates beta_g(A) as lim_ultrafilter g_n. This scalar function is not
  Haar measurable: its plus event is invariant under any finite coordinate
  change and hence, if measurable, has probability zero or one by the product
  tail law; global sign reversal preserves measure and exchanges plus and
  minus, forcing probability one half. Thus a general GNS average may not
  even be integrable. This abstract compact-group countermodel is not the
  finite SU(2) endpoint model. Its finite sign-twirl checks are diagnostics;
  the analytic tail argument supplies nonmeasurability. AJ1's proved normal
  representation excludes precisely this unjustified transfer.
* For h e_n=n^2 e_n, v_n=1/n lies in l2 while its energy form diverges.
  The bounded rank-one A=|v><e0| sends the ground to a vector outside the
  form and operator domains. Finite prefixes verify the exact divergent
  sums; the series argument proves the obstruction.
* An explicit projection mixing energy-3 and energy-5 vectors of a centered
  three-level model fails resolvent/spectral reduction and gives compressed
  value 4. The same fixture retains the raw ground -2, its subtraction and
  delta=alpha/8. J2's 973alpha/8640 is not silently substituted for alpha/16.
* A two-dimensional model with symmetry diag(1,-1), vacuum e0 and energy
  diag(0,1) has one-dimensional physical cyclic/fixed space. Its inherited
  restricted gap inequality holds, but it has no positive physical spectral
  measure. The inequality alone cannot prove a Wilson excitation.

The missing-head control initially meets a blind candidate: the chosen head
gauge element is the identity, so omitting it changes nothing. The deterministic
link scan retains every blind candidate and its gauge value before recording
a discriminating replacement. This is a control repair within AJ1, not another
investigation. The preliminary input snapshot command had an administrative
parsing typo, failed before any write, and was corrected; input-pack-attempt.json
preserves it separately. The
finite checks do not establish all-volume geometry completeness, normality,
infinite-group equality or an infinite-dimensional generator theorem.
Those claims come from the explicit proofs above.

## 8. Sources, reproducibility and remaining scope

The 49 original repo snapshots include the exact contract and all 48 declared
sources. The 26 actual instruction files match previously applied/read
instructions; three main skill files were reopened. Two new arXiv retrieval
records preserve the exact primary topology/core passages used. The reading
ledger separates direct passages, inherited proofs, previous readings and
project-context summaries. The immutable six-loop draft/network are current
knowledge: AG's spent support weights, AI's candidate-indexed clocks and AH's
finite-graph exact-heat certificates supply no substituted AJ1 physical premise.

Source novelty is unverified. The inherited stability theorem is established
literature; the present work supplies an explicit local-energy/tightness and
averaging application to this workbench's actual complete homogeneous model.
The source creation-core proof is attributed, not claimed as independently
reconstructed. No historical or occult source contributes a new physical
coefficient here.

From the repository root, each destination must be absolute and absent:

```bash
python -B research/round28/reverse/aj1/check.py --output /absolute/fresh/aj1-normal
python -B -O research/round28/reverse/aj1/check.py --output /absolute/fresh/aj1-optimized
```

Both runs produce results.json and geometry.json; explicit exceptions make
checks independent of Python assert optimization. The output binds the active
checker, report, original sources, snapshots, actual instruction originals and
manifests. The freeze binds every owned file except precisely the top-level
freeze.json, including every nested historical freeze snapshot. Fresh normal
and optimized bytes are compared in verification.json.

The next question is not selected here. An actual nonzero physical invariant
fluctuation or its precise obstruction would strengthen nonvacuity. Evaluated
stability constants, boundary-state equivalence, a matched continuum theory,
and the Yang–Mills mass gap remain separate unresolved goals. This report
executes AJ1 only; no AJ2 or fifth-goal science has started.
