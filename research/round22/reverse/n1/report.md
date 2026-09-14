# N1 reverse reconstruction: stationary local correlations

## Frozen independent verdict

The proposed estimate is valid in the frozen canonical summable full-link
model. It proves uniform convergence on fixed local-observable windows
`T_q=(hbar/alpha) C (1-q)^(-gamma)` for `0<=gamma<3`. For a nonempty
incident-face set the displayed certificate has a positive limit at `gamma=3`;
the actual endpoint correlation is unresolved. This report and its executable
were derived without reading current Round22 forward or skeptic solutions.
Inherited Round21 proofs and the frozen contract are shared premises.

The contribution is a quantitative application of established bounded
perturbation and strong-operator methods, not a new general dynamics theorem.
Scientific priority is unverified. N2 is unselected here.

## 1. Reverse target and sufficient premises

Work on the admitted selected-strip/free incomplete tensor product over the
nonnegative-octant cubic graph, in its fixed reference representation. Write
`H0=H_ref`, `Omega=Psi_ref`, and `H=H_q=H0+V`. The fixed reference factors
include the entire ten-link selected strips, not just individual displayed
Wilson loops. The reference Hamiltonian is the nonnegative sum of independent
factor Hamiltonians. The bounded self-adjoint perturbation is

\[
 V=-\alpha\tau_q\sum_{f\ {
 omitted}}q^{x_f+y_f+z_f}x_f/24,\qquad x_f=\operatorname{Tr}(U_f)/2,
 \quad\|x_f\|\le1.
\]

The repeated `x_f` in the exponent denotes the base-coordinate component;
in the operator symbol it denotes the normalized Wilson multiplier. To avoid
this notational collision below, use `r(f)=x+y+z` and `w_f(q)=q^{r(f)}/24`.
The series converges in operator norm for each `q<1`. Define

\[
 p(q)=2+5q+5q^2+6q^3+3q^4,\quad
 \mathcal B(q)=\frac{p(q)}{24(1-q)^3(1+q)^2(1+q^2)},\quad
 \tau_q=\frac{\eta}{8\mathcal B(q)},\quad
 \bar g=\frac{\alpha(1-\eta)}8.
\]

`mathcal B` is the profile budget; `B` below is an observable. The inherited
M1/M2 gates supply a simple stationary ground vector `Psi_q`, its energy `e_q`,
and the rank-one projector distance

\[
 d_q=\|P_q-P_0\|\le\frac{\sigma_q}{\bar g},\quad
 \sigma_q^2=\frac{\alpha^2\tau_q^2\mathcal B(q^2)}{96},\quad
 -\frac{\sigma_q^2}{\bar g}\le e_q\le0.
\]

The reverse proof requires: (i) stationary states, (ii) trace-distance control,
(iii) bounded `V`, (iv) complete reference-factor support preserved by reference
evolution, and (v) the local commutator sum. A vector-residual estimate alone
would retain the old time-times-sigma term. Domain invariance by arbitrary
bounded `A` or `B` is neither required nor true in general.

Fix bounded complex gauge-invariant local `A,B`; their complete finite covers
are fixed as `q` varies. Keep spacing, `E_star>0`, `alpha/E_star>0`, `hbar>0`
and `0<eta<1` fixed. `q,eta,tau_q` are dimensionless action-profile parameters;
`alpha,sigma_q,e_q,gbar` are energies; `t` has physical time units. `C>0` and
`gamma>=0` specify an observation window, not a clock fit or model deformation.

## 2. Reconstruct the stationary Heisenberg form first

Let `U_j(t)=exp(-it H_j/hbar)` and
`beta_j(t)(X)=U_j(t) X U_j(-t)`. This convention has the negative sign inherited
from the contract's propagator. For `H_j Psi_j=e_j Psi_j`,

\[
 \beta_j(t)(B)\Psi_j
 =e^{ite_j/\hbar}U_j(t)B\Psi_j
 =e^{-it(H_j-e_j)/\hbar}B\Psi_j.
\]

Consequently the contract correlation is exactly

\[
 C_j(t)=\omega_j(A^*\beta_j(t)(B))
            -\omega_j(A^*)\omega_j(B).
 \tag{1}
\]

Replacing `H_j` by `H_j-c_j I` leaves beta unchanged, because its two scalar
phases cancel. This cancellation is legitimate in (1), after using the
stationary eigenvector identity. It does not permit deleting `e_j` from the
original single-unitary matrix element. Identity observables reject that
deletion. A nonstationary state likewise need not permit (1).

For complex observables `omega(A*)=conj(omega(A))`. With the shifted unitary
fixing the vacuum, (1) equals the matrix element between centered vectors
`(A-omega(A))Psi` and `(B-omega(B))Psi`. It is invariant under adding independent
complex scalar constants to either observable. Both mean factors must change
when the state changes.

