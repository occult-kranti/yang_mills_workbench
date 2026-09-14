# Round19 backward B2 reconstruction

This is the independent reverse/skeptic B2 reconstruction from the accepted B1 gate and backward B1 exact data.  It was written before inspecting any Round19 forward B2 implementation.

The proof works on the finite two-cube physical Hilbert space only.  It does not prove homogeneous dense stability, limiting spectral passage, continuum Yang-Mills, or a Clay mass gap.

## Block setup on \(\Omega^\perp\)

Use the accepted B1 projector

\[
P=\mathbb C\Omega\oplus R,
\]

where `dim P=48` and `dim R=47`.  The 47 channels in `R` split into 11 face cycles with electric level `3 alpha` and 36 six-edge cycles with electric level `9 alpha/2`.  The complement `Q=1-P` has electric threshold `6 alpha`.  This explicitly rejects the old Round18 constant `3 alpha` block shortcut for all of `P-Omega`.

For `|lambda_f| <= r alpha`, the checker reconstructs the exact `R V R` linear coefficient matrix using B1's signed Wilson words and exact SU(2) Haar contractions.  It also uses the exact B1 `W^*W=P V^2P-(PVP)^2` Gram restricted to `R`.  Row-sum interval bounds give

\[
A:=R(H_0+V)R\ge a\alpha,
\qquad Q(H_0+V)Q\ge d\alpha,
\qquad W^*W\le w\alpha^2.
\]

For \(\mu<d\alpha\), the Schur-complement/min-max condition

\[
A-\mu - \frac{W^*W}{d\alpha-\mu}\ge0
\]

is certified by

\[
(a-\mu/\alpha)(d-\mu/\alpha)-w\ge0.
\]

The lower root is reported as the certified `E1` lower bound on \(\Omega^\perp\).  Separately, the vacuum Rayleigh quotient is `0`, so `E0 <= 0`.  The finite-graph gap statement is therefore `lambda_1 - lambda_0 >= E1_lower - E0_upper`, and with `E0_upper=0` this is the reported positive lower bound.

## Primary box \(r=1/8\)

For the required continuous box `|lambda_f| <= alpha/8`, the exact interval data is

- `a = 11/4`, from `3 - 1/4` on the 47-dimensional block,
- `d = 37/8`, from `6 - 11/8` on `Q`,
- `w = 19/256`, from the accepted B1 exact `W^*W` row sums.

Thus

\[
E_1/\alpha\ge \frac{11/4+37/8-\sqrt{61/16}}2.
\]

The outward decimal interval recorded by integer arithmetic is `[2.711218790511668, 2.711218790511669]`.

Since `E0 <= 0`, this gives the same certified finite two-cube gap lower bound over the full signed continuous box.

## Round18 \(r=3/8\) benchmark

The Round18 benchmark is rederived under the enlarged 48-channel projector rather than assumed.  The checker obtains

- `a = 9/4`,
- `d = 15/8`,
- `w = 171/256`,

and therefore

\[
E_1/\alpha\ge \frac{9/4+15/8-\sqrt{45/16}}2.
\]

The outward decimal interval is `[1.223974508437578, 1.223974508437579]`; the lower endpoint is rounded outward, not to nearest.

This is a Round19 finite-graph row-sum certificate using the enlarged projector and exact B1 Gram.  The historical Round18 value `R*(3/8)=0.11876245` is retained only as history, not as the proof used here.

## Controls

The checker rejects stale 12-channel `P`, the constant `3 alpha` block shortcut, omission of nonzero face-six or six-six `PVP` terms, `PV2P` or a norm bound labeled as exact `W^*W`, an unrederived Round18 `3/8` claim, finite Ritz/sample promotion, bad physical scale, sign/direction mixing between `E1` and `E0`, and deletion of a coefficient-box interval cell.

## Natural parameter envelope

The same row-bound proof gives a continuous parameter envelope.  Exact rows verify

\[
a(r)=3-2r,\qquad d(r)=6-11r,\qquad w(r)=\frac{19}{4}r^2.
\]

The resulting Schur lower root is

\[
R(r)=\frac{9-13r-\sqrt{100r^2-54r+9}}{2}.
\]

The determinant condition is

\[
18-45r+\frac{69}{4}r^2>0,
\]

so this certificate proves positivity for

\[
0\le r<\frac{30-2\sqrt{87}}{23},
\]

with outward decimal upper-end interval `[0.493271386687929, 0.493271386687930]`.  As controls, `r=7/16` is positive with exact lower bound `19/32`, while `r=1/2` is insufficient for this certificate because the determinant is `-3/16`.


## Final forward comparison

The final comparison was run with the standard source-bound API:

```bash
python3 research/round19/backward/b2/compare.py --producer research/round19/forward/b2 --evidence research/round19/forward/b2/output --output research/round19/backward/b2/comparison
python3 -O research/round19/backward/b2/compare.py --producer research/round19/forward/b2 --evidence research/round19/forward/b2/output-optimized --output research/round19/backward/b2/comparison-optimized
```

Both runs accepted.  The canonical ordinary comparison is `comparison/comparison.json`; the optimized replay is `comparison-optimized/comparison.json`.  The comparison maps B1 channels and faces by coordinate-normalized masks, compares the full 47-row envelope table, compares all 208 compressed `P V P` entries by canonical `(row, column, face)` masks, and verifies the exact certificate formulas for `r=1/8`, `r=3/8`, `r=7/16`, and the insufficient `r=1/2` control.

The final forward lock bytes checked by the comparison are:

- `research/round19/forward/b2/check.py`: `772e4e9f30c5bf759551159c916f652e6b51d7a856abf99c861de5d10056ce3f`
- `research/round19/forward/b2/output/results.json`: `0e13e1ffb50c05b47260d3a6c830a6126b0286ff5771b98872f1cb47f888f0a5`
- `research/round19/forward/b2/output/source-manifest.json`: `6fdfb55a60ac3520e2aeb885c33bdcb44cee14749da6aff4ae3c02275e55ebc1`
- `research/round19/forward/b2/output/certificates.json`: `4400f28fa848fe4f1b39f9d69149fa88ebe66aa4e74aefbefd9e5656d902835e`
- `research/round19/forward/b2/output/block-envelopes.json`: `c2210dc4b1772954e1bdf39f92f8374c7ffa238ef5ed210a06ded174a263fb80`
- `research/round19/forward/b2/output/compressed-pvp-RR.json`: `f79ab1f147975e331be21dbef38f3bb39462d67580358e3506edf5088a46827c`

The source-manifest check requires the declared source files and all required output fixtures, including `block-certificate.json`, `certificates.json`, `block-envelopes.json`, `compressed-pvp-RR.json`, `controls.json`, `pvp-linear.json`, `results.json`, and `row-envelopes.csv`.  It validates the accepted forward B1 source bindings rather than requiring the producer to reuse the backward implementation hashes.

The mutation controls reject stale projector dimension, constant-block shortcuts, omitted or altered `P V P` entries, wrong cross-Gram factors, unrederived `3/8` claims, sample Ritz promotion, zero/kappa/Fibonacci `E_star`, `E1/E0` sign mixing, row envelope deletion, misstated `7/16` and `1/2` controls, missing parameter range, and missing manifest source/output entries.
