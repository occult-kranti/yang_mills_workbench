# I2 forward: an exact local dressing lemma with a retained remainder

The forward derivation is frozen before comparison with reverse I2. It uses the corrected admitted I1 gate and the frozen I2 contract. The current reverse I2 files were not read. The result is a one-star operator identity and bound. It does not evaluate a homogeneous infinite-lattice stability interval.

## 1. Source extraction attempt and its exact stopping point

I1 normalizes each onsite reference by `delta=alpha/8`, at fixed positive `alpha/E_star`, and derives `epsilon=7|tau|` on the four-block star `S={0,e_x,e_y,e_z}`. In [Yarotsky, math-ph/0411042v1, pp. 2–4](https://arxiv.org/pdf/math-ph/0411042), Theorems 1–3 introduce range-dependent `c1,c2` without numerical values. Section 2, p. 6, explicitly uses variable constants `c` and `epsilon`; Lemma 1 and the later commutator bound do not give numerical smallness thresholds. Substituting a guessed value would not extract a constant.

The alternative [Yarotsky, math-ph/0412040v1, pp. 2–4, Theorems 1–2](https://arxiv.org/pdf/math-ph/0412040) allows infinite-dimensional site spaces and splits the perturbation into relative and bounded parts. Its threshold `delta(kappa,dimension,range)` is also existential. It additionally imposes translation-invariance and a classical reference structure that would require a new dictionary; no transfer is asserted here. Its purely relative part annihilates the reference vacuum. This motivates the direct test below, not a numerical application of that theorem.

Thus the specific extraction attempt is insufficient: the missing data are numerical cluster/commutator convergence constants for the actual range and admissible site spaces. A finite-star norm or an eigenvalue sample cannot determine them. Full copyrighted source PDFs were not stored in this deliverable.

## 2. Frozen local operator and exact Haar variance

Work on the tensor product of the four complete I1 sites in one star. Let

\[
H_0=\sum_{b\in S}h_b,\quad H_0\Omega=0,\quad
P=|\Omega\rangle\langle\Omega|,\quad Q=1-P,\quad H_0\ge Q,
\]

and retain all 21 omitted faces anchored at the central block:

\[
\phi=-{\tau\over3}\sum_{f\in O_0}W_f,
\qquad\|\phi\|=7|\tau|=:M.
\tag{I2.1}
\]

The exact coefficient is inherited from `nu/delta=tau/3`, not chosen to improve a bound. Every such face has two free Haar links: two z links for xz/yz, two odd-y y links for odd-y xy, or two separator x links for even-y xy with x residue 3. A link in these classes occurs in no selected strip. Two distinct elementary square faces share at most one link, so at least one free link of f does not occur in g. Its conditional Haar integral gives `E[W_f W_g]=0`. Integrating one free link in a repeated face gives `E[W_f²]=1/4`; integrating it once gives `E[W_f]=0`. The selected strip ground states may be internally entangled; independence of entire faces is never assumed.

The source of this model-specific Haar mechanism is [H2](../../../round20/forward/h2/report.md). The checker independently reconstructs every face and pair in this local group and verifies both witness links are globally free. The elementary-square argument, rather than the 210 checked pairs, supplies the general reason.

Consequently

\[
v:=\phi\Omega\perp\Omega,\qquad
\sigma^2:=\|v\|^2={21\tau^2\over9\cdot4}
={7\tau^2\over12}.
\tag{I2.2}
\]

All quantities here are dimensionless because the Hamiltonian has been divided by delta. Multiplying any transformed energy remainder by delta restores physical energy units.

## 3. Why the untransformed interaction is not purely relatively bounded

For tau nonzero, v is nonzero. Define the inverse on the excited subspace,

\[
u=(H_0|_{Q\mathcal H})^{-1}v.
\tag{I2.3}
\]

Since `H0|Q>=1`, its inverse is bounded by one, its range belongs to `D(H0)`, and `H0u=v`. Thus `u perpendicular Omega` and `||u||<=sigma`. Let `a=<u,H0u>=<u,v>>0`. For real t and `psi_t=Omega+t*u`,

\[
\langle\psi_t,H_0\psi_t\rangle=t^2a,\qquad
\langle\psi_t,\phi\psi_t\rangle=2ta+t^2\langle u,\phi u\rangle.
\tag{I2.4}
\]

Their absolute ratio diverges as `t->0`. Hence no finite constant r can make `|<psi,phi psi>|<=r<psi,H0 psi>` hold for every form-domain vector at tau nonzero. The conclusion would be different at tau=0, where phi vanishes. Adding a bounded additive term is possible; calling the whole perturbation purely relative is not.

## 4. A bounded skew generator and the correct cancellation sign

Set

\[
S_u=|u\rangle\langle\Omega|-|\Omega\rangle\langle u|,
\qquad A=|v\rangle\langle\Omega|+|\Omega\rangle\langle v|.
\tag{I2.5}
\]

`S_u*=-S_u`, `||S_u||=||u||`, and `||A||=||v||=sigma`. Because Omega and u belong to `D(H0)`, `S_u` maps the full Hilbert space into this domain. Its exponential differs from the identity by an operator with range in their two-dimensional span. Therefore `exp(±S_u)` preserves `D(H0)`.

On that domain, `H0 S_u=|v><Omega|` and `S_u H0=-|Omega><v|`. In particular,

\[
[H_0,S_u]=A,\qquad [S_u,H_0]=-A,
\qquad\phi-A=Q\phi Q.
\tag{I2.6}
\]

The last identity uses the already proved `P phi P=0`. If that mean were nonzero, its scalar P component would have to be retained. With the sign in Equation I2.5, it is **exp(S_u) H exp(-S_u)** that cancels the offdiagonal term to first order. Reversing the conjugation sign doubles that first-order term instead.

## 5. Exact transformed remainder and its bound

No truncated Baker–Campbell–Hausdorff series is used. The bounded commutator permits the exact domain-preserving integral identity

\[
e^{S_u}(H_0+\phi)e^{-S_u}=H_0+Q\phi Q+R,
\tag{I2.7}
\]

where

\[
R=-\int_0^1(1-t)e^{tS_u}[S_u,A]e^{-tS_u}\,dt
  +\int_0^1e^{tS_u}[S_u,\phi]e^{-tS_u}\,dt.
\tag{I2.8}
\]

The integrals converge in operator norm. Unitary conjugation preserves the norms; the triangle and commutator inequalities give

\[
\|R\|\le\|u\|\sigma+2\|u\|M
\le\left({7\over12}+14\sqrt{7/12}\right)\tau^2
\le {707\over60}\tau^2.
\tag{I2.9}
\]

The rational last step follows from `7/12<16/25`, so `sqrt(7/12)<4/5`; it is a proved conservative rounding. Also

\[
\|S_u\|^2\le {7\tau^2\over12}.
\tag{I2.10}
\]

The remaining first-order diagonal block is genuinely pure relative:
`|<psi,Q phi Q psi>|<=M ||Q psi||²<=M <psi,H0 psi>`. The nonzero R is part of the transformed Hamiltonian, not an optional error to discard.

For the numerical local fixture `tau=1/64`, the exact bounds are

\[
\sigma^2=7/49152,\quad \|S_u\|^2\le7/49152,
\quad\|R\|\le707/245760,\quad M=7/64.
\]

These are evaluated local bounds. They do not declare tau=1/64 inside the global stability domain.

## 6. Independent finite-dimensional sanity fixture

Use a separate two-dimensional lemma fixture, not an SU(2) truncation:

\[
H_0=\begin{pmatrix}0&0\\0&1\end{pmatrix},\quad
\phi=\begin{pmatrix}0&t\\t&0\end{pmatrix},\quad t=1/10.
\]

Here `u=v=t e_1`, and `e^{S_u}` is the real rotation with angle t. The exact transformed remainder has entries

\[
R_{00}=\sin^2t-2t\sin t\cos t,
\quad R_{01}=t(\cos^2t-\sin^2t)-\sin t\cos t,
\quad R_{11}=-R_{00}.
\]

Alternating Taylor bounds with rational endpoints certify `||R||<=3t²` without floating-point assumptions. They also certify that the wrong-sign transformed offdiagonal entry exceeds `1/10`, while the correct first-order remainder is below `3/100`. Dropping R changes the determinant from `-t²` to zero and changes the spectrum. Exact rational matrices independently check the commutator cancellation. An added vacuum diagonal term tests the zero-mean premise.

## 7. Scope, variables and next missing proof

`u`, `S_u`, and R are quantities constructed from the specified local operator. The transformation is exactly unitary when R is retained. It introduces no action coefficient, field, physical clock, or fitted matching variable. Its local domain proof permits the unbounded onsite operators and does not assume a finite representation cutoff.

Different stars overlap. A product of their local transformations produces additional commutators and enlarges supports. This single-star lemma neither constructs that infinite product nor proves convergence of a many-block expansion. Removing R or applying the local formula to every anchor without controlling the overlap changes the problem. A valid global iteration needs summable bounds on all generated interactions, explicit combinatorial constants, retained domain control, and a vacuum/gap theorem for the final representation.

Contribution classification: the explicit `7/12` model variance and this instantiated remainder bound are project derivations, with scientific priority unverified. Bounded unitary dressing is an established operator method. The failed pure-relative route is a proved obstruction to that route. The global numerical tau interval and continuum mass-gap problem remain unresolved. No subsequent loop has been executed here.

Reproduce:

```bash
python -B research/round21/forward/i2/check.py --output /tmp/ym21-forward-i2-replay
```