## 3. Strong integral without an unbounded-domain step involving B

We prove the following bounded-perturbation identity for every bounded B and
all real t, before invoking locality:

\[
 \boxed{\beta_q(t)(B)-\beta_0(t)(B)
 =-\frac{i}{\hbar}\int_0^t
 \beta_q(t-s)\bigl([V,\beta_0(s)(B)]\bigr)\,ds.}
 \tag{2}
\]

The integral is strong: apply its integrand to any Hilbert-space vector and
integrate in that vector's norm. It is not asserted to be a Bochner integral
in the operator-norm Banach space `B(H)`.

Since V is bounded self-adjoint, H is self-adjoint on exactly `D(H0)`. Put
`W(s)=U_q(-s)U_0(s)`. On `D(H0)` the two unitary groups preserve their common
domain, and the ordinary product rule, applied to a domain vector, gives

\[
 W'(s)\psi=\frac{i}{\hbar}U_q(-s)V U_0(s)\psi.
 \tag{3}
\]

For clarity, the variable-vector product rule is valid here because the
reference orbit is continuous in the `H0` graph norm and hence in the H graph
norm: `H=H0+V` with V bounded. There is no B in this differentiation.
Integrating (3) on a finite interval first on the dense common domain and
then extending by the bound `||V||/hbar` gives

\[
 (W(b)-W(a))\psi=\frac{i}{\hbar}\int_a^b
 U_q(-s)V U_0(s)\psi\,ds
 \quad(\psi\in\mathcal H).
 \tag{4}
\]

The integrand is strongly continuous. Equation (4) and the vector fundamental
theorem of calculus prove (3) for every vector, with a uniformly bounded
derivative and `||W(b)-W(a)||<=|b-a|||V||/hbar`. The adjoint is strongly
differentiable as well; this follows directly by subtracting
`W(s+h)^*W(s+h)=I=W(s)^*W(s)`, using the bounded difference quotients.

For fixed t, define the bounded interpolation

\[
 F_t(s)=U_q(t)W(s)B W(s)^*U_q(-t).
\]

All differentiated factors now have bounded strong derivatives on the whole
Hilbert space. Their product rule is justified by the uniform bounds and
strong continuity. Substituting (3) and its adjoint gives

\[
 F_t'(s)=\frac{i}{\hbar}\beta_q(t-s)
                  ([V,\beta_0(s)(B)]).
\]

Since `F_t(0)=beta_q(t)(B)` and `F_t(t)=beta_0(t)(B)`, integration gives (2),
including negative t by oriented integration. For any vector psi, the
integrand in (2) applied to psi is norm continuous: products of uniformly
bounded strongly continuous maps are strongly continuous. It is bounded by
`2||V||||B||||psi||`. Thus the integral defines a bounded operator and

\[
 \|\beta_q(t)(B)-\beta_0(t)(B)\|
 \le\frac1\hbar\int_{\min(0,t)}^{\max(0,t)}
       \|[V,\beta_0(s)(B)]\|\,ds.
 \tag{5}
\]

The operator norm in the integrand is measurable, for example by taking the
supremum over a countable dense unit-vector set in this separable incomplete
tensor product. Alternatively the uniform constant bound used below follows
directly from the vector integral and requires no norm continuity assumption.

## 4. Recover the complete support needed in (5)

Let `F_B` be a finite set of complete reference factors supporting B and
`E(F_B)` the union of every link in those factors. The reference nonnegative
form sum splits into its finite factor part and its exterior part. Their
spectral measures commute, and their unitary product therefore gives

\[
 \beta_0(s)(B)
 =U_{0,F_B}(s) B U_{0,F_B}(-s)\otimes I_{F_B^c},\qquad
 \|\beta_0(s)(B)\|=\|B\|.
 \tag{6}
\]

This is valid for all real s, even if B does not preserve `D(H0)`. Displayed
link support can move within a dressed strip, while this complete cover
remains fixed. Evolution by H_q is not claimed to preserve this finite cover;
in (5) its outer conjugation is used only as a norm-preserving map.

A strip anchored at `(4i,2j,k)` has the six x-links with tails
`(4i+r,2j+s,k)`, `r=0,1,2`, `s=0,1`, and four y-links with tails
`(4i+r,2j,k)`, `r=0,1,2,3`. Other links are free singleton factors. This is
the inherited unique ownership partition. A face not meeting E acts on link
tensor factors disjoint from this cover and commutes with the evolved B.

Let `N(F_B)` be the omitted faces whose link set intersects E and

