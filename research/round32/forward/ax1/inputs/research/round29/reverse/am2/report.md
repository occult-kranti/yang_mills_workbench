# HNM four-site stability certificate — independent reverse AM2

Project author: Hruday N M (BUNZEEY). The candidate majorant and constants were shared by the advisor before execution; the derivation below independently checks them. Creation expansions are established methods, with Gauvin's inspected supplement A.6–A.8 an explicit proof template and Yarotsky the inherited qualitative source. This is a model-specific quantitative adaptation, not an asserted priority discovery. No current forward/skeptic AM2 output was read.

## Statement and exact model

For every nonempty finite complete-factor I1 volume, retain the original selected-strip onsite operators, all whole-star omitted interactions, and every original endpoint gauge action. Normalize by delta=alpha/8>0, after subtracting the reference strip ground scalars. Write H=H0+V, H0=sum_x h_x, h_x>=Q_x=I-|Omega_x><Omega_x|. Each V_X is an original omitted anchor group with its declared support of size at most four; repeats are separate indexed terms. The actual site sum obeys J=sup_u sum_(X contains u)||V_X||<=28|tau|. For |tau|<=10^-8, the actual untruncated physical Hamiltonian has a unique physical ground and gap at least 1/2 in these normalized units, hence alpha/16 in energy units. An empty volume has only the vacuum, so spectral exclusion is vacuous and no excitation is asserted.

This is a finite-volume theorem uniform over the stated volume family. It does not numerically evaluate Yarotsky c1/c2 or identify the inherited infinite-volume state at every coupling in this new interval.

## 1. Excitation sectors, covariance and cutoffs

First impose finite-rank full spectral projections of each h_x, including its ground. They are nested, gauge covariant and increase strongly to identity. Onsite spectra are discrete because each finite rotor factor is elliptic on a compact manifold with bounded smooth potential. Their ground is unique, positive and fixed by all endpoint gauge actions. The product vacuum is Omega.

For nonempty M, P_M is Q_x on x in M and the vacuum projector elsewhere. These projectors commute with all gauge actions. On its physical range C_M, H_M=sum_(x in M)h_x>=|M|. This uses one gap per factor, with no four-factor or four-link premise. Physical c_M defines the creation operator c-hat_M=|c_M><Omega_M| tensor I_outside. Factorized gauge actions and the invariant exterior vacuum prove covariance. Creation operators commute; overlapping supports give zero product because the vacuum bra at a shared factor annihilates the excited ket. These are finite-cutoff bounded identities.

For a physical collection c use ||c||=sup_u sum_(M contains u)||c_M||, and C=sum_M c-hat_M. This sum can be extensive in a fixed finite volume; no bounded infinite-volume operator is asserted. Since every nonzero product has disjoint nonempty supports, C is nilpotent and e^C and e^-C are finite inverse polynomials.

## 2. Derive the complete four-site coefficient

For collections c1,...,ck define

\[
L_k(c_1,\ldots,c_k)_M=H_M^{-1}P_M\operatorname{ad}_{C_1}\cdots\operatorname{ad}_{C_k}(V)\Omega.
\]

Fix one indexed interaction V_X and one creation support I_j per commutator. Each I_j must meet X: creations commute, so a disjoint one can be moved innermost and then its commutator is zero. Put N=union_j I_j. Outside X a nonzero product excites every singly touched factor; twice touched factors make that product zero. Hence N\X subset M subset N union X. There are at most 2^4=16 possible M, and |I_j|<=|M|+4. The expanded commutator has 2^k products, each bounded by ||V_X|| times the product of the vector norms. These estimates count support sets, not internal basis states.

Anchor the output at u in M and overcount two possibilities. If u in X, use ||H_M^-1||<=1 and sum each incoming collection over supports meeting X at cost at most 4||c_j||. Summing X containing u costs J. The coefficient is 16*8^k.

If u lies in an I_j, use

\[
\|H_M^{-1}\|\le {1\over|M|}\le {5\over|I_j|},
\]

since |M|>=1 and |I_j|<=|M|+4. Sum the other k-1 collections at cost 4^(k-1), and use sum_(X meets I_j)||V_X||<=J|I_j|; this cancels the inverse denominator. There are k choices of j. This contribution is 16*2^k*5k*4^(k-1). Thus

\[
\|L_k(c_1,\ldots,c_k)\|
\le J\,16\,8^k(1+5k/4)\prod_j\|c_j\|. \tag{HNM-AM2.1}
\]

For k>8, one side of V_X in each expanded product has at least five creations meeting a set of at most four sites. Two overlap and their product vanishes. Consequently these nested commutators are identically zero. The positive infinite majorant is nevertheless convenient:

\[
G(t)=\sum_{k\ge0}{16\,8^k(1+5k/4)\over k!}t^k
=16e^{8t}(1+10t).
\]

All sums above are finite in the cutoff proof. No neglected generated support, incoming star, scalar or diagonal term appears in this derivation.

## 3. Complete fixed point with scalar energy

