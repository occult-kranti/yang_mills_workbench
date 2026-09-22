# HNM numerical-cap physical gap and Wilson witness — independent reverse AQ2

Project author: Hruday N M (BUNZEEY). Gauge averaging and Fourier gap passage follow the generic strategy already explicit in Gauvin's supplement A.10. The contribution here is its actual SU(2) selected-strip placement, complete endpoint algebra and seven-star witness at AM2's numerical cap; scientific priority is unverified. No current forward/skeptic AQ2 output was read. This is investigation ten and ends scientific production.

## Same state and physical clock

Use exactly AQ1's chosen locally normal subsequential state omega from centered full-Z³ whole-star boxes, with fixed repeated selected triple, |tau|<=10^-8, and its stationary strongly continuous GNS dynamics U_t=exp(it H_infinity/hbar). Fixed alpha,hbar,a,E_star>0 and delta=alpha/8 remain. AQ1 gives H_infinity>=0. No old tau_*, HTW constant, orthant state identity or AO2 moment/domain statement is used. Finite AM2 physical gaps are g=alpha/16; the separately reviewed full-Hilbert strengthening will be explicitly named where used.

## 1. Complete original-endpoint gauge sector

Let G be the compact product of SU(2) over every original lattice vertex. Each full bounded local operator depends on finitely many link factors; its gauge action depends on finitely many original endpoints and is strong-star continuous in those variables. It need not be norm continuous. Such an action agrees locally with a finitely supported gauge assignment, so AQ1's state invariance extends to G.

The implementing operators V_g pi(A)Omega=pi(beta_g(A))Omega are unitaries. Local normality makes omega(A* beta_g(A)) continuous in the finitely many relevant parameters: bounded strong-star convergence paired with a trace-class local density is continuous. The usual squared-vector-difference identity proves strong continuity of V_g on local cyclic vectors and then on their dense span. Thus vectorwise Haar averaging defines the orthogonal projection P_phys onto the joint fixed subspace. Finitely supported gauge assignments are dense in the compact product, so their joint fixed subspace is the same.

For local A, define E(A) by a **weak/ultraweak** Haar integral of beta_g(A) over the finitely many original endpoint groups. It is bounded, local and invariant. This is not a norm-Bochner integral of an arbitrary B(H_R) orbit. Pairing against local cyclic vectors and using the normal local state permits the integral to pass through omega(B* beta_g(A)). Consequently

\[
P_{\rm phys}\pi(A)\Omega=\pi(E(A))\Omega,
\qquad
\mathcal H_{\rm phys}=\overline{\{\pi(A)\Omega:A\text{ bounded, local, gauge invariant}\}}. \tag{HNM-AQ2.1}
\]

The density follows by applying the bounded projection to the dense local cyclic span. The fixed space is not obtained by tensoring independently gauge-fixed coarse factors; endpoint transformations are shared by neighboring factors. Every finite Hamiltonian commutes with original gauge actions, hence its norm-limit dynamics does too. Therefore U_t commutes with V_g and P_phys, and this physical space reduces the actual Stone generator.

## 2. Centered spectral passage, including zero

For any bounded local gauge-invariant A, let m_Lambda=omega_Lambda(A), m=omega(A). The finite centered physical vector (A-m_Lambda)Omega_Lambda has spectral measure supported on [g,infinity) by AM2. Local trace-norm convergence gives m_Lambda→m and mass convergence omega_Lambda(A*A)-|m_Lambda|²→omega(A*A)-|m|². The modulus is essential for complex means.

AQ1's compact-time correlation convergence and the moving-mean identity

\[
C_\Lambda(t)=\omega_\Lambda(A^*\alpha_t^\Lambda(A))-|m_\Lambda|^2
\]

give the Fourier transform of the actual limiting measure on chi_A=(pi(A)-m)Omega. For every smooth compactly supported physical-energy test f in (-infinity,g), Fourier inversion and dominated convergence pass its integral through these bounded correlations. Every finite integral is zero, so the limit is zero. Nonnegative tests exhaust that whole interval, **including a neighborhood of zero**. Thus the limiting centered measure is supported on [g,infinity).

