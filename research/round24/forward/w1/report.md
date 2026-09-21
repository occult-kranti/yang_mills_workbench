# W1 forward — actual residual persistence and a spectral certificate

Independent forward analysis of the S1/S2 source, before current reverse work. Newton's inverse test asks which full operator data are missing; Tesla's loading test keeps exterior sectors. Historical analogies enter no coefficient. The result is actual short-filter residual persistence plus a quantitative **conditional** spectral certificate, not a uniform evaluated residual-removal theorem.

## Actual source and retained identity

Use exactly S1's initial homogeneous complete24-link block model, not the canonical q model. On Y=Z_0 write v=phi_0 Omega_Y, u=H_Y,Q^-1 v, a=<u,v>, beta=||u||², sigma²=||v||²=7tau²/12. The actual indexed cubic term gives

    w=-a u-(beta/3)v,
    r²=||w||²=(5/3)a² beta+(beta²/9)sigma²,
    <u,w>=-(4/3)a beta<0 for tau≠0.                (W1.1)

The source is A=(|w><Omega_Y|+adjoint) tensor I_ext, ||A||=r>0. It is one specified repeated-anchor term; neither the total cubic coefficient nor the complete remainder is identified with A. The original scalar bI and centered diagonal Q(C-bI)Q remain in their S1 decomposition.

For actual self-adjoint initial G in a finite retained-star cuboid, or the S2-identified R2 product-reference representation, retain the strong integrals

    R_Theta(A)=(1/(2Theta)) integral_-Theta^Theta exp(isG)Aexp(-isG) ds,
    [L_Theta(A),G]=-A+R_Theta(A), ||R_Theta(A)||≤r.   (W1.2)

S2 proves L preserves D(G), including the infinite representation without equating D(G) and D(H0). Every outside sector and all crossing stars remain. S2's rooted weight-2 certificate also remains valid: with M=7|tau|, c=192M, p=8/3,

    ||R_Theta(A_family)||_weight2≤64r_*(1-cTheta)^(-p),
    cTheta≤105/416<1.                              (W1.3)

This is an upper interaction budget, not contraction of the source.

## Actual vacuum-column formula and what it can prove

The product vacuum Omega is in ker G because H0 Omega=0 and each Q_b phi_b Q_b annihilates it. Put xi=A Omega=w tensor Omega_ext, ||xi||=r. Let nu(B)=||E_G(B)xi||²/r² be its normalized spectral measure. Nonnegativity of G puts nu on [0,infinity). This measure is **derived from the actual source and actual G**, not an adjustable spectrum. The spectral theorem gives the exact formula

    R_Theta(A)Omega = sinc(Theta G)xi,
    ||R_Theta(A)Omega||²/r²
      = integral sinc²(Theta lambda) dnu(lambda).  (W1.4)

This vector formula uses an ordinary scalar spectral measure. It is not a claim that a pointwise scalar multiplier bound gives the full operator norm of an arbitrary double spectral integral.

For any finite energy cutoff E>0 let m(E)=nu([0,E]). If 0<Theta E≤1, elementary sine bounds yield sinc(x)≥1-x²/6≥5/6 on [0,1]. Therefore

    ||R_Theta(A)|| ≥ ||R_Theta(A)Omega||
                  ≥ (5/6) r sqrt(m(E)).            (W1.5)

This is a useful quantitative conditional certificate: the single actual datum m(E)≥p gives a rigorous full-operator **lower** bound (5/6)r sqrt(p). It supplies no full-operator upper bound or all-exterior-sector frequency control.

There is also an unconditional qualitative consequence for this actual source. Because nu is a probability measure, some finite E has m(E)≥1/2. For that source/volume or that fixed infinite representation, every 0<Theta≤min(1/16,1/E) satisfies ||R_Theta(A)||≥5r/(6sqrt(2))>0. No evaluated numerical E or uniformity across changing volumes is claimed. This proves actual residual nonvanishing for sufficiently short filters; a generic resonant matrix is not the basis of this statement.

