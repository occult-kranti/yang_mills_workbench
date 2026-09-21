# AA1: the complete free-cube shell, before an embedding claim

One agent performed the derivation, reverse construction and skeptical review. The checks are correlated. The contract was frozen before computation. The first attempt stopped at an unavailable symbolic dependency; the admitted producer uses only Python's standard library and exact fractions.

## Forward synthesis

Use the canonical reference Hamiltonian and the U observable, with fixed positive alpha and hbar. Translate the unit cube by O=(3,1,0). Every x edge has tail x=3, every y edge has tail y=1, and every z edge is free. Thus all twelve are independent free Casimir factors, with the outside reference ground unchanged. Each of the six cube faces is omitted from the reference strips. Work first on the cube's all-vertex gauge invariant subspace.

An energy 9/2 spin network has, in quarter-energy units, 3 n_(1/2)+8 n_1+15 n_(3/2)=18; larger spins already exceed the total. The only nonnegative integer solutions are six spin-half edges, or one spin-half and one spin-3/2 edge. Two distinct edges form a forest and leave a nontrivial representation at a leaf, so the latter has no invariant intertwiner. In the former, each degree-three cube vertex must have zero or two incident half-spins: one or three half-spins cannot couple to the singlet. The occupied graph is a union of cycles. The cube has no cycle shorter than four, so six occupied edges form one simple six-cycle. Every degree-two invariant intertwiner is unique. This proves completeness, not merely a choice of trial functions.

The basis functions are the unnormalized fundamental characters phi_C=Tr(U_C). Their Haar squared norm is one, since an independent product of Haar matrices is Haar and fundamental characters have norm one. Distinct cycles are orthogonal by changing the sign of a link present in exactly one cycle. The checker finds sixteen cycles by both six-edge subset enumeration and closed six-vertex path enumeration.

For x_f=Tr(U_f)/2, center parity forces a matrix element to vanish unless C symmetric-difference D equals the four-edge face f. The enumeration verifies that every surviving flip replaces two adjacent edges with the other two edges. Let their path transports be X,Y and let Z be the remaining common four-edge path. These are independent Haar products. Character convolution gives

    integral chi(X Z^-1) chi(Y Z^-1) dZ = chi(X Y^-1)/2,
    <phi_D,x_f phi_C> = (1/4) integral chi(X Y^-1)^2 dX dY = 1/4.

The characters are real for SU(2), so reversing a loop orientation changes no sign. Diagonals vanish by the same parity rule. These facts determine every entry: B_cube=-A/96, where A is the sixteen-vertex flip adjacency matrix. This is a compressed omitted potential, not yet a proof of reducing-subspace closure in the full reference energy shell.

Exact matrix arithmetic gives twelve vertices of degree two, four of degree six, and

    A(A^2-4I)(A^2-12I)=0.

The rational projectors on squared eigenvalues 0,4,12 have traces 8,6,2. Their A-weighted traces vanish. Consequently the eigenvalues are 0 (multiplicity 8), +/-2 (each 3), +/-2 sqrt(3) (each 1). No floating diagonalization is used.

## Reverse reconstruction from the actual U input

Construct phi_X and phi_Y from the original two short paths and common four-edge Z path, rather than selecting a convenient eigenvector. For psi=(phi_X+phi_Y)/sqrt(2), the first seven adjacency moments are 1,1,4,8,32,80,320. The exact spectral weights are

| eigenvalue | weight |
|---|---:|
| 0 | 1/3 |
| +2 | 3/8 |
| -2 | 1/8 |
| +2 sqrt(3) | 1/12+1/(8 sqrt(3)) |
| -2 sqrt(3) | 1/12-1/(8 sqrt(3)) |

Put theta=z/84, using the inherited slow endpoint rho=8z/7. The cube scalar is therefore

    f_cube(z)=1/3 + cos(2 theta)/2 + cos(2 sqrt(3) theta)/6
      + i[sin(2 theta)/4 + sin(2 sqrt(3) theta)/(4 sqrt(3))].

This formula has the correct inherited slope +i z/84. Its complete scalar Taylor remainder obeys |f_cube-1-i theta|<=2 theta^2=z^2/3528, from the second moment 4. Centering the adjacency random variable by its mean 1 similarly gives |f_cube-exp(i theta)|<=3 theta^2/2. These are continuum-in-z analytic bounds, not fitted sample tolerances. At z=1e-6 the first disk radius is below 2.835e-16. Until AA2, neither formula is identified with the full canonical endpoint.

## Skeptical self-review and decision

The two-state U plane fails even inside the averaged cube shell: each initial basis vector has outgoing flip edges to other six-cycles. Replacing it by a single phase or a two-state cosine loses the actual second moment. The exact sixteen-state compression repairs this particular omission. It does not repair all omissions automatically.

The unresolved objection is an exterior face that trades a cube spin for excitations in selected strips or other free factors at exactly equal total reference energy. The strip ground gap is not a separation theorem around arbitrary excited energies. Enumerating cube states does not exclude such an exterior resonance. We therefore admit AA1's exact cube result and mark the larger canonical target limited at this gate.

AA2 is selected to test a geometric charge-selection workaround: enumerate all exterior faces incident to the cube, prove strictly positive exterior energy after every allowed fusion, and either establish a reducing observable-reachable component of the whole energy block or exhibit its missing states. Only after that proof may the cube scalar be called the full endpoint. A source-specific participating-frequency bound is a further target, not an inherited assumption.

Scientific priority is unverified. Historical Newton analysis/synthesis and Tesla loading checks suggested the questions; Haar theory, Gauss constraints and the explicit matrix establish these statements. This is neither a homogeneous lattice gap nor a continuum construction.
