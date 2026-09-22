# Hruday same-state Wilson energy certificate — independent reverse AT1

Human author: **Hruday N M (BUNZEEY)**. AI-assisted mathematical reconstruction and exact controls. HNM labels are project aliases, not priority claims; scientific priority remains unverified. The current forward and skeptic AT1 solutions were not read. The contract, inherited reports, gates and primary-source excerpt are copied in `inputs/`. Newton's backward-analysis method and Tesla's complete-system energy accounting motivate the workflow; neither historical authority nor mystical material supplies a mathematical premise.

## 1. Reverse target and necessary bridge

The target is the actual AQ1/AQ2 centered-full-Z3 subsequential state, not the older AO orthant state. To prove a local Wilson vector belongs to the domain of its actual energy generator, the spectral theorem requires a finite second energy moment in that same representation. Compact spectral-test convergence plus a uniform finite-volume second-moment bound suffice. To obtain an exact first-moment identity, the same bound supplies the missing uniformly integrable first-energy tails. A mere first-moment ceiling would be insufficient. This identifies the finite regional kinetic estimate, full commutator and same-state Fourier convergence as the necessary bridge; each is established below.

Keep exactly AQ's chosen subsequence of centered whole-star boxes, fixed repeated selected coefficient triple, and complete original 24-link SU(2) factors. Fix positive physical energy alpha, action hbar, spacing a and comparison energy E_star; delta=alpha/8. Both signs of tau with |tau|<=10^-8 are allowed. The spectral cutoff L>0 used below has energy units and is a proof parameter, not an interaction deformation. No symbolic smallness threshold from AO is assumed.

AQ1 provides locally normal compatible limits and the physical-time stationary dynamics. AQ2 gives its reducing physical sector, gap alpha/16 and nonzero original Wilson fluctuation. Write H=H_phys, U_t=exp(itH/hbar), H Omega=0, and

\[
 W=\tfrac12\operatorname{Tr}[U_x(0)U_z(e_x)U_x(e_z)^{-1}U_z(0)^{-1}],\quad
 \chi=(\pi(W)-\omega(W))\Omega,\quad
 \nu(B)=\langle\chi,\mathbf1_B(H)\chi\rangle.\tag{HNM-AT1-R01}
\]

The corresponding finite quantities are K_N=H_N^raw-E_N^raw, m_N=omega_N(W), chi_N=(W-m_N)Omega_N and nu_N. Their measures have support in [alpha/16,infinity) and mass at most one. This inherited gap is not needed for the moment proof except to preserve the exact physical state and positive-energy setting.

## 2. Complete geometry and seven-star reset

The coarse factor b=(i,j,k) owns every positive-direction original link with tail (4i+r,2j+s,k), 0<=r<4, 0<=s<2. The four stored Wilson links have owners 0,0,e_z,0; inverse occurrences retain the original stored link and its original endpoints. The complete region R={0,e_z} therefore contains 48 links. Its 16 tail vertices plus outgoing boundary slabs of sizes 4,8,8 give 36 endpoint actions. All remain present, including heads outside the tail box.

A whole-star support is b+S, S={0,e_x,e_y,e_z}. The incident anchors are precisely R-S:

\[
 \{0,-e_x,-e_y,-e_z,e_z,e_z-e_x,e_z-e_y\}.\tag{HNM-AT1-R02}
\]

There are seven, as set enumeration and the shared anchor 0 show. Near a finite boundary there can be fewer retained stars, never more. For sufficiently large centered boxes all seven are retained. An origin region in the positive orthant instead meets only anchors 0,e_z; its two-star budget cannot be used here.

Reset the reduced state on R to the product of the actual selected-reference vacua while preserving its exterior marginal. Outside onsite energies are unchanged; bounded spectral truncation and monotone convergence justify this for unbounded energies. The actual finite-volume full ground energy, admitted in AQ's premises, permits this full-Hilbert mixed trial. All terms disjoint from R agree. Each incident star has normalized operator norm <=7|tau| and its expectation changes by at most twice that norm. Hence

\[
 \omega_N(h_R)\le 2\cdot7\cdot7|\tau|=98|\tau|.\tag{HNM-AT1-R03}
\]

