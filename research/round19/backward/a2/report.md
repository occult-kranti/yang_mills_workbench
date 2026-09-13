# Round19 backward A2: product-representation summable exception

## Preliminary verdict before forward comparison

The independent reconstruction accepts the narrow A2 theorem route as mathematically sufficient under the frozen `ym19-a2-contract-v1` premises. The result is an incomplete tensor-product representation theorem for a summable perturbation of the A1 complete-strip/free reference. It is not a proof that finite clipped restrictions converge to this representation, not a dense homogeneous nondecaying stability theorem, and not a continuum Yang-Mills mass-gap result.

No forward A2 source/evidence was inspected before this derivation and checker were written. The comparison helper is present but awaits canonical forward A2 artifacts.

## Reconstruction

The reference representation is the incomplete infinite tensor product stabilized by `Omega_ref`: complete LMR strip ground states on selected complete strip blocks and normalized Haar vectors on all free link factors. The local algebra is used with a domain qualification: finite-support bounded operators are admissible only after applying them to vectors in the local form domains. The finite-excitation form core consists of algebraic finite tensors whose non-reference entries lie in the corresponding local closed form domains, with an operator-domain subcore reserved for graph-norm statements. Arbitrary `B(H)` local vectors are not assumed to be in the form domain.

For every complete strip block, A1 supplies a unique full-link ground and a local gap at least

```text
delta = alpha/8.
```

Free link factors have the larger gap `3alpha/4`. After subtracting each local ground energy, define

```text
H_ref = sum_C (H_C - E_C) + sum_free alpha C_e
```

as the closed monotone sum of nonnegative local forms. The finite-excitation core satisfies

```text
q_ref[psi] >= delta ||(1 - |Omega_ref><Omega_ref|) psi||^2.
```

This supplies the product-sector isolation and essential-spectrum boundary: the vacuum is isolated by at least `delta` for `H_ref`, with the excitation threshold at or above `delta` in the closed form domain.

The perturbation is

```text
V = - sum_f nu_f x_f,
nu_f = alpha * tau * 2^(-x-y-z) / 24
```

on every positive-orientation face outside the complete LMR selected strips. The absolute coefficient ledger is summable before removing selected faces: for each orientation,

```text
sum_{x,y,z>=0} 2^(-x-y-z)/24 = (2*2*2)/24 = 1/3,
```

so the total positive-orientation face sum is `1`, and the remainder subset has total weight at most `1`. Since `||x_f|| <= 1`, no signed cancellation is used:

```text
||V|| <= beta <= alpha |tau|.
```

For the canonical `tau=1/64`, `beta=alpha/64`. With the frozen scale example `alpha/E_star=2`, the exact fields are

```text
alpha/E_star = 2
delta/E_star = 1/4
beta/E_star = 1/32
gap/E_star >= 7/32
```

The zero trial mean is termwise. The exhaustive witness classes are: xz/yz remainder faces contain a z-directed link, while selected strip blocks use only xy links; odd-y xy faces contain an odd-y y-link, while selected rows use even-y intervals; even-row x-separator xy faces have x residue `3 mod 4`, with an x-link outside every complete LMR support. In all cases the witness is a free Haar factor in `Omega_ref`, so `<Omega_ref, x_f Omega_ref>=0`. Therefore `<Omega_ref,V Omega_ref>=0` and the ground energy obeys `lambda0 <= 0`.

For vectors orthogonal to `Omega_ref`, the codimension-one compression bound gives

```text
Q(H_ref+V)Q >= (delta - beta) Q,  Q = 1 - |Omega_ref><Omega_ref|.
```

If the spectral projection `E_H((−∞, delta-beta))` had rank at least two, its range would contain a nonzero vector orthogonal to `Omega_ref`, contradicting the compression bound. Hence that projection has rank at most one. The zero trial mean gives a vector with Rayleigh quotient `0 < delta-beta`, so the projection is nonzero. It is therefore rank one and yields a genuine isolated ground eigenvector below the rest of the spectrum, even without compact resolvent. The gap lower estimate is `delta-beta`. If the zero-mean premise is withdrawn, the comparison falls back to the generic `delta-2beta` route; that is weaker and is not the same theorem.

## Objections and blockers retained

