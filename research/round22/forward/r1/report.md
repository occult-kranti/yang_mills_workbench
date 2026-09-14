# R1 forward: the initial interacting inverse and its actual boundary defect

The initial O1 diagonal has a uniformly gapped local inverse, but the
resulting local homological cancellation leaves every crossing star. For
the frozen actual-SU2 source the full defect on the product vacuum satisfies

\[
\boxed{\|([S_Y,H_{0,\Lambda}+D_\Lambda]+A_Y)\Omega_\Lambda\|^2
       ={7\tau^2\over432}.}                                      \tag{1}
\]

This is nonzero for nonzero tau. It is a diagnostic rank-two source, not an
assertion about a generated O1 residual. No numerical gap for H0+D+R or
later iteration is proved. This forward derivation precedes current R1
reverse/skeptic reading; R2 is neither selected nor executed here.

## Model, inverse and domains

Use precisely the full-link homogeneous I1/O1 reference, with complete
24-link onsite factors (one ten-link strip and fourteen free Casimirs).
Write Z_b=b+{0,e_x,e_y,e_z}, retaining b only when Z_b is wholly in Lambda.
Each phi_b=-(tau/3) sum_(21 omitted anchored faces) W_f has norm at most
M=7|tau|. Set D_b=Q_b phi_b Q_b, with Q_b the complement of the star vacuum.
Declared supports remain Z_b even if an individual face uses fewer sites.

For finite nonempty Y, put n_Y=#{b:Z_b subset Y}, H_Y=sum_(x in Y)h_x,
D_Y=sum_(Z_b subset Y)D_b, G_Y=H_Y+D_Y, and P_Y=|Omega_Y><Omega_Y|.
The admitted h_x are self-adjoint and nonnegative, h_x>=I-P_x, with their
actual unbounded strip/free domains. Hence H_Y>=Q_Y=I-P_Y. Finite D_Y is
bounded self-adjoint with norm at most M n_Y and annihilates Omega_Y.
Bounded perturbation gives D(G_Y)=D(H_Y); its form domain is D(H_Y^(1/2)).

For every form-domain psi, using the commuting onsite projections,

\[
|\langle\psi,D_Y\psi\rangle|
 \le M\sum_{Z_b\subset Y}\langle\psi,Q_b\psi\rangle
 \le4M\langle\psi,H_Y\psi\rangle.                              \tag{2}
\]

The overlap four counts anchors x,x-e_x,x-e_y,x-e_z; boundaries only delete
them. Thus, with kappa=28|tau| and g=1-kappa,

\[
gH_Y\le G_Y\le(1+\kappa)H_Y,\quad
G_Y|_{Q_Y}\ge g,\quad \|(G_Y|_{Q_Y})^{-1}\|\le g^{-1}.           \tag{3}
\]

Omega_Y is the unique zero-energy ground. The frozen |tau|<=5/1664 gives
g>=381/416 and inverse norm <=416/381, uniformly in Y and Lambda. The
initial-diagonal argument alone works on the larger open interval |tau|<1/28;
this is not an enlarged interval for an O1 remainder or full stability theorem.
On Q_Y, H_Y+1<=2H_Y, so G_Y>=(g/2)(H_Y+1). In particular the bounded
extensions of (H_Y+1)^(1/2)G_Y^(-1/2)Q_Y and
(H_Y+1)^(1/2)G_Y^(-1)Q_Y have norms at most sqrt(2/g) and sqrt(2)/g.
Their adjoints give the opposite orderings. These follow from quadratic
forms and the spectral gap, without commuting D_Y with H_Y.

For bounded self-adjoint R_Y define v=Q_Y R_Y Omega_Y, r=||R_Y||,
u=(G_Y|Q_Y)^(-1)v, A=|v><Omega_Y|+|Omega_Y><v|, and
S=|u><Omega_Y|-|Omega_Y><u|. Then

\[
\|A\|=\|v\|\le r,\quad \|S\|=\|u\|\le r/g,\quad
\|G_Yu\|=\|v\|,\quad
\|G_Y^{1/2}u\|^2\le r^2/g,\quad
\|H_Y^{1/2}u\|\le r/g.                                        \tag{4}
\]

Here u is in D(G_Y)=D(H_Y), perpendicular to Omega_Y, and
||H_Yu||<=c_Y:=r(1+M n_Y/g). This last graph estimate explicitly retains its
support-size dependence; n_Y<=|Y|<=|Lambda|. There is no unproved uniform
operator bound H_Y G_Y^(-1) inferred from form comparison.

On D(G_Y), direct rank-two multiplication gives

\[
G_YS=|v\rangle\langle\Omega_Y|,\quad
SG_Y=-|\Omega_Y\rangle\langle v|,\quad [S,G_Y]=-A.              \tag{5}
\]

