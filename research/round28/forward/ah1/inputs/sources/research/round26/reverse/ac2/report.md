# AC2 reverse: delayed leakage improves the same-preparation heat certificate

Independent reverse analysis under AC2, without current forward AC2 access. The exact AC1 magnetic matrix and improved ground bounds originated in forward AC1; they are explicitly inherited, independently reconstructed here, and not claimed as reverse-first discoveries. The actual model remains the complete Gauss-invariant 18-vertex, 33-link, 20-face graph with L=K+lambda(20-S), 0<=lambda<=1/100, and sigma=alpha t/hbar at fixed positive physical scales.

For the mathematical exact 293-state heat centered at its own true Ritz ground, the result is

    sup_(sigma>=0) ||(E(sigma)-E293(sigma))x||/||E(sigma)x|| < 0.000048

for every normalized x in the ORIGINAL P21 space with ||x-Omega||<=0.01. For x=Omega the bound is below 0.000043. The same lambda interval and true denominator are retained. These improve the inherited 21-state certificates 0.00044 and 0.00028 respectively; they are conservative upper bounds, not measured errors or an optimal solver comparison. An exact rational retained-generator action is supplied. Numerical evaluation of the full matrix exponential is not included in these physical error bounds.

## Independently reconstruct the sparse metric matrix

Use AC1's rational basis Omega, 20 phi_f, 20 chi_f, 128 disjoint products, 62 shared singlets and 62 shared triplets. Its diagonal Gram has triplet weight three and every other weight one; K energies are 0,3,8,6,9/2,13/2 respectively. The checker reconstructs every actual graph face/pair, the 293 basis records and all 1088 sparse entries from geometry, and compares the resulting lists with the frozen forward-origin artifact.

To prove its zero pattern, multiply each positively oriented link in direction a at v by the central sign (-1)^(sum_(i<a) v_i). The product around every elementary face is -1. This measure-preserving unitary leaves K invariant, makes Omega and all new two-face/spin-one channels even, makes every phi_f odd, and sends S to -S. Therefore no retained same-parity entries exist. All old columns follow from character multiplication. Metric self-adjointness determines every remaining column; in particular a triplet has face coefficients 3/4, not 1/4. The checker rejects the metric-blind replacement.

Let P=P21, R=P293-P21 and F be the twenty-dimensional face subspace. These are orthogonal physical projections despite the rational coordinate metric. Write A=P293 L P293, mu=min spec A, E293(t)=exp[-t(A-mu)]P293 and B=Q293 L P293. The complete omitted-map facts are

    BP=0, ||B||<=20lambda,
    R(A-mu)R=K_R+(20lambda-mu)R >=(9/2)R,
    F(A-mu)F=(3+20lambda-mu)F >=3F.              (AC2.R1)

Here mu<=20lambda and R is all even, so its internal S compression is zero. The new subspace is not autonomous; B remains bounded on all 272 new inputs. Its norm estimate includes every omitted intertwiner.

The exact retained magnetic columns also give

    ||R S F||=sqrt(39)/2 <=13/4,
    ||F S (I-F)P293||=sqrt(59)/2 <4.             (AC2.R2)

For the second, the old omitted Gram is (19/4)I+(1/4)J; the extra vacuum coupling contributes (1/4)J, so the largest eigenvalue is 59/4. These are operator norms in the actual Hilbert metric. The checker reconstructs both Gram matrices from all sparse entries.

## Delayed leakage on every old prepared input

Fix unit x in P with ||x-Omega||<=eta, so ||F x||<=eta and R x=0. Put v(t)=E293(t)x. Since the true own-ground-centered retained semigroup is contractive, ||v(t)||<=1. The finite-dimensional variation-of-constants equation for its face component, (AC2.R1)-(AC2.R2), gives

    ||F v(t)|| <= eta exp(-3t)+(4lambda/3)(1-exp(-3t)). (AC2.R3)

The equation for its new component starts at zero and gives

    ||R v(t)|| <= (13lambda/4) integral_0^t
       exp[-(9/2)(t-u)] [eta exp(-3u)+(4lambda/3)(1-exp(-3u))] du. (AC2.R4)

