# C1 advisor watch

Status: active watch only. This is not a C1 gate and does not freeze C2.

C1 is authorized only after the accepted B2 gate and is scoped to the static U-V-W chain integral in `advisor/contract-c1.json`. The result may be a valuable static common-variable checkpoint, but it must not be presented as physical time-generator matching, dense stability, finite-volume convergence, continuum Yang-Mills, or a mass-gap theorem.

## Required scope checks

The first gate question is geometric. The producers must reconstruct the actual four-cube signed graph rather than hard-code the reduced variables. Expected counts are 18 vertices, 33 edges, 20 faces, active vertical links U at `(1,1,0)`, V at `(1,0,0)`, W at `(0,0,0)`, 30 fixed links, seven affected faces, and 13 constant faces. The seven affected face words must reduce to

\[
S=3x+y+z+w+t,
\]

where `x=Tr(U)/2`, `y=Tr(V)/2`, `z=Tr(W)/2`, `w=Tr(U V^dagger)/2`, and `t=Tr(V W^dagger)/2`. The observable remains

\[
O=(4x^2-1)^3(4w^2-1)/81.
\]

The freeze-W regression is mandatory: setting `W=I` gives `S=3x+2y+w+1`, so the normalized quotient must recover the Round18 C2 two-link value after the constant factor cancels.

## Moment and normalization checks

The key mathematical discriminator is the unweighted Haar common-V moment

\[
E[x z w t]=1/64.
\]

A model that resamples independent V copies for the U-V and V-W branches gives zero and must fail as the primary model. This is the intended failed-independence exception.

The two exact routes should be genuinely distinct. One route may use character fusion with the frozen formula

\[
2^{-(a+b+c+d+e)}\sum_{i,k,m}\frac{m(a,i)m(d,i)m(c,k)m(e,k)m(b,m)N(i,k,m)}{(i+1)(k+1)},
\]

for exponents on `(x,y,z,w,t)`. The other should use conditional angular or coordinate polynomial integration and must be regular at `y=±1`.

The conditional-weight checkpoint must be explicit. After integrating W at fixed V,

\[
K_\kappa(y)=\sum_m \frac{(\kappa^2(1+y)/2)^m}{m!(m+1)!},
\]

and the outer V weight is `exp(kappa*y) K_kappa(y) Z_U(V)`. Averaging normalized inner expectations against bare Haar, or dropping `Z_U(V)`, is a different calculation.

## Evidence required before gate

- normal and optimized forward and reverse outputs for the predeclared degree ladder `0,2,4,6,8`, target width `1e-12`, max total moment 16;
- exact graph/reduction JSON with signed face words and active/fixed face ledger;
- exact moment tables and numerator/partition/refinement interval outputs;
- source manifests that fail closed on missing source/output entries;
- a final independent forward/reverse comparison that reconstructs graph, moments, normalized intervals, controls and scope wording from actual bytes.

## Controls to watch

- wrong graph counts, active links, affected faces, or constant-face ledger;
- altered signed word on a noncommuting fixture;
- hard-coded reduced action without graph derivation;
- independent trace variables or independent V copies used as primary;
- missing SU(2) dimension divisors or wrong parity/triangle fusion;
- missing true outer partition weight or using bare-Haar averaged normalized inner values;
- failed freeze-W regression or mishandled constant `+1`;
- truncated Taylor coefficients labeled as a full integral without a rigorous remainder;
- noncanonical rational kappa, wrong kappa, Boolean/negative/wrong-dimension exponents, mutable cache aliasing;
- kappa, Fibonacci or static labels claimed as physical energy-scale matching;
- forcing a consistent dagger substitution to mismatch at the integrated level when it is a Haar-preserving change of variables. Signed-word reconstruction still has to be pointwise checked.

## C2 selection hold

Do not freeze C2 from plans. After C1 gate, choose the next loop from actual C1 evidence. A valid C2 must make a new scientific step beyond rerunning the same `kappa=1/64` integral, for example a larger/signed-coupling certificate or a rigorous wrong-measure bias theorem if the C1 outputs support it.
