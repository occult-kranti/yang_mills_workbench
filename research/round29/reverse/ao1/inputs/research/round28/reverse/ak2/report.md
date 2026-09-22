# AK2 reverse: the actual Wilson form moment, finite window and lower heat

All frozen targets follow for the same actual homogeneous orthant state:

    chi in D(sqrt(H_phys)),   mu1=int E dnu(E)<=alpha,
    nu([alpha/16,10alpha])>=1/10,
    C(t)>= (1/5) exp[-5alpha t/hbar], every finite t>=0.     (1)

The inherited upper bound remains C(t)<=v exp[-alpha t/(16hbar)]. Here
chi=(pi(W)-omega(W))Omega, nu is its actual physical energy spectral measure,
and v=||chi||^2>=1/5 is the admitted common AK1 consequence. The producer
119/576 and independent-skeptic 131/576 floors retain their attribution;
neither stronger fraction is needed below. This proves an upper bound, not
equality, for the limiting first moment. No physical operator-domain or second
moment assertion is made.

This is investigation ten under contract ce7044e37b6263bc32767dddbfa28b95860c1c2f54064737a4577f195a6fd601.
All 50 source originals, the contract and used instructions were snapshotted
before science. Root authorized production after preflight. The current AK2
forward and skeptical mathematics remain unread through this independent
freeze. Historical names describe modern methods, not participation or
endorsement. Shared sources and the proposed form route are shared premises,
not independent physical observations.

## 1. Reconstruct what the three conclusions require

The window statement would follow from actual mass at least 1/5, support
above alpha/16, and a physical first moment at most alpha: the tail above
10alpha would cost at most 1/10. The lower heat envelope requires that same
first-moment ceiling, applied to the normalized spectral probability through
convexity. A lower gap and positive variance alone give neither assertion.
Consequently the missing premise is a uniform finite-volume physical form
bound and a valid passage to the actual limiting measure. AK1's normalized
local reference-density energy is not that premise.

Keep exactly the actual I1/AJ1/AJ2/AK1 nonsummable homogeneous omitted
interaction, selected-strip reference, specified whole-star positive-orthant
limit and full bounded physical GNS completion. The fixed coefficients obey
|lambda_L|,|lambda_R|<=alpha/2 and |mu|<=alpha/8. The fixed positive scales
are alpha,hbar,E_star,a, with delta=alpha/8 a physical energy. The regime is
the intersection |tau|<tau_*=min(c1(S),1/(2c2(S)))/7 and |tau|<=2^-16.
The positive source constants remain unevaluated. The additional cap admits
no chosen positive numerical tau by itself.

At coarse b=(i,j,k), all three positive links at tails
(4i+r,2j+s,k), 0<=r<4, 0<=s<2, belong to b. Euclidean division gives
unique ownership. The onsite space has 24 unreduced Haar factors: ten links
in the three selected xy faces and fourteen free links. On a finite coarse
cuboid Lambda, retain every complete 21-face omitted group whose anchor
star b+S lies in Lambda, S={0,e_x,e_y,e_z}. No physical tensor
factorization, independent plaquette variables, alternative boundary state,
summable representation or mobility is introduced.

The original Wilson is

    W=Tr[U_x(0)U_z(e_x)U_x(e_z)^(-1)U_z(0)^(-1)]/2.       (2)

The signed original links have owners 0,0,e_z,0. Their complete cover
R={0,e_z} contains 48 links and 36 endpoint actions: sixteen tails, four
added x heads, eight y heads and eight z heads. Every stored link transforms
as U_(v,w)->g_v U_(v,w)g_w^(-1). The closed word telescopes to conjugation
at zero, so W is real, smooth, bounded by one, and physical. Both inverse
occurrences are retained. Its derivatives vanish on the other 44 links;
those factors and all their endpoint actions are still present.

For an arbitrary face, its owners are those of its base and its two
forward axis neighbors. Remainders in x modulo four and y modulo two give
the omitted support multiplicities 1,3,1,10,2,4 for {0,e_x}, {0,e_y},
{0,e_x,e_y}, {0,e_z}, {0,e_x,e_z}, {0,e_y,e_z}; their union is S.
There are three selected and 21 omitted faces per anchor. In an n-cube
there are 8n^3 tails, 24n^3 links, 8n^3+14n^2 endpoints and (n-1)^3
complete retained stars. Thus the fixtures 222/333/444 have respectively
192/648/1536 links, 120/342/736 endpoints and 21/168/567 omitted faces.
These analytic ownership and remainder arguments apply at all volumes;
the exact fixtures audit them. No finite fixture proves a thermodynamic
limit, and no smaller face boundary prescription replaces the whole stars.