These bounds keep feeding and return coupling through the full v(t); no autonomous original P21 dynamics is substituted. Because B=BR, integrate (AC2.R4), change integration order, and bound the inner decaying integral by 2/9. The complete time-integrated omitted leakage obeys

    integral_0^t ||B v(s)||ds <= (130/9)lambda²
      [eta(1-exp(-3t))/3
       +(4lambda/3)(t-(1-exp(-3t))/3)].          (AC2.R5)

All 272 new columns are controlled through ||B||; none is discarded. The exact old-input cancellation buys the extra generation step before leakage, though (AC2.R5) deliberately relaxes some additional short-time powers. It vanishes at time zero, unlike a constant residual inserted from the start.

## Ground centering, true denominator and all-time joining

Inherit and rederive AC1's continuous envelopes, with Lambda=1/100 and g=3-20Lambda=14/5:

    p21=1/12000, r293=1/60000,
    p293=1/168000, d293=1/10080000000.

They follow by the old Ritz residual r21<=7Lambda²/3, its actual spectral separation g, the exact Bf21=0, and the full ||B||<=20Lambda. In particular ||G-G293||<=p293 and 0<=mu-epsilon<=d293 for the actual full and retained ground data. The positive projection error is not an omitted physical gap assumption: L>=K gives the full excited spectrum >=3, while compression obeys the same min-max bound.

Set

    b=3Lambda/4+3p21/2+eta,
    a=1-5Lambda²/9-3p21/2-eta-p293 >0.           (AC2.R6)

The old exact ground and its angle to the new one give ||(I-G293)x||<=b, and the true output satisfies ||E(t)x||>=||Gx||>=a for every t. The denominator is the original full output, not the retained output or a fitted floor.

The exact strong Duhamel identity retains its centering defect delta=mu-epsilon:

    (E(t)-E293(t))x=-integral_0^t E(t-s)[B+delta P293]v(s)ds.

Its early upper bound V_eta(t) is the right side of (AC2.R5), using Lambda, plus d293 t. Independently, full and retained spectral decompositions give the late bound

    J_eta(t)=p293+(2b+p293)exp(-g t).             (AC2.R7)

V_eta increases and J_eta decreases. Therefore for any join T,

    sup_t relative_error(t,x) <=max(V_eta(T),J_eta(T))/a. (AC2.R8)

Choose T=5/2. The positive Taylor sum for exp(7) exceeds 1000, so exp(-gT)<1/1000 and exp(-3T)<1/1000. Entirely rational outward upper values are consequently

    V_eta(T) <=d293 T+(130/9)Lambda²
                  [eta/3+(4Lambda/3)(T-333/1000)],
    J_eta(T) <=p293+(2b+p293)/1000.              (AC2.R9)

The checker proves these yield less than 0.000048 for eta=0.01 and less than 0.000043 for eta=0, with exact fractions. The proof covers the entire coupling interval because every coefficient used is an analytic upper envelope at Lambda and both block damping rates retain uniform lower bounds. It is not sampled-lambda extrapolation.

At time zero E x=E293 x=x exactly. At lambda=0 P293 reduces K and mu=epsilon=0, so the physical retained-input error is exactly zero at every time. These exact exceptions supersede a nonzero loose spectral upper bound. Ground centering is retained throughout; BP=0 alone would not remove the initial derivative delta x of the own-ground-centered error.

## Arithmetic and scope

The supplied standard-library checker reconstructs the exact sparse metric operator and exposes apply_L(lambda,vector), using rational arithmetic. It executes vacuum and face/difference inputs and a triplet metric discriminant. The optional --vector-file argument accepts a JSON list of 293 rational strings and --lambda selects a rational coupling in the contract interval; its exact generator action is saved. This is a useful retained matrix action, not a pretense that 293-state exponentiation or the new ground eigenpair has been numerically evaluated. The rational proof bounds and actions have zero rounding error. Any future heat evaluator must add its own arithmetic error before advertising these thresholds for computed vectors.

Newton's reconstruction organizes sufficient error/denominator premises; Tesla's loading audit retains every new input and outside return. This finite-graph same-clock result gives no all-input relative bound, real-time accuracy theorem, graph-size uniformity, homogeneous/canonical model equivalence, mass calibration or continuum construction. Scientific priority remains unverified.
