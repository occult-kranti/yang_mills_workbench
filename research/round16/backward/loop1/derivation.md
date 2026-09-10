# Independent shared-face audit — Round16 Loop1

The result is an exact finite normalized SU(2) link-Haar identity. It establishes a graph-integration dependency. It does not construct a physical time generator, a volume-uniform interacting Hamiltonian gap, or four-dimensional continuum Yang–Mills theory.

## Work backward from the mixed observable

The requested new moment contains ten outer normalized fundamental traces and the square of the internal trace. An ordinary two-factor link orthogonality argument cannot integrate the four shared-boundary links: each now has four matrix occurrences. That is the specific new obligation. The independent implementation expands the actual trace indices and applies the fourth-order Haar projector on each of those four links; it never calls the producer's fusion or disk moment function to obtain an expected value.

The independent graph parser reconstructs elementary coordinate squares from vertices and edges. It verifies twelve vertices, twenty edges and eleven distinct faces. The unique square at x=1 is internal. Four edges have incidence three, and the other sixteen have incidence two. Removing the internal face produces a ten-face sphere, with Euler characteristic 12−20+10=2. The square boundary words are checked against their actual signed links. Declared disk memberships, cell orientations, Haar convention and full versus outer action are also checked.

For distinct face products, construct the face-to-edge boundary matrix over GF(2). Independent column elimination gives rank nine. Exhaustive enumeration of all 2,048 masks finds precisely four kernel elements: the empty surface, the two six-face cube boundaries, and their symmetric difference, the ten-face outer boundary. Every other product vanishes because multiplication of one odd-incidence Haar link by the center element −1 changes its sign. Even incidence is only a necessary condition; the four remaining amplitudes are evaluated by actual matrix-index contraction.

For an oriented closed surface, the second Haar moment is

\[
\int U_{ab}\overline{U}_{cd}\,dU=\frac{\delta_{ac}\delta_{bd}}2.
\]

Trace-position indices, rather than presumed graph vertices, are identified explicitly. A connected fundamental color loop contributes two, a paired link contributes 1/2, and each normalized trace contributes 1/2. The one-cube calculation has eight surviving color loops, twelve links and six traces, giving 2^(8−12−6)=1/1024. The outer surface has twelve color loops, twenty links and ten traces, giving 2^(12−20−10)=1/262144. Whole-face reversal is allowed when orienting a selected surface because the SU(2) trace is real and invariant under inversion.

## The independent fourth-order projector

Write the two shared trace copies with opposite whole-face orientations. Their product is still x_shared². At each shared-boundary edge the resulting integrand contains two matrix entries of U and two of its complex conjugate. There are two row and two column pairing permutations. The invariant-pairing Gram matrix at representation dimension two is

\[
G=\begin{pmatrix}4&2\\2&4\end{pmatrix},\qquad
G^{-1}=\begin{pmatrix}1/3&-1/6\\-1/6&1/3\end{pmatrix}.
\]

The coefficients therefore follow by exact matrix inversion: matching row/column permutations have weight 1/3; unequal permutations have weight −1/6. These are not fitted constants. The balanced SU(2) fourth moment equals the U(2) moment because its integrand is invariant under an overall U(1) phase; the U(2) Haar integral factors into that irrelevant phase and SU(2). Thus the two invariant pairings provide the complete projector here, including the antisymmetric SU(2) channel.

The code first integrates the sixteen ordinary links, then enumerates all 4^4=256 choices of row and column pairings at the four shared links. For each term it counts the remaining trace-index equivalence classes and multiplies the exact rational weights. The positive contributions sum to 1681/42467328 and the negative contributions sum to −25/663552. Their exact sum is

\[
\left\langle\prod_{f\in\mathrm{outer}}x_f\;x_s^2\right\rangle_0
=\frac1{524288}=2^{-19}.
\]

Dropping the negative projector terms gives the incorrect value 41/2654208. Replacing the projector by two independent pairs gives the different incorrect value 41/8388608. Omitting the shared insertion gives 1/262144. All three are discriminating controls.

The mixed-representation insertion follows from the exact SU(2) identity χ₂=4x²−1:

\[
\left\langle\prod_{f\in\mathrm{outer}}x_f\;\chi_2(U_s)\right\rangle_0
=4\,2^{-19}-2^{-18}=2^{-18}.
\]

The eleven-fundamental product instead vanishes: a shared-boundary link appears three times. This distinction directly rejects a transfer of the old one-surface formula to the full eleven-face complex.

## Independent normalization and the disk implication

Our character convention is the ordinary unnormalized character χ_n, with n=2j and dimension d_n=n+1. Characters are orthonormal under normalized Haar measure. Therefore a class weight has coefficients

\[
a_n=\int f(U)\chi_n(U)\,dU,
\quad f=\sum_n a_n\chi_n.
\]