\[
 D_{F_B}(q)=\sum_{f\in N(F_B)}q^{r(f)}/24.
\]

For a link with tail v and direction a, its incident faces in each transverse
direction b have base v or `v-e_b`; the latter exists only in the octant.
There are at most four faces per link. Deduplicate faces and remove selected
faces, yielding `m=|N(F_B)|<=4|E(F_B)|`. Therefore

\[
 D_{F_B}(q)\le m/24\le|E(F_B)|/6,\quad
 \|[V,\beta_0(s)(B)]\|
 \le2\alpha\tau_q\|B\|D_{F_B}(q).
 \tag{7}
\]

Termwise commutation is justified by norm convergence of the defining series
for V. Only the finite incident-face set remains, for every reference time.
Combining (5) and (7) proves

\[
 \boxed{\|\beta_q(t)(B)-\beta_0(t)(B)\|
 \le2\alpha\tau_q |t|\|B\|D_{F_B}(q)/\hbar.}
 \tag{8}
\]

The origin-xz loop gives a concrete complete cover with 22 links and 28
incident omitted faces. Counting just its four displayed links gives five
faces and is inadequate for arbitrary evolved bounded factor operators.

## 5. Close the centered correlation comparison

For two rank-one state projections, the nonzero eigenvalues of their
difference are `+d_q,-d_q` on their at-most-two-dimensional span. Thus
`||P_q-P_0||_1=2d_q`, and for every bounded complex X,

\[
 |\omega_q(X)-\omega_0(X)|\le2d_q\|X\|.
\]

Compare the first term in (1) in two stages: change the state while holding
`A* beta_q(t)(B)` fixed, costing `2d_q||A||||B||`; then change beta in the
reference state, costing `||A|| ||beta_q(t)(B)-beta_0(t)(B)||`. For the means,

\[
\begin{split}
 |\omega_q(A^*)\omega_q(B)-\omega_0(A^*)\omega_0(B)|
 &\le|\omega_q(A^*)-\omega_0(A^*)|\,|\omega_q(B)|\\
 &\quad+|\omega_0(A^*)|\,|\omega_q(B)-\omega_0(B)|\\
 &\le4d_q\|A\|\|B\|.
\end{split}
\]

Together with (8), this proves precisely

\[
 \boxed{|C_q(t)-C_0(t)|\le\|A\|\|B\|
 [6d_q+2\alpha\tau_q|t|D_{F_B}(q)/\hbar].}
 \tag{9}
\]

The coefficient six is sufficient; no optimality is claimed. The argument
already holds in the full representation and therefore for the admitted
bounded gauge-invariant local algebra. It imports no gap from a different
profile. The inherited canonical physical sector and its gbar remain intact.

## 6. Only now determine the growing-window scope

Set `epsilon=1-q`. Direct rational simplification gives

\[
 \frac{\tau_q}{\epsilon^3}
 =\frac{3\eta(1+q)^2(1+q^2)}{p(q)}\longrightarrow\frac{8\eta}7,
\]
\[
 \frac{\sigma_q^2}{\alpha^2\eta^2\epsilon^3}
 =\frac{p(q^2)(1+q)}{256p(q)^2(1+q^4)}
 \longrightarrow\frac1{5376}.
\]

In particular the normalized upper bound `sigma_q/gbar` has leading constant
`eta/((1-eta)sqrt(84))` times `epsilon^(3/2)`. This is not an asymptotic
equality claim for the actual distance d_q. Because the incident set is finite,
`D_FB(q)->D_FB(1)=m/24`. Substitution of the physical time window into (9)
gives the sufficient certificate

\[
 K_q=6\sigma_q/\bar g+2C\tau_q\epsilon^{-\gamma}D_{F_B}(q),
\]
\[
 K_q=\left[\frac{6\eta}{(1-\eta)\sqrt{84}}+o(1)\right]\epsilon^{3/2}
 +\left[\frac{16C\eta}7D_{F_B}(1)+o(1)\right]\epsilon^{3-\gamma}.
 \tag{10}
\]

Thus `sup_|t|<=Tq |C_q-C0| -> 0` for `0<=gamma<3`, with sufficient rate
`O(epsilon^min(3/2,3-gamma))`. The old `gamma=3/2` endpoint is included by
this newly proved estimate. More generally `T_q epsilon^3 ->0` suffices in
the fixed physical units.

Explicit finite-q constants also follow without sampling: `p(q)>=2`,
`p(q^2)<=p(q)`, `(1+q)/(1+q^4)<=2` and the exact identities give
`tau_q<=12 eta epsilon^3` and
`sigma_q/gbar<=eta epsilon^(3/2)/(2(1-eta))`. Hence for every allowed q,