## 2. Finite-volume domains and all scalar and magnetic terms

Let Q_Lambda be the sum of every original link Casimir. Its product
Peter--Weyl spectral domain is H^2 on the finite compact product group;
its form domain is H^1. One way to identify these domains is to use the
sum-of-squares elliptic product Laplacian and its Fourier eigenvalues.
Its eigenvalues are sums of j(j+1), with finite multiplicities. Bounded
real smooth multiplication perturbations preserve the operator domain and
form domain, and the finite Hamiltonian has compact resolvent.

Write the actual uncentered physical operator explicitly:

    delta Hhat_Lambda
      =alpha Q_Lambda -sum_selected lambda_f W_f
       -(alpha tau/24)sum_retained_omitted W_f
       -sum_(b in Lambda) E_strip,b.                     (3)

The bridge coefficient is included among lambda_f. The last sum is the
exact reference ground scalar. Set

    K_Lambda=delta(Hhat_Lambda-Ehat_Lambda),
    K_Lambda Omega_Lambda=0, ||Omega_Lambda||=1,
    m_Lambda=<Omega_Lambda,W Omega_Lambda>,
    chi_Lambda=(W-m_Lambda)Omega_Lambda.                  (4)

I1 gives the finite ground and nonnegative centered K_Lambda. Its ground
lies in H^2. Multiplication by W and W^2 preserves H^2 and H^1: both
functions and all derivatives through order two are bounded on the compact
group, and the weak Leibniz rule bounds each derivative of the product by
the corresponding Sobolev norm. Density of smooth functions extends this
estimate to those domains. This proves precisely the finite-volume
regularity used below; bounded locality alone would not do so.

Every selected and retained omitted magnetic term in (3) is a real smooth
bounded multiplication operator. It commutes with W and W^2 on the common
domains. Both the reference scalar and the actual ground scalar commute
as well, but must be retained in (3)--(4) to identify the correct ground
and zero center. Therefore their double commutators vanish individually.
There is no omitted magnetic remainder and no interacting Haar expectation
substitution.

## 3. Original-link derivatives and the exact finite form identity

Choose the usual normalized real fields generating left translations

    X_(e,a) f(U_e)=d/dt f(exp(t T_a)U_e)|_(t=0),
    T_a=-i sigma_a/2,       C_e=-sum_(a=1)^3 X_(e,a)^2.    (5)

Equivalently T_a is one half of a unit imaginary quaternion. This
normalization gives C_e the fundamental eigenvalue 3/4, hence the
inherited free-rotor gap 3alpha/4. Haar invariance gives X*=-X on smooth
functions. Leibniz on that core, then the H^2 bounds just proved, yields

    [C_e,W]f=(C_e W)f-2sum_a (X_(e,a)W)X_(e,a)f,
    [W,[C_e,W]]f=2sum_a (X_(e,a)W)^2 f.                  (6)

The first commutator is a first-order operator and is not asserted bounded
on L2. The double commutator has the displayed bounded multiplication
extension, and its domain identity is valid on H^2.

To derive every gradient coefficient, fix the other three face matrices.
Varying a positive occurrence changes the holonomy through left/right
isometries of SU(2); varying an inverse occurrence differentiates

    (exp(tT_a)U)^(-1)=U^(-1)exp(-tT_a),                  (7)

so its derivative is -U^(-1)T_a. Both multiplication and inversion are
isometries for the bi-invariant metric in (5). More explicitly, on unit
quaternions the three fields q->(e_a/2)q are an orthogonal tangent frame
of length 1/2. For the scalar coordinate w of a unit quaternion, the
Euclidean tangent projection of its coordinate gradient has squared norm
1-w^2. Pulling back by these isometries therefore proves, for EACH of
the four actual face links,

    sum_a (X_(e,a)W)^2=(1-W^2)/4,
    C_e W=(3/4)W.                                      (8)

The second identity also follows directly by differentiating
exp(tT_a) twice, since T_a^2=-I/4; the inverse version has the same
second derivative. All other link contributions vanish. Consequently

    sum_(e,a) (X_(e,a)W)^2=1-W^2,
    [W,[K_Lambda,W]]=2alpha(1-W^2).                      (9)