Extend S,A by identity outside Y. The exterior H0 strongly commutes with S.
The commutator with H0 on D(H0_Lambda) has a bounded extension of norm
||H_Yu||<=c_Y. For the graph norm ||psi||+||H0 psi||,
||S psi||_graph<=(r/g+c_Y)||psi||_graph. The decomposition into local and
exterior energies also gives ||S|| on the form space with norm
||(H0+1)^(1/2)psi|| at most sqrt(2)r/g. Therefore the exponential series
converges in both spaces: exp(plus/minus theta S) preserves both full
domains, with graph bound exp(|theta|(r/g+c_Y)) and form bound
exp(sqrt(2)|theta|r/g). It is unitary on the Hilbert space. The same operator
and form domains belong to H0_Lambda+D_Lambda. These are preservation
statements; S does not regularize arbitrary rough exterior vectors.

## The full boundary identity and declared-support budget

Let B_Lambda(Y) contain every retained anchor b with Z_b meeting Y but
Z_b not contained in Y, and N_boundary its cardinality. Interior terms
belong to (5); disjoint terms commute. On the full operator domain,

\[
\boxed{[S_Y,H_{0,\Lambda}+D_\Lambda]+A_Y
       =E_Y:=\sum_{b\in B_\Lambda(Y)}[S_Y,D_b].}                 \tag{6}
\]

Each summand is a bounded operator with declared support Y union Z_b,
size at most |Y|+3, norm at most 2M r/g. Hence

\[
\|E_Y\|\le14|\tau|N_{\partial}r/g,
\qquad\|E_Y\Omega_\Lambda\|\le7|\tau|N_{\partial}r/g.           \tag{7}
\]

The vector improvement uses D_b Omega=0. Always N_boundary<=4|Y|.
For the indexed interaction sum, the root count
n_x(Y)=#{b in B_Lambda(Y):x in Y union Z_b} is N_boundary when x is in Y,
and at most four otherwise. Its weighted root budget at weight exp(mu|Z|)
is at most 14|tau|(r/g) exp(mu(|Y|+3)) n_x(Y). No support is replaced by
its interior, and coincident unions retain their indexed multiplicity.

For completeness, a family with r_mu=sup_x sum_(Y contains x)
exp(mu|Y|)||R_Y|| yields, at mu'=mu-ell>0,

\[
\|E\|_{\mu'}\le {56|\tau|e^{3\mu'}\over g}
                 (\ell^{-1}+4)r_\mu.                          \tag{8}
\]

To see this, split roots into x in Y and x in Z_b. The first part uses
N_boundary<=4|Y| and |Y|exp(-ell|Y|)<=1/ell. The second has at most four
stars containing x and four possible meeting sites in each, giving sixteen
root sums. The prefactor per pair is 14|tau|/g. Absolute convergence in a
finite volume is enough for this indexed bound; no infinite global unitary
is constructed. Equation (8) is an upper budget, not a lower bound on every
actual residual or proof that every improved iteration fails.

## Exact crossing counts

For origin Y={0,...,L-1}^3 in a larger positive cuboid, an anchor meeting Y
must lie in Y: an incoming anchor outside Y would have a negative coordinate.
There are L^3 meeting anchors and (L-1)^3 interior anchors, so

\[
N_{\partial}^{origin}=3L^2-3L+1.                               \tag{9}
\]

For bulk Y={1,...,L}^3 in Lambda={0,...,L+1}^3, the same L^3 anchors are
joined by three disjoint incoming planes: one coordinate zero and the other
two in {1,...,L}. They contribute 3L^2. Interior anchors still number
(L-1)^3. Thus

\[
N_{\partial}^{bulk}=6L^2-3L+1.                                \tag{10}
\]

These hold for every integer L>=1, giving one and four at L=1. Outward
stars are already among anchors in Y; incoming stars cannot be omitted
in the bulk. At a physically clipped outer boundary, use the actual
retained-star definition rather than either unqualified count.

## Frozen SU2 probe: all faces, actual Haar and nonzero defect

Now take exactly Lambda={0,1}^3 and Y={0}. The only retained anchor is
zero, with the full four-site star. There are no interior stars in Y.
Let e be the positive z link at physical tail (0,0,0), and
v=chi_(1/2)(g_e)Omega_Y=(Tr g_e)Omega_Y. This is the actual full-link space,
without a Gauss-sector restriction. Free-link Haar orthogonality gives
<Omega_Y,v>=0 and ||v||=1. The selected-strip ground is unchanged.
The dimensionless free Casimir is 8C_e, so H_Y v=8(3/4)v=6v and u=v/6.
The frozen source is R_Y=A_Y=|v><Omega_Y|+adjoint, of norm one.

