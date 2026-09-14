# T1 reverse — full-space magnetic-memory evolution with certified error

The shared candidate defines a well-posed evolution on the entire selected Hilbert space. It realizes the leading magnetic memory with the full repeated return, and its compressed heat evolution approximates the actual full graph with a cubic error at fixed physical time. A separate positive-energy estimate also gives a uniform **absolute** error of order lambda squared in the fixed, unshifted energy convention. Neither statement supplies relative late-time accuracy, an interacting ground-state identification, measured calibration, nor continuum Yang–Mills.

The candidate was shared by root/reverse planning; this report independently proves its properties from the frozen T1 premises. No current forward T1 or skeptic T1 solution was read.

## 1. Actual spaces, domains and positivity

Keep Q2's finite physical SU(2) graph: 18 vertices, 33 edges, 20 faces, all Gauss constraints and the P2 infinite-rank Haar isometry J from the full selected H3. This is not the homogeneous S model. P=JJ* reduces the electric Hamiltonian H_E, and Q=1-P. Its actual block domains are

`D(A_lambda)=D(H_eff)` on H3,
`D(C0)=Q D(H_E)`,
`D(H_lambda)=J D(A_lambda) direct-sum D(C0)`.

The corresponding closed form domains are the inherited physical/selected H1 domains. The bounded magnetic multiplication satisfies `0<=Vmag<=40`; all twenty faces remain present. In units of alpha the block lower bounds and offdiagonal norm are

`A_lambda/alpha>=19lambda`, `C0/alpha>=3`,
`C_lambda=C0+alpha lambda QVmagQ>=C0`,
`B_lambda=alpha lambda B1`, `||B1||=5/2`.

Define the candidate on this complete block domain:

\[
\widetilde H_\lambda=
\begin{pmatrix}A_\lambda&B_\lambda^*\\B_\lambda&C_0\end{pmatrix},
\qquad
\widetilde T_\lambda(t)=J^*e^{-t\widetilde H_\lambda/\hbar}J.\tag{1}
\]

The bounded offdiagonal perturbation proves self-adjointness on exactly the displayed unbounded block domain. The forms have the corresponding direct-sum domain. No finite-channel compression replaces either diagonal block.

There is a useful stronger positivity statement. Let `m=18lambda`. On vectors (f,q), the form of `(Htilde-alpha m)` is bounded below by alpha times

`lambda||f||^2+(3-18lambda)||q||^2-5lambda||f||||q||`.

The associated scalar two-by-two form is nonnegative when

`lambda[(3-18lambda)-(25/4)lambda]
 =lambda[3-(97/4)lambda]>=0`.

This holds for `0<=lambda<=1/100`, with strict positivity of this two-by-two form when lambda>0. Since the exact Hamiltonian differs from Htilde by the positive complementary block `alpha lambda QVmagQ`,

\[
\boxed{H_\lambda\ge\widetilde H_\lambda\ge18\alpha\lambda I.}\tag{2}
\]

This is an **absolute energy floor in the retained energy origin**, not a gap above the interacting ground. It does not assert semigroup order between the noncommuting operators. It does imply separately

`||exp(-tH/hbar)||, ||exp(-tHtilde/hbar)|| <= exp(-18lambda sigma)`,

where `sigma=alpha t/hbar`. In particular both semigroups and their compressions are contractions. At lambda zero, both are exactly the admitted electric evolution and their zero vacuum is retained.

## 2. Exact leading-memory return and uniqueness

For f in the selected operator domain, evolve the initial state (f,0) with Htilde. Write its selected and complementary components as u(t),v(t). Their common block domain and bounded B give the strong equations and variation of constants

`v(t)=-hbar^(-1) integral_0^t exp(-(t-r)C0/hbar) B_lambda u(r) dr`.

Substitution into the selected equation proves