Interpolate H(s)=H0+sV for -1<=s<=1. Because [H0,c-hat_M] is the creation associated with H_M c_M, all further creation commutators with it vanish. Thus e^C H0 e^-C=H0-sum_M creation(H_M c_M). The vector psi(s)=e^-C Omega has vacuum coefficient one. It is an eigenvector exactly when

\[
c=s\sum_{k=0}^{8}{L_k(c,\ldots,c)\over k!},\qquad
E(s)=s\langle\Omega,e^CVe^{-C}\Omega\rangle. \tag{HNM-AM2.2}
\]

The scalar equation is required; E(s) is not set to zero and no diagonal compression is discarded. On the ball ||c||<=R=1/64, the map norm is at most JG(R), and multilinearity bounds its Lipschitz constant by JG'(R). Since e^(1/8)<8/7 (bound its series by the geometric series),

\[
G(R)<148/7,\quad G'(R)<352,\quad J\le7/25000000.
\]

Therefore JG(R)<148/25000000<R and JG'(R)<2464/25000000<1. The map is a contraction of a complete finite-dimensional physical collection ball. The unique fixed point exists for every s and depends continuously on s by subtracting two fixed-point equations and absorbing the common Lipschitz constant. The eigenvalue E(s) is real and continuous because H(s) is self-adjoint and psi(s) nonzero.

## 4. Centered excited-sector exclusion

Constructing a vacuum alone would not prove a gap. Suppose a physical eigenvector phi independent of psi(s) has eigenvalue E(s)+z, z real and |z|<1/2. Decompose e^C phi=b0 Omega+sum_(M nonempty)b_M and define B=sum_M b-hat_M. Then b is nonzero and, since B commutes with C, phi=(B+b0)psi(s). Subtracting the two actual eigenvalue equations and conjugating gives

\[
b_M=s(H_M-z)^{-1}P_M[B,e^CVe^{-C}]\Omega. \tag{HNM-AM2.3}
\]

The H0 commutator contributes H_M b_M; the creation part from the fixed point commutes with B. The scalar E(s) cancels only because both eigenvalue equations use the actual E(s). This is not a bare-vacuum centering assumption.

As H_M>=|M|>=1, ||(H_M-z)^-1||<=2/|M| for |z|<1/2. Repeating the two anchored estimates costs at most two. The remaining commutator is the sum of ad_B ad_C^k V/k!, so its collection norm is at most 2JG'(R)||b||. But

\[
2JG'(R)<4928/25000000<1,
\]

forcing b=0, a contradiction. Thus E(s) is simple with no other physical eigenvalue at distance less than 1/2. At s=0 it is the ground. Finite-dimensional continuous eigenvalues cannot cross this isolated branch, so it remains the physical ground for all s. Both signs and the endpoint |tau|=10^-8 are included; the inequalities have positive slack. Zero V gives c=E=0 and the original gap directly.

## 5. Remove the cutoff in the actual model

Fix a finite volume. Tensor products of onsite eigenvectors form an H0 eigenbasis. Nested product spectral projections therefore approximate every vector in the form norm of H0, since the nonnegative spectral tails tend to zero. The projections commute with gauge actions; applying them to physical vectors proves the same form-core density in the physical space. V is bounded in that fixed volume, so after a harmless scalar shift H0+V has the same form core and compact resolvent, and is self-adjoint on D(H0).

The first two physical cutoff eigenvalues decrease to the first two untruncated physical eigenvalues by min–max: the lower inequality follows by restriction of trial spaces, and the upper limit follows by form-approximating the actual first two eigenspaces and their Gram matrices. Hence their difference retains the uniform 1/2 bound. Every nonempty complete factor volume has a nonzero physical excited sector, for example the centered selected Wilson from AM1; sufficiently large cutoffs contain approximations to two independent physical vectors. The actual full finite rotor Schrödinger ground is unique and positive and therefore gauge invariant, so the physical ground is also the actual full ground. Restoring alpha/8 multiplies the gap by that factor; physical time remains t/hbar with the original energy Hamiltonian.

## Evidence, attribution and scope

Run `python research/round29/reverse/am2/check.py --output /absolute/new-directory`. Exact arithmetic reconstructs the two coefficient contributions, exponential enclosure, self-map, derivative and shifted-resolvent bounds. A four-factor 16-state algebra fixture has nonzero seventh/eighth nested commutators and zero ninth, discriminating a copied three-site termination. Two-state characteristic-polynomial controls distinguish actual scalar ground centering and retained diagonal energy. These fixtures test algebra; the uniform infinite-dimensional statement follows from the proof and cutoff passage above, not a finite simulation. Normal/optimized outputs agree and all inputs/code/report/results are frozen by hashes.

The result is an alternative quantitative **finite-volume** theorem for |tau|<=10^-8, with a deliberately conservative constant. It does not establish a sharp threshold, a new universal axiom, a continuum mass, a numerical HTW boundary constant, or a unique infinite-volume limiting state at all these numerical couplings. Those obligations require their own estimates.
