# AH2 independent pre-exchange derivation

The unchanged AH1 graph admits a complete delayed-loading certificate

\[
 \frac{\|e^{-\sigma(L-\epsilon)}x-e^{-\sigma(A-\mu)}x\|}
      {\|e^{-\sigma(L-\epsilon)}x\|}
 \leq \frac{4501862190047}{53190472572678750}
 <\frac1{10000},\qquad \sigma\geq0.
\]

Here the second exponential is embedded from the retained space, both centers are their actual independent ground energies, `0<=lambda<=1/100`, and x is any normalized complex vector in the original strict-cutoff space P0 with `||x-Omega||<=1/100`. The decimal of the exact upper certificate is about `0.00008463662705563888`. This is an analytic physical omission budget, not an evaluated heat-vector error. No optimality or comparison with an actual numerical error is claimed.

The source inventory was frozen before this derivation or checker. No current AH2 forward or reverse scientific file was read. AH1's admitted Haar construction, physical basis, complete matrix and isolation theorems are shared premises. The new checker parses and independently reconstructs their relevant blocks and exact norm data; it imports and executes no historical checker. This report does not claim a new comprehensive reproof of AH1.

## Physical model and complete block

The full space remains `L2(SU(2)^46,Haar)^SU(2)^24` on the open `3x2x1`-cell graph. Every one of the 46 original link Casimirs enters K, with all 24 original endpoint Gauss actions. There are 29 oriented plaquettes. The positive gauge-invariant Laplacian has the physical H2 operator domain, H1 form domain, a smooth Peter–Weyl core and compact resolvent. The bounded self-adjoint multiplier `lambda(29-S)` preserves these domains. The admitted pointwise inequality `0<=29-S<=58` implies `L>=K`. The physical clock remains `sigma=alpha*t/hbar` with the contract's positive reference scales fixed.

Write P for the admitted rank561 projection, P0 for the strict rank30 projection, `N=P-P0` for its rank531 complement, `F=P0-|Omega><Omega|`, and `Q=I-P` for the infinite full outside. A is `PLP` on P. In the supplied physical metric the complete new basis consists of:

| Channel | Count | Squared norm | K energy |
|---|---:|---:|---:|
| same-face spin one | 29 | 1 | 8 |
| disjoint pair | 310 | 1 | 6 |
| shared-edge singlet | 96 | 1 | 9/2 |
| shared-edge triplet | 96 | 3 | 13/2 |

The complete AH1 magnetic action has 2124 nonzero entries and 312597 exact zero entries. In particular `NSN=0` on all 531 new states and `NS Omega=0`. Therefore, using `mu<=29 lambda`,

\[
 D_N:=N(A-\mu)N=K_N+(29\lambda-\mu)N\geq dN,
 \qquad d=9/2.
\]

This is an exact block identity, not an assumption that N reduces A. The off-diagonal blocks couple N to F. Let `T=NSF` and `C=NAF=-lambda T`. Fresh summation over every new channel, with the triplet metric 3, gives

\[
 T^*T=7I_{29}+\tfrac14J_{29},\qquad
 \|C\|=\lambda\sqrt{57}/2.
\]

The bright eigenvalue of the Gram matrix is 57/4 and its 28 dark eigenvalues are 7. The checker independently constructs all oriented faces, individually matches every basis label/metric/energy, reconstructs all complete magnetic entries, checks every Gram entry, and checks the nonzero contribution of each of the 531 new rows. No bright-only dynamical reduction is used.

## Centers, projectors, stationary and excited components

Put `Lambda=1/100`, `eta_class=1/100`, and

\[
\begin{aligned}
 g&=3-29\Lambda=271/100, &r_0&=41\Lambda^2/12, &p_0&=r_0/g,\\
 r_+&=29\Lambda p_0, &p_+&=r_+/g, &d_+&=r_+^2/g.
\end{aligned}
\]

These are uniform upper budgets. They are not equalities for actual residuals or projector distances. Both separate AH1 comparisons are retained:

\[
 \|G-G_0\|\leq p_0,
 \qquad \|G_P-G_0\|\leq p_0.
\]

Here G, G0 and GP are the exact full, original rank30 Ritz and enriched rank561 ground projectors. Their use follows the admitted full variational ordering and isolation: every relevant second eigenvalue is at least 3, while `0<=epsilon<=mu<=mu0<=29 lambda<3`. The original normalized Ritz vector has full residual at most r0, and its full L image belongs to P, so the same residual controls both separate comparisons. Since `BG0=0` for `B=QLP`, the enriched ground has full residual at most `29 Lambda p0=r+`. The full spectral angle and Temple estimates give `||G-GP||<=p+` and `0<=mu-epsilon<=d+`.

