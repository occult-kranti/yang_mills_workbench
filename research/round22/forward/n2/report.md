# N2 forward: exact tail-cube budget and joint support/time certificate

The incident-face budget is exactly

\[
\boxed{D_L(q)=\mathcal B(q)(1-q^{4L})(1-q^{2L})(1-q^L).}
\tag{1}
\]

Here the model and profile-generating function are precisely N1's, and
`L>=1` is an integer. The result gives a vanishing uniform certificate for
`0<=beta<1` and `0<=gamma<3(1-beta)`. At beta=0 its constants use the actual
fixed integer L, not ell. At beta>=1 the certificate fails to vanish even
for a fixed positive time window. These last statements concern this upper
certificate alone; actual correlation nonconvergence is not proved.

This is the independently derived forward N2 submission. No current reverse
N2 or skeptical N2 findings were read. The accepted N1 report/review and I1
ownership dictionary are inherited inputs, not new research loops.

## Model, variables, and inherited operator input

Use the canonical summable full-link SU(2) selected-strip/free incomplete
tensor product on the nonnegative cubic orthant. The Hamiltonian H_q, its
ground, and all coefficients are unchanged from N1. In particular

\[
\mathcal B(q)=\frac{2+5q+5q^2+6q^3+3q^4}
 {24(1-q)^3(1+q)^2(1+q^2)},\quad
\tau_q=\frac{\eta}{8\mathcal B(q)},\quad
\bar g=\alpha(1-\eta)/8,
\quad \sigma_q^2=\alpha^2\tau_q^2\mathcal B(q^2)/96.
\]

Keep E_star>0, alpha/E_star>0, hbar>0, eta in (0,1), and lattice spacing
a>0 fixed. q in (0,1) and eta/tau are dimensionless profile coefficients.
Alpha, sigma_q and gbar are energies. The integers L and dimensionless
ell>0,beta>=0 specify an observed support, not an action change or a
regulator limit. The cube's physical side lengths are `4aL,2aL,aL`.

For every q, A_q and B_q are bounded complex gauge-invariant operators on
finite complete reference-factor supports, with B_q supported in F_L(q).
Assume `K=sup_q ||A_q||||B_q||<infinity`. A_q's support need not obey the
same size bound. No smoothness in q or generator-domain preservation of the
operators is needed. Both the perturbed and reference correlation use the
same A_q,B_q at a given q; the reference observable is not held fixed while
changing the perturbed one.

N1 proves the strong commutator integral for every bounded local B, uniformly
over all real reference times, and the rank-one state comparison for every
bounded complex operator. Applied separately at each q, that theorem gives

\[
\sup_{|t|\le T_q}|C_q^{A_q,B_q}(t)-C_0^{A_q,B_q}(t)|
\le K\left[6\frac{\sigma_q}{\bar g}
  +\frac{2\alpha T_q\tau_q}{\hbar}D_{L(q)}(q)\right].
\tag{2}
\]

No step in N1's strong integral demands one common finite support for all
q; the finite support is fixed only within its time integral at each q.
Trace duality is uniform on the whole bounded operator unit ball, so moving
A_q and B_q create no additional state-distance term. Conjugation retains
complete reference factors for all real times. Stationarity and both complex
mean factors are the same as N1. Hence (2) is a direct justified application
of the accepted operator theorem after calculating the new geometry.

## Ownership and the exact boundary characterization

For a block b=(i,j,k), the tail set consists of `(4i+r,2j+s,k)` with
`0<=r<4,0<=s<2`. Euclidean division gives each positive link a unique owner
from its tail. Each block owns 24 links, including links whose heads leave
the block. Ten links make its whole three-face reference strip: six x-links
at r=0,1,2 and s=0,1, and four y-links at r=0,1,2,3 and s=0. The other
fourteen are the two separator x-links, four odd-row y-links and eight
z-links, each a complete free factor. Thus a union of these blocks is a
union of complete reference factors; no selected strip is cut.

For `0<=i,j,k<L`, their tail rectangle is

\[
R_L=\{0,\ldots,4L-1\}\times\{0,\ldots,2L-1\}
       \times\{0,\ldots,L-1\},
\quad E_L=\{(p,c):p\in R_L,\ c=x,y,z\},
\quad |E_L|=24L^3.
\]

