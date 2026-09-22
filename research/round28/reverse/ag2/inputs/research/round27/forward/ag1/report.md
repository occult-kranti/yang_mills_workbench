# AG1 forward: a complete one-step selected-source correction

Independent forward derivation under the frozen AG1 contract; no current reverse AG1 solution was read. This treats the actual selected S1 cubic source family A in the homogeneous complete-24-link model. It proves a full nonlinear update estimate on `0<=M<=1/1000`, and a contraction of its newly extracted local mixing family on the predeclared narrower interval `0<M<=1/10000`. It does not treat the selected source as the complete original remainder or prove a later-stage induction.

## Actual source and exact input denominator

In a finite coarse cuboid Lambda retain every complete star `Z_b=b+{0,e1,e2,e3}`. Keep `G=H0+sum_b D_b`, `D_b=Q_b phi_b Q_b`, `||D_b||<=M=7|tau|`. S1 defines the actual vector

\[
 v_b=\phi_b\Omega_b,\quad u_b=H_{0,Z_b,Q}^{-1}v_b,
 \quad a_b=\langle u_b,v_b\rangle,\quad
 w_b=-a_bu_b-\|u_b\|^2v_b/3,
 \quad A_b=|w_b\rangle\langle\Omega_b|+\mathrm{adjoint}.
 \tag{AG1-F1}
\]

S1 proves `r=||A_b||=||w_b||>0` for tau nonzero and

\[
 r\le\frac43(7/12)^{3/2}|\tau|^3
 \le\frac{M^3}{567}=:r_{\rm bd}(M).
 \tag{AG1-F2}
\]

The rational upper bound uses `sqrt(7/12)<=7/9` and `tau=M/7` in magnitude. It is not equality. Every retained b uses the same translated homogeneous block/star construction; translation identifies its local operator and vacuum unitarily, so every r is the same for fixed tau. Boundary deletion removes stars, not links inside retained stars.

For a>1 define the **chosen indexed interaction norm**

\[
 \|\Phi\|_a=\sup_x\sum_{i:X_i\ni x}a^{|X_i|}\|\Phi_i\|.
\]

Repeated terms on the same declared support retain their indices unless explicitly grouped. Let `m_Lambda=max_x #{b:x in Z_b}`, which lies between one and four for a nonempty retained family. Then the actual input norms are exactly

\[
 A_a:=\|\{A_b\}\|_a=m_\Lambda a^4r,
 \qquad A_\rho/A_2=(\rho/2)^4,\quad\rho=9/4.
 \tag{AG1-F3}
\]

This is an evaluated multiplicity times the unevaluated **actual** norm r, rather than the cubic upper budget used as a false denominator. It also covers small boundary cuboids with `m_Lambda<4`. Empty families and tau zero have zero update and no ratio. Physical energies throughout multiply normalized quantities by `delta=alpha/8`; a, hbar, E_star and alpha/E_star remain fixed and positive.

## Reconstruct the filter at the auxiliary weight

At T=3 use the AE2 kernels

\[
 p_T(t)=(1-|t|/T)_+/T,\quad
 h_T(t)=\tfrac12\operatorname{sgn}(t)(1-|t|/T)_+^2,
\]
\[
 R_b=\int p_T(t)\alpha_t^G(A_b)dt,\quad
 J_b=-i\int h_T(t)\alpha_t^G(A_b)dt.
 \tag{AG1-F4}
\]

Their exact integrals are `int p=1`, `int |h|=T/3=1`, `int |p'|=2/T`, and `h'=delta_0-p`. Weak pairing with domain vectors and integration by parts give `[J_b,G]=-A_b+R_b`. This bounded commutator proves `J_b D(G) subset D(G)` by the self-adjoint adjoint-domain characterization, without assuming A_b preserves the domain. In each finite volume S=sum J_b is bounded skew-adjoint and bounded on the G graph norm, and `exp(±S)` preserves D(G). This is a finite-volume statement; no bounded infinite extensive S is claimed.

The source-specific boundary identity retains all twelve interior crossing stars, not the origin's three. The difference set of the four-site star has thirteen anchors including zero; each crossing adds a connected seven-site union. The actual interior inverse gives the unchanged per-source certificate

\[
 \|R_b\|/r\le\frac{24M+2/T}{1-M}
 \le2072/2997<7/10\quad(M\le1/1000).
 \tag{AG1-F5}
\]

This is not yet an interaction-norm contraction. To obtain the latter kind of norm, remove the unbounded onsite evolution by the bounded interaction picture. A depth-n word contains a source star and n ordered interaction stars; repetitions remain, and its connected union has at most `4+3n` sites. Define N_n(a) as the rooted a-weighted norm sum before time-simplex integration. Its exact initial value is A_a. Adding an interaction costs `2M a^3`. If the root is in the old union, at most `4(4+3n)` stars meet it; if the root is in the new star, at most four root stars and four overlap sites each contribute an old rooted sum. Thus

