# T1 forward — certified full-space leading-memory evolution

The proposed full block Hamiltonian with electric complementary block C0 is self-adjoint and positive in the frozen range. Its compressed heat evolution is the unique full-selected-space evolution with Q2's leading magnetic memory and the full return factor. The actual projected error is O(lambda³) at fixed physical time. A positive lower bound also gives a uniform-in-time absolute O(lambda²) certificate for these unshifted heat operators. Neither statement identifies physical calibration, a closed two-channel system or ground-normalized long-time accuracy.

This independent forward submission uses only the frozen T1 definition, inherited Q2 evidence and reviewed S2 decision. Current reverse/skeptic T1 solutions were not read. T2 is not selected or executed here.

## 1. Actual spaces, domains and lower bounds

Keep the physical 18-vertex,33-edge,20-face SU2 graph, all Gauss constraints and the P2 isometry J from the entire selected Hilbert space H3. On Hphys=JH3 direct-sum QHphys, write

    H_lambda = [[A,B*],[B,C]],
    H_tilde = [[A,B*],[B,C0]],
    C=C0+alpha lambda D, D=QVmag Q, 0<=D<=40,
    B=alpha lambda B1, ||B1||=5/2.                         (1)

The exact inherited domains are

    D(A)=H²(SU2³) intersect H3,
    D(C)=D(C0)=Q D(H_E),
    D(H_lambda)=D(H_tilde)=D(H_E)=J D(A) direct-sum D(C0). (2)

The form domains are J(H¹ intersect H3) direct-sum QD(H_E^(1/2)). The diagonal H_E is self-adjoint and all additional blocks in H_tilde are bounded symmetric; bounded perturbation proves self-adjointness on precisely (2), without requiring B to map D(A) into D(C0). The same argument preserves its core and form domain. This is the actual infinite-rank block problem, not a finite spectral truncation.

The admitted multiplier formula A=H_eff+alpha lambda(20-b), -1<=b<=1, gives A>=19alpha lambda. Q2 proves C0>=3alpha on its entire complement. For lambda>0 and vectors x,y in the form domains, Young's inequality gives

    2|<Bx,y>| <= alpha lambda||x||²
                    +(25/4)alpha lambda||y||².

Consequently H_tilde is bounded below by the block diagonal with entries18alpha lambda and alpha(3-25lambda/4). Since lambda<=1/100 implies3-25lambda/4>=18lambda,

    H_lambda >= H_tilde >=18alpha lambda I.                (3)

The first relation is quadratic-form order because the omitted block alpha lambda D is positive. We use it only to infer lower spectral bounds, never to order heat semigroups. At lambda=0 both operators equal H_E, are nonnegative and reduce under P. Thus their heat semigroups are contractions throughout the frozen range. For lambda>0 their norms are at most exp(-18lambda sigma), sigma=alpha t/hbar. This is an unshifted finite-graph ground-energy lower bound, not a gap above the interacting ground.

## 2. Exact leading-memory evolution and uniqueness

Set T_tilde(t)=J*exp(-t H_tilde/hbar)J and R_tilde(t)=Qexp(-t H_tilde/hbar)J. Starting from f in D(A), the common block domain permits differentiation and gives

    hbar T_tilde'=-A T_tilde-B* R_tilde,
    hbar R_tilde'=-C0 R_tilde-B T_tilde,
    T_tilde(0)=I, R_tilde(0)=0.

The complementary equation has the mild solution

    R_tilde(t)=-(1/hbar) integral_0^t
                       exp(-(t-u)C0/hbar) B T_tilde(u) du.

Substitution and one more mild integration yield, on every selected vector,

    T_tilde(t)=exp(-tA/hbar)
       +(1/hbar²) integral_(0<=u<=s<=t)
         exp(-(t-s)A/hbar) K2(s-u) T_tilde(u) du ds,
    K2(v)=B*exp(-vC0/hbar)B.                               (4)

All integrals are strong vector integrals of uniformly norm-bounded operators on compact intervals. The differential equations have their stated initial domain; (4) extends by density to all H3. The final factor is the full T_tilde, so repeated returns are retained. The first two channel matrix elements of K2 do not replace this operator or make their two-dimensional span invariant.

Equation(4) is unique among strongly continuous, locally uniformly bounded operator families satisfying its initial condition and acting by these vector integrals. On any fixed time interval, the norm of a difference obeys the Volterra upper bound with kernel (||B||²/hbar²)(t-u). Iterating n times gives at most its initial compact-interval supremum times (||B||t/hbar)^(2n)/(2n)!, which tends to zero. For merely strong continuity, local operator boundedness follows from uniform boundedness; the iterated integral argument may also be applied vectorwise. This proves uniqueness without assuming a scalar memory fit.

## 3. Leakage and the actual projected error