Use (4) and the proved domain preservation to take its ground expectation.
In 2W K_Lambda W-W^2 K_Lambda-K_Lambda W^2 the last two expectations
vanish by self-adjointness and K_Lambda Omega_Lambda=0. Centering W by
m_Lambda leaves its form energy unchanged for the same reason. Thus

    int E dnu_Lambda(E)
      =<chi_Lambda,K_Lambda chi_Lambda>
      =alpha <Omega_Lambda,(1-W^2)Omega_Lambda>
      <=alpha,                                         (10)

where nu_Lambda is the positive spectral measure of K_Lambda on
chi_Lambda. The identity uses the actual finite ground expectation.
It is uniform in volume and all allowed fixed selected coefficients.
Neither a reference-density energy ceiling nor a finite representation
cutoff replaces (10).

## 4. Actual tested resolvents and a nonnegative moment passage

The bound primary retrieval in the inputs gives Yarotsky's full local
algebra and Theorems 2--3, especially equation (6): matrix elements of
the centered finite resolvent converge when tested on A Omega_Lambda and
B Omega_Lambda for fixed bounded local A,B. The domain-qualified creator
and essential-self-adjointness passage is separate. I1/AJ1 supplies its
specified orthant transfer and actual reducing physical restriction. This
is not a common-concrete-Hilbert-space strong resolvent claim.

Bounded-local state convergence gives m_Lambda->m and
v_Lambda=omega_Lambda(W^2)-m_Lambda^2->v. For physical nonreal z,

    (K_Lambda-z)^(-1)
      =delta^(-1)(Hhat_Lambda-Ehat_Lambda-z/delta)^(-1).   (11)

Take the fixed local A=W-mI in the source theorem. Replacing A by
W-m_Lambda I changes its cyclic vector by norm |m_Lambda-m|. Resolvent
norm at most 1/|Im z| and uniformly bounded vector norms show that the
quadratic resolvent matrix element changes by a quantity tending to zero.
Thus the Cauchy transforms of nu_Lambda converge to those of the actual
spectral measure nu of H_phys on chi. AJ1's reducing identification
justifies using this physical measure; no new domain of chi is assumed.

Here is a direct sufficient measure argument. The uniformly closed linear
span of resolvents (E-z)^(-1), z nonreal, is C0([0,infinity)): it is
closed under conjugation and products, using the resolvent difference
identity and its uniform coincident-parameter limit, separates points and
vanishes nowhere. The locally compact Stone--Weierstrass theorem applies.
The masses v_Lambda are bounded by one, as is v. Therefore convergence
on resolvents extends by uniform approximation to every C0 function.

Choose continuous compactly supported nonnegative functions

    f_L(E)=E min(1,max(0,2-E/L)), L>0, E>=0.

They satisfy 0<=f_L<=E and increase pointwise to E as L increases.
For every fixed L, C0 convergence and (10) give

    int f_L dnu =lim_Lambda int f_L dnu_Lambda <=alpha.

Monotone convergence now proves mu1=int E dnu<=alpha. The spectral
form-domain characterization gives chi in D(sqrt(H_phys)). This
establishes an upper bound without equality of first moments. The bound
also gives tail tightness; together with the finite bound (10) it extends
the C0 convergence to bounded continuous tests by a compact cutoff.
The total masses already converge by the local variance calculation.
No moment equality, uniform integrability, common-space vector convergence
or limiting operator-domain statement has been silently added.

## 5. The frozen window and all finite imaginary times

AJ1/AJ2 supplies support(nu) in [g,infinity), g=alpha/16, with no vacuum
mass. AK1 supplies v>=1/5. Since E>=0 and alpha>0,

    nu((10alpha,infinity))<=mu1/(10alpha)<=1/10,
    nu([alpha/16,10alpha])=v-nu((10alpha,infinity))>=1/10. (12)

The upper window endpoint is included. A positive mass in this interval
need not be an eigenatom or the lowest overlapping energy.

For finite t>=0 let s=t/hbar. Normalize nu by its positive mass v.
The convex function exp(-sE) lies above its tangent at the finite mean
mu1/v. Integrating that tangent proves Jensen's lower estimate directly:

    C(t)=int exp(-sE)dnu >=v exp[-s mu1/v]
         >=(1/5) exp[-5alpha t/hbar].                    (13)

The last step uses mu1<=alpha, v>=1/5, and s>=0 separately. At t=0
it reads C(0)=v>=1/5. The inherited support bound independently gives
C(t)<=v exp[-alpha t/(16hbar)]. The exponents retain physical energy
divided by hbar. These are imaginary-time inequalities; no real-time
magnitude decay, exact mass or sharp asymptotic rate follows.

