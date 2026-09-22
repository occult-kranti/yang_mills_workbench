# AO1 forward: HNM finite Wilson second-moment bound

Human project author: **Hruday N M (BUNZEEY)**. Independent forward derivation of the shared prospective commutator route, without reading current reverse or skeptic results. The method uses standard product rules; scientific priority is unverified.

**Finite-volume result:** the original origin xz Wilson in every contracted actual whole-star orthant ground state satisfies

\[
\int E^2d\nu_\Lambda(E)=\|K_\Lambda\chi_\Lambda\|^2
\le\alpha^2(36+28|\tau|)
\le\alpha^2(36+7/16384)<37\alpha^2.\tag{HNM-AO1.1}
\]

Here `chi_Lambda=(W-omega_Lambda(W))Omega_Lambda` and `K_Lambda=Hraw_Lambda-Eraw_Lambda` is the actual centered physical operator. The inherited `|tau|<tau_*` and `|tau|<=2^-16` remain in force. Reference-ground energy is not an excited-vector spectral moment.

## Exact local kinetic reconstruction

The complete cover is R={0,e_z}: 48 links and 36 endpoint actions. Its actual orthant incident anchor union is `(R-S) intersect Z_+³={0,e_z}`, counting the star at zero once. AK1 therefore gives `omega_Lambda(h_R)<=28|tau|`.

Let `T_R=alpha sum_(e owned by R)C_e`, `Vsel_R=-sum_(selected faces in R)lambda_f W_f`, and `B_R=sum_(b in R)Estrip_b`. Keeping every selected ground scalar,

\[
\delta h_R=T_R+Vsel_R-B_R,\qquad
T_R=\delta h_R-Vsel_R+B_R,\qquad\delta=\alpha/8.\tag{HNM-AO1.2}
\]

The constant Haar trial on each strip has zero electric and selected-Wilson mean, so Estrip_b<=0. Each strip has selected absolute budget at most `alpha/2+alpha/8+alpha/2=9alpha/8`. Thus

\[
\omega_\Lambda(T_R)\le{\alpha\over8}28|\tau|+{9\alpha\over4}
=\alpha(9/4+(7/2)|\tau|).\tag{HNM-AO1.3}
\]

Both coupling signs and every allowed signed selected coefficient are covered. Omitting B_R from the exact identity is wrong; discarding its nonpositive contribution after writing an upper inequality is legitimate. Omitting Vsel_R from the reconstruction is also wrong. At tau=0 a nontrivial selected ground has zero reference energy while its electric expectation need not vanish.

## Domains and four original links

At finite volume the Casimir sum is elliptic on compact SU(2)^L, and the full magnetic potential is a bounded smooth real multiplier. Its operator domain is the product H² domain. The ground is smooth. W has bounded derivatives through order two, so multiplication preserves this domain. Hence chi_Lambda lies in D(K_Lambda), and its second spectral moment equals the squared generator norm. No infinite-volume domain is assumed.

All selected and omitted magnetic multipliers commute with W. For `C_e=-sum_a X_ea²`,

`[C_e,W]u=(C_eW)u-2 sum_a(X_eaW)X_ea u`.

The original four stored links are distinct. Each contributes C_eW=3W/4, with inverse occurrences retaining their derivative side and sign. Consequently

\[
K_\Lambda\chi_\Lambda=3\alpha W\Omega_\Lambda-2\alpha Z_\Lambda,
\quad Z_\Lambda=\sum_{e\in p,a}(X_{ea}W)X_{ea}\Omega_\Lambda.\tag{HNM-AO1.4}
\]

AK2's half-Pauli identity gives `sum_(e in p,a)(X_eaW)²=1-W²<=1`. Pointwise Cauchy–Schwarz followed by integration yields

\[
\|Z_\Lambda\|^2\le\int(1-W^2)\sum_{e\in p,a}|X_{ea}\Omega_\Lambda|^2
\le\omega_\Lambda(T_R)/\alpha.\tag{HNM-AO1.5}
\]

The derivative cross term is retained: the actual selected reference is generally not constant. Using `||W Omega||<=1` and `||u+v||²<=2||u||²+2||v||²`,

\[
\|K_\Lambda\chi_\Lambda\|^2\le18\alpha^2+8\alpha\omega_\Lambda(T_R)
\le\alpha^2(36+28|\tau|).\tag{HNM-AO1.6}
\]

This proves the claimed bound in physical energy-squared units. A frequency second moment would divide by hbar². The fixed energy reference and clock are unchanged.

## Controls and finite scope

At the fully free corner, where all selected coefficients and tau vanish, the Haar ground is constant, variance is 1/4, and the Wilson energy is 3alpha. Its exact second moment is 9alpha²/4 despite zero reference-ground energy. This rejects equating those two energies.

The checker reconstructs origin versus interior incidence (two versus seven stars), the complete link cover, and exact coefficients. A smooth one-rotor diagnostic Omega(q)=1+q_0/3, W=q_0 at q_0=3/5 has a nonzero gradient cross term; dropping it changes the commutator. It is an algebra control, not an I1 ground. A finite matrix expectation fixture tests the negative ground scalar in the exact reconstruction and its safe removal only for an upper inequality. Doubling Lie generators quadruples squared gradients and is rejected. Measures with bounded first moments but escaping high-energy tails have growing second moments, so first-moment boundedness cannot replace this proof.

The regional constant is specific to the original orthant cover; interior or summable-model substitution needs a new dictionary. No limit is taken. Uniform integrability, limiting moment equality and the actual infinite-volume operator domain remain for adaptive AO2.

Reproduce: `python -B research/round29/forward/ao1/check.py --output /absolute/new/output`.