\[
u'(t)=-A_\lambda u(t)/\hbar
 +\hbar^{-2}\int_0^t K_2(t-r)u(r)\,dr,\qquad
K_2(s)=B_\lambda^*e^{-sC_0/\hbar}B_\lambda.\tag{3}
\]

Its mild form on every selected vector is

\[
\widetilde T(t)=E_A(t)+\hbar^{-2}
\int_0^t ds\int_0^s dr\,
E_A(t-s)K_2(s-r)\widetilde T(r).\tag{4}
\]

All integrals are strong vector integrals, with bounded integrands controlled on each finite time interval. Equation (4) contains the complete returned Ttilde, not E_A in its rightmost position. It is a full-space realization of Q2's leading kernel; the two tabulated channels are only matrix elements of that kernel.

Existence follows from (1). For uniqueness among strongly continuous, locally uniformly bounded operator families satisfying (4), subtract two candidates. On `[0,T]`, iteration of the difference equation yields

`||D(t)|| <= M_T (||B_lambda|| t/hbar)^(2n)/(2n)!`

for every n, using the contraction of E_A, the kernel bound `||K_2||<=||B_lambda||^2`, and the nested simplex volumes. The right side tends to zero. The same argument works vectorwise with locally bounded solutions. Thus no stability assumption is omitted when replacing the exact kernel by its leading full-space kernel.

The corresponding resolvent elimination has the inherited minus self-energy sign:

`J*(Htilde+z)^(-1)J=[A_lambda+z-B_lambda*(C0+z)^(-1)B_lambda]^(-1)`

for z>0, on D(A_lambda). The actual lower bound and bounded offdiagonal blocks justify the elimination and inverse. A plus sign would represent a different equation.

## 3. Projected Duhamel comparison with two controlled leakages

Normalize the generators by alpha and use sigma as time. Let b=(5/2)lambda and `W=QVmagQ`, with `||W||<=40`. The exact difference between the generators is `lambda QWQ`. Bounded-perturbation Duhamel on their common operator domain, extended by density, gives

\[
T(\sigma)-\widetilde T(\sigma)
=-\lambda\int_0^\sigma
 J^*e^{-(\sigma-r)H/\alpha}QWQ
 e^{-r\widetilde H/\alpha}J\,dr.\tag{5}
\]

There is a complementary leakage on each side. For either generator, variation of constants in its complementary block gives

`||Q exp(-sH/alpha)J|| <= b integral_0^s exp(-3(s-r)) dr
 = (b/3)(1-exp(-3s))`,

and identically for Htilde. The adjoint gives the needed left leakage. Therefore

\[
\boxed{
\|T(t)-\widetilde T(t)\|
\le {250\over9}\lambda^3 I_3(\sigma),\quad
I_k(\sigma)=\sigma(1+e^{-k\sigma})
-{2\over k}(1-e^{-k\sigma}).}\tag{6}
\]

Indeed `I_k(sigma)=integral_0^sigma (1-exp(-k(sigma-r)))(1-exp(-kr))dr>=0`. This calculation uses both actual generators, not a cubic kernel-error insertion without a solution bound. It also yields

`||T-Ttilde|| <= min(1, (125/3)lambda^3 sigma^3, (250/9)lambda^3 sigma)`.

The first bound follows because both compressions are positive contractions; the cubic one follows from `1-exp(-x)<=x`. Thus the error is O(lambda^3) at every fixed sigma. The linear bound alone would tend to zero for growing windows sigma=O(lambda^(-p)) with p<3; it would not settle the p=3 endpoint. The additional energy estimate below proves a stronger **absolute** statement and must not be confused with relative behavior.

## 4. Separate proof of a uniform absolute bound

Use (2) in the same leakage integral. With `m=18lambda` and `k=3-m`,

`||Q exp(-sH/alpha)J||
 <= b (exp(-ms)-exp(-3s))/k`,

and the same bound holds for Htilde. Since `k>=141/50>0`, equation (5) now gives

