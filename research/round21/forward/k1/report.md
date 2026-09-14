# K1 forward: mobility changes dynamics while preserving every static moment

Frozen before reverse-K1 comparison. This is the explicitly conditional `SU(2)^3` model from [F1](../../../round20/forward/f1/report.md) and [F2](../../../round20/forward/f2/report.md), not the physical lattice representation identified in J2. Keep known `|kappa|<=1/8`, product Casimir metric, `S=3x+y+z+w+t`, and `rho=exp(kappa S)/Z`. Introduce the dimensionless dynamics deformation `m=1+zeta x`, `|zeta|<1`, and independent positive energy coefficient c. No observed physical correlation data are supplied.

## 1. Divergence form and self-adjoint realization

On smooth functions define

\[
A_{\kappa,\zeta}=-\rho^{-1}\operatorname{div}(\rho m\nabla)
=-m\Delta-(\nabla m+\kappa m\nabla S)\cdot\nabla.
\tag{K1.1}
\]

Integration by parts on the compact manifold gives the nonnegative symmetric form

\[
q_{\kappa,\zeta}[f]=\int m|\nabla f|^2\rho\,d\mathrm{Haar}.
\]

Since `1-|zeta|<=m<=1+|zeta|`, its closed form domain is H1, with equivalent weighted norm. Smooth strict ellipticity gives the self-adjoint operator with H2 domain. The closed form is Markovian. Constants form the unique kernel: vanishing energy forces zero gradient and hence a constant by connectedness. Set `H=c A`; physical imaginary time uses `exp(-t H/hbar)`.

The term `grad(m)` is essential. At kappa zero, the wrong operator `-m Delta` has `E_Haar[A_wrong x]=3zeta/16`, which is nonzero when zeta is nonzero. The correct divergence drift contributes `-zeta E[(1-x²)/4]=-3zeta/16`, restoring stationarity. At `|zeta|=1` uniform ellipticity is lost; at larger absolute zeta, m is negative somewhere. These cases are outside the stated theorem.

## 2. The full ground-state transform

Multiplication by `sqrt(rho)` is unitary from weighted to Haar L2. Direct differentiation yields

\[
\widetilde H=c\left[-\operatorname{div}(m\nabla)
 +{\kappa\over2}\operatorname{div}(m\nabla S)
 +{\kappa^2\over4}m\Gamma(S)\right],
\tag{K1.2}
\]

with ground `sqrt(rho)`. The kinetic term divided by this ground is the negative of the displayed potential, so cancellation is exact. In particular

\[
\operatorname{div}(m\nabla S)=m\Delta S+\zeta\Gamma(x,S),\qquad
\Gamma(x,S)={3+y-3x^2-xw\over4}.
\]

Retain the F2 shared-link expressions

\[
\Delta S=-\tfrac34(3x+y+z+2w+2t),
\quad
\Gamma(S)={15+8y+2x+2z+2r-(3x+w)^2-(y+w+t)^2-(z+t)^2\over4},
\]

where `r=Tr(UW†)/2` is a derived observable, not an added action term. The square involving the common middle link includes `(r-wt)/2`; replacing that link by independent copies changes the model. At `u=q=(0,1,0,0), v=(1,0,0,0)`, the checker derives `Gamma(S)=6`, `Gamma(x,S)=1`, and `Delta S=-3/4` from tangent projections. Removing either the mobility-divergence contribution or the shared derivative gives a nonzero ground-state residual.

## 3. Gap, units and static nonidentifiability

Form comparison gives `q_kappa,zeta >= (1-|zeta|)q_kappa,0`. F2's exact action oscillation is 12 and its Haar Casimir gap is 3/4. Therefore

\[
\Delta\ge{3c\over4}(1-|\zeta|)e^{-12|\kappa|}
\ge {c(1-|\zeta|)\over6}.
\tag{K1.3}
\]

The last rational bound uses the inherited enclosure `exp(3/2)<9/2`. It holds for the chosen reversible dynamics. `c/E_star` and the lattice coefficient `alpha/E_star` are distinct until matched; kappa and zeta are dimensionless. All c,zeta have exactly the same normalized stationary density rho, so every static moment is independent of these two dynamic parameters.

For a nonconstant real form-domain observable f, the centered stationary imaginary-time correlator satisfies

\[
r_f:=-\hbar C_f'(0+)=c q_{\kappa,\zeta}[f].
\tag{K1.4}
\]

A constant observable has zero Dirichlet form and supplies no calibration. The formula is an inverse relation only when an independent physical-time slope is available. No such slope was measured here.

## 4. Exact two-rate reconstruction at known kappa zero

For the Haar coordinate x, `Gamma(x)=(1-x²)/4`, odd moments vanish, `E[x²]=1/4`, and `E[x⁴]=1/8`. The exact moment recurrence is `E[x^(2n)]=(2n-1)E[x^(2n-2)]/(2n+2)`. For `f=x` and `g=x+x²`, centering does not affect gradients. Polynomial integration gives

\[
r_f={3c\over16},\qquad
r_g=c\left({5\over16}+{\zeta\over8}\right).
\tag{K1.5}
\]

The matrix in the **linear variables `(c,c*zeta)`** is

\[
\begin{pmatrix}3/16&0\\5/16&1/8\end{pmatrix},
\quad\det=3/128.
\]

The Jacobian with respect to `(c,zeta)` instead has determinant `3c/128`. For admissible rates,

\[
c={16r_f\over3},\qquad
\zeta={8r_g\over c}-{5\over2},
\quad r_f>0,\quad 1<r_g/r_f<7/3.
\tag{K1.6}
\]

These inequalities exactly encode c positive and absolute zeta below one. Synthetic `c=2`, `zeta=1/2` gives rates `(3/8,3/4)` and reconstructs the inputs; it is not experimental data.

The alternative pair `x,x²` is parity-degenerate: its rates are `3c/16,c/8`, both independent of zeta. Its two-column matrix has rank one, so two slopes do not identify two parameters merely because there are two observables. For nonzero known kappa the general rate coefficients require their actual weighted moments; the Haar inverse above is not asserted there.

## 5. A necessary matching obstruction

In these same coordinates, a multiplication ground-state conjugacy changes first- and zeroth-order terms but leaves the second-order principal symbol unchanged. The transformed operator has principal symbol `c(1+zeta x)|xi|²` in the declared Casimir metric. A constant-mobility rotor with matched coordinates has symbol `alpha|xi|²`. Equality at both x=1 and x=-1 requires zeta zero and the corresponding constant kinetic normalization to match. Thus nonconstant mobility cannot be identified with that rotor by this limited conjugacy.

This is only a necessary test. Even zeta zero does not identify the potentials, state spaces, domains, or observables. No reduction from the infinite lattice to this conditional three-link system has been established. The mobility is explicitly a dynamics deformation; equal static distributions do not make it the original Yang–Mills dynamics.

## 6. Evidence and remaining task

The standard-library checker integrates the rate polynomials exactly, verifies rank and synthetic inverses, checks tangent derivative and ground-transform residuals, and rejects the missing drift, invalid mobility, zero-form observable and false principal-symbol match. The new project contribution is this concrete model discrimination and parameter map, with scientific priority unverified. Divergence forms, ground transforms and principal symbols are established tools. The conditioning of the inverse and nonzero-kappa identification are separate next questions; K2 was not executed.

```bash
python -B research/round21/forward/k1/check.py --output /tmp/ym21-forward-k1-replay
```
