# Q2 independent preparation

This preparation uses the frozen Q2 contract and admitted C1/P2/Q1 evidence.
Neither current Q2 producer has been read. It supplies independent comparators
and rejection conditions, not an admission or an R1 calculation. The exact
model, Haar map, fixed physical clock, and fixed f0=1,f1=2x are retained.

## Actual complementary spectrum

In the physical link Peter-Weyl decomposition, the electric eigenvalue is
alpha sum_e j_e(j_e+1). At every gauged vertex, incident representations must
contain a singlet. A vertex with just one incident nontrivial representation
cannot do so. Thus the nontrivial-edge support of a nonvacuum physical basis
vector has no degree-one vertex and contains a cycle. The actual simple open
rectangular graph has no self-loop, doubled edge or triangle; every cycle has
at least4 edges. Every nontrivial edge contributes at least3/4. Therefore

    H_E >= 3alpha (I-|1><1|).

This argument uses the complete physical Peter-Weyl decomposition, not a
spin cutoff. It extends from its invariant core to the closed form. P contains
the constant vacuum; hence C0=H_E|Q>=3alpha. W0 is nonzero, in Q because its
conditional mean vanishes, and has energy3alpha. The complementary spectral
bottom is therefore exactly3alpha, attained in this actual graph.

For lambda>=0, W=alpha lambda QVmagQ is bounded positive, ||W||<=40alpha lambda.
Thus C_lambda=C0+W is self-adjoint on D(C0), retains its form domain and is
bounded below by3alpha. No homogeneous stability gap or spatial/regulator
limit is used.

## Fixed-channel exact electric sectors

Let R=sum_(p!=8) Wp. Q1 gives B1 f0=-R and B1 f1=-chi_U R, where
chi_U=2x=Tr U. The actual original-link word of U is

    (14,-1),(2,+1),(28,+1),(3,-1),(15,+1),(26,-1).

It is a simple6-edge loop. The checker reconstructs this root-based word and
every original signed face independently. All Wp have electric energy3alpha,
so g0=B1f0 lies entirely at that energy. Its norm squared is19/4.

For each p!=8 put v_p=chi_U Wp. Different v_p have different edge-center
parities U xor face_p. Center flips commute with H_E, so these vectors and
all their electric spectral components are mutually orthogonal. The only
cross parities between Wp and v_q are(p,q)=(9,15),(15,9).

Every nonempty U/face overlap is one connected shared path of k edges; its
symmetric difference is a simple loop with10-2k edges. The exact census is:

| Shared path length k | Face IDs | Count |
|---|---|---|
| 0 | 4,5,6,7,11,13,14,18,19 | 9 |
| 1 | 0,1,10,12,16,17 | 6 |
| 2 | 2,3 | 2 |
| 3 | 9,15 | 2 |

For k0 the loops have disjoint edge sets, so v_p has energy15alpha/2 and norm
squared1/4. For k>0, cyclic trace invariance and reversal let the two traces
be expressed using one shared path holonomy G and two edge-disjoint remaining
paths A,B. In an orientation with both shared factors G, their product is
v=Tr(GA)Tr(GB)/2. As a function of the unit quaternion G it is quadratic.
Its Haar-constant part is v0=Tr(AB^-1)/4 and its remaining part v1=v-v0 is
traceless quadratic. The constant part has shared-edge spin0, and v1 has
shared-edge spin1 on every one of the k shared edges. This follows directly
from C_G(q_a q_b)=2q_a q_b-delta_ab/2, with the frozen normalization C=-Delta_S3/4.
Products along the shared path transform by the same left/right Casimir;
there are no independently assignable spin choices at its internal vertices.
Each unshared edge remains a fundamental matrix coefficient.

Consequently the two exact energies and squared norms are

    e0=(3/4)(10-2k),  weight1/16;
    e1=e0+2k,        weight3/16,

where energy=alpha e. The norms follow by independent Haar integration of
G,A,B: ||v||^2=1/4, ||v0||^2=1/16 and <v0,v1>=0. The checker independently
verifies these integrals with exact quartic S3 cubature. These are analytic
finite invariant sectors of the actual vectors, not a numerical truncation.

For g_i=B1 f_i define positive spectral matrices W_e,ij=<g_i,Pi_(alpha e)g_j>.
The independently derived full list is:

| e | W00 | W01=W10 | W11 |
|---|---|---|---|
| 3 | 19/4 | 1/4 | 1/8 |
| 9/2 | 0 | 0 | 1/8 |
| 6 | 0 | 0 | 3/8 |
| 15/2 | 0 | 0 | 9/4 |
| 8 | 0 | 0 | 9/8 |
| 17/2 | 0 | 0 | 3/8 |
| 9 | 0 | 0 | 3/8 |

The off-diagonal value is independently fixed by the Q1 identity
<g0,g1>=E[k*2x]=1/4. Since g0 has only energy3alpha, that entire cross
coefficient belongs at e3. The matrices sum to[[19/4,1/4],[1/4,19/4]].
The leading channel matrices therefore must be

    K_lead,ij(s)=(alpha lambda)^2 sum_e W_e,ij exp(-alpha e s/hbar),
    Sigma_lead,ij(z)=(alpha lambda)^2 sum_e W_e,ij/(alpha e+z).