\[
\boxed{
\|T(t)-\widetilde T(t)\|
\le {250\lambda^3\over k^2}e^{-m\sigma}I_k(\sigma).}\tag{7}
\]

This is valid for every t>=0 and the whole frozen lambda range, with zero error when lambda=0. For lambda>0, `I_k(sigma)<=sigma` and `sup_(sigma>=0) sigma exp(-m sigma)=1/(em)` imply

\[
\sup_{t\ge0}\|T(t)-\widetilde T(t)\|
\le {125\over9e k^2}\lambda^2
\le {312500\over178929e}\lambda^2.\tag{8}
\]

The numerical last coefficient is approximately 0.643; the displayed expression is the certificate. Equation (7) additionally bounds the short-time error by `(125/3)lambda^3 sigma^3 exp(-18lambda sigma)`.

The uniform absolute bound is meaningful for the stated unshifted heat operators, which both tend to zero when lambda>0. It is **not** a bound on their normalized ratio, relative error, logarithmic decay rate, ground-centered correlation, or interacting ground projection. Small absolute differences between exponentially decaying signals may coexist with large relative errors. The scalar energy floor used here is not a measured mass and is not transferred to another model.

## 5. Controls, energy conventions and limitations

The exact checker constructs noncommuting finite block matrices satisfying the conservative bounds, verifies the lower-form certificate, and checks the actual fourth-order repeated-return term `(B*B)^2/4!`. Deleting repeated returns changes that coefficient. It rejects a wrong Volterra sign already at second order and a wrong Schur sign by exact rational inversion. A rigorous finite-matrix exponential enclosure checks the projected error inequality in a nonzero-coupling fixture. These matrices test the operator identities and estimates; they are not a truncation of the actual physical graph.

The actual Q2 two-channel leading kernel has seven energies, a nonzero offdiagonal coefficient, and unequal first moments `57/4` and `285/8` despite equal initial diagonals `19/4`. The checker independently totals those admitted exact weights. These controls reject a shared scalar exponential and an autonomous two-channel interpretation; the certified approximation uses full C0, B and A on their actual Hilbert spaces.

A common scalar shift beta I of **both** full generators changes both compressed evolutions and their difference by `exp(-beta t/hbar)`. The complementary block, selected block and all memory time factors shift consistently. Shifting only A leaves the complementary kernel's first derivative wrong. If beta is negative, an unshifted absolute contraction or uniform bound cannot be retained without its corresponding factor. A normalized-ground convention is therefore a distinct question, not supplied by (8).

Alpha, hbar, E_star and lattice spacing are fixed positive scales; `sigma=alpha t/hbar` is merely their dimensionless combination. No clock or action coefficient is fitted. Lambda is constant in time. A time-dependent lambda would require a different nonautonomous evolution and is not covered by this proof.

The closest checked primary structures remain those in the inherited P2/Q1/Q2 source review, notably Burbano and Bauer's [full electric/magnetic and invariant-tensor construction](https://arxiv.org/html/2409.13812v2). This loop read the inherited reports; it did not claim a fresh complete-paper audit. Block elimination, bounded perturbation and Duhamel are standard methods. The actual-model cubic and uniform absolute certificates above are project derivations; scientific priority is unverified.

No finite-spin truncation error is hidden: the theorem concerns the full finite-graph spaces. However, this does not make the formula a completed finite executable simulation of all those infinite-dimensional operators. A practical numerical implementation would need an independently controlled spectral/spatial approximation. Relative late-time accuracy, interacting ground reconstruction, physical calibration, a homogeneous mass gap and the four-dimensional continuum construction remain open.

T2 should be selected from these reviewed limits, for example testing ground-centered or relative behavior with the actual spectral data, or certifying an implementable full-space truncation. No T2 investigation is executed here.

Reproduce with `python3 -B research/round23/reverse/t1/check.py --output /tmp/ym23-reverse-t1-fresh` and a separate fresh optimized run.
