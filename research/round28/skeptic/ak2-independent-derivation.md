# AK2 independent skeptical derivation — before producer exchange

The frozen targets follow for the same actual homogeneous model and original origin xz Wilson: the centered physical vector has form energy at most alpha; at least 1/10 of its spectral mass lies in [alpha/16,10 alpha]; and its connected imaginary-time correlation is at least (1/5) exp[-5 alpha t/hbar] for every finite t >= 0. This report is independently produced after root input preflight and before reading either current AK2 producer. Targets are proved below rather than imported from the selection note. There is no operator-domain or second-moment claim for the infinite-volume vector.

## Frozen premises and source-reading scope

Contract `research/round28/contracts/ak2.json` has SHA256 `ce7044e37b6263bc32767dddbfa28b95860c1c2f54064737a4577f195a6fd601`, sequence ten. All 50 contract sources, the contract and used instructions were copied into 73 immutable owned snapshots. Root's preflight receipt has SHA256 `141e850eff97b91afce6e130d70ea484b2d62ac7b37a30cd59ff1a5c9ce089d3`. The input pack and prior frozen science remain unchanged.

Use real |tau| < tau_* = min(c1(S),1/(2c2(S)))/7 and additionally |tau| <= 2^-16, with fixed |lambda_L|, |lambda_R| <= alpha/2, |mu| <= alpha/8 and alpha,hbar,E_star,a > 0. The source constants remain unevaluated. The cap supplies no evaluated stability interval or selected positive admissible numerical tau.

I1 supplies the actual full-algebra state and bounded-local tested resolvent limit for the specified whole-star positive-orthant volumes. AJ1 supplies the actual normal local restrictions and reducing physical completion. AJ2 supplies the centered physical spectral support away from zero, at least alpha/16. AK1 supplies only the common admitted consequence v = Var(W) >= 1/5 as the numerical premise here; 119/576 is the common producer floor and 131/576 is the independently attributed skeptical refinement. Neither sharper fraction is needed for this contract.

The same reviewer previously read all full controlling AJ1/AJ2/AK1 proofs, and their bytes match the frozen current sources. The 43-page current draft received differential textual coverage against the previously fully read 40-page text: all changed passages, including the complete new AK1 section, were read; unchanged text was matched. This is not a fresh linear 43-page reread or visual PDF review. All five AK1 network nodes and seven incident edges were read. The original preserved arXiv text of Yarotsky's Theorems 2–3 and equation (6), plus the domain/commutator passage around equation (18), was read directly in the frozen retrieval. The full cluster proof and its earlier references were not re-proved. `ak2-source-reading.json` records exact depth; historical material contributes no physical premise.

## 1. Actual finite-volume operator and necessary domains

Let Lambda be any allowed finite coarse volume containing R = {0,e_z}. Each coarse site owns all original links with tails (4b_x+r,2b_y+s,b_z), r=0,1,2,3 and s=0,1; there are eight tails and three positively oriented links per tail. Thus each site owns 24 links. On their complete Haar product let

    C_Lambda = sum over every owned link e of C_e,
    C_e = -sum_{a=1}^3 X_{e,a}^2,
    X_{e,a} f(U_e) = d/dt f(exp(t T_a) U_e)|_{t=0},
    T_a = -i sigma_a/2,  -sum_a T_a^2 = (3/4) I.

This is the Casimir convention of A1/A2/I1: a spin-j matrix coefficient has eigenvalue j(j+1). In physical units the actual operator before actual ground centering is

    delta Hhat_Lambda = alpha C_Lambda + V_selected,Lambda
                       - sum_b E_strip,b + V_omitted,Lambda,
    V_omitted,Lambda = -(alpha tau/24) sum_{b: b+S subset Lambda}
                                          sum_{f in O_b} W_f,
    delta = alpha/8,  S = {0,e_x,e_y,e_z},  |O_b| = 21.

