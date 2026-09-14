# P1 forward: the static section has no closable physical Hilbert extension

The frozen P1 section is a well-defined map of smooth invariant functions,
but is not closable in the declared L2 spaces. It does not intertwine the
electric generators for any c, and the designated slope fit fails the reserved
full-time channel. These are exact obstructions for this section and these
endpoints. Physical calibration remains open. No current reverse/P1 or
skeptic/P1 material was consulted before this submission was frozen.

## 1. Graph, states, and domains

Use precisely contract p1.json: the 18 vertices (x,y,z), 0<=x,y<=2,
0<=z<=1, all 33 positive nearest-neighbor edges, all 20 elementary faces,
and gauge actions at every vertex. Independent enumeration in check.py
reconstructs every signed face and compares it with admitted C1 bytes.
Edges are enumerated by axis x,y,z, then lexicographic base coordinate.
The active edges are 28=z(1,1,0)=U, 27=z(1,0,0)=V,
24=z(0,0,0)=W. The complete nonconstant restrictions are

| Face | Active word | Normalized trace |
|---|---|---|
| f8_xz_000 | VW^-1 | t |
| f9_xz_010 | U | x |
| f11_xz_100 | V^-1 | y |
| f12_xz_110 | U^-1 | x |
| f14_yz_000 | W^-1 | z |
| f16_yz_100 | UV^-1 | w |
| f17_yz_110 | U^-1 | x |

The other 13 faces restrict to the identity, including all eight xy faces.
Thus C1's static sum 13+3x+y+z+w+t is verified, without promoting it to
a dynamical reduction. The graph is connected, so its cycle rank is
33-18+1=16. The fixed 30-edge subgraph is also connected and has cycle
rank 30-18+1=13. A spanning tree has 17 edges. Setting these 30 edges
to identity imposes 13 additional independent loop constraints beyond
tree gauge fixing; three remaining variables cannot parameterize general
physical configurations modulo gauge.

Hphys=L2(SU(2)^33,Haar^33)^G and Hcond=L2(SU(2)^3,Haar^3)^Ad
use normalized Haar. Their constant ground vectors have norm one.
On the specified invariant smooth/Peter-Weyl core,
H_E=alpha sum_e C_e and H_c=c(C_U+C_V+C_W), with
C=-sum_a L_a^2 and T_a=-i sigma_a/2. These are restrictions of positive
elliptic self-adjoint product Laplacians to reducing invariant sectors,
with the declared H2 intersection domains. The section R sends the
physical smooth core into smooth simultaneous-conjugation invariants:
a common vertex gauge h conjugates U,V,W and leaves all fixed identities
unchanged. This statement is only a smooth-function statement.

## 2. An invariant core sequence proves nonclosability

Let L0=g0 g16 g2^-1 g12^-1 be the holonomy of f0_xy_000.
Its trace characters are invariant under all vertex gauges, and L0 is
Haar-distributed in the physical product state by integrating any one
of its four independent edges. For n>=1 let chi_n be the SU(2) spin n/2
character, of dimension n+1, and set

    f_n = chi_n(L0)/(n+1).

Each f_n is a smooth invariant Peter-Weyl polynomial in the full operator
core. Character orthogonality and chi_n(I)=n+1 give exactly

    <1,f_n>phys=0,  ||f_n||phys=1/(n+1),  R f_n=1.

For completeness, writing Tr(g)/2=cos(theta), Haar class integration is
(2/pi) sin(theta)^2 dtheta on [0,pi], while
chi_n(g)=sin((n+1)theta)/sin(theta). Ordinary sine orthogonality proves
both integral statements for every n, not just the executable fixtures.
Hence f_n ->0 in physical L2 but R f_n ->1 in conditional L2. The graph
closure of R contains (0,1): R is not closable, and there is no bounded
extension agreeing with R on this dense invariant core. The diverging
operator norm ratio is n+1. The n limit changes only a test-function
representation label at fixed graph, alpha/E_star, hbar and spacing;
it is not a physical ultraviolet or volume limit.

Already F0=chi_1(L0)/2 has physical mean zero and variance 1/4, whereas
R F0=1 has mean one and variance zero. Therefore the section also fails
state compatibility despite R1=1. No assumption about point evaluation
of arbitrary L2 representatives, and no unsupported trace theorem, is used.

## 3. Complete electric derivatives and scalar test

