# Forward B1: strict cutoff projector and exact cross Gram on the actual two-cube graph

This executes the frozen `ym19-b1-contract-v1` forward loop. It uses the actual two-cube graph with 12 vertices, 20 links and 11 faces, including the shared/internal face counted once. It does not start B2 and does not claim homogeneous dense stability, continuum Yang-Mills or a mass gap.

## Graph, scale and cutoff

The Hamiltonian contract is

\[
H=\alpha\sum_e C_e-\sum_f\lambda_f x_f,
\qquad x_f=\chi_f/2=\operatorname{ReTr}(U_f)/2.
\]

A positive `E_star` is recorded separately from `alpha/E_star` and the ratios `lambda_f/alpha`; `kappa`, numerical tolerances, volume and Fibonacci labels are absent from the energy scale. The physical sector is the SU(2) gauge-invariant spin-network sector.

The strict projector is

\[
P=1_{E_{\rm el}<6\alpha}(H_0).
\]

## Strict channel classification

For an edge label \(n=2j\), the electric cost is

\[
\alpha j(j+1)=\alpha\frac{n(n+2)}4.
\]

Below \(6\alpha\), at most seven fundamental edges can be active. The checker enumerates every edge support up to size seven and every label assignment with labels \(n=1,2,3\) whose total electric energy is below the strict cutoff. At each active vertex it computes the exact SU(2) invariant multiplicity by Clebsch-Gordan fusion to spin zero.

The complete result is sharp and positive: the only channels below the strict cutoff are

- the vacuum;
- 11 fundamental four-edge simple cycles, one for each actual face;
- 36 fundamental six-edge simple cycles.

The 36 six-edge cycles include 32 nonplanar cycles. The 28 seven-edge no-leaf supports that survive a graph-only test have no admissible low-energy SU(2) intertwiner assignment, so they are not physical channels below the cutoff.

Each admitted non-vacuum channel below the strict cutoff has all active labels \(n=1\) and all active vertices of degree two, hence intertwiner multiplicity one. The threshold layer at exactly \(E_{\rm el}=6\alpha\) is not included in \(P\). It contains 99 support/label assignments; counting local SU(2) invariant multiplicities gives 107 physical threshold channels, with multiplicity distribution 91 assignments of multiplicity one and 8 assignments of multiplicity two. The checker records the eight multiplicity-two assignments and their degree-four vertices. Thus the complement threshold is

\[
QH_0Q\ge 6\alpha Q.
\]

Since the basis vectors are complete eigenspaces of \(H_0\) below the cutoff, \(P\) reduces \(H_0\).

## Exact cross Gram

Let

\[
V=-\sum_{f=0}^{10}\lambda_f\chi_f/2,
\qquad W=QVP.
\]

The exact object is

\[
W^*W=PV^2P-(PVP)^2.
\]

The B1 checker computes this on the 48-dimensional orthonormal basis consisting of the vacuum plus all strict-cutoff fundamental cycles. The Haar moments are exact tensor contractions of SU(2) fundamental matrix entries on the signed two-cube graph. The contraction first validates basic identities, including single Wilson-loop mean zero, face norm one and the fourth moment \(E\chi_f^4=2\). It then builds the sparse symbolic coefficient tensor for the polynomial entries of \(W^*W\) in the eleven variables \(\lambda_f\lambda_g\).

The output stores the full sparse coefficient tensor rather than only a norm bound. Representative rational fixture matrices are included for zero, equal, alternating and single-face coefficient choices. The coefficient tensor has 867 nonzero ordered quadratic coefficients. The vacuum cross row vanishes only after subtracting \((PVP)^2\); presenting \(PV^2P\) alone as the cross Gram is rejected.

## Evidence and limits

Run from this directory:

```bash
python -B check.py --output /absolute/new/output_dir
```

The generated output is compact but complete for replay:

- `graph.json`: actual signed incidence graph;
- `channels.json`: strict cutoff classification, multiplicities, threshold witness and threshold multiplicity ledger;
- `cross-gram-coefficients.json`: sparse exact symbolic cross-Gram coefficients and PVP linear coefficients;
- `fixture-matrices.json`: exact rational matrix fixtures;
- `basis.csv`: basis inventory;
- `controls.json`: wrong-model controls;
- `source-manifest.json`: source, report, contract and method snapshot hashes.

This is a finite two-cube strict-cutoff and cross-operator result. B2 coefficient boxes, scalar gap estimates, homogeneous dense stability and continuum limits remain separate obligations.