A scalar reference replacement fails both the nonzero off-diagonal entry and
the seven-energy nonconstant channel. Equal instantaneous diagonal values do
not imply equal time dependence. These2x2 matrices are channel data; they do
not prove that span(f0,f1) is invariant or that a2x2 autonomous semigroup or
inverse can replace the full selected dynamics.

## Full-Hilbert error bounds, units and uniformity

Q1 proves ||B1||=5/2. Strong bounded-perturbation Duhamel on the common domain,
using both complementary lower bounds3alpha, gives

    ||e^(-s C_lambda/hbar)-e^(-s C0/hbar)||
       <=40alpha lambda (s/hbar) exp(-3alpha s/hbar).

The norm statement follows from strong vector integrals, not norm continuity
of either heat semigroup at zero. Sandwiching by alpha lambda B1 yields

    ||K_lambda(s)-K_lead(s)||
       <=250alpha^3 lambda^3 (s/hbar) exp(-3alpha s/hbar),  s>=0.

The second resolvent identity similarly gives

    ||Sigma_lambda(z)-Sigma_lead(z)||
       <=250alpha^3 lambda^3/(3alpha+z)^2,  z>0.

These hold for all lambda>=0, including the required0..1/100 regime, because
positivity retains the complementary lower bound; a small-coupling Neumann
series is not needed. Kernel units are energy squared, self-energy units
energy. The kernel remainder has a uniform-in-delay upper bound
250alpha^2 lambda^3/(3e), and the self-energy remainder is bounded uniformly
as z decreases to0 by250alpha lambda^3/9. These are absolute operator-norm
error statements on the full selected Hilbert space. They are not relative
errors for exponentially small matrix entries or a uniform approximation to
the full compressed resolvent: its inverse bound1/z can still diverge.

For positive lambda, the resolvent order also gives
0<=Sigma_lead-Sigma_lambda. Do not infer an analogous heat-operator order
from C_lambda>=C0: operator exponentiation does not supply that order here.
Neither the individual memory kernel nor its electric leading term has an
operator-norm time Taylor expansion implied by these cancellation estimates.

## Exact projected identities and rejection conditions

Use Q1's common operator/form domains. The off-diagonal B_lambda is bounded;
A_lambda and C_lambda are self-adjoint diagonal blocks. Writing T(t)=J*e^(-tH/hbar)J
and Y(t)=Qe^(-tH/hbar)J, on domain vectors the block equations are

    hbar T'=-A T-B*Y,
    hbar Y'=-B T-CY,  Y(0)=0.

Solving the second equation and extending its vector-valued integral gives
the positive memory return:

    hbar T'(t)=-A T(t)+hbar^-1 int_0^t K(t-u)T(u)du,
    T(t)=e^(-tA/hbar)+hbar^-2 int_0^t dv int_0^v du
          e^(-(t-v)A/hbar)K(v-u)T(u).

The differential equation is a domain-vector assertion; the mild double
integral holds strongly on all selected vectors. Its final factor is the
full compressed T, not the autonomous A semigroup. The independent checker
verifies the Volterra coefficient ordering through degree5 on a noncommuting
positive block fixture. This is algebra support only.

For z>0, C+z is invertible, its inverse maps into D(C), and
Sigma(z)=B*(C+z)^-1B is bounded self-adjoint. The Schur operator

    S(z)=A+z-Sigma(z), D(S)=D(A)

is self-adjoint and at least zI. The latter follows by minimizing the positive
H+z quadratic form over the complementary vector, or by the completed-square
identity at q=-(C+z)^-1Bf. Domain-preserving block factorization then proves

    J*(H+z)^-1J = [A+z-Sigma(z)]^-1.

The sign is minus. Also int_0^infinity e^(-zt/hbar)T(t)dt equals hbar times
this resolvent, and the analogous transform of K is hbar Sigma(z), consistent
with both Volterra factors of hbar. The checker rejects plus Sigma and the
omitted-return inverse on a noncommuting exact rational block.

A common scalar c shifts A and C as well as H, leaving B unchanged. Thus
K(s) gains exp(-cs/hbar), and Sigma(z) becomes the original Sigma(z+c) in a
regime where the shifted resolvents exist (z+c>0 is sufficient here). A
shift on one side only is a different model. Lambda0 recovers the exact
P2 electric map. The Haar reference remains an electric reference, never an
interacting ground by implication.

## Targeted primary-source check and review boundary

Rechecked Burbano/Bauer arXiv2409.13812v2,28September2024: Appendix B.3,
Eqs.132-134,145-151; B.4.1 Eqs.153-157; and the vertex contraction discussion
following Eq.168. These give product Haar, vertex gauge invariance, electric
Casimirs and the complete link representation decomposition. The graph's
no-leaf/girth argument, actual overlaps and finite channel weights above are
independently derived. The source's coupling is not identified with lambda.
Reading is targeted, not a full-paper or priority audit.

Reuse the previously read Teschl second-edition author PDF Theorem6.4 and
Lemma6.5, printedp159, for bounded common-domain perturbations and the
resolvent identity. The Volterra and Schur arguments above are explicit and
must match the actual blocks. No generic source substitutes for the finite
graph spectral computation or the error regime. The source map records exact
locators and gaps. Reject missing physical support, an assumed complementary
gap, independent spins along a common path, discarded cross-channel weights,
wrong Schur sign/Volterra factor, or promotion of2x2 channel data to closure.
Await both frozen submissions and the advisor's explicit review opening.