Since -sum_a T_a^2=3I/4, a normalized fundamental Wilson loop through
four distinct edges obeys C_e F=3F/4 for each of those four edges and
zero for the other 29. Inverse edges carry the dual representation with
the same Casimir. This evaluates the derivatives before restriction:

    H_E F0=3 alpha F0,   H_E F9=3 alpha F9,
    H_E F16=3 alpha F16.

All fixed edges in these words contribute. In particular F9 uses edges
(2,28,3,25), including three fixed edges; F16 uses (16,28,17,27),
including two fixed edges; all four F0 edges are fixed. Restricting first
would discard 9alpha/4, 3alpha/2 and 3alpha respectively.
On the conditional side,

    H_c 1=0,   H_c x=(3c/4)x,   H_c w=(3c/2)w.

Thus (R H_E-H_c R)F0=3alpha times 1, of conditional norm 3alpha,
for every c. An added scalar lambda I is forced to have lambda=0 by
the core test on 1. Subtracting a physical scalar likewise must respect
the declared zero ground energies; a common equal shift cancels from
the proposed relation and does not remove this defect. These explicit
core calculations are legitimate unbounded-operator tests because all
test functions belong to both stated domains after smooth restriction.
No extension of R to an unbounded-operator domain is presumed.

## 4. Designated training fit and held-out full time

Use C_H(A,B;t)=<A1,exp(-tH/hbar)B1>-<A1,1><1,B1>, t>=0,
with the inner product conjugate-linear in its first slot. All four
nonconstant functions F9,F16,x and w have mean zero and variance 1/4;
the latter pair follow by Haar integration of U or UV^-1. More generally
multiplying the two channel observables by complex a,b multiplies each
displayed autocorrelation by conjugate(a)b. Spectral calculus on the
exact eigenvectors gives full semigroup formulas with no power-series
domain assumption:

    C_E(F9,F9;t)=1/4 exp(-3alpha t/hbar),
    C_c(x,x;t)=1/4 exp(-3c t/(4hbar)).

Their nonzero initial slopes are -3alpha/(4hbar) and -3c/(16hbar).
The training rule uniquely fixes c=4alpha. For this eigenchannel that
fit also happens to match the full training curve. It does not test other
channels. With that same c and clock, the reserved comparison is

    C_E(F16,F16;t)=1/4 exp(-3alpha t/hbar),
    C_c(w,w;t)=1/4 exp(-6alpha t/hbar),
    Delta(t)=1/4[exp(-3s)-exp(-6s)]>0 for t>0, s=alpha t/hbar.

At the fixed positive time t_star=hbar/alpha, exact rational alternating
Taylor bounds for exp(-1), then monotone powers and interval subtraction,
certify the numerical Delta recorded in results.json. The associated
core defect after fitting is (R H_E-H_c R)F16=-3alpha w, of norm
3alpha/2. Refitting c=2alpha to this held-out channel would break F9 and
violates the declared training/holdout split. A scalar cannot change
these centered gaps while retaining the actual ground condition.

## 5. Scope and possible repair after review

The accepted result is the nonclosability/state/core obstruction and the
exact held-out mismatch, not a matched physical generator. A justified
next map candidate is a genuine 17-edge maximal-tree reduction retaining
16 loop variables and residual simultaneous conjugation, with the induced
electric derivatives including their cross terms. A three-variable
compression would additionally need a specified Haar conditional
expectation or another bounded map, and proof of the relevant generator
invariance or quantified compression error. Neither is implemented or
selected here; P2 awaits skeptical review.

Primary support is identified at actual reading depth in source-notes.md.
The calculations above are independent for the actual graph. This P1
failure differs from inherited K1's same-coordinate principal-symbol
test and a finite-slope underidentification statement: it supplies an
explicit physical invariant-core nonclosability sequence and one reserved
whole-time prediction. These are analytic electric/product-endpoint
predictions at magnetic coefficient zero and kappa=zeta=0, not measured
calibration data, an interacting J2/O transfer, a physical mass gap, or
a continuum Yang-Mills result. Scientific priority is unverified.

The checker independently enumerates the entire finite graph; tests exact
SU(2) character norms and all 33 per-channel electric contributions;
derives the fit and a rational held-out interval; rejects the false map,
state, scalar and refit proposals; and hashes every contract dependency,
instruction snapshot, consulted inherited report/code, and executed proof
artifact. Finite character fixtures accompany the all-n proof above.