This is a bound for the selected reference energy. It is not yet the pure kinetic energy or the Wilson excitation energy.

## 3. Reconstruct kinetic energy with all scalar terms

For a complete factor b, let Q_b=sum_(e in b) C_e, C_e=-sum_a X_ea^2 with half-Pauli generators i sigma_a/2. The exact dictionary is

\[
 \delta h_b=\alpha Q_b-\sum_{p\in b,selected}\lambda_pW_p-E_{strip,b},
 \qquad \sum_{p\in b,selected}|\lambda_p|\le9\alpha/8.\tag{HNM-AT1-R04}
\]

The ground scalar is that of the actual selected strip, not zero by convention. The constant Haar trial has zero kinetic expectation and zero selected Wilson means, so E_strip,b<=0. Rearranging (R04), summing the two factors and only then dropping its nonpositive scalar contribution gives

\[
 \omega_N(Q_R)\le\tfrac18\omega_N(h_R)+\tfrac94
 \le\tfrac94+\tfrac{49}{4}|\tau|.\tag{HNM-AT1-R05}
\]

All 48 regional links enter this estimate. Positivity permits the kinetic form on just the four Wilson links to be bounded by Q_R. The selected potential cannot generally be discarded: at an allowed nonzero one-face coefficient lambda, the Haar-based trial 1+tW has energy numerator 3alpha t^2/4-lambda t/2. Choosing t=lambda/(3alpha) makes it negative. Thus even at tau=0 the true selected ground generally differs from Haar and its raw ground scalar is negative.

## 4. Finite domains, derivatives and first-moment identity

At fixed N the full compact manifold is SU(2) to the number of owned original links. Its elliptic Q_N has operator domain H^2 and form domain H^1. Every selected and omitted Wilson potential is bounded, real and smooth. Therefore H_N^raw=alpha Q_N+V_N is self-adjoint on H^2, with form domain H^1 and compact resolvent. The actual ground vector belongs to H^2. Multiplication by W, W^2, W-m_N and (W-m_N)^2 preserves H^2 and H^1: use their bounded derivatives through order two and the weak Leibniz rule, initially on smooth functions and then by completion. No volume-uniform global potential norm is needed for these fixed-volume domain statements.

The exact finite physical subtraction is

\[
 \delta\widehat H_N=H_N^{raw}-\sum_bE_{strip,b},\quad
 E_N^{raw}=\sum_bE_{strip,b}+\delta\widehat E_N,\quad
 K_N=\delta(\widehat H_N-\widehat E_N).\tag{HNM-AT1-R06}
\]

Both scalars are retained before cancellation. Selected and omitted magnetic multipliers and these scalars all commute with W.

Write the Wilson holonomy as a unit quaternion (w,v). For one positive link, left variation by a half-Pauli generator gives scalar derivatives equal to the components of -v/2 after an orthogonal adjoint rotation. For an inverse stored link, d(U(t)^-1)/dt=-U^-1 T_a when U(t)=exp(tT_a)U; the sign and right-multiplication placement are retained. Left/right multiplication, inversion and adjoint rotation preserve the quadratic sum. Since T_a^2=-I/4, each of the four distinct link occurrences satisfies C_e W=3W/4 and contributes (1-W^2)/4 to the gradient square. Thus

\[
 Q_NW=3W,\qquad \Gamma(W):=\sum_{e,a}(X_{ea}W)^2=1-W^2.\tag{HNM-AT1-R07}
\]

Now put f=W-m_N. Expand the form on f Omega_N and subtract the real part of the ground equation tested against f^2 Omega_N. For each X the kinetic integrand difference is

\[
 |X(f\Omega_N)|^2-\Re\{\overline{X\Omega_N}X(f^2\Omega_N)\}
 =(Xf)^2|\Omega_N|^2.\tag{HNM-AT1-R08}
\]

All scalar and multiplication terms cancel. The established domains justify the ground test. Consequently, without differentiating a limiting correlation,