\[
 K_q\le\frac{3\eta}{1-\eta}\epsilon^{3/2}
       +C\eta m\epsilon^{3-\gamma}.
\]

At `gamma=3` and `m>0`, K_q tends to the positive number
`16 C eta D_FB(1)/7=2 C eta m/21`; for the origin-xz cover, `C=1,eta=1/2`,
this is `4/3`. For `gamma>3` this particular uncapped certificate diverges.
Neither fact supplies a lower bound on the actual correlation error. If the
incident set is empty, the dynamical term vanishes for all times. Scalar
observables have identically zero connected correlations; choosing a larger
cover for them can only weaken a sufficient bound. These exceptions rule out
an interpretation of gamma=3 as a universal physical obstruction.

The profile is defined for `0<q,eta<1`; q=1 is a limit, not an admissible
substitution into its budget formula. Eta must remain fixed away from its
excluded endpoints in this theorem. No homogeneous nonzero omitted coupling,
operator-norm propagator convergence, real-time decay, continuum matching or
four-dimensional Yang-Mills mass-gap conclusion follows.

## 7. Counterexamples and executable boundary

`check.py` uses standard-library rational and Gaussian-rational arithmetic.
Its independently constructed finite spectral fixture evaluates the oriented
Duhamel integral exactly at positive and negative multiples of pi/2. It uses
noncommuting two-level Hamiltonians and independent spectral projections;
wrong sign and reversed endpoint controls fail. Scalar energy shifts preserve
Heisenberg evolution, while omission from the single propagator fails on
identity observables. Complex scalar additions, a missing adjoint, and holding
either mean fixed are separately checked.

A support control reconstructs the octant graph with unordered vertex-pair
edges and compares two face-incidence enumerations. A two-qubit within-factor
swap exposes migration beyond displayed support. These finite fixtures
discriminate mistakes; equations (2)-(9) provide the infinite-dimensional proof.

For the domain control take `H0 e_n=E_star n^2 e_n` on `ell^2(N_0)` and
`v=sum_(n>=1) e_n/n`. The rank-one bounded B=`|v><e_0|` satisfies
`||v||^2<=2`, but B e0 is outside even the form domain: its energy-form sum
is `E_star sum_(n>=1)1=+infinity`. Thus arbitrary bounded B need not preserve
the generator domain. For a distinct norm-continuity control, the shift
`S e_n=e_(n+1)` has
`||beta_0(t_n)(S)-S||=2` at `t_n=pi hbar/(E_star(2n+1))->0` by evaluating
on e_n. Strong continuity does not give point-norm continuity on all B(H).
The checker verifies finite exact partial sums and phase identities; these
series arguments establish the infinite claims.

Finally, abstract phase families with frequencies `epsilon^4` and `epsilon^3`
both obey an `O(epsilon^3)` upper estimate, but their phases at time
`epsilon^-3` respectively vanish and persist. This rejects inferring actual
endpoint behavior from that order bound alone. They are logical controls,
not simulated lattice correlations or evidence of actual endpoint failure.

Run ordinary and optimized Python into distinct new directories:

```
python3 -B research/round22/reverse/n1/check.py --output FRESH_DIRECTORY
python3 -O -B research/round22/reverse/n1/check.py --output OTHER_FRESH_DIRECTORY
```

The checker rejects an existing output directory and invalid scale/profile
inputs, uses explicit exceptions (no optimization-sensitive assertions), and
hashes every declared input plus both scientific outputs. The source manifest
does not hash itself; its own hash is recorded by the frozen submission.

## 8. Closest checked sources and next missing premise

The targeted primary comparison is Nachtergaele and Sims, *On the dynamics of
lattice systems with unbounded on-site terms in the Hamiltonian* (2014),
section 2, equations (6)-(12), Proposition 2.1 and Lemma 2.2. These passages
handle strong products, operator integrals and bounded evolution; the present
cocycle proof instantiates that established framework with the canonical local
commutator budget. Section 2 was read through the lemma's proof; the broader
Lieb-Robinson and thermodynamic-limit results are not used as imported premises.
[Primary source](https://arxiv.org/html/1410.8174v1#S2).

Teschl, *Mathematical Methods in Quantum Mechanics*, Theorem 5.1 (printed
pp. 123-124) and Theorem 6.4 (printed p. 135), were checked for unitary
domain preservation and self-adjoint bounded perturbations. These standard
operator facts support the domain step, not a physical matching claim.
[Author-hosted text](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf).

The missing premise for the actual gamma=3 endpoint is information about the
true long-time local dynamics beyond this first commutator upper estimate.
The advisor must select N2 only after the independent N1 submissions and
skeptical review; this report neither selects nor executes it.
