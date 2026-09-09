## A causal Maxwell–Dirac closure that can actually be computed

The missing link in the previous investigation was the dynamical quantum current. A prescribed-field pair-production probability is not enough to evolve Maxwell's equations. The construction below supplies that current, a common energy subtraction, and a closed initial-value system in homogeneous flat spacetime with a constant magnetic field. It is a semiclassical matter-loop closure: the charged Dirac field is quantized and the electric field responds to its expectation value. Photon fluctuations, collisions and gravitational evolution are not included.

This is an independent derivation of a restricted research model, checked against established current-renormalization methods. Domcke, Ema and Mukaida distinguish particle transport, charge renormalization and finite Euler–Heisenberg response in a Landau-level formulation. Their treatment also explicitly neglects time variation of the cosmological scale factor when solving the displayed reduced modes. It therefore cannot simply be imported as the missing curved-spacetime closure. [@C01]

### 1. Conventions and degrees of freedom

Use Heaviside–Lorentz units, natural units and metric signature \((-+++ )\). Let \(e>0\) denote the magnitude of the renormalized charge and choose the positive-charge member of the charge-conjugate pair when defining the reduced one-particle Hamiltonian. Let

$$
s=mt,\quad a=eA_z/m,\quad x=eE/m^2,\quad b=|eB|/m^2,
\quad p=k-a,\quad M_n^2=1+2bn,\quad \omega_n=\sqrt{p^2+M_n^2}.
$$

Here \(m>0\) is the physical fermion mass, \(k\) the dimensionless canonical longitudinal momentum, \(B\) constant and spatially uniform, and a prime means \(d/ds\). Since \(E=-\dot A_z\), \(a'=-x\) and \(p'=x\). A constant magnetic field is consistent with the homogeneous Maxwell equations. Its support and its constant energy are treated as an external background; gravity would respond to its anisotropic stress and is a separate calculation.

For each Landau block,

$$
i y_{nk}'=h_{nk}y_{nk},\qquad
h_{nk}=M_n\sigma_1+p\sigma_3,\qquad y_{nk}^{\dagger}y_{nk}=1.
$$

With \(\boldsymbol r=y^{\dagger}\boldsymbol\sigma y\), this becomes

$$
r_1'=-2pr_2,\qquad r_2'=2(pr_1-M_nr_3),\qquad r_3'=2M_nr_2.
\tag{C1}
$$

The spin multiplicity is \(d_n=2-\delta_{n0}\). Write a sum-integral as

$$
\mathcal S_b[f]=\frac{b}{4\pi^2}\sum_{n=0}^{\infty}d_n
\int_{-\infty}^{\infty}dk\,f_{nk}.
\tag{C2}
$$

This counts one filled negative-energy state per block. A second factor of two for particles and antiparticles must not be appended: the excitation energy per block already equals \(2\omega f\), where

$$
f=\frac{1+\boldsymbol h\cdot\boldsymbol r/\omega}{2},
\qquad \boldsymbol h=(M_n,0,p).
$$

The mode density \(\mathcal S_b[f]\) is an instantaneous-basis pair diagnostic. At intermediate times it is basis-dependent and it must not replace the expectation value of the current.

### 2. The finite-regulator identity comes first

Temporarily replace (C2) by any finite set of fixed canonical momenta, Landau levels and positive quadrature weights. Define

$$
S=\mathcal S_b[r_3+p/\omega],\qquad
U=\mathcal S_b[\boldsymbol h\cdot\boldsymbol r+\omega].
\tag{C3}
$$

The added terms subtract the instantaneous magnetic-vacuum energy and current. Because the Bloch equation makes \(\boldsymbol h\cdot\boldsymbol r'=0\),

$$
(\boldsymbol h\cdot\boldsymbol r+\omega)'
=x(r_3+p/\omega),\qquad U'=xS.
\tag{C4}
$$

The physical unrenormalized excitation current is \(J_0=em^3S\). Maxwell's equation \(x'=-e^2S\) would exactly conserve \(x^2/2+e^2U\) at this finite regulator. This is a useful algebraic check; it does not make the three-dimensional continuum current finite.

To see why particle counting is insufficient, resolve the Bloch vector along \(\hat h\) and an orthogonal vector \(\hat t=(p,0,-M_n)/\omega\). If \(v=\boldsymbol r\cdot\hat t\), then

