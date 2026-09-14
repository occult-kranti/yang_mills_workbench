# N2 reverse: complete tail-cube support and time certificate

## Verdict and independence

The exact incident-face budget is

\[
 D_L(q)=\mathcal B(q)(1-q^{4L})(1-q^{2L})(1-q^L).
 \tag{1}
\]

For the frozen support/time protocols, the normalized N1 certificate vanishes
exactly when `beta<1` and `gamma<3(1-beta)`. This is necessity for this specified
nonnegative upper certificate only, not for actual correlation convergence.
Fixed-L logarithmically shortened gamma=3 windows converge by the certificate.
No current forward or skeptic N2 solution was read. N1 and I1 are inherited
shared results; this is an independent reconstruction under those premises.

## 1. Reconstruct the geometry required by the desired bound

To use N1 for moving observables, reconstruct `D_F(q)` for each finite cover,
not a new Hamiltonian. Define the tail rectangle

`R_L={0,...,4L-1} x {0,...,2L-1} x {0,...,L-1}`.

For every v in R_L own all three positive links `(v,v+e_a)`. Tail division
`(floor(v_x/4),floor(v_y/2),v_z)` is unique, giving exactly `24L^3` links.
Each block contains its entire ten-link selected strip (six x-links and four
y-links) plus fourteen free singleton factors. Every link of the strip has
its tail in that block. Thus this union really is a complete reference-factor
cover. It includes outgoing links whose heads lie outside R_L. It is not the
graph of links internal to the displayed vertex rectangle.

For a positive-oriented face with base v and axes a<b, its link tails are
v, v+e_a and v+e_b. If any one lies in R_L, then v lies in R_L: the rectangle
is downward closed within the nonnegative octant. Conversely, v in R_L supplies
two incident owned links. Therefore, for every integer L>=1,

**a face meets E_L if and only if its base lies in R_L.**

This proves completeness, including all crossing faces. It uses the origin
boundary: negative face bases are not present. There are three face orientations
per base. The selected faces are precisely xy faces with `x mod 4 in {0,1,2}`
and even y. There are `3L^3` selected faces and `21L^3` omitted incident faces.
Deduplicating by base and unordered axis pair counts each once.

Write `S_n(q)=(1-q^n)/(1-q)`. Subtract the selected sum from all faces:

\[
24D_L(q)=3S_{4L}(q)S_{2L}(q)S_L(q)
 -(1+q+q^2)S_L(q^4)S_L(q^2)S_L(q).
\tag{2}
\]

Both terms have the common numerator
`F_L(q)=(1-q^(4L))(1-q^(2L))(1-q^L)`. The remaining infinite geometric
coefficient is exactly the canonical profile budget

\[
\mathcal B(q)=\frac1{24}\left[
\frac3{(1-q)^3}-\frac{1+q+q^2}{(1-q^4)(1-q^2)(1-q)}\right].
\]

Its rational simplification is the N1 polynomial expression, proving (1).
Consequently `0<D_L(q)<mathcal B(q)` for finite L and `0<q<1`, and
`D_L(1)=21L^3/24=7L^3/8` by the finite polynomial's continuous extension.
For example `D_1(1/2)=107/384`, while the infinite budget is `107/135`.

## 2. Reconstruct exactly what must vanish

Use the same fixed canonical infinite-volume state, representation and
Hamiltonian as N1. Let `A_q,B_q` be the contract's complex gauge-invariant
bounded local observables, with B_q supported on F_L(q), and let
`M=sup_q ||A_q||||B_q||<infinity`. For each q the cover is finite. N1's
all-vector strong integral and reference-factor support preservation therefore
apply directly at that q, even though the family of covers grows. The
reference support is preserved for every integration time. Outer perturbed
conjugation only needs to preserve norms. No uniform domain invariance by B_q,
fixed-vector convergence argument or interchange of q with an infinite
integral is introduced.

The rank-one trace bound is uniform over every bounded operator; hence its
state cost and both complex mean-product costs remain `6d_q M`. The frozen
stationary subtraction and conjugation remain precisely those of N1. Thus

\[
 \sup_{|t|\le T_q}|C_q^{A_q,B_q}(t)-C_0^{A_q,B_q}(t)|
 \le M K_q,
\]
\[
 K_q=6\sigma_q/\bar g+
       (2\alpha/\hbar)T_q\tau_qD_{L(q)}(q).
 \tag{3}
\]

The same moving observables are compared in both states. N1 gives
`sigma_q/gbar ~ eta epsilon^(3/2)/((1-eta)sqrt(84))`, with epsilon=1-q.
Since `tau_q=eta/(8 mathcal B(q))`, (1) yields the exact simplification

\[
 K_q=6\sigma_q/\bar g+
 \frac{C\eta}{4}\epsilon^{-\gamma}F_{L(q)}(q).
 \tag{4}
\]

The state term tends to zero. All terms are nonnegative. Therefore `K_q->0`
if and only if `T_q tau_q D_L(q)->0`, equivalently the second term of (4)
vanishes. This equivalence concerns K_q, before any possibly vanishing actual
observable norms. M=0 gives a trivial zero correlation; a smaller true support
or shrinking norms can improve the estimate without changing this certificate.

