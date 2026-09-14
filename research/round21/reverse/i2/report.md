# Reverse I2: a local vacuum rotation with its full remainder

The proposed one-star dressing lemma and constants are valid. They do not evaluate a homogeneous many-block stability interval. This report independently reconstructs the lemma from its target and does not read the current forward solution.

## 1. The quantitative target still needs an evaluated expansion constant

I1 gives the dimensionless local interaction norm `epsilon=7|tau|`, onsite gap one, and fixed coarse support `S={0,e_x,e_y,e_z}`. To certify a particular positive numerical coupling through [Yarotsky's theorem](https://arxiv.org/pdf/math-ph/0411042), one must evaluate the source's `c1(S)` and `c2(S)` or prove another usable bound for this model.

The source Theorem 1, p.3, leaves these constants existential. Section 2, p.6, explicitly allows the symbols `c` and `epsilon` to change meaning between formulas. Lemma 1 and Eq.(8), p.7, give a qualitative small-interaction contraction; Eq.(14), p.8, has an unevaluated commutator constant; Eq.(15), p.9, uses its smallness to converge a resolvent series. Reference [23] is identified on p.17 as the earlier detailed proof. This loop has not numerically reconstructed that expansion or its original full proof. No negative statement about the existence of computable constants is intended. The precise quantitative outcome here is **insufficient**.

`source-review.json` records source locations and the primary PDF digest. Full downloaded paper bytes remain outside the repository. The remaining construction is a proved local workaround for vacuum mixing, not a replacement numerical global theorem.

## 2. Recover the local forcing from independent Haar variables

Work on the four-site coarse star alone. Let `H0` be the sum of its normalized nonnegative onsite references, with unique vacuum `Omega`, `P=|Omega><Omega|`, and `Q=1-P`. Thus `H0>=Q`. The local perturbation is

\[
\phi=-{\tau\over3}\sum_{f\text{ among 21 omitted anchors}}W_f,
\qquad\|\phi\|=7|\tau|.
\]

An omitted xz or yz face has two free z links. An omitted odd-y xy face has two free odd-y y links. An omitted even-y separator xy face has two free x links at `x=3 mod4`. Every such link is a separate Haar factor of the dressed reference. Two distinct elementary faces share at most one link. Integrating a free link of the first face absent from the second therefore kills their cross moment, even when the two faces touch the same dressed strip factor.

For the diagonal moment, condition on all other links. Haar invariance converts the Wilson trace to one coordinate of a unit quaternion. The four coordinate squares have equal expectation and sum to one, giving `E W_f^2=1/4`. Therefore

\[
\langle\Omega,\phi\Omega\rangle=0,
\qquad v:=\phi\Omega\in Q\mathcal H,
\qquad
\boxed{\|v\|^2={21\over9}\,{\tau^2\over4}
={7\over12}\tau^2.}
\]

This finite-star formula requires no spatial summability or infinite-volume state identification. The checker independently enumerates all 21 faces and 210 pairs and verifies actual unmatched free links. It does not assume independent plaquette variables.

## 3. The proposed bare relative form estimate is impossible

For nonzero `tau`, define

\[
u=(H_0|_{Q\mathcal H})^{-1}v.
\]

The spectral lower bound `H0|Q>=1` makes this inverse bounded from `QH` into `D(H0) intersect QH`; `H0 u=v` and `||u||<=||v||`. The positive number `a=<u,H0u>=<u,v>` is nonzero. For real `t` and the unnormalized trial vector `psi_t=Omega+t u`,

\[
\langle\psi_t,H_0\psi_t\rangle=t^2a,
\qquad
\langle\psi_t,\phi\psi_t\rangle=2ta+t^2\langle u,\phi u\rangle.
\]

The ratio of the absolute second form to the first grows like `2/|t|`. Hence no finite constant `C` makes `|<psi,phi psi>|<=C<psi,H0psi>` hold for all domain vectors at any fixed nonzero `tau`. Dividing trial vectors by their norm changes neither ratio. The zero-coupling exception is valid: then `v=0` and this obstruction disappears. Adding a scalar allowance would change the form estimate and must be recorded explicitly.

## 4. Construct the local unitary and prove the domain statements

Set

\[
B=|v\rangle\langle\Omega|+|\Omega\rangle\langle v|,
\qquad
S=|u\rangle\langle\Omega|-|\Omega\rangle\langle u|.
\]

The symbol `S` in this section is an operator; the geometric support remains the four-site coarse star. `S` is bounded skew-adjoint, `||S||=||u||`, and its range lies in the two-dimensional subspace spanned by `Omega,u`, both in `D(H0)`. Thus `exp(tS)-I` has range in that subspace and `exp(tS)` preserves `D(H0)` for every real `t`; the inverse has the same property. Direct multiplication on this domain gives

\[
[S,H_0]=-B,\qquad \|B\|=\|v\|.
\]

This commutator has a bounded extension. Since `P phi P=0`, `phi=B+Q phi Q`. The **correct** conjugation direction is `exp(S)(H0+phi)exp(-S)`, whose first commutator cancels `B`. Reversing the conjugation sign adds another `B` instead.

All projectors and vectors here live on the finite four-site star. Extending the resulting operator to the lattice uses tensor identity outside this star. A projector onto the vacuum of the entire infinite lattice would instead be nonlocal and is not the construction used here.

## 5. Retain the exact conjugation remainder

The domain result and bounded commutator justify the following identity on `D(H0)`, with bounded remainder:

\[
e^S(H_0+\phi)e^{-S}=H_0+Q\phi Q+R,
\]

\[
R=\int_0^1(1-s)e^{sS}[S,[S,H_0]]e^{-sS}\,ds
+\int_0^1e^{sS}[S,\phi]e^{-sS}\,ds.
\]

These are norm integrals of bounded operators; the unitary conjugations do not increase norm. Using the factor `1/2` from the first integral,

\[
\|R\|\le\|S\|\|B\|+2\|S\|\|\phi\|
\le\|v\|^2+2\|v\|\|\phi\|.
\]

Consequently the proposed constants follow:

\[
\boxed{\|S\|\le\sqrt{7/12}\,|\tau|,\qquad
\|R\|\le\left({7\over12}+14\sqrt{7/12}\right)\tau^2
\le{707\over60}\tau^2.}
\]

For the last rational bound, `(4/5)^2>7/12`, and `7/12+14*(4/5)=707/60`. No smallness assumption on `tau` is needed for this **single-star** unitary identity and bound. In physical energy units multiply the remainder bound by `delta=alpha/8`.

The surviving compression satisfies `|<psi,Q phi Q psi>|<=7|tau|<psi,H0psi>` because `H0>=Q`. The remainder may again contain vacuum-offdiagonal terms. Dropping it would falsely turn a first-order cancellation into exact vacuum decoupling.

## 6. Exact finite-dimensional checks and next missing premise

For a discriminating two-state fixture use

\[
H_0=\begin{pmatrix}0&0\\0&1\end{pmatrix},\quad
\phi=\begin{pmatrix}0&\tau\\\tau&\tau/2\end{pmatrix},\quad
S=\begin{pmatrix}0&-\tau\\\tau&0\end{pmatrix}.
\]

Here `||phi||<=3|tau|/2` and `||u||=||v||=|tau|`, so the general lemma gives `||R||<=4tau^2`. The checker encloses the actual rotation matrix using consecutive rational Taylor sums for sine and cosine at `tau=1/100,1/10,1/2`. Interval matrix arithmetic rigorously verifies the remainder bound. Its vacuum diagonal is strictly negative, rejecting the omitted-remainder model. Wrong-sign conjugation retains an offdiagonal magnitude greater than `tau`, rejecting the claimed cancellation. These are sanity fixtures for the operator lemma, not lattice spectrum measurements.

Applying local transformations at all anchors introduces overlapping commutators and larger supports. Their weighted interaction sums and all-order convergence must be bounded before a uniform many-block theorem follows. The local rotations need not commute, and their infinite global sum is not admitted as a bounded operator. Therefore this lemma supplies neither numerical global `c1,c2` nor a chosen homogeneous nonzero interval, despite having explicit local constants.

This is an established finite-rank operator method applied with a model-specific exact Haar forcing norm. Its scientific priority is unverified. The local unitary changes representation without deforming the Hamiltonian; treating the truncated transformed operator as the exact original theory would be a deformation. The continuum theory and physical mass matching remain separate unsolved targets.

Reproduce:

```bash
python -B research/round21/reverse/i2/check.py --output /tmp/ym21-reverse-i2
python -B -O research/round21/reverse/i2/check.py --output /tmp/ym21-reverse-i2-optimized
```
