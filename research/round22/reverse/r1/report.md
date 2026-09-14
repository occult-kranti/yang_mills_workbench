# R1 reverse: the actual initial diagonal inverse and its boundary

The initial interacting inverse exists uniformly on the required interval.
It cancels the interior homological source exactly, but the complete boundary
commutator survives. For the frozen actual SU(2) diagnostic source its squared
norm on the product vacuum is exactly `7 tau^2/432`, nonzero at every nonzero
tau. This source is admissible; it is **not** identified with an O1-generated
residual. Neither a later-stage iteration nor a numerical homogeneous gap is
established. The current forward and skeptical R1 solutions were not read.

## Actual reference and inverse premises

Use the homogeneous I1/O1 full-link model, with tail ownership
`b(a)=(floor(a_x/4),floor(a_y/2),a_z)`. Each complete factor owns 24 links.
The selected strip comprises the three xy faces based at `(0,0,0)`, `(1,0,0)`,
`(2,0,0)` and their ten links. Its actual normalized ground remains unchanged.
Fourteen independent free Haar rotors complete the factor. In energy unit
`delta=alpha/8`, the inherited onsite operator is

`h_x=(H_strip-E_strip)/delta + 8 sum_(14 free e) C_e >= I-P_x`.

The selected couplings remain in the inherited region
`|lambda_L|,|lambda_R|<=alpha/2`, `|mu|<=alpha/8`. Its unique zero vacuum
and onsite gap at least one are accepted I1 premises, not Q2 gap transfers.
Let `Gstar={0,e_x,e_y,e_z}`. For every retained whole star `B_b=b+Gstar`,
`phi_b=-(tau/3)sum_(21 omitted anchored f)W_f`, `D_b=Q_b phi_b Q_b`.
All declared four-factor supports remain, including projector factors.
Wilson multipliers have norm one, so `||D_b||<=7|tau|`, and `D_b Omega=0`.
No positivity of D_b is assumed.

For any finite nonempty allowed Y, put `N_Y=#{b:B_b subset Y}` and
`H_Y=sum_Y h_x`, `D_Y=sum_(B_b subset Y)D_b`, `G_Y=H_Y+D_Y`.
The spectral tensor sum H_Y is nonnegative self-adjoint, with domain the
intersection of its finitely many factor domains. D_Y is bounded
self-adjoint, with norm at most `7|tau|N_Y`; consequently

`D(G_Y)=D(H_Y)`, `D(G_Y^(1/2))=D(H_Y^(1/2))`

in the positive regime below. Indeed the second equality follows directly
from the two-sided form comparison. Commuting vacuum projectors give

`Q_b <= sum_(x in B_b)(I-P_x)`.

A site is in at most four retained stars (anchors x and x-e_i). Thus on the
entire form domain

\[
 |\langle\psi,D_Y\psi\rangle|
 \le 28|\tau|\langle\psi,H_Y\psi\rangle,
 \qquad (1-a)H_Y\le G_Y\le(1+a)H_Y,\quad a=28|\tau|.
 \tag{1}
\]

Write `g=1-a`. For `|tau|<1/28`, `G_Y Omega_Y=0` and
`G_Y>=g H_Y>=g Q_Y`. Its zero ground is unique, and its complementary inverse
exists with norm at most `1/g`, uniformly in Y and Lambda. In particular
`|tau|<=5/1664` gives `g>=381/416` and inverse bound `416/381`.
The larger open interval is justified only for this initial G, independently
of O1's rotation radius.

## Reconstructed homological map and domains

For bounded self-adjoint R_Y define v,A,u,S exactly as in the contract, and
write `r_v=||v||<=||R_Y||`. The inverse maps into `Q_Y D(H_Y)` and

\[
 \|u\|\le r_v/g,\quad
 \|G_Y^{1/2}u\|\le r_v/\sqrt g,\quad
 \|H_Y^{1/2}u\|\le r_v/g,\quad
 \|H_Yu\|\le c_Yr_v,\quad
 c_Y=1+7|\tau|N_Y/g.
 \tag{2}
\]

