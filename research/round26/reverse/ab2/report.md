# AB2 reverse: a bounded Gaussian inverse with full-source contraction

Independent reverse derivation under the frozen AB2 contract; current forward AB2 was not read. The model, source, domain, complete factors, three possible crossing stars and fixed positive physical scales are exactly AB1. Write delta=alpha/8, M=7|tau|<=35/1664, r=||A||. The actual local identity is [K,G]=-A+F, with K skew-adjoint, ||K||<=r/(1-M), F=sum_crossing[K,D_c] self-adjoint and ||F||<=6Mr/(1-M). The source remains A_Y tensor I_ext on every finite containing cuboid.

The new result is an actual full-operator finite-resolution residual smaller than r uniformly in those finite volumes. At proof duration s=2 it obeys

    ||R_2(A)|| <= (1042/1629)r < (2/3)r.          (AB2.R1)

It is a norm contraction for this fixed actual source and initial G. The nonzero retained boundary budget, useful weighted locality and later-diagonal induction remain unresolved.

## Construct the operator before asking for its spectral inverse

For s>0 put p_s(t)=exp[-t²/(2s²)]/(sqrt(2pi)s), alpha_t(B)=exp(itG)Bexp(-itG), and

    R_s(B)=integral_R p_s(t) alpha_t(B) dt,
    h_s(t)=sign(t) integral_(|t|)^infinity p_s(u)du,
    J_s(A)=-i integral_R h_s(t) alpha_t(A) dt.     (AB2.R2)

All integrals are strong vector integrals defining bounded operators, because p_s and h_s are integrable and alpha_t is strongly continuous on each vector. No operator-norm continuity or norm-Bochner integrability is assumed. Gaussian normalization follows by squaring the integral and polar coordinates. Its derivative is p_s'=-t p_s/s²; direct integration on the two half lines gives

    integral p_s=1,
    ||p_s'||_1=sqrt(2/pi)/s,
    ||h_s||_1=E|T|=s sqrt(2/pi),
    h_s'=delta_0-p_s (in distributions).         (AB2.R3)

Thus R_s is a positive average of actual conjugations and ||R_s||<=1, J_s is skew-adjoint for self-adjoint A, and ||J_s(A)||<=s sqrt(2/pi)r<=s r. The last conservative inequality uses pi>=2; exact Gaussian values are retained in the formulas.

Test between two vectors in D(G). Their alpha_t(A) matrix element is differentiable in the weak form, with derivative involving G on the test vectors; A need not preserve D(G). Integration by parts against the integrable bounded-variation h_s, including its jump one at zero and zero boundary values at infinity, gives

    [J_s(A),G]=-A+R_s(A).                         (AB2.R4)

The right side is bounded with norm <=2r. The weak commutator identity and closedness of G imply J_s(A)D(G) subset D(G): the weak expression for GJ_s(A)v is J_s(A)Gv+A v-R_s(A)v, a Hilbert vector for every v in D(G). Hence

    ||J_s(A)v||+||GJ_s(A)v||
      <=[s sqrt(2/pi)r+2r](||v||+||Gv||).

This proves graph preservation without applying G directly to arbitrary A v. The bounded graph action and its Banach-space exponential show exp(plus/minus J_s(A)) preserve D(G) at every finite s. This statement is not a uniform bound for the s->infinity exponential.

At a Bohr difference omega=E_m-E_n the exact multiplier is

    (R_s A)_mn=exp(-s²omega²/2) A_mn,
    (J_s A)_mn=[1-exp(-s²omega²/2)] A_mn/omega,    (AB2.R5)

with continuous zero-frequency multiplier zero for J_s. Formula (AB2.R4) fixes its sign since [J_s,G]_mn=-omega(J_s)_mn. No scalar multiplier bound for an arbitrary double spectral integral is used to infer operator norms: the actual integral norms above prove them.

## Full actual-source residual and the complete boundary term

The inherited K preserves D(G) and has bounded commutator. Hence alpha_t(K) has bounded strong derivative i[G,alpha_t(K)]. Since A=F-[K,G], Gaussian integration by parts yields the exact all-sector identity

    R_s(A)=R_s(F)+i integral_R p_s'(t)alpha_t(K)dt. (AB2.R6)

Every retained crossing contribution stays inside R_s(F), and no spectral matrix element is guessed. Therefore

    ||R_s(A)||/r <= min(1, [6M+sqrt(2/pi)/s]/(1-M)), tau!=0. (AB2.R7)

The estimate is uniform in containing finite cuboids and in both nonzero signs of tau; it does not assert their spectra coincide. At tau=0, A=K=F=R_s(A)=J_s(A)=0 exactly, and ratios by r are not formed. If a cuboid retains fewer crossing stars, replace 6 by twice their number.

Using sqrt(2/pi)<=1 and s=2 gives (AB2.R1) exactly at the maximum M; smaller M only decreases the expression. More generally the simple sufficient condition s>1/(1-7M) gives strict contraction, because 7M<1 throughout the frozen interval. The exact square-root version can improve this sufficient duration, but no optimal s is claimed. The parameter s is dimensionless averaging duration; its physical spectral resolution is delta/s. It changes neither Hamiltonian nor physical experimental clock.

As s grows the upper certificate approaches 6Mr/(1-M), the previously admitted quartic boundary budget. That positive upper floor is not a lower bound on actual residual and does not prove a surviving equal-energy block. Compact-resolvent spectral decomposition in each fixed volume gives R_s(A)->D_G(A) strongly, with the actual diagonal map identified as D_G(F). In addition (AB2.R7) supplies limsup_s ||R_s(A)||<=6Mr/(1-M) directly; this conclusion follows from the boundary identity, not from interchanging norm and strong limit. No norm limit to D_G(A) is asserted.

## Locality and iteration are separate

The Gaussian has nonzero weight at arbitrarily large |t|. The earlier connected Dyson majorant has only a finite time radius. Its pointwise expression cannot be integrated over the whole Gaussian support; multiplying by a decaying Gaussian does not authorize a formula beyond its proven radius. Thus (AB2.R2) and (AB2.R7) establish bounded all-sector operators and the stated norm contraction, but no useful infinite-volume weighted interaction decomposition.

The residual R_s(A) is a new generally nonlocal source. Repeating the same numerical factor as if its source still had AB1's four-factor structure would be invalid. Although Gaussian convolution gives R_s^n=R_(sqrt(n)s) for this fixed G, the available bound approaches the retained boundary budget and does not establish its removal. A changed diagonal G_j also requires new domain, support and source-specific estimates. The scalar, centered diagonal and all generated terms of the original decomposition remain untouched by this fixed-G identity.

Newton's synthesis supplies the bounded inverse/defect reconstruction; Tesla's complete-loading check prevents deletion of F. Historical analogy contributes no coefficient or priority claim. The checker verifies exact cap and duration conditions, both signs and zero, complete crossing geometry, and algebraic homological signs on labeled scalar multiplier controls. The Gaussian analytic integrals and domain proof establish the physical theorem; no generic matrix is represented as the actual SU(2) spectrum.

The finite-resolution target is accepted within scope. Actual resonant block values, a bounded exact all-sector inverse, useful weighted locality, all-stage homogeneous stability, calibration and four-dimensional continuum construction remain open.