A face with anchor p and axes c<d has positive-link tails
`p,p,p+e_c,p+e_d`. If p is in R_L, its two links at p lie in E_L, so the
face meets E_L even when other links cross the top boundary. Conversely,
if any face link lies in E_L, one of those four tails is in R_L. The anchor
p is nonnegative and coordinatewise no greater than that tail. R_L is
downward closed within the orthant, so p lies in R_L. Therefore

\[
\boxed{\operatorname{links}(f)\cap E_L\ne\varnothing
       \quad\Longleftrightarrow\quad a_f\in R_L.}
\tag{3}
\]

This proves the complete incident set for every L, rather than extrapolating
an enumeration. It depends on the origin-anchored downward-closed geometry.
Translated rectangles generally have incoming faces anchored outside them.

## Closed weighted ledger

Let `S_n(q)=(1-q^n)/(1-q)`. The weighted sum of all faces anchored in R_L
is `3 S_(4L) S_(2L) S_L`. Selected faces are exactly xy faces at even y,
x residue 0,1,2 modulo 4. Their weighted sum is

\[
(1+q+q^2)\frac{1-q^{4L}}{1-q^4}
             \frac{1-q^{2L}}{1-q^2}
             \frac{1-q^L}{1-q}.
\]

Subtract selected faces and divide by 24. Factoring the three finite-sum
numerators gives

\[
D_L(q)=\frac{(1-q^{4L})(1-q^{2L})(1-q^L)}{24}
\left[\frac{3}{(1-q)^3}
 -\frac{1+q+q^2}{(1-q^4)(1-q^2)(1-q)}\right].
\tag{4}
\]

Putting the bracket over its common denominator yields exactly
`24 mathcal B(q)`, proving (1). The unweighted count is 24L^3 total faces
minus 3L^3 selected faces, hence 21L^3 incident omitted faces and
`D_L(1)=7L^3/8` as a polynomial endpoint value. This endpoint evaluation
does not insert q=1 into the nonsummable infinite Hamiltonian.

Write `P_L(q)=(1-q^(4L))(1-q^(2L))(1-q^L)`. The canonical normalization
then cancels exactly:

\[
\boxed{\tau_q D_L(q)=\frac\eta8 P_L(q),\qquad 0<P_L(q)<1.}
\tag{5}
\]

The infinite budget would instead set P_L to one. That replacement is a
valid but weaker upper bound, and erases the support-size information needed
for this certificate. It is not the exact finite answer.

## The certificate and all support-growth regimes

Set epsilon=1-q. For the time protocol
`T_q=(hbar/alpha) C epsilon^(-gamma)`, with C>0 and gamma>=0, define the
nonnegative envelope

\[
\mathcal E_q=6\sigma_q/\bar g
 +\frac{\eta C}{4}\epsilon^{-\gamma}P_{L(q)}(q).
\tag{6}
\]

Equation (2) is `error <= K mathcal E_q`. Since N1 gives

\[
6\sigma_q/\bar g
=\frac{6\eta}{(1-\eta)\sqrt{84}}\epsilon^{3/2}(1+o(1)),
\]

the envelope vanishes if and only if
`epsilon^(-gamma) P_L(q) ->0`, equivalently
`(alpha T_q/hbar) tau_q D_L(q)->0`. This is necessity for vanishing of the
specified envelope, not necessity for convergence of any actual observable
pair. A pair can have zero correlations even when this envelope stays
positive. The degenerate case K=0 is automatically trivial.

The support rule is `L(q)=max(1,floor(ell epsilon^(-beta)))`. For beta=0,
use the fixed integer `L_0=max(1,floor(ell))`. For beta>0, the floor differs
from ell epsilon^(-beta) by less than one, so their ratio tends to one.
Using `-log(1-epsilon)/epsilon ->1`, all three regimes follow:

| Support regime | Exact leading P_L(q) | Dynamic term in (6) | Vanishing-envelope range |
| --- | --- | --- | --- |
| beta=0 | `8 L_0^3 epsilon^3 (1+o(1))` | `2 eta C L_0^3 epsilon^(3-gamma) (1+o(1))` | `0<=gamma<3` |
| 0<beta<1 | `8 ell^3 epsilon^(3(1-beta)) (1+o(1))` | `2 eta C ell^3 epsilon^(3(1-beta)-gamma) (1+o(1))` | `0<=gamma<3(1-beta)` |
| beta=1 | `p(ell)+o(1)` | `(eta C/4) p(ell) epsilon^(-gamma) (1+o(1))` | none for gamma>=0 |
| beta>1 | `1+o(1)` | `(eta C/4) epsilon^(-gamma) (1+o(1))` | none for gamma>=0 |