The tighter admitted reverse AH1 envelope `q0=(9/10)Lambda` is used with explicit attribution to that proof. It follows directly from the original Ritz parameter `h<=lambda/6`, vacuum angle `sqrt(29)h/sqrt(1+29h^2)`, and `sqrt(29)<27/5`.

Define

\[
 q=q_0+p_0=14839/1626000,\qquad
 b=q+\eta_{\rm class}=31099/1626000.
\]

For the actual normalized enriched ground f, the rank-one angle identity and the second projector comparison imply

\[
 \|Ff\|\leq\|(I-P_\Omega)f\|
 =\|(I-G_P)\Omega\|\leq q_0+p_0=q.
\]

The first comparison gives the corresponding full ground/vacuum angle. Consequently both full and retained excited components of every allowed x have norm at most b. Spectral isolation gives the complete, complex-vector estimate

\[
 u(s)=e^{-s(A-\mu)}x,\qquad
 \|Fu(s)\|\leq q+b e^{-gs}.
\]

The q term is stationary. Omitting it would discard the actual interacting ground component.

For the true full output the original Ritz vacuum overlap is at least `z0=1-29 Lambda^2/72`. Thus

\[
 \|e^{-s(L-\epsilon)}x\|\geq\|Gx\|
 \geq z_0-\eta_{\rm class}-p_0
 =D=193136341/195120000>0.
\]

This is the admitted true-output denominator, not a retained or rounded-output norm.

## Exact delayed loading with feedback

Since `Nx=0`, the exact finite-dimensional block equation is

\[
 \frac{d}{ds}Nu(s)=-D_NNu(s)-CFu(s),\qquad Nu(0)=0,
\]

and hence

\[
 Nu(s)=-\int_0^s e^{-(s-r)D_N}CFu(r)\,dr.
\]

The source is the full evolving retained trajectory. Its equation still contains the return term `-C* Nu`; no Born approximation, prescribed free source or omitted return path has been introduced. Define the rational simultaneous source envelope

\[
 c=151\Lambda/40>\Lambda\sqrt{57}/2.
\]

For every allowed lambda, x and s,

\[
 \|Nu(s)\|\leq Y(s):=
 c\left[\frac{q(1-e^{-ds})}{d}
       +\frac{b(e^{-gs}-e^{-ds})}{d-g}\right].
\]

Both terms are integrals of nonnegative kernels. The first is ground loading; the second is the complete excited loading. Their exact integral is

\[
 I(s)=c\left[\frac qd\left(s-\frac{1-e^{-ds}}d\right)
 +\frac b{d-g}\left(\frac{1-e^{-gs}}g-\frac{1-e^{-ds}}d\right)\right].
\]

The integral is nondecreasing because `I'=Y>=0`; this conclusion is not inferred by differentiating numerical samples. A convenient all-time upper envelope is

\[
 I(s)\leq c\left(\frac{qs}d+\frac b{gd}\right).
\]

Indeed the first kernel integrates to at most `s/d`, and the second nonnegative convolution integrates over `[0,infinity)` to `1/(gd)`. The simplified upper envelope is deliberately slack at zero time. The exact Y and I vanish at zero time.

## Full outside evolution and the fixed all-time join

The admitted simultaneous outside envelope is `||B||<=29 Lambda`. Its exact annihilation `BP0=0` implies `Bu=B Nu`; it does not imply B=0. On a normalized same-face spin-one input B has an actual outside spin3/2 component with magnitude `lambda/2`.

The strong Duhamel identity, initially on the admitted smooth finite retained inputs and then by the bounded integral, is

\[
 (e^{-s(L-\epsilon)}-e^{-s(A-\mu)})x
 =-\int_0^s e^{-(s-r)(L-\epsilon)}
       [B+(\mu-\epsilon)P]u(r)\,dr.
\]

The sign and scalar-center defect are retained. The full exact centered semigroup on the left of the source is a contraction. It contains the entire outside evolution, including all return paths. Thus

\[
 V(s):=d_+s+29\Lambda I(s)
 \leq \bar V(s):=d_+s+
 29\Lambda c\left(\frac{qs}d+\frac b{gd}\right).
\]

This proves an absolute error bound. The affine nondecreasing `bar V` controls every real `0<=s<=3` by its value at 3. At late times the spectral projector comparison gives, conservatively retaining the admitted extra slack,

\[
 J(s)=p_++(2b+p_+)e^{-gs}.
\]

Both actual centered excited semigroups decay at least at rate g. A positive Taylor sum through degree30 proves `exp(3g)>3000`, so for all `s>=3` one has

\[
 J(s)\leq p_++(2b+p_+)/3000
 =34696603/1321938000000
 <\bar V(3).
\]

