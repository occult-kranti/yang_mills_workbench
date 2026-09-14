# R2 forward: boundary-complete vacuum response with explicit collar tails

The initial diagonal defines a closed infinite-volume form in the fixed
product-reference representation. Its specified Neumann series converges
to the full vacuum response, with explicit Hilbert, energy and response
operator-graph tails and finite-volume errors. Two promotions fail: the
vacuum rank-two source is not the local source extended by identity, and
the stated positive volume-weight upper certificate diverges at every fixed
nonzero coupling. Neither fact proves divergence of the actual coefficients
or failure of every subsequent stability method.

This is the independent forward final loop, before current reverse/skeptic
solution exchange. No additional research loop is executed or selected.

## Infinite initial form, its operator and bounded inverse

Keep the actual I1/O1/R1 positive-octant complete 24-link factors and their
strip/free onsite h_x. Let Z_b=b+{0,e_x,e_y,e_z},
D_b=Q_b phi_b Q_b, phi_b=-(tau/3)sum_(21 actual omitted faces)W_f, and
M=7|tau|. Every term retains its full declared star. Set

\[
\kappa=28|\tau|,\qquad g=1-\kappa,
\qquad \kappa\le35/416<1,\quad g\ge381/416.                    \tag{1}
\]

On the product-reference incomplete tensor product H_Omega, define
h0[psi]=sum_x ||h_x^(1/2)psi||² with domain F where this sum is finite.
It is densely defined: finite-factor vectors in the onsite form domains
are dense. It is closed: a Cauchy sequence in its form norm converges in
the Hilbert space and in the direct sum of the h_x^(1/2) graph components;
closedness of each h_x^(1/2) identifies the limits. Its nonnegative
self-adjoint operator is H0. A subspace with vacuum outside finite F0
reduces H0, with restriction sum_(x in F0)h_x. In this representation
the finite products of onsite vacuum projections decrease strongly to
P=|Omega><Omega|. Therefore H0>=Q=I-P, since h_x>=I-P_x.

For psi,chi in F the series d(psi,chi)=sum_b <psi,D_b chi> is absolutely
convergent. Indeed Cauchy–Schwarz and at most four stars per site give

\[
\sum_b|\langle\psi,D_b\chi\rangle|
 \le M\Big(\sum_b\|Q_b\psi\|^2\Big)^{1/2}
        \Big(\sum_b\|Q_b\chi\|^2\Big)^{1/2}
 \le\kappa\,h0[\psi]^{1/2}h0[\chi]^{1/2}.                    \tag{2}
\]

This constructs the initial homogeneous interaction as a form, not a
bounded global sum. The form h0+d is closed by equivalence of its form
norm with that of h0, or KLMN at relative bound kappa<1. Let G be its
associated self-adjoint operator. Then

\[
D(G^{1/2})=F,\quad gH0\le G\le(1+\kappa)H0\quad\hbox{as forms},
\quad G\Omega=0,\quad G|_Q\ge g,\quad\|(G|_Q)^{-1}\|\le1/g.  \tag{3}
\]

The product vacuum is the unique ground of this initial G. It is not
identified with a ground of the original Hamiltonian including the O1
remainder. No global equality D(G)=D(H0) is inferred. The operator domain
is the representation-theorem domain: those psi in F for which
(h0+d)(chi,psi)=<chi,f> for all chi in F and some Hilbert vector f; Gpsi=f.

All inverse powers below are on Q, extended by zero on P. The form
d(H0^(-1/2)psi,H0^(-1/2)chi) defines a bounded self-adjoint K on Q with
||K||<=kappa by (2). Given v=v_Y tensor Omega_ext with v_Y=Q_Y R_Y Omega_Y,
r=||v_Y||, set w=(I+K)^(-1)H0^(-1/2)v and u=H0^(-1/2)w. Testing the
form against chi gives
(h0+d)(chi,u)=<H0^(1/2)chi,(I+K)w>=<chi,v>.
Thus u is in D(G), Gu=v, and

