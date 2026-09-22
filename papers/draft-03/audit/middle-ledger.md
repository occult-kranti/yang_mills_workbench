# Rounds 13–22 contribution ledger

All 62 historical entries are accounted for: 4 named studies and 58 numbered loops. Replays, reviews and repairs are not extra loops. Double-star means original to this workbench, with scientific priority unverified.

This pass inspected the named reports and independently checked 14 exact arithmetic identities. It did not rerun every accepted executable or execute a new research loop. The JSON ledger contains source hashes, exact historical statuses, source mapping and scratch audit corrections.

| ID | Group | Historical status | Manuscript location |
|---|---|---|---|
| R13-locality | dynamics | historical study — scope below | sec:middle-dynamics |
| R13-stability | homogeneous | historical study — scope below | sec:middle-rotation |
| R13-moments | moments | historical study — scope below | sec:middle-moments |
| R13-response | moments | historical study — scope below | sec:middle-moments |
| R14-loop1 | moments | accepted within declared finite-model scope | sec:middle-moments |
| R14-loop2 | moments | accepted within declared finite-model scope | sec:middle-moments |
| R15-A1 | moments | accepted correctly diagnosed insufficiency | sec:middle-moments |
| R15-A2 | moments | accepted exact complete positive cover | sec:middle-moments |
| R15-B1 | gluing | accepted exact finite cube graph and Haar identities | sec:middle-gluing |
| R15-B2 | gluing | accepted exact finite cube integral and rejected factorization | sec:middle-gluing |
| R15-C1 | finite-gap | accepted finite-graph side theorem and retained original source gap | sec:middle-finite-gap |
| R15-C2 | finite-gap | accepted finite physical cube variational improvement | sec:middle-finite-gap |
| R16-loop1 | gluing | accepted | sec:middle-gluing |
| R16-loop2 | gluing | accepted | sec:middle-gluing |
| R17-a1 | homogeneous | accepted | sec:middle-rotation |
| R17-a2 | strips | accepted | sec:middle-strips |
| R17-b1 | finite-gap | accepted | sec:middle-finite-gap |
| R17-b2 | finite-gap | accepted | sec:middle-finite-gap |
| R17-c1 | conditional | accepted | sec:middle-conditional |
| R17-c2 | conditional | accepted | sec:middle-conditional |
| R18-a1 | strips | accepted | sec:middle-strips |
| R18-a2 | strips | accepted | sec:middle-strips |
| R18-b1 | finite-gap | accepted | sec:middle-finite-gap |
| R18-b2 | finite-gap | accepted | sec:middle-finite-gap |
| R18-c1 | conditional | accepted | sec:middle-conditional |
| R18-c2 | conditional | accepted | sec:middle-conditional |
| R19-a1 | strips | accepted | sec:middle-strips |
| R19-a2 | strips | accepted | sec:middle-strips |
| R19-b1 | finite-gap | accepted | sec:middle-finite-gap |
| R19-b2 | finite-gap | accepted | sec:middle-finite-gap |
| R19-c1 | conditional | accepted | sec:middle-conditional |
| R19-c2 | conditional | accepted | sec:middle-conditional |
| R20-d1 | strips | accepted | sec:middle-strips |
| R20-d2 | strips | accepted | sec:middle-strips |
| R20-e1 | strips | accepted | sec:middle-strips |
| R20-e2 | strips | accepted | sec:middle-strips |
| R20-f1 | clock | accepted | sec:middle-clock |
| R20-f2 | clock | accepted | sec:middle-clock |
| R20-g1 | dynamics | accepted | sec:middle-dynamics |
| R20-g2 | gns | accepted | sec:middle-gns |
| R20-h1 | profile | accepted | sec:middle-profile |
| R20-h2 | profile | accepted | sec:middle-profile |
| R21-i1 | homogeneous | limited | sec:middle-rotation |
| R21-i2 | homogeneous | limited | sec:middle-rotation |
| R21-j1 | gns | accepted | sec:middle-gns |
| R21-j2 | gns | accepted | sec:middle-gns |
| R21-k1 | clock | accepted | sec:middle-clock |
| R21-k2 | clock | accepted | sec:middle-clock |
| R21-l1 | clock | accepted | sec:middle-clock |
| R21-l2 | clock | accepted | sec:middle-clock |
| R21-m1 | profile | accepted | sec:middle-profile |
| R21-m2 | windows | accepted | sec:middle-windows |
| R22-n1 | windows | accepted | sec:middle-windows |
| R22-n2 | windows | accepted | sec:middle-windows |
| R22-o1 | homogeneous | limited | sec:middle-rotation |
| R22-o2 | inverse | limited | sec:middle-inverse |
| R22-p1 | tree | accepted | sec:middle-tree |
| R22-p2 | tree | accepted | sec:middle-tree |
| R22-q1 | memory | accepted | sec:middle-memory |
| R22-q2 | memory | accepted | sec:middle-memory |
| R22-r1 | inverse | accepted | sec:middle-inverse |
| R22-r2 | inverse | accepted | sec:middle-inverse |

## R13-locality — Local finite-time volume limit

- Equation: eq:middle-lr; ||difference|| <= ||A|| min(2,|X|/4 sum_{k>=R}(8qJ)^k/k!).
- Assumptions: Common full-link generators and unbounded onsite terms; bounded interactions with declared uniform envelope or summable tail; fixed spacing; correct complete support and physical time/hbar.
- Application: Local finite-time boundary comparison.
- Change: Removed the extensive global-volume factor for local dynamics.
- Limitation: Fixed spacing and common envelope; no vacuum comparison or continuum-uniform velocity.
- Next: Sharper physical scaling estimate and an appropriate observable algebra.
- Derivation: `sec:middle-dynamics` in `sections/middle.tex`.
- Sources: `research/round13/locality/locality.md`, `research/round13/README.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R13-stability — Qualitative homogeneous stability

- Equation: epsilon <= (4/3) binom(d,2) lambda_max/alpha; gap >= 3alpha/8 qualitatively.
- Assumptions: Full unreduced SU(2) links grouped by d outgoing directions; onsite electric gap 3alpha/4; bounded plaquette range S={0,e1,...,ed}; fixed spacing and alpha>0; source smallness constants existential; explicit boundary padding and gauge restriction.
- Application: Apply a known product-vacuum theorem to full rotor links.
- Change: Matched infinite-dimensional sites, boundaries and gauge-invariant uniqueness.
- Limitation: Numerical smallness constants unevaluated; weak bare coupling exits this regime.
- Next: Extract a matched explicit local stability threshold.
- Derivation: `sec:middle-rotation` in `sections/middle.tex`.
- Sources: `research/round13/advisor/weak-coupling-stability.md`, `research/round13/README.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R13-moments — Compact moment certificates and uniqueness

- Equation: eq:middle-moments; H_r >= 0; L_{r-1} >= 0.
- Assumptions: Normalized compact SU(2) Haar-derived Euclidean measure; finite dimensionless action coefficients; complete signed normalization and remainder; static coupling response.
- Application: Exact scalar Haar moment enclosures.
- Change: Retained variance and all recurrence/support constraints; proved complete-hierarchy uniqueness.
- Limitation: No hierarchy rate; code only levels 1–6 and slack must vanish.
- Next: Connected shared-link hierarchy with complete identities.
- Derivation: `sec:middle-moments` in `sections/middle.tex`.
- Sources: `research/round13/moments/README.md`, `research/round13/README.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R13-response — Exact scalar response

- Equation: eq:middle-response; kappa u'+3u=kappa(1-u^2), u'(0)=1/4.
- Assumptions: Normalized compact SU(2) Haar-derived Euclidean measure; finite dimensionless action coefficients; complete signed normalization and remainder; static coupling response.
- Application: Coupling-response analysis and residual error transport.
- Change: Separated regular Haar branch, singular branches and changed-prior countermodel.
- Limitation: Static response; sampled floating error is not a global enclosure.
- Next: Certify a full residual envelope between numerical nodes.
- Derivation: `sec:middle-moments` in `sections/middle.tex`.
- Sources: `research/round13/response/response.md`, `research/round13/README.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R14-loop1 — Exact conditional Haar reduction with removable zero field.

