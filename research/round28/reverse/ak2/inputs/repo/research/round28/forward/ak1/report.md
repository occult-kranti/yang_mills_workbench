# AK1 forward: a constructive actual Wilson variance floor

For the **same original xz Wilson at zero** in the actual I1/AJ1/AJ2
homogeneous positive-orthant state, this independent forward derivation gives

\[
 \operatorname{Var}_{\omega}(W)\ge {119\over576}>{1\over5}
 \quad\text{if}\quad |\tau|<\tau_*,\qquad |\tau|\le2^{-16}.       \tag{1}
\]

This is a conditional dimensionless signal bound. The additional numerical
cap does **not** evaluate
`tau_*=min(c1(S),1/(2c2(S)))/7` or certify any chosen positive coupling.
The selected coefficients remain fixed in their inherited ranges
`|lambda_L|,|lambda_R|<=alpha/2`, `|mu|<=alpha/8`. The result is uniform
over those choices. AJ2's qualitative positivity on the larger symbolic
regime remains unchanged.

This is investigation nine, under frozen contract
`2afd1ff408b4774e79f1964f796835c6e4088cce22de5c1c66c85d796c9a9810`.
The advisor proposed the overlap route prospectively; its constants and
mixed-state argument below were independently derived after input preflight.
Current reverse AK1 and skeptic AK1 mathematics stayed unread throughout
production and freeze. Historical names are methodological lenses, not people
participating or endorsements; common sources imply correlated model
authorship, not independent physical observations.

## 1. The original links, endpoints and complete interaction groups

A coarse site `b=(i,j,k)` owns all three positive original links with tails
`(4i+r,2j+s,k)`, `0<=r<4`, `0<=s<2`. Euclidean division gives each
original tail its unique owner
`(floor(x/4),floor(y/2),z)`. The unreduced Hilbert factor is
`K_b=L2(SU(2)^24)`. The selected xy strip uses six x links with
`r=0,1,2; s=0,1` and four y links with `r=0,1,2,3; s=0`.
The remaining two x, four y and eight z links are free reference links.
Physical Gauss-invariant factors are not assumed to tensorize.

The frozen face is

\[
 W={1\over2}\operatorname{Tr}
 [U_x(0)U_z(e_x)U_x(e_z)^{-1}U_z(0)^{-1}].                    \tag{2}
\]

Its four distinct stored links have owners `0,0,e_z,0`, so its complete
region is `R={0,e_z}`: 48 original links, twenty selected and twenty-eight
free. Its sixteen tails have `0<=x<4, 0<=y<2, 0<=z<2`. The endpoint
set adds four x heads `(4,y,z)`, eight y heads `(x,2,z)` and eight z
heads `(x,y,2)`, for 36 endpoint SU(2) actions. Every link's tail and
head actions are explicitly listed in `output/results.json`.
The original transformation `U_(v,w) -> g_v U_(v,w)g_w^-1` telescopes
around (2) to conjugation at zero. Thus `W` is a bounded self-adjoint
physical multiplier with `||W||=1`. Its four loop vertices do not replace
the complete region's endpoint set.

For any elementary face anchored at original tail `t` in axes `a<c`,
the stored tails are `t,t+e_a,t+e_c,t`. Hence its coarse support is
exactly the owners of the first three tails; there is no diagonal-corner
tail. Increasing x crosses a block exactly at `r=3`, increasing y
exactly at `s=1`, and increasing z always crosses. Exhausting those
phases gives the complete omitted-face table:

| Relative support | Number |
|---|---:|
| `{0,e_x}` | 1 |
| `{0,e_y}` | 3 |
| `{0,e_x,e_y}` | 1 |
| `{0,e_z}` | 10 |
| `{0,e_x,e_z}` | 2 |
| `{0,e_y,e_z}` | 4 |

