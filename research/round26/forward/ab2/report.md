# AB2 forward: a Gaussian inverse with certified full-source contraction

This independently derived second loop uses both frozen AB1 reports and the skeptical first-loop gate. No current reverse AB2 solution was read. The same actual homogeneous G, identity-extended cubic source A and fixed physical scales are retained. The result is a finite-resolution homological inverse whose full operator residual is below 0.385 times ||A|| uniformly in all finite containing cuboids. This is not an exact inverse or a weighted-locality theorem.

## Actual kernel and homological identity

For a dimensionless proof duration s>0 set p_s(t)=exp[-t²/(2s²)]/(sqrt(2pi)s), and define the odd integrable kernel

    h_s(t)= integral_t^infinity p_s(u)du       (t>0),
           -integral_-infinity^t p_s(u)du     (t<0).

Its jump at zero is one and its distributional derivative is h_s'=delta_0-p_s. Gaussian integration in polar coordinates gives integral p_s=1. Direct integration gives

    integral |h_s(t)|dt=s sqrt(2/pi),
    integral |p_s'(t)|dt=sqrt(2/pi)/s.             (AB2.1)

For alpha_t(T)=exp(itG)T exp(-itG), use bounded vectorwise strong integrals

    R_s(A)=integral p_s(t) alpha_t(A)dt,
    L_s(A)=-i integral h_s(t) alpha_t(A)dt.

The maps have ||R_s(A)||<=r and ||L_s(A)||<=s sqrt(2/pi)r. R_s preserves self-adjointness; L_s(A) is skew-adjoint. Since [alpha_t(A),G]=i d alpha_t(A)/dt in weak domain pairings, integration by parts, including the jump, yields

    [L_s(A),G]=-A+R_s(A).                          (AB2.2)

The sign is fixed by the actual spectral coefficient: for omega=E_m-E_n, L_s has multiplier [1-exp(-s²omega²/2)]/omega at nonzero omega, with continuous value zero at omega=0. The residual multiplier is exp(-s²omega²/2). In particular equal-energy blocks survive exactly; the regulator cannot erase them.

The domain claim does not assume that A initially preserves D(G). First establish the integrated identity against two vectors of D(G), using their differentiable scalar matrix elements and integrability of h_s,h_s'. The bounded right side and self-adjoint adjoint-domain characterization then imply L_s(A)D(G) subset D(G). Explicitly,

    ||G L_s(A)xi||<=s sqrt(2/pi)r ||Gxi||+2r||xi||.

Thus the bounded skew generator and its exponential preserve the actual graph domain. No global sum over all translated generators is asserted.

## Boundary-complete residual and contraction

AB1 retains the actual interior inverse K0 and all origin crossing stars:

    [K0,G]=-A+E,  ||K0||<=r/(1-M),
    E=sum_(c crossing Y)[K0,D_c],
    ||E||<=6M r/(1-M),  M=7|tau|<=35/1664.

The derivatives of alpha_t(K0) are bounded because this commutator is bounded. Since d alpha_t(K0)/dt=i alpha_t(A-E), a second integration by parts gives the exact identity

    R_s(A)=R_s(E)+i integral p_s'(t) alpha_t(K0)dt.
                                                        (AB2.3)

Every retained crossing defect remains in R_s(E). Neither its actual resonant value nor its norm is assumed zero. Equations (AB2.1)-(AB2.3) prove the full-source, all-exterior-sector estimate

    ||R_s(A)||/r <= min(1,[6M+sqrt(2/pi)/s]/(1-M)).
                                                        (AB2.4)

This improves the vacuum-column-only reduction of W2 to an actual full-operator contraction. Since pi>2, sqrt(2/pi)<1. The fixed choice s=4 therefore certifies for every allowed nonzero tau and every finite containing cuboid

    ||R_4(A)||/r <=626/1629 <77/200=0.385,
    ||L_4(A)||<4r.                                 (AB2.5)

A sufficient general threshold is s>1/(1-7M), whose denominator is at least 1419/1664. This follows by comparing the conservative bound using sqrt(2/pi)<1 with one. It is not an optimized threshold. At tau=0, A=E=L_s(A)=R_s(A)=0; no division by r is made. For either nonzero sign, all estimates use |tau| without claiming equal spectra. Removing finite-volume boundary stars improves the same bounds. With no retained crossings, (AB2.4) has no 6M term and the already-known interior inverse is exact.

The 6M/(1-M) limiting term is a nonzero upper-bound floor, not a proved positive lower bound for the actual residual. Letting s grow in this certificate cannot establish norm convergence to zero. In fixed finite volume Gaussian averaging converges strongly to D_G(A), whose actual excited blocks remain uncomputed. Even an eventual proof D_G(A)=0 would not alone supply an operator-norm inverse or summable local construction. The source remains a specified indexed cubic term, not the entire BCH remainder.

## Scales, support and limitations

The physical resolution is delta/s with delta=alpha/8. This proof variable changes neither the action nor the physical clock or positive reference energy. The full support of A is its four-site star tensored with the exterior identity, and K0's boundary defect retains each complete seven-site union. Gaussian time support is unbounded. The old connected-series estimates have only a finite time radius, so integrating those majorants over this Gaussian would be unjustified. No weighted-interaction bound, volume-uniform local generator sum or later-diagonal iteration follows from (AB2.5).

Both terms in (AB2.3) are actual operator expressions. An excited-state fixture checks the commutator sign and retained diagonal multiplier only; it neither approximates SU(2) spectra nor supplies the physical contraction. The latter comes from the actual inherited K0 and complete boundary bound. The source inventory binds all frozen inputs, and explicit exceptions remain active under normal and optimized Python. Scientific priority remains unverified. Full homogeneous inversion, the numerical homogeneous gap and continuum construction remain unresolved.
