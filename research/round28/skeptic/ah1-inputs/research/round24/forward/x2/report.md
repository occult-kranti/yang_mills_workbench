# X2 forward: the complete 21-state Ritz residual certifies the full graph

The actually assembled vacuum-plus-20-faces sector gives a useful full-graph
ground and late-heat certificate. At lambda=1/100 the true dimensionless ground
energy lies within an interval of width below 1.04e-8 around 0.19983333; the
distance between its ground projection and the 21-state Ritz ground projection
is below 8.32e-5. The separately centered full and Ritz heat operators differ
in full physical operator norm by less than 0.000103 on every sigma>=4.
A certified rational spectral representation has negligible additional error.
These are rigorous bounds, not an observed physical trajectory.

The omitted residual is computed completely, not replaced by the known single
spin-one channel. It contains 20 spin-one face states and 190 two-face products;
the 62 products sharing an edge retain both singlet and triplet channels.
The small computation supplies exact moments, actual physical coefficients,
and rational enclosures. No high-cutoff matrix is assumed to have been built.

Authorship: independent model-agent derivation, using the reviewed X1 evidence.
No reverse/X2 solution was read. Shared premises and model-agent review are
not external peer review. Newton's analysis/synthesis is used to distinguish
what a Ritz residual identifies from what remains unknown. Tesla's complete
mechanism check is implemented by retaining all omitted product channels.
Historical analogy is not a physics premise; priority remains unverified.

## 1. Actual graph, scales and the previously assembled sector

The model is the open (3,3,2)-vertex cubical SU(2) graph with 18 vertices,
33 links, 20 square faces and every vertex Gauss constraint. On
Hphys=L2(SU(2)^33,Haar)^SU(2)^18 write

    K=H_E/alpha, L=H_lambda/alpha=K+lambda(20-S),
    S=sum_(p=0)^19 W_p, W_p=Tr(U_boundary(p))/2,
    sigma=alpha*t/hbar, 0<=lambda<=1/100.

The positive scales a,E_star,alpha/E_star,hbar remain fixed. All energies below
are divided by alpha; multiply energy intervals and residual norms by alpha
for physical energies. Heat norms and projection distances are dimensionless.
Ritz coefficients, residuals and observation time are approximation diagnostics,
not action deformations or fitted clocks. This is actual H_lambda, never the
distinct leading-memory operator Htilde.

Use the admitted projection P=1_[0,9/2)(K), of rank 21, with orthonormal
basis Omega=1 and phi_p=2W_p. Its gauge, domain and complete low-energy-support
proof is in both X1 reports and the independent review. Briefly, Peter-Weyl
spin blocks commute with all Gauss actions; an invariant nonzero support has
no vertex of degree one; below energy 9/2 it must be one square with all spins
1/2. The corresponding vertex intertwiner is unique. K has compact resolvent,
unique ground Omega and full physical excited spectrum >=3. Bounded smooth
invariant multiplication preserves D(L)=D(K), its form domain and its smooth
invariant core. Every vector used here is a finite smooth polynomial in that
core. The norm calculations therefore concern actual physical vectors.

The exact compression A=PLP has A00=c, A0p=Ap0=-lambda/2,
Apq=(3+c)delta_pq, where c=20lambda. It is assembled again in the checker.
Set

    D=sqrt(9+20lambda^2), w=(D-3)/2,
    mu=c-w, h=lambda/[2(3+w)], Z=1+20h^2,
    f=(Omega+h sum_p phi_p)/sqrt(Z).                         (1)

Then Af=mu f, ||f||=1, and the other Ritz eigenvalues are 3+c (multiplicity
19) and c+(3+D)/2. Its ground is simple. Since L>=K and <Omega,L Omega>=c,
the true ground epsilon is simple and satisfies

    0<=epsilon<=mu<=c<=1/5, E_1(L)>=3.                      (2)

Neither Omega nor f is assumed to be the interacting ground.

## 2. Complete Haar moments and every omitted sector

Let F=S^2-5. A simple square holonomy is Haar, so

    E W_p=0, E W_p^2=1/4, E W_p^4=1/8.

For two distinct squares there is an edge exclusive to each. Integrating an
exclusive edge in W_p^2 makes that factor exactly 1/4, independent of the
shared links; hence E W_p^2 W_q^2=1/16 even when the two faces share an edge.
This is an exact conditional Haar calculation, not a statistical-independence
assumption for the entire face family.