There are 24 anchored faces, three selected and 21 omitted. Their union
is the whole four-site star `S={0,e_x,e_y,e_z}`. The actual normalized
interaction is `phi_b=-(tau/3) sum_(21 faces) W_f`, with
`||phi_b||=M=7|tau|`. The upper bound is the triangle inequality; equality
follows from positive-Haar-measure neighborhoods of the identity configuration.
The Hamiltonian retains this entire group only when `b+S` lies in the
finite coarse cuboid. The observable cover R itself has no whole star,
although ten individual omitted faces fit inside it. That two-factor
boundary Hamiltonian is not substituted for the actual incident environment.

An incident anchor must be `r-s` for `r in R,s in S`. Conversely every
nonnegative such anchor has a star meeting R. Thus

\[
 \mathcal I_+(R)=(R-S)\cap\mathbb Z_+^3=\{0,e_z\},\qquad
 \mathcal I_\Lambda(R)=\mathcal I_+(R)\cap
                         \{b:b+S\subset\Lambda\}.            \tag{3}
\]

The star at zero meets both sites and is counted once. Summing separate
site incidences would incorrectly count it twice (three instead of two);
that overestimate is safe but unnecessary. The finite cubes have:

| Coarse sides | Links | Endpoints | All retained stars | Incident stars at R | Charged incident faces | Energy ceiling |
|---|---:|---:|---:|---:|---:|---|
| `(2,2,2)` | 192 | 120 | 1 | 1 | 21 | `14|tau|` |
| `(3,3,3)` | 648 | 342 | 8 | 2 | 42 | `28|tau|` |
| `(4,4,4)` | 1536 | 736 | 27 | 2 | 42 | `28|tau|` |

For the incidence-only interior control `{(1,1,1),(1,1,2)}`, the orthant
anchor union has seven elements: `(1,1,1),(1,1,2),(0,1,1),(0,1,2),
(1,0,1),(1,0,2),(1,1,0)`. It is absent from the first cube; the other
two retain four and seven incident groups. Outgoing-only counting gives
one and two. They must charge 84 and 147 group faces, although just 49
and 82 individual faces touch the interior region. This is a genuine
discriminator against substituting individual-face incidence for star cost.
No translated-observable variance theorem is claimed.

At the origin both tempting controls are blind: every incident anchor is
in R, and all faces in its group touch R. The checker retains these
nondiscriminating origin cases and their interior replacements explicitly.

## 2. Actual reference energy gives actual vacuum overlap

Keep the inherited shifted reference, including every free link and its
unique vacuum:

\[
 h_b={H_{\mathrm{strip},b}-E_{\mathrm{strip},b}
                  +\alpha\sum_{e\mathrm{\ free}}C_e\over\delta},
 \quad\delta={\alpha\over8},\quad h_b\ge I-P_b,\quad h_b\Omega_b^0=0.
                                                                    \tag{4}
\]

The selected-strip gap is at least delta; each free rotor's physical gap
is `3alpha/4=6delta`. These source results justify (4) uniformly over
the frozen selected-coefficient ranges. Put
`h_R=h_0+h_ez`, `Omega_R^0=Omega_0^0 tensor Omega_ez^0`,
and `P=|Omega_R^0><Omega_R^0|`. The two local projections commute.
On the full unreduced tensor space their four joint projection sectors
sum to the identity, and

\[
 h_R\ge (I-P_0)+(I-P_{e_z})\ge I-P_0P_{e_z}=I-P.            \tag{5}
\]

The second difference is the positive projection
`(I-P_0)(I-P_ez)`. These are closed-form inequalities for the
nonnegative self-adjoint reference sum, with bounded right sides; they
extend by closure from the finite tensor form core. The common kernel
is precisely the one-dimensional product vacuum. No physical tensor
factorization or finite representation cutoff enters (5).