\[
 N_{n+1}(a)\le8Ma^3(8+3n)N_n(a),\qquad
 N_n(a)\le A_a(24Ma^3)^n(8/3)_n.
 \tag{AG1-F6}
\]

The incoming-root case, every ordered repeated word and all complete factor supports are included. Finite boundaries delete terms. The all-order recurrence supplies the proof; finite word counts in the checker are diagnostics of it.

With `c_a=24a^3 M`, `x_a=c_a T`, integration of the time simplex gives

\[
 \|R\|_a\le A_a\sum_{n\ge0}\frac{2(8/3)_n x_a^n}{(n+2)!},
\quad
 \|S\|_a\le A_a\sum_{n\ge0}\frac{2T(8/3)_n x_a^n}{(n+3)!}.
 \tag{AG1-F7}
\]

At T=3 both are bounded by `A_a F_a`, where `F_a=(1-x_a)^-3`, provided x_a<1. Indeed the whole orbital series is `(1-c_a|t|)^(-8/3)`, bounded by F_a, and both absolute kernel masses are one. At the main endpoint,

\[
 x_\rho=6561/8000<1,\quad
 F_\rho\le(8000/1439)^3.
 \tag{AG1-F8}
\]

This proves summability continuously throughout the declared interval. The factor rho is dimensionless proof bookkeeping, not a physical deformation.

## Entire nonlinear update with paid weight loss

For two interactions with nonempty overlap and output weight b>=2,
`b^{|X union Y|} <= b^-1 b^{|X|}b^{|Y|}`. Split the root between X and Y, then sum overlapping supports through each site. If a>b and d=log(a/b),

\[
 \|[\Phi,\Psi]\|_b
 \le\frac{4}{b}\sup_{m\ge1}m e^{-dm}\,
          \|\Phi\|_a\|\Psi\|_a
 \le\frac{2}{ed}\|\Phi\|_a\|\Psi\|_a.
 \tag{AG1-F9}
\]

Divide the loss `d0=log(rho/2)=log(9/8)` equally over n nested commutators. Every intermediate output weight stays at least two. Using `n! >= (n/e)^n` gives

\[
 \frac{\|\mathrm{ad}_S^n X\|_2}{n!}
 \le\left(\frac{2\|S\|_\rho}{d_0}\right)^n\|X\|_\rho
 \le\vartheta^n\|X\|_\rho,
 \quad\vartheta=18 A_\rho F_\rho.
 \tag{AG1-F10}
\]

Here `log(9/8)>=1/9` follows by integrating `1/(1+x)` from 0 to 1/8. For a volume-independent rational certificate replace vartheta by

\[
 \vartheta_{\rm bd}(M)=72\rho^4 F_\rho(M)r_{\rm bd}(M)<1.
 \tag{AG1-F11}
\]

Monotonicity in M and its exact endpoint evaluation establish this on the full interval. No fixed-weight commutator bound is silently assumed. A diagnostic family proves why loss matters: on n sites let S_X=`2^-n X^{tensor n}` and Phi have singleton terms `Z_i/2`. Both weight-2 norms equal one, while the single-support commutator has weight-2 norm n, since `||sum_i Z_i||=n` and the X string is unitary. Hence no support-independent fixed-weight bilinear constant exists for that class.

Let A=sum A_b and R=sum R_b. From `[S,G]=-A+R`, first integrate the bounded commutator to conjugate unbounded G on D(G), and conjugate bounded A separately. The exact identity is

\[
 e^S(G+A)e^{-S}=G+R+N,
\quad N=\sum_{n\ge1}\frac{\mathrm{ad}_S^n(nA+R)}{(n+1)!}.
 \tag{AG1-F12}
\]

Equivalently `N=int_0^1 exp(s ad_S){s[S,A]+(1-s)[S,R]} ds`. The first nonlinear term is `[S,A+R]/2`; a G-only BCH remainder would have the wrong A coefficient. All series beyond G's first bounded commutator involve bounded interactions, and (AG1-F10) proves absolute convergence of their whole indexed decomposition. Consequently

\[
 \|N\|_2\le\frac{\vartheta_{\rm bd}}{1-\vartheta_{\rm bd}}
                   A_\rho(1+F_\rho/2),
\quad
 \frac{\|N\|_2}{A_2}\le\nu(M):=
 \frac{\vartheta_{\rm bd}}{1-\vartheta_{\rm bd}}
 (9/8)^4(1+F_\rho/2).
 \tag{AG1-F13}
\]

This is a volume-independent bound on the **entire** nonlinear N. The actual denominator (AG1-F3) makes the ratio legitimate for r>0. It proves one bounded update in the main interval, without claiming that the loose main residual majorant contracts.