## 3. Floors, regimes and exact boundary interpretation

For beta=0, `L=L0=max(1,floor(ell))` is fixed; replacing it by ell cubed is
incorrect. For beta>0, floor division gives
`L=ell epsilon^(-beta)+O(1)`, so the maximum with one is eventually inactive.
Since `log(1-epsilon)=-epsilon+O(epsilon^2)`, the three factors in F give:

| Support regime | Asymptotic F_L(q) | Dynamic term in K_q |
|---|---|---|
| beta=0 | `8L0^3 epsilon^3` | `2C eta L0^3 epsilon^(3-gamma)` |
| 0<beta<1 | `8ell^3 epsilon^(3(1-beta))` | `2C eta ell^3 epsilon^(3(1-beta)-gamma)` |
| beta=1 | `f(ell)=(1-e^(-4ell))(1-e^(-2ell))(1-e^(-ell))` | `(C eta/4) f(ell) epsilon^(-gamma)` |
| beta>1 | `1` | `(C eta/4) epsilon^(-gamma)` |

The first two asymptotic ratios tend to one; the last two entries mean positive
limits. For beta<1 use `epsilon L->0` and
`(1-q^(aL))/(aL epsilon)->1`. For beta=1, `epsilon L->ell`; the floor's
O(epsilon) effect on the exponent vanishes. For beta>1,
`q^(aL)<=exp(-a epsilon L)->0`. These arguments cover every allowed sequence
approaching q=1, not just the checker's rational fixtures.

For beta<1 and gamma<3(1-beta), all terms vanish with sufficient rate
`O(epsilon^min(3/2,3(1-beta)-gamma))`. At gamma=3(1-beta), the normalized
certificate instead tends to `2C eta L0^3` for beta=0 or `2C eta ell^3` for
0<beta<1. Above that boundary it diverges. For beta=1, gamma=0 has positive
limit `(C eta/4)f(ell)`; for beta>1, gamma=0 has limit `C eta/4`. Positive
gamma in either of these regimes makes this uncapped certificate diverge.
Consequently the stated strict region is necessary and sufficient for K_q
to vanish within the frozen nonnegative exponent domain.

For fixed L and `T_q=(hbar/alpha)C epsilon^-3/[log(1/epsilon)]^k`, any fixed
k>0 gives dynamic certificate asymptotic `2C eta L^3/[log(1/epsilon)]^k->0`.
The unshortened k=0 endpoint tends to `2C eta L^3>0`. These are substitutions
into (3), not additional research loops or proofs of true endpoint failure.

## 4. Rejecting controls and scope

The checker independently generates physical edges, complete blocks and square
incidences, then compares with (2) and (1) using exact rational arithmetic.
Clipping heads outside R_L removes `14L^2` outgoing links. Keeping only faces
whose four links are owned loses crossing terms: the omitted count becomes
`21L^3-28L^2+7L`; at L=1 this is zero instead of 21. The first counterexample
also changes the incident weighted budget. Substituting the infinite sum for
D_L suppresses F_L, falsely destroying the fixed-support convergence range.

For beta=0, ell=3/2 gives L=1 and endpoint coefficient `2C eta`, whereas using
ell as L would multiply it by 27/8. Exact protocol fixtures test this floor
effect and all three support regimes. Controlled exponential and logarithm
enclosures accompany the critical/logarithmic examples; they do not replace
the asymptotic proof.

Constant B_q has exactly zero connected correlations at all q and t even when
its chosen enclosing support is large. Thus a positive K_q cannot imply actual
nonconvergence. Neither D_L's exactness nor its positive weights make the
commutator/correlation upper estimates into lower bounds. Actual moving-family
failure and the nonconstant endpoint remain open.

Physical spacing a, E_star>0, alpha/E_star>0, hbar>0 and eta in (0,1) are fixed.
The observed side lengths are `4aL,2aL,aL`; ell,beta and the time window are
observation-design parameters. No action, physical clock, state, gap or
representation is changed. This is not a continuum or homogeneous limit.

N1's checked strong-operator framework is established mathematics:
Nachtergaele-Sims, section 2, equations (6)-(12), Proposition 2.1 and Lemma 2.2.
The section was checked in N1 and the primary text revisited for this
application; no additional theorem is imported. The complete tail-cube budget
and the resulting support/time certificate are this loop's scoped derivation.
[Primary source](https://arxiv.org/html/1410.8174v1#S2).
Scientific priority is unverified. Actual endpoint behavior needs additional
information beyond this upper estimate; future targets belong to the advisor.

Reproduce with `python3 -B research/round22/reverse/n2/check.py --output NEW_DIR`
and independently with `python3 -O -B` into another new directory. Exact
controls, outputs and source hashes accompany this mathematical proof; the
checker is not an infinite-dimensional formalization. The N1 method snapshots
are bound by reference, avoiding duplicate mutable instruction copies.
