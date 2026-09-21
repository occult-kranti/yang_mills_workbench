# U1 forward — actual free-link resonance

Single-author construction with correlated reverse reconstruction and skeptical self-review. The Newton and Tesla skills guide the method; their historical claims are not premises. This report proves an actual full-model matrix element and a first-order response. The endpoint target remains **limited** until a bulk remainder is controlled.

## Model, state and observable

Use exactly the frozen M1/M2/N1 canonical summable model. Write b(q)=P(q)/[24(1-q)^3(1+q)^2(1+q²)], P=2+5q+5q²+6q³+3q⁴, tau=eta/[8b(q)], and V_q=−alpha tau Σ_omitted q^|anchor| x_f/24. The full self-adjoint operator H_q=H_0+V_q has D(H_q)=D(H_0). Its unique invariant ground Psi_q and projector obey d_q≤sigma_q/gbar, sigma_q²=alpha² tau² b(q²)/96, gbar=alpha(1−eta)/8. No T-model gap is imported. All physical scales in the contract stay fixed.

Let O=(3,1,0), D=(3,2,1). Choose paths

* X: O → (3,2,0) → D;
* Y: O → (3,1,1) → D;
* Z: O → (4,1,0) → (4,2,0) → (4,2,1) → D.

They share endpoints but no links. All eight links are free singleton reference factors: z-links are free, each y-tail has odd y=1, and each x-tail has x=3 modulo 4. Haar variables along disjoint paths induce independent Haar holonomies X,Y,Z. In the local Hilbert space set phi_X=Tr(XZ⁻¹), phi_Y=Tr(YZ⁻¹). The characters are real, orthonormal, and orthogonal to the constant Omega_F. Each traverses six links once in spin 1/2, so its electric energy is E=6(3alpha/4)=9alpha/2. Tensoring with Omega outside preserves this exact eigenvalue of H_0, including all strip factors.

Set psi+=(phi_X+phi_Y)/sqrt(2), W_F=|psi+><Omega_F|+|Omega_F><psi+|, and W=W_F tensor I_out. Then W*=W, ||W||=1, omega_0(W)=0, omega_0(W²)=1. Closed-loop characters and the constant are invariant under every endpoint gauge action, hence their rank operators commute with that action. Thus W belongs to the inherited bounded physical local algebra. It is a rank-two operator on eight links extended by identity, **not** multiplication by a Wilson loop and not a finite truncation of H_q. W is independent of q. Actual interacting variance tends to 1; more explicitly it is ≥1−2d_q−4d_q², positive for q sufficiently near 1.

## Exact resonance and its selection rule

Let f0 be the yz plaquette anchored at O. Its weight is q⁴/24 and x_f0=Tr(XY⁻¹)/2. SU(2) character convolution gives

    ∫dZ Tr(YZ⁻¹) Tr(XZ⁻¹) = Tr(YX⁻¹)/2,
    <phi_Y,x_f0 phi_X> = 1/4.

Alternatively unit quaternions give phi_X=2 x·z, phi_Y=2 y·z, x_f0=x·y, and E[x_i x_j]=delta_ij/4; the same integral is 4*4/4³=1/4. Both diagonal entries vanish.

For any other face, central sign flips on free links show the off-diagonal matrix element is zero: phi_X phi_Y has odd parity on exactly the four X/Y links, and even parity on Z. A plaquette must contain all four odd links, which uniquely identifies f0. Every omitted face contains a free link (z for xz/yz; odd-row y or residue-three x for omitted xy). Therefore diagonal elements in phi_X and phi_Y, as well as the vacuum mean, vanish for every omitted face. Absolute norm convergence of V permits termwise integration. Consequently in the **full system**

    <psi+, V_q psi+> = <phi_Y,V_q phi_X> = −alpha tau_q q⁴/96.

This does not assert invariance of the two-state subspace. Couplings to other spins and other factors remain.

## Actual first-order response

Use U_j(t)=exp(−itH_j/hbar), Z_q(t)=U_0(−t)U_q(t), V_I(r)=U_0(−r)V_qU_0(r). Bounded V on the common domain gives Z′=−i V_I Z/hbar in the strong sense on all vectors. Thus ZWZ*=W−(i/hbar)∫[V_I(r),W]dr plus higher terms. No derivative of an arbitrary bounded observable through H_0 is assumed.

Since W Omega=psi+, W psi+=Omega, and both psi components have energy E,

    <psi+,[V_I(r),W]Omega>
      = <psi+,V_q psi+> − <Omega,V_q Omega>
      = −alpha tau_q q⁴/96.

Also e^(iEt/hbar) omega_0(W beta_q^t(W))=<psi+,ZWZ*Omega>. For C_q(t)=omega_q(W beta_q^t(W))−omega_q(W)², N1's stationary state replacement costs at most 6d_q uniformly in t. The reference autocorrelation is C_0(t)=e^(−iEt/hbar). With s_q=alpha tau_q t/hbar the leading demodulated difference is +i s_q q⁴/96. Demodulation is a unit-modulus display factor and changes neither time nor |C_q−C_0|.

At t=C(hbar/alpha)(1−q)^−3, tau_q/(1−q)^3→8eta/7, so the leading term tends to i C eta/84. U1 supplies no uniform bound on the higher terms. A derivative at zero coupling or a two-by-two sine law cannot by itself prove an endpoint lower bound.

## Checks, limits and next premise

The executable verifies the exact graph, unique plaquette parity and degree-two Haar integrals with a finite S³ quadrature exact for the polynomials used. It is algebraic integration, not a simulation or cutoff of the infinite Hamiltonian. The reverse calculation contracts Haar moments directly. Both are same-author checks. Normalized traces would give state norm²=1/4 and invalidate the chosen normalization; removing f0 removes the resonant coefficient. Scalar identity has zero connected variance.

The next missing premise is a full-system bound on all connected higher commutators, including every complete reference factor generated by free evolution. Scientific priority is unverified. No homogeneous limit, calibration or four-dimensional continuum construction is obtained. Source reading and hypotheses are pinned in the contract; historical method snapshots include passage-level references.
