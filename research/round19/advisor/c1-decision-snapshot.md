# C1 decision snapshot

Status: accepted for Goal C loop 1 only.

C1 establishes an exact static three-link U-V-W chain integral on the actual four-cube graph with all other links fixed to identity. It is a static mathematical checkpoint. It does not satisfy physical energy/time-scale matching, does not use `kappa` as `E_star`, and does not prove dense stability, finite-volume convergence, continuum Yang-Mills, a spectral gap theorem, or the Clay mass gap.

Both implementations reconstruct the 18-vertex, 33-edge, 20-face graph with active vertical links `U=(1,1,0)`, `V=(1,0,0)`, and `W=(0,0,0)`, seven affected faces, thirteen constant faces, and thirty fixed links. The signed face-word reduction gives

\[
S=3x+y+z+w+t,
\]

where `x=Tr(U)/2`, `y=Tr(V)/2`, `z=Tr(W)/2`, `w=Tr(U V^dagger)/2`, and `t=Tr(V W^dagger)/2`. The observable remains the old U-V branch observable

\[
O=(4x^2-1)^3(4w^2-1)/81.
\]

For `kappa=1/64`, the accepted normalized static expectation is enclosed by the forward interval

\[
[13325994408253817/16816281566993287151031,
  13325994823319489/16816281566992872085359],
\]

with width below `1e-12`. The reverse interval is tighter and lies inside this enclosure. For `kappa=-1/64`, the accepted forward enclosure is

\[
[12038974297206137/16816249495448420068791,
  12038974712271809/16816249495448005003119],
\]

again with width below `1e-12`; the reverse interval is tighter and contained in it. The positive and negative `kappa` enclosures are disjoint. The sign asymmetry is also supported by exact odd coefficients, with numerator Taylor coefficient `N3=13/1296`.

The exact coefficient rows through degree 8 agree between forward and reverse. In particular, numerator Taylor coefficients begin

\[
N_0=0,\quad N_1=0,\quad N_2=1/324,\quad N_3=13/1296,
\]

and partition Taylor coefficients begin

\[
Z_0=1,\quad Z_1=0,\quad Z_2=13/8,\quad Z_3=1/4.
\]

Both implementations agree on all 6054 moments through max total degree 16 when keyed by exponent vector. The exact common-V discriminator is

\[
E[x z w t]=1/64,
\]

while an independent-V resampling model gives `0`; this is the accepted failed-independence exception.

The freeze-W regression is accepted as an exact coefficient and constant-cancellation statement: setting `W=I` gives `S=3x+2y+w+1`, and `exp(kappa)` multiplies numerator and partition by the same factor. The accepted evidence is the coefficient identity/convolution, not mere overlap of finite intervals.

The final independent comparison accepts 27 checks. It canonicalizes moments by exponent vector, recomputes coefficient/interval ladders with positive partition denominator checks and a geometric tail lower bound, checks signed quaternion word fixtures, verifies static-scale wording, validates source manifests, and rejects graph, action, observable, independent-V, divisor, truncation, sign, scale, and missing-manifest mutations.