- Equation: C'(0)=v1 v2; |C''|<=7; C(0,0,eta)=u(eta)/4.
- Assumptions: Normalized compact SU(2) Haar-derived Euclidean measure; finite dimensionless action coefficients; complete signed normalization and remainder; static coupling response.
- Application: Controlled two-holonomy interaction and local covariance sign.
- Change: Exact conditional field and removable zero-field reduction replace factorization.
- Limitation: Small-eta bound insufficient at selected central fixture; floating comparisons diagnostic.
- Next: Exact rational same-action covariance enclosures.
- Derivation: `sec:middle-moments` in `sections/middle.tex`.
- Sources: `research/round14/forward/loop1.md`, `research/round14/advisor/loop1_gate.json`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R14-loop2 — 23 exact finite-measure covariance enclosures independently replayed using characters.

- Equation: R_N=M^(N+1)/(N+1)!/(1-M/(N+2)); Z>=1.
- Assumptions: Normalized compact SU(2) Haar-derived Euclidean measure; finite dimensionless action coefficients; complete signed normalization and remainder; static coupling response.
- Application: Normalized rational covariance certification.
- Change: 23 exact enclosures certify selected central target including full tails.
- Limitation: Static finite action; cap48 distinct from uncapped convergence theorem.
- Next: Continuous target-interval coverage.
- Derivation: `sec:middle-moments` in `sections/middle.tex`.
- Sources: `research/round14/forward/loop2.md`, `research/round14/advisor/loop2_gate.json`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R15-A1 — All8 positive exact midpoints, all8 coarse transported lower bounds insufficient.

- Equation: C(cell) subset [L-2rho,U+2rho].
- Assumptions: Normalized compact SU(2) Haar-derived Euclidean measure; finite dimensionless action coefficients; complete signed normalization and remainder; static coupling response.
- Application: Transport exact covariance point intervals.
- Change: Eight positive midpoint results correctly fail all eight coarse cells.
- Limitation: Positive point values do not prove complete interval positivity.
- Next: Bisect failing cells using unchanged point accuracy.
- Derivation: `sec:middle-moments` in `sections/middle.tex`.
- Sources: `research/round15/forward/A1/derivation.md`, `research/round15/advisor/loop-gates/A1.json`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R15-A2 — Refined failing cell radii rather than increasing already sufficient point precision.

- Equation: 8 -> 16 -> 21 cells; minimum lower approximately0.0003346525.
- Assumptions: Normalized compact SU(2) Haar-derived Euclidean measure; finite dimensionless action coefficients; complete signed normalization and remainder; static coupling response.
- Application: Complete positive cover of eta in[1/8,1/4].
- Change: Refined geometry rather than unnecessarily increasing point precision.
- Limitation: Finite SU2^2 action only; cap failures retained.
- Next: Higher-dimensional or larger-graph certified covers.
- Derivation: `sec:middle-moments` in `sections/middle.tex`.
- Sources: `research/round15/forward/A2/result.md`, `research/round15/advisor/loop-gates/A2.json`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R15-B1 — Closed cube has six-way dependence while any five face class observables factorize; use actual character gluing and distinct face derivatives in B2.

- Equation: eq:middle-cube; E product6 x=1/1024.
- Assumptions: Actual oriented finite cube/two-cube graph; normalized link Haar; ordinary SU(2) characters of dimension n+1; exact total action degree and all fusion channels.
- Application: Graph-faithful closed-cube Haar contraction.
- Change: Proved six-way dependence alongside any-five class-function factorization.
- Limitation: Does not assert six independent holonomies or Hamiltonian gap.
- Next: Full normalized Wilson-weighted cube integral.
- Derivation: `sec:middle-gluing` in `sections/middle.tex`.
- Sources: `research/round15/forward/B1/derivation.md`, `research/round15/advisor/loop-gates/B1.json`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R15-B2 — Character dimension and separate face derivatives retained; coarse degree failures remain explicit.