Products with an odd edge-center parity have zero mean. Distinct face masks
are different; no triple of masks has zero XOR; no four distinct face masks
have zero XOR. The checker exhausts all triples, all 4,845 four-face sets and
all 160,000 ordered quadruples on the actual graph. The fourth moment is
therefore completely enumerated:

    E S^2=20/4=5,
    E S^4=20/8 + 6*C(20,2)/16 =295/4,
    ||F||^2=E(S^2-5)^2=195/4.                              (3)

Odd moments vanish by an actual global center symmetry, not merely the
first few parity checks. Assign central signs +1 on x links, (-1)^x on y
links and (-1)^(x+y) on z links. Every elementary square acquires sign -1.
Product Haar measure is invariant under this link multiplication, so S goes
to -S and every odd moment is zero. The checker verifies all 20 signs.
In particular F is orthogonal to Omega and to every phi_p; PF=0.

For completeness, the omitted vector has the exact expansion

    F=(1/4)sum_p chi_(1,p) + 2 sum_(p<q) W_p W_q,
    chi_(1,p)=4W_p^2-1.                                   (4)

The 20 spin-one characters are normalized orthogonal physical eigenvectors
of K, each of energy 8; their different edge representation labels prove
orthogonality even though their central parities are all even. Their squared
contribution to ||F||^2 is 20/16=5/4. The 190 two-face products have pairwise
distinct nonempty central parity masks, and are orthogonal to all spin-one
terms. Their total squared contribution is 190/4=95/2. Thus (3) accounts for
every term and every cross term in (4).

The graph has 128 edge-disjoint face pairs and 62 pairs sharing exactly one
edge. An edge-disjoint product is an electric eigenvector of energy 6,
including pairs sharing only a vertex. For a shared edge use independent
Haar path holonomies G,A,B to write X=W_p W_q=t(GA)t(G^-1 B), where t=Tr/2.
The tensor product 1/2 tensor 1/2 splits into spin 0 and spin 1. Haar
projection on G gives X_s=t(AB)/4; ||X_s||^2=1/64, while
||X-X_s||^2=3/64. Six unshared fundamental edges cost 9/2. The shared triplet
costs a further 2, so these two energies are 9/2 and 13/2. Multiplication by
the factor 2 in (4) produces the complete electric spectral-weight table:

| Electric energy | Squared weight of F | Source |
|---:|---:|---|
| 9/2 | 31/8 | 62 shared-edge singlets |
| 6 | 32 | 128 edge-disjoint pairs |
| 13/2 | 93/8 | 62 shared-edge triplets |
| 8 | 5/4 | 20 spin-one faces |

These weights sum to 195/4 and their first energy moment is 295. They give
an independent verification of the quadratic-form identity

    <F,KF>=4 E S^4=295.                                    (5)

For (5), KS=3S and integration by parts on the compact product group gives
<S^3,KS>=3 E[S^2 Gamma(S)]; hence E[S^2 Gamma(S)]=E S^4.
The chain rule h[S^2]=4E[S^2 Gamma(S)] proves (5), with Gamma the carré du
champ of this exact K. All functions are smooth; no domain extension or
constant from the distinct S/W model is imported.

## 3. Actual residual and a two-vector variational improvement

Since the P component of (L-mu)f vanishes and the scalar term has no
off-diagonal block, the entire residual is

    r=(L-mu)f=-(2lambda h/sqrt(Z)) F,
    rho^2=||r||^2=195lambda^2 h^2/Z
          =195lambda^4/[4(3+w)D].                         (6)

This is an exact full-Hilbert norm. Keeping only the spin-one face channels
would give rho^2/39, a factor-39 underestimate. The omitted products cannot
be dismissed as unrelated exterior states: they are present in the actual
vector r. Every matching spin-one coefficient is

    <chi_(1,p),r>=-lambda h/(2sqrt(Z)),                     (7)

which is nonzero for lambda>0. At lambda=0 both h and r vanish exactly.

The normalized boundary vector xi=-F/sqrt(195/4) is defined also at lambda=0.
It is orthogonal to the entire 21-state space. Equations (3)-(5) and the odd
moment symmetry give the actual matrix element

    nu=<xi,L xi>=236/39+c,
    <xi,L f>=rho>=0.                                      (8)