The checker rejects zero or nonphysical energy normalization, static `kappa`, homogeneous nondecaying remainders, `beta>=delta`, missing zero-mean premises for the sharp theorem, finite-only eigenvalue reruns, missing closed form/domain construction, missing essential-spectrum isolation, finite clipped-restriction convergence claims, dense/continuum promotion, Boolean `tau`, and negative `alpha/E_star`.

The product representation can be useful as a summable exception, but it does not prove that the literal finite boxes from A1 converge in state, form, resolvent, or spectrum. That would require a separate A2-sized theorem and is deliberately left open. The local gauge-invariant operator reduces the Gauss sector; the isolated one-dimensional ground carries a continuous one-dimensional representation of the local gauge group, hence is invariant. A physical-sector gap claim is non-vacuous only with at least one finite-energy non-ground Gauss-sector vector; local Wilson-loop/character excitations in complete strip blocks provide such vectors when selected blocks are present, and closed gauge-loop excitations supply the free/no-block case.

## Executed artifacts

`check.py --output ABS_NEW_DIR` writes `results.json`. Ordinary and optimized outputs are byte-identical. `compare.py --producer SOURCE --evidence OUTPUT --output NEW_DIR` is ready for canonical forward A2 artifacts and separates provenance from mathematics without importing producer code.

## Final producer comparison

The final canonical forward A2 comparison is accepted. The compared producer source was `research/round19/forward/a2/check.py` with SHA-256 `e6d8617a0593d13a711cb63447e1d2d3e32a3c9337efdbc95fe1a2ffac22323e`. The compared producer evidence was `research/round19/forward/a2/output/results.json`, whose source manifest binds the current source, report and output files.

The independent comparison recomputed, rather than trusted status strings:

- the scale/gap fields: `alpha/E_star=2`, `delta/E_star=1/4`, `tau=1/64`, crude `beta/E_star=1/32`, exact `beta/E_star=107/4320`, crude gap `7/32`, exact gap `973/4320`, and common crude physical floor `7/64`;
- the full dyadic ledger: selected weight `28/135`, omitted weight `107/135`, total weight `1`;
- all nine tail fixture rows and `tail-fixtures.csv` from the exact finite cutoff formulas;
- representative selected and omitted coefficients, including the actual zero-mean witness links for xy separator, odd-y xy, xz and yz cases;
- structured domain, finite tensor core, reference and perturbed ground gauge invariance, non-vacuous Gauss excitation, and open-claim boundaries;
- mutation controls for `beta>=delta`, altered exact gap, missing tail fixture and missing zero-mean witness.

Comparison status is `accepted` with 14 checks, 0 provenance failures and 0 mathematics failures. Its SHA-256 is `a71ee7600c0843d23a6938e240976286820125baf4aade55a9316076fbdc73eb`.

## Corrected-source domain review

A later forward revision temporarily stated that the operator domain of `H=H_ref+V` need not equal `D(H_ref)`. I rejected that formulation: because `V` is bounded self-adjoint and `H_ref` is self-adjoint, the bounded perturbation theorem gives `D(H_ref+V)=D(H_ref)`. The closed quadratic-form domain is also unchanged. The proof itself uses the form inequality and spectral projection argument, but the source record must not misstate the operator-domain fact.

The final compared forward source corrects this point. Its operator-theorem record states that `H=H_ref+V` is self-adjoint on exactly `D(H_ref)` and that the closed quadratic-form domain is the same as the form domain of `H_ref`. The final comparison accepts this corrected wording.

Final compared forward hashes:

- `research/round19/forward/a2/check.py`: `e6d8617a0593d13a711cb63447e1d2d3e32a3c9337efdbc95fe1a2ffac22323e`
- `research/round19/forward/a2/report.md`: `6fc6b0c4ee95d11e5e1ab8f9b6249ace7b9792728ee93bd919510ce440bc51fb`
- `research/round19/forward/a2/output/results.json`: `43f45abfdc365e1c1f423bfa64b93a4ff3f8386acaed49c139a05521a2e269b9`
- `research/round19/forward/a2/output/source-manifest.json`: `a51d5f4a1e980f4f3a02772cdbf3c1879b1fbcb460cdec87412e5e6fbf9bd38f`

Final comparison status is `accepted` with SHA-256 `f657d610651118b23ef3ed2ea0ad387b936f7979ba77e0950d1779d3c1fe9f71`.
