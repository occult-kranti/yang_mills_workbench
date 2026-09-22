# HNM numerical-certificate transfer audit — independent reverse AM1

Project author: Hruday N M (BUNZEEY). HNM identifies this model-comparison audit, not an externally established theorem. Scientific priority is unverified. Current forward/skeptic AM1 outputs were not read.

## Target and inherited numerical gap

A usable numerical I1 radius requires a complete inequality with evaluated constants for the actual untruncated selected-strip reference and its homogeneous four-site-star omitted interaction. I1 supplies epsilon=7|tau| and tau_*=(1/7)min(c1(S),1/(2c2(S))). Neither c1 nor c2 is evaluated. The inherited I2 source audit locates the other missing pieces: Yarotsky math-ph/0411042v1 Section 2 changes the meanings of c and epsilon between formulas; Lemma 1/equation (8) has no evaluated contraction radius; equation (14) retains a commutator constant; equation (15) needs that constant times the perturbation norm below one for resolvent convergence. Reference [23] contains further detailed proof. Repeating this ledger does not constitute a new quantitative result. I2's explicit one-star rotation and AG3's single weight-changing correction do not evaluate the entire iteration.

## What the proposed source actually says

Gauvin arXiv:2503.15539v3 supplement A.6–A.8 uses SU(3), three outgoing fine links per site, a constant Haar reference, and interactions on at most three sites. Its physical-sector bound counts at least four **active links** from cycle girth and at least |M| links from excited outgoing blocks. It does **not** assert at least four excited blocks. Its creation and shifted-resolvent estimates depend on this energy counting. The source's displayed radius therefore has no automatic transfer to I1's selected-strip, 24-link, four-site assignment. Reading depth: these sections inspected directly; the proposed transfer is tested here, not the entire external paper's proof.

## A genuine one-factor physical excitation

Choose a selected endpoint plaquette inside one complete coarse factor b. Its normalized real Wilson trace W is a bounded smooth nonconstant gauge-invariant function of four links, all assigned to b. Let Omega_b be that factor's actual unique selected-strip ground vector including its free links, and m=<Omega_b,W Omega_b>. The finite compact connected rotor operator is elliptic with a bounded smooth real potential; its unique ground can be chosen strictly positive. Hence

\[
v_b=(W-m)\Omega_b\ne0,\qquad P_bv_b=0.
\]

Indeed zero variance would make W constant almost everywhere in the strictly positive ground density, contradicting its distinct values on open neighborhoods. The smooth multiplier preserves the finite-factor form domain. In any finite complete-factor volume containing b, put psi=v_b tensor Omega_outside. Every endpoint gauge action fixes this vector: W is a closed Wilson loop, each actual factor vacuum is gauge invariant, and the original endpoint actions are retained. Thus psi is a nonzero physical vector with exactly one excited coarse factor:

\[
\Big(\sum_xQ_x\Big)\psi=\psi.
\]

The proposed replacement of “four active fine links” by “four excited coarse factors” is false. The checker enumerates this loop: four links, four fine vertices, three outgoing fine-link blocks, **one** coarse factor. This argument does not show <psi,H0 psi><4||psi||². In fact the pure-electric selected Wilson can have much higher normalized energy. It refutes the counting premise, not a numerical energy bound; the latter would need a new selected-reference proof. I1 directly gives only h_b>=Q_b. Its shifted interacting onsite energy is not the sum of independent active-link Casimir costs used by the source.

## Full support and normalization audit

Every complete I1 cell owns 24 links. It anchors 21 omitted faces grouped in phi_b=-(tau/3)sum W_f, with exact norm 7|tau|. With the specified star support S={0,ex,ey,ez}, a bulk site belongs to four anchor stars: its own and three incoming stars. Therefore the source-style site incidence budget for this declared decomposition is

\[
J_{\rm HNM}=\sup_x\sum_{b:x\in b+S}\|\phi_b\|=28|\tau|.
\]

The value 7|tau| is an anchor supremum, not this site sum. The source's at-most-three support hypothesis also becomes four; any transfer must recompute the creation support count and all majorants. SU(3)'s fundamental Casimir 4/3 differs from SU(2)'s 3/4, and the minimal centered trace norm is 3/4 versus 1. Copying a coefficient or ratio without that dictionary is invalid.

The exact matrix control K=cI+B+Z retains c=<Omega,K Omega>, vacuum mixing B=PKQ+QKP and centered diagonal Z=Q(K-cI)Q. Deleting c or Z changes the operator. An all-stage source transfer must keep both as well as the actual new ground subtraction; none is supplied merely by a local rotation.

## Verdict and executable evidence

**Insufficient numerical I1 interval.** The added result beyond I2 is a source-specific transfer audit, the physical one-coarse-factor excitation, and the exact incidence conversion. No convenient c1/c2 is inserted. This does not show that computable constants do not exist, that the external source is false, or that the actual homogeneous gap fails.

Run `python research/round29/reverse/am1/check.py --output /absolute/new-directory`. Rational geometry, tensor-sector and matrix controls run in normal and optimized modes with identical results. The positivity/nonconstant-W proof is analytic, not simulated. Source metadata, inherited premises, code and output hashes are recorded in the manifest and freeze. A subsequent complete proof must supply the actual-reference creation estimates, all-stage contraction and resolvent constants, domain/cutoff passage, physical restriction and boundary family before publishing a positive numerical radius.