The centered invariant local vectors are dense in H_phys intersect Omega-perp by (HNM-AQ2.1). The spectral projection onto [0,g) annihilates that dense subspace; hence

\[
H_{\rm phys}:=H_\infty|_{\mathcal H_{\rm phys}}
\ge {\alpha\over16}(I-P_\Omega),\qquad
\ker H_{\rm phys}=\mathbb C\Omega. \tag{HNM-AQ2.2}
\]

This is a physical energy gap, with frequency gap alpha/(16hbar). An additive raw scalar cancels only when the actual ground energy is subtracted. Testing only the open interval (0,g) would fail to rule out an additional zero-energy vector.

**Full-GNS strengthening:** AM2's separately reviewed full-Hilbert gap permits the same centered argument for arbitrary bounded local A, without the gauge-invariant restriction. Those vectors are dense in the full GNS space, so H_infinity>=g(I-P_Omega) there too. This stronger conclusion uses that distinct admitted premise; the physical restriction above does not depend on silently replacing a physical gap by a full-space gap.

Vacuum simplicity is within this chosen representation. It is not a theorem of unique thermodynamic state, whole-sequence convergence, translation invariance, boundary independence or equality with the old orthant state.

## 3. Nonzero actual Wilson signal on the full lattice

Use W=Tr[U_x(0)U_z(ex)U_x(ez)^(-1)U_z(0)^(-1)]/2. Its four signed links have owners 0,0,ez,0. The complete factor region R={0,ez} contains 48 links and 36 distinct original endpoints. The incident anchors are

\[
\{0,-e_x,-e_y,-e_z,e_z,e_z-e_x,e_z-e_y\},
\]

seven in total. The old positive-orthant two-star budget does not apply. AQ1's actual reset argument gives <h_R><=98|tau| in finite boxes and in omega: pass bounded spectral truncations of positive h_R and then use monotone convergence. Since h_R>=I-P_R, where P_R is the product of the **actual selected-reference** onsite vacua,

\[
1-\operatorname{Tr}(\rho_RP_R)\le\epsilon:=98|\tau|,
\quad\|\rho_R-P_R\|_1\le2\sqrt\epsilon.
\]

Each selected strip uses only xy links, so an original z link in W is a genuinely free independent Haar link in this reference. Conditioning on all other links makes its plaquette product Haar distributed. SU(2) quaternion symmetry gives reference W mean zero and W² mean1/4. These are reference moments only. Trace duality then yields |omega(W)|<=2sqrt(epsilon) and omega(W²)>=1/4-2sqrt(epsilon), so the actual interacting variance obeys

\[
\operatorname{Var}_\omega(W)\ge\frac14-2\sqrt{98|\tau|}-392|\tau|.
\]

At |tau|<=10^-8, sqrt(98|tau|)<1/1000. Therefore

\[
\operatorname{Var}_\omega(W)\ge {3099951\over12500000}>{1\over5}. \tag{HNM-AQ2.3}
\]

The corresponding centered Wilson vector is a nonzero physical vector in this same numerical-cap GNS state. This makes the positive-gap sector nonvacuous. No operator-domain or first-moment identity from AO2 is imported into this state.

## Exact controls and stop boundary

A centered diagnostic measure with mass1/2 at zero and1/2 at2g passes every test supported inside (0,g), but a test near zero detects it. It can be realized by a centered vector in a degenerate ground space, showing why centering alone does not rule it out.

An exact quaternion endpoint fixture transforms the closed Wilson to itself when all heads/tails act; a tails-only assignment changes its half-trace from1 to0. A two-spin singlet is fixed by the joint SU(2) action while its factors have no singlets, rejecting a general physical tensor-factorization shortcut. Further exact controls check complex centering, actual ground subtraction, seven versus two stars, reference-versus-interacting variance and energy/frequency scales.

Run `python research/round29/reverse/aq2/check.py --output /absolute/new-directory`. Normal and optimized results agree, with source packets, report, code and output bindings in the manifest/freeze. The analytic arguments prove the full-sector and limiting claims; the finite fixtures are controls. After this freeze/review, no additional scientific loop is executed. Further work is planning, presentation and publication.
