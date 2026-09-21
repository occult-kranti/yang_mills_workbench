# Y1 reverse — a finite spatial collar retains the canonical endpoint signal

Independent reverse reconstruction before reading forward Y1. The model is exactly canonical M/N/U at fixed spacing and physical energy/time units. The new regulator is the number of complete-reference-factor layers. It does not renormalize q, eta, tau_q, the Hamiltonian coefficients, or the original physical clock. Newton's reconstruction starts from the required endpoint error; Tesla's full-channel check includes the entire boundary tail and reference-strip enlargement.

## Construct the actual finite approximation

Keep U1's eight free singleton factors F_0 supporting W. A reference factor is either one free link or an entire ten-link selected strip. For any finite factor set F, let E(F) be every link of those factors and I(F) the omitted plaquettes meeting at least one link in E(F). Recursively define, for d>=1,

    J_d=I(F_(d-1)),
    F_d=F_(d-1) union {complete factors owning links of faces in J_d}.

Each step is finite: each factor owns at most ten links, each link lies on at most four elementary faces, and each face meets at most four complete factors. Faces are counted once. The exact ownership is M1's partition: all z-links, odd-row y-links and x-links with x-tail residue three are free; all other links belong to their complete selected xy strip. No strip is cut at the spatial boundary. This recursive rule is independent of q.

Define

    V_(q,d)=-alpha tau_q sum_(f in J_d) q^|anchor(f)|_1 x_f/24,
    H_(q,d)=H_0+V_(q,d),
    beta_(q,d)^t(W)=exp(-itH_(q,d)/hbar)W exp(itH_(q,d)/hbar).

All selected reference strips inside F_d remain complete and all exterior reference factors remain unchanged. V_(q,d) is bounded self-adjoint, with norm at most alpha eta/8, because it is a subset of the original positive coefficient ledger. Thus D(H_(q,d))=D(H_0). The perturbation is supported on F_d and the reference Hamiltonian factorizes over it and its complement, so the observable evolution is exactly a finite **spatial-factor** evolution extended by identity. Each factor's full Haar Hilbert space and unbounded reference Hamiltonian are retained. This is not a finite-spin matrix.

Each retained plaquette multiplication and complete reference factor is gauge invariant on the full link representation. No boundary Gauss constraint is silently removed. The physical invariant sector is reducing, and the following full-operator estimates also hold on it.

The executed exact geometry gives:

| Depth d | Complete factors | Physical links | Retained omitted faces | Whole strips |
|---|---:|---:|---:|---:|
| 0 | 8 | 8 | 0 | 0 |
| 1 | 35 | 98 | 19 | 7 |
| 2 | 135 | 297 | 125 | 18 |
| 3 | 308 | 623 | 327 | 35 |

All layers contain the actual U1 resonant yz plaquette anchored at (3,1,0). At depth one, completing the seven strips adds 56 links absent from the union of displayed retained-face links and original W links. The next layer includes the origin xz plaquette via a strip already reached by the xy plaquette at (2,1,0). These are actual geometry checks of eligible connected supports; they are not claims that every eligible nested commutator is nonzero.

## Exact matching of words and a complete operator tail

For fixed q and finite physical t, use the interaction picture with the unchanged H_0. Its bounded full and restricted perturbations have strongly continuous interaction-picture generators. The bounded-perturbation Dyson commutator expansion is valid on the full Hilbert space; a global norm majorant first justifies each expansion. Every term uses only bounded operators and vectorwise integrals, so no arbitrary local operator is differentiated through the unbounded reference generator.

In a nonzero nested word read from its innermost commutator with W, each new face must meet the accumulated union of complete factors. By induction, after k such faces the support lies in F_k. Hence every possibly nonzero word of length n<=d uses only faces in J_d. The restricted and full expansions agree **term by term** through order d, including exact q-dependent coefficients and time integrals. They also agree at every order on all words whose faces are retained. Subtracting leaves only full words with at least one face outside J_d, necessarily of order n>=d+1.

U2's complete-factor count applies to those words: after k attachments at most 8+3k factors are present, with at most 40 incident faces per factor. With s=alpha tau_q |t|/hbar and x=10s, the complete order-n norm sum is bounded by

    x^n (8/3)_n/n! <= x^n (3)_n/n!
                    = ((n+1)(n+2)/2)x^n.

Repeated faces, incoming faces, all reference-factor enlargement, all time orders and all exterior channels remain in this bound. No extra factor of two is required after subtraction: the identical retained words cancel exactly, so the difference is a subset of the full word sum. Bounding the two complete tails separately would give a valid but weaker factor-two bound.

For 0<=x<1 this proves

    ||beta_q^t(W)-beta_(q,d)^t(W)|| <= B_d(x),
    B_d(x)=sum_(n=d+1)^infinity ((n+1)(n+2)/2)x^n
      = x^(d+1) [(d+2)(d+3)-2(d+1)(d+3)x+(d+1)(d+2)x^2]
        /[2(1-x)^3].                                  (Y1.R1)