\[
u=(G|_Q)^{-1}v
 =\sum_{n=0}^{\infty}u_n,\qquad
u_n=H0^{-1/2}(-K)^nH0^{-1/2}v.                                \tag{4}
\]

The sign and both inverse factors follow from this form equation; they
are not imported from an isolated resolvent formula.

## Coefficient support, energy and response graph

Write F_n=Y^(n), the prescribed nonnegative l-infinity collar, and
p_N=sum_(n=0)^N u_n. A vector supported on a finite F0 means a vector
in H_(F0) tensor Omega_(F0^c), not a bounded operator supported on F0.
H0 inverse powers preserve this subspace. For such a vector psi, every
D_b with Z_b disjoint from F0 annihilates psi. The remaining at most
4|F0| terms define an actual Hilbert vector Dpsi, with

\[
\|D\psi\|\le\kappa|F0|\|\psi\|,
\qquad \operatorname{supp}(D\psi)\subset F0^{(1)}.             \tag{5}
\]

This includes incoming and outgoing stars. Each star meeting F0 is
contained in its unit l-infinity collar. The form definition agrees with
this finite sum when psi is also in F. It follows by induction that

\[
\operatorname{supp}(u_n)\subset F_n,\qquad
u_0=H0^{-1}v,\quad u_{n+1}=-H0^{-1}D u_n,\quad
H0u_{n+1}=-D u_n.                                            \tag{6}
\]

Each u_n is in D(H0): the first assertion follows from the bounded
reduced inverse; each subsequent right-hand side is a Hilbert vector
by (5). Finite-support domain vectors are also in D(G), with Gpsi=H0psi+Dpsi,
by the representation-theorem test. No domain-preservation assumption on
Wilson multiplication is needed in this induction.

The bounded K formula and ||H0^(-1/2)||<=1 yield

\[
\|u_n\|,\ \|H0^{1/2}u_n\|\le r\kappa^n,\qquad
\|H0u_0\|=r,\quad
\|H0u_n\|\le r|F_{n-1}|\kappa^n\quad(n\ge1).                \tag{7}
\]

The coarse cardinality bound |F_n|<=|Y|(2n+1)^3 holds for any finite Y.
For the origin singleton the exact cardinality is (n+1)^3. In particular,
the H0 graph series is absolutely convergent for kappa<1. Closedness of
H0 proves that this response u, already in D(G), is also in D(H0).

Here are explicit tail functions, including kappa=0. For a>=1, define

\[
J(a,k)=k^a\left[{a^3\over1-k}
 +{3a^2k\over(1-k)^2}+{3ak(1+k)\over(1-k)^3}
 +{k(1+4k+k^2)\over(1-k)^4}\right],                           \tag{8}
\]

which equals sum_(n=a)^infinity n^3 k^n. Put m=2N+1 and

\[
T_N(k)=k^{N+1}\left[{m^3\over1-k}
 +{6m^2k\over(1-k)^2}+{12mk(1+k)\over(1-k)^3}
 +{8k(1+4k+k^2)\over(1-k)^4}\right].                         \tag{9}
\]

This is sum_(n=N+1)^infinity (2n-1)^3 k^n. Both follow by expanding a
shifted cube and differentiating the geometric series up to three times
inside |k|<1. Set c_N=|Y|T_N(kappa), or the sharper
c_N=J(N+1,kappa) for the origin singleton. Then, for every N>=0,

\[
\|u-p_N\|,\ \|H0^{1/2}(u-p_N)\|
 \le {r\kappa^{N+1}\over g},\qquad
\|H0(u-p_N)\|\le r c_N.                                    \tag{10}
\]

The H0 graph norm is bounded by the sum of the Hilbert and H0 bounds.
The spatial projection Pi_N onto vacuum outside F_N commutes with H0.
Replacing u-p_N by (I-Pi_N)u in each of these three inequalities is valid.
Thus these are actual spatial response tails as well as series remainders.