The selected term is the original sum -lambda_L W_L - mu W_M - lambda_R W_R on each complete selected strip. Every selected and omitted magnetic term is a smooth bounded multiplication operator on the actual finite product. They commute with W by multiplication even when their plaquettes overlap. No conditional Haar law in the interacting ground state is assumed.

Let Ehat_Lambda be the actual dimensionless ground energy and Omega_Lambda a normalized actual ground. The positive centered physical operator is

    K_Lambda = delta(Hhat_Lambda - Ehat_Lambda),
    m_Lambda = <Omega_Lambda,W Omega_Lambda>,
    chi_Lambda = (W-m_Lambda) Omega_Lambda.

Ground scalars are retained until this centering. At each finite volume the magnetic potential and reference scalar are bounded, so the self-adjoint operator domain of the bounded perturbation is D(C_Lambda). In particular Omega_Lambda belongs to that domain.

Here is a direct multiplier-domain argument; boundedness alone is insufficient. Finite Peter-Weyl sums form a graph core for C_Lambda. Both W and W squared are finite matrix-coefficient polynomials on the product, and all their first and second X derivatives are bounded. On the core the Leibniz rule gives

    C_Lambda(F psi) = F C_Lambda psi + (C_Lambda F) psi
                     - 2 sum_{e,a} (X_{e,a}F) X_{e,a}psi,
    F = W or W squared.

Moreover sum ||X_{e,a}psi||^2 = <psi,C_Lambda psi>, and the spectral inequality x <= 1+x^2 bounds the form norm by the graph norm. A graph-approximating core sequence therefore makes both F psi_n and C_Lambda(F psi_n) converge. Closedness proves F D(C_Lambda) subset D(C_Lambda). This establishes every finite-volume domain needed below, including W Omega_Lambda and W squared Omega_Lambda. The finite-volume domain constants need not be uniform in volume; the ensuing energy bound is uniform because only four original links differentiate W. No infinite-volume D(H_phys) conclusion is inferred.

## 2. Original-link gradient and the physical coefficient

Write the actual word

    W = (1/2) Tr[U_x(0) U_z(e_x) U_x(e_z)^(-1) U_z(0)^(-1)].

The four link variables are distinct. An original positive factor varies with derivative T_a U and second derivative -U/4; an inverse factor varies with derivative -U^(-1) T_a and second derivative -U^(-1)/4. Thus for **each** of the four links C_e W = 3W/4, irrespective of inverse orientation, and sum_e C_e W = 3W. Every other link derivative is zero.

For one selected original link, cyclically move the fixed factors in the trace so its variation has the form scalar(exp(plus-or-minus t T_a) Q), for a fixed unit quaternion Q (or its conjugate). Write Q = q0 I - i q dot sigma, so q0 = W and |q|^2 = 1-W^2. The three first derivatives are components of q/2 up to an orthogonal rotation and sign. Consequently, pointwise on the complete configuration space,

    sum_a (X_{e,a}W)^2 = (1-W^2)/4,
    Gamma(W) := sum_{all owned e,a} (X_{e,a}W)^2 = 1-W^2.       (1)

This retains four original kinetic terms. It is not a one-plaquette kinetic replacement. Full local endpoint actions telescope around the word and preserve its half-trace; all 48 links and 36 endpoint vertices of R remain present.

On the finite core the differential expression and multiplication of all magnetic terms give

    [W,[K_Lambda,W]] = 2 alpha Gamma(W).

The preceding domain argument extends the matrix element at Omega_Lambda: the terms W K W, W squared K and K W squared are all defined there. Since K_Lambda Omega_Lambda = 0, self-adjointness yields

    mu1_Lambda := ||sqrt(K_Lambda) chi_Lambda||^2
        = <W Omega_Lambda,K_Lambda W Omega_Lambda>
        = (1/2)<Omega_Lambda,[W,[K_Lambda,W]]Omega_Lambda>
        = alpha omega_Lambda(1-W^2) <= alpha.                 (2)

It is also nonnegative. Centering by the moving m_Lambda changes neither this energy nor its derivation because K_Lambda annihilates the actual ground. The factor one-half in the double commutator is essential. The selected and omitted potentials cancel only because they are multiplication operators; their ground state is still the actual interacting state in (2). AK1's reference-density energy is not used as this physical moment.

