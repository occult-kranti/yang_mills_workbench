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

The metric response changes the current, that current changes the field, and field plus quantum stress change the metric. Boundary conditions and state variations enter this response. The fully strong-curvature current/stress kernels remain unresolved. The following homogeneous flat-space model now computes a restricted causal electromagnetic response and backreaction, with the metric held fixed. Linear-response and stress-fluctuation analyses are part of checking the semiclassical approximation, separately from the electron derivative expansion. [@ROOT01; @ROOT02]

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
