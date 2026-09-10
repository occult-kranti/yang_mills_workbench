# C1: the complete four-adjoint central-link tensor

## Actual cubical geometry and what is integrated

The full cell complex has four cubes arranged in a 2 by 2 by 1 box. Its vertices are x,y in {0,1,2}, z in {0,1}. Positive coordinate links and explicitly signed elementary square words give 18 vertices, 33 edges and 20 distinct faces. Cell-face incidence identifies four internal faces and sixteen outer faces. The unique edge incident to four faces is the vertical central link from (1,1,0) to (1,1,1). Removing the internal faces from the face set leaves an outer-boundary graph with 18 vertices, 32 edges and 16 faces; the central edge is absent.

The integral here is over that one central link with normalized SU(2) Haar measure while every other link is fixed. This is not the twenty-face bulk integral. It does not define a physical Hamiltonian, transfer eigenvalue or mass scale. Earlier spectral results and their common physical energy normalization alpha are separate.

## Complete invariant subspace, not an assumed channel

The adjoint is the real spin-one representation R(U). With V=R^3, the central integral is the 81 by 81 matrix P=integral R(U)^(tensor 4) dU. On V^(tensor 4), write

    B1_abcd = delta_ab delta_cd,
    B2_abcd = delta_ac delta_bd,
    B3_abcd = delta_ad delta_bc.

Each is invariant because R is orthogonal. Direct summation of all 81 components gives the Gram matrix with diagonal 9 and off-diagonal 3. Its eigenvalues are 15,6,6, so these vectors are independent. The inverse has diagonal 2/15 and off-diagonal -1/30.

Completeness is a separate representation-theoretic step. Pairwise spin-one addition gives 1 tensor 1 = 0 direct-sum 1 direct-sum 2, with each summand once. Two such pairs combine to a singlet precisely when their intermediate spins agree, supplying one invariant for each of j=0,1,2. Thus the invariant dimension is exactly three. The three independent B columns span the entire invariant space; it is not enough merely to observe rank three in an arbitrary matrix.

Normalized Haar averaging of a unitary representation is the orthogonal projector onto its invariant space: group invariance fixes its range, inversion gives self-adjointness, and convolution gives idempotence. Therefore the complete tensor is

    P = B (B^T B)^(-1) B^T.

All 6561 matrix entries are retained. Exact tests verify the full matrix, not only its rank: symmetry, idempotence, trace three, fixed invariant columns and invariance under a nontrivial rational adjoint rotation. The analytic delta-tensor argument establishes group invariance for every rotation; a finite rotation test is only an implementation check. The independent reviewer constructs the same matrix through quaternion sphere moments, using separate arithmetic.

Deleting the negative off-diagonal inverse entries destroys idempotence. Retaining only one normalized B channel gives a genuine rank-one projector, but misses two invariant channels. Neither is the complete Haar integral.

## Boundary holonomies realized by actual signed paths

Each of the four incident face words is reversed in its entirety if necessary, then cyclically rotated so the central link U appears first with positive orientation. This preserves the real SU(2) character. It yields a closed square word U times a three-edge boundary path H_i. Changing only one dagger would not implement this reorientation and is rejected by the signed closure check.

The four three-edge paths are disjoint outside U. Each contains one distinct outer vertical link. Set the other surrounding links to identity and assign that vertical link H_i or its inverse according to its path sign. This realizes, on the full 33-link graph,

    H1 = (1, 1, 1, 1)/2,
    H2 = (1, 1,-1,-1)/2,
    H3 = (1,-1, 1,-1)/2,
    H4 = (1,-1,-1, 1)/2.

These are unit quaternions and are not commuting boundary data. Their trace directions a_i=(h_i0,-h_i1,-h_i2,-h_i3) form an orthonormal basis of R^4, so Tr(U H_i)/2=q dot a_i for a unit quaternion q representing U. The runner verifies the path identities on four exact central-link fixtures, checks all twenty original face holonomies under a specified nonconstant assignment of vertex gauge transformations, and compares eighty actual face words to a separate raw complex 2 by 2 matrix multiplication. The general gauge-covariance identity follows by cancellation of adjacent endpoint transformations along each closed signed word. These tests connect the tensor calculation to the signed link geometry.

## A channel-sensitive exact contrast

For each face use the normalized adjoint observable chi_2(U H_i)/3, where chi_2=4(Tr/2)^2-1=Tr R. The fourfold product has denominator 3^4=81. At zero central action its exact conditional expectation is

    Tr[P (R(H1) tensor R(H2) tensor R(H3) tensor R(H4))]/81
      = -1/405.

The unnormalized character product is -1/5. This sign is compatible with Haar positivity: the real adjoint character itself takes negative values, and the product is not pointwise nonnegative. Each single normalized adjoint mean is zero by Haar orthogonality, so their product is zero and does not reproduce the joint expectation.

The invalid diagonal-only inverse instead gives +2/405, and the rank-one channel gives +1/729. These are decisive sign errors, not small floating-point differences. The identity-boundary fixture gives 3/81=1/27, independently checking normalization against the invariant dimension.

This establishes a finite conditional obstruction to discarding recoupling channels. It does not assert that the same number survives integration of the surrounding links. At this stage the central action is exactly zero. The proposed nonzero-coupling C2 calculation has not been executed.

## Reproduction

Run `python -B check.py --output ../c1-output` from this source directory. All mathematical code uses standard-library rational arithmetic; the additional raw complex matrix comparison is a finite arithmetic diagnostic. Outputs include the complete projector, graph, signed boundary assignments, a CSV of retained correct and incorrect contractions, semantic check results and hashes. Normal and optimized runs must give identical output bytes. Independent scientific acceptance is separate from the author checks.
