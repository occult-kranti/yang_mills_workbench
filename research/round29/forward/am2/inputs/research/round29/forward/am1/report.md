# AM1 forward: HNM complete-model numerical-certificate transfer audit

Human project author: **Hruday N M (BUNZEEY)**. Independent forward report under the frozen AM1 contract. Current reverse and skeptic work were not read. **Verdict: the inspected explicit SU(3) proof template cannot be copied into I1 with its constants; the numerical I1 radius remains insufficient in this loop.** The new result is the exact failed dictionary, not another claim that unspecified constants were just discovered.

## What the older source still leaves unevaluated

I1 uses `h_b>=I-P_b`, a complete 24-link factor, `S={0,e_x,e_y,e_z}`, and `||phi_b||=7|tau|`. Theorem1 of Yarotsky math-ph/0411042v1 introduces range-dependent `c1,c2`. Section2 uses variable constants; its Lemma1 requires a sufficiently small interaction to obtain weighted ground-expansion coefficients. The required fixed-point radius/contraction constant is not evaluated. Equation14 then bounds a dressed commutator with a further unspecified factor; the resolvent argument of Eq15 needs that factor times the interaction norm below one. The I2 report already isolated these stops. This fresh source read does not convert them into numbers or a new obstruction.

## A precise template comparison

Fresh reading of Gauvin arXiv:2503.15539v3, companion supplement A.6–A.11, identifies a different reference: three outgoing **fine links** at each fine vertex, constant Haar vacuum and pure-electric onsite operator. Lemma2.14 separately counts at least four nontrivially labelled fine links from graph girth and at least one active link for each excited outgoing block. It does **not** say every physical excitation occupies four blocks. Lemma2.15 uses an interaction support of at most three fine blocks, a per-site interaction sum, and physical-sector electric inverse estimates. The numerical SU(3) result follows only with that dictionary and its complete fixed-point, spectral-exclusion and cutoff-removal argument.

I1 instead uses the selected-strip ground within each 24-link coarse factor, and its omitted interactions are grouped into four-site stars. Its onsite theorem provides normalized gap at least one; it does not provide the template's stronger inverse bound with a four-link electric floor. Its vacuum is generally not the constant Haar vector on selected links. Replacing source fine sites with coarse labels therefore changes the hypotheses. Individual omitted faces have at most three coarse owners, but this is not the contracted complete four-site grouping; changing the decomposition would require a new norm and source dictionary.

The source's dimensionless SU(3) constants also depend on its Casimir, trace range and support count. In the present normalization the SU(2) fundamental Casimir is `3/4`, while the corresponding SU(3) value is `4/3`; SU(2)'s normalized real trace has range `[-1,1]`, not the SU(3) fundamental real-trace range. Copying `1/648` into I1 is unsupported. The source is treated as a proposed proof template, not a verified continuum solution.

## An actual one-coarse-factor physical excitation

Fix a selected xy plaquette p entirely inside the strip of factor b. Let `Omega_b` be the actual normalized onsite reference ground, and set

\[
m_p=\langle\Omega_b,W_p\Omega_b\rangle,\quad
v_b=(W_p-m_p)\Omega_b,\quad
v=v_b\mathbin\otimes\!\bigotimes_{c\ne b}\Omega_c .
\tag{HNM-AM1.1}
\]

The finite compact rotor ground is smooth and strictly positive: the positive heat kernel of the connected compact product together with bounded real potential gives a positivity-improving semigroup and its unique positive ground. The selected strip ground times the free Haar factors has this property. Since `W_p` is continuous and nonconstant, its variance in the full-support measure `|Omega_b|²dm` is strictly positive. Thus `v_b!=0` and `v_b` is perpendicular to `Omega_b`. Gauge transformations at all original endpoints fix the ground and the closed Wilson multiplication, so v is physical. Its smoothness also gives the onsite operator domain.

With actual coarse reference projectors `P_c=|Omega_c><Omega_c|`, the vector satisfies `Q_b v=v` and `Q_c v=0` for every `c!=b`. Exactly **one coarse factor** is excited. The selected square still has four distinct fine vertices and four links; there is no contradiction. This rejects an imported assertion that physicality forces four excited coarse factors. It does not prove the falsity of any proposed numerical lower energy bound: the energy of this vector has not been bounded above by that number.

At zero selected coefficients, a useful exact subcase is `Omega_b=1`, `m_p=0`, `||v_b||²=1/4`: condition on three plaquette links and the remaining holonomy is Haar SU(2), whose scalar coordinate has second moment one quarter. This subcase audits the variance mechanism. The positivity argument, rather than substituting Haar moments for the dressed state, proves the nonzero-coefficient statement.

## Complete incidence and norm conversion

There are three selected and 21 omitted anchored face classes. Each omitted group has norm `M=7|tau|`. A bulk coarse site x belongs to exactly the anchors `x,x-e_x,x-e_y,x-e_z`. Thus the source-style indexed site sum for this actual grouping is

\[
J_{\rm HNM}=\sup_x\sum_{b:x\in b+S}\|\phi_b\|=4M=28|\tau|.
\tag{HNM-AM1.2}
\]

Boundary clipping can only decrease it. The 84 face occurrences in these four grouped stars are retained in the indexed budget even though only 49 individual faces actually touch an interior factor. Contracting supports after grouping would change the declared norm. Counting only the outgoing anchor incorrectly divides J by four.

Scalar and retained diagonal terms are independent obstacles to a shortcut: an interaction splitting must retain `cI`, the centered complement term and the mixing term. Removing a scalar changes raw ground energy while leaving centered gaps; removing the complement diagonal generally changes gaps. The exact diagnostic matrix in the checker separates these effects. It is not an SU(2) truncation.

## Outcome and next missing premise

The executable reconstructs the one-factor square and complete star incidence, checks the exact Haar subcase and unit conventions, and runs the wrong-transfer controls. No unknown source constant is replaced by a convenient rational. The template's mathematical proof is not disproved; its direct **transfer** has missing premises. A later loop could prospectively rederive the creation estimates for I1's actual four-site support and available onsite inverse, including every stage of its fixed-point and spectral argument. That work has not been executed here.

Source reading: Yarotsky Theorem1 and Section2 Lemma1/Eqs14–15; Gauvin supplementary A.6–A.11, downloaded from `https://arxiv.org/src/2503.15539v3/anc/PinchedMultiAffineGeometry_Supplement.pdf`. Historical methods enter through complete mechanism and inverse-dictionary checks, not as mathematical authority.

Reproduce: `python -B research/round29/forward/am1/check.py --output /absolute/new/output`.
