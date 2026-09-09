# Causal quantum backreaction: a critical reconstruction

**Independent research report, third corrective cycle. Research cutoff: 9 September 2026.**

This investigation now computes a quantum current that changes the electric field, instead of stopping at particle creation in an imposed field. The selected calculation quantizes a massive Dirac field in a homogeneous, constant magnetic background and evolves Maxwell's electric field with its expectation-value current. A shared subtraction and a finite physical charge-matching condition preserve both the magnetic vacuum response and the energy/work identity. The result is a tested finite-regulator mean-field solution. It is not a solution of the full Einstein–QED problem or a discovery that resolves any of the four original open research fronts.

The principal executed experiment uses $B/B_c=10$, a smooth external-current pump of duration $4/m_e$, and a bare-Maxwell target $E/E_c=1$. After the pump ends, the electric field evolves from the quantum current. It reverses sign and reaches approximately $E/E_c=-0.03757$ at $m_et=50$. The final momentum refinement changes the sampled field history by $3.26\times10^{-9}$; the separate Landau-cutoff comparison changes the endpoint by $5.06\times10^{-8}$. These are measured numerical comparisons within the stated model, not rigorous continuum or physical error bounds.

An independent complex-spinor implementation agrees with the production Bloch-vector implementation on a deliberately small identical regulator. Separate exact solutions, deliberately defective controls and a fully quantum one-dimensional comparator test assumptions that conservation alone cannot test. The gravitational analysis supplies a compatible anisotropic interface and a verified classical constraint fixture; its covariantly renormalized quantum stresses and metric feedback remain unfinished.

## What was actually wrong, incomplete, or misleading

The previous artifact already disclosed several limitations. This audit preserves those disclosures and does not invent a contradiction merely because the result was rejected. It distinguishes five types of issue: an invalid mathematical implication, a physically incomplete model, a coding defect, an unresolved numerical limit and an unsupported interpretation.

| Issue | Evidence and correction | Present status |
|---|---|---|
| Backreaction was missing | Prescribed-field occupations supplied no evolved quantum source for Maxwell | Current and electric field now evolve together in flat homogeneous geometry |
| Excellent energy conservation concealed quadrature error | The 1024-to-2048 momentum refinement shifted the late field by about $1.12\times10^{-5}$ despite tiny work residual | A fixed-window 4096-node run reduces the observed field-history change to $3.26\times10^{-9}$ |
| Subtraction could erase physical magnetic response | Removing the full adiabatic current also removes a finite magnetic susceptibility | Restore the on-shell susceptibility exactly once; weak-drive controls discriminate its omission |
| Relative energy error had an unphysical denominator | Normalizing by the larger of one and the energy hid errors in weak experiments | Use the measured physical energy/work scale and report absolute error separately |
| Current subtraction lost avoidable digits | Adding two already-summed large quantities amplified cancellation | Sum the subtracted mode integrand before reduction |
| A current label was too strong | The Maxwell numerator omitted the polarization moved onto its left side | Report the numerator and the full reconstructed matter current separately |
| Small intersolver disagreement was not an accuracy certificate | Related methods shared precision, endpoint and state assumptions | Add exact Sauter references, stable overlaps and independent endpoint tests |
| The expansion-only benchmark had an unrecognized exact reduction | A constant unitary turns it into a known Sauter two-state transition | Retain it as a benchmark, not an analytically unsolved discovery |
| A provisional constraint-propagation coefficient was wrong | Direct Einstein-tensor differentiation gives one factor of the volume expansion rate | Correct it and retain the symbolic countercheck |
| The full stress was absent | One energy density does not determine two directional pressures | Derive the anisotropic interface; do not insert energy alone into Einstein's equations |

## What the advisor and panel did

The advisor assigned distinct reviews of current renormalization, implementation, independent verification, gravitational consistency and empirical/source criticism. The coding task used a lower-cost model after the equation contract was fixed. These are functional AI review roles; no named human physicist is represented as having endorsed the work. The lead researcher reviewed the interfaces and the advisor rejected the initial convergence claim before accepting the refined result.

The decisive debate was about what would falsify the model. A finite grid can conserve energy with an incorrectly matched susceptibility. A normalized quantum state can have the wrong transition probability. An energy-conserving semiclassical trajectory can omit a real quantum correction. A patent or government project can contain an invalid equation. Each objection below therefore has an analytic comparator, executed numerical control, or explicit experiment required to resolve it.

This report provides reproducible derivations, assumptions, decision records and verification results. Its source ledger records sections actually inspected, abstract-only leads and access failures separately. The search extends to government laboratories, primary criticism, author repositories and patent texts, but is not an exhaustive inventory of every country or all existing literature. Complete books and third-party papers are linked rather than reproduced.



## The target as an initial-value problem

Use four spacetime dimensions, metric signature (-+++), rationalized electromagnetic units, and hbar=c=1. The reduced Planck mass is defined by Mpl²=(8 pi G)^(-1). Let e>0 be the magnitude of the electron charge; the signed charge must be assigned consistently in the covariant derivative and current. Define the invariant electromagnetic scalars

$$
\mathcal F=\frac14F_{\mu\nu}F^{\mu\nu}=\frac{B^2-E^2}{2},\qquad
\mathcal G=\frac14F_{\mu\nu}\widetilde F^{\mu\nu}.
$$

The sign of G depends on the dual convention; the parity-even G² term does not. The actual physical target includes regions with E/Ec of order one, B/Bc much larger than one, and possibly electron-scale curvature. Specify a metric, electromagnetic field, supporting matter and quantum state on an initial slice; solve their constraints. An externally imposed dipole does not supply its own material stress tensor. A monopole and a dipole have different topology and symmetry.

For the displayed Dirac operator with signature $(-+++)$, choose $\{\gamma^\mu,\gamma^\nu\}=-2g^{\mu\nu}$ and $D_\mu=\nabla^{\rm spin}_\mu-ieA_\mu$. This choice reproduces the positive-charge reduced Hamiltonian with kinetic momentum $k-eA_z$. The retarded kernels below include the invariant integration density in their second argument, so the displayed $d^4y$ denotes the density-weighted kernel convention.

### Local terms and their status

An organizing action before integrating out the electron is

$$
S=\int d^4x\sqrt{-g}\,[\mathcal L_0+\mathcal L_{\rm ct}+\mathcal L_{\rm UV}]+S_{\rm support},
$$
$$
\mathcal L_0=\frac{M_{\rm Pl}^2}{2}R-\frac14 Z(\phi)F^2
-\frac12G_{ij}(\phi)\nabla_\mu\phi^i\nabla^\mu\phi^j-V(\phi)
-\frac14\theta(\phi)F\widetilde F+\bar\psi(i\gamma^\mu D_\mu-m(\phi))\psi.
$$
$$
\mathcal L_{\rm ct}=c_1R^2+c_2R_{\mu\nu}R^{\mu\nu}
+c_3R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}.
$$
Representative higher-dimension terms include

$$
\mathcal L_{\rm UV}=\frac{a_1RF^2+a_2R_{\mu\nu}F^{\mu\rho}F^\nu{}_{\rho}
+a_3R_{\mu\nu\rho\sigma}F^{\mu\nu}F^{\rho\sigma}
+a_4(\nabla_\mu F^{\mu\nu})(\nabla^\rho F_{\rho\nu})}{\Lambda_*^2}
+\frac{b_1(F^2)^2+b_2(F\widetilde F)^2}{\Lambda_*^4}+\cdots.
$$

This is an operator inventory. The coefficients need a specified matching prescription, and the basis has redundancies. In four dimensions a constant Euler-density combination is topological in the bulk; a constant theta term is locally topological, with boundary and magnetic-charge qualifications. Scalar-dependent coefficients change those statements. Scalar-gradient terms of the same order cannot be dropped when their power counting makes them relevant. The electron contribution must be integrated out once: adding its full determinant and its Euler-Heisenberg expansion independently double-counts the same loop.

### Causal closure and the part now computed

After integrating out matter, the real-time functional depends on two histories and an initial density operator rho0:

$$
\Gamma_{\rm CTP}=S_b[g_+,A_+,\phi_+]-S_b[g_-,A_-,\phi_-]
+\Gamma_\psi[g_+,A_+,\phi_+;g_-,A_-,\phi_-;\rho_0].
$$

Here Sb excludes the integrated-out matter and duplicate matched terms. The physical equations are obtained by varying one branch and only then identifying the branches. A compact formal system is

$$
\left.\frac{\delta\Gamma_{\rm CTP}}{\delta A_{+\mu}}\right|_{+=-}=0,\qquad
\left.\frac{\delta\Gamma_{\rm CTP}}{\delta g_+^{\mu\nu}}\right|_{+=-}=0,\qquad
\left.\frac{\delta\Gamma_{\rm CTP}}{\delta\phi_+^i}\right|_{+=-}=0.
$$

These equations are exact formal definitions within the chosen semiclassical functional, not a numerical closure. One must compute the state-dependent two-point function, subtract its local singularity covariantly, match the finite counterterms, and establish a causal response. For a consistently defined physical current, matter exchanges energy-momentum with electromagnetism through the Lorentz force; total stress and charge obey their Ward identities. Varying an in-out effective action or inserting a local pair count does not accomplish this.

The nonlinear feedback is not one magical extra monomial. A mixed curvature-field term contributes locally, but the causal loop also contains

$$
\delta\langle j^\mu(x)\rangle=
\int d^4y\,[\Pi_{\rm ret}^{\mu\nu}(x,y)\delta A_\nu(y)
+K_{\rm ret}^{\mu\alpha\beta}(x,y)\delta g_{\alpha\beta}(y)]
+\delta_{\rho_0}\langle j^\mu(x)\rangle.
$$

The metric response changes the current, that current changes the field, and field plus quantum stress change the metric. Boundary conditions and state variations enter this response. The fully strong-curvature current/stress kernels remain unresolved. The following homogeneous flat-space model now computes a restricted causal electromagnetic response and backreaction, with the metric held fixed. Linear-response and stress-fluctuation analyses are part of checking the semiclassical approximation, separately from the electron derivative expansion. [@H07; @H06]

### Scale and geometry checks before any numerical run

| Check | Required distinction | Falsifying example |
|---|---|---|
| Electron expansion | Curvature/me² and gradients/me | A background with radius of order an electron Compton wavelength defeats a local curvature truncation |
| Gravitational loop expansion | G times curvature | Curvature of order me² can still give G me² approximately 1.75e-45; it is not automatically Planckian |
| Curvature invariant | Ricci scalar versus Riemann tensor | Classical RN has R=0 but nonzero Kretschmann invariant |
| Field strength | Lab E,B versus invariant electric component | A plane wave can have large E and B but both field invariants vanish |
| Ray geometry | Transverse magnetic component | A radial ray through a radial monopole has zero leading transverse mixing |
| State | In-vacuum, thermal state, incoming flux | The same metric and field support different renormalized currents |
| Boundary family | Infinity versus cosmological horizon | de Sitter static-patch data cannot be replaced by asymptotically flat infinity |

The four original research fronts remain active. The following theory and numerical chapters close a restricted electromagnetic loop; the gravity chapter states the additional stress and state dependencies needed for the full system.


## Four research fronts: equations, assumptions and remaining tests

The four fronts share quantum matter, gauge fields and gravity, but do not describe one interchangeable background. A flat homogeneous pair plasma has no Cauchy horizon. A spherical magnetic monopole is not a stellar dipole. A de Sitter static patch has a cosmological horizon rather than asymptotically flat infinity. These distinctions determine which partial solutions can be combined.

### Festina Lente, weak gravity and charged black-hole discharge

For a canonically normalized photon, integer charge $n$, gauge coupling $g$ and reduced Planck mass, the simple electric WGC normalization is

$$m^2\leq 2g^2n^2M_{\rm Pl}^2.$$

It proposes an appropriate superextremal state under specified assumptions. It does not assert that every charged species obeys a dimensionful $q/m\geq1$. The magnetic argument suggests an effective cutoff of order $gM_{\rm Pl}$; it is not a second particle charge-to-mass inequality. With massless scalars, a same-species repulsive-force criterion instead involves

$$g^2n^2\geq \frac{m^2}{2M_{\rm Pl}^2}+G^{ij}\partial_i m\partial_jm.$$

Long-range force balance and black-hole superextremality need not be identical with moduli. Scalar masses, screening and field-dependent gauge normalization modify the comparison. These conjectural statements must be distinguished from a measured spectrum or an existence theorem. [@G01; @R222]

A sharpened Festina Lente version used in the prior analysis is

$$m^4\gtrsim6g^2n^2M_{\rm Pl}^2H^2.$$

Its coefficient and scope belong to the adopted de Sitter discharge argument. Combining it with the preceding electric condition yields a possible mass window only if $g|n|\gtrsim\sqrt{3/2}\,H/M_{\rm Pl}$ in this normalization. An algebraic overlap does not establish the actual fate of a charged horizon. Decay channels require a physical energy, spectrum, quantum state and conservation of charge and energy including the emitted shell. Near-extremal and near-Nariai limits must not be interchanged without checking their horizons. [@G02; @G04]

The reference metric is

$$ds^2=-f(r)dt^2+f(r)^{-1}dr^2+r^2d\Omega^2,$$
$$f(r)=1-\frac{2GM}{r}+\frac{GQ^2}{4\pi r^2}-H^2r^2.$$

For $H=0$, $f\to1$ at spatial infinity. For $H>0$, the static exterior is between its black-hole and cosmological horizons. A double root signals degeneracy and invalidates an ordinary root shift proportional to $1/f'$. Recent nonequilibrium discharge/evaporation work reinforces the need to evolve mass and charge rather than infer the whole trajectory from a local pair exponent. The earlier uniform root calculation remains a restricted geometric benchmark. The present flat backreaction run does not test the WGC or prove/disprove Festina Lente. [@G14; @R228]

**Next discriminating calculation.** Fix one charged de Sitter geometry, state and charged-matter spectrum; derive renormalized horizon fluxes or a controlled reduction; evolve mass and charge with the corresponding stress flux and test the horizon discriminant. Compare any rate approximation with the causal mode result in a shared regime before inferring a decay endpoint. A dipolar field and arbitrary light moduli should enter only after that closed reference problem works.

### Nonperturbative pair creation in magnetized curved space

The physical electron critical fields are $E_c=m_e^2/e$ and $B_c=m_e^2/e$ in natural units; $B_c\simeq4.41\times10^{13}$ gauss. Magnetic field strength, electric invariant strength, derivatives and curvature are separate expansion parameters. In constant parallel fields, the spinor vacuum-persistence density has the benchmark form

