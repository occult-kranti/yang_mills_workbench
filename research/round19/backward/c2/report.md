# Round19 backward C2 reconstruction

This is the independent backward C2 reconstruction from the frozen C2 contract and accepted C1 gate.  It proves a continuous statement for the accepted static C1 integral

\[
F(\kappa)=\frac{N(\kappa)}{Z(\kappa)},
\qquad S=3x+y+z+w+t,
\qquad O=\frac{(4x^2-1)^3(4w^2-1)}{81}.
\]

The parameter \(\kappa\) remains a static integral coupling only.  It is not `E_star`, not a physical energy/time scale, and does not imply dense convergence, continuum Yang-Mills, or a Clay mass gap.

The checker reconstructs the accepted C1 coefficients through degree 8 from the backward C1 graph/moment machinery and binds both backward and forward accepted C1 result hashes.  The low coefficients are

\[
N_0=N_1=0,
\quad N_2=1/324,
\quad N_3=13/1296,
\quad Z_0=1,
\quad Z_1=0,
\quad Z_2=13/8,
\quad Z_3=1/4.
\]

For \(|\kappa|\le K\), the numerator proof uses

\[
N(\kappa)\ge \kappa^2\left(N_2-\sum_{n=3}^8 |N_n|K^{n-2}-E\frac{7^9K^7}{9!}\right)=C_N(K)\kappa^2,
\]

where \(E\) is an exact rational upper bound for \(\exp(7K)\).  Since \(Z(\kappa)\le E\) and \(Z(\kappa)>0\), the lower-bound direction is

\[
F(\kappa)\ge \frac{C_N(K)}{E}\kappa^2.
\]

At \(K=1/8\), exact arithmetic gives \(C_N/E>1/2048\), so the checker proves

\[
F(0)=0,
\qquad F(\kappa)\ge \kappa^2/2048
\quad\text{for all } |\kappa|\le 1/8.
\]

The endpoint \(\kappa=0\) is handled by the exact zeros \(N_0=N_1=0\) and \(Z_0=1\), before any division by \(\kappa^2\).

For sign asymmetry, the checker forms

\[
D(\kappa)=N(\kappa)Z(-\kappa)-N(-\kappa)Z(\kappa).
\]

The leading coefficient is exactly \(2N_3=13/648\).  Bounding every higher truncated term and both product tails over \(0<\kappa\le1/64\) leaves a positive exact lower bound for \(D(\kappa)/\kappa^3\), hence

\[
F(\kappa)>F(-\kappa)
\quad\text{for }0<\kappa\le1/64.
\]

Boundary diagnostics are explicit.  With the same degree-8 absolute-tail certificate, \(K=1/7\) still has a positive numerator margin but does not reach the coefficient \(1/2048\).  At \(K=1/6\), the numerator margin is negative, so this proof method is insufficient.  Neither diagnostic is reported as a theorem that positivity is false.


## Forward comparison

The current manifest-bound forward C2 bytes compared are:

- `research/round19/forward/c2/check.py`: `cdc0c61881a0fb185f9f8defa7fb7b04ac2a08c57cda037701d5b58ab5700e82`
- `research/round19/forward/c2/report.md`: `b304e3d40e7737656b0288beebc191eaaebd1a94b806798091103ec1f79d79e9`
- `research/round19/forward/c2/output/results.json`: `2cb833b225b1d93c704faca00eee86f35c0654a922ea0c3652ec7dbb08e8c437`
- `research/round19/forward/c2/output/source-manifest.json`: `e5066450985c20769501097171d79e3bf29264b5f66667eb5c185865436cb4d6`
- `research/round19/forward/c2/output/primary-certificate.json`: `2b621dbb298ae63ac29e1fc356f5c197dad7526fe28d09d8d4a36c3124b5c4b8`
- `research/round19/forward/c2/output/sign-asymmetry.json`: `f5e8aa85fe76934962e9054bf37b5ff88d1790bfcb4dfe2c176ba82da6908340`

The canonical comparison commands are:

```bash
python3 research/round19/backward/c2/compare.py --producer research/round19/forward/c2 --evidence research/round19/forward/c2/output --output research/round19/backward/c2/comparison
python3 -O research/round19/backward/c2/compare.py --producer research/round19/forward/c2 --evidence research/round19/forward/c2/output-optimized --output research/round19/backward/c2/comparison-optimized
```

Both accept.  The comparison requires exact C1 coefficient rows through degree 8, validates the primary certificate internally from exact rational `C_N`, `E`, and margin fields, checks the denominator direction `Z(kappa)<=E`, and accepts producer-specific rational exponential upper bounds only when the theorem constant remains certified.  It compares the retained cross-difference coefficients and accepts the producer's stronger sign-asymmetry interval because its declared tail-subtracted margin is positive and the retained coefficients match the independent reconstruction.

The boundary diagnostics agree in content: at `K=1/7`, the degree-8 absolute-tail method proves only a weaker positive coefficient and does not reach `1/2048`; at `K=1/6`, the degree-8 numerator margin is insufficient, so no wider theorem is claimed from that crude certificate.

Mutation controls reject altered `N2`, altered `N3`, nonzero `N0`/`N1`, using the point interval as a continuous theorem, wrong denominator direction, underestimated tail, flipped primary margin, independent-V substitution, removed or sign-flipped odd cross-difference, overclaimed `K=1/7`/`K=1/6` diagnostics, static κ as `E_star`, Fibonacci physical-scale wording, and missing manifest source/output entries.


## Round20 admission repair

A later independent audit reproduced two invalid certificates accepted by the
old comparison: an exponential envelope `E=1` at `K=1/8`, and a sign-asymmetry
endpoint `H=1000` with unchanged losses. These were validation defects; neither
mutation was used by the actual forward or backward computation. The old source
and comparison are retained in `history/pre-round20-validator-audit/`.

The repaired comparator independently constructs a degree-80 rational upper
bound for `exp(7K)`, reconstructs every finite loss from the exact coefficients,
requires the full tail and margin identities, and validates both boundary
certificates. The asymmetry check reconstructs every cross-difference coefficient
and all losses at its declared positive endpoint. Missing denominator or zero
endpoint premises now fail closed. Both signed helpers reject nonpositive range
endpoints. New controls explicitly execute each formerly accepted mutation.

For the product tail, coefficient majorization gives `|N_8(k)|,|Z_8(k)|<=E`
and `|N(k)|,|Z(k)|<=E` on the declared interval. Two products therefore cost
at most `4ER(k)`. Since `R(k)/k^3 <= E*7^9*H^6/9!` for `0<k<=H`, the
reported asymmetry tail is uniform down to zero; it does not divide a fixed
endpoint remainder by an arbitrarily smaller coupling. The accepted physical
claims and interval constants are unchanged.