More precisely, dominated scalar convergence in (W1.4) gives R_Theta(A)Omega→xi as Theta→0. Since ||R_Theta(A)||≤r, while its vacuum-column norm tends to r,

    lim_(Theta→0+) ||R_Theta(A)||/r=1.              (W1.6)

Thus shortening the filter retains essentially the entire actual source in operator norm size. Equation (W1.6) does not claim operator-norm convergence R_Theta(A)→A, nor any conclusion as Theta→infinity. Tau=0 is the exact exception r=0. Reversing nonzero tau preserves the nonvanishing conclusion; nu can change with the actual G and must not be assumed unchanged.

A convenient alternative input is an evaluated first spectral moment mu=int lambda dnu<infinity. Markov's inequality gives m(E)≥1-mu/E and hence

    ||R_Theta(A)||≥(5/6)r sqrt(max(0,1-mu Theta))    (Theta E=1). (W1.7)

An unevaluated mu is not a number the advisor may fit. This report does not need moment regularity for (W1.4)–(W1.6). Establishing an actual source-energy/form bound uniform in volume would make (W1.7) effective; it is a specific next datum.

## Why the column cannot close the all-sector problem

For every actual equal-energy projection, P_E R_Theta(A)P_E=P_E A P_E. The product-vacuum column can be entirely gapped while a source block between excited sectors survives. No actual such forbidden excited block is proved here. In particular a lower bound from (W1.5) at short Theta is not a theorem forbidding an unregulated inverse at large Theta.

A sufficient full-operator condition for residual removal is explicit: if a bounded K preserving D(G) solves [K,G]=-A, integrate the strong commutator identity to obtain

    R_Theta(A)=(alpha_Theta(K)-alpha_-Theta(K))/(2iTheta),
    ||R_Theta(A)||≤||K||/Theta.                     (W1.8)

The sign follows d alpha_s(K)/ds=i alpha_s([G,K])=i alpha_s(A). This is a sufficient criterion, not a construction of K; invoking it as if known would restate the unsolved homological equation.

For clarity, the exact convention throughout is [K,G]=-A, so [G,K]=A and R_Theta(A)=(alpha_Theta(K)-alpha_-Theta(K))/(2iTheta). Any proposed full inverse needs equal-energy blocks zero, bounded operator control across all excited energy differences, graph preservation, and summable connected supports. A ground-state gap supplies only one part of this information. To pass from L_Theta to an unfiltered K one additionally needs convergence of the filtered generators in a useful norm with a bounded commutator limit; pointwise sinc decay is insufficient.

Later-diagonal G_k changes are separate obligations: retain its complete support decomposition, scalar and diagonal parts, actual reference projection, common closed forms/domains, and a quantitative residual or homological certificate for A_k. Neither (W1.5) nor S2's initial-G limit establishes that induction.

## Verification and scope

The checker recomputes the source norm and inner-product identities from exact rational vectors, the spectral lower certificate and positive-series radius. A separate computed excited-sector fixture verifies that a vanishing tested vacuum residual need not imply a zero full residual. That fixture is labeled a logical counterexample and never substituted for actual SU2 data. Sinc bounds are certified by their alternating-series sign on [0,1], not by a grid. The source-specific conclusions (W1.4)–(W1.6) are infinite-Hilbert-space proofs from S1's actual nonzero source and the spectral theorem; fixtures only check algebra.

No new external theorem is imported beyond the inherited S2 spectral/strong-integral framework; all new inequalities are proved above. Theta is dimensionless proof duration, with physical resolution delta_energy/Theta and delta_energy=alpha/8; E and mu are derived dimensionless energies, physically delta_energy times these numbers. Positive a,E_star,alpha/E_star,hbar stay fixed. Scientific priority is unverified. Actual uniform moment evaluation, full excited-sector spectral control, later-diagonal closure, homogeneous gap and continuum construction remain open.