AJ1's full controlling proofs establish actual normal local densities and
the domain-valid vacuum-reset inequality. Explicitly, replacing R in a
finite ground density rho by `P tensor Tr_R rho` removes its R reference
energy, preserves the complementary marginal and cancels all disjoint
interactions. Bounded spectral truncations and monotone convergence justify
the unchanged unbounded exterior energy. The mixed reset is a valid trial
density of finite form energy. The variational principle cancels the
finite ground scalar exactly and charges each incident group by `2M`:

\[
 \operatorname{Tr}(\rho_{\Lambda,R}h_R)
 \le2M|\mathcal I_\Lambda(R)|\le4M=28|\tau|.                 \tag{6}
\]

AJ1 proves trace-norm local convergence to the actual density rho_R.
Alternatively its inherited bounded-local state limit suffices on each
bounded spectral truncation of h_R. Passing (6) for such truncations
and then increasing the truncation proves
`Tr(rho_R h_R)<=28|tau|`. This trace is the actual local density's
**reference** energy, not an excited vector's physical spectral moment.

Taking traces in (5) gives the actual overlap estimate

\[
 e:=1-\operatorname{Tr}(\rho_RP)
 \le\operatorname{Tr}(\rho_Rh_R)\le28|\tau|
 \le {7\over16384}=:\varepsilon_*.                         \tag{7}
\]

The state rho_R is not replaced by P. At tau zero, (7) forces rho_R=P;
for nonzero admissible tau it only constrains their distance.

## 3. A proved mixed-density trace estimate

For every positive trace-one density rho and rank-one P on any separable
Hilbert space,

\[
 \|\rho-P\|_1\le2\sqrt{1-\operatorname{Tr}(\rho P)}.        \tag{8}
\]

Here is a proof rather than an assumption of local purity. For a unit
vector psi, choose its phase so its overlap with the unit vector of P
is nonnegative. On their span write
`psi=a Omega+sqrt(1-a^2) eta`. The matrix of
`|psi><psi|-P` has trace zero and eigenvalues
`+-sqrt(1-a^2)`; outside the span it is zero. Therefore its trace norm
is `2sqrt(1-a^2)`, including the coincident and orthogonal limits.
The trace-class spectral decomposition
`rho=sum_j p_j |psi_j><psi_j|`, `p_j>=0`, `sum p_j=1`, converges
in trace norm. Since `rho-P=sum_j p_j(|psi_j><psi_j|-P)`, the
triangle inequality and weighted Cauchy–Schwarz give

\[
 \|\rho-P\|_1\le2\sum_jp_j\sqrt{1-|\langle\Omega,\psi_j\rangle|^2}
 \le2\sqrt{\sum_jp_j(1-|\langle\Omega,\psi_j\rangle|^2)}.
\]

The last expression is (8); the countable sums follow by monotone
convergence and trace-norm convergence. This is an upper bound and
usually not an equality for mixed densities.
For every bounded A, the trace-class/operator inequality
`|Tr[(rho-P)A]|<=||rho-P||_1 ||A||` follows by the singular-value
expansion of rho-P and the bound on each unit-vector matrix element.

Combining (7) and (8), write `d=||rho_R-P||_1`. Then

\[
 d\le2\sqrt{28|\tau|},\qquad
 d^2\le {7\over4096}<{1\over576},\qquad d<{1\over24}.       \tag{9}
\]

The exact rational comparison is `7*576=4032<4096`. No irrational
number is approximated numerically and no source stability constant is
evaluated.

## 4. Reference moments and both actual moments

The product reference vector includes arbitrary selected-strip entanglement,
but it is independent of each of its free original z links. Condition on
all link matrices except `u=U_z(0)`, an actual free link in R. Then the
holonomy in (2) is `A u^-1`, where A is fixed in SU(2) for that
conditional integral. Inversion followed by left multiplication preserves
normalized Haar measure. The remaining weight
`|Omega_R^0|^2` is independent of u and integrates to one.

A Haar SU(2) element is a uniform unit quaternion on S3. Its scalar
component is its half trace. Antipodal symmetry makes its mean zero;
the four equal second moments sum to one, so each is one quarter.
Consequently, for the actual selected reference, uniformly in its allowed
coefficients,