There is also a sharper response G-graph residual. Telescoping (6) gives

\[
Gp_N=v+D u_N,\qquad
\|G(u-p_N)\|\le r|F_N|\kappa^{N+1}.                          \tag{11}
\]

All constants depend on the fixed source size and the explicitly shown
coupling, rather than a containing volume. In particular no unnamed
asymptotic remainder is needed. The arguments also hold for initial D at
|tau|<1/28, without enlarging an O1/full-Hamiltonian stability interval.

## Finite volumes and their boundary errors

In a finite complete-star cuboid Lambda, R1 gives G_Lambda with operator
domain D(H0_Lambda), complementary gap g, and its corresponding K_Lambda
and coefficients u_(n,Lambda). Embedded by the exterior vacuum, they obey
all bounds (5)–(11), with D_Lambda and the same majorants. If F_N is
contained in Lambda, every star that can act through order N is retained,
so u_(n,Lambda)=u_n for 0<=n<=N. Hence

\[
\|u-u_\Lambda\|,\ \|H0^{1/2}(u-u_\Lambda)\|
 \le {2r\kappa^{N+1}\over g},\qquad
\|H0(u-u_\Lambda)\|\le2r c_N.                               \tag{12}
\]

Each embedded u_Lambda is finite-factor supported and in D(H0), hence
in D(G) as well. Its global equation has the additional crossing stars,
(G u_Lambda-v)=(D-D_Lambda)u_Lambda. This difference annihilates each
coefficient n<N, while its action on u_(n,Lambda) is bounded by
r|F_n|kappa^(n+1). Absolute summation gives

\[
\|G(u-u_\Lambda)\|\le r c_N.                               \tag{13}
\]

Indeed sum_(n=N)^infinity |F_n|kappa^(n+1) is bounded by c_N with the
same general or origin choice. These statements are response-specific
operator-graph convergence along any cuboid exhaustion containing each
fixed collar. They do not identify global operator domains for arbitrary
vectors or assert uniform operator-norm convergence of full inverses.

## The actual source sector and the boundary/sign controls

For finite Lambda define S_vac=|u_Lambda><Omega_Lambda|-adjoint. Since
u_Lambda,Omega_Lambda are in D(G_Lambda), direct multiplication proves

\[
[S_{vac},G_\Lambda]=-A_{vac},\qquad
A_{vac}=|v_\Lambda\rangle\langle\Omega_\Lambda|+adjoint
       =A_Y\otimes P_{ext}.                                 \tag{14}
\]

The same construction works in H_Omega with the response u. Its bounded
rank-two range lies in both D(G) and D(H0). Exponentials preserve both
domains; for G's graph norm the generator norm is at most r/g+r.
This is a global rank-two operator statement, not local-operator locality.

The exact remaining bounded operator for R1's identity-extended target is

\[
[S_{vac},G_\Lambda]+A_Y\otimes I
       =A_Y\otimes(I-P_{ext}).                               \tag{15}
\]