- Equation: Z=sum d^-4 a_n^6; inserted A=sum d^-4 (a_n')^6.
- Assumptions: Actual oriented finite cube/two-cube graph; normalized link Haar; ordinary SU(2) characters of dimension n+1; exact total action degree and all fusion channels.
- Application: Finite closed-cube Wilson expectation.
- Change: Retained dimension factors and distinct-face derivatives with full Taylor tails.
- Limitation: Product expectation is not a connected six-face cumulant; coarse degrees fail.
- Next: Shared-face higher-incidence graph.
- Derivation: `sec:middle-gluing` in `sections/middle.tex`.
- Sources: `research/round15/forward/B2/derivation.md`, `research/round15/advisor/loop-gates/B2.json`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R15-C1 — Cube lower bound is zero at common lambda=alpha/2; accepted B1 trial moments permit a variational ground-energy upper bound.

- Equation: delta_G=3alpha*girth/4; Delta>=delta_G-sum|lambda_p|.
- Assumptions: Full untruncated finite SU(2) link Hamiltonian; all-vertex Gauss law, no external charges; alpha>0 in fixed physical energy units; bounded Wilson potential; analytically complete omitted spectrum where used.
- Application: Full untruncated finite-graph gap bound.
- Change: Distinguished physical girth gap from full-link 3alpha/4 gap.
- Limitation: Cube bound zero at lambda=alpha/2; global budget grows with volume.
- Next: Variational E0 upper bound with independent E1 lower bound.
- Derivation: `sec:middle-finite-gap` in `sections/middle.tex`.
- Sources: `research/round15/forward/C1/derivation.md`, `research/round15/advisor/loop-gates/C1.json`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R15-C2 — The independent E1 lower bound and trial E0 upper bound repair the C1 zero-margin fixture; no trial gap was substituted for the full gap.

- Equation: eq:middle-arrow; common cube range r<12/23.
- Assumptions: Full untruncated finite SU(2) link Hamiltonian; all-vertex Gauss law, no external charges; alpha>0 in fixed physical energy units; bounded Wilson potential; analytically complete omitted spectrum where used.
- Application: Repair finite cube zero margin.
- Change: Combined one-sided full E1 and trial E0 bounds correctly.
- Limitation: Radical interval encloses lower-bound formula, not actual gap.
- Next: Dense two-cube and complete complement improvements.
- Derivation: `sec:middle-finite-gap` in `sections/middle.tex`.
- Sources: `research/round15/forward/C2/derivation.md`, `research/round15/advisor/loop-gates/C2.json`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R16-loop1 — Exact finite two-cube Haar/fusion identities and separate conditional physical energy-scale audit.

- Equation: eq:middle-two-cube; E[(product outer10 x)x_s^2]=2^-19.
- Assumptions: Actual oriented finite cube/two-cube graph; normalized link Haar; ordinary SU(2) characters of dimension n+1; exact total action degree and all fusion channels.
- Application: Shared-face Haar fusion on12-vertex, 20-link, 11-face graph.
- Change: Replaced invalid single-surface label rule by two-disk fusion.
- Limitation: Static graph; full 11-face and outer 10-face actions differ.
- Next: Same observable comparison with shared action on/off.
- Derivation: `sec:middle-gluing` in `sections/middle.tex`.
- Sources: `research/round16/forward/loop1/derivation.md`, `research/round16/advisor/loop1-gate.json`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R16-loop2 — Positive normalized all-eleven observable difference for outer1/8 and shared1/8 versus0, exact width<=1e-12.

- Equation: D near2.4303274916e-7; omitted baseline coefficient41/(81*2^18).
- Assumptions: Actual oriented finite cube/two-cube graph; normalized link Haar; ordinary SU(2) characters of dimension n+1; exact total action degree and all fusion channels.
- Application: Quantitative shared-face action comparison.
- Change: Retained nonzero omitted-action baseline and both normalization errors.
- Limitation: Finite static target; no general monotonicity theorem.
- Next: Additional recoupling and surrounding-link dependence.
- Derivation: `sec:middle-gluing` in `sections/middle.tex`.
- Sources: `research/round16/forward/loop2/derivation.md`, `research/round16/advisor/loop2-gate.json`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R17-a1 — Exact local projector and incidence bounds; physical counterexample to the full pure relative-form shortcut. Dense uniform threshold remains open.

- Equation: Q_p x_p P_p norm1/2; |<Wdiag>|<=(16/3)(lambda_max/alpha)<H0>.
- Assumptions: Finite open cubic full-link graph; H0=alpha sum C_e, alpha>0; all-vertex Gauss law; local plaquette Haar projectors; magnetic energy coefficients lambda_p; at most four elementary plaquettes per link. No dressed-strip blocking is assumed.
- Application: Diagnose diagonal control and vacuum mixing.
- Change: Actual physical trial disproves pure relative bound for full W.
- Limitation: Does not refute valid additive bounds or dressing.
- Next: Restricted link-disjoint support theorem.
- Derivation: `sec:middle-rotation` in `sections/middle.tex`.
- Sources: `research/round17/forward/a1/report.md`, `research/round17/advisor/a1-gate.json`, `research/round17/backward/a1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R17-a2 — Volume-uniform physical gap for the pairwise link-disjoint magnetic-support family with a common positive energy scale; dense overlapping family remains open.

- Equation: Delta>=alpha_min(3/4-rho), rho<3/4.
- Assumptions: All links/electric terms retained; nonzero magnetic plaquettes have pairwise disjoint link supports (shared vertices allowed); rho=max|lambda_p|/alpha<3/4; common alpha>=alpha_min>0. Full-space factorization precedes Gauss restriction.
- Application: Volume-uniform sparse magnetic family.
- Change: Full-link factorization plus gauge-invariant unique ground.
- Limitation: Pairwise link-disjoint support; dense overlaps excluded.
- Next: Internally overlapping dressed strip.
- Derivation: `sec:middle-strips` in `sections/middle.tex`.
- Sources: `research/round17/forward/a2/report.md`, `research/round17/advisor/a2-gate.json`, `research/round17/backward/a2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R17-b1 — Improved full physical gap lower bound on the dense eleven-face two-cube graph, positive for common |lambda|/alpha < 12/43; finite volume only.

- Equation: eq:middle-arrow with11 faces; r<12/43.
- Assumptions: Full untruncated finite SU(2) link Hamiltonian; all-vertex Gauss law, no external charges; alpha>0 in fixed physical energy units; bounded Wilson potential; analytically complete omitted spectrum where used.
- Application: Dense finite two-cube spectral guarantee.
- Change: Rebuilt every repeated-index trial entry on actual graph.
- Limitation: Fixed graph; zero margin at12/43 is certificate boundary.
- Next: Add actual shared-face adjoint trial channel.
- Derivation: `sec:middle-finite-gap` in `sections/middle.tex`.
- Sources: `research/round17/forward/b1/report.md`, `research/round17/advisor/b1-gate.json`, `research/round17/backward/b1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R17-b2 — Exact positive full physical gap lower alpha*1388/284767457 at the dense finite coupling lambda/alpha=12/43, with a proved open variational-amplitude interval.

- Equation: [(6/473)eta-(347/43)eta^2]/[45/44+eta^2]; midpoint1388/284767457.
- Assumptions: Full untruncated finite SU(2) link Hamiltonian; all-vertex Gauss law, no external charges; alpha>0 in fixed physical energy units; bounded Wilson potential; analytically complete omitted spectrum where used.
- Application: Positive full gap at previous endpoint.
- Change: Actual adjoint trial lowers E0 below independent E1 bound.
- Limitation: Amplitude midpoint maximizes numerator, not quotient; no volume theorem.
- Next: Complete low-energy complement.
- Derivation: `sec:middle-finite-gap` in `sections/middle.tex`.
- Sources: `research/round17/forward/b2/report.md`, `research/round17/advisor/b2-gate.json`, `research/round17/backward/b2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R17-c1 — Complete four-adjoint Haar tensor and realized four-cube conditional boundary; no bulk or spectral claim.

- Equation: P=B(B^TB)^-1 B^T; normalized tetrahedral contraction-1/405.
- Assumptions: Actual18-vertex33-link20-face graph; explicitly fixed surrounding links; declared normalized adjoint observable; exact Haar conditioning with outer partition weights.
- Application: Complete central four-adjoint Haar tensor.
- Change: Three invariant channels and negative inverse-Gram entries retained.
- Limitation: One central link with32others fixed.
- Next: Nonzero-action joint observable with actual boundary.
- Derivation: `sec:middle-conditional` in `sections/middle.tex`.
- Sources: `research/round17/forward/c1/report.md`, `research/round17/advisor/c1-gate.json`, `research/round17/backward/c1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R17-c2 — Same-action conditional four-face expectations with complete rational numerator and partition errors; action-only observable closure rejected, full bulk and spectrum open.

- Equation: O_T(0)=-1/405; O_C(0)=13/1215; same action vector.
- Assumptions: Actual18-vertex33-link20-face graph; explicitly fixed surrounding links; declared normalized adjoint observable; exact Haar conditioning with outer partition weights.
- Application: Reject action-only observable closure.
- Change: Equal partition and action coexist with different joint observables.
- Limitation: Conditional central result; surrounding marginal not integrated.
- Next: Sufficient complete action-observable coordinates.
- Derivation: `sec:middle-conditional` in `sections/middle.tex`.
- Sources: `research/round17/forward/c2/report.md`, `research/round17/advisor/c2-gate.json`, `research/round17/backward/c2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R18-a1 — Finite dressed three-square bridge; physical gap at least alpha/8 throughout the declared primary family; no homogeneous volume extension.

- Equation: Delta_strip>=alpha(3/4-rho)-|mu|>=alpha/8.
- Assumptions: Actual ten-link three-square strip; end plaquettes are link-disjoint, |lambda_L| and |lambda_R|<=alpha/2, bridge |mu|<=alpha/8; two bridge links are free in the dressed-end reference; untruncated full-link Hilbert space and fixed alpha>0.
- Application: Bridge two dressed sparse blocks.
- Change: Free bridge link proves zero reference mean and one-norm improvement.
- Limitation: Finite cluster; exact dressed wavefunction unknown and unnecessary.
- Next: Repeat clusters with complete remainder ledger.
- Derivation: `sec:middle-strips` in `sections/middle.tex`.
- Sources: `research/round18/forward/a1/report.md`, `research/round18/advisor/a1-gate.json`, `research/round18/backward/a1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R18-a2 — All finite volumes of the specified spatially decaying inhomogeneous family have physical gap at least7alpha_min/64; boundary reclassification and homogeneous dense/thermodynamic limits remain explicit.

- Equation: Delta>=alpha_min(1/8-|tau|); tau = 1/64 gives7alpha_min/64.
- Assumptions: Finite open cubic graphs; only complete strips at (4i,2j,z) are selected; end/bridge bounds as in A1; every other face has dyadic coefficient alpha tau/(24*2^(x+y+z)); alpha>=alpha_min>0. Boundary coefficients may be reclassified when the volume changes.
- Application: All-finite-volume inhomogeneous full-support family.
- Change: Repeated link-disjoint overlapping strips plus summable remaining faces.
- Limitation: Boundary rule reclassifies coefficients; not yet literal restrictions.
- Next: Fixed infinite assignment and clipped-component theorem.
- Derivation: `sec:middle-strips` in `sections/middle.tex`.
- Sources: `research/round18/forward/a2/report.md`, `research/round18/advisor/a2-gate.json`, `research/round18/backward/a2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R18-b1 — Complete physical complement threshold9alpha/2 and exact QVP Gram on the dense two-cube graph; no finite trial spectrum substituted for the entire omitted space.

- Equation: QH0Q>=9alpha/2; C_pp=sum lambda^2/4; C_pq=lambda_p lambda_q/4.
- Assumptions: Full untruncated finite SU(2) link Hamiltonian; all-vertex Gauss law, no external charges; alpha>0 in fixed physical energy units; bounded Wilson potential; analytically complete omitted spectrum where used.
- Application: Complete physical complement and exact leakage Gram.
- Change: Classified all states below threshold and retained projection subtraction.
- Limitation: Independent Haar faces agree at fourth order; Gaussian fourth moment is false control.
- Next: Codimension-one full excited-energy estimate.
- Derivation: `sec:middle-finite-gap` in `sections/middle.tex`.
- Sources: `research/round18/forward/b1/report.md`, `research/round18/advisor/b1-gate.json`, `research/round18/backward/b1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R18-b2 — Full untruncated physical two-cube signed coefficient-box gap lower bound, separate endpoint ground trial, and bare-coupling domain obstruction. No volume-uniform or continuum claim.

- Equation: Delta/alpha>=(27-3sqrt70)/16 on signed r<=3/8 box.
- Assumptions: Full untruncated finite SU(2) link Hamiltonian; all-vertex Gauss law, no external charges; alpha>0 in fixed physical energy units; bounded Wilson potential; analytically complete omitted spectrum where used.
- Application: Full untruncated dense two-cube gap.
- Change: Converted exact complement/Gram into continuous signed-box theorem.
- Limitation: Fixed graph; standard bare-coupling membership requires g^4>=32/3.
- Next: Larger complete projector and better cross envelope.
- Derivation: `sec:middle-finite-gap` in `sections/middle.tex`.
- Sources: `research/round18/forward/b2/report.md`, `research/round18/advisor/b2-gate.json`, `research/round18/backward/b2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R18-c1 — Complete joint-Gram sufficiency for the declared central S3 observable/action class, exact rational admissibility including singular cases, and independently matched degree0–6 diagnostics. No minimality, finite-t tail, surrounding measure or mass-gap conclusion.

- Equation: eq:middle-gram; fullGram suffices for all real expansion parameter.
- Assumptions: Actual18-vertex33-link20-face graph; explicitly fixed surrounding links; declared normalized adjoint observable; exact Haar conditioning with outer partition weights.
- Application: Coordinate sufficiency for central integral.
- Change: Handles rank-deficient, reflected and zero-action data exactly.
- Limitation: Sufficiency is not minimality or surrounding measure closure.
- Next: Integrate actual surrounding Haar link.
- Derivation: `sec:middle-conditional` in `sections/middle.tex`.
- Sources: `research/round18/forward/c1/report.md`, `research/round18/advisor/c1-gate.json`, `research/round18/backward/c1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R18-c2 — Full normalized two-link conditional six-face integral at the declared signed fixtures, exact tails, actual surrounding Gram/measure connection and preserved omission/symmetry controls. Thirty-one links remain fixed; no physical spectrum or full bulk/continuum claim.

- Equation: E x^a y^b w^c=2^-sum sum m(a,n)m(b,n)m(c,n)/(n+1).
- Assumptions: Actual18-vertex33-link20-face graph; explicitly fixed surrounding links; declared normalized adjoint observable; exact Haar conditioning with outer partition weights.
- Application: Two-link normalized six-face conditional integral.
- Change: Restored all surrounding-only weights and partition reweighting.
- Limitation: 31links fixed; consistent V->Vdagger is a valid integrated exception.
- Next: Three-link shared-middle chain.
- Derivation: `sec:middle-conditional` in `sections/middle.tex`.
- Sources: `research/round18/forward/c2/report.md`, `research/round18/advisor/c2-gate.json`, `research/round18/backward/c2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R19-a1 — For every reachable selected clipped component L, M, R, LM, MR or LMR under the frozen coefficient bounds |lambda_L|/alpha<=1/2, |mu_M|/alpha<=1/8 and |lambda_R|/alpha<=1/2, the full-link local gap lower estimate is at least alpha/8. Positive full-link uniqueness and gauge invariance permit the same lower estimate after Gauss-sector restriction for the finite local component result.

- Equation: Every L,M,R,LM,MR,LMR clipped component gap>=alpha/8.
- Assumptions: Literal finite restrictions of one fixed infinite selected-strip assignment, including all six possible nonempty clips L,M,R,LM,MR,LMR; endpoint bounds alpha/2 and bridge alpha/8; full links, fixed alpha/E_star>0; no thermodynamic convergence assumed.
- Application: Literal finite restrictions of one infinite assignment.
- Change: Removes Round18 coefficient reclassification.
- Limitation: Finite gap statement alone does not construct thermodynamic representation.
- Next: Direct product representation and summable perturbation.
- Derivation: `sec:middle-strips` in `sections/middle.tex`.
- Sources: `research/round19/forward/a1/report.md`, `research/round19/advisor/a1-gate.json`, `research/round19/backward/a1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R19-a2 — Goal A Loop 2 only: direct incomplete product-representation construction for a summable omitted-face perturbation of the accepted A1 complete-strip/free reference. This is not finite clipped-restriction convergence, homogeneous dense stability, continuum Yang-Mills or a mass-gap theorem.

- Equation: eq:middle-dyadic; eq:middle-summable-gap.
- Assumptions: Full-link selected-strip/free reference; end coefficients<=alpha/2 and bridge<=alpha/8; fixed positive alpha/E_star and spacing; summable omitted coefficients; explicit finite/infinite embedding and boundary convention.
- Application: Explicit infinite-volume summable Hamiltonian.
- Change: Closed product-reference form and rank-one spectral isolation.
- Limitation: Initially no finite clipped-limit convergence; fixed representation and spacing.
- Next: Quantitative finite-factor and literal-box convergence.
- Derivation: `sec:middle-strips` in `sections/middle.tex`.
- Sources: `research/round19/forward/a2/report.md`, `research/round19/advisor/a2-gate.json`, `research/round19/backward/a2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R19-b1 — Goal B Loop 1 only: complete strict-cutoff physical projector and exact full cross Gram on the actual finite two-cube SU(2) graph. No continuous coefficient box, dense limit, continuum Yang-Mills or mass-gap claim is accepted here.

- Equation: P=1_{Eel<6alpha}, dimension 48; threshold 99 labels / 107 channels.
- Assumptions: Full untruncated finite SU(2) link Hamiltonian; all-vertex Gauss law, no external charges; alpha>0 in fixed physical energy units; bounded Wilson potential; analytically complete omitted spectrum where used.
- Application: Exact physical channel and cross-Gram inventory.
- Change: Includes all 36 six-cycles and threshold intertwiner multiplicities.
- Limitation: Strict cutoff is full spectral classification, not chosen variational list.
- Next: Continuous signed-box full E1 estimate.
- Derivation: `sec:middle-finite-gap` in `sections/middle.tex`.
- Sources: `research/round19/forward/b1/report.md`, `research/round19/advisor/b1-gate.json`, `research/round19/backward/b1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R19-b2 — Goal B Loop 2 only: finite two-cube continuous signed coefficient-box gap certificate using the accepted B1 48-channel projector, full compressed PVP ledger and exact ordered W^*W cross Gram. No dense limit, continuum Yang-Mills, Clay mass gap or physical-scale matching claim is accepted.

- Equation: eq:middle-48gap; R(7/16)=19/32.
- Assumptions: Full untruncated finite SU(2) link Hamiltonian; all-vertex Gauss law, no external charges; alpha>0 in fixed physical energy units; bounded Wilson potential; analytically complete omitted spectrum where used.
- Application: Wider finite signed coefficient box.
- Change: Improved complement6alpha and exact 47-state row/cross envelopes.
- Limitation: r = 1/2 fails only this sufficient envelope.
- Next: Sharper fixed-graph envelopes or separate volume method.
- Derivation: `sec:middle-finite-gap` in `sections/middle.tex`.
- Sources: `research/round19/forward/b2/report.md`, `research/round19/advisor/b2-gate.json`, `research/round19/backward/b2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R19-c1 — Goal C Loop 1 only: exact finite static U-V-W chain integral on the actual four-cube graph with all other links fixed. This accepts a static mathematical checkpoint and common-V failed-independence discriminator; it does not accept physical energy/time-scale matching, dense convergence, continuum Yang-Mills, a spectral gap theorem or the Clay mass gap.

- Equation: S=3x+y+z+w+t; E[xzwt]=1/64.
- Assumptions: Actual18-vertex33-link20-face graph; explicitly fixed surrounding links; declared normalized adjoint observable; exact Haar conditioning with outer partition weights.
- Application: Actual three-link conditional chain integral.
- Change: Shared-middle dependence retained and freezeW regression checked.
- Limitation: Thirty surrounding links remain fixed; static scale unmatched.
- Next: Continuous signed-kappa result.
- Derivation: `sec:middle-conditional` in `sections/middle.tex`.
- Sources: `research/round19/forward/c1/report.md`, `research/round19/advisor/c1-gate.json`, `research/round19/backward/c1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R19-c2 — Static common-V integral only; physical energy/time matching remains open. No Hamiltonian spectral gap or continuum claim.

- Equation: eq:middle-static-sign.
- Assumptions: Actual18-vertex33-link20-face graph; explicitly fixed surrounding links; declared normalized adjoint observable; exact Haar conditioning with outer partition weights.
- Application: Certified continuous positivity and sign asymmetry.
- Change: Converted exact coefficients into normalized all-interval inequalities.
- Limitation: Degree8 boundary failures do not prove nonpositivity; static model only.
- Next: More surrounding variables or independent physical matching.
- Derivation: `sec:middle-conditional` in `sections/middle.tex`.
- Sources: `research/round19/forward/c2/report.md`, `research/round19/advisor/c2-gate.json`, `research/round19/backward/c2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R20-d1 — Finite-factor completion gives norm-resolvent convergence with explicit dyadic tail on the exact A2 exterior-reference lift.

- Equation: resolvent difference<=alpha|tau|t_L/|Im z|^2.
- Assumptions: Full-link selected-strip/free reference; end coefficients<=alpha/2 and bridge<=alpha/8; fixed positive alpha/E_star and spacing; summable omitted coefficients; explicit finite/infinite embedding and boundary convention.
- Application: Quantitative finite-factor completion.
- Change: Correct exterior-reference lift preserves infinite generator.
- Limitation: Finite factors remain infinite-dimensional; no literal arbitrary-phase theorem yet.
- Next: Ground energies, projections and states.
- Derivation: `sec:middle-strips` in `sections/middle.tex`.
- Sources: `research/round20/forward/d1/report.md`, `research/round20/advisor/d1-gate.json`, `research/round20/reverse/d1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R20-d2 — Ground energy, rank-one projections and bounded observables converge with explicit dyadic errors for D1 lifts.

- Equation: |e-eL|<=epsilonL; ||P-PL||<=min(1,epsilonL/gL).
- Assumptions: Full-link selected-strip/free reference; end coefficients<=alpha/2 and bridge<=alpha/8; fixed positive alpha/E_star and spacing; summable omitted coefficients; explicit finite/infinite embedding and boundary convention.
- Application: Ground-state convergence with explicit dyadic errors.
- Change: Zero trial mean and rank-one residual give sharp denominator.
- Limitation: Requires beta<delta and correct embedding.
- Next: Literal geometric boxes and energy origins.
- Derivation: `sec:middle-strips` in `sections/middle.tex`.
- Sources: `research/round20/forward/d2/report.md`, `research/round20/advisor/d2-gate.json`, `research/round20/reverse/d2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R20-e1 — Literal aligned boxes N=4m+3 converge after explicit reference-energy subtraction and exact exterior-reference lift.

- Equation: (Hbox,N-cN) tensor I+I tensor Href,out=Href+Vbox,N, N=4m+3.
- Assumptions: Full-link selected-strip/free reference; end coefficients<=alpha/2 and bridge<=alpha/8; fixed positive alpha/E_star and spacing; summable omitted coefficients; explicit finite/infinite embedding and boundary convention.
- Application: Aligned literal-box convergence.
- Change: Retained exact strip energy subtraction and orientation-specific tail.
- Limitation: Unshifted absolute energy/resolvent convergence not proved.
- Next: All boundary phases in local-state topology.
- Derivation: `sec:middle-strips` in `sections/middle.tex`.
- Sources: `research/round20/forward/e1/report.md`, `research/round20/advisor/e1-gate.json`, `research/round20/reverse/e1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R20-e2 — All upper-boundary phases of literal growing rectangular boxes converge to the A2 ground state on bounded local observables.

- Equation: |omega_box(A)-omega_inf(A)|<=4||A||epsilonM/gM.
- Assumptions: Full-link selected-strip/free reference; end coefficients<=alpha/2 and bridge<=alpha/8; fixed positive alpha/E_star and spacing; summable omitted coefficients; explicit finite/infinite embedding and boundary convention.
- Application: All-phase rectangular local-state limit.
- Change: Observable support included in common complete central factors.
- Limitation: No global vector or arbitrary-phase norm-resolvent conclusion.
- Next: Local dynamics and GNS identification.
- Derivation: `sec:middle-strips` in `sections/middle.tex`.
- Sources: `research/round20/forward/e2/report.md`, `research/round20/advisor/e2-gate.json`, `research/round20/reverse/e2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R20-f1 — Even among local reversible diffusions the C1 static law does not identify an energy/time coefficient: H_kappa,c=c A_kappa.

- Equation: H=c[-Delta-kappa gradS.grad]; gap>=(3c/4)e^-14|kappa|.
- Assumptions: Conditional SU(2)^3 manifold with shared V; Casimir metric fundamental3/4; known density/kappa; independently supplied energyc; smooth positive mobility; specified observables and initial imaginary-time slopes.
- Application: Demonstrate static clock nonidentifiability.
- Change: Same static density supports independently scaled reversible dynamics.
- Limitation: Added conditional generator, not physical lattice derivation.
- Next: Full derivative closure and independently observed slope.
- Derivation: `sec:middle-clock` in `sections/middle.tex`.
- Sources: `research/round20/forward/f1/report.md`, `research/round20/advisor/f1-gate.json`, `research/round20/reverse/f1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R20-f2 — Exact shared-middle gradient closure, action range[-5,7] and conditional diffusion gap c/6 on |kappa|<=1/8.

- Equation: oscS=12; gap>=c/6 for|kappa|<=1/8; c=-hbar C'(0)/q[f].
- Assumptions: Conditional SU(2)^3 manifold with shared V; Casimir metric fundamental3/4; known density/kappa; independently supplied energyc; smooth positive mobility; specified observables and initial imaginary-time slopes.
- Application: Exact chosen-generator transform and conditional clock inverse.
- Change: Retained actual common-V derivative and improved action range.
- Limitation: No physical slope measured; c unmatched to alpha.
- Next: Mobility deformations and identifying observables.
- Derivation: `sec:middle-clock` in `sections/middle.tex`.
- Sources: `research/round20/forward/f2/report.md`, `research/round20/advisor/f2-gate.json`, `research/round20/reverse/f2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R20-g1 — Literal-box real-time dynamics converges in operator norm on each local observable at fixed physical time, with a strongly continuous Hilbert implementation.

- Equation: local dynamics error<=4||A|||t|epsilonM/hbar.
- Assumptions: Common full-link generators and unbounded onsite terms; bounded interactions with declared uniform envelope or summable tail; fixed spacing; correct complete support and physical time/hbar.
- Application: All-phase fixed-time literal-box dynamics limit.
- Change: Bounded strong Duhamel avoids false operator-norm differentiation.
- Limitation: Full bounded local algebra need not have point-norm time continuity.
- Next: Limiting state's GNS generator.
- Derivation: `sec:middle-dynamics` in `sections/middle.tex`.
- Sources: `research/round20/forward/g1/report.md`, `research/round20/advisor/g1-gate.json`, `research/round20/reverse/g1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R20-g2 — The E2 limiting local state GNS on the full factor algebra is the A2 representation with canonical generator H-e and its inherited gap.

- Equation: GNS[full local algebra] is A2representation; generatorH-e.
- Assumptions: Full bounded local-factor algebra in the A2 incomplete product representation; beta=alpha|tau|107/135<delta=alpha/8; unique ground e<=0; E2 local-state limit; fixed alpha/E_star and hbar. The value |tau|=1/64 is a fixture, not the full theorem domain.
- Application: Identify physical energy origin of full-algebra limiting state.
- Change: Irreducibility and cyclicity proved on dense finite-excitation core.
- Limitation: Gauss-only algebra not yet identified; beta<delta restored.
- Next: Nonvacuous invariant local algebra and physical GNS.
- Derivation: `sec:middle-gns` in `sections/middle.tex`.
- Sources: `research/round20/forward/g2/report.md`, `research/round20/advisor/g2-gate.json`, `research/round20/reverse/g2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R20-h1 — The continuous omitted-face profile has an exact budget and a rigorously delimited sufficient gap certificate at fixed physical scale.

- Equation: eq:middle-profile; gap>=alpha(1/8-|tau|B(q)).
- Assumptions: Omitted weights q^(x+y+z)/24 with 0<q<1, fixed selected strips and positive physical alpha/E_star and spacing; arbitrary tau subject to |tau|B(q)<1/8 for the gap certificate. No canonical ray is assumed; tau=1/64 is the threshold fixture.
- Application: Continuous spatial decay budget.
- Change: Exact class sums locate sufficient budget boundary.
- Limitation: qcrit is not physical transition; q1 infinite sum diverges.
- Next: Constant-budget rays and actual ground-state behavior.
- Derivation: `sec:middle-profile` in `sections/middle.tex`.
- Sources: `research/round20/forward/h1/report.md`, `research/round20/advisor/h1-gate.json`, `research/round20/reverse/h1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R20-h2 — Every strict uniform global perturbation-budget ray returns the actual ground projection to the selected-strip reference, with an exact vacuum variance and a quantitative rate.

- Equation: eq:middle-variance; ||Pq-P0||<=sigma/gbar; -sigma^2/gbar<=eq<=0.
- Assumptions: Same selected-strip reference and 0<q<1; any strict uniform budget |tau(q)|B(q)<=eta/8 with fixed 0<eta<1; fixed positive alpha/E_star and spacing. Exact perturbation norm and leading constants are additionally specified on the canonical ray tau=eta/(8B(q)).
- Application: Ground-state return along fixed-budget rays.
- Change: Exact two-free-link variance beats generic overlap bound.
- Limitation: Endpoint retains selected strips; fixed omitted coefficients vanish.
- Next: Strong operator and correlation limits.
- Derivation: `sec:middle-profile` in `sections/middle.tex`.
- Sources: `research/round20/forward/h2/report.md`, `research/round20/advisor/h2-gate.json`, `research/round20/reverse/h2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R21-i1 — Complete 24-link blocking gives 21 omitted anchor faces and exact normalized local interaction norm 7|tau|; qualitative fixed-spacing stability applies with unevaluated source constants.

- Equation: 24=10+14;21omittedfaces;epsilon=7|tau|.
- Assumptions: Homogeneous bounded Wilson interactions on full infinite-dimensional24-link coarse blocks; selected-strip gap delta=alpha/8; four-site stars including crossing faces; fixed positive physical scales; explicit support norm.
- Application: Exact homogeneous theorem dictionary.
- Change: Complete ownership, all crossing supports and boundary-aware padding.
- Limitation: Yarotsky constants remain unevaluated; no declared numerical tau.
- Next: Construct explicit local rotations and audit global iteration.
- Derivation: `sec:middle-rotation` in `sections/middle.tex`.
- Sources: `research/round21/forward/i1/report.md`, `research/round21/advisor/i1-gate.json`, `research/round21/reverse/i1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R21-i2 — Exact one-star vacuum rotation cancels first-order vacuum mixing and retains a bounded quadratic remainder; a bare pure relative bound for the original interaction fails.

- Equation: ||phiOmega||^2=7tau^2/12; ||R||<=707tau^2/60.
- Assumptions: Homogeneous bounded Wilson interactions on full infinite-dimensional24-link coarse blocks; selected-strip gap delta=alpha/8; four-site stars including crossing faces; fixed positive physical scales; explicit support norm.
- Application: Local domain-safe vacuum dressing.
- Change: Exact cancellation sign and full quadratic remainder.
- Limitation: One-star result; overlapping generated terms not yet controlled.
- Next: Simultaneous finite-volume rotation.
- Derivation: `sec:middle-rotation` in `sections/middle.tex`.
- Sources: `research/round21/forward/i2/report.md`, `research/round21/advisor/i2-gate.json`, `research/round21/reverse/i2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R21-j1 — An actual omitted Wilson loop has a nonzero gauge-invariant fluctuation in the perturbed dyadic vacuum, with a uniform rational variance floor.

- Equation: Var_Psi W>=5321/22500; d^2<=2817/64377572.
- Assumptions: Dyadic summable incomplete product representation; |tau|<=1/64; bounded local-factor or invariant local algebra explicitly named; unique invariant ground; fixed physical scale and hbar.
- Application: Nonzero physical Wilson fluctuation.
- Change: Transfers actual reference variance to perturbed dyadic ground.
- Limitation: Invariant cyclic space only inclusion at this stage.
- Next: Prove equality with invariant Hilbert subspace.
- Derivation: `sec:middle-gns` in `sections/middle.tex`.
- Sources: `research/round21/forward/j1/report.md`, `research/round21/advisor/j1-gate.json`, `research/round21/reverse/j1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R21-j2 — Physical vacuum GNS space equals the gauge-invariant subspace of this representation, with the restricted shifted energy generator and a nonzero imaginary-time Wilson correlator.

- Equation: eq:middle-gns; 0<CW(t)<=VarW exp(-973alpha t/(8640hbar)).
- Assumptions: Dyadic summable incomplete product representation; |tau|<=1/64; bounded local-factor or invariant local algebra explicitly named; unique invariant ground; fixed physical scale and hbar.
- Application: Physical GNS space and imaginary-time spectrum.
- Change: Finite gauge averaging proves reverse cyclic inclusion.
- Limitation: No real-time magnitude decay or measured glueball mass.
- Next: Different homogeneous/continuum representation requires separate proof.
- Derivation: `sec:middle-gns` in `sections/middle.tex`.
- Sources: `research/round21/forward/j2/report.md`, `research/round21/advisor/j2-gate.json`, `research/round21/reverse/j2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R21-k1 — A positive state-dependent mobility preserves the static density but changes reversible dynamics; two chosen Haar correlation slopes identify c and zeta within this conditional family.

- Equation: r_x=3c/16;r_g=c(5/16+zeta/8).
- Assumptions: Conditional SU(2)^3 manifold with shared V; Casimir metric fundamental3/4; known density/kappa; independently supplied energyc; smooth positive mobility; specified observables and initial imaginary-time slopes.
- Application: Two-rate affine-mobility identification.
- Change: Static law independent ofc, zeta; gradmobility drift retained.
- Limitation: Haar inverse only known kappa = 0; synthetic rates only.
- Next: Uniform nonzero-kappa rank and conditioning.
- Derivation: `sec:middle-clock` in `sections/middle.tex`.
- Sources: `research/round21/forward/k1/report.md`, `research/round21/advisor/k1-gate.json`, `research/round21/reverse/k1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R21-k2 — A tunable observable gives a uniform two-rate inverse across the declared static interval, while a positive blind cubic proves that two slopes do not identify arbitrary mobility.

- Equation: D>=1/7168 for a = 1/4,|kappa|<=1/8.
- Assumptions: Conditional SU(2)^3 manifold with shared V; Casimir metric fundamental3/4; known density/kappa; independently supplied energyc; smooth positive mobility; specified observables and initial imaginary-time slopes.
- Application: Robust rank certificate in declared affine family.
- Change: Monotone double-integral determinant and blind cubic countermodel.
- Limitation: Finite-family injectivity does not identify arbitrary mobility.
- Next: Third rate detects hidden cubic.
- Derivation: `sec:middle-clock` in `sections/middle.tex`.
- Sources: `research/round21/forward/k2/report.md`, `research/round21/advisor/k2-gate.json`, `research/round21/reverse/k2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R21-l1 — A third observable detects the previously hidden cubic mobility and gives an exact three-parameter inverse in the declared conditional family.

- Equation: eq:middle-rates; det27/262144;m>=13/32;gap>=13c/192.
- Assumptions: Conditional SU(2)^3 manifold with shared V; Casimir metric fundamental3/4; known density/kappa; independently supplied energyc; smooth positive mobility; specified observables and initial imaginary-time slopes.
- Application: Three-parameter conditional inverse.
- Change: Third observable exposes p3 invisible to old pair.
- Limitation: Inverse at known kappa = 0; polynomial itself classical.
- Next: Finite-data nonidentifiability beyond chosen family.
- Derivation: `sec:middle-clock` in `sections/middle.tex`.
- Sources: `research/round21/forward/l1/report.md`, `research/round21/advisor/l1-gate.json`, `research/round21/reverse/l1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R21-l2 — Any finite list of initial correlation slopes leaves strictly positive mobility freedom; a second derivative detects the explicit hidden fifth-degree direction.

- Equation: N rates admit degreeN null polynomial; Cx''=(c/hbar)^2(9/64+epsilon^2/1024).
- Assumptions: Conditional SU(2)^3 manifold with shared V; Casimir metric fundamental3/4; known density/kappa; independently supplied energyc; smooth positive mobility; specified observables and initial imaginary-time slopes.
- Application: Exact finite-slope limitation and held-out curvature.
- Change: Explicit positive p5 mobility keeps3 slopes but changes generator.
- Limitation: Does not show complete-time-curve ambiguity.
- Next: Specify finite basis and reserve dynamical data.
- Derivation: `sec:middle-clock` in `sections/middle.tex`.
- Sources: `research/round21/forward/l2/report.md`, `research/round21/advisor/l2-gate.json`, `research/round21/reverse/l2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R21-m1 — The fixed-budget summable perturbation converges strongly to zero, giving strong-resolvent and compact-time strong dynamics convergence to the selected-strip reference.

- Equation: Vq->0 strongly with ||Vq||=alpha eta/8.
- Assumptions: Canonical summable family0<q<1, fixed0<eta<1, tau_q=eta/(8B(q)); selected interactions, alpha/E_star, spacing and hbar fixed; complete factor cover.
- Application: Strong-resolvent and compact-time strong dynamics limit.
- Change: Complete-factor commutator extends vacuum residual to dense set.
- Limitation: Norm resolvent/dynamics status unresolved; endpoint is selected strip.
- Next: Connected correlations on growing time windows.
- Derivation: `sec:middle-profile` in `sections/middle.tex`.
- Sources: `research/round21/forward/m1/report.md`, `research/round21/advisor/m1-gate.json`, `research/round21/reverse/m1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R21-m2 — Connected physical correlations converge on explicitly growing time windows in the canonical summable profile, with a nonzero actual physical Wilson fluctuation.

- Equation: error<=||A||||B||[6d+T/hbar(|e|+sigma+2alpha tau D)].
- Assumptions: Canonical profile and stationary complex centered correlations; uniform observable norm product; complete reference-factor supports; physical time; q1 is a limit, not an admitted action.
- Application: Connected physical correlations with gamma<3/2.
- Change: All centering, phases and factor supports retained.
- Limitation: Endpoint failure is failure of this upper certificate.
- Next: Use stationary Heisenberg comparison.
- Derivation: `sec:middle-windows` in `sections/middle.tex`.
- Sources: `research/round21/forward/m2/report.md`, `research/round21/advisor/m2-gate.json`, `research/round21/reverse/m2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R22-n1 — Stationary Heisenberg comparison proves the sharper local connected-correlation bound in the canonical summable model.

- Equation: eq:middle-stationary; gamma<3.
- Assumptions: Canonical profile and stationary complex centered correlations; uniform observable norm product; complete reference-factor supports; physical time; q1 is a limit, not an admitted action.
- Application: Improved fixed-support growing-time certificate.
- Change: Stationarity removes unnecessary time-times-vacuum-residual term.
- Limitation: Actual gamma3 behavior unresolved; no real-time decay assertion.
- Next: Moving complete-factor support budgets.
- Derivation: `sec:middle-windows` in `sections/middle.tex`.
- Sources: `research/round22/reverse/n1/report.md`, `research/round22/advisor/n1-gate.json`, `research/round22/forward/n1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R22-n2 — Complete tail-block cubes have an exact weighted incident-face budget, yielding a joint support/time convergence certificate.

- Equation: eq:middle-moving; beta<1,gamma<3(1-beta).
- Assumptions: Canonical profile and stationary complex centered correlations; uniform observable norm product; complete reference-factor supports; physical time; q1 is a limit, not an admitted action.
- Application: Joint support and time design certificate.
- Change: Exact incident budget including outgoing links and origin boundary.
- Limitation: Necessity only for nonnegative certificate; translated cubes differ.
- Next: Actual endpoint or stronger dynamics estimate.
- Derivation: `sec:middle-windows` in `sections/middle.tex`.
- Sources: `research/round22/reverse/n2/report.md`, `research/round22/advisor/n2-gate.json`, `research/round22/forward/n2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R22-o1 — Complete simultaneous homogeneous rotation has explicit weighted remainder with preserved unbounded operator domain.

- Equation: eq:middle-global-rotation; common25460736/25, reverse1970176/5.
- Assumptions: Homogeneous bounded Wilson interactions on full infinite-dimensional24-link coarse blocks; selected-strip gap delta=alpha/8; four-site stars including crossing faces; fixed positive physical scales; explicit support norm.
- Application: One simultaneous homogeneous rotation.
- Change: All ordered connected supports, root counts and unbounded domain retained.
- Limitation: One-step radius is not gap threshold or iteration closure.
- Next: Generated-support recurrence including diagonal part.
- Derivation: `sec:middle-rotation` in `sections/middle.tex`.
- Sources: `research/round22/reverse/o1/report.md`, `research/round22/advisor/o1-gate.json`, `research/round22/forward/o1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R22-o2 — The bare-reference elimination has explicit all-support bounds, but its retained-diagonal loss majorants cannot certify an infinite iteration at nonzero coupling.

- Equation: eq:middle-recurrence; F = 4r(b+3r/2)/(loss-4r); for r > 0, b >= 0, loss > 4r, F < r iff loss > 4b+10r; r = 0 is separate.
- Assumptions: Finite homogeneous cuboids with arbitrary generated indexed supports; bare H0_Y has gap at least one; retained D terms annihilate local vacua and are updated each stage; scalar, diagonal, residual and domain terms retained; common O1 initial budgets and |tau|<=5/1664; positive-limit exponential weight schedule.
- Application: Precise failed iteration certificate.
- Change: Retained diagonal term forces eventual failure of stated loss majorant.
- Limitation: Not actual algorithm failure; regrouped1/64 differs indexed(9N+16)/(64(3N+1)).
- Next: Structure-sensitive interacting inverse and full boundary terms.
- Derivation: `sec:middle-inverse` in `sections/middle.tex`.
- Sources: `research/round22/reverse/o2/report.md`, `research/round22/advisor/o2-gate.json`, `research/round22/forward/o2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R22-p1 — The prescribed section is nonclosable and its fitted clock fails the reserved correlation.

- Equation: section chi_n(Q0)/(n+1)=1 despite L2norm->0;cfit4alpha.
- Assumptions: Actual18-vertex33-link graph; full Gauss law; magnetic coefficient zero; alpha/E_star, hbar and spacing fixed; treeT0..15+26/root(0,2,0); full physical observable completion frozen.
- Application: Falsify proposed physical section and clock.
- Change: Nonclosable map and held-out full-time discrepancy on actual graph.
- Limitation: Rejects this section only; other reductions remain possible.
- Next: Genuine Haar maximal-tree isometry.
- Derivation: `sec:middle-tree` in `sections/middle.tex`.
- Sources: `research/round22/reverse/p1/report.md`, `research/round22/advisor/p1-gate.json`, `research/round22/forward/p1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R22-p2 — A genuine Haar reduction exactly transports the finite electric dynamics; the declared conditional family fails the reserved data.

- Equation: eq:middle-effective; loop energies9alpha/2,6alpha,9alpha/2.
- Assumptions: Actual18-vertex33-link graph; full Gauss law; magnetic coefficient zero; alpha/E_star, hbar and spacing fixed; treeT0..15+26/root(0,2,0); full physical observable completion frozen.
- Application: Exact pure-electric selected reduction.
- Change: Unitary16chord map, Haar adjoint, full tree/mixed derivatives and domains.
- Limitation: Different observable completion from P1; conditional family still fails.
- Next: Restore all magnetic faces and quantify leakage.
- Derivation: `sec:middle-tree` in `sections/middle.tex`.
- Sources: `research/round22/reverse/p2/report.md`, `research/round22/advisor/p2-gate.json`, `research/round22/forward/p2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R22-q1 — The full magnetic action has correlated positive conditional variance, proving selected-image leakage and a quantitative nonautonomous dynamic defect.

- Equation: eq:middle-leakage; 4<=d<=25/4.
- Assumptions: Same actual graph/tree/J3 as P2; all20-faces; dimensionlesslambda>=0 and fixedalpha; Haar electric reference, not interacting ground; full infinite-rank blocks and H1/H2 domains.
- Application: Exact actual-model magnetic leakage.
- Change: Three correlated faces rule out autonomous selected compression.
- Limitation: Haar is not interacting ground; no operator-norm Taylor promotion.
- Next: Exact projected memory and complementary spectrum.
- Derivation: `sec:middle-memory` in `sections/middle.tex`.
- Sources: `research/round22/reverse/q1/report.md`, `research/round22/advisor/q1-gate.json`, `research/round22/forward/q1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R22-q2 — The actual magnetic projection has exact memory/resolvent identities, seven-energy fixed-channel leading matrices and explicit cubic full-Hilbert operator remainders.

- Equation: eq:middle-memory-errors; seven exact channel energies.
- Assumptions: Same actual graph/tree/J3 as P2; all20-faces; dimensionlesslambda>=0 and fixedalpha; Haar electric reference, not interacting ground; full infinite-rank blocks and H1/H2 domains.
- Application: Projected dynamics with explicit kernel and self-energy errors.
- Change: Full return factor, offdiagonal weight1/4 and complete leading spectrum.
- Limitation: No autonomous2-channel closure; absolute not late-time relative accuracy.
- Next: Controlled interacting projected approximation with original clock.
- Derivation: `sec:middle-memory` in `sections/middle.tex`.
- Sources: `research/round22/reverse/q2/report.md`, `research/round22/advisor/q2-gate.json`, `research/round22/forward/q2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R22-r1 — The actual initial diagonal has a uniform local inverse, while its local homological generator leaves an exact nonzero SU2 crossing-boundary defect.

- Equation: eq:middle-boundary; GY>= (1-28|tau|)HY.
- Assumptions: Homogeneous initial diagonal from I1/O1; actual untruncated24-link blocks; |tau|<=5/1664 (initial inverse may allow<1/28); complete generated supports, exterior-source convention, unbounded domains and cardinality weights retained.
- Application: Initial interacting local inverse and boundary audit.
- Change: Absorbs interior diagonal while proving actual SU2 crossing defect.
- Limitation: Diagnostic source not identified as generated residual; initial D only.
- Next: Boundary-complete inverse response with domain control.
- Derivation: `sec:middle-inverse` in `sections/middle.tex`.
- Sources: `research/round22/reverse/r1/report.md`, `research/round22/advisor/r1-gate.json`, `research/round22/forward/r1/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## R22-r2 — The actual initial boundary-complete vacuum response converges with explicit spatial and graph tails; its source-sector and specified volume-weight limits are exact.

- Equation: eq:middle-neumann; local-source remainderA_Y tensor Qext.
- Assumptions: Homogeneous initial diagonal from I1/O1; actual untruncated24-link blocks; |tau|<=5/1664 (initial inverse may allow<1/28); complete generated supports, exterior-source convention, unbounded domains and cardinality weights retained.
- Application: Initial boundary-complete response with spatial/graph tails.
- Change: Proves actual response regularity and exact source-sector mismatch.
- Limitation: Global vacuum cancellation not local identity extension; cardinality upper sum fails.
- Next: Full-source cancellation plus useful weighted decomposition and later-stage gaps.
- Derivation: `sec:middle-inverse` in `sections/middle.tex`.
- Sources: `research/round22/reverse/r2/report.md`, `research/round22/advisor/r2-gate.json`, `research/round22/forward/r2/report.md`.
- Audit: historical status preserved; source bytes hashed; new targeted arithmetic is recorded separately in JSON.

## Independent arithmetic

| Identity | Exact value |
|---|---|
| dyadic omitted weight | 107/135 |
| squared profile weight | 2504/11475 |
| dyadic spectral threshold | 973/8640 |
| I2 local variance | 7/12 |
| J1 projector squared budget | 2817/64377572 |
| J1 variance floor | 5321/22500 |
| L1 inverse determinant | 27/262144 |
| R1 crossing residual squared | 7/432 |
| R17 B2 exact positive margin | 1388/284767457 |
| R19 r7/16 discriminant | 289/64 |
| R19 r7/16 E1 lower | 19/32 |
| Q2 excited-channel total | 19/4 |
| Q2 excited-channel first moment | 285/8 |
| N2 origin one-cell budget | 107/384 |

## Literature mapping

- `yarotsky2004quasiparticles`: https://arxiv.org/abs/math-ph/0411042 — Definitions and Theorems1-3; infinite onsite spaces, bounded finite-range perturbations, qualitative constants; no numerical threshold imported.
- `bravyi2008polynomial`: https://arxiv.org/abs/0707.1894 — Qubit/two-site theorem scope excluded as numerical rotor threshold.
- `bauer2023basis`: https://arxiv.org/abs/2307.11829 — ArXivv1 equations55-56 for electric/magnetic normalization; published metadata key retained by bibliography reviewer.
- `nachtergaele2014dynamics`: https://arxiv.org/abs/1410.8174 — Strong/weak operator products, cocycles and integrals in section2; no imported numerical gap theorem.
- `burbano2024gauge`: https://arxiv.org/abs/2409.13812 — v2 AppendixC maximal-tree variables and electric transport; actual graph expressions/domain statements proved in project.
- `delvecchio2021unbounded`: https://arxiv.org/abs/2108.13907 — Domain and local interacting inverse comparison; evolving-gap/induction premises not automatically supplied and no source threshold imported.
- `nistDLMFGegenbauer`: https://dlmf.nist.gov/18.5.E10 — Classical C3^(2) and C5^(2) finite polynomial provenance; not claimed as new polynomials.
- `teschl2014methods`: https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf — Standard forms, spectral theory, bounded perturbation and resolvent identities. Historical R2 source uses an older2009 pagination and derives the inverse sign directly; do not conflate editions.