\[
 \langle\Omega_R^0,W\Omega_R^0\rangle=0,\qquad
 \langle\Omega_R^0,W^2\Omega_R^0\rangle={1\over4}.          \tag{10}
\]

This conditions on one original link, not independent plaquette variables.
It applies only to the reference moments; the interacting density need not
factor in that link. With the actual unknown real mean `m=omega(W)`,
trace duality and `||W||=||W^2||=1` give

\[
 |m|\le d,\qquad \omega(W^2)\ge {1\over4}-d,\qquad
 v=\omega(W^2)-m^2\ge {1\over4}-d-d^2.                    \tag{11}
\]

The polynomial `d+d^2` increases for nonnegative d: its difference at
`y>=x>=0` is `(y-x)(1+y+x)>=0`. Thus (9) proves

\[
 v\ge {1\over4}-{1\over24}-{1\over576}
       ={119\over576}={1\over5}+{19\over2880}.             \tag{12}
\]

Before rational relaxation the derived lower expression is
`1/4-2sqrt(28|tau|)-112|tau|`. Either coupling sign is covered by
the same absolute-value budget. The numerical endpoint in (7) is
conditional algebra under the additional actual symbolic stability premise.
The unknown squared mean in (11) is indispensable; no symmetry of the
interacting state has been asserted.

## 5. Controls that can damage the inference

The new checker performs 69 explicit-exception checks and reconstructs the
geometry directly. It never imports or executes an earlier science checker.
The finite controls are diagnostics of the argument, not proofs of the
infinite-dimensional premises or observations of the actual state.

* For `psi=(24/25,7/25)` and P onto the first coordinate, the exact
  trace distance is `14/25`, with `e=49/625`. Replacing (8) by `2e`
  or by `sqrt(e)` fails strictly. This detects the missing square root
  and the missing factor of two separately.
* The mixed density `diag(3/4,1/4)` has determinant `3/16`, purity
  `5/8` and trace distance `1/2` to P. It cannot be a pure-vector
  projector; falsely imposing the pure-state equality in (8) would give
  1. The valid upper bound survives. The noncommuting mixed matrix
  `[[4/5,1/5],[1/5,1/5]]` separately has determinant `3/25` and
  distance squared `8/25<4/5`, auditing the same inequality with
  off-diagonal coherence retained.
* On the actual local configuration space, the normalized vector
  `sqrt(1+W) Omega_R^0` defines a legitimate normal state. By (10)
  and the vanishing reference third moment its mean is `1/4`, second
  moment `1/4`, and variance `3/16<1/5`. This rejects dropping the
  squared mean or assigning Haar moments to every normal density.
  It is not an actual interacting ground at a tested coupling. Equation
  (8) and its nonzero mean require `1-Tr(rho P)>=1/64`, hence
  reference energy at least `1/64>7/16384` (possibly infinite).
  Precisely the added energy/overlap premise excludes this control.
* A direct concentration alternative uses
  `psi_A=1_A Omega_R^0/sqrt(p)`, `A={|W|<1/4}` and
  `p=<Omega_R^0,1_A Omega_R^0>`. Conditional Haar gives the positive
  density `(2/pi)sqrt(1-w^2)` on `(-1,1)`, so `p>0` and symmetry
  gives mean zero and `0<Var(W)<1/16`. This normal, gauge-invariant
  rank-one state therefore refutes a uniform margin from normality alone.
  Since the Haar density is at most one (`pi>2`), `p<=1/2`.
  Its reference-vacuum overlap is exactly p, hence its reference energy
  is at least `1-p>=1/2`, far outside (7). This is an extended-form
  inequality; no finite form energy of the discontinuous indicator is
  asserted. The energy premise, rather than normality, excludes it.