For lambda>0 xi=r/rho. The sign in (8) uses the minus sign in xi; reversing
it changes the off-diagonal coefficient. The two-dimensional span(f,xi)
is only a variational test space of the full graph. It does not close the
dynamics or assert that xi is an electric eigenvector. Its exact compression
has entries [[mu,rho],[rho,nu]], and Rayleigh-Ritz implies

    epsilon <= mu-delta_low,
    delta_low=2rho^2/[nu-mu+sqrt((nu-mu)^2+4rho^2)].         (9)

This small extra test vector is a polynomial already fixed by the complete
21-state residual. No large sector or additional approximation model is
introduced. In particular (9) proves a strictly positive true-versus-Ritz
energy difference for positive lambda, with an evaluated lower bound.

## 4. Full-graph ground enclosures without assuming an exact Ritz state

Because all spectrum other than epsilon lies >=3 and mu<3, the spectral
measure of f gives

    0<=<f,(L-epsilon)(L-3)f>
       =rho^2-(mu-epsilon)(3-mu).

The second moment is finite because f is smooth. Thus the complete energy
error obeys the residual enclosure

    delta_low <= mu-epsilon <= delta_high:=rho^2/(3-mu).    (10)

This derives the usual variational-residual inequality directly in the actual
physical spectral measure. Its positive denominator is essential. Let G be
the actual ground projection and G_R=|f><f|. On the excited physical space,
|L-mu|>=3-mu, so

    ||G-G_R||=||(I-G)f|| <= p:=rho/(3-mu).                 (11)

This concerns the full infinite physical Hilbert space, not the residual
test space. Min-max has already established an actual isolated simple ground;
(10)-(11) do not infer spectral isolation from a small residual alone.

At lambda=1/100, the checker encloses all radicals by rational bisection and
evaluates positive monotone endpoint expressions. Rounded explanatory values
(the JSON fractions are authoritative) are

    mu = 0.19983334259156...,
    rho^2 = 5.4157640560... * 10^-8,
    delta_low = 8.94953309... * 10^-9,
    delta_high = 1.93408633... * 10^-8,
    epsilon in [0.19983332325070..., 0.19983333364204...],
    p = 8.310860407... * 10^-5.

The reported endpoints are rounded illustrations, not outward-rounded
replacement certificates. A safe outward decimal enclosure is
[0.19983332325, 0.19983333365], verified by exact fraction comparisons.
No unknown actual eigenfunction was numerically substituted in these formulas.

## 5. Uniform late-time centered heat and an explicitly evaluable surrogate

The true centered heat is E(sigma)=exp[-sigma(L-epsilon)]. Its excitation
gap is at least g=3-mu. Let E_R(sigma)=exp[-sigma(A-mu)]P be the exactly
ground-centered Ritz heat, extended by zero. Its smallest excitation gap is
gamma_d=(D+3)/2. By decomposing both actual operators into ground projection
and decaying excited spectrum,

    sup_(sigma>=tau)||E(sigma)-E_R(sigma)||
        <= p+exp(-g tau)+exp(-gamma_d tau), tau>=0.         (12)

The simpler rank-one approximation obeys

    sup_(sigma>=tau)||E(sigma)-G_R|| <=p+exp(-g tau).        (13)

These are full physical operator norms. Compressing by the inherited J also
preserves the upper bounds on all selected H3. The full true ground energy
and the Ritz ground energy are different and each is retained in its own
centered heat. The lack of secular energy-error growth in (12) follows from
this exact spectral decomposition, not from discarding delta in a Duhamel
bound. At time zero the zero-extended Ritz heat still has norm error one;
(12) is useful only after the excited tail decays. It is absolute, not relative.

At lambda=1/100 and tau=4, rational exponential enclosures give

    sup_(sigma>=4)||E(sigma)-E_R(sigma)|| < 103/1000000,
    sup_(sigma>=4)||E(sigma)-G_R|| < 97/1000000.              (14)

Thus the physical starting time is 4hbar/alpha. No time calibration is fitted.
The checker also computes examples at lambda=0 and 1/200. At zero coupling
the ground and residual errors vanish exactly; the excited heat tail of a
finite-rank approximation remains. No real-time smoothing follows.