\[
 \mu_{1,N}=\langle\chi_N,K_N\chi_N\rangle
 =\alpha\omega_N(\Gamma(W))=\alpha\omega_N(1-W^2).\tag{HNM-AT1-R09}
\]

Equivalently one half of the ground expectation of [W,[K_N,W]] gives the same identity; the double commutator is 2alpha times multiplication by Gamma(W). This one-half factor is essential.

## 5. Complete commutator and finite second moment

The finite domain statements allow the actual L2 identity

\[
 K_N\chi_N=\alpha[Q_N,W]\Omega_N
 =\alpha(3W\Omega_N-2S_N),\quad
 S_N=\sum_{e,a}(X_{ea}W)(X_{ea}\Omega_N).\tag{HNM-AT1-R10}
\]

The first commutator is not claimed to be bounded. Pointwise Cauchy–Schwarz and (R07) show |S_N|^2<=(1-W^2) sum_(four links,a)|X_ea Omega_N|^2. Integrating bounds its L2 norm squared by omega_N(Q_R). Using (x+y)^2<=2x^2+2y^2 and |W|<=1 yields

\[
 \mu_{2,N}=\|K_N\chi_N\|^2
 \le\alpha^2[18+8\omega_N(Q_R)]
 \le B_2:=\alpha^2(36+98|\tau|)<37\alpha^2.\tag{HNM-AT1-R11}
\]

At the maximal cap B2/alpha^2=1800000049/50000000. The gradient cross term cannot be deleted: applied to the test vector W, Q_N(W^2)=8W^2-2, hence [Q_N,W]W=5W^2-2 rather than 3W^2. The bounds cover every finite centered whole-star box containing R and every allowed selected triple, with either sign of tau. They retain the actual reference potential and energy clock.

## 6. Compact spectral tests in AQ's actual representation

No common finite/infinite Hilbert space is assumed. AQ1's dynamics converge in norm on every bounded local observable, uniformly on compact physical time intervals. Its chosen states converge in trace norm on every finite region. Approximate the evolved W by the evolution inside one fixed large region; the norm error is uniform on a fixed time interval, and trace-norm state convergence controls the bounded local expectation. Thus

\[
 \omega_N(W\alpha_t^N(W))\longrightarrow\omega(W\alpha_t(W)).\tag{HNM-AT1-R12}
\]

uniformly on compact times. Local convergence gives m_N->m. Therefore the actual centered correlations

\[
 C_N(t)=\omega_N(W\alpha_t^N(W))-m_N^2
 =\int e^{itE/\hbar}d\nu_N(E)
 \longrightarrow C(t)=\int e^{itE/\hbar}d\nu(E).\tag{HNM-AT1-R13}
\]

Their masses are variances and are <=1, so the correlations are uniformly bounded. For f in C_c^infinity(R), use physical-energy Fourier inversion f(E)=integral k_f(t) exp(itE/hbar)dt, with k_f integrable. Bounded correlations and dominated convergence give integral f dnu_N -> integral f dnu. Smooth compact tests are uniformly dense in C_0(R); the common mass bound extends this convergence to every C_0 test. This is a passage of scalar spectral measures for the actual Stone generator, not a formal differentiation or a strong-resolvent statement across different spaces. AQ2's original-endpoint gauge proof places chi in the reducing physical sector.

## 7. Second-moment inequality, domain and exact first moment

For E>=0 set theta_L(E)=1 on [0,L], 2-E/L on [L,2L], and zero above 2L. Let f_L(E)=E theta_L(E) and g_L(E)=E^2 theta_L(E), extending both by zero to E<0. These are continuous compactly supported functions, nonnegative, and increase pointwise to E and E^2 as L increases. Compact-test convergence and (R11) imply integral g_L dnu<=B2. Monotone convergence gives

\[
 \int E^2d\nu(E)\le B_2,\qquad
 \chi\in D(H),\qquad\|H\chi\|^2=\int E^2d\nu(E).\tag{HNM-AT1-R14}
\]

The equality here is the spectral-domain characterization for the limiting generator. It is not equality with the limiting sequence of finite second moments.

For all finite volumes and for the limiting measure,