* All four joint projection sectors verify (5). The separate units fixture
  keeps `alpha=24, delta=3` and abstract raw onsite ground scalars
  `-5,-7`. Correct subtraction gives zero reference-vacuum energy;
  omitting it gives `-4`. Dividing a physical delta excitation by alpha
  instead gives `1/8`, which cannot support a unit-gap inequality.
  A common added scalar cancels. These are abstract bookkeeping fixtures,
  not evaluations of the selected-strip energies.
* The origin's blind incidence controls and the interior discriminators
  are retained as described in Section 1. An explicit full noncommuting
  quaternion assignment gives Wilson `-49/170` before and after full
  endpoint transformation; dropping head actions instead gives
  `-2471/2890`. Its first attempted gauge assignment discriminates.
* To test the cap inference, hypothetical positive constants
  `c1=2^-16,c2=1` give a hypothetical `tau_*=2^-16/7`, smaller
  than the additional cap. They are explicitly not the actual theorem's
  constants. Positivity of unspecified constants alone cannot certify
  the cap endpoint; the strict source inequality is also retained.

No scientific diagnostic run failed. Two blind proposed incidence channels
were identified analytically before the first run and were deliberately
implemented as blind controls, with their replacements. The first successful
development output and fresh normal/optimized outputs have identical result
bytes; the verification record preserves their hashes and commands.

## 6. Source depth, reproducibility and supported scope

The exact contract, all 43 required source originals and all used instructions
were snapshotted before scientific production. The input inventory uses generic
entries under `inputs/source-inventory.json`. An additive administrative
correction placed its unchanged bytes at that canonical location; original
input history remains bound unchanged. The advisor's input preflight passed
before scientific work. Every runtime content read uses an owned snapshot;
original paths and installed absolute origins are provenance metadata only.
The results have a flat repository-relative binding map for the checker,
contract, required originals, canonical and historical manifests, and owned
snapshots. The report is separately included by the final full-file freeze.

Both complete AJ1 and AJ2 producer reports, the AJ1 post-review, and AJ2
independent and post-review proofs were read directly from owned snapshots.
I1's two complete reports and source dictionary, and A1/A2's complete forward
reports, were also read. AJ1 supplies the local normality and reset theorem;
I1's external stability result is inherited, not reproved. The immutable
40-page eight-loop addendum was read in full on all forty pages, with
particular attention to the actual homogeneous AJ chapters and the scope
ledger; this reading does not independently revalidate every inherited
proof chain. The network's structure, all loop summaries, full AJ
nodes and incident edges were inspected. `reading-ledger.json` records
these depths and distinguishes source verification from full theorem audits.
No new external primary-source retrieval or scientific-priority comparison
is claimed in AK1. The closest controlling results are AJ1's regional
energy estimate and AJ2's actual Wilson construction; elementary projector,
trace-class and conditional-Haar arguments supply this quantitative application.

Run from the repository root with fresh absolute destinations:

```bash
python -B research/round28/forward/ak1/check.py --output /absolute/fresh/ak1-normal
python -B -O research/round28/forward/ak1/check.py --output /absolute/fresh/ak1-optimized
```

Each invocation emits only `results.json` in the destination directory.
The frozen `validation.json` records fresh normal/optimized equality and
the first successful development comparison. `freeze.json` binds every
owned file except exactly itself, including all administrative history and
any nested historical files named freeze.json.

The added conclusion is (1) for this particular original physical observable,
state, boundary limit and conditional subregime. The fixed positive
`alpha,hbar,E_star,a` are not recalibrated: h_R and variance are dimensionless,
delta is an energy, and the physical Hamiltonian remains AJ1's centered
restriction. Nothing here places the Wilson-excited vector in a physical
operator or form domain, evaluates its energy moment, provides a spectral
window or lower exponential decay, or computes a mass. No global faithfulness,
other boundary limit, summable-model substitution, continuum matching or
Yang–Mills completion percentage follows. Scientific priority is unverified.
AK2 remains unselected and no additional investigation was executed.