Here

\[
p(\ell)=(1-e^{-4\ell})(1-e^{-2\ell})(1-e^{-\ell})\in(0,1).
\]

For beta<1, epsilon L tends to zero and each factor
`1-q^(rL) ~ r epsilon L`, r=4,2,1. This proves the first two rows. For
beta=1, epsilon L tends to ell and q^(rL) tends to exp(-r ell). For
beta>1, epsilon L diverges and every q^(rL) tends to zero, proving the
remaining rows. These arguments also explicitly account for floors.

In the vanishing region the sufficient rate is

\[
O\!\left(\epsilon^{\min\{3/2,\,3(1-\beta)-\gamma\}}\right).
\tag{7}
\]

For beta<1 and `gamma=3(1-beta)`, the uncapped envelope tends to the strictly
positive constant `2 eta C ell^3`, with ell replaced by L_0 when beta=0.
For gamma above that threshold it diverges. For beta=1,gamma=0 its limit
is `(eta C/4)p(ell)>0`; for beta>1,gamma=0 it is eta C/4. Positive gamma
makes the last two regimes diverge. The actual correlations remain bounded;
an upper-envelope divergence is not a statement that the physical error
diverges or even stays nonzero. No endpoint lower bound has been supplied.

## Fixed-L logarithmic check

For fixed integer L and k>0, choose the allowed observation protocol

\[
T_q=\frac\hbar\alpha
 \frac{C\epsilon^{-3}}{[\log(1/\epsilon)]^k}.
\]

The dynamic term becomes
`2 eta C L^3 [log(1/epsilon)]^(-k)(1+o(1))`, so the envelope tends to zero.
Its sufficient order is `O(epsilon^(3/2)+[log(1/epsilon)]^(-k))`.
The unshortened k=0 endpoint has envelope limit `2 eta C L^3>0`.
This is a substitution in the proved estimate, not a separate research loop.
The logarithm and k are dimensionless observation-design choices; no clock
or physical scale is fitted.

## Checks, source use, and limits

The independent standard-library checker implements incidence by link
neighbors and compares it with separately enumerated anchors. Three small
exact fixtures cover L=1,2,3 and rational q. It also verifies the selected
strip/free partition, counts, finite weighted sum, and rational factorization.
Rejecting controls remove outgoing links, discard crossing faces, replace
the finite budget by the infinite one, mishandle beta=0 floors, and infer
actual nonconvergence from a positive upper bound. An incoming-face fixture
rejects extending (3) to translated rectangles without qualification.
The all-L proof and real-parameter asymptotics above do not follow from these
finite fixtures. No statistical, truncation or numerical inference is used.

Closest checked prior work is N1's accepted strong-integral correlation bound
and I1's complete tail-ownership dictionary. The I1 Hamiltonian considered
homogeneous stability; only its exact geometry is used here. Its numerical
gap or representation is not transferred. N1's primary-source record checks
Teschl's operator foundations; the current N2 step requires only finite
geometric sums and elementary exponential limits, which are explicitly
derived above. No new specialized blocking theorem is invoked. This is an
explicit model-specific budget and observation-protocol derivation;
scientific priority remains unverified.

The immutable shared method snapshots, consulted N1/I1 gates and reports,
this report, executed code and all generated outputs are source-bound.
Normal and optimized runs use fresh separate directories and explicit
exceptions, without other-producer imports:

```bash
python3 -B research/round22/forward/n2/check.py --output /absolute/new/n2-forward
python3 -B -O research/round22/forward/n2/check.py --output /absolute/new/n2-forward-optimized
```

The missing premise for actual endpoint behavior remains a dynamical lower
bound or a sharper cancellation estimate in the true canonical ground.
There is no homogeneous interaction, continuum limit, global unit-ball
operator convergence, physical generator matching, or Yang–Mills mass-gap
completion. N2 changes the observation region and time window only.