## 3. Source-qualified limit and form domain, without moment equality

Set chi = (pi(W)-omega(W))Omega and H_phys = delta G_phys in the actual reducing physical space. The inherited local state convergence gives m_Lambda -> m and v_Lambda = omega_Lambda(W^2)-m_Lambda^2 -> v. Each v_Lambda <= 1 because W is a self-adjoint contraction.

Yarotsky's Theorem 3, as matched in I1/AJ1, is convergence of matrix elements of centered resolvents tested on bounded-local vectors, not strong resolvent convergence on an unprovided common concrete Hilbert space. Physical rescaling uses (delta G-z)^(-1) = delta^(-1)(G-z/delta)^(-1). First apply the source statement to the fixed bounded local operator A = W-mI. Replacing A Omega_Lambda by (W-m_Lambda)Omega_Lambda changes a resolvent matrix element by at most

    4 |m_Lambda-m| / |Im z|,

which tends to zero, using ||A||, ||W-m_Lambda|| <= 2. Hence the positive spectral measures nu_Lambda of (K_Lambda,chi_Lambda) converge against every nonreal resolvent to the spectral measure nu of (H_phys,chi). Their masses converge to v by the local state limit. Reduction of the physical subspace preserves this scalar measure.

For clarity, these tested resolvents determine convergence against C0(R): their linear span is closed under conjugation; products with distinct poles reduce by the resolvent identity, repeated poles are uniform limits of such products, and the resulting algebra separates real points and vanishes nowhere. The nonunital Stone-Weierstrass theorem gives density in C0(R). Uniformly bounded measure masses extend convergence to that closure. This is a scalar measure argument, not a common-space operator-domain assertion.

For L>0 put f_L(E) = (L-|E|)_+, a continuous compactly supported function. All measures have nonnegative energy support, and min(E,L) = L-f_L(E) there. Therefore mass convergence and the C0 limit imply

    integral min(E,L) dnu(E)
      = lim_Lambda integral min(E,L) dnu_Lambda(E) <= alpha.

Monotone convergence as L increases proves

    mu1 := integral E dnu(E) <= alpha,
    chi in D(sqrt(H_phys)).                                   (3)

More specifically (2) and local W-squared convergence permit the upper bound mu1 <= alpha[1-omega(W^2)], but no equality with this expression is needed or asserted. A bounded sequence of first moments can lose moment at infinity even when measure masses and bounded tests converge; the explicit control below verifies that distinction. Uniform integrability is not silently supplied. No second moment or infinite-volume operator-domain theorem is claimed.

## 4. Frozen window and lower imaginary-time envelope

The admitted actual centered support is [g,infinity), g = alpha/16, and nu(R)=v>=1/5. Markov's inequality, directly from 1_{E>10alpha} <= E/(10alpha), gives

    nu((10alpha,infinity)) <= mu1/(10alpha) <= 1/10,
    nu([alpha/16,10alpha]) >= v-1/10 >= 1/10.                 (4)

The upper endpoint is included; this is interval mass, not an eigenatom or an identified lowest overlapping energy.

For finite t>=0 use the probability measure nu/v. Its mean mu1/v is finite by (3). The convex tangent inequality for exp(-tE/hbar), integrated at that mean, gives Jensen's bound

    C(t) = integral exp(-Et/hbar) dnu(E)
       >= v exp[-mu1 t/(v hbar)]
       >= v exp[-alpha t/(v hbar)]
       >= (1/5) exp[-5 alpha t/hbar].                         (5)

The last step uses both v>=1/5 and 1/v<=5. At t=0 it is the admitted mass inequality. At every finite t the right side is positive. The distinct inherited upper bound remains C(t)<=v exp[-alpha t/(16hbar)]. Neither imaginary-time inequality entails decay of a real-time magnitude. Alpha is an energy and hbar converts energy times time to a dimensionless exponent; no new time parameter or normalization replaces either.