At the main endpoint the rational certificates give `vartheta_bd<5.5920e-7`, `||N||_2/A_2<7.7851e-5`, and `||N||_2<8.7874e-15`. These figures bound normalized interactions, not a physical spectral gap. At the narrower endpoint, `nu<1.1095e-11`; the full selected-source mixing ratio below is less than `0.639242`. Decimal values are rounded displays of exact rational bounds.

If the full transformed Hamiltonian contains an additional actual remainder E, retain

\[
 e^S(G+A+E)e^{-S}=G+R+N+e^SEe^{-S},
\quad \|e^SEe^{-S}\|_2\le e_*/(1-\vartheta_{\rm bd})
 \tag{AG1-F14}
\]

conditionally on the genuine bound `||E||_rho<=e_*`. This does not provide that bound or replace E by a fitted physical term.

## Predeclared narrower refinement: free source plus positive interaction tail

At `0<M<=1/10000`, split each filtered source's Dyson expansion into n=0 and n>=1. The n=0 operator is supported on the original star and is exactly

\[
 R_b^{(0)}=|f_T(H_{0,Z_b})w_b\rangle\langle\Omega_b|+
 \mathrm{adjoint},\quad f_T(E)=\operatorname{sinc}^2(TE/2).
 \tag{AG1-F15}
\]

The actual local source is orthogonal to the reference vacuum, and S1's local H0 has spectral gap at least one. Thus `|f_3(E)|<=4/(9E^2)<=4/9` on its source spectral support. This gives `||{R_b^(0)}||_2 <=(4/9)A_2`. It is a source-specific rank-to-vacuum spectral estimate, not a generic multiplier bound on every excited-sector operator.

The positive n>=1 interaction terms in (AG1-F6) cost at most `A_2(F_2-1)`, where `F_2=(1-576M)^-3`; both exact kernel mass and support labels remain. Therefore

\[
 \|R\|_2/A_2\le\kappa(M)=4/9+(1-576M)^{-3}-1,
\]
\[
 \|R+N\|_2/A_2\le\kappa(M)+\nu(M)<2/3
 \quad(0<M\le1/10000).
 \tag{AG1-F16}
\]

The inequality is checked as an exact rational endpoint bound; all ingredients are increasing functions of M on this interval. It is a **contraction for the declared actual input decomposition**, not comparison of two unrelated upper budgets. It consumes the rho-to-two weight margin and changes the diagonal in the next paragraph, so it cannot be repeated as an unchanged induction.

## Scalar, diagonal and new source remain explicit

For every generated self-adjoint indexed term K_X of `K=R+N` on its connected complete support, let `P_X=|Omega_X><Omega_X|`, `Q_X=1-P_X`, and define

\[
 c_X=\langle\Omega_X,K_X\Omega_X\rangle,\quad
 B_X=P_XK_XQ_X+Q_XK_XP_X,\quad
 D'_X=Q_X(K_X-c_X I)Q_X.
\]
\[
 K_X=c_X I+B_X+D'_X,\quad
 |c_X|\le\|K_X\|,\quad\|B_X\|\le\|K_X\|,
 \quad\|D'_X\|\le2\|K_X\|.
 \tag{AG1-F17}
\]

The mixing bound follows because its norm is `||Q_X K_X Omega_X||`; the diagonal bound uses subtraction of c_X. Retaining all three families costs at most four times the K budget in total. Each scalar keeps its indexed support for a density budget; the finite-volume sum of scalar energies can be extensive. These reference-vacuum expectations are not exact interacting ground energies. The new source B alone obeys (AG1-F16); the new diagonal and scalar cannot be discarded to claim complete Hamiltonian contraction. Any transported E must likewise remain in a separate full split or uncombined conditional term.

## Controls, reproduction and final scope

The checker reconstructs origin/interior/no-crossing geometry, exact kernel moments, finite connected words with repetitions and incoming roots, both signs and tau zero, continuous-interval rational constants, contraction against the actual denominator, all-order tail convergence, fixed-weight failure, scalar bookkeeping and conditional E transport. A separately implemented finite rational matrix polynomial diagnostic checks the whole `e^(tS)(G+tA)e^(-tS)` identity through degree eight, rejects the omitted residual and the G-only BCH coefficient, and checks every term's scalar/source/diagonal reconstruction. This finite algebra fixture is not the physical Hilbert-space proof.

Run `python3 -B research/round27/forward/ag1/check.py --output /absolute/new/output`. Explicit exceptions remain active under Python -O, and output binds all inputs, code and report. No sampled finite graph establishes the volume-uniform estimate: the full recurrence, weight-loss series and domain proofs do.

The main interval has a complete one-step nonlinear bound. The predeclared narrower interval has selected-source mixing contraction. Still open are the complete original E inventory, all-stage changed-diagonal estimates with sufficient future weight margin, a homogeneous numerical spectral gap, physical/cutoff matching, and the nontrivial continuum Yang–Mills construction. This is the third and final authorized loop; AG2 and AI3 are unexecuted. Scientific priority is unverified.