$$2\,\operatorname{Im}\mathcal L^{(1)}=
\frac{e^2|EB|}{4\pi^2}\sum_{\ell=1}^{\infty}
\frac{1}{\ell}\coth\!\left(\frac{\ell\pi |B|}{|E|}\right)
e^{-\ell\pi m^2/|eE|}.$$

This is not a local causal current and is not generally the mean pair count. A uniform static magnetic field alone does not create charged pairs from a stable vacuum. A strong plane wave can have vanishing local electromagnetic invariants; intensity alone does not justify a constant-electric Schwinger formula. Time dependence, photon-initiated processes and spatial geometry require their own calculation. [@FT01; @RT06; @RT08]

The quartic Euler–Heisenberg expression

$$\mathcal L^{(4)}=\frac{2\alpha^2}{45m^4}
\left[(E^2-B^2)^2+7(\mathbf E\cdot\mathbf B)^2\right]$$

is a weak-field expansion. The magnetic susceptibility used in the executed model instead keeps its one-loop magnetic-field dependence unexpanded. This does not resum arbitrary gravitational derivatives, photon loops or strong-curvature nonlocality. Curved-space proper-time and heat-kernel results can organize amplitudes while retaining restrictions on curvature or gradients; labels such as “nonperturbative” must identify the parameter being resummed. [@FT02; @FT06; @FT07]

When a curvature scale is of order $m_e^2$, the local electron curvature expansion is not controlled even though $Gm_e^2$ is extremely small. Conversely classical Reissner–Nordstrom has $R=0$ while its Riemann tensor is nonzero: using only the Ricci scalar can miss the problem entirely. For physical electron fields $E/E_c=1$, $B/B_c=100$, their own gravitational source scale is about $2.40\times10^{-39}m_e^2$. Electron-scale curvature therefore requires another gravitating source or imposed geometry; it does not follow from those electromagnetic fields alone.

**Executed advance.** The following mode system supplies a causal electric current with magnetic Landau levels and finite charge matching. **Next dependency.** Evolve the anisotropic quantum current, energy and both pressures with common covariant subtractions before coupling to the metric. Adding a real local Euler–Heisenberg action to a separately counted full electron determinant would duplicate the loop.

### Mass inflation, evaporation and the Cauchy horizon

In spherical symmetry a useful double-null ansatz is

$$ds^2=-\Omega^2(u,v)du\,dv+r(u,v)^2d\Omega_2^2,$$
$$1-\frac{2Gm(u,v)}r+\frac{GQ(u,v)^2}{4\pi r^2}
-\frac{\Lambda r^2}{3}=-\frac{4r_u r_v}{\Omega^2}.$$

Counterstreaming fluxes can blueshift at the inner horizon and make the mass aspect grow while the areal radius remains finite. The outcome depends on tail decay, charge evolution, quantum state and the strength of the chosen extension criterion. A divergent mass function, an inextendible continuous metric, an inextendible twice-differentiable metric and failed weak-solution continuation are different assertions. Classical results for rough data and semiclassical horizon singularities test different hypotheses. [@G03; @R227; @H09]

Quantum renormalized stress can violate pointwise classical energy conditions. That does not prove desingularization: quantum energy inequalities and semiclassical singularity theorems can impose different restrictions. A four-dimensional scalar reduction also contains the areal-radius/dilaton coupling and backscatter; a purely two-dimensional Polyakov flux cannot be called the full four-dimensional stress merely by dividing by area. State functions and finite counterterms matter at a horizon. [@G06; @G07; @H10]

The previous project checked a reduced system's identities and a principal-coefficient degeneracy; it did not evolve a quantum inner horizon to a validated endpoint. This round adds a constraint-propagation methodology and explains exactly why an energy-only source cannot complete that evolution. Near-extremal quantum corrections and nonperturbative evaporation analyses provide comparators, but their boundary conditions and approximation domains must be matched before combining their claims. [@G08; @G09; @G10; @G11; @G12]

**Next discriminating calculation.** Specify double-null characteristic data, renormalized null fluxes and a charge-current model; monitor both constraints, state regularity and curvature in horizon-regular coordinates. Repeat with the full reduced matter potential before attributing a bounce or singularity avoidance to quantum gravity. Stop a continuum claim when subtraction or curvature control fails; do not continue numerically through that failure and label the graph a resolved spacetime.

### Quantum-corrected Gertsenshtein conversion

For a constant, lossless two-mode propagation matrix, with $\delta=\omega(n_\gamma-n_g)$ and $\mu=B_T/(\sqrt2M_{\rm Pl})$ in the stated normalization,

$$P_{\gamma\to g}(L)=\frac{4\mu^2}{\delta^2+4\mu^2}
\sin^2\!\left[\frac L2\sqrt{\delta^2+4\mu^2}\right].$$

Large mismatch caps conversion for this matrix. It is not a no-conversion theorem for every plasma, inhomogeneous field or resonant crossing. A radial ray in a radial monopole has $B_T=0$ at leading order. Dipolar rays, polarization rotation, absorption and varying plasma density require a transfer problem. A zero mismatch helps only if the crossing remains coherent and the flux-normalized modes and mixed vertex are consistent. [@G13; @R229]

A newly inspected August 2026 paper keeps a one-loop magnetic response unexpanded and studies magnetar polarization transport. Its low-frequency approximation, algebraic treatment of loop corrections and separation between inner magnetosphere and polarization freeze-out are essential. A formal maximum near $17B_c$ from products of one-loop terms is not a controlled all-orders QED prediction. A large local index correction need not strongly change polarization frozen farther out in weaker fields. No publicly accessible solver was established here, and the project did not reproduce that transport calculation. [@N03]

Our static parallel susceptibility is not either transverse photon's full momentum-dependent refractive index. It cannot be inserted alone into the photon–graviton matrix. **Next calculation:** construct the transverse polarization eigenmodes and mixed kernel in a shared loop approximation, validate the classical constant-field limit, then evolve a ray with an explicit magnetic/plasma profile and absorption. Compare observed Stokes parameters or converted energy flux, rather than treating an index shift as an observed gravitational signal.



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

Adiabatic order assignments become more restrictive when the metric also evolves. A common covariant stress/current renormalization must then reproduce the relevant anomaly and conservation identities. The flat-space derivation above does not license a substitution \(m\to ma(t)\) in its counterterms. [@N02]

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


## Executed causal calculation and its numerical limits

### Model, pump and measurement

The theory chapter calls the mode-current sum $S$ and the finite-window derivative coefficient $D$. The code calls these `J0` and `S`, respectively. This notation map matters: the code's `Sx2` is the theory's $Dx^2$. Define the effective numerator $Q=S+Dx^2$. It is not by itself the full physical renormalized current. In the theory's dimensionless matter-current units,