The exact uniform early cap is

\[
 \bar V(3)=4501862190047/53736779700000000.
\]

Its contributions are:

| Term | Exact upper budget | Decimal for reading |
|---|---|---:|
| stationary loading | 64979981/975600000000 | 0.0000666051465765 |
| excited loading | 136182521/7931628000000 | 0.0000171695547245 |
| independent-center defect | 1413721/955320528000000 | 0.00000000147983945 |

Dividing the maximum early/late absolute budget by D proves the displayed all-time result. It strictly improves the common AH1 sufficient bound `11/5000`. The stationary contribution is the largest term in this particular proof. The fixed predeclared join is 3; no join optimization was performed.

All bounds were derived with simultaneous cap constants, so they cover every real coupling in the full interval. The proof does not interpolate the fixture couplings. At zero coupling the exact heats agree on P0 for every time because K reduces P, and at zero time both equal x for every allowed coupling. These exact zero-error statements override slack cap bounds.

## Executed fixtures and discriminating controls

The checker uses only the prescribed 27 combinations: three couplings `{0,1/200,1/100}`, three heat parameters `{0,1,3}`, and three preparations `{Omega, sqrt(1-eta^2)Omega+eta phi0, sqrt(1-eta^2)Omega+i eta phi0}` with `eta=1/200`. The last two have exact metric norm1. Their squared distance from Omega is `2-2sqrt(1-eta^2)`, strictly larger than `eta^2` but below `1/10000`. Therefore eta is correctly treated as the face coefficient, not the exact distance. Every row remains a certificate using the entire unchanged preparation class; no numerical heat vector is evaluated.

Positive Taylor terms plus a geometric tail produce rational exponential enclosures. Taking reciprocals and rounding outward on a rational `10^-30` grid bounds both exponentials in the explicit Y and I formulas. At zero arguments the exact value1 is used. These checks verify the declared fixture certificates; the preceding inequalities prove the continuous quantifiers.

Executed controls include:

- N and Q differ on actual spin-one and spin3/2 vectors. In particular `||NS phi0||^2=29/4` while `QS phi0=0`. Confusing N with Q would erase actual loading.
- Each of all 531 new channels has strictly positive contribution to the normalized bright source norm. Deleting any row loses that contribution. This is a completeness test of the exact Gram, not a claim that a separately retained conservative upper constant becomes invalid merely because a smaller matrix also fits beneath it.
- Replacing the triplet metric3 with1 changes the complete bright norm. The physical metric is necessary for adjoints and operator norms.
- `BP0=0` coexists with the actual nonzero spin3/2 outside coefficient `lambda/2` on a new input.
- The actual feedback product is `C*C=lambda^2(7I+J/4)`. Its first-face second-derivative return on the declared nonzero face preparation is nonzero. A one-way triangular replacement therefore changes the actual matrix evolution.
- Dropping the stationary term is refuted on the actual retained ground. The vacuum row of its eigen-equation yields `(29lambda-mu)a=(lambda/2) sum_p f_p`. The admitted variational inequality `mu<=mu0=29lambda-w` and `a>=1-q^2` give a strictly positive lower bound for `||Ff||`. Using the outward Ritz radical enclosure, the checker shows that for the declared vacuum preparation at cap coupling and time3, the ground face contribution minus the excited tail already exceeds an excited-only proposed upper bound. This is a matrix-based physical inequality, not an extra heat-vector sample.
- An explicitly labeled abstract scalar-ground shift demonstrates why rounded centers cannot be exponentiated uniformly over unbounded time. The actual physical center defect stays in the Duhamel budget.
- An abstract norm counterexample rejects replacing the smaller proved true denominator by a retained norm1. The physical theorem instead uses the actual full ground overlap D.
- The abstract polynomial `s(s-1)(s-3)` demonstrates that agreement at the three fixture times is not an all-time proof. Its evaluation at2 is an inference control, not an additional physical fixture.
- Doubling the clock changes the original K-face derivative from3 to6. The existing smaller-graph accuracy is not transferred; this bound remains above that unrelated `0.000037` certificate.

No nondiscriminating candidate control or failed run occurred in this independent production. Exact interval arithmetic and the fresh normal/optimized executions are recorded separately.

## Scope limits

This is a sufficient all-time same-clock omission bound for exact own-ground-centered heat on the one specified graph, coupling interval and preparation class. It evaluates no finite matrix exponential, supplies no rounded numerical ground center, and claims no actual observed error. It does not extend to arbitrary full-space initial vectors, real time, changing graph size, matching the original physical model, or thermodynamic/continuum Yang–Mills construction or gap. The existing finite retained block, full physical ambient space, independent actual centers and true denominator remain essential. No later research goal was selected or executed.