The complete rational tail, not a finite-order truncation, bounds the error. One may first compare finite face sums and then pass to the norm-convergent perturbation at fixed q,t. The connected majorant is summable in the stated regime and bounds the same limit. Reference conjugation is an isometry, so the interaction-picture estimate gives exactly the displayed physical Heisenberg estimate.

## Uniform on the original endpoint window

For epsilon=1-q, U2 gives

    tau_q/epsilon^3=3eta(1+q)^2(1+q^2)/P(q)<=3eta/2,
    P(q)=2+5q+5q^2+6q^3+3q^4.

Keep T_q=C(hbar/alpha)epsilon^-3 and z=Ceta in (0,10^-6]. Then for every q in (0,1) and |t|<=T_q, x<=15z<1. The power series in (Y1.R1) has nonnegative coefficients, so

    sup_(|t|<=T_q)||beta_q^t(W)-beta_(q,d)^t(W)||<=B_d(15z).   (Y1.R2)

At z=10^-6, depth two gives B_2(15z)<3.4*10^-14. This is a deterministic all-tail operator bound uniform in q and physical time on the declared growing window. It does not estimate the norm of the full propagator on arbitrary states. No q=1 Hamiltonian is substituted and no physical time is rescaled to reduce the bound.

## Regional stationary state and correct connected comparison

Let Psi_(q,d) be the unique ground of H_(q,d), with projector P_(q,d). The same isolated-vacuum argument as M/N applies: the reference complement costs at least alpha/8, the perturbation norm is at most alpha eta/8, and its reference mean is zero because every retained omitted face has a free Haar link. Thus the complement of the reference vacuum has quadratic form at least gbar=alpha(1-eta)/8, there is a unique ground e_(q,d)<=0, and

    d_(q,d):=||P_(q,d)-P_0||
       <=||V_(q,d)Omega||/gbar
       <=tau_q N_d/[3(1-eta)], N_d=|J_d|.              (Y1.R3)

The final estimate uses only the triangle bound ||V_(q,d)Omega||<=alpha tau_q N_d/24; it does not require a new assertion about all restricted covariance cancellations. It is deliberately conservative. Since d and N_d are fixed before q tends to one, this regional state bound is O(epsilon^3). The full admitted state error d_q<=sigma_q/gbar is O(epsilon^(3/2)). The regional ground factorizes with the unchanged reference vacuum outside F_d. Uniqueness and gauge invariance give its invariant physical ground, as in the inherited argument.

Define each connected correlation in its **own** stationary ground,

    C_(q,d)(t)=omega_(q,d)(W beta_(q,d)^t(W))-omega_(q,d)(W)^2.

Using trace distance between pure projectors, the two raw expectations differ from state replacement by at most 2(d_q+d_(q,d)); the difference of squared means costs at most 4(d_q+d_(q,d)). Inserting the operator error separately proves

    sup_(|t|<=T_q)|C_q(t)-C_(q,d)(t)|
       <= B_d(15z)+6(d_q+d_(q,d)).                    (Y1.R4)

Both disconnected terms are retained. Ground-energy shifts cancel in Heisenberg conjugation; dropping one from an uncentered propagator would be a different expression. Equations (Y1.R3)–(Y1.R4) are state comparisons, not an assumption that a full interacting ground restricts to the regional ground.

Let L(z)=z/84-(44/9)(80z/7)^2/(1-80z/7)^5 be U2's accepted lower endpoint margin, L(z)>z/168. Since both state terms vanish,

    liminf_(q->1) |C_(q,d)(T_q)-C_0(T_q)| >= L(z)-B_d(15z).   (Y1.R5)

For d=2 this remains positive throughout the inherited z interval: B_2(15z)/z increases with z and the exact cap arithmetic bounds it below 1/10^6. The region is fixed independently of q, with the original full local Hilbert spaces. It retains an endpoint signal with certified error; it does not supply an exact limiting trajectory.

For a fully finite example, eta=1/2, z=10^-6 and q=1-10^-8 give N_2=125. Using exact rational arithmetic and an enclosing square root for sigma_q/gbar, the checker obtains d_q<=1.09110*10^-13 and d_(q,2)<=4.76191*10^-23. The stationary comparison error is below 6.88405*10^-13. Combining it with U2's actual finite-q bound proves the regional endpoint difference is greater than z/101 (approximately 9.90099*10^-9); its sharper certified lower value is approximately 1.12648*10^-8. Decimal values here display enclosures derived from exact fractions, not simulated observations.

## Remaining obligations

The finite spatial approximation is an actual self-adjoint Hamiltonian with finite factor support and a uniform observable error. It still acts on the infinite-dimensional space of 297 physical Haar links at depth two. Its ground, transition amplitudes and eight-setting readout have not been numerically computed or implemented. A finite Peter–Weyl truncation would need its own retained-input class, full residual and same-clock certificate; no finite T-graph gap or Ritz constant transfers here.

The spatial recursion, tail and ground comparison are modern model-specific applications of inherited connected estimates. W's rank on its observed factors is not a finite-dimensional state space for the region, and a finite support control is not a physical continuum limit. The next missing useful step is a rigorously matched evaluation or further reduction of these full local dynamics, with all errors carried to the original endpoint. Homogeneous gap, calibration, continuum construction and scientific priority remain open.