$$\mathcal J=\frac{j_{\rm matter}}{em^3}
=Q-Cx'+\frac{\chi_B}{e^2}x'
=\frac{F-x'}{e^2},\qquad x'=\frac{F-e^2Q}{Z}.$$

Moving polarization onto the Maxwell left side changes the named source, not the physical solution. The delivered refinement metadata records both $Q$ and $\mathcal J$. A previous draft called $Q$ the physical current; the theory reviewer and lead researcher independently caught this labeling error. The differential system and solver source did not change.

The executed pump is normalized by its integral:

$$F(s)=\frac{x_{\rm target}}{T_p I}
\exp\!\left[-\frac{1}{u(1-u)}\right],\quad
u=s/T_p\in(0,1),$$
$$I=\int_0^1\exp[-1/(u(1-u))]du,$$

and $F=0$ outside that interval. Thus $x_{\rm target}$ is the electric field an empty classical Maxwell system would acquire, not the actual peak in the responding vacuum. The first and last derivatives of every finite order vanish at the pump endpoints. Initially $x=a=0$ and all modes occupy the magnetic negative-energy state.

Production parameters are $b=10$, $T_p=4$, $x_{\rm target}=1$, $s_f=50$, Landau levels $0$ through $8$, canonical window $[-40,40]$ and 4096 Gauss–Legendre nodes per level. There are 36,864 Bloch modes. DOP853 uses relative tolerance $2\times10^{-10}$, absolute tolerance $2\times10^{-12}$ and maximum step $0.05$. The recorded history has 251 equally spaced times; a sampled maximum is not a continuous-time extremum.

### Results that survive the advisor's convergence challenge

| Quantity | Measured value | Interpretation |
|---|---:|---|
| Final field $x(50)$ | -0.037571642494 | Report approximately -0.03757 for this model |
| Final potential $a(50)$ | -26.5864064568 | Residual gauge convention $a(0)=0$ |
| Sampled maximum absolute field | 0.9893066812 | Sampling at intervals 0.2 misses the exact peak |
| Minimum effective coefficient $Z$ | 0.9960199826 | No ill-conditioned denominator on this trajectory |
| Maximum absolute energy/work residual | $5.89\times10^{-12}$ | Finite-grid conservation diagnostic |
| Physical energy/work scale | 0.4978069367 | Actual denominator used for relative error |
| Maximum relative energy/work residual | $1.18\times10^{-11}$ | Does not bound quadrature or model error |
| Maximum raw Bloch norm defect | $2.94\times10^{-8}$ | Reported without renormalizing trajectories |
| Final raw occupation range | about $-1.6\times10^{-15}$ to 0.04934 | Tiny negative floor is numerical; output is not clipped |

The source vanishes for $s\geq4$. Field reversal at late time is therefore an actual consequence of the computed matter current in this model, rather than an imposed reversal of the external electric profile. The background magnetic energy is constant and omitted from the energy *difference*; the pump supplies the changing system's energy. This observation does not imply energy extraction from an unprepared vacuum.

| Numerical axis | Comparison | Observed change |
|---|---|---:|
| Longitudinal quadrature, coarse | 1024 to 2048 nodes, fixed $K=40$, $n_{\max}=8$ | Endpoint $1.115\times10^{-5}$: initially unresolved |
| Longitudinal quadrature, refined | 2048 to 4096 nodes, same bounds | Maximum sampled field-history difference $3.257\times10^{-9}$ |
| Full matter current | Same fixed-window refinement | Maximum $|\Delta\mathcal J|=1.1315\times10^{-6}$ |
| Effective numerator source | Same fixed-window refinement | Maximum $|\Delta Q|=1.1270\times10^{-6}$ |
| Momentum window | $K=40$, 2048 nodes to $K=60$, 3072 nodes | Endpoint difference $4.107\times10^{-11}$ |
| Landau truncation | Levels through 8 to levels through 12, $K=40$, 2048 nodes | Endpoint difference $5.061\times10^{-8}$ |

The window comparison approximately preserves central node spacing; it cannot replace refinement at fixed window. That was the advisor's reason to require the 4096-node run. The largest recorded endpoint change among the final component tests is the Landau shift. No rigorous tail bound or simultaneous all-observable continuum extrapolation has been established. Full-current convergence is weaker than field convergence, because the field integrates a rapidly varying source. The raw mode current alone is regulator-dependent and cannot substitute for $\mathcal J$.

The initial 256-node result, $x(50)\simeq-0.03743286$, is superseded. Historical short-time scans and deliberately wrong controls remain in the package as audit evidence; their filenames do not designate accepted production results. `production_baseline.json` and `production_baseline.csv` identify the final 4096-node data. The earlier file named `production_baseline_converged` is an intermediate window check, not a stronger certificate.

### A physical matching test that conservation cannot fake

For $b=100$, $x_{\rm target}=0.01$, pump duration 20 and final time 40, the static linear prediction is $x_{\rm target}/(1+\chi_B)=0.00931301998$. The late-time mean averages the final 50 of 401 stored points, spanning $s=35.1$ through $40$. These control runs use maximum ODE step 0.08. The mean does not assert an exact stationary field.

| Prescription | Measured late mean | What it tests |
|---|---:|---|
| Matched physical susceptibility | 0.00931301064 | Finite response retained once |
| Subtraction with finite matching omitted | 0.00999998497 | Incorrectly erases nearly all static magnetic response |
| Sign-reversed finite matching | 0.01079637896 | Deliberately wrong finite response |
| Unrenormalized finite-cutoff model | 0.00926614690 | Different cutoff-dependent prescription |

The matched late mean differs from the static prediction by about $9.33\times10^{-9}$ in this finite-duration test. Its true relative work residual is $3.63\times10^{-9}$ at energy scale $4.66\times10^{-5}$. The omitted-matching model also conserves its own consistently defined energy very closely, while yielding the wrong physical static response. This is the central counterexample to treating conservation as sufficient validation.

### Independent checks and a retained failure

The separate verifier implements complex spinors, not production Bloch vectors, with no production import. On the shared small grid its sampled field and potential differ from production by at most $3.63\times10^{-12}$ and $4.62\times10^{-12}$. Exact spectra, boundary shifts, gauge-window changes and deliberately broken vacuum subtraction supply additional tests described next.

The advisor's independent high-precision Sauter formula identifies the prior expansion-only benchmark exactly. Its strictest double-precision target, absolute error below $10^{-18}$, **failed** at about $1.82\times10^{-18}$. That failed gate remains in `advisor_checks.json`. It concerns a benchmark precision target, not the larger-scale field reversal, but it prevents a blanket statement that every requested accuracy test passed.


## Independent verification: what the numerical checks establish

This review separates a wrong physical model, a wrong implementation and an overstated accuracy claim. They require different corrections. The previous report already stated that its 2.14e-16 agreement was not a sixteen-digit physical result, and already classified the smallest strong-field occupations as unresolved. Those qualifications were correct. This round adds an exact reference, more informative error measures and an independently implemented backreaction check. It does not manufacture an error merely because the previous answer was rejected.

### Occupation error is not norm error

Let $P$ be the exact orthogonal positive-energy projector, $Y$ the exact evolved occupied basis, and $\widehat Y=Y+\delta Y$. Writing $N=\|PY\|_F^2$ gives

$$
|\widehat N-N|\leq 2\sqrt N\,\|\delta Y\|_F+\|\delta Y\|_F^2.
$$

If the projector itself has error $\delta P$, there is an additional contribution bounded by $\|\delta P\|_2\|\widehat Y\|_F^2$. The Gram residual $\|\widehat Y^\dagger\widehat Y-I\|$ does not bound $\|\delta Y\|$: a perfectly normalized vector can point in the wrong direction. Conversely, a radial rescaling of a negative-energy state changes its norm while leaving its exact positive-energy projection zero. The executable counterexamples give a zero norm residual with an occupation error of approximately 1e-6, and a norm residual of approximately 2e-6 with zero occupation error. These are deliberately constructed counterexamples to an invalid inference, not evidence that the production calculation suffered those particular defects.

Computing $P_+=(I+H/\omega)/2$ can subtract quantities of order one to obtain a very small occupation. For three static Hamiltonians, where the true production is exactly zero, this formula gives signed values between approximately -2.73e-17 and 1.39e-17. Direct overlaps with the positive eigenvectors instead give nonnegative values below 1e-32. Neither formula alone supplies a rigorous floating-point error bound, but the overlap avoids this cancellation mechanism.

The flat $b=10,n=1,K=0$ test has an exact independent reference,

$$
N_{\rm flat}=2\left[\frac{\sinh\pi}{\sinh(\pi\sqrt{22})}\right]^2
=1.6950184976499554\times10^{-10}.
$$

The previous four-component projector result has an absolute error of 2.0988e-16, which is a relative error of 1.2382e-6. Its stable two-sector overlap result has an absolute error of 4.96e-20. The new independent overlap integration differs from the exact reference by 7.24e-20. Thus a small absolute inter-method discrepancy can coexist with substantially fewer reliable relative digits in a rare occupation. Renormalizing a vector removes radial drift only; it does not repair phase or mixing-angle errors.

The expansion-only counterexample also has an exact reference. A constant unitary maps

$$
h_s=a_g(s)\sigma_1-s\sqrt{2bn}\,\sigma_2+K\sigma_3,
\qquad a_g=1.5+0.5\tanh(2s)
$$

to a Sauter Hamiltonian with longitudinal offset 1.5, longitudinal amplitude 0.5, pulse duration 0.5, and transverse mass $\sqrt{2bn+K^2}$. For $b=10,n=1,K=0$, the exact two-sector occupation is approximately 1.8823980738606993e-6. An independently integrated spinor result differs by 6.89e-18. This confirms the earlier nonzero result and falsifies the zero-production shortcut, while removing the need to rely exclusively on two numerical implementations.

### Finite boundaries and initial states require their own test

The in/out conditions in these tests are temporal. There is no black-hole horizon in the prescribed homogeneous FLRW problem. An instantaneous eigenstate at a finite initial time equals the intended asymptotic in-vacuum only up to a separate boundary error. For a two-state Hamiltonian $h=\mathbf h\cdot\boldsymbol\sigma$, the local nonadiabatic scale is controlled by $|\mathbf h\times\dot{\mathbf h}|/|\mathbf h|^3$; small background amplitudes by themselves do not bound a tiny occupation's relative error.

For the expanding electric case, extending the dimensionless endpoint factor from $L=8$ to $L=16$ changes the computed occupation by approximately 2.58e-12. At relative tolerance 2e-13, extending $L=16$ to $L=20$ changes it by approximately 5.51e-18. At fixed $L=16$, tightening the tolerance from 2e-12 to 2e-13 changes the answer by approximately 2.86e-17. This provides an empirical plateau for the checked case. It does not establish a uniform error bound for every Landau level, momentum or background.

The new massive backreaction experiment starts in the exact magnetic vacuum with zero electric field, then applies a smooth compactly supported external current. All derivatives of the pump vanish at its start. This makes the selected initial state explicit and avoids silently identifying a finite-time instantaneous vacuum in an already nonzero electric field with an adiabatically dressed state. Different initial states remain different physical experiments, even if each numerical evolution conserves energy.

### Independent derivation of the matched finite-grid closure

The verifier uses two-component wavefunctions satisfying $i\psi'=h\psi$; the production solver evolves Bloch vectors. No production module is imported. With $p=k-a$, $a'=-x$, $h=M\sigma_1+p\sigma_3$ and $\omega=\sqrt{M^2+p^2}$, one has $p'=x$. Writing $\mathbf r=\psi^\dagger\boldsymbol\sigma\psi$ gives $\mathbf r'=2\mathbf h\times\mathbf r$.

The adiabatic expansion starts with $\mathbf r^{(0)}=-\mathbf h/\omega$ and

$$
\mathbf r^{(1)}=\frac{\mathbf h\times\mathbf h'}{2\omega^3},
\qquad
r_z^{(2)}=\frac{M^2x'}{4\omega^5}-\frac{5M^2p x^2}{8\omega^7}.
$$

The second term includes the longitudinal normalization correction from the first-order vector. Omitting it changes the coefficient. On a fixed shared quadrature, define

$$
S=\sum w\left(r_z+\frac p\omega\right),\quad
C=\sum w\frac{M^2}{4\omega^5},\quad
D=\sum w\frac{5M^2p}{8\omega^7},\quad
Z=1+\chi_B-e^2C.
$$

The proposed equation is

$$
Zx'=F_{\rm drive}-e^2(S+D x^2).
$$

Here $\chi_B$ is a specified on-shell finite magnetic susceptibility matching coefficient. The finite-grid construction is not a proof that every subtraction and cutoff limit reproduces the full four-dimensional renormalized effective action. Adiabatic subtraction and its compatibility with gravitational renormalization are substantive theoretical requirements, not merely ways to improve quadrature. [@V04]

For the chosen fixed grid, the exact common energy is

$$
W=\frac{Zx^2}{2}+e^2\sum w\left(\mathbf h\cdot\mathbf r+\omega\right).
$$

Since $C'=-2Dx$, differentiation gives $W'=xF_{\rm drive}$. This checks the signs and the common finite counterterms. It does not prove the uniqueness of the finite matching prescription: an incorrectly matched but consistently varied model can conserve its own energy too.

For $b=10,n_{\max}=2,K_{\max}=6,N_k=32$, pump duration 4 and final time 8, the independent spinor calculation has a maximum energy-minus-integrated-pump-work residual of 1.066e-11. Its maximum spinor norm error is 1.053e-11. The electric field at the final time is 0.9550507371994522 in critical units. This deliberately small grid is an implementation comparison, not a continuum result.

The subsequent production comparison uses the same finite grid and pump, while evolving real Bloch vectors instead of complex spinors. Across 81 output times, the two electric histories differ by at most 3.63e-12 and the vector potentials by at most 4.62e-12. The production energy-work residual is 1.17e-15; this smaller residual does not imply that its physical prediction is accurate to fifteen digits. The source hash was unchanged during the comparison. `implementation_comparison.json` records the exact parameters, source hashes and measured differences; `compare_implementations.py` reproduces this final comparison against the independently generated reference data.

### Two deliberate failures establish that the diagnostics have power

At finite momentum cutoff, the instantaneous-vacuum term is generally nonzero:

$$
\int_{-K}^{K}\frac{k-a}{\sqrt{(k-a)^2+M^2}}\,dk
=\sqrt{(K-a)^2+M^2}-\sqrt{(-K-a)^2+M^2}.
$$

For $K=2,a=M=1$, its value is -1.7480640977952844. Discarding this boundary term by appealing to oddness while the momentum window is not centered on the kinetic momentum changes the model. The independent defective evolution, which intentionally deletes this term, produces a maximum energy-work defect of 12.6099 and an electric-field difference of 4.0688 from the matched calculation. The actual production model retains the term.

For a constant gauge shift $a\mapsto a+C$, one must shift the canonical modes and the finite window by the same $C$. The independent translated-window test with $C=7.3$ changes the electric history by only 4.44e-16. Keeping the window fixed instead changes it by 0.0151097. This demonstrates regulator sensitivity. It does not test arbitrary local gauge transformations or the full Ward identities of an inhomogeneous four-dimensional theory.

### A separate exact anomaly benchmark

The massive subtraction formula must not be evaluated by simply setting its mass to zero. Use a distinct massless lowest-Landau-level model with an arbitrary fixed reference scale. Its Hamiltonian is diagonal, so an initially filled negative branch has $r_z(k,t)=-\operatorname{sgn}(k-a_0)$. The subtracted integral is

$$
\int_{-\infty}^{\infty}\left[-\operatorname{sgn}(k-a_0)+\operatorname{sgn}(k-a)\right]dk
=-2(a-a_0).
$$

Writing $\lambda=e^2b/(4\pi^2)$ yields $J=-2\lambda(a-a_0)$, $a'=-x$ and, without a drive,

$$
x''+2\lambda x=0,
\qquad \frac{x^2}{2}+\lambda(a-a_0)^2=\text{constant}.
$$

For $\lambda=0.1,x(0)=1,a(0)=a_0=0$, an independent oscillator integration agrees with the cosine electric field to 3.79e-12 over the tested interval, with an energy drift below 3.86e-12. Exact piecewise spectral-flow integration reproduces the coefficient and shows how a window that fails to enclose the spectral crossing clips the current. An oscillator solved correctly is a benchmark of this massless model, not a demonstration that the massive model inherits its exactness.

### Independent weak-frequency check

The proposed below-threshold response kernel can also be tested without the nonlinear implementation. Substituting $k=M\tan\theta$ into its longitudinal integral produces a smooth integrand. At $b=10$, 96 Gauss nodes in $\theta$, Landau levels through 8192, and frequencies 0.01, 0.02 and 0.04, extrapolation of $\Delta\chi/\nu^2$ to zero frequency gives 0.0015604099969639626. The finite-sum analytic value is 0.0015604099969628834, a difference of 1.08e-15. The infinite-Landau trigamma expression is 0.00156041094205709; the explicitly omitted coefficient tail is 9.45e-10.

The independent $B\to0$ longitudinal integral gives $e^2/(60\pi^2)=0.00015485463105144795$ for the coefficient of $\nu^2$. This checks a frequency-dependent term rather than only re-reading the static susceptibility supplied as input. It remains a response-kernel quadrature and limiting-formula check; a fitted response from a driven nonlinear evolution would be an additional test.

### Challenge the comparator literature as well

The 2025 linear-response study by Newsome, Anderson and Grotzke explicitly includes a retarded current commutator, which is nonzero even before pair production. Their selected near-critical-field cases show growing perturbations. Consequently, a converged mean-field trajectory and a conserved mean-field energy do not establish that neglected quantum fluctuations remain small. Their result is a model-specific warning and test design, not a theorem that every strong-field semiclassical calculation fails. [@V02] The earlier Pla et al. study used an approximate linear-response criterion; the later study supplies a direct comparison and a more informative baseline. [@V03]

Gralla and Mizuno derive a first-order-in-mass correction in bosonized 1+1-dimensional QED which is absent in the corresponding semiclassical prediction. Their controlled result motivates the separate period experiment supplied by the lead researcher. It must not be transferred quantitatively to a multi-Landau-level four-dimensional theory without matching its degrees of freedom and regime. The latest version, v2 of 9 April 2026, also distinguishes a conserved total energy from a naive split into quantum field and particle energies: Appendix B retains a nonfactorizing quadratic expectation value. [@N01]

There is a specific logical point to check in that comparison: a pointwise small-mass expansion containing $m/k$ is nonuniform near $k=0$. The absence of an order-$m$ term at each nonzero momentum does not by itself justify exchanging an expansion with an infinite integral. For a compact region this problem can be addressed directly. Let $u=r_x+i r_y$. Then

$$
u'=2ipu-2imr_z,\qquad r_z'=2m\operatorname{Im}u.
$$

For the exact massive initial vacuum, $|u(0)|=|m|/\sqrt{k^2+m^2}$, and unit Bloch norm implies

$$
|u(t)|\leq\frac{|m|}{\sqrt{k^2+m^2}}+2|m|T,\qquad 0\leq t\leq T.
$$

Therefore

$$
\int_{-K}^{K}|r_z(t)-r_z(0)|\,dk
\leq4m^2T\operatorname{arsinh}\left(\frac K{|m|}\right)+8Km^2T^2
=o(|m|)
$$

for fixed $K,T$. This excludes a hidden linear-mass contribution from the shrinking $k\sim m$ region in this fixed-time compact estimate. It is not a uniform ultraviolet or long-time proof: $K\to\infty$, times of order $1/m$, and the renormalized high-momentum tail still require separate control. The supplied script evaluates the bound across decreasing masses; it does not label a finite set of evaluations a proof of the asymptotic statement.

### Acceptance decision

Accept the corrected curved-mode counterexample, the finite-regulator backreaction implementation checks, the exact massless spectral-flow coefficient, and the response-coefficient quadratures within their stated scopes. Do not yet accept a continuum four-dimensional stress/current closure, a mean-field validity theorem, a coupled Einstein evolution or a solution of the original unrestricted problem. The immediate next gates are stable simultaneous momentum/Landau cutoff changes, independently prepared states, a retarded linear-response or fluctuation test, and stress-tensor matching compatible with the same current subtraction.


## A fully quantum comparator that challenges mean-field validation

Gralla and Mizuno's revised April 2026 analysis uses bosonization in massive $1+1$-dimensional QED to compute a controlled first-order-in-mass correction in a strong external field. Its frequency correction is absent in the corresponding semiclassical calculation. This is a useful adversarial comparator: reproducing an anomaly or conserving mean-field energy cannot certify that a massive mean-field model contains all relevant quantum physics. It is not a numerical error bar for our $3+1$-dimensional Landau model. [@N01]

### Reduction, periodicity and a separate numerical scheme

Use the source's positive charge $q$, electric-field parameter $E_C$ and bosonization mass $M=q/\sqrt\pi$. Define

$$\tau=Mt,\qquad A=\frac{2\pi E_C}{q},\qquad
g=2e^{\gamma}\sqrt\pi\,\frac{m}{q},\qquad
z=2\sqrt\pi\langle\phi\rangle+A.$$

Here $g$ is the comparator's mass-expansion parameter, not the WGC gauge coupling or the metric. The first-order effective equation becomes

$$z''+z+g\sin(z-A)=0,\qquad z(0)=A,\quad z'(0)=0,$$
$$V(z)=\frac{z^2}{2}-g\cos(z-A),\qquad
\frac{z'^2}{2}+V(z)=V(A).$$

For the tested $|g|<1$, $V''\geq1-|g|>0$. The nonstationary trajectories between two regular turning points are periodic. This avoids silently applying a blanket claim that every bounded one-dimensional trajectory is periodic: equilibrium and separatrix cases need separate treatment in more general potentials.

The source predicts

$$\frac{\omega}{M}=1+g\cos A\,\frac{J_1(A)}A+O(g^2).$$

The project implemented two independent period measurements: a time-domain DOP853 solution with successive minimum events, and an energy integral between the turning points. A sine-type turning-point substitution removes the square-root endpoint singularity before 128/256-node Gauss–Legendre integration. The code does not infer frequency from a visually fitted plot.

### Executed results and their proper meaning

Fifteen cases use $A=0.5,2,5$ and $g=0,0.02,0.01,0.005,0.0025$. The maximum period difference between the two numerical methods is $1.21\times10^{-11}$. The observed small-$g$ remainder orders approach 1.985, 2.007 and 2.001 for the three amplitude sequences, consistent with the stated second-order remainder.

| Amplitude, at $g=0.0025$ | Numerical $\omega/M$ | First-order prediction |
|---|---:|---:|
| $A=0.5$ | 1.001063299799 | 1.001063052869 |
| $A=2$ | 0.999700230880 | 0.999699997245 |
| $A=5$ | 0.999953598003 | 0.999953539093 |

All four declared comparator gates passed. Solving the truncated nonlinear equation accurately also generates higher powers of $g$ numerically. Those powers are not derived higher-order predictions of full QED. The comparator establishes a reproducible first-order challenge and a numerical check of its effective equation, not a new all-orders quantum solution.

### Questioning the argument rather than merely citing it

The source's small-mass comparison needs care near zero momentum: a pointwise expansion in $m/k$ is not uniform at $k=0$. The independent verifier supplies a compact-momentum finite-time bound. With $u=r_x+ir_y$ and $u'=2ipu-2imr_z$, initial vacuum data and unit norm give

$$|u(t)|\leq\frac{|m|}{\sqrt{k^2+m^2}}+2|m|T,$$
$$\int_{-K}^{K}|r_z(t)-r_z(0)|dk
\leq4m^2T\,\operatorname{asinh}(K/|m|)+8Km^2T^2=o(|m|).$$

This repairs the compact region's order estimate at fixed $K,T$. It does not justify exchanging the limit with an infinite ultraviolet integral or extending it to secular times $T\sim1/m$. Those are additional estimates, not automatic consequences of the paper's headline result.

The revised source also warns that a conserved classical-looking effective total energy need not split into the separate quantum field and matter expectation values by naive replacement of operators with their means. In particular, a normal-ordered quadratic expectation can contain a variance term beyond the square of the expectation. We therefore use the comparator's period and total effective energy, without identifying each nonlinear-potential term as a separately measured quantum energy. [@N01]



## Gravitational closure: equations, counterexamples and verified next steps

### What this audit changes

The previous curved-mode calculation was a valid calculation on a prescribed geometry. It was not an Einstein–Maxwell–Dirac solution, and its small occupation-number discrepancies could not certify the missing gravitational equations. The next meaningful extension must calculate **two directional pressures as well as energy and current**, and must propagate an initial gravitational constraint. A homogeneous magnetic field selects an axis; a single FLRW scale factor cannot in general respond to its stress. This is a restriction on the self-consistent extension, not a reason to discard the earlier prescribed-background benchmark. Magnetized Bianchi-I calculations explicitly retain this anisotropy. [@H01]

This module supplies a complete classical gravitational interface, a finite-regulated anisotropic Dirac interface, a common-counterterm Ward test, and an independently evolved classical test fixture. It does not supply the missing four-dimensional renormalized quantum state. Its executed checks appear in `gravity_checks.py` and `gravity_checks.json`. No quantum-gravity endpoint is inferred from them. The independent advisor reviewed and accepted (H11), (H14)–(H17) and (H19), including the spin and pressure factors, rotating-basis connection and counterterm signs, within the stated finite/classical scope.

### 1. Fix signs before coupling modules

Take signature $(-+++)$, $\hbar=c=1$, Heaviside–Lorentz electromagnetic units, $\kappa=8\pi G$, and

$$ds^2=-dt^2+a_\perp^2(t)(dx^2+dy^2)+a_\parallel^2(t)dz^2.$$

Let $h=\dot a_\perp/a_\perp$, $k=\dot a_\parallel/a_\parallel$, and $\theta=2h+k$. Choose $F=dA$, $F_{xy}=B_0$, $F_{0z}=\dot A_z=-a_\parallel E$, and $B=B_0/a_\perp^2$. Define the physical current $j=a_\parallel J^z$ by the matter-action variation $\delta W/\delta A_\mu=\sqrt{-g}J^\mu$. These definitions require

$$\nabla_\nu F^{\mu\nu}=J^\mu,\qquad
\dot E+2hE=-j,\qquad \dot B+2hB=0.\tag{H1}$$

Writing the antisymmetric tensor indices in the opposite order changes the sign of the Maxwell equation. The Lorentz-force Ward identities in these conventions are

$$\nabla_\mu J^\mu=0,\qquad
\nabla_\mu T_{\rm m}^{\mu\nu}=F^{\nu}{}_{\lambda}J^\lambda,\qquad
\nabla_\mu T_{\rm EM}^{\mu\nu}=-F^{\nu}{}_{\lambda}J^\lambda.\tag{H2}$$

The homogeneous Gauss constraint requires zero total charge density. Neutral pair creation is consistent with a nonzero longitudinal current. A charge density or transverse momentum introduced by a new state would require additional constraints and generally a larger ansatz. Parallel $E$ and $B$ carry no electromagnetic Poynting flux in this frame. A dipole or multipolar magnetic geometry is not represented by this homogeneous model.

**New source check.** Newsome–Anderson–Grotzke's 2025 PDF uses $E=-\dot A$ and $\ddot A=-\dot E=J_C+\langle J_Q\rangle$ in equation (3.1). Its displayed Sauter source (3.3a) has a minus sign, whereas differentiating its positive pulse (3.3b) requires $J_C=+2qE_0\operatorname{sech}^2(qt)\tanh(qt)$. Its perturbation (4.3) uses the latter sign. The introductory covariant equation also reverses the sign relative to its action and equation (2.2). These are displayed-equation inconsistencies; they do not establish what sign the authors' numerical implementation used. Our symbolic differentiation reproduces the discrepancy. The HTML numbers these formulas differently and displays a regenerated date; the PDF dates itself May 2, 2025. [@H02]

### 2. Full Einstein–Maxwell energy and stress system

Write the orthonormal matter tensor as $\operatorname{diag}(\rho_m,p_{m\perp},p_{m\perp},p_{m\parallel})$. With $u=(E^2+B^2)/2$,

$$\rho=\rho_m+u,\quad p_\perp=p_{m\perp}+u,\quad
p_\parallel=p_{m\parallel}-u.\tag{H3}$$

These field pressures, including the negative longitudinal pressure, follow from the Maxwell stress tensor; replacing all of them by $u/3$ changes the problem. The independent Einstein equations are

$$C\equiv h^2+2hk-\kappa\rho-\Lambda=0,\tag{H4}$$

$$\dot h=\frac{\Lambda-\kappa p_\parallel-3h^2}{2},\tag{H5}$$

$$\dot k=\Lambda-\kappa p_\perp-h^2-k^2-hk-\dot h,\tag{H6}$$

$$\dot a_\perp=ha_\perp,\quad \dot a_\parallel=ka_\parallel,\quad
\dot A_z=-a_\parallel E.\tag{H7}$$

The matter Ward identity and electromagnetic work identity reduce to

$$\dot\rho_m+2h(\rho_m+p_{m\perp})+k(\rho_m+p_{m\parallel})=Ej,\tag{H8}$$

$$\dot u+4hu=-Ej.\tag{H9}$$

Equations (H1), (H3)–(H9) become a closed initial-value problem only when the quantum state supplies $j,\rho_m,p_{m\perp},p_{m\parallel}$ consistently. One cannot determine all four functions from (H8). An external current requires the external apparatus' energy and stress, or a clearly prescribed-background approximation.

The curvature expressions useful for local screens are

$$R=4\dot h+2\dot k+6h^2+4hk+2k^2,$$

$$R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
=4\left[2(\dot h+h^2)^2+(\dot k+k^2)^2+h^4+2h^2k^2\right].\tag{H10}$$

The script independently constructs all Christoffel symbols, the Ricci tensor and Einstein tensor from the four-dimensional metric before comparing the reduced equations. This checks their signs and the relative factors rather than simply rearranging a copied ODE.

#### 2.1 Constraint propagation and an actual review correction

Define the residual

$$\mathcal R_E=\dot\rho+2h(\rho+p_\perp)+k(\rho+p_\parallel).$$

Using precisely (H5)–(H6), direct differentiation gives

$$\boxed{\dot C=-\theta C-\kappa\mathcal R_E.}\tag{H11}$$

Thus constrained data stay constrained when total stress is conserved. The evolution equation also provides a diagnostic: compare the directly evaluated $C$ with the integrated source residual; they should agree to numerical error. Dividing by a tiny energy density alone is not a robust normalization near a field zero.

The reviewer initially suggested $-2\theta C$ by recalling a different constraint-added evolution system. The independent metric calculation rejected it: this spatial-Einstein evolution gives $-\theta C$. The equation above was corrected before acceptance and before any claimed result. Constraint propagation coefficients are formulation dependent off the constraint surface; memory of a standard formula is not a proof.

For running $\kappa(t)$ and $\Lambda(t)$ the same calculation yields

$$\dot C=-\theta C-\kappa\mathcal R_E-\dot\kappa\rho-\dot\Lambda.\tag{H12}$$

Simply replacing couplings by running functions while retaining separately conserved matter therefore fails unless $\dot\kappa\rho+\dot\Lambda=0$, or the additional terms follow from a consistently varied action or energy exchange. A 2026 asymptotic-safety Bianchi-I preprint, whose September 7 revision was checked, explicitly encounters an overdetermined magnetic system and introduces additional stress. Its equations (44)–(46) independently agree with the constraint-decay and running-coupling structure derived here. That is a model-dependent closure, not a four-dimensional QED current calculation. Its classical electric–magnetic duality also does not transfer unchanged to electrically charged pair production. [@H03]

#### 2.2 Why mean-energy conservation is insufficient

Let $\Delta=k-h$. Subtracting the spatial Einstein equations gives

$$\dot\Delta+\theta\Delta=\kappa(p_\parallel-p_\perp).\tag{H13}$$

An initially isotropic geometry with isotropic matter and aligned electromagnetic fields has $\dot\Delta=-\kappa(E^2+B^2)$ immediately. A prescribed FLRW pulse cannot be turned into a self-consistent magnetic solution by evolving its single scale factor from $\rho$ alone.

There is an explicit nullspace in the energy constraint: changing $p_\perp$ by $k f(t)$ and $p_\parallel$ by $-2h f(t)$ leaves $2hp_\perp+kp_\parallel$ unchanged at every instant, while changing the shear source by $-\kappa\theta f(t)$. Here $f$ has units pressure divided by expansion rate. An energy-only fit cannot identify the missing anisotropic stress. The nullspace remains even with exact numerical energy conservation.

### 3. A concrete anisotropic Dirac bridge

Rescale the spinor by $\chi=(a_\perp^2a_\parallel)^{1/2}\psi$ to remove the homogeneous spin-connection volume term. For charge $q>0$ and a fixed comoving Landau basis define

$$P=\frac{k_z-qA_z}{a_\parallel},\quad
c_n=\frac{\sqrt{2n|qB_0|}}{a_\perp},\quad
H_n=m\beta+P\alpha_z+c_n\alpha_x,\qquad i\dot Y_n=H_nY_n.\tag{H14}$$

For $n\ge1$ one may use $\beta=\tau_z\otimes I$, $\alpha_z=\tau_x\otimes\sigma_z$, $\alpha_x=\tau_x\otimes\sigma_x$, and a $4\times2$ matrix of initially occupied negative-energy modes $Y_n$. The lowest Landau level has a single $2\times1$ occupied column and no transverse term. The longitudinal symbol $k_z$ is the canonical momentum, not the Hubble parameter $k$ used above. Transverse rotational symmetry and charge-neutral initial data are assumed.

Let

$$\mathcal D(t)=\frac{|qB_0|}{4\pi^2a_\perp^2a_\parallel},\qquad
\mathcal S[X]=\sum_n\int dk_z\operatorname{Tr}(Y_n^\dagger X_nY_n).$$

At a **fixed finite comoving mode regulator**, the common Hamiltonian variations give

$$\rho_{\rm bare}=\mathcal D\mathcal S[H],\quad
j_{\rm bare}=q\mathcal D\mathcal S[\alpha_z],\tag{H15}$$

$$p_{\parallel,\rm bare}=\mathcal D\mathcal S[P\alpha_z],\quad
p_{\perp,\rm bare}=\frac{\mathcal D}{2}\mathcal S[c_n\alpha_x].\tag{H16}$$

Both spin channels are already represented by the columns of $Y_n$ at $n\ge1$. Multiplying again by the usual twofold Landau degeneracy double counts them. The factor one-half in each transverse pressure is different: changing $a_\perp$ changes two spatial directions.

From $\dot{\mathcal D}=-\theta\mathcal D$, $\dot P=qE-kP$, $\dot c_n=-hc_n$, and $d\langle H\rangle/dt=\langle\dot H\rangle$, equations (H15)–(H16) satisfy (H8) exactly. The script checks this finite-mode identity symbolically. It is a useful interface test for a later mode solver, but fixed comoving cutoffs are not covariant renormalization and can violate gauge-shift comparisons through their boundaries. Divergent sea energies and anisotropic regulator stresses cannot be inserted into Einstein's equations as physical sources.

The previous curved-mode connection also generalizes. The conserved sector operator is $S=\tau_z\otimes\sigma_y$. In sector $s=\pm1$, write $h_s=P\sigma_3+m\sigma_1-sc_n\sigma_2$. A time-dependent rotation making the transverse mass real yields

$$h_{s,\rm rot}=\left[P+\frac{s(m\dot c_n-c_n\dot m)}{2(m^2+c_n^2)}\right]\sigma_3+
\sqrt{m^2+c_n^2}\sigma_1.\tag{H17}$$

Here $\dot m=0$ in cosmic time, so the connection is $-smhc_n/[2(m^2+c_n^2)]$. A naive replacement $m\to\sqrt{m^2+c_n^2}$ drops it. In conformal FLRW time the mass coefficient changes instead and reproduces the earlier connection with the corresponding sign. These are different time parametrizations of the same basis issue.

### 4. Renormalize current and stress together

A causal in-in effective action or a locally covariant point-splitting construction must define both observables from one state and one set of local counterterms. Formally, on coincident physical branches,

$$J^\mu=\frac1{\sqrt{-g}}\frac{\delta W_{\rm CTP}}{\delta A_\mu},\qquad
T_{\mu\nu}=-\frac2{\sqrt{-g}}\frac{\delta W_{\rm CTP}}{\delta g^{\mu\nu}}.\tag{H18}$$

Gauge and diffeomorphism invariance then give (H2). Variation of an in-out vacuum-persistence action is not automatically a causal expectation value in a chosen initial state. Zahn's construction demonstrates the current-renormalization freedom and the role of local covariance. Its stress-conservation discussion carefully restricts backgrounds or includes their dynamics; it must not be summarized as separate matter-stress conservation in an arbitrary external electromagnetic field. [@H04]

An explicit finite-counterterm test is useful. Add $W_{\rm ct}=-(c/4)\int\sqrt{-g}F^2$ to the matter effective action. In our convention it induces

$$\delta j=c(\dot E+2hE),\quad
\delta\rho_m=cu,\quad \delta p_{m\perp}=cu,\quad\delta p_{m\parallel}=-cu.\tag{H19}$$

These shifts satisfy (H8) using $\dot B=-2hB$, without imposing the sourced Maxwell equation. Changing only the current subtraction leaves a residual $-E\delta j$ if the old stress is kept. Changing both observables while compensating the electromagnetic coupling is a renormalization-scheme transformation; changing only one is a different, generally inconsistent dynamics. This is a concrete check rather than an appeal to a renormalization label.

The next initial state must also have appropriate short-distance structure. A finite-time instantaneous vacuum on an arbitrary rapidly changing geometry is not automatically a Hadamard state with a finite fourth-order-subtracted stress. Work on the semiclassical initial-value problem explicitly treats compatibility between initial geometry, quantum two-point functions and constraints, and labels important existence and uniqueness statements as conjectures. We therefore cannot choose all geometry derivatives and an arbitrary ultraviolet state independently. [@H05]

### 5. What the new numerical calculation verifies

Before putting a quantum source into this geometry, we solved a deliberately transparent classical fixture. Set $\Lambda=0$, $j=\sigma E$, and use an isotropic radiation reservoir with $p_m=\rho_m/3$ and

$$\dot\rho_m=-\frac43\theta\rho_m+\sigma E^2.$$

This Ohmic constitutive law is phenomenological. It is not a Schwinger current. The chosen dimensionless $\kappa=0.1$ makes gravitational effects visible for an algorithmic test and must not be interpreted as the physical electron coupling. Initial data are $a_\perp=a_\parallel=1$, $E=1$, $B=3$, $\rho_m=0.2$, $\sigma=0.2$, with $h=k=\sqrt{\kappa\rho/3}$. We evolve to $t=2$.

An independent formulation uses $H=(2h+k)/3$ and $\Delta=k-h$:

$$\dot H=-H^2-\frac{2\Delta^2}{9}-\frac\kappa6(\rho+3\bar p),\qquad
\dot\Delta=-3H\Delta+\kappa(p_\parallel-p_\perp),$$

where $\bar p=(2p_\perp+p_\parallel)/3$. The directional and Raychaudhuri–shear formulations were evolved independently; their equations agree on constrained solutions but differ off the constraint surface.

| Executed check | Result |
|---|---:|
| Symbolic zero-residual identities | 19 passed |
| Maximum Hamiltonian residual | $4.11\times10^{-14}$ |
| Maximum magnetic-flux error, $Ba_\perp^2-B_0$ | $7.86\times10^{-14}$ |
| Maximum damped-electric-flux error, $Ea_\perp^2e^{\sigma t}-E_0$ | $7.33\times10^{-14}$ |
| Independent Raychaudhuri–shear versus directional solver | $8.73\times10^{-14}$ |
| RK4 errors at 100, 200, 400, 800 steps | $5.62\times10^{-9}$, $3.47\times10^{-10}$, $2.15\times10^{-11}$, $1.34\times10^{-12}$ |
| Observed RK4 convergence orders | 4.018, 4.009, 4.009 |

At the endpoint $h=0.2373631$ and $k=-0.03305215$: the transverse directions expand while the longitudinal direction contracts. This demonstrates a behavior that an isotropic scale factor cannot represent. It validates the classical gravitational interface and numerical implementation only.

#### 5.1 A quantitative scale obstruction

For the physical electron, the retained constants give $8\pi Gm_e^2\simeq4.40\times10^{-44}$. At $E/E_c=1$ and $B/B_c=100$, the field energy is about $5.45\times10^4m_e^4$, so $\kappa\rho_{\rm EM}/m_e^2\simeq2.40\times10^{-39}$. These fields by themselves do not generate electron-scale spacetime curvature. An order-one stress-curvature budget from a purely magnetic field would require $B/B_c$ of order $2.04\times10^{21}$ in this elementary estimate, far outside the previously tested $b\le1000$ range.

This is not a theorem forbidding $R\sim m_e^2$: other gravitating matter, a compact-object geometry or a cosmological sector can supply it. It is a missing-source test. The classical Maxwell trace is zero, so the scalar $R$ alone is especially misleading. The exact Kasner example $a_\perp\propto t^{2/3}$, $a_\parallel\propto t^{-1/3}$ has $R=0$ but $R_{\mu\nu\rho\sigma}^2=64/(27t^4)$. Both formulas were checked. The earlier report already printed a Kretschmann diagnostic; that stronger screen should be retained.

### 6. Stability and fluctuations are independent acceptance gates

Mean stress is not a complete measure of quantum fluctuations. Even a bounded energy observable can have the same conserved mean in an energy eigenstate and a mixture with probability $p$ at energy $\bar E/p$ and probability $1-p$ at zero. The variances are respectively zero and $\bar E^2(p^{-1}-1)$. At $p=0.01$ this is $99\bar E^2$. This elementary counterexample does not itself diagnose gravitational breakdown; it shows why equal conserved means cannot decide it.

The physically relevant object is a smeared stress noise kernel and its gravitational response, schematically $N=\langle\{T-\langle T\rangle,T'-\langle T'\rangle\}\rangle/2$ and an induced metric correlation $G_RNG_R^T$. Coincident unsmeared variances are singular, while ratios to a zero mean can spuriously label the Minkowski vacuum invalid. Stochastic-gravity analyses distinguish induced and intrinsic fluctuations. [@H06]

For the coupled problem one needs the retarded block response of current and stress to both $A$ and $g$, including $JJ$, $JT$, $TJ$, and $TT$ kernels with contact terms. The metric/current variations must respect the same Ward identities as the mean equations. A linear-response stability test is a necessary internal check, not a universal sufficient theorem that a semiclassical solution is exact. [@H07]

The 2025 Maxwell–Dirac study provides a concrete lower-dimensional benchmark for this next test. It evaluates the causal current commutator rather than only comparing two nonlinear trajectories. Consequently, a future finite-difference perturbation test must shrink its perturbation size and compare with a tangent or retarded-kernel calculation; agreement over an early interval must not be extrapolated indefinitely. [@H02]

#### 6.1 Higher derivatives and order reduction

Retaining $R^2$ and $R_{\mu\nu}R^{\mu\nu}$ in an EFT introduces higher metric derivatives. Solving a truncated fourth-order equation with arbitrary extra initial data can excite modes outside the expansion's validity. A schematic equation $\ddot x+\omega^2x-\ell^2x^{(4)}=0$ has a rapidly growing branch with rate of order $1/\ell$ even though its low-frequency branch has a regular perturbative limit. A numerical integrator accurately resolving that branch does not establish a physical instability of the ultraviolet completion.

Order reduction uses the lower-order equation inside perturbative corrections and retains the requested order in the EFT expansion. It must be applied consistently to constraints and response equations, with the discarded order recorded. [@H08] An $R^2$ term is not automatically a ghost: it can represent an additional healthy scalar in a different theory; generic curvature-squared spin-two poles and EFT extra branches require separate analysis. [@H16] Conversely, deleting all matter-loop effects as “runaways” can discard meaningful large-$N$ physics. The choice between an EFT expansion and an enlarged dynamical theory must precede the initial-value problem. [@H06]

### 7. Cauchy horizons and quantum energy inequalities remain distinct tests

The earlier scalar diagnostic $\phi\sim |V|^\beta$ implies local squared-derivative behavior $|\partial_V\phi|^2\sim |V|^{2\beta-2}$. Its integral converges for $\beta>1/2$, diverges logarithmically at $\beta=1/2$, and diverges as a power below it. This is an energy-regularity statement about a specified asymptotic profile. It neither proves smooth extension of a metric nor supplies a backreacted quantum endpoint.

An extension claim must specify whether it means continuous metric extension, square-integrable connection, classical differentiability, or a distributional solution with a well-defined stress. Fixed-background divergent $\langle T_{VV}\rangle$ is not the same object as a solved singular backreacted geometry. Shahbazi-Moghaddam's analysis relates a mild singularity structure to robust, state-independent behavior in a near-horizon wedge construction; it explicitly does not prove that all states fit that construction or that every allowed divergence appears. [@H09]

Violating a pointwise classical energy condition also does not prove that a quantum bounce occurs. Fewster–Kontou establish a semiclassical singularity theorem for a specified minimally coupled scalar model with quantum-energy-inequality and initial contraction hypotheses. Its theorem and quantitative example were checked beyond the abstract. It cannot be imported unchanged into interacting spinor QED with strong electromagnetic fields. It is a counterexample to the generic inference “quantum negative energy removes all singularity arguments,” not a proof of censorship for our target. [@H10]

### 8. Reopened 2025–2026 entanglement dispute: test the channel

Aziz–Howl's 2025 Nature paper argues that classical gravity coupled to quantum matter can generate the relevant entanglement through a field-theoretic mechanism. This is a theoretical claim, not a reported observation of gravitationally mediated entanglement. [@H11] Marletto, Oppenheim, Vedral and Wilson contest the combination of an ultralocal nonrelativistic Hamiltonian with a propagator that reintroduces the discarded momentum term, and distinguish classical modulation of a quantum channel from classical mediation. [@H12]

Di Biagio emphasizes a separate qualification: subsystem mediation assumptions and relativistic no-signalling are different, and gauge-constrained field theories do not automatically admit the naive tensor-product decomposition. This is a criticism of overbroad interpretations of witness theorems, not a numerical renormalized-current closure. [@H13] Lin–Mondal's March 2026 paper calculates three quadrupole models and finds entanglement in its quantized tidal-parity model but not in its stated mean-field or stochastic alternatives. Its conclusion is model specific; it also illustrates how perturbative truncation can manufacture an apparent witness. [@H14]

We execute a small algebraic falsifier of that latter failure mode. Exact local evolution $U=e^{-i\eta\sigma_x}\otimes e^{-i\eta\sigma_x}$ maps $|00\rangle$ to a product state. Keeping only its first-order state, $|00\rangle-i\eta(|01\rangle+|10\rangle)$, and renormalizing yields apparent concurrence $2\eta^2/(1+2\eta^2)$, equal to $0.0196078$ at $\eta=0.1$. The apparent signal is at the omitted order and disappears in the exact channel. This does not replicate either gravity experiment; it tests the logic of taking a nonlinear witness after an uncontrolled truncation.

An actionable experiment must therefore compare complete channels under the same initial state, retain terms to the accuracy needed by the witness, bound electromagnetic and quantum-matter mediation, and identify which locality assumptions it tests. No gravity witness inferred from a source-field simulation should be presented as an observed quantum-gravity result.

### 9. Advisor decision: next experiments and rejection criteria

| Experiment | What is already available | Required advance | Decisive failure criterion |
|---|---|---|---|
| Bianchi-I finite-mode pressure test | Equations (H14)–(H16), symbolic work identity | Independent matrix-mode integration with evolving two scale factors | Energy Ward residual or unequal spin normalization beyond discretization error |
| Common four-dimensional subtraction | Local action identities and counterterm test | Hadamard/adiabatic expansion for current and all stresses in one convention | Gauge-shift or finite-scheme transformation changes a physical prediction |
| UV regulator comparison | Fixed-regulator identity only | Remove longitudinal and Landau cutoffs with a common covariant subtraction | Stable mean energy but drifting anisotropic pressure/shear |
| Causal fluctuation response | Lower-dimensional current-response primary benchmark | Tangent equations, then mixed current/stress kernels and smearing | Gauge-invariant growth not attributable to discretization or an EFT-discarded branch |
| Physical electron coupling | Scale-budget calculation | Perturbative gravitational correction or explicit external gravitating source | Visible order-one curvature from $b\sim100$ without an additional energy source |
| Cauchy-horizon bridge | Existing characteristic reduced model and regularity criteria | Specified state, charge evolution and extension norm | Endpoint changes under admissible state/subtraction variations without controlled error |

The down-selection is to complete the causal renormalized Maxwell–Dirac benchmark first, while using this anisotropic system as a verified gravitational interface. The full four-dimensional renormalized pressure calculation and noise response remain explicit research work. They have not been replaced by the classical fixture.

Public programmes are useful sources of methods and constraints, not evidence that a conjecture is true. For example, the European Commission-funded QuEST project ran in 2017–2019 and supported quantum-energy-condition and singularity research; the official university record establishes that historical funding, not a current machine or a solved quantum-gravity theory. [@H15]


## Empirical and source challenge: third research cycle

### What this pass actually adds

This pass reopens omitted mechanisms and tests the sources themselves. It does not infer that a government programme, patent, impressive sensitivity number, or agreement among simulated models establishes the proposed physics. Six concrete additions change the research plan: a 2026 disagreement over the support and renormalization of constant electric fields in de Sitter; an invalid action argument inside an electrostatic-force patent; an incorrect graviton–fermion selection rule in another patent; a detector-noise bookkeeping problem in a released government report; a recent multi-detector rejection of apparently interesting transients; and a spin-polarization experiment whose apparent displacement arose from its optical readout environment.

The international search adds Canada, South Korea and Brazil and deepens Australia, Italy, Germany and the United States. These are targeted searches, recorded in `search_coverage.json`. They are not an inventory of every country's projects. Historical source documents, current research activity, simulations and measurements have separate statuses. No inaccessible or classified record is treated as read.

### A new challenge to the negative-current narrative

Bastero-Gil and colleagues' April 2026 revision studies a dynamical, homogeneous vector field in de Sitter and chooses a tachyonic mass, $m_A^2=-2H^2$, to sustain its constant electric background. Their finite subtraction uses flat-space vacuum polarization evaluated at $p^2=2H^2$ and yields a positive, finite current in regimes previously associated with negative infrared divergence. They explicitly leave stress evolution and realistic electromagnetic generation outside their calculation. Sections 2.1–2.4, rather than the headline, define the comparison. [@E01]

The following is our independent consistency check. With physical electric field and physical current defined in the usual cosmological Ampere convention, homogeneous Maxwell evolution is

$$\dot E+2HE=-j_{\rm matter}-j_{\rm pump}.$$

Multiplication by $E$ yields the energy budget

$$\dot\rho_E+4H\rho_E=-E(j_{\rm matter}+j_{\rm pump}),\qquad \rho_E=E^2/2.$$

An externally maintained constant field is therefore possible in ordinary Maxwell theory when the pump supplies the dilution and matter-work losses. A source-free Maxwell field instead redshifts as $a^{-2}$. The statement that constant physical $E$ universally demands a tachyonic photon mass is too broad: it demands support, and the support model must be specified. Comparing a pumped massless theory with a source-free modified vector theory is not a clean renormalization-only comparison. Neither calculation supplies the current of our finite pulse merely by substituting its instantaneous field.

Hayashinaka and Xue's original maximal-subtraction proposal makes a different choice: remove the inverse-mass terms so the heavy-particle current decays exponentially. Its Eqs. 12–15 show how the finite subtraction changes the conductivity, and Eq. 7 keeps the product of renormalized charge and gauge potential invariant. This is a physical prescription that must be examined, not a theorem that any term without a Schwinger exponential is erroneous. [@E02]

Our falsifiable test is to compare the **same** pumped background, quantum state, measured charge and stress/current counterterms under two admissible descriptions. Move a local polarization contribution between the field equation and the source consistently. A claimed physical amplification must persist in the total field evolution and work balance. A sign change in one named piece is insufficient. Re-entry requirements are a finite renormalization map, Ward identity, matched pump stress and an evolved field; this source review does not claim to have run that continuum calculation.

### Government and international comparators with explicit status

| Jurisdiction and record | Established status and measurement | Exact use in this project |
|---|---|---|
| Canada: TRIUMF, ALPHA/HAICU | The May 2026 laboratory article reports antimatter spectroscopy and describes HAICU as infrastructure being developed. The existing ALPHA gravitational result is distinct from the future hydrogen quantum-sensing programme. [@E04] | Magnetic-trap force gradients and state preparation must enter the gravitational observable. A new initiative is not a completed interference test. |
| South Korea: IBS CoReLS | The laboratory's May 2021 report documents the demonstrated laser-intensity milestone and describes focusing and beam diagnostics. It is a historical performance result, not a current world-record assertion. [@E05] | Use measured pulse geometry and fluctuations when predicting strong-field processes; peak intensity alone does not specify electric-like invariants. |
| Australia: MAGE at UWA | A 2025 report analyzes 61 days of data with two quartz detectors and uses coincidence selection to reject predecessor-like rare transients as gravitational candidates. [@E03] | Test a proposed signal in an independent sensor and calibrate coincidence efficiency. Narrowband strain sensitivity is not an unexplained-event detection. |
| Brazil and international partners: BINGO | The 2026 collaboration analysis is a forecast using simulated HI maps and Planck likelihoods. Its acknowledgements identify Brazilian public funding and national supercomputing resources. It omits some correlated noise and beam/leakage complexities. [@E06] | A cosmological inference comparator, not a strong-field laboratory. Repeat forecasts under omitted nuisance models before translating precision into evidence for new gravity. |
| Italy: INFN/CNR Archimedes | The 2024 prototype paper reports torque noise near $7\times10^{-13}\,\mathrm{N\,m}/\sqrt{\mathrm{Hz}}$ around 60 mHz. The final vacuum-weight target is a future sensitivity requirement, not the reported signal. [@E07] | Model the weight of the complete energy-changing apparatus, thermal and seismic transfer functions, and superconducting-state changes. |
| Germany: IFW Dresden/TU Dresden NMR test | The original 2024 experiment compares spin-polarized samples and control configurations. Its sensitivity differs by material and polarized mass fraction. [@E13] | Do not convert a best resolution from one sample into a universal exclusion for every material or DNP mechanism. |
| United States: NASA BPP | Official indexed records identify the historical programme and memoranda. Direct full retrieval failed again in this pass. [@E16] | Retain as an access gap and historical lead; do not claim detailed source adjudication from the unread memorandum. |
| United States: DIA released HFGW reference document | A dated 2010 report is directly available in DIA's public reading room, with author identity redacted in this copy. It discusses projected concepts and calculations. [@E09] | Its equations and assumptions can be tested. Release by an agency does not transform forecasts into measured performance. |

The source map deliberately excludes generic quantum-computing announcements that would inflate geographic coverage without changing a QED–gravity test. It also avoids claiming that conventional laboratory fields realize $R/m_e^2\sim1$. No newly inspected facility demonstrates the complete strongly curved Einstein–QED feedback problem.

### Two patents whose equations can be challenged directly

#### Electrostatic propulsion: the invalid inference appears before the force calculation

The Aurigema–Buhler patent US11511891B2, in “Theory of Operation,” Eqs. 1–5, replaces stationarity of the action with an ordinary differential condition on an energy–time product, obtaining $d(Ut)=0$ and $Udt=-t\,dU$. Later paragraphs treat Coulomb attraction and electrostatic pressure as separate contributions. These are substantive claims to test, not merely unusual terminology. [@E15]

Our counterexample requires no disputed new physics. Take

$$L=\tfrac12 m\dot x^2-U_0,\qquad x(t)=vt+x_0,$$

with a nonzero constant potential offset $U_0$ and fixed endpoint variations. Euler–Lagrange gives $m\ddot x=0$, so the trajectory has stationary action. Nevertheless,

$$\frac{d(U_0t)}{dt}=U_0\ne0.$$

Thus $\delta\int Ldt=0$ does not imply $d(Ut)=0$. Adding an arbitrary constant to a potential cannot change forces, whereas the disputed inference is sensitive to that constant. The proposed derivation therefore fails before its geometry optimization. This does not by itself diagnose every reported instrument signal; that requires data and a complete apparatus model.

An independent whole-system identity is

$$\mathbf F_{\rm matter}=\oint_{\partial V}\mathbf T_{\rm EM}\cdot\mathbf n\,dS-\frac{d}{dt}\int_V\epsilon_0\mathbf E\times\mathbf B\,dV,$$

$$T_{ij}=\epsilon_0(E_iE_j-\tfrac12\delta_{ij}E^2)+\mu_0^{-1}(B_iB_j-\tfrac12\delta_{ij}B^2).$$

For an isolated, localized, electrostatic charge distribution and a boundary taken to infinity, field momentum is static and the surface integral vanishes. The result includes the total matter, bound charges and supports. Integrating selected electrode faces can produce a force on those faces while missing its reaction elsewhere. In matter, use a vacuum bounding surface around the apparatus to avoid confusing alternative macroscopic stress conventions.

The corresponding discrete counterexample is exact: for any finite collection of separated charges, the internal Coulomb force obeys $\sum_i\sum_{j\ne i}\mathbf F_{ij}=0$ because $\mathbf F_{ij}=-\mathbf F_{ji}$. Asymmetric charge geometry does not change the pair cancellation. A finite-element extension should integrate the same closed surface at multiple radii, include the supply and shield, and compare against all volume forces. A nonzero residual that moves with the integration boundary is a diagnostic of missing terms or discretization, not thrust.

#### Graviton spin does not prohibit coupling to an electron

The Pais patent US10322827B2 claims, in its discussion following Eq. 4, that spin-two gravitons do not couple to spin-one-half electrons. It also assumes extraordinary source fields in its conversion estimates; those values are premises rather than reported measurements. [@E08]

Our direct field-theory test starts with the generally covariant Dirac action. Variation with respect to the metric gives the symmetric matter stress, with on-shell form

$$T_D^{\mu\nu}=\frac{i}{4}\bar\psi\left(\gamma^\mu\overleftrightarrow{D}^{\nu}+\gamma^\nu\overleftrightarrow{D}^{\mu}\right)\psi.$$

The linear metric perturbation couples to this tensor through $\delta S_D=\tfrac12\int\sqrt{-g}\,T_D^{\mu\nu}\delta g_{\mu\nu}\,d^4x$ under that stress convention. It is nonzero for an electron state carrying energy and momentum. Different particle spins do not remove this interaction. Weak coupling or kinematic restrictions for a particular process must not be replaced by a universal spin prohibition. This counterexample invalidates that inference, without adjudicating every patent claim.

### A government report can double-count measurement resources

The DIA HFGW document's Section 2.2.3 first estimates an “effective stored” RF energy from power times a 1000-second observation times a cavity factor. It then incorporates temporal and spatial selectivity factors in another effective quality factor. Its later communication example explicitly chooses a hypothetical bandwidth and noise floor. These numbers require a detector transfer-function derivation before they can be used as sensitivity. [@E09]

Our dimensional and dynamical comparator is the actual cavity balance,

$$\dot U=P_{\rm in}-\kappa U,\qquad \kappa=\omega/Q_{\rm cav},\qquad U_{\rm ss}=P_{\rm in}Q_{\rm cav}/\omega.$$

Here $P_{\rm in}$ is the power deposited in the mode; coupling and reflection must be included when converting a generator rating into that quantity. For fixed deposited power, observing longer does not cause the steady stored energy to grow indefinitely. Integration time improves an estimator through its noise bandwidth and number of independent data, not by repeatedly counting the same intracavity energy. For a given physical apparatus, replace verbal “quality factors” by an input–output transfer matrix, loss channels and noise covariance. Separate loaded cavity $Q$, observation duration, angular response and collection efficiency.

The actual opposing view was read. GravWave's author-side response argues that the Li–Baker synchro-resonant Gaussian-beam geometry differs from bare Gertsenshtein conversion and that transverse detection rejects background. This geometry objection deserves a matched calculation; it is not answered by citing a critic's status. [@E11] The JASON archive records a contrary assessment, but the complete linked report could not be retrieved here. We therefore do not claim to have independently checked its detailed equations. [@E10]

Here is our small independent detector benchmark. For an ideal lossless balanced mixer with coherent signal and local oscillator, measured photon counts are Poisson with

$$\bar N_\pm=\tfrac12(N_{\rm LO}+N_s)\pm\sqrt{N_{\rm LO}N_s}\cos\phi.$$

For difference $D=N_+-N_-$,

$$\langle D\rangle=2\sqrt{N_{\rm LO}N_s}\cos\phi,\qquad \operatorname{Var}D=N_{\rm LO}+N_s.$$

At fixed signal and optimal phase, increasing $N_{\rm LO}$ gives $\mathrm{SNR}\to2\sqrt{N_s}$, rather than unbounded noiseless gain. This is an explicitly defined benchmark, not a full proof about an arbitrary Li–Baker geometry. A proposed background-free output requires its own mode-overlap, loss and detector covariance calculation. Squeezing or active media changes the quantum state and resource accounting; it cannot be silently inserted into the coherent benchmark.

### A critic's negative control and an actual replication are different evidence

Prutchi's 2019 author-hosted critique identifies a reported magnet-off control that undermines attribution of an apparent weight change to resonance-dependent spin ordering. He also identifies missing simultaneous recording of microwave timing. His diagrams partly reconstruct the apparatus from a book; this is a documentary critique, not his own complete replication. [@E12]

Stark, Grafe and Tajmar then supplied an actual NMR investigation. Its material-dependent sensitivity table matters: some metallic samples have too little polarized mass relative to noise to support exclusion. Apparent shifts at higher pulse loading also occur without a specimen and track heating-induced refractive-index changes in the interferometer path. This is a specific instrumental account, not an argument that every conceivable spin-dependent force is impossible. [@E13]

The alternative-propulsion community's 2026 event page still presents spin ordering as a test target and explicitly distinguishes DNP's established spectroscopic role from gravitational control. It is a current participant-community lead, not an independently validated force law. [@E14]

The improved experiment must measure spin polarization and force simultaneously. Use independent sensing principles, randomized resonant/off-resonant settings with matched deposited heat, blank specimens and optical-path monitoring. A resonance in the force channel alone is ambiguous: resonant absorption itself changes thermal power. Fit the alternative amplitude to a separately measured spin observable rather than to the microwave command.

### Executed source-criticism checks

`empirical_logic_checks.py` was executed and wrote `empirical_logic_results.json`. Four check groups passed: the fixed-endpoint action variation vanishes while $d(U_0t)/dt=-9$ for a constant-potential example that also satisfies the patent’s assumed zero total energy; energy differentiation and direct Coulomb summation independently give forces $(-5/3,7/2,-11/6)$ with zero total; a dimensionless lossy-cavity integration agrees with its analytic energy law to $5.20\times10^{-13}$; and 200,000 simulated coherent-detector trials at each of seven local-oscillator settings reproduce the predicted count mean and variance within the declared six-standard-error threshold. At fixed two signal photons, the analytic SNR approaches $2\sqrt2$ rather than increasing without bound. These are mathematical and simulated measurement checks. The full apparatus reconstructions, continuum-current comparison and hardware experiments below remain proposed.

### New hypothesis and experiment ledger

These are proposed discriminating experiments and calculations. None is presented as hardware work executed by this source-review agent.

| ID | Hypothesis | Distinguishing observation or calculation | Nuisance model and failure criterion |
|---|---|---|---|
| E-X01 | Negative current represents observable field amplification. | Compare two matched finite-renormalization descriptions of one pumped background and the total evolved $E(t)$. | Unmatched charge, local polarization and pump work. Fail if amplification changes only when bookkeeping changes. |
| E-X02 | Constant de Sitter $E$ universally forces a photon mass change. | Integrate ordinary Maxwell with a prescribed compensating current and its power budget. | External support is explicitly included. Counterexample succeeds if constant $E$ and energy balance coexist with massless Maxwell. |
| E-X03 | Stationary action requires $d(Ut)=0$. | Free-particle/constant-potential analytic counterexample; repeat after changing the potential zero. | No statistical uncertainty needed. Failure is mathematical and occurs before numerical optimization. |
| E-X04 | Electrode asymmetry produces isolated steady thrust. | Closed-surface stress, pair-force cancellation and a source-inclusive finite-element model. | Bound charges, supports, grounded enclosure, lead forces and radiation. Fail if a force disappears when the whole system is counted. |
| E-X05 | Graviton–electron coupling vanishes because spins differ. | Vary Dirac action and evaluate its stress between nonzero-energy electron states. | Distinguish nonzero coupling from a kinematically forbidden special process. The universal claim fails if the stress vertex is nonzero. |
| E-X06 | A local oscillator amplifies conversion without added quantum noise. | Poisson balanced-detector benchmark, then a full proposed-mode transfer model. | LO fluctuations, vacuum ports, losses and detector dark counts. Fail if signal growth is accompanied by the omitted variance. |
| E-X07 | Longer observation increases stored cavity energy. | Solve the driven lossy cavity and compare energy with estimator SNR as duration changes. | Ring-up time and finite bandwidth. Fail if stored energy saturates while the proposed formula grows with observation time. |
| E-X08 | Spin ordering changes weight beyond ordinary forces. | Simultaneous polarization, interferometric and independent force measurements under blinded settings. | Heat-matched detuning, magnetic gradients, sample-free optical paths. Reject a claimed mechanism if its spin dependence is absent under adequate sensitivity. |
| E-X09 | Rare narrowband transients are gravitational. | Two-detector coherent injection and coincidence analysis with declared timing/antenna response. | Local crystal events, RF pickup and correlated environmental disturbances. Lack of coincidence is informative only above both instruments' detection efficiency. |
| E-X10 | A vacuum-weight signal identifies the absolute cosmological vacuum energy. | Model and modulate a specified finite apparatus energy difference including supports. | Condensation energy, heat flow, thermal expansion, magnetic force and seismic tilt. A measured energy difference does not identify the absolute cosmological constant. |
| E-X11 | A facility's peak intensity fixes the pair-production signal. | Sample measured vector pulse shapes and compute field invariants and spectra. | Spatiotemporal coupling, incoming particles, focal averaging. Fail if indistinguishable peak intensity produces different process predictions. |
| E-X12 | Simulated cosmological precision is insensitive to omitted systematics. | Add correlated noise, frequency-dependent beams and polarization leakage to held-out forecasts. | Foreground complexity and fitting flexibility. Fail if nominal intervals lose their injection-calibrated coverage. |

The new priority is not a wider unstructured bibliography. It is a source-to-equation challenge record: state the premise, build an admissible counterexample, identify what the measured observable is, and prevent the counterexample from silently becoming another substitute for the full coupled problem.


## What AI-assisted breakthroughs actually teach this project

Three documented examples show how AI can improve difficult research problems when proposals face an independent, executable correctness criterion. Their achievements concern specified mathematical objects and algorithms. They provide useful methods for our project, but no evidence that generating persuasive explanations solves quantum gravity. The transfer recommendations below are this project's methodological synthesis. Sources and repository contents were checked on 9 September 2026; none of these research engines was executed in this run.

### FunSearch: discover a construction, then inspect its structure

FunSearch produced a cap set containing 512 vectors in eight dimensions over the three-element field, improving the previous construction of size 496. This established a better lower bound; it did not establish the optimal size or solve the unrestricted cap-set problem. A frozen language model proposed priority functions inside a supplied construction procedure. Executable evaluation rejected invalid outputs and scored valid sets; evolutionary selection retained useful programs. Inspecting the resulting program helped the authors derive an explicit structured construction. Only four of 140 reported experiments reached 512, illustrating why failed searches and total search budget matter. [@A01]

Its public repository includes the evolutionary pipeline and examples, while omitting the language models, execution sandbox, and distributed infrastructure. It supplies reusable components rather than a complete reproduction environment. [@A02]

### AlphaTensor: exact residuals separate discovery from proof

AlphaTensor found a 47-multiplication algorithm for multiplying two 4-by-4 matrices over the field with two elements, improving the 49-multiplication Strassen-square construction in that arithmetic. TensorGame subtracts proposed rank-one tensors from the fixed multiplication tensor. Reaching the exact zero residual supplies a correctness certificate; reinforcement learning and tree search guide the difficult search. This certificate does not prove minimum rank. Restricting permissible factor coefficients can exclude better algorithms, a limitation the authors explicitly identify. The finite-field result also cannot be relabelled a 47-multiplication real-arithmetic algorithm. [@A03]

The public repository supplies factorizations, loading and verification notebooks, recombination code, and hardware benchmarking material. These are valuable independent-check artifacts; their presence should not be described as release of the entire training system. [@A04]

### AlphaEvolve: improve the search algorithm under staged evaluation

The 2025 report describes evolving code that searches for tensor decompositions, including optimizer, initialization, and loss changes. Candidate programs encounter increasingly demanding evaluations and multiple random seeds. It reports a 48-scalar-multiplication construction for two 4-by-4 complex matrices, improving 49 in that setting. The complex field distinguishes this result from AlphaTensor's finite-field result. Discretized factors permit exact reconstruction checks; a small floating-point fitting loss alone would not certify an algorithm. [@A05]

The official results repository contains correctness-checking code, expressly excludes the AlphaEvolve engine, and includes only instances outperforming earlier constructions. That selection limits assessment of overall success from the notebook alone. A May 2026 official update reports broader applications; it is a developer report, not independent validation of our electromagnetic–gravitational model. [@A06; @A07]

### Transfer to the next physics iteration

1. Freeze an advisor-reviewed contract: action, units, quantum state, renormalization conditions, sources, boundary conditions, and approximation domain. Candidate agents may improve numerical methods; changing this contract creates a separately labelled hypothesis.
2. Use inexpensive coding agents to propose reductions, asymptotic expansions, quadrature, and integrators. Keep the evaluator independently maintained and inaccessible to candidate edits.
3. Reject dimensional inconsistencies, broken identities, wrong analytic limits, and charge or energy accounting failures before costly evolution. Then require independent implementations, grid and cutoff convergence, and regulator checks appropriate to the claimed observable.
4. Reserve untouched parameter cases and adversarial limits. Optimize speed only after correctness gates. Preserve all failures, seeds, budgets, and discrepancies; use disagreements to reopen assumptions rather than average incompatible answers.
5. Separate evidence levels: an exact identity verifies mathematics; numerical convergence supports a declared continuum model; experimental discrimination tests its physical relevance. No level automatically establishes the next.

A flawed evaluator can efficiently select a wrong closure. The useful lesson is therefore to strengthen falsification alongside search. Our executed counterexamples and solver checks are local validation artifacts, not a claimed reproduction of these AI discovery systems.


## Synthesis: a staged research programme with rejection rules

The useful combination of partial solutions is a dependency graph expressed as tests. The matched flat current is a reference for the zero-expansion limit of a curved solver. The gravity fixture supplies independent constraint identities. The fully quantum comparator and retarded-current literature test the mean-field approximation. None of these outputs can simply be added to obtain a solved spacetime.

| Stage and hypothesis | Required calculation | Observable and rejection condition | Status |
|---|---|---|---|
| P1: finite magnetic matching survives causal evolution | Shared mode current/energy and weak pumped-field experiment | Reject if the physical low-frequency response is erased despite conservation | Executed; matched model passes tested comparison |
| P2: late field reversal is quadrature-resolved | Fixed-window momentum refinement, separate window and Landau checks | Reject stated precision if any component shift exceeds it | Executed; approximate reversal accepted, rigorous continuum bound absent |
| P3: the selected mean-field trajectory is stable to quantum response | Retarded-current commutator and perturbed-state evolution | Track growth relative to the background; reject validity if small perturbations grow beyond the declared regime | Proposed; the separate one-dimensional quantum comparator is executed |
| P4: anisotropic stress closes with the same subtraction | Compute current, energy, transverse and longitudinal pressure from the same modes and counterterms | Ward residual and Einstein constraint must converge together | Finite identities derived; full covariant quantum subtraction unfinished |
| P5: weak curvature reproduces both independent limits | Small anisotropic expansion, zero-expansion matched limit and zero-field anomaly checks | Reject a shortcut if it loses a basis connection or a curvature counterterm | Classical gravity fixture and prior external-field tests executed; coupled quantum test proposed |
| P6: target curvature has a realizable support budget | Solve initial Einstein constraints including matter, pump and magnetic supports | Reject a nominal target if its curvature is imposed without the required stress | Electromagnetic scale obstruction quantified |
| P7: resonant conversion survives a matched dispersive treatment | Transverse polarization tensor, mixed vertex and flux-normalized transfer system | Compare phase mismatch, absorption and full flux; reject an index-only inference | Proposed; constant two-state identity retained |
| P8: charged-horizon claims survive causal flux evolution | Geometry-matched current/stress, horizon-regular state and evolving mass/charge | Monitor constraints and continuation regularity at the actual horizons | Open; homogeneous calculation cannot decide it |

### Why the numerical method was down-selected

| Candidate | Symmetry and boundaries | Numerical hazard | Best first method | Advisor decision |
|---|---|---|---|---|
| Matched homogeneous Maxwell–Dirac | Temporal initial-value ODEs; Landau and momentum modes | Fast phases, subtraction cancellation, UV and quadrature limits | Vectorized adaptive ODE plus independent spinors and analytic limits | Selected and executed |
| Bianchi-I quantum backreaction | Homogeneous anisotropic metric plus modes | Two pressures, common covariant subtraction, constraints | Symbolic derivation then constrained ODE/mode integration | Interface and classical fixture executed |
| Spherical charged quantum interior | Double-null $1+1$ geometry plus state-dependent flux | Inner-horizon blueshift, stiff null layers, stress regularity | Characteristic finite differences with constraint refinement | Full evolution deferred until closure is specified |
| Static or slowly varying conversion ray | Two/four polarization amplitudes along a ray | Resonance layers, rapid phase and damping | Adaptive transfer ODE; spectral methods for smooth boundary problems | Requires matched quantum kernel |
| Axial multipolar Einstein–QED | Nonlinear geometry plus nonlocal matter state | Gauge/gravity constraints, UV subtraction, support, memory | Established numerical-relativity infrastructure plus verified quantum module | Research-scale integration, not a reasoning-only solution |

A PINN is not a remedy for an unspecified current or stress. It can interpolate or approximate a well-defined solution only after loss scaling, initial-state constraints and independent residual/error checks are established. High-frequency mode phases and competing physical scales are concrete hazards. Chebyshev collocation is suitable for smooth finite-domain boundary problems with well-treated endpoints; it is not inherently preferable to a causal initial-value solver here. [@ROOT13]

### Open-source tool choices and what was actually used

NumPy, SciPy, SymPy and mpmath supply the executed array integration, symbolic identities and high-precision benchmarks. The package contains complete project-authored Python and saved outputs. It does not replace those libraries with a new numerical framework. Requirements record the versions used; small independent checks can be rerun separately from the costly production mode evolution.

WarpX, Smilei and Ptarmigan are valuable strong-field simulation comparators, but their documented QED modules or reference configurations must be matched to the mechanism. Photon-emission and photon-induced pair Monte Carlo models do not automatically implement vacuum Schwinger production with a four-dimensional renormalized in-in stress tensor. None was used here as a substitute for that missing calculation. [@ROOT03; @ROOT05; @R235; @R236]

Two author GitHub repositories were inspected in this pass. One demonstrates Qiskit Schwinger-model simulations; the other is an external-field Schwinger plotting project with work-in-progress extensions. Their READMEs were checked, not their complete code or runtime output. Neither was represented as a ready-made three-dimensional causal gravity-backreaction solver. The educational quantum simulation can inform a separate lattice benchmark only after Hamiltonian normalization, truncation and continuum extrapolation are specified. [@N04; @N05]

For study, use the earlier source ledger's accessible proper-time QFT chapter, the initial-value pair-production review and the Dirac renormalization papers as a sequence: derive mode normalization, reproduce the exact pulse, derive the shared subtraction, then reproduce the weak response and the coupled experiment. Reading an entire textbook is not a prerequisite to checking a specified identity, but reading a source's abstract is not enough to claim its derivation was reproduced. [@R238; @C03; @V04]

### What would count as a new result

A new converged solution of a previously specified initial-value problem can be a useful research result even if it is not a solution of quantum gravity. A publishable novelty claim additionally needs a prior-art comparison, matched limiting cases, a physical observable, uncertainty from model and numerical approximations, and reproducible evidence that does not depend on selecting only successful parameter points. This run offers a corrected research foundation and executed partial solutions. It makes no priority or publication claim.

Before expanding the project again, the next advisor milestone is P4: implement covariantly compatible directional stresses and verify the shared Ward identity in an anisotropic background. P3 should run alongside it, because a beautifully conserved coupled mean field can still lie outside its fluctuation-validity regime. The original dipole, charged horizons and curvature of order $m_e^2$ should then be introduced in separate controlled stages, each with its own supporting sources and rejection conditions.



## Targeted solver specification for GPT Astra

### Role, target and output contract

Act as a computational QED researcher with a separate adversarial verification role. Reproduce and extend the following *specified* homogeneous semiclassical Maxwell–Dirac experiment. Quantize the charged fermion; evolve the classical electric expectation field causally from its current. Use a static uniform parallel magnetic field and initially the exact magnetic vacuum. Do not claim to solve the full multipolar Einstein–QED system. Provide derivations that a reviewer can check, complete runnable code, environment versions, convergence tables, raw invariants and a precise account of failed gates. Use NumPy/SciPy and SymPy; use mpmath for independent analytic references. Do not substitute a PINN before a conventional reference exists.

### Geometry, scales and state

Use natural Heaviside–Lorentz units, signature $(-+++)$, physical mass $m>0$, physical charge magnitude $e>0$, $e^2=4\pi\alpha$, and $\alpha=1/137.035999084$. The spacetime is Minkowski:

$$ds^2=-dt^2+dX^2+dY^2+dZ^2.$$

With dimensionless coordinates $(s,\xi,\eta,\zeta)=m(t,X,Y,Z)$, the metric is $m^{-2}\operatorname{diag}(-1,1,1,1)$ and its connection and curvature vanish. Landau gauge may be chosen for the constant $B$; the electric connection is homogeneous $A_z(t)$. No cosmological scale factor is hidden in the notation.

Define $a=eA_z/m$, $x=eE_z/m^2$, $b=|eB|/m^2$, canonical longitudinal momentum $k$, kinetic momentum $p=k-a$, $M_n^2=1+2bn$, and $\omega_{nk}=(M_n^2+p^2)^{1/2}$. The positive-charge member is used to define the reduced one-particle Hamiltonian. With the negative branch initially occupied, no extra particle/antiparticle degeneracy factor is added.

### Complete differential system

For each mode evolve the real Bloch vector $\mathbf r=(r_1,r_2,r_3)$:

$$a'=-x,\quad r_1'=-2pr_2,\quad
r_2'=2(pr_1-M_nr_3),\quad r_3'=2M_nr_2.$$

On a fixed canonical Gauss–Legendre grid, with $n=0,\ldots,N$ and positive longitudinal weights $w_i^{(k)}$, use

$$w_{ni}=\frac{b(2-\delta_{n0})}{4\pi^2}w_i^{(k)},$$
$$S=\sum_{ni}w_{ni}(r_3+p/\omega),\quad
U=\sum_{ni}w_{ni}(M_nr_1+pr_3+\omega),$$
$$C=\sum_{ni}w_{ni}\frac{M_n^2}{4\omega^5},\qquad
D=\sum_{ni}w_{ni}\frac{5M_n^2p}{8\omega^7}.$$

Use the physical finite magnetic matching term

$$\chi_b=\frac{e^2}{12\pi^2}
\left[b-\ln(2b)-\psi\!\left(1+\frac1{2b}\right)\right],
\qquad Z=1+\chi_b-e^2C,$$

where $\psi$ is digamma. For very small positive $b$, use a cancellation-safe proper-time or asymptotic evaluation with a checked overlap region; the production experiment uses $b=10$ and the formula is well conditioned. The exact $b=0$ transverse continuum is a separate limit, not a zero-weight Landau grid.

Close Maxwell's equation and integrate accumulated pump work $I_W$:

$$x'=\frac{F(s)-e^2(S+Dx^2)}{Z},\qquad I_W'=xF(s).$$

All right-hand sides now depend only on the current state, fixed grid and specified pump. The full matter current is

$$\mathcal J=S+Dx^2-Cx'+\chi_b x'/e^2=(F-x')/e^2.$$

Do not label $S+Dx^2$ the full physical current; it is the effective numerator after moving local polarization to the left side. Compute the subtracted integrands before summing to reduce avoidable cancellation. Never clip occupations or renormalize Bloch vectors inside the evolution to make an invariant look exact.

### Initial and asymptotic conditions

At $s=0$, set $x=0$, $a=a_0$, $I_W=0$, and

$$\mathbf r_{ni}=-\frac{(M_n,0,k_i-a_0)}{\sqrt{M_n^2+(k_i-a_0)^2}}.$$

For $s\leq0$, this static magnetic vacuum is the preparation. On $0<s<T_p$, set $u=s/T_p$ and

$$F(s)=\frac{x_{\rm target}}{T_pI}
\exp[-1/(u(1-u))],\qquad
I=\int_0^1\exp[-1/(v(1-v))]dv.$$

Set $F=0$ elsewhere. For $s>T_p$, impose no final electric value: solve the source-free evolution. There is no spatial horizon or distinguished radial origin in this homogeneous model, so horizon boundary data would be spurious. The ultraviolet mode boundary is an integration limit, not a spacetime infinity condition. Begin with finite $k\in[a_0-K,a_0+K]$ and increase $K$, node count and Landau cutoff separately. Do not impose a vacuum final state while pairs or coherent polarization remain present. A late field oscillation need not have a static $s\to\infty$ limit.

A residual gauge test changes $a_0$ and every canonical node by the same constant. Holding the window fixed changes the regulator and is a deliberately inequivalent comparison.

### Required derivation and analytic gates

Before coding, verify symbolically:

1. $p'=x$, $|\mathbf r|^2{}'=0$, and $U'=xS$ at any fixed quadrature.
2. The second-order current subtraction is $c=M_n^2x'/(4\omega^5)-5M_n^2p x^2/(8\omega^7)$ and its common energy term is $u_2=M_n^2x^2/(8\omega^5)$; verify $u_2'=xc$.
3. $C'=-2Dx$ and the exact finite-grid identity $W'=xF$ for $W=Zx^2/2+e^2U$.
4. The full-longitudinal integral of $M_n^2/(4\omega^5)$ is $1/(3M_n^2)$; subtract a matched zero-field transverse continuum and recover $\chi_b$.
5. Independently recover $\chi_b$ from the proper-time integral, its weak-field limit $\alpha b^2/(9\pi)$ and the below-threshold frequency coefficient. Keep physical finite matching distinct from regulator convergence.

### Discretization and execution

Use vectorized mode arrays and DOP853 or a demonstrably equivalent adaptive high-order integrator. Integrate source work as a state variable. Avoid estimating it with a coarse trapezoid over saved plots. Stop with an explicit failure if the integration fails, a nonfinite value occurs or $Z$ approaches the declared positive floor. A negative denominator is not automatically a physical instability.

First run a small shared-regulator comparison: $b=10$, $N=2$, $K=6$, 32 nodes, $T_p=4$, $s_f=8$, 81 output times. Implement independent complex-spinor equations $iy'=(M_n\sigma_1+p\sigma_3)y$ without importing production dynamics. Compare histories and energy/work residuals, not only a final number.

Then reproduce the final experiment: $b=10$, $N=8$, $K=40$, 4096 nodes, $T_p=4$, $x_{\rm target}=1$, $s_f=50$, 251 output times, relative tolerance $2\times10^{-10}$, absolute tolerance $2\times10^{-12}$ and maximum step 0.05. Expect approximately $x(50)=-0.03757$ within the explicitly reported finite-model tests, not eleven-digit certified accuracy. Keep exact machine outputs in data files.

Vary ODE tolerance independently of quadrature. Compare 1024, 2048 and 4096 nodes at fixed $K=40$; compare $K=40$/2048 with $K=60$/3072; compare $N=8$ with $N=12$. Report field and full-current histories separately. Distinguish sampled maxima from event-located extrema. A window enlargement at nearly fixed central spacing does not replace node refinement.

For the physical-response check use $b=100$, target 0.01, pump duration 20 and final time 40. Compare the measured late-field mean with $0.01/(1+\chi_b)$ and repeat with omitted/sign-reversed matching as explicitly wrong controls. A consistently wrong model may conserve its own energy: acceptance needs both conservation and physical matching.

### Deliverables and extension gate

Return runnable Python files, requirements, commands, source hashes, JSON/CSV histories and a gate ledger containing failures. Report absolute energy error, the actual physical normalization scale, relative error, raw mode norm defects, raw occupation extrema, minimum $Z$, gauge test, independent implementation discrepancy and each numerical limit. Provide no blanket “all tests passed” if a stricter requested target failed.

Keep the full quantum one-dimensional bosonized comparator separate; it tests a known missing mean-field correction in another theory. For gravitational extension, start from the supplied Bianchi-I equations and compute both directional pressures with common covariant current/stress counterterms. Require the Einstein constraint and Ward identity before evolving the metric. Do not substitute $m\to ma(t)$ into the flat subtraction or identify the current calculation as a proof of semiclassical validity. The original charged horizons, strong curvature and multipolar fields remain future geometry-matched problems.



## Advisor acceptance and disposition

The first production run actually closes the electric-field loop. Its prescribed quantity is an external current supported on $0<s<4$, normalized to leave $x=1$ in the absence of quantum matter. The actual initial field is zero. The run uses $b=10$, Landau levels $0\ldots8$, 256 Gauss–Legendre momentum nodes per level on $[-40,40]$, and $0\le s\le50$. It is therefore a specific 2304-mode approximation, not an implicitly unregulated continuum.

On this grid the electric field reaches approximately $0.98949$, is approximately $0.98791$ when the external source ends, and subsequently falls through zero to approximately $-0.03743$ at $s=50$. The source is exactly zero throughout the recorded post-pump interval. The retained quantum current is consequently responsible for the later evolution. This is a new causal electromagnetic calculation beyond the earlier prescribed-field results.

The recorded work is $W_{\rm drive}\simeq0.49780688$ in the code's $e^2\rho/m^4$ normalization. The maximum absolute energy/work residual is approximately $8.79\times10^{-12}$, or $1.77\times10^{-11}$ relative to that supplied energy. The initial diagnostics incorrectly called an error divided by $\max(1,|W|)$ a relative energy error; the implementation reviewer identified this and required a truthful normalization. The sampled maximum squared-Bloch-norm residual is approximately $3.14\times10^{-8}$. The minimum $Z$ is approximately $0.99602$. A constant gauge/grid translation changes the sampled field by approximately $8.48\times10^{-13}$. These checks support correct finite-system evolution; they do not assign a continuum error bar to the quoted late-time field.

### A convergence failure that changes acceptance

The advisor rejected treating the initial scan as successful momentum convergence. Even at $s=20$, the final fields at 128, 256 and 512 nodes are approximately $0.72844247$, $0.72817454$ and $0.72847889$. The difference between 256 and 512 nodes is $3.04\times10^{-4}$ at the endpoint and $3.33\times10^{-4}$ over the sampled history. It is much larger than the integration-tolerance or energy residual. This is precisely the kind of logical mistake the new protocol must prevent: conservation of an accurately solved quadrature approximation does not establish accuracy of the quadrature itself.

The old window scan also held the node count fixed while changing the interval. It therefore changed momentum resolution and the ultraviolet cutoff simultaneously. It is a useful stress test, but cannot isolate the physical cutoff contribution. The advisor requested a targeted resolved-grid sequence through the actual $s=50$ production interval, followed by a larger window at maintained resolution and a Landau-level comparison. Those later results must determine the release precision. The original eleven displayed digits of $x(50)$ are finite-grid output, not eleven validated physical digits.

The requested long-interval follow-up was then executed and inspected. All rows below use the same $b=10$ and pump, evolve through $s=50$, and retain the common subtraction.

| Long-interval test | Observed result |
|---|---:|
| $K_{\max}=40$, $n_{\max}=8$, 1024 nodes: $x(50)$ | $-0.0375827954464$ |
| Same bounds, 2048 nodes: $x(50)$ | $-0.0375716457510$ |
| Same bounds, 4096 nodes: $x(50)$ | $-0.0375716424940$ |
| Maximum sampled field-history change, 2048 to 4096 nodes | $3.26\times10^{-9}$ |
| Maximum effective-numerator-history change, 2048 to 4096 nodes | $1.13\times10^{-6}$ |
| Endpoint change, $K_{\max}=40$ with 2048 nodes to $K_{\max}=60$ with 3072 nodes | $4.11\times10^{-11}$ |
| Endpoint change, $n_{\max}=8$ to 12 at $K_{\max}=40$ with 2048 nodes | $5.06\times10^{-8}$ |

The large 1024-to-2048 change required the 4096-point calculation: enlarging the interval while preserving essentially the same resolution could otherwise share the unresolved quadrature error. The final comparison resolves that particular risk for the field history. The largest recorded endpoint change among the last component tests is the Landau truncation change. These are measured finite sequences, not mathematical tail bounds or a proof that every renormalized observable has converged. They support reporting the late-time field approximately as $x(50)=-0.03757$ for this matched mean-field experiment, and support its post-source sign reversal.

The refined runs record 251 time samples, compared with 501 in the first run. Their reported maximum field around $0.98931$ is a **sampled** maximum and misses the earlier sample near the true peak around $0.98949$; it is not evidence that momentum refinement substantially changed the peak. Current convergence must use the matched physical current inferred from the complete Maxwell right-hand side. The raw quantity $J_0$ alone changes with the subtraction/window and is not that observable.

### Weak-response and non-mean-field comparators

At $b=100$, a slow weak drive with bare-vacuum target $0.01$ gives a recorded matched late-field average approximately $0.0093130106$, compared with the static linear prediction $0.01/(1+\chi_b)\simeq0.0093130200$. The difference is approximately $9.33\times10^{-9}$. This is useful evidence that the intended finite magnetic response survives once after subtraction. It remains a finite-duration, finite-grid test; the late-time averaging window and residual oscillations must be reported. The deliberate fully subtracted/no-restoration control is the test of erasing that response. A negative-restoration control is a further deliberately wrong model, not the definition of the ordinary no-restoration control.

The separate bosonized one-dimensional comparison is accepted as a check on the first-order effective equation derived from that quantum theory. Fifteen parameter cases compare the oscillation period from an ODE with an independent energy quadrature; their largest reported difference is approximately $1.21\times10^{-11}$. The first-order truncation remainders scale with orders approximately $1.985$, $2.007$ and $2.001$ in the three amplitude sequences. This provides a useful example of a quantum correction omitted by a mean-field treatment, while retaining the source's dimensional and perturbative limitations. Solving the truncated equation accurately does not turn its higher numerical powers into derived higher-order QED predictions. The comparison does not supply an error bar for the three-dimensional massive Landau calculation.

### Disposition of the four original research fronts

| Original front | Accepted contribution from this round | What is still required before a conclusion about the open problem |
|---|---|---|
| Festina Lente and weak gravity | Clear separation of matter-induced discharge, imposed support and spectrum conjectures; causal-current methods are available for a future geometry-matched test | Charged de Sitter horizons, the chosen quantum state, physical charge normalization, scalar forces and actual decay channels; flat homogeneous pumping does not test either conjecture |
| Magnetized curved Schwinger backreaction | A matched, causal electromagnetic mode/current system and a finite-regulator energy identity; exact audit of the earlier external curved benchmark | Anisotropic curved current, energy and both pressures with common covariant subtractions, then metric feedback at the target curvature |
| Mass inflation and quantum evaporation | Explicit rejection of energy-only stress closure and a separately tested Einstein-constraint methodology | Null fluxes, horizon state/boundary data, dilaton/backscatter structure and a renormalized stress on the charged black-hole geometry; a homogeneous plasma oscillator cannot determine the Cauchy-horizon endpoint |
| Photon–graviton mixing | A checked magnetic susceptibility and a retarded finite-frequency electromagnetic comparator | Momentum-dependent polarization, both polarizations, the matched mixed photon–graviton kernel and geometry-dependent propagation; the homogeneous scalar response alone is not a conversion probability |

The source review's source-free de Sitter vector model and this pumped Maxwell system use different support assumptions. A mass or source requirement proved in one ansatz is not universally necessary for a field maintained by an external current. This is an example of comparing the full equation and support conditions before promoting a criticism into a general no-go result.

### Next decision

The mathematical and implementation acceptance is **a causal matched finite-regulator mean-field calculation**, with independently checked limits and the targeted long-interval momentum, window and Landau comparisons above. The field reversal and approximate late-time field are accepted; unqualified continuum convergence, eleven-digit physical precision and convergence of the entire stress tensor are not. Full quantum electromagnetic fluctuations, collisions, anisotropic covariant stress and metric feedback remain unresolved dependencies. The next physical advance should compute the compatible anisotropic current and pressures from a common state and subtraction prescription and test the Einstein constraint, with a quantum linear-response or fluctuation comparator. It should not add the present energy curve to a prescribed metric and call the combination self-consistent.

The final nomenclature audit distinguishes the full current from the effective Maxwell numerator. For the fixed-window refinement the full matter-current difference is $1.1315\times10^{-6}$ in $j/(em^3)$ units; the numerator difference is $1.1270\times10^{-6}$. The detailed results chapter gives the reconstruction.