The energy bound follows by taking the inner product of `G_Yu=v` with u
and then using (1). The last bound follows from `H_Yu=v-D_Yu` and explicitly
depends on volume. No uniform second-energy bound is inferred from a form
bound. Also `G_Y >= (g/2)Q_Y(H_Y+I)Q_Y`; therefore the weighted inverse
`(H_Y+I)^(1/2)Q_Y G_Y^(-1)` is bounded by `sqrt(2)/g`, as is its adjoint.

Since u and Omega lie in D(H_Y), direct multiplication on that domain gives

`G_Y S=|v><Omega|`, `S G_Y=-|Omega><v|`, `[S,G_Y]=-A`.

Here `S*=-S`, `||S||=||u||`, `||A||=r_v`, including v=0. In particular
`||[S,H_Y]||=||H_Yu||<=c_Y r_v`, while
`||H_Y^(1/2)S||=||S H_Y^(1/2)||=||H_Y^(1/2)u||` for the bounded extensions.
The sign is derived from these products, not from a displayed source sign.

Tensor S by the exterior identity. Nonnegative commuting spectral sums give
`D(H0_Lambda)=D(H_Y) intersection D(H_ext)`. S preserves the first domain
by its finite-rank range and preserves the second by commuting with exterior
spectral projections. Hence it preserves the full operator domain and is
bounded in its graph norm, with

`||H0_Lambda S psi|| <= ||S|| ||H0_Lambda psi|| + c_Y r_v ||psi||`.

Its graph-convergent exponential and inverse preserve the same domain.
The form domain is preserved too: use (2) locally and the same exterior
spectral argument. Tensoring S with identity does not regularize arbitrary
exterior vectors. Because D_Lambda is bounded, all these operator and form
domains are also those of `H0_Lambda+D_Lambda`.

## Complete crossing identity, support and root budgets

Let `C_Lambda(Y)={b:B_b subset Lambda, B_b intersects Y, B_b not subset Y}`.
Every other retained diagonal term is interior or disjoint, so on the common
operator domain, with bounded extension,

\[
 [S_Y,H0_\Lambda+D_\Lambda]+A_Y
 =E_Y:=\sum_{b\in C_\Lambda(Y)}[S_Y,D_b].
 \tag{3}
\]

Every summand is declared on `Y union B_b`, a connected union of complete
factors, with size at most `|Y|+3`. Its norm is at most
`14|tau| r_v/g`. Thus, writing `N_cross=|C_Lambda(Y)|<=4|Y|`,

`||E_Y|| <= 14|tau| N_cross r_v/g <=56|tau| |Y| r_v/g`.

For a fixed root x let `m_x(Y)=#{b in C_Lambda(Y):x in Y union B_b}`.
It equals N_cross when x is in Y, is at most four when x is outside Y,
and is zero outside the union of these supports. The actual indexed
root-weight budget satisfies

\[
 \sum_{b\in C_\Lambda(Y):\,x\in Y\cup B_b}
 2^{|Y\cup B_b|}\|[S_Y,D_b]\|
 \le {14|\tau|\over g}\,2^{|Y|+3}r_v\,m_x(Y).
 \tag{4}
\]

For a family of sources, sum the right side over Y before taking the
supremum over x. This retains both root placements and ordered pair
multiplicity; it is not a support-independent interaction contraction.

For origin cubes `Y={0,...,L-1}^3`, every meeting anchor is in Y: negative
incoming anchors are excluded by the physical octant. There are L^3 such
anchors, and `(L-1)^3` interior ones. For bulk cubes `Y={1,...,L}^3` in
`Lambda={0,...,L+1}^3`, there are additionally `3L^2` incoming anchors,
one coordinate zero and the other two in `{1,...,L}`. Thus for all L>=1:

| Cube | Outgoing crossings | Incoming crossings | All crossings |
|---|---:|---:|---:|
| Origin | `3L^2-3L+1` | 0 | `3L^2-3L+1` |
| Bulk | `3L^2-3L+1` | `3L^2` | `6L^2-3L+1` |

The proofs count every possible anchor; exact finite enumeration checks
L=1,2,3,5 and the root incidences, including the singleton cases 1 and 4.

## Actual SU(2) boundary falsifier