$$
r_3+p/\omega=2pf/\omega-M_nv/\omega.
\tag{C5}
$$

The second term contains coherent particle–antiparticle polarization. Dropping it generally spoils (C4), even when the occupation itself was obtained from the exact Dirac equation.

### 3. Deriving the subtraction from the same mode expansion

Expand the negative-energy solution in time derivatives of the background:

$$
\boldsymbol r^{(0)}=-\boldsymbol h/\omega,\qquad
\boldsymbol r^{(1)}=(0,-M_nx/(2\omega^3),0).
$$

The perpendicular part at the next order follows by solving
\(2\boldsymbol h\times\boldsymbol r^{(2)}=(\boldsymbol r^{(1)})'\).
The longitudinal part is fixed by \(|\boldsymbol r|^2=1\), rather than guessed. This gives

$$
c_{nk}\equiv r_3^{(2)}
=\frac{M_n^2x'}{4\omega^5}
-\frac{5M_n^2p x^2}{8\omega^7},
\qquad
u_{nk}^{(2)}=\frac{M_n^2x^2}{8\omega^5}.
\tag{C6}
$$

Direct differentiation, with \(\omega'=px/\omega\), proves

$$
(u_{nk}^{(2)})'=x c_{nk}.
\tag{C7}
$$

This is the essential compatibility check: the subtraction of current and energy is derived together. It would be inconsistent to subtract only a logarithm from the current while monitoring the unsubtracted matter energy as though it were the physical renormalized energy.

The recent Aleksandrov–Bokhan–Baksheev–Kudlis paper independently requires one common charge-renormalization constant for current and stress tensor and fixes its finite part by the zero-field on-shell condition. Its homogeneous-electric-field analysis uses both one-potential subtraction and a Pauli–Villars argument. It also shows that finite unrenormalized post-pulse observables do not establish finite intermediate-time observables. We use these as methodological cross-checks; that paper does not provide the constant-magnetic-field implementation below. [@C02]

### 4. Why a finite magnetic susceptibility must be restored

Subtracting (C6) for every Landau level removes not only the logarithmic ultraviolet term but the entire static linear magnetic-vacuum susceptibility. It is therefore an over-subtraction unless a physical finite matching condition is imposed. The matching can be derived rather than inserted arbitrarily.

Since

$$
\int_{-\infty}^{\infty}\frac{M_n^2\,dp}{4(p^2+M_n^2)^{5/2}}
=\frac{1}{3M_n^2},
$$

the static coefficient through Landau level \(N\), after taking the full longitudinal integral, is

$$
e^2 C_B(N)=\frac{e^2}{12\pi^2}
\left[b+\psi\!\left(N+1+\frac{1}{2b}\right)
-\psi\!\left(1+\frac{1}{2b}\right)\right].
\tag{C8}
$$

Here \(\psi\) is the digamma function. A zero-magnetic-field transverse continuum with the matched squared transverse cutoff \(2bN\) contributes

$$
e^2 C_0(N)=\frac{e^2}{12\pi^2}\ln(1+2bN).
$$

The finite difference is

$$
\chi_B=\lim_{N\to\infty}e^2[C_B(N)-C_0(N)]
=\frac{e^2}{12\pi^2}\left[
b-\ln(2b)-\psi\!\left(1+\frac{1}{2b}\right)\right].
\tag{C9}
$$

It agrees with the independently evaluated proper-time expression

$$
\chi_B=\frac{e^2}{12\pi^2}\int_0^{\infty}\frac{dt}{t}e^{-t}
\left[bt\coth(bt)-1\right].
\tag{C10}
$$

Consequently, adding back \(\chi_BE'\) to the physical current and \(\chi_BE^2/2\) to the matter energy restores the on-shell finite magnetic response. At infinite longitudinal range this is equivalent to subtracting the common zero-field charge counterterm. It is not an additional independently counted Euler–Heisenberg medium placed on top of the full unrenormalized response.

For weak \(b\), \(\chi_B=e^2b^2/(36\pi^2)+O(b^4)\), or \(\alpha b^2/(9\pi)\). This agrees with the parallel-field weak-response coefficient extracted from the Euler–Heisenberg action. The exact expression, rather than its weak-field expansion, is needed at large \(b\). The static matching is one-loop exact in the magnetic field; it does not claim all-loop accuracy.

### 5. Complete closed system at a specified regulator

For the chosen fixed quadrature define

$$
C=\mathcal S_b[M_n^2/(4\omega^5)],\qquad
D=\mathcal S_b[5M_n^2p/(8\omega^7)],\qquad
Z=1+\chi_B-e^2C.
\tag{C11}
$$

Let \(F(s)=-eJ_{\rm ext}/m^3\) denote a specified homogeneous external-current drive. Combining Maxwell's equation with the subtracted current gives the explicit ODEs

$$
\boxed{
 a'=-x,\qquad
 x'=\frac{F-e^2(S+Dx^2)}{Z},\qquad
 \boldsymbol r_{nk}'=2\boldsymbol h_{nk}\times\boldsymbol r_{nk}.
 }
\tag{C12}
$$

The dimensionless renormalized matter energy and total energy are

$$
\frac{\rho_{\rm matter}}{m^4}
=U-\frac{Cx^2}{2}+\frac{\chi_Bx^2}{2e^2},
\qquad
W\equiv\frac{e^2\rho_{\rm total}}{m^4}
=\frac{Zx^2}{2}+e^2U.
\tag{C13}
$$

The constant magnetic background energy has been omitted from the difference \(W(s)-W(s_0)\). Since

$$
C'=-2Dx,\qquad Z'=2e^2Dx,
$$

equations (C4) and (C12) yield the exact finite-regulator work identity

$$
\boxed{W'=xF.}\tag{C14}
$$

After the external drive ends, \(W\) is constant. The \(Dx^2\) term is necessary for this finite-window identity. It disappears after an infinite symmetric kinetic-momentum integration because its integrand is odd. Deleting it at finite canonical cutoff and then blaming an energy discrepancy on the ODE solver would be a logical error.

The raw form of (C12) exposes cancellations between ultraviolet polarization and charge subtraction. Require \(Z>0\) throughout the tested cutoff sequence and report its minimum. A small or negative \(Z\) signals an ill-conditioned regulator/charge description, not a newly discovered physical runaway. Continuum QED itself has a Landau-pole issue; extrapolating a one-loop numerical regulator arbitrarily far beyond its domain is not a meaningful numerical convergence exercise.

### 6. Initial state, gauge transformations and limits

Use a field that is exactly static before the start of the experiment:

$$
x(s_0)=0,\qquad a(s_0)=a_0,\qquad
\boldsymbol r_{nk}(s_0)=-\boldsymbol h_{nk}(s_0)/\omega_{nk}(s_0).
\tag{C15}
$$

Generate the electric field through a smooth external-current pulse. A convenient compactly supported \(C^{\infty}\) shape is

$$
F(s)=F_0\exp\!\left[4-\frac{1}{u(1-u)}\right],
\quad u=(s-s_0)/T,\quad 0<u<1,
$$

and zero elsewhere. All its derivatives vanish at the endpoints. The initial state is the exact vacuum in the smooth static magnetic background, and smooth time evolution avoids an artificial abrupt ultraviolet excitation. Finite adiabatic order and the full Hadamard condition are different statements; do not claim that a chosen finite-order approximate initial state is automatically Hadamard.

Starting with \(x(s_0)\ne0\) but setting every mode to the instantaneous negative-energy eigenstate omits the derivative corrections in (C6). This can generate initial-surface artifacts that grow with the cutoff. A vacuum-preparation error cannot be cured by reducing the ODE tolerance. Earlier self-consistent backreaction work explicitly discusses the role of adiabatic initial states and the inadequacy of particle number as a general intermediate-time observable. [@C03]

A residual constant gauge shift is \(a\mapsto a+c\), \(k\mapsto k+c\). It leaves \(p\), every weight and all equations invariant if the canonical grid is shifted with the state. Moving \(a\) while holding a finite canonical window fixed changes which physical modes are retained. That is a cutoff change, not a pure gauge comparison.

Two limits need separate tests: increase longitudinal window \(K\) at fixed transverse cutoff, and increase the Landau cutoff \(N\) with an appropriately large longitudinal range. A very large longitudinal cutoff with insufficient Landau levels remains effectively a reduced-dimensional model. Low occupation of high levels does not imply small vacuum-polarization contributions from those levels. The finite-grid identity (C14) holds before these limits and therefore cannot prove them.

Adiabatic order assignments become more restrictive when the metric also evolves. A common covariant stress/current renormalization must then reproduce the relevant anomaly and conservation identities. The flat-space derivation above does not license a substitution \(m\to ma(t)\) in its counterterms. [@C04]

### 7. Nontrivial analytic checks

**Zero drive.** Equations (C15) must remain stationary to numerical tolerance, and no pair diagnostic should grow.

**Weak finite-frequency response.** Linearizing the Bloch equations about the magnetic vacuum gives an independent frequency-domain comparator. With the convention \(e^{-i\nu s}\),

$$
\chi(B,\nu)=\chi_B+e^2\mathcal S_b\left[
\frac{M_n^2}{\omega_n^3}
\left(\frac{1}{4\omega_n^2-(\nu+i0)^2}
-\frac{1}{4\omega_n^2}\right)\right].
\tag{C16}
$$

The residual sum is convergent. Below \(|\nu|=2\), it is real; above the first threshold a causal imaginary part is possible. Replacing \(i0\) by a finite width changes the spectral problem and must be declared. Checking only (C9) against an input constant would be circular; comparing a small-amplitude time-domain experiment to (C16) tests the mode evolution and the finite-frequency polarization.

The small-frequency expansion gives

$$
\chi(B,\nu)-\chi_B
=\frac{e^2b\nu^2}{60\pi^2}
\left[1+\frac{\psi_1(1+1/(2b))}{2b^2}\right]+O(\nu^4),
\tag{C17}
$$

where \(\psi_1\) is the trigamma function. As \(b\to0\), this tends to \(e^2\nu^2/(60\pi^2)=\alpha\nu^2/(15\pi)\). This is a useful normalization check of the zero-field on-shell polarization.

**Massless lowest Landau level.** This is a distinct exactly solvable limiting model, not a substitution into the massive matching expression (C9). Choose an arbitrary fixed nonzero reference scale \(\mu\), and now define \(s=\mu t\), \(x=eE/\mu^2\), \(b=|eB|/\mu^2\), \(a=eA_z/\mu\), and \(\mathcal J=eJ_{\rm phys}/\mu^3\). No division by the vanishing fermion mass is implied. Retain only the gapless level. Then \(h=p\sigma_3\), and the filled state keeps \(r_3=-\operatorname{sgn}k\). If \(a_0=0\), the spectral-flow integral is

$$
\int dk\,[\operatorname{sgn}(k-a)-\operatorname{sgn}k]=-2a.
$$

Hence the dimensionless induced current obeys

$$
\mathcal J'=\Omega_B^2 x,\qquad
\Omega_B^2=\frac{e^2b}{2\pi^2},\qquad
x''+\Omega_B^2x=F'.
\tag{C18}
$$

This is the anomaly oscillator. A quadrature that smears the moving discontinuity may give a misleading massless test, so integrate the spectral-flow interval analytically or use an independent oscillator solver. The agreement of this special model with a fully quantum result does not establish massive mean-field accuracy.

### 8. What even perfect numerical convergence cannot establish

The expectation-value closure is nonlinear and causal, but it neglects electromagnetic quantum fluctuations and correlated scattering. Pla and collaborators constructed a linear-response validity diagnostic for semiclassical pair production in 1+1 dimensions and found problematic growth in a regime near the critical field for their tested setups. Their result is not a theorem that every constant-B 3+1 calculation fails near criticality; it is a reason to test perturbations and state the approximation. [@C05]

Gralla and Mizuno's fully quantum bosonized 1+1-dimensional calculation obtains a mass-dependent shift in the strong-field oscillation frequency which the usual semiclassical treatment misses at the same order. This is a concrete comparator against the idea that a conserved mean-field calculation has thereby solved quantum backreaction in full. It cannot be used by dimensional analogy to assign a numerical error bar to the present 3+1 Landau calculation. [@C06]

The honest deliverable is therefore a defined, testable Maxwell–Dirac mean-field problem with analytic charge matching, explicit initial state, independent frequency and anomaly checks, and demonstrated regulator convergence over the reported parameter range. A renormalized anisotropic stress tensor, a causal metric evolution and a validity study for stress/current fluctuations remain additional tasks before joining it to the gravitational meta-problem.
