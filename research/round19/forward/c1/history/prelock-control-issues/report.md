# Forward C1: exact static U-V-W chain integral

This executes the frozen `ym19-c1-contract-v1` forward loop. It reconstructs the actual Round18/Round19 four-cube graph with 18 vertices, 33 links and 20 faces, fixes all but the three vertical links `U,V,W`, and evaluates the normalized static integral at `kappa=1/64`. Static `kappa` remains only a mathematical checkpoint; physical energy/time-scale matching is open and unmatched.

## Graph reduction

The active links are the vertical axis-2 links at `(1,1,0)`, `(1,0,0)` and `(0,0,0)`, named `U,V,W`. The checker reconstructs all signed face words before reduction. Seven faces are affected and thirteen faces are constant. The affected face traces reduce to

\[
S=3x+y+z+w+t,
\]

where

\[
x={\operatorname{Tr}U\over2},\quad y={\operatorname{Tr}V\over2},\quad z={\operatorname{Tr}W\over2},\quad
w={\operatorname{Tr}(UV^\dagger)\over2},\quad t={\operatorname{Tr}(VW^\dagger)\over2}.
\]

The observable is kept unchanged on the `U-V` branch:

\[
O={(4x^2-1)^3(4w^2-1)\over81}.
\]

## Moment routes

The primary route is exact SU(2) character fusion. For monomial exponents `(a,b,c,d,e)` on `(x,y,z,w,t)`, it uses

\[
2^{-(a+b+c+d+e)}\sum_{i,k,m}
{M(a,i)M(d,i)M(c,k)M(e,k)M(b,m)N(i,k,m)\over(i+1)(k+1)}.
\]

Here `M(p,n)` is the multiplicity of character `chi_n` in `chi_1^p`, and `N(i,k,m)` is the parity and triangle fusion indicator. The independent route expands `w=(u\cdot v)` and `t=(v\cdot q)` in quaternion coordinates and integrates monomials over three independent `S^3` variables. The two routes agree for every monomial used by the degree ladder.

The common-`V` discriminator is exact:

\[
E[xzwt]=1/64.
\]

A control that resamples independent `V` copies between the two branches gives zero and is rejected as the primary model.

## Normalized static integral

The normalized expectation is

\[
{E[O\exp(\kappa S)]\over E[\exp(\kappa S)]},\qquad \kappa=1/64.
\]

The frozen ladder is `N=0,2,4,6,8`; the observable has degree 8, so the maximum monomial degree is 16. Since `|S|<=7` and `|O|<=1`, the Taylor tail is bounded rigorously by the exponential remainder. The final `N=8` primary interval has width below `1e-12`.

The checker also evaluates the signed fixture `kappa=-1/64`, verifies the kappa-zero partition and numerator, and records the conditional outer partition structure. After integrating out `W` at fixed `V`,

\[
K_\kappa(y)=\sum_{m\ge0}{[\kappa^2(1+y)/2]^m\over m!(m+1)!},
\]

and the outer measure uses `exp(kappa*y) K_kappa(y) Z_U(y)`, not bare Haar and not averaged normalized inner expectations.

## Freeze-W regression

Setting `W=I` gives `z=1`, `t=y`, and

\[
S=3x+2y+w+1.
\]

The constant factor cancels in the normalized quotient, leaving the old two-link action `3x+2y+w`. The generated interval overlaps the Round18 C2 primary interval, so the regression is recorded as passed.

## Evidence

Run from this directory:

```bash
python -B check.py --output /absolute/new/output_dir
```

Generated files:

- `results.json`: summary theorem, static-kappa scope, interval and controls;
- `graph-reduction.json`: actual graph, signed face words, affected and constant face ledgers;
- `moment-table.json`: exact route-agreement moment table through the frozen ladder;
- `intervals.json`: primary, negative-kappa and freeze-W interval ladders;
- `taylor-ladder.csv`: compact ladder rows;
- `controls.json`: discriminators and exception controls;
- `source-manifest.json`: source, report, contract, B2 gate, lessons and Round18 C2 input hashes.
