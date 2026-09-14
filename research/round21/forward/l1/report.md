# L1 forward: a third observable exposes the hidden cubic

Frozen before reverse-L1 comparison. This goal was selected after the six I/J/K gates. Extend the **conditional** dynamics explicitly to

\[
m(x)=1+\zeta x+\xi p_3(x),\qquad p_3=x^3-3x/8,
\quad |\zeta|,|\xi|\le1/4,\quad c>0.
\]

The new xi is a dimensionless dynamics-deformation coefficient. It is not inferred from a static law or inserted into the lattice Hamiltonian. Exact rate inversion below assumes known kappa zero; the positivity and gap comparison separately cover absolute kappa at most 1/8.

## 1. Positive reversible extension

On `[-1,1]`, the conservative bound `|p3|<=11/8` gives

\[
m\ge1-1/4-11/32=13/32>0.
\tag{L1.1}
\]

The mobility is smooth and bounded above by `51/32`. Thus K1's closed-form construction applies with all hypotheses checked:

\[
A=-\rho^{-1}\operatorname{div}(\rho m\nabla),\qquad
q[f]=\int m|\nabla f|^2\rho\,d\mathrm{Haar}.
\]

It has H1 form domain, self-adjoint H2 operator domain, a unique constant zero mode, and stationary density rho. The additional drift is explicit:
`grad(m)=[zeta+xi(3x²-3/8)]grad(x)`. Retaining it also preserves the general unitary ground-transform identity of K1. Multiplying A by c gives physical energy units. Form comparison with the unchanged density and its action oscillation gives

\[
\Delta\ge{13\over32}{3c\over4}e^{-12|\kappa|}
\ge13c/192\qquad(|\kappa|\le1/8).
\tag{L1.2}
\]

The parameter box is a sufficient certificate. Outside it positivity can still hold, for example zeta one-half and xi zero gives mobility at least one-half. Failure to meet the box is not evidence of negative mobility.

## 2. Exact three-rate matrix at kappa zero

Use `f=x`, `g=x+x²/4`, and `h=x²+x³`. For each observable F,

\[
r_F=-\hbar C_F'(0+)
=c\int[1+\zeta x+\xi p_3(x)]\,G(x)[F'(x)]^2\,d\nu_0,
\quad G=(1-x^2)/4.
\]

Centering does not change the derivative. Haar odd moments vanish, while the even recurrence gives `E x²=1/4`, `E x⁴=1/8`, `E x⁶=5/64`, and `E x⁸=7/128`. Independent polynomial integration yields

\[
\begin{pmatrix}r_f\\r_g\\r_h\end{pmatrix}
=\underbrace{\begin{pmatrix}
3/16&0&0\\
25/128&1/32&0\\
59/256&9/64&9/512
\end{pmatrix}}_{M}
\begin{pmatrix}c\\c\zeta\\c\xi\end{pmatrix}.
\tag{L1.3}
\]

The new row follows from `(h')²=4x²+12x³+9x⁴`. Its odd cross term is what detects the odd cubic mobility. In particular

\[
\int p_3G(h')^2
=3\left[(\mathbb E x^6-\mathbb E x^8)
-\tfrac38(\mathbb E x^4-\mathbb E x^6)\right]=9/512.
\]

The first two rows retain the cubic blindness found by K2. The third responds by exactly `9c xi/512` relative to the xi-zero prediction at the same c,zeta.

## 3. Reconstruction and determinant coordinates

Triangularity gives

\[
\det M=27/262144>0,
\]

in the linear coordinates `(c,c*zeta,c*xi)`. The Jacobian in `(c,zeta,xi)` is `c² det(M)`, not merely det(M). The inverse is

\[
c={16r_f\over3},\qquad
\zeta={32r_g\over c}-{25\over4},\qquad
\xi={512r_h\over9c}-{118\over9}-8\zeta.
\tag{L1.4}
\]

Measured inputs would require c positive and a checked mobility domain after inversion. The present checker uses synthetic inputs only, including positive and negative zeta/xi and sufficient-box endpoints. It separately solves the rational matrix system and compares that result with the displayed inverse.

If the third observable is instead x², its derivative square is even. Its cubic coefficient is zero and the three-row determinant collapses. Omitting xi from the model leaves a nonzero third-rate residual whenever xi is nonzero; fitting the first two rates does not remove it. Conversely three fitted rates identify only this specified three-parameter family. Neither arbitrary mobility nor actual lattice dynamics is identified.

## 4. The polynomial is classical

The checked primary source [NIST DLMF 18.5.10](https://dlmf.nist.gov/18.5.E10) gives the finite Gegenbauer expansion. Substituting n=3 and lambda=2 yields the two terms

\[
C_3^{(2)}(x)={(2)_3\over3!}(2x)^3
-{(2)_2\over1!1!}(2x)=32x^3-12x,
\quad p_3=C_3^{(2)}/32.
\]

The checker performs the shifted-factorial substitution exactly. This polynomial is an established Gegenbauer polynomial, not a newly discovered universal equation. Its particular blind/detecting roles in the chosen observable rates are the model calculation here.

## 5. Scope and evidence

The derived rate matrix, inverse, synthetic recovery, drift expression, sufficient mobility/gap factors and failure controls are source-bound in the output manifest. The gap factor is a theorem for the declared positive conditional dynamics; the inverse is exact at kappa zero. Extending this three-rate inverse over nonzero kappa or arbitrary noise requires its own coefficient/rank/error analysis. c remains unmatched to alpha, and no physical time data were acquired. Scientific priority for the model application is unverified. L2 has not been executed.

```bash
python -B research/round21/forward/l1/check.py --output /tmp/ym21-forward-l1-replay
```
