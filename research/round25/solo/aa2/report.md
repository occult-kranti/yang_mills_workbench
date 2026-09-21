# AA2: an exact reachable component and a finite-q certificate

AA2 was selected and frozen after AA1's exterior-resonance objection. A single agent performed all passes. This is correlated mathematical self-review, not external peer review. The result below concerns the canonical summable model and the original rank observable W, not homogeneous Yang–Mills or Wilson multiplication alone.

## 1. The exterior selection rule

Let L be the sixteen-dimensional physical cube shell from AA1, tensored with the unchanged reference ground on every outside factor. In any complete-factor collar k>=1, L lies in the whole reference eigenspace E=9/2. This inclusion does not assert that L exhausts that eigenspace. The reference K=H_0/alpha is a sum of shifted nonnegative complete-strip Hamiltonians and free Casimirs. Each actual strip has its inherited full-link gap >=1/8 and a unique ground invariant under every vertex gauge transformation acting on that strip's links.

Every omitted plaquette falls into one of three cases:

1. **Inside the cube.** Its action leaves all outside factors in their ground. Projection onto reference energy E therefore gives exactly the complete physical cube compression computed in AA1.
2. **Disjoint from cube edges.** It acts only outside. Its reference mean is zero by an unused Haar link, as in A2/Y2. It therefore creates an outside excitation orthogonal to the outside ground, with positive energy >=1/8. The unchanged cube energy cannot cancel this cost. Sharing a vertex alone changes no factor support.
3. **Meeting cube edges but not contained in the cube.** A unit face then meets exactly one cube edge. There are twenty such faces in the actual positive orthant; both incidence enumeration and a separate candidate-box search give the same list. The edge opposite the shared edge is free: it has the same direction and the same relevant x=3 or y=1 free coordinate, or is a z edge. The remaining sides lie outside the cube in two distinct reference factors. The complete owner list is in output/results.json.

For case 3, if the shared edge is occupied by spin 1/2, multiplication by its fundamental matrix fuses it to spin 0 or 1. The least cube energy change is -3/4, canceled by +3/4 on the opposite, initially constant, free edge. If the shared edge was unoccupied, its change is +3/4 instead. A remaining free side costs +3/4. A remaining strip side produces a vector orthogonal to that strip's ground: the matrix coefficient of one open edge transforms nontrivially under an endpoint SU(2) action, whereas the ground is invariant. Its ground matrix element is consequently zero, including every matrix index. The strip spectral gap then bounds that factor's entire excitation by >=1/8. Distinct ownership of the two sides is essential; no cancellation within one strip is silently assumed.

These tensor-factor bounds remain valid for the finite sums of matrix-index contractions produced by the trace. Spectral projections of the reference factors commute; the face image lies in their specified tensor spectral subspaces, not merely above the bound in expectation. Thus the least case-3 energy increment is >=1/4. The spin-1 fusion branch costs a further 2. At the z=0 boundary the nonexistent negative-z faces are absent; the checker uses this actual boundary.

It follows that P_E A_(q,k) L is contained in L for every k>=1, with A_(q,k)=-sum_(f in O_k) q^|anchor(f)| x_f/24. All statements concern the actual selected-strip operators; no strip spectral level was substituted by a free rotor. The bounded self-adjoint pinched operator Abar_(q,k)=sum_lambda P_lambda A_(q,k) P_lambda therefore leaves L and its orthogonal complement invariant. This is a **reducing component reached by the observable**, not an enumeration of the entire regional energy shell.

## 2. Participating frequencies, not a global excited gap

On an internal face meeting r occupied cube edges, let m of those edges fuse to spin 1. Its energy change is

    Delta E = 3 - (3/2) r + 2m.

Every nonzero value has absolute value at least 1/2. External touching faces have increment >=1/4; disjoint faces have increment >=1/8. Therefore the spectral measure of (I-P_E) A_(q,k) P_L avoids (-1/8,1/8) about E. The vacuum source has the same conservative lower bound from the reference gap. This does not bound the distance of every regional excited eigenvalue from E; eigenvalues unreachable in one application to L do not enter this primitive.

For tau=tau_q and M_k=N_k/24, the Y2 primitive identity now gives the evaluated operator-on-input-subspace bound

    sup_|s|<=S ||R_tau(s) P_L|| <= 16 tau M_k.

The averaged orbit and its Abar derivative stay in L by the preceding reducing proof. The bounded strong-generator integration by parts of Y2 therefore yields

    ||(Z_tau(s)-exp(-i s Abar_(q,k))) P_L||
      <= b_k :=16 tau M_k(1+2 S M_k),  S=3z/2.

The same bound holds on the vacuum input. For the adjoint vacuum use ||Z*Omega-Omega||=||Z Omega-Omega|| since Abar Omega=0. Domains, gauge reduction, finite-region compact resolvent and vectorwise strong evolution are inherited as explicitly proved in Y2; no global norm averaging theorem is invoked.

## 3. The actual endpoint is evaluated

