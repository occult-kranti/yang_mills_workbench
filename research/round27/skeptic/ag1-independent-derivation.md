# AG1 independent derivation before producer exchange

This concerns the frozen selected-source correction G+A in the homogeneous complete-block model. It does not identify that selected source with all cubic words or the complete original transformed Hamiltonian. The only new execution is this third loop.

## Strong support norm and actual cubic size

For rho=9/4, the inherited complete translated-word argument extends to

    ||R||_rho, ||S||_rho <= rho^4 F(zeta) r*,
    F(zeta)=(4-zeta)/(1-zeta)^2,
    zeta=26 M rho^3 T, T=3,
    ||A||_rho <=4 rho^4 r*.

Here r*=sup_b||A_b|| is the actual source supremum, bounded above by (4/3)(7/12)^(3/2)|tau|^3. The exact rational simplification r*<=(2/3)|tau|^3 is valid because the squared coefficients compare directly. At M=1/1000, zeta=28431/32000<1. Every complete support, repeated word, root placement and twelve interior crossing stars remains. The root's three-star count is a separate boundary case. These are interaction-family bounds, not an extensive-operator bound uniform in volume.

## Every commutator pays the support loss

For 2<=a<b, assigning [Phi_X,Psi_Y] to X union Y and using X intersect Y nonempty gives

    ||[Phi,Psi]||_a <=(2/a)(||Phi||_(a,1)||Psi||_a
                                      +||Phi||_a||Psi||_(a,1)),

where ||Phi||_(a,1) is the same rooted sum with factor |X|. Both ways that the root can enter the union are retained. The inequality n(a/b)^n<=1/[e log(b/a)] controls each support moment. Hence

    ||[Phi,Psi]||_a <=2||Phi||_b||Psi||_b/[e log(b/a)].

Set delta=1/10. Since exp(delta)<=1/(1-delta)=10/9<9/8=rho/2, an n-step chain a_j=2 exp(j delta/n) stays below rho. Applying the preceding bound n times and using n!>=(n/e)^n gives

    ||ad_S^n B||_2/n! <=x^n ||B||_rho,
    x=2||S||_rho/delta.

This controls the entire nested series, with a distinct weight loss at every commutator. Finiteness of the weight-2 norm alone would not give its first support moment: one n-site term of norm 2^-n has weight-2 norm one but first moment n.

## Exact transformation and domain

In a finite containing cuboid, S is a finite sum of actual bounded AE2 skew-adjoint filters, each preserving D(G) with bounded commutator. Their sum is bounded on the graph domain, so exp(plus or minus S) preserves that domain. Integrating the bounded commutator along the conjugation orbit, followed by an ordinary bounded-operator series, yields

    exp(S)(G+A)exp(-S)=G+R+N,
    N=sum_(k>=1) ad_S^k(kA+R)/(k+1)!,
    [S,G]=-A+R.

It is unnecessary and incorrect to posit an operator-norm series for unbounded G itself. The entire nonlinear interaction remainder obeys

    ||N||_2 <= [x/(1-x)] (||A||_rho+||R||_rho/2), x<1.

The independent rational cap bounds give x<2.493e-7 and ||N||_2<0.000825 r* on M<=1/1000. These endpoint estimates extend throughout the interval because the positive upper functions increase with M and r*. They are uniform over containing finite volumes, without constructing a global infinite-volume unitary.

For any additional remainder E with a separately supplied finite ||E||_rho<=e*, its transported interaction satisfies

    ||exp(ad_S)E||_2 <=e*/(1-x).

The actual E has not been computed here. Omitting it would turn a selected-source theorem into an unjustified statement about the original Hamiltonian.

## Scalar, diagonal and source bookkeeping

For each generated nonempty support X, let P_X be the product reference-vacuum projection and Q_X=I-P_X. For its self-adjoint term B_X define

    c_X=<Omega_X,B_X Omega_X>,
    A'_X=P_X B_X Q_X+Q_X B_X P_X,
    D'_X=Q_X(B_X-c_X I)Q_X.

Then B_X=c_X I+A'_X+D'_X exactly, with |c_X|<=||B_X||, ||A'_X||<=||B_X|| and ||D'_X||<=2||B_X||. Each scalar keeps its assigned support in the interaction budget; the finite sum of scalar values may be extensive. This reference scalar is not the exact interacting ground energy. No later-diagonal filtering theorem follows solely from this split.

## Narrow interval: a selected-source norm contraction

At M<=1/10000, split R into the n=0 free-onsite filter and all n>=1 D-interaction terms. The actual source is |w><Omega| plus adjoint with excitation spectrum of the local free onsite Hamiltonian at least one. Its T=3 triangular multiplier has magnitude at most 4/9 on that spectrum. Therefore the n=0 family satisfies

    ||R_free||_2 <=(4/9)||A||_2.

The complete positive n>=1 residual tail from AE2 is bounded by

    t(M) r*,
    t(M)=(16/3)[F(624 M)-4],

because the exact integrated coefficient is 32(4+3n)(624M)^n/[(n+1)(n+2)] and the denominator is at least six for n>=1. At M=1/10000, t(M)<2.555511, so the looser total residual upper budget is below31 r*. A statement of budget reduction alone would not be a norm contraction.

For the actual declared input interaction family, every nonzero term has four sites and contributes 16||A_b|| at a root in that support. Consequently ||A||_2>=16r* for any nonempty finite family. This elementary lower denominator does not require a root lying in four different stars. The small one-star box has actual norm16r*, and a sufficiently large homogeneous box has64r*; the checker distinguishes them.

The source projection has norm cost at most one on each self-adjoint support term. Combining the free piece, full positive tail and nonlinear remainder gives for the selected updated off-diagonal source

    ||A_new||_2 <= [4/9 + (t(M)+n(M))/16] ||A||_2,

where n(M)r* bounds N. The independent conservative cap at M=1/10000 is below0.605 (and hence below0.61). This is a genuine one-step contraction for the selected-source update, using r* as the actual supremum. If r* were only a freely chosen loose upper budget, the lower-denominator step would be invalid. It does not control an omitted E, establish a next changed-diagonal inverse, or prove all-stage convergence.

At tau=0 the source and correction are exactly zero and no ratio is divided by r*. Both nonzero signs use the same absolute upper bounds without asserting equal spectra.

## Executed verification scope

`ag1_independent.py` executes 60 exact checks. It verifies both cap calculations, full geometric tails, boundary counts, small-volume norm denominators and missing-weight-moment examples. A three-by-three rational formal-power-series diagnostic independently expands exp(tS)(G+tA)exp(-tS) through order nine, rejects the wrong G-only coefficients, reconstructs all scalar/diagonal/source pieces and detects nontrivial E transport. These finite matrices check algebra; they do not replace the inherited infinite-dimensional source and domain proofs. No current producer AG1 report or checker was read before completing this derivation and execution.
