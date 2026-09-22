# AI1 independent algebra, prepared before producer exchange

Fix hbar > 0 and the mathematical surrogate kappa = alpha eta (1-q)^3/hbar with alpha > 0, eta,q in (0,1). Let the two inherited endpoint functions be F_X(z), F_+(z), with theta=z/84. This calculation concerns their reparameterized readout curves R_j(t)=F_j(kappa t). It does not assert that these curves are the exact finite-q physical correlations. The actual endpoint theorem uses growing times. At fixed t, z tends to zero as q tends to one.

Their derivatives with respect to physical t are

- R_X'(0)=0 and R_X''(0)=-2(kappa/84)^2;
- R_+'(0)=i kappa/84 and R_+''(0)=-4(kappa/84)^2.

The first nonzero coherent slope identifies kappa from an exact complete curve. Since kappa is positive, the single-cycle curvature also identifies kappa algebraically, although it has a different sensitivity at small signal. Neither creates a second combination of alpha, eta and q. All values of every endpoint probe depend on the same scalar argument. Exact equal-kappa parameter points therefore give identical complete curves, not only equal finite samples. At fixed scaled argument z, the functions contain no such physical parameter dependence at all.

For example, in units with hbar=1, (alpha,eta,q)=(2,1/2,3/4), (4,1/4,3/4), and (2,1/16,1/2) all give kappa=1/64. Each is inside the declared parameter domain. The log-sensitivity vector is (1,1,-3q/(1-q)), so any exact endpoint-data information matrix obtained by weighting these sensitivities has rank at most one. This is structural information for the surrogate, not a numerical condition number for the unknown finite-q experiment.

Conditionally retaining the carrier gives U_j(t)=exp[-i(9alpha/2hbar)t]R_j(t). Then

alpha=-(2hbar/9) Im U_X'(0),

kappa=84 Im[U_+'(0)-U_X'(0)].

These equations identify alpha and eta(1-q)^3 if the full complex carrier-sensitive curves and absolute physical clock really are available under this model. They still do not separate eta from unknown q. An independent q measurement would do so. Demodulation by the unknown alpha cannot be counted as free calibration. Complete continuous ideal curves determine slopes; a discretely sampled or noisy curve needs a separate sampling/uncertainty certificate. This derivation does not claim the carrier surrogate is an exact finite-q theorem or a realizable laboratory protocol.

The executed standard-library checker reconstructs the fibers, slopes, inverse, all rank-one minors and wrong-model controls using exact fractions without importing producer code. A finite-q correction epsilon*q gives an explicit abstract counterexample to inferring exact finite-q nonidentifiability from identical limiting maps. An overlapping-interval control shows that arbitrarily close effective rates cannot be separated at a fixed nonzero observation error. A single phase matched to the coherent mean fails its second moment; a single cosine matched to the X curvature fails its fourth moment. These are mathematical controls, not fitted experimental data.