For each cube flip, let r_f be its anchor sum, either 4 or 5. Let Q(q) be the symmetric sixteen-by-sixteen matrix with entry q^r_f on that flip and zero otherwise. It has row norm <=6, and Abar_(q,k)|L=-Q(q)/96. Its action is the same in every collar k>=1. In particular Q(1)=A from AA1. Applying the Y2 spatial transfer to these identical finite-region scalar limits proves that its previously implicit full scalar is exactly

    F_infinity(z)=1/3 + (1/2)cos(2 theta) + (1/6)cos(2 sqrt(3) theta)
      + i[(1/4)sin(2 theta)+(1/(4 sqrt(3)))sin(2 sqrt(3) theta)],
    theta=z/84, 0<z<=1e-6.

Here F_infinity=lim_(q->1) exp(i E T_q/hbar) C_q(T_q), E=9alpha/2, for the actual full stationary connected correlation. The original physical clock is T_q=(z/eta)(hbar/alpha)(1-q)^-3. The identity does not construct a global q=1 Hamiltonian. The two frequencies in the scalar are spectral splittings in the dimensionless endpoint coordinate; they are not Earth resonances, a replacement physical clock, or a measured mass.

The full limit now satisfies |F_infinity-1-i z/84|<=z^2/3528. This replaces the prior unevaluated-block disk for this observable. Both the AA1 sixteen-state spectral weights and the multiple frequencies survive; a two-state fit still fails.

## 4. Finite q: a usable mathematical enclosure

Keep the q profile inside Q(q), instead of replacing every coefficient of the regional Hamiltonian by one. Let

    p(q)=2+5q+5q^2+6q^3+3q^4,
    b(q)=p(q)/[24(1-q)^3(1+q)^2(1+q^2)],
    tau_q=eta/[8 b(q)],
    s_q=(z/eta) tau_q/(1-q)^3 <=3z/2,
    dhat_q=tau_q sqrt(b(q^2)/96) / [(1-eta)/8].

The original W still acts on eight free links and extends by identity; it was not replaced by a globally rank-two observable. Y2's ordered reference-state matrix element and the two vector bounds give error <=2b_k relative to <psi,exp(i s_q Q(q)/96)psi>. Changing the full stationary state to the reference state costs <=6dhat_q, including the connected mean. Comparing full and regional reference-state dynamics costs <=D_k(15z), directly by Y1. No regional stationary state is introduced in this route, so the state cost is six rather than twelve:

    |exp(i E T_q/hbar) C_q(T_q) - <psi,exp(i s_q Q(q)/96)psi>|
      <=6dhat_q + D_k(15z) +32 tau_q M_k(1+3z M_k).       (AA2.1)

This is continuous in the admitted q,eta,z ranges, not a grid interpolation claim. For degree n scalar Taylor evaluation, the exact rational partial sum has arithmetic error at most (s_q ||Q(q)||/96)^(n+1)/(n+1)! by the unitary integral remainder. The producer uses n=8 and the rigorous symmetric row norm. Square roots in dhat are rounded upward with integer arithmetic. Exact rational scalar centers and every separate error are saved. Floating display values are illustrative: near one, use Re(F)-1 to avoid cancellation; the rational center is authoritative.

At eta=1/2, z=1e-6, q=1-1e-12 and collar depth three, N_3=332 and the certified errors are bounded by:

| term | upper bound |
|---|---:|
| full stationary-state replacement | 6.547e-19 |
| entire omitted spatial tail | 5.455e-19 |
| both averaging errors | 2.530e-34 |
| degree-eight scalar remainder | 1.334e-70 |
| combined radius about exact rational center | 1.201e-18 |

The scalar center has Im approximately 1.1904761904715985e-8 and Re-1 approximately -2.834467120157e-16. The physical time is 2e30 hbar/alpha: this is a precise mathematical enclosure with an impractical clock, not a demonstrated experiment. Comparing the finite-q matrix scalar with the exact limiting formula adds at most s_q(1-q^5)/16+|s_q-8z/7|/16, below 3.674e-19 at this example. State, spatial, averaging, coefficient comparison and arithmetic errors have distinct meanings.

## 5. Skeptical disposition

The strongest objections were exterior equal-energy channels, possible two-edge cancellation inside one strip, unaveraged leakage, incorrect state/adjoint order, and rounding a nearly unit scalar. The owner table and charge proof address the first two. Instantaneous invariance is explicitly false: an exterior face excites higher-energy states, and Y2 already measured nonzero single-face leakage. Only the averaged component reduces. The Y2 ordered identity and two separately bounded inputs fix the third/fourth issues; exact rational centers fix arithmetic interpretation. Larger whole energy shells and their degeneracies remain unenumerated because they are unnecessary for this particular input after the reducing proof.

The verdict is accepted within this canonical observable/endpoint scope, under same-author self-review. It completes the next planned goal AA by a proved reachable-component workaround to whole-block assembly. Independent mathematical review remains desirable before treating this as established literature. Scientific priority is unverified. No homogeneous inverse, volume-uniform stability, physical scale calibration, nontrivial continuum limit or mass-gap solution follows. AB, AC and the new observable/scale bridge goal remain planned only.