For an anchored physical face at p in directions a<c, its positive link
tails are p,p+e_a,p+e_c,p. With ownership
pi(p)=(floor(p_x/4),floor(p_y/2),p_z), the 21 omitted-face classes are:

| Class | Number | Actual coarse support |
|---|---:|---|
| xy, r<3, s=1 | 3 | {0,e_y} |
| xy, r=3, s=0 | 1 | {0,e_x} |
| xy, r=3, s=1 | 1 | {0,e_x,e_y} |
| xz, r<3 | 6 | {0,e_z} |
| xz, r=3 | 2 | {0,e_x,e_z} |
| yz, s=0 | 4 | {0,e_z} |
| yz, s=1 | 4 | {0,e_y,e_z} |

Every face has at least two globally free links. Distinct elementary faces
share at most one link. For each f there is a free link other than e,
so <Omega,phi_0 v>=0. Thus Q_0 v=v and Q_0 phi_0 v=phi_0 v; the vacuum
projections in D_0 cause no hidden correction on this vector. Equation (6)
becomes

\[
E_Y\Omega_\Lambda=-D_0v/6
 ={\tau\over18}\sum_{f\in O_0}W_f\,\chi_{1/2}(g_e)\Omega_\Lambda. \tag{11}
\]

Conditional on all other links, integrating one free link of f other than
e gives E[W_f^2]=1/4 independently of g_e. Thus
E[chi_e^2 W_f^2]=1/4. If f differs from h, their free-link symmetric
difference contains a link other than e: each has at least two free links
and their full edge sets meet in at most one. Center sign reversal of that
free link changes exactly one Wilson trace and leaves chi_e^2 and the
strip ground unchanged. Therefore E[chi_e^2 W_f W_h]=0. This argument
conditions on the possibly entangled strip ground; it never assumes face
independence or replaces the strip ground by Haar.

Consequently ||sum_f W_f chi_e Omega||^2=21/4, proving (1) exactly, with
||E_Y Omega||=sqrt(21)|tau|/36. It is also a lower bound on ||E_Y||.
The sign in (11) is positive tau with the frozen conventions. At tau=0
the boundary defect vanishes, while the source and generator remain defined.

The singleton probe has no interior D and cannot itself discriminate a
bare from an interacting inverse. A separate actual-model diagnostic does:
take Y=Z_0 and w=chi_e Omega_Y, so ||D_Yw||^2=7tau^2/12 by the same Haar
calculation. Choose source vector v'=G_Yw=6w+D_Yw, and its bounded rank-two
source. Its interacting inverse is exactly w. Its bare inverse is
u_0=w+H_Y^(-1)D_Yw. Since ||D_Y||<=7|tau|,

\[
\|([S_{u_0},G_Y]+A_{v'})\Omega_Y\|
 =\|D_Yu_0\|\ge(1-7|\tau|)\sqrt{7/12}|\tau|>0               \tag{12}
\]

for nonzero frozen tau. Also ||v'||^2=36+7tau^2/12, since
<w,D_Yw>=0 by a free-link integral. This second source is explicitly
another diagnostic, not a generated residual or a replacement for (11).

## Consequence, checks and attribution

The interacting inverse removes the interior retained-D commutator, but
(1) rejects promoting that interior identity to full-volume cancellation.
Equation (8) retains a linear boundary/source upper cost, with support and
weight dependence. This explains why simply replacing the O2 bare inverse
does not authorize deleting its retained-D issue. R1 does not establish an
all-stage recurrence for later centered diagonals, nor prove that every
possible improved recurrence must fail.

The independent standard-library checker generates faces, free links and
complete-star sets; verifies exact SU2 second-moment contractions using the
eight signed quaternion axes (exact for the conditional quadratic moments,
not a Haar sampling approximation); and checks all cross-term sign witnesses.
It rejects missing crossing anchors/faces, incorrect declared support weight,
trace/energy normalization, wrong homological sign and bare cancellation.
The mathematical domain and all-size arguments above are not finite fixtures.
Explicit exception controls remain active under optimized Python.

Targeted primary reading and its boundary are recorded in source-notes.md.
The interacting-inverse method is established mathematics; the complete
actual geometry, constants and diagnostic defects here are instantiated
derivations. Scientific priority is unverified.

All h,D,G,A and inverse-vector quantities are dimensionless in delta=alpha/8.
Multiplying Hamiltonians/source energies by delta restores energies; S is
dimensionless and physical evolution uses delta*t/hbar. The fixed positive
a,E_star,alpha/E_star,hbar are unchanged. Q2's finite-graph complementary gap
and magnetic positivity are not used. No infinite representation, fitted
physical clock or continuum Yang–Mills conclusion follows.

```bash
python3 -B research/round22/forward/r1/check.py --output /absolute/new/r1-forward
python3 -B -O research/round22/forward/r1/check.py --output /absolute/new/r1-forward-O
```