## 5. Exact controls and retained blind channels

The independent checker reconstructs the whole original 24-link factors, three complete cubes, original four-edge word, all local endpoint actions and retained 21-face interaction groups. Cubes 222,333,444 have respectively 192/648/1536 links, 120/342/736 endpoints and 1/8/27 whole stars. The target region always has 48 links and 36 endpoints. These are algebraic diagnostics; the finite table does not prove the universal domain or thermodynamic argument.

For the differential identity, exact noncommuting rational unit quaternions are varied on each of the four original links. Independent rational Cayley paths have the same first and second jets as exp(t T_a); direct evaluation of the complete word verifies the derivative signs, factor one-half and C_e W=3W/4. The first identity-link normalization fixture has Gamma=0 and cannot detect multiplying the kinetic coefficient: that blind result is retained, then the noncommuting fixture discriminates. Squaring derivatives also hides reversal of an inverse-link first-derivative sign, so that aggregate-only control remains labeled blind; the signed Cayley derivative test detects the error. Full endpoint gauge actions and a missing-head diagnostic retain actual original geometry.

At the explicitly labeled all-zero-coupling free reference corner, W has norm squared 1/4 and physical excitation eigenvalue 3 alpha, hence moment 3 alpha/4. This agrees with (2), not a replacement of the nonzero-coupling state by Haar. Incorrect kinetic normalization or omission of the double-commutator half-factor fails this normalization control. Physical alpha=24, delta=3, hbar=5 examples discriminate omission of delta, actual ground centering and the hbar conversion; a joint additive ground shift cancels exactly.

Bounded locality alone is tested on the same free original-link space with an auxiliary observable, not W. Let phi_n be the spin-n/2 character of the same four-link holonomy. Conditional Haar and character orthogonality give ||phi_n||=1, pairwise orthogonality, and physical energy alpha n(n+2). The vector

    f = sqrt(3) sum_{k>=1} 2^(-k) phi_(2^k)

has norm one, is gauge invariant and orthogonal to the vacuum. Its N-term norm squared is 1-4^(-N), while its form-energy prefix divided by alpha is 3N+6(1-2^(-N)), which diverges. The bounded local physical self-adjoint rank-two operator A=|f><Omega|+|Omega><f| has norm one but A Omega=f outside the free form domain. This falsifies the bounded-local inference without denying the separately proved smoothness of W.

For moment loss, in units alpha define the abstract diagnostic measures

    eta_n = (1/5-1/(10n)) delta_(1/16) + (1/(10n)) delta_n, n>=1.

Their masses are 1/5, their bounded-test difference from eta=(1/5)delta_(1/16) is at most ||f||/(5n), and their first moments are 9/80-1/(160n), tending to 9/80. The limiting measure's first moment is only 1/80: 1/10 is lost at infinity. These are abstract measures, not observations of the actual state.

The free auxiliary multiplier W+1/2 adds vacuum mass 1/4 to its uncentered spectral measure; its centered measure has only mass 1/4 at 3 alpha. This detects noncentered vacuum contamination. Conversely the abstract measure (1/5)delta_(11alpha) has the admitted mass and lower gap but zero mass in the proposed finite window and heat below the proposed lower envelope for t>0. Its first moment violates the new premise, showing exactly why variance plus a lower gap alone does not prove (4) or (5). An additional endpoint fixture retains mass at 10alpha inside the closed window. These controls claim no actual spectral atoms or real-time decay.

## Accepted scope and stopping boundary

The finite original-link/domain calculation and the source-qualified upper-moment transfer prove the three frozen consequences (3)–(5). This is investigation ten within the same specified homogeneous state, coupling intersection, positive physical scales and original observable. It establishes neither equality of first moments across the limit nor D(H_phys), a second moment, an eigenatom, a lowest overlapping energy, a numerical stability interval, other-boundary identification, a continuum Yang-Mills construction, scientific priority or a defensible completion percentage. After this investigation's independent freeze and review, any further goal is planning only; no eleventh scientific investigation is authorized here.