Its norm is r when the exterior has an excited sector (zero if r=0 or the
exterior is absent). For the frozen actual probe, Y={0},
v=Tr(g_e)Omega, with free z-link e at physical tail(0,0,0), R1 gives r=1
and H0v=6v. Take the second free z-link e' with tail(4,0,0), owned by
coarse e_x. The normalized actual vector eta=Tr(g_e')Omega has vacuum in Y
and is orthogonal to the exterior vacuum. Character orthogonality on these
two independent free Haar factors proves

\[
A_{vac}\eta=0,\quad (A_Y\otimes I)\eta
   =Tr(g_e)Tr(g_{e'})\Omega,\quad
\|([S_{vac},G]+A_Y\otimes I)\eta\|=1.                       \tag{16}
\]

The strip ground remains unchanged. These are exact actual-Hilbert-space
calculations, valid at tau=0 and either coupling sign, without a Gauss-sector
restriction or a finite-spin replacement.

The bare truncation u0=v/6 does not solve the full response at nonzero tau.
Only the origin star acts on it, and the admitted actual Haar calculation
with all 21 omitted faces gives

\[
\|Gu_0-v\|^2=\|D u_0\|^2=7\tau^2/432.                      \tag{17}
\]

It also proves u1=-H0^(-1)D u0 is nonzero by injectivity on Q. A wrong-sign
first correction p1_wrong=u0+H0^(-1)D u0 has residual
2D u0+D H0^(-1)D u0. The intermediate vector has support in the origin
star. Exactly four positive anchors meet that star, so the latter D action
has norm at most 4M=kappa on this support. Consequently

\[
\|Gp1_{wrong}-v\|^2\ge(2-\kappa)^2\,7\tau^2/432>0           \tag{18}
\]

for nonzero frozen tau. No strip spectral truncation is used. These
diagnostics are not asserted to be generated O1 residuals.

## The specified positive volume-weight certificate

The proved geometric majorant is b_n=r kappa^n. For origin Y={0}, keep
the declared full collars, so the proposed certificate is

\[
\sum_{n\ge0}\exp\{\mu(n+1)^3\}\,r\kappa^n.                  \tag{19}
\]

For r>0, fixed nonzero tau and every mu>0, its summands tend to infinity:
their logarithms are mu(n+1)^3+n log(kappa)+log(r). Equivalently the ratio
is kappa exp(mu(3n^2+9n+7)), eventually larger than any fixed number.
This upper certificate diverges. At tau=0 only u0 remains and the sum is
exp(mu)r; at r=0 it is zero. Replacing (n+1)^3 by n+1 would instead give
a geometric radius condition, but changes the declared support weight.

One may associate each vector coefficient with a rank-two operator on F_n
of norm ||u_n||, extended by identity outside F_n. Those operators agree
with the global coefficients on the vacuum only: the actual global
rank-two coefficients contain exterior vacuum projections. Equations
(15)–(16) prevent equating these two families on the full Hilbert space.
Thus vector locality alone does not construct the local operator interaction
that O2's fixed positive volume weight requires, and (19) does not certify
even the chosen local-coefficient upper budget. Neither observation proves
divergence of sum exp(mu|F_n|)||u_n||, excludes finer connected-support
regrouping, or establishes an all-stage impossibility theorem.

## Evidence, units and final scope

The checker imports only its explicitly hash-verified own frozen R1 helper
for actual face/free-link Haar arithmetic. New independent calculations
check collars and all meeting anchors, the exact geometric/polynomial tail
identities, noncommuting Neumann algebra, and the actual two-character
source-sector control. The finite matrix used for inverse bookkeeping is
labelled as an algebra fixture; it supplies no physical spectral premise.
All controls use explicit exceptions and run unchanged with assertions
disabled. Finite checks do not replace the infinite form and domain proofs.

Source reading is recorded in source-notes.md. Closed-form representation,
KLMN, spectral calculus and Neumann inversion are established methods. The
actual-model locality, evaluated tails and scoped obstructions here are
instantiated derivations; scientific priority is unverified.

The energy unit is delta=alpha/8; h,D,G,v and inverse equations are
dimensionless, S is dimensionless, and physical evolution uses delta*t/hbar.
The fixed positive a,E_star,alpha/E_star,hbar are unchanged. The construction
stays in H_Omega for the initial retained diagonal. It imports no Q2
complementary gap or positivity, proves no subsequent diagonal induction or
gap for H0+D+R, and gives no interacting-ground representation or continuum
Yang–Mills result. This completes only the assigned tenth loop.

```bash
python3 -B research/round22/forward/r2/check.py --output /absolute/new/r2-forward
python3 -B -O research/round22/forward/r2/check.py --output /absolute/new/r2-forward-O
```