## 6. Exact controls and preserved limitations

The fresh standard-library checker enumerates the full cuboids, original
face words and endpoint actions. Noncommuting rational quaternion fixtures
check each oriented first derivative against an independent exact symmetric
group displacement; every second derivative is checked with its half-angle
normalization. They also check full gauge covariance and (8)--(9). A wrong
sign on an inverse first derivative is deliberately blind after squaring;
that blind gradient-sum check is preserved beside the discriminating signed
derivative test. Any other blind or failed execution is retained in the
production history.

At the specifically labeled all-zero-coupling free reference corner, W times
the constant ground has eigenvalue 3alpha and squared norm 1/4, hence
first moment 3alpha/4. This checks the coefficient, not the interacting
ground law. Omitting the half in the double-commutator expectation would
give 3alpha/2 and even violate the desired alpha ceiling. Replacing T_a
by a full imaginary quaternion multiplies the Casimir and gradient budget
by four. Both mistakes are detected.

The remaining controls are abstract and have distinct purposes:

* On a vacuum plus ell2 space, H e_n=alpha n^2 e_n and
  xi=sum_(n>=1)(2n)^(-1)e_n have bounded norm squared below 1/2 but
  divergent form energy alpha sum 1/4. The bounded self-adjoint operator
  |xi><Omega|+|Omega><xi| creates it. Exact prefixes and the analytic
  series reject automatic form-domain membership from boundedness.
* In units of alpha, the probability measures
  nu_n=(1-1/n)delta_(1/16)+(1/n)delta_(1/16+n/2) have mass one,
  bounded-test convergence to delta_(1/16), and constant first moment
  9/16. The limiting first moment is only 1/16. The uniform difference
  for unit-norm bounded tests is at most 2/n. This proves why even a
  uniform first-moment ceiling and mass/resolvent convergence do not
  license equality of moments.
* A two-level observable with a nonzero vacuum mean retains an atomic
  zero-energy component and heat plateau if not centered. Centering
  removes that mass, although the first moment itself is unchanged.
* A scalar/units fixture retains the actual ground subtraction, delta
  and hbar separately. Common shifts of raw operator and ground cancel;
  omitting the ground center, delta or division by hbar changes the
  corresponding energy or frequency.
* Spectral mass 1/5 at 20alpha has the inherited lower support and
  sufficient variance, but no mass in the frozen window and violates
  the proposed lower heat envelope. Its first moment exceeds alpha:
  the newly proved upper moment, not the lower gap alone, excludes it.
* Hypothetical positive source constants with tau_* below the additional
  cap reject admitting a coupling merely because it is below that cap.
  Those constants are not evaluations of the actual source constants.

These finite controls audit coefficients and implications; analytic
domain, geometry, spectral approximation and monotone-convergence
arguments prove their infinite-dimensional extensions. There is no
historical checker import or execution as the new algorithm.

## 7. Source closure and stop boundary

The reading ledger records full controlling AJ1/AJ2/AK1 proof readings
from this same agent, reused at verified unchanged hashes; the original
theorem passages were read directly in the bound prior primary retrieval.
Both complete I1 reports and the A1/A2 reference arguments were read.
Current 43-page manuscript reading is honestly focused, with the new AK1
chapter and scope/source appendices read fully, rather than claimed as a
full rereading of all earlier branches. The current network was structurally
parsed with full AJ/AK nodes inspected. No new external primary retrieval,
full cluster-expansion proof reconstruction or priority audit is claimed.

From the repository root (or using an absolute script path elsewhere):

    python -B research/round28/reverse/ak2/check.py --output /absolute/fresh/normal
    python -B -O research/round28/reverse/ak2/check.py --output /absolute/fresh/optimized

Each invocation produces only results.json. Runtime reads use owned local
snapshots; absolute instruction origins are provenance only. Flat result
bindings name the checker, report, contract, required originals, manifests
and snapshots. The top-level freeze uses repository-relative bindings and
includes every owned file except exactly itself, including inputs/freeze.json.
Fresh normal/optimized byte equality is recorded separately.

Equation (1) is a fixed-lattice actual-state result in the frozen conditional
regime. No numerical stability radius, limiting moment equality, second
moment, physical operator-domain assertion, threshold eigenatom, different
boundary-state equality, continuum construction, scientific priority or
percentage of the Yang--Mills problem follows. This is the final authorized
investigation. Further questions remain planning only after review.