For H_lambda use C>=3alpha and its exact complementary mild equation; for H_tilde use C0>=3alpha. Both selected evolutions have norm<=exp(-beta sigma), beta=18lambda. Thus for either full operator F and lambda>0,

    ||Q exp(-tF/hbar)J||
       <=(5lambda/2) exp(-beta sigma)
                    (1-exp(-d sigma))/d,
    d=3-beta>=141/50>0.                                    (5)

The bound is the exact convolution of complementary decay with the selected global lower-bound decay. It is also valid by continuity at lambda=0, where both leakage operators vanish.

Their difference is the bounded complementary perturbation alpha lambda QDQ. Bounded-perturbation Duhamel on the common domain gives the full-space identity, whose selected compression is

    T(t)-T_tilde(t)=-(alpha lambda/hbar) integral_0^t
       J*exp(-(t-s)H_lambda/hbar) QD Q
       exp(-s H_tilde/hbar)J ds.                            (6)

The left complement factor is the adjoint leakage operator for H_lambda. Applying (5) on both sides retains two powers of lambda beyond the omitted complementary block. For every sigma>=0 define

    F_d(sigma)=integral_0^sigma
             [(1-exp(-d(sigma-u)))/d][(1-exp(-du))/d] du
      =[sigma(1+exp(-d sigma))
                          -2(1-exp(-d sigma))/d]/d².        (7)

The integral definition establishes positivity and its value0 at sigma=0 without cancellation-sensitive arithmetic. The result is

    ||T(t)-T_tilde(t)||
       <=250lambda³ exp(-18lambda sigma) F_d(sigma),
    F_d(sigma)<=min(sigma³/6, sigma/d²).                     (8)

The factor250 is40*(5/2)². All powers of alpha and hbar cancel into sigma as required for a dimensionless operator difference. Equation(8) is a theorem on the full selected H3, not a finite-channel estimate or an assumed stable kernel replacement. It is O(lambda³) at any fixed sigma, and its small-time envelope is250lambda³ sigma³/6. No operator-norm Taylor series for unbounded A is invoked.

There is also a genuine uniform absolute consequence. For lambda>0, sup_sigma sigma exp(-18lambda sigma)=1/(18e lambda), so

    sup_(t>=0)||T(t)-T_tilde(t)||
       <=125lambda²/[9e(3-18lambda)²]
       <=[312500/477144]lambda².                            (9)

The last rational relaxation uses e>8/3 and d>=141/50. It therefore applies also along every growing physical-time window t=t(lambda), with exact zero error at lambda=0. This uniformity comes from the decay of *unshifted* heat operators. It gives no uniform relative error when the exact compressed operator becomes small, and no uniform comparison after subtracting an interacting ground energy. Ground-energy shifts of the two models may differ; multiplying by compensating exponential factors can defeat (9). This is the next meaningful long-time question, not an already solved consequence.

## 4. Discriminating controls and exceptions

The exact algebra checker uses a noncommuting four-dimensional block fixture to check Volterra power coefficients through order6, complementary leakage order, the leading projected difference and the minus-Schur sign. Replacing the final return factor by exp(-uA) drops the term (B*B)² at fourth order; the checker exhibits the difference. The matrix is a block-identity fixture, not a physical spin cutoff or an actual invariant selected sector.

The scalar shortcut is also tested against inherited *actual* Q2 spectral data: the instantaneous diagonal weights both equal19/4, but their first energy moments are57/4 and285/8 and the cross weight is1/4. The checker reconstructs these moments from the admitted seven energy weights. Matching one instantaneous scalar cannot reproduce that matrix-valued memory. Those two diagnostic channels still do not form a closed dynamic space.

For a common energy shift cI applied to both compared full operators, every A,C0,C diagonal changes, K2(v) gains exp(-cv/hbar), and T,T_tilde gain exp(-ct/hbar). The bounded difference scales by the same factor. A negative shift need not preserve the unshifted decay estimate (9). Shifting just one complement or omitting its kernel factor is a changed problem. At lambda=0 memory and error vanish and the exact electric selected reduction is recovered. A time-dependent lambda would require a nonautonomous derivation; it is not included here. All physical scales remain positive and fixed, and no clock coefficient is fitted.

## Sources, scope and next premise

Source reading and the actual bounded-perturbation hypotheses are recorded in source-notes.md. The domain, Volterra and Duhamel methods are standard. The explicit projected certificate and constants in this fixed physical graph are project derivations; scientific priority remains unverified.

The accepted target is a full-selected-space Euclidean approximation on this finite physical graph. It proves no autonomous finite-channel semigroup, real-time approximation, measured energy calibration, interacting-ground identification, homogeneous thermodynamic gap or four-dimensional continuum construction. A justified next question is the error after physically meaningful ground-energy centering or relative normalization; any such target must separately control the actual spectral/eigenvector shift. T2 is selected only after this report's independent review.

    python3 -B research/round23/forward/t1/check.py --output /absolute/new/t1-forward
    python3 -B -O research/round23/forward/t1/check.py --output /absolute/new/t1-forward-O