There is no extra factor d_n in this definition. A convention that places d_n outside the expansion must redefine the coefficient accordingly. In particular x=χ₁/2 and x²=(χ₀+χ₂)/4.

The five-face disk has four interior vertices and eight nonboundary edges. Tree gauge integration has volume one, and four elementary character convolutions leave one boundary character with coefficient d_n^−4 times the five face coefficients. The two disks have disjoint internal links, conditional on their shared boundary. The remaining holonomy is Haar. This justifies the producer's finite-polynomial reduction; the actual mixed raw-index computation independently tests its crucial shared-edge factor.

As an additional independent check, `character_triple` constructs each χ_n as a polynomial in t=Tr U using χ_(n+1)=tχ_n−χ_(n−1), multiplies three polynomials, and integrates monomials with the exact Haar semicircle moments: odd moments vanish and the 2r moment is Catalan(r). It verifies all 343 label triples with n,m,k from zero through six, including forbidden parity and triangle cases. This polynomial oracle does not use the producer's triangle-inequality fusion test.

## Gauge, input and saved-evidence audit

The exact quaternion fixture consists of rational unit quaternions obtained by stereographic coordinates. For all eleven faces, independent vertex gauge transformations preserve the trace exactly, complete face reversal preserves it, and reversing only one dagger produces a nonzero exact gauge defect. An inhomogeneous full action is gauge invariant. The full and outer actions differ by exactly one nonzero shared-face term in this fixture.

Graph mutations omit or duplicate a face, break a dagger, replace integer signs or normals with Booleans, corrupt disk memberships or cell orientation, and substitute an outer action or unsupported time generator. Both independent and producer validators reject these cases. The retained producer cache-alias failure is also challenged: mutating the returned public coefficient dictionary must leave later moments unchanged, and a populated integer cache cannot admit Boolean input. The current repaired source passes.

The saved 2,048-row producer ledger is independently reconstructed, including selected face sets, odd edge sets, moments, and all reference insertions. A passed status alone cannot substitute for this replay. Tests reject missing rows, modified sources, altered graph hashes or scopes, and a plausible outer-only replacement for the mixed moment. All fourteen files in the producer manifest are checked against their current hashes. Inputs are checked again at the end of the run.

The acceptance runs contain 118 named gates, plus the exhaustive 2,048 subset and 343 triple comparisons. Ordinary Python and `python -O` outputs are byte identical. The earlier 111-gate outputs predate the added saved-evidence checks and remain as intermediate records. The mathematical production module and this independent module were read at function and line scope; this is not a claim of exhaustive branch coverage or an audit of unrelated historical files.

## Separate physical energy-scale review

For a fixed self-adjoint spectral problem, multiplying its operator by α>0 multiplies its spectrum and gap by α. On finite open cubic graphs with Gauss law at every vertex and no charges, a nonvacuum spin network has active minimum degree at least two and hence contains a cycle. These bipartite graphs have girth four. Each nontrivial edge contributes at least j(j+1)=3/4; a fundamental Wilson square saturates the lower bound. Thus the exact free physical gap is 3α.

The independent audit enumerates elementary squares for n=2,3,4 and checks all recorded larger-box face counts from the three choices of coordinate plane. It reconstructs every scale row and the signed global norm bound. With α_n=1/n and λ_n=0 the dimensionless free gap stays exactly three, while the physical gap 3/n tends to zero. A common dimensionless lower bound alone consequently supplies no common physical lower bound. If α_n≥α_min>0 and Δ(K_n)≥d>0, then Δ(H_n)≥α_min d.

The scale condition is sufficient and needed for that inference from lower bounds alone; it is not universally necessary for arbitrary spectral families. A divergent dimensionless gap could compensate for α→0. An explicit algebraic compensation example is checked, preventing an overstatement of necessity. The free-box counterexample has no such compensation. Negative global perturbation lower bounds remain insufficient certificates and do not imply gap closure. Euclidean κ parameters are not identified with λ/α.

## Feedback for the unexecuted second loop

The all-eleven observable at nonzero outer coupling need not have zero mean when the internal coupling is set to zero. At common outer t, center parity forces the first nonzero numerator term to add one extra power on either entire five-face disk. Each choice contributes 41/(81·2^19), so the numerator begins 41 t^5/(81·2^18)+O(t^7). This follows from the two allowed labels 0 and 2 of x², with ordinary coefficients 1/4, together with the reviewed disk factor. At zero outer coupling, differentiating the numerator with respect to the shared coupling gives the independently checked 2^−19 mixed moment.

A second loop should therefore compare the same observable in the full and outer-only actions with separate exact normalization and total-action remainders. This note records a planning implication; the nonzero-coupling simulation and its coefficient audit have not been executed in Loop1.
