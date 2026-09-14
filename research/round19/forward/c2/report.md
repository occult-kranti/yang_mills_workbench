# Forward C2: continuous static-kappa certificate

This executes the frozen `ym19-c2-contract-v1` forward loop. It uses the accepted C1 coefficient table for the actual U-V-W chain and proves a continuous static-kappa theorem. This remains a static mathematical checkpoint only: it does not match `kappa` to a physical energy or time scale and makes no dense-limit, continuum, spectral-gap, or Clay mass-gap claim.

Let

\[
F(\kappa)={N(\kappa)\over Z(\kappa)},\qquad
N=E[Oe^{\kappa S}],\quad Z=E[e^{\kappa S}],
\]

with the accepted C1 action `S=3x+y+z+w+t` and observable `O=(4x^2-1)^3(4w^2-1)/81` under the common-V Haar measure.

## Positivity on `|kappa| <= 1/8`

The checker recovers

\[
N_0=N_1=0,\quad N_2={1\over324},\quad N_3={13\over1296},
\]

and

\[
Z_0=1,\quad Z_1=0,\quad Z_2={13\over8},\quad Z_3={1\over4}.
\]

For `|kappa|<=K`, `|S|<=7` and `|O|<=1`. With rational `E_K >= exp(7K)`, the degree-8 numerator tail gives

\[
{N(\kappa)\over \kappa^2}\ge
C_N(K)=N_2-\sum_{n=3}^8 |N_n|K^{n-2}-E_K{7^9K^7\over 9!}
\]

for nonzero `kappa`. The endpoint `kappa=0` is handled separately by `N0=N1=0`. Since `Z(kappa)>0` pointwise and `Z(kappa)<=E_K`, the denominator direction is

\[
F(\kappa)\ge {C_N(K)\over E_K}\kappa^2.
\]

At `K=1/8`, exact arithmetic gives `C_N(K)/E_K > 1/2048`, hence

\[
|\kappa|\le {1\over8}\quad\Longrightarrow\quad F(\kappa)\ge {\kappa^2\over2048},
\]

with `F(0)=0` established before division.

## Sign asymmetry

The sign comparison is separate. The checker forms

\[
D(\kappa)=N(\kappa)Z(-\kappa)-N(-\kappa)Z(\kappa).
\]

The retained leading term is

\[
2N_3\kappa^3={13\over648}\kappa^3.
\]

The exact degree-8 product contributes retained odd powers through degree 15. The common certificate subtracts the finite retained loss and a rational product-tail envelope. For `0<kappa<=1/64`, the resulting lower bound for `D(kappa)/kappa^3` is positive. Because both denominators are positive, this proves

\[
0<\kappa\le {1\over64}\quad\Longrightarrow\quad F(\kappa)>F(-\kappa).
\]

## Boundary diagnostics

The same degree-8 absolute-tail certificate is tested at `K=1/7` and `K=1/6`.

At `K=1/7`, the certificate still proves a positive numerator coefficient but does not reach the stronger `1/2048` quotient coefficient. At `K=1/6`, the degree-8 numerator margin is negative. A bounded higher-degree probe through degree 20 is recorded in `boundary-probe.csv`; it is a proof-method diagnostic, not a theorem that positivity is false.

## Evidence

Run from this directory:

```bash
python -B check.py --output /absolute/new/output_dir
```

Generated files:

- `results.json`: theorem statement, static scope, source-bound inputs, checks, and controls;
- `coefficients.json`: accepted C1 Taylor coefficients used by C2;
- `primary-certificate.json`: exact `K=1/8` range proof and denominator direction;
- `sign-asymmetry.json`: exact cross-difference proof on `(0,1/64]`;
- `boundary-diagnostics.json` and `boundary-probe.csv`: `K=1/7` and `K=1/6` diagnostics;
- `controls.json`: mutation and public-domain controls;
- `source-manifest.json` and `manifest.json`: source, report, C2 contract, C1 gate, accepted C1 input hashes, and output hashes.