\[
 \int_{E>L}E\,d\nu_N(E)\le B_2/L,
 \qquad\int_{E>L}E\,d\nu(E)\le B_2/L.\tag{HNM-AT1-R15}
\]

This follows pointwise from E<=E^2/L on that tail and supplies the required uniform integrability. Moreover 0<=E-f_L(E)<=E 1_(E>L). The bounded-local right side of (R09) tends to alpha omega(1-W^2). For each L, take N to infinity in

\[
 0\le\alpha\omega_N(1-W^2)-\int f_L\,d\nu_N\le B_2/L.\tag{HNM-AT1-R16}
\]

Then let L increase to infinity using monotone convergence. The exact same-state energy certificate is

\[
 \boxed{\langle\chi,H\chi\rangle=\int E\,d\nu(E)
 =\alpha\omega(1-W^2),\qquad
 \|H\chi\|^2\le\alpha^2(36+98|\tau|)<37\alpha^2.}\tag{HNM-AT1-R17}
\]

The left inner product is justified by the operator domain already proved. No hbar belongs in an energy moment; H/hbar would instead give frequency moments. Division by E_star expresses all energies on the declared common physical comparison scale without changing the model.

## 8. Executed counter-inferences and scope

The exact standard-library checker reconstructs all link/endpoints and incident stars, evaluates noncommuting rational-quaternion derivative fixtures including inverse signs, and checks scalar, tail and normalization controls. Its named controls execute genuinely different values:

- Two-star substitution gives coefficient 28 instead of the required seven-star 98; centered geometry rejects it.
- A nonzero selected-face trial has negative raw energy, rejecting a pure-electric Haar reference with zero scalar.
- The computed Q(W^2) and commutator on W reject omission of the gradient cross term. The inverse-sign derivative square is insensitive to a global sign, so an additional derivative of U U^-1 rejects that sign error.
- Free-reference first and second moments scale as alpha and alpha^2. Doubling the generators quadruples energy and multiplies the second moment by sixteen. Ground shifts, the one-half double-commutator factor and hbar frequency conversion are separately exercised.
- A two-state matrix example has an uncentered zero-energy contribution that disappears under the actual mean subtraction; positive moments alone cannot detect that change in mass.
- The abstract family (1-1/n)delta_g+(1/n)delta_(g+n/2), g=1/16, has first moment 9/16, but second moment g^2+g+n/4. Its bounded-test limit is delta_g. It rejects first-moment equality from bounded first moments alone.
- The abstract family (1-1/n^2)delta_g+(1/n^2)delta_(g+n) has second moments g^2+2g/n+1, uniformly bounded; its limiting measure delta_g has second moment g^2. This rejects finite-to-infinite second-moment equality under the proved assumptions.
- Two explicit normalized ground states for two positive gapped matrix Hamiltonians both satisfy a variance floor above 1/5 yet give different Wilson means. Common gap/variance properties therefore do not identify states. These fixtures are logical controls, not claimed AQ or AO states.

No second-moment convergence, identification of AQ with AO/AN, whole-sequence or all-ground-state uniqueness, particle pole, exact mass, dispersion or continuum Yang–Mills claim follows. No new axiom is introduced.

The nearest checked primary source is Gauvin, arXiv:2503.15539v3, Supplement A.9–A.10: its ground-state Wilson energy identity and compactness/dynamics/Fourier construction are directly relevant established proof patterns. The copied selected-page excerpt was read. Its SU(3), pure-electric link dictionary and numerical constants are not imported. The new work here is a same-state SU(2) application retaining AQ's selected onsite potential, full 48-link geometry and seven-star numerical second-moment coefficient. AQ's dynamics remain source-matched to Nachtergaele–Sims, arXiv:1410.8174v1. The current abstract/version pages were checked; no broad literature-priority claim is made.

Reproduce with `python -B research/round30/reverse/at1/check.py --output /absolute/fresh-directory`. The checker requires a fresh absolute directory, copied-source hashes and explicit exceptions, so optimized Python cannot disable gates. Normal and optimized output bytes are compared. The manifest binds deterministic report/code/input bytes; freeze.json binds every owned scientific source and output. This ends reverse AT1 production. No next loop is selected or executed here.