In the prescribed `Lambda={0,1}^3`, the only retained anchor is zero;
`Y={0}` contains no whole star, so `D_Y=0`. Let e be the free z-link at the
fine origin and `chi_e=Tr(g_e)`. Actual normalized Haar measure gives
`<chi_e>=0`, `||chi_e||_2^2=1`, and `C_e chi_e=(3/4)chi_e`.
Therefore the frozen `v=chi_e Omega_Y` has norm one, `H_Yv=6v`,
`u=v/6`, `||R_Y||=||A_Y||=1` and `||S_Y||=1/6`.

Every omitted face has at least two independent free Haar links: z links
for xz/yz faces, odd-row y links for odd-y xy faces, or separator x links
for the remaining xy face. Distinct elementary faces share at most one
link. The checker enumerates all 21 faces and 210 distinct pairs in the
actual 4x2x1 ownership cell, without replacing their joint law by independent
plaquette variables.

Choose a free link of f different from e. Haar integration kills
`<Omega,W_f chi_e Omega>`, so `Q_0 phi_0 v=phi_0 v`. For distinct f,h,
choose a free link of f absent from h. Its central sign flip reverses W_f
but leaves `chi_e^2` invariant even if that link is e. Consequently
`<chi_e^2 W_f W_h>=0`. For f=h, integrate a free link different from e.
Conditional Haar invariance makes its Wilson trace one coordinate of a
uniform unit quaternion, with second moment 1/4. Hence

`<chi_e^2 W_f^2>=1/4`, `||sum_(21 f)W_f v||^2=21/4`.

These arguments hold conditionally on every selected-strip link, so they
keep its exact ground wavefunction and require no finite-spin replacement.
Using `D_0 Omega_Lambda=0`, (3) now gives

\[
 E_Y\Omega_\Lambda=-D_0(v\otimes\Omega_{\rm ext})/6
 ={\tau\over18}\sum_{f=1}^{21}W_f
       (v\otimes\Omega_{\rm ext}),\qquad
 \boxed{\|E_Y\Omega_\Lambda\|^2={7\over432}\tau^2.}
 \tag{5}
\]

In particular `sqrt(7/432)|tau| <= ||E_Y|| <= (7/3)|tau|` for this probe.
At tau=0 the defect is zero. Formula (5) rejects deleting outgoing stars or
promoting the interior inverse to a full-volume cancellation for arbitrary
admissible sources. It does not prove a lower bound for an O1-generated
residual, a generic boundary-area lower bound, or failure of actual iteration.

## Source comparison, controls and remaining premise

The primary comparison is Del Vecchio, Froehlich and Pizzo,
[arXiv:2108.13907v1](https://arxiv.org/pdf/2108.13907), 31 August 2021.
Theorem 3.3, Lemma 4.1 and equations 4.232–4.252 were read at printed
pp.36–38, and Appendix A.3 equations A.8–A.10 at p.50. Lemma 4.1 assumes an
evolving potential estimate and a prior local gap at least 1/2; its inverse
uses interacting G minus its vacuum energy. Appendix A.3 additionally uses
a comparison to the bare energy. The full induction and a numerical
threshold were not reconstructed or imported. Equations (1)–(2) above
directly supply our initial-model premises, with vacuum energy zero.

The exact checker tests free-Haar normalization, actual-face witnesses,
complete supports, cube and root counts, and both signs of tau. A separate
three-level noncommuting H/D fixture rejects using the bare inverse for an
interacting cancellation, the opposite skew sign, and assuming D positive.
It checks algebra only; (5) supplies the actual-model counterexample.
All checks use explicit exceptions; ordinary and optimized outputs agree
bytewise. The scripts complement, rather than formalize, the domain proof.

Compared with O2, the interacting inverse absorbs its interior D commutator.
The actual boundary remains linear in the source, with explicit support
growth and root counts. Later diagonal updates are not the initial D treated
here. Controlling those updates, all boundary contributions, inverse gaps,
domains and summable support losses through every stage remains unresolved.
A gap for H0+D alone is not a gap for H0+D+R. No Q2 positivity or spectral
bound is transferred, no homogeneous representation is identified, and no
continuum result follows. Scientific priority remains unverified.

All operators and tau above are dimensionless. Physical energies multiply
by delta=alpha/8; a,E_star,alpha/E_star and hbar stay positive and fixed,
and physical evolution uses t/hbar. No time fit is made.

Reproduce with `python3 -B research/round22/reverse/r1/check.py --output NEW_DIR`
and `python3 -O -B` into another fresh directory. R2 is not selected here.