For reproducible finite-matrix evaluation, define

    U=|Omega><Omega|+(1/20)|sum phi_p><sum phi_p|,
    D0=P-U,
    E_R(sigma)=G_R+exp(-gamma_d sigma)D0+exp(-D sigma)(U-G_R). (15)

These are orthogonal physical projectors of ranks 1,19,1. The rank-one
projector G_R has explicit entries G00=(D+3)/(2D), G0p=lambda/(2D), and
Gpq=lambda^2/[2D(D+3)]. The checker constructs the exact rational matrix A
and a rational approximation to G_R as follows. Enclose D and h in intervals,
choose midpoint hhat and Dhat, and put

    Ghat=|Omega+hhat sum phi_p><Omega+hhat sum phi_p|/(1+20hhat^2),
    Ehat(sigma)=Ghat+exp[-(Dhat+3)sigma/2]D0
                       +exp(-Dhat sigma)(U-Ghat).          (16)

Ghat is an exact rational orthogonal projector, checked by matrix arithmetic.
The approximate centered generator in (16) has its ground eigenvalue exactly
zero. Rounding a scalar ground shift independently would instead cause a
secular exponential or loss of the limiting ground, so that shortcut is
explicitly rejected.

If widths of the radical and h enclosures are e_D and e_h, respectively,
the rank-one angle identity gives ||Ghat-G_R||<=5 e_h. Since both excited
gaps are >=3 and sup_s s exp(-3s)<=1/3, the two gap approximations add at most
e_D/4. Therefore

    sup_(sigma>=0)||Ehat(sigma)-E_R(sigma)|| <=5e_h+e_D/4.   (17)

This bound is below 10^-35 in the executed cap example. Evaluating the two
scalar exponentials in (16) at sigma=4 uses positive Taylor lower/upper
bounds followed by reciprocals, yielding certified intervals. Their combined
evaluation widths are below 10^-45. Equations (14)+(17) still give an error
below 0.000103 for the symbolic finite representation (16) on the full delayed
half-line. A finite-time table of exponentials is not mislabelled as evaluation
of every real time; the uniform representation bound is the analytic (17).

## 6. Executed controls, source bindings and remaining scope

The standalone standard-library checker writes exactly results.json and
controls.json. It assembles the actual 21x21 matrix, enumerates the complete
face parity/multiplicity data, derives the independent residual spectral
weights and form moment, encloses all numeric claims, and constructs/checks
the rational projector and spectral representation. No Monte Carlo or
uncontrolled quadrature appears. Explicit exceptions survive Python -O.

Discriminants include: ignoring the 190 two-face products changes rho^2 by
a factor of 39; ignoring shared-edge singlets changes the first energy moment;
using only 19 physical faces changes the Haar moments; wrong normalized
fundamental fourth moment changes the residual norm; reversing the Ritz face
sign fails its ground equation; a scalar ground miscentering grows/losses the
ground mode; invalid gap denominators are rejected. Lambda=0 is treated as an
exact exception rather than divided by rho. These tests do not manufacture an
infinite-dimensional proof; the physical spectral/domain argument above does.

All current contract inputs, actual further inherited files read and producer
artifacts are bound by submission.json. X1 and earlier instructions remain
immutable. The installed Newton/Tesla methods and their research references
were read during X1 and are retained through those frozen input snapshots;
the additional W residual lesson was read in full for X2. The X1 gate was
parsed for its admission verdict, source hashes and payload/control structure;
its duplicated coefficient payload is not a new derivation. No reverse/X2
material was read. The only external technical reading remains the explicitly
limited X1 background reading of arXiv:2307.11829v1; no new historical or
literature-priority assertion is introduced.

The proved target is useful finite-graph late-heat and ground information
from a manageable actual computation. It does not give the exact ground,
early-time full-space accuracy, a relative heat ratio, real-time control,
thermodynamic uniformity, a homogeneous spectral gap, physical mass calibration
or a four-dimensional continuum construction. These limits survive the small
numeric errors. No Y/Z work is selected or executed by this producer.

    python3 -B research/round24/forward/x2/check.py --output /absolute/fresh/x2
    python3 -B -O research/round24/forward/x2/check.py --output /absolute/fresh/x2-O
