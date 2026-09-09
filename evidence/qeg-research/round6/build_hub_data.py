"""Bind the review pages to authored claims and recorded evidence, not live computation."""
from pathlib import Path
import csv
import json
import math
import shutil

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
SITE = RESEARCH.parent / 'physics-observatory'
DIST = SITE / 'dist'

def read(name):
    return json.loads((RESEARCH / name).read_text())

def claim(id, title, summary, equation, definitions, assumptions, steps, tests,
          objection, resolution, connection, route, falsifiers, limit, *,
          kind='proof', new=False, doc='round5/theorem_advisor.md', related=(),
          sources=('D001',), plot=None, verification='', scope='', claim_text=None):
    return dict(id=id, title=title, summary=summary, technicalSummary=claim_text or summary,
                claim=claim_text or summary, equation=equation, definitions=definitions,
                assumptions=assumptions, steps=steps, tests=tests, objection=objection,
                resolution=resolution, connection=connection, route=route,
                falsifiers=falsifiers, limit=limit, kind=kind, new=new, doc=doc,
                related=list(related), sources=list(sources), plot=plot,
                status={'proof':'Conditional mathematical result','check':'Verified on stated tests','conditional':'Conditional framework identity'}[kind],
                verification=verification, scope=scope,
                origin='Project derivation; literature novelty unestablished' if kind=='proof' else 'Reproduction / computational implementation',
                reviewStatus='Independent skeptic reviewed the stated scope; accepted with the limitations below.',
                extraDoc='round6/skeptic_review.md')

claims = []
claims.append(claim('R5-T1','Global existence of the finite coupled model',
 'The finite list of quantum modes and the electric field can evolve for every finite forward time, provided the denominator stays globally positive. The proof uses a positive energy and an ODE continuation theorem.',
 'a′ = −x;  rᵢ′ = 2 hᵢ × rᵢ\nx′ = [F − e²(S + D x²)] / Z\nW = Z x²/2 + e²U ≥ 0;  W′ = xF;  Z ≥ μ > 0',
 'In natural units ℏ=c=1, s=mₑt, a=eA_z/mₑ, x=eE_z/mₑ² and b=|eB|/mₑ². Fix canonical momenta kᵢ, Mᵢ>0, wᵢ>0, e²>0 and finite real χ. The kinetic momentum pᵢ(s)=kᵢ−a(s) evolves in time. Define hᵢ=(Mᵢ,0,pᵢ), ωᵢ=|hᵢ|, S=Σwᵢ(rᵢz+pᵢ/ωᵢ), C=ΣwᵢMᵢ²/(4ωᵢ⁵), D=Σwᵢ5Mᵢ²pᵢ/(8ωᵢ⁷), Z=1+χ−e²C, U=Σwᵢ(hᵢ·rᵢ+ωᵢ).',
 ['A fixed finite mode list, constant e² and χ, and finite initial data.', 'Physical Bloch data |rᵢ(0)| ≤ 1; fixed positive masses and weights.', 'F is continuous on every finite forward interval.', 'Z(a) ≥ μ > 0 for all real a; checking one sampled trajectory is insufficient.'],
 [('Preserve physical mode norms','The cross product is orthogonal to rᵢ, so d|rᵢ|²/ds = 0.'),
  ('Build a nonnegative energy','hᵢ·rᵢ ≥ −ωᵢ makes U ≥ 0. The positive denominator then controls x².'),
  ('Check every derivative and sign','pᵢ′ = x gives U′ = xS and C′ = −2Dx. Substitution cancels the mode exchange and derivative-subtraction terms, leaving W′ = xF.'),
  ('Avoid dividing by zero energy','Apply the differential estimate to √(W+ε), integrate, then let ε decrease to zero. This covers a vacuum start W(0)=0.'),
  ('Close the continuation argument','The energy controls x on every finite interval; a(s)=a(0)−∫x is then finite there, and every rᵢ remains bounded. The smooth finite-dimensional vector field cannot escape a compact set in finite time.')],
 ['Sixteen symbolic checks, including fourteen exact identities and two deliberate-defect controls, repeated in the corrected runner.', 'Independent critic checks physical-state and zero-energy premises.', 'Exact denominator certificates supply μ for selected finite families.'],
 'A time plot with no blow-up is not a global theorem; a coefficient that becomes zero invalidates division in the ODE. The energy argument also fails for arbitrary nonphysical Bloch data.',
 'The result is conditional on a global positive gap, fixed finite dimension and physical data. The selected and extended fixed-window certificates establish the gap in stated cases; the joint-cutoff counterexample prevents generalizing it.',
 'Local ODE theory supplies continuation, while the energy identity and a separate coefficient bound supply its hypotheses. Continuum current and stress convergence are later obligations.',
 'Finite physical modes + global Z-gap + continuous F → positive work identity → finite-time bounds → global finite-model continuation',
 ['Reverse a feedback sign and recheck W′−xF.', 'Allow Z=0 or an infinite unbounded-energy mode family: the proof no longer applies.'],
 'No continuum theorem, metric evolution, arbitrary initial quantum state or all-time bound on a is proved.',
 related=('R5-C1','R5-E1','R6-L2','R6-L3'), verification='Conventional proof, independent scope review and exact symbolic identities; not a proof-assistant certificate.', scope='Finite homogeneous Maxwell–Dirac mean-field ODE.'))

claims.append(claim('R5-C1','An exact positive-denominator certificate',
 'For the original b = 10, K = 20, N = 4 setup, the denominator exceeds 3/4 at every potential. This is an exact inequality, stronger than checking its value along a numerical run.',
 'e²C(a) < 66325137500 / 274510827927 < 1/4\nχᵦ > 0  ⇒  Z(a) > 3/4,  for every a ∈ ℝ',
 'N is the inclusive highest Landau index: n=0,…,4. Mₙ²=1+2bn and dₙ=2−δₙ0. Positive longitudinal weights integrate constants exactly, summing to 2K. α=e²/(4π)<1/137 and π>157/50.',
 ['Exact coefficients with positive weights and total weight 2K on each level.', 'b=10, K=20, N=4; the all-finite-N extension is a separate new result.', 'The fixed susceptibility matching defined in the model.'],
 [('Bound every mode independently','ω ≥ M implies M²/(4ω⁵) ≤ 1/(4M³), independent of the moving potential.'),
  ('Sum only certified positive weights','The total longitudinal weight converts the estimate to bK[1+2Σₙ₌₁⁴(1+20n)⁻³ᐟ²]/(8π²).'),
  ('Replace irrational values conservatively','Use explicit lower bounds 84, 246, 427, 729 for the four mass cubes, α<1/137 and π>157/50.'),
  ('Compare exact integers','Fraction arithmetic establishes the quoted rational is below 1/4. Binet’s positive integral proves χᵦ>0, so Z>3/4.')],
 ['Exact rational cross multiplication.', 'A separate rounded-coefficient certificate gives a conservative margin about 0.7653173589 for its stored finite list.', 'A deliberately coarse grid in a different K-window shows why an integral maximum cannot replace this discrete proof.'],
 'A coefficient certificate for exact weights does not automatically certify rounded machine coefficients, and neither is an interval enclosure of an ODE trajectory.',
 'The exact theorem and the stored rounded-coefficient check are labeled separately. The later all-N proof extends the exact finite family at the same K, without asserting state convergence.',
 'This certificate supplies the global-gap premise of the finite continuation and forcing estimates.',
 'Mass lower bound + positive weights + exact arithmetic + χ>0 → Z>3/4 → finite continuation / forced bound',
 ['Negative weights or an altered total weight invalidate the proof.', 'Changing K or matching requires recomputing the certificate.'],
 'This original result covers N=4 and exact coefficients; the rounding record is a different certificate.',
 related=('R5-T1','R6-L2','R6-L1'), sources=('D002','D003'), verification='Exact rational proof independently reconstructed; rounded coefficients checked separately.', scope='Original finite discrete family, all real a.'))

claims.append(claim('R5-E1','An explicit bound on the driven electric field',
 'The total size of the applied drive bounds the electric field. A vacuum-start pulse with total amplitude λ keeps |x| below 4|λ|/3 in the certified family.',
 '|x(s)| ≤ √(2W₀/μ) + (1/μ) ∫₀ˢ |F(τ)| dτ\nW₀=0, μ=3/4, F=λg, g≥0, ∫g=1 ⇒ |x(s)| ≤ 4|λ|/3',
 'W is the positive total energy of the reduced model; μ is a proven global denominator lower bound. The pulse normalization is over its entire support.',
 ['The hypotheses of the finite continuation theorem.', 'Finite source integral on the interval being bounded.', 'For the simplified pulse bound: exact vacuum initial data and nonnegative normalized g.'],
 [('Start with the exact work identity','W′=xF and W≥μx²/2 imply |W′|≤√(2W/μ)|F|.'),
  ('Regularize the square root','Use W+ε to avoid a singular expression at a vacuum start. Integrate before taking ε→0.'),
  ('Translate energy back to the field','Apply |x|≤√(2W/μ). For an integrable source this bound is uniform in time.'),
  ('Respect what integration can do','a is the time integral of −x. A uniform bound on x alone permits linear growth of a and does not bound a for all time.')],
 ['Symbolic work identity and exact coefficient proof.', 'Independent counterexamples to replacing an electric bound with full-state all-time stability.', 'Finite source and zero-energy edge cases included in the proof review.'],
 'The bound is sometimes read as decay or stability of every variable; it states neither.',
 'Only the electric amplitude and positive energy receive the stated global control. Decay, scattering, potential growth and pumped tangent stability require additional analysis.',
 'The nonlinear energy argument motivates the new positive second variation at stationary vacuum, but cannot be differentiated into a positive norm without a separate derivation.',
 'W′=xF + Z≥μ → integrated field bound → candidate stationary-vacuum response bound (new proof required)',
 ['A signed source integral ∫F cannot replace ∫|F| for an arbitrary oscillatory source.', 'Omitting the ε argument leaves the vacuum-start proof incomplete.'],
 'No decay rate, bound on all tangent variables, or quantum-noise estimate follows.',
 related=('R5-T1','R5-C1','R6-L4'), verification='Exact inequality under the theorem hypotheses; numerical plots are illustrations only.', scope='Finite-model forced dynamics, locally integrable source size.'))

claims.append(claim('R4-R1','Causal tangent response of the coupled trajectory',
 'The code computes how the coupled field changes under a small change in the applied source, including the current’s feedback. A delayed source perturbation has no earlier response in the checked setup.',
 'v′=−u; q=−v\nu′ = [f−e²(δS+δD x²+2Dxu)+e²δC x′]/Z\nηᵢ′ = 2hᵢ×ηᵢ + 2(0,0,q)×rᵢ',
 'v=δa, u=δx, ηᵢ=δrᵢ and f=δF. For fixed grid: δS=Σw[ηz+M²q/ω³], δC=−Σw5M²pq/(4ω⁷), δD=Σw5M²(M²−6p²)q/(8ω⁹). A simultaneous gauge/grid translation instead uses q=δk−v.',
 ['A common parameter neighborhood with differentiable admissible initial data and source parameter derivatives jointly continuous on compact time/parameter sets, on a finite interval where the base denominator stays separated from zero.', 'Retarded support requires zero initial tangent and no source change before the probe.', 'The plus/minus reference runs must be centered on the same base source, including any nonzero probe.'],
 [('Differentiate the full quotient','Retain variation of Z; moving its derivative to the numerator gives the +e²δC x′ term.'),
  ('Differentiate the state feedback','The Bloch variation and all counterterm variations contribute to the current. A prescribed-field response is not this coupled tangent.'),
  ('Specify preparation before interpreting causality','Uniqueness of the homogeneous tangent system gives zero response before a delayed perturbation only for unchanged prior source and zero tangent data.'),
  ('Cross-check independently','Compare centered finite differences, spinor controls, simultaneous grid/potential gauge translation and work/orthogonality identities. Refine time accuracy and quadrature separately.')],
 ['Historical selected response: 512→1024 nodes gives max |Δu|=2.1572511138545636e−10 at fixed b=10,K=20,N=4.', '128→256 and 256→512 fail the historical 10⁻⁶ full-history gate; those failures remain recorded.', 'Nonzero-probe bug repaired: finite-difference error now 4.59e−8 → 5.02e−9 → 4.70e−10 on a separate small regression setup.', 'Gauge comparison for that corrected regression differs in x by 2.78e−14. Missing causal observation samples now cannot pass vacuously.'],
 'This source-amplitude tangent is a restricted projection of the finite-model retarded current response, including its contact terms; it does not reconstruct the full spacetime kernel or symmetrized quantum noise. A signed first variation of energy is not a norm. Some comparisons used the wrong nonzero probe history.',
 'The code-family bug is reproduced and fixed in round6/code; the matched default fixture is unchanged. The result remains a finite-time classical tangent of a quantum mean-field expectation trajectory, with fixed regulators.',
 'Finite ODE differentiability supplies the tangent equations. The exact stationary vacuum allows a new positive quadratic response energy; a pumped base does not inherit it automatically.',
 'Finite smooth flow + declared source family → tangent response → vacuum-only positive second variation; quantum noise remains open',
 ['Nonzero delayed-probe finite differences centered at zero reproduce the old false failure.', 'An initial-state perturbation can cause pre-probe response and violates the claimed retarded preparation.'],
 'No continuum convergence, full retarded QED kernel, quantum noise, metric response or all-time pumped stability is established.',
 kind='check', doc='round4/response_contract.md', related=('R5-T1','R6-L4'), verification='Historical fixed-grid convergence and independent controls; newly repaired nonzero-probe regression.', scope='Finite-time response of the stated finite mean-field trajectory.', plot='probe'))

claims.append(claim('R3-M1','A recorded backreacting electric-field baseline',
 'The electric field and quantized Dirac modes evolve together after an externally supplied pulse, with a fixed magnetic background. The recorded curves are a finite-model baseline for later response tests.',
 'rᵢ′=2hᵢ×rᵢ; a′=−x\nZx′=F−e²(S+Dx²);  W′=xF',
 'Flat homogeneous background in natural units ℏ=c=1; dimensionless b=|eB|/mₑ². A fixed finite Landau list and canonical momentum window define the regulator. An external pump supplies energy before being switched off.',
 ['Specified matched current and energy subtraction, with a fixed magnetic field.', 'The initial vacuum and external pulse encoded in the archived run.', 'A finite numerical approximation; trajectory samples do not certify every intermediate time.'],
 [('Define the state and source','Initialize the physical mode vacuum and a smooth pulse with documented normalization.'),
  ('Evolve the coupled equations','Compute the expectation-value current from evolving modes and feed it into the electric evolution.'),
  ('Audit the energy source','Track supplied work and the renormalized energy identity; do not interpret externally supplied energy as vacuum extraction.'),
  ('Check independent observables','Norm conservation, work balance, sign tests and weak-source matching offer different checks. An energy-conserving wrong matching is still possible.')],
 ['Archived baseline, diagnostic histories and independent-control records remain accessible in Computed fields.', 'The new audit inspected every line of the legacy computational file but does not claim a new production rerun.', 'The matched small baseline comparator is bit-for-bit unchanged by round6 response fixes.'],
 'Conservation alone can pass for a self-consistent but physically wrong subtraction; a previous claimed cancellation fix was absent from the legacy source.',
 'Legacy source and its limitation are preserved explicitly. The current matched response implementation uses its documented per-mode organization; physical matching requires an independent low-field check.',
 'The baseline makes a concrete trajectory available for finite-time tangent tests. It does not provide the directional quantum stresses needed for gravity.',
 'Declared finite modes + matched mean-field current → baseline trajectory → tangent and stress obligations',
 ['Remove supplied work from the accounting and the energy interpretation becomes false.', 'Change the finite matching consistently in current and energy: conservation alone may not detect it.'],
 'Fixed magnetic background, flat metric, no collisions or full quantum photon fluctuations; no vacuum-energy extraction claim.',
 kind='check',doc='round4/response_contract.md',related=('R4-R1','R5-G1'),verification='Archived finite numerical baseline with controls; new source audit, not a new production acceptance.',scope='Homogeneous finite mean-field dynamics.'))

claims.append(claim('R5-G1','A constraint test for the stress–gravity bridge',
 'For an anisotropically expanding background, the Einstein constraint stays satisfied only when the matter energy balance is consistent. This gives a precise test for the missing quantum stress closure.',
 'Cɡ = H⊥² + 2H⊥H∥ − κρ − Λ\nQ = ρ̇ + 2H⊥(ρ+p⊥) + H∥(ρ+p∥)\nĊɡ = −(2H⊥+H∥)Cɡ − κQ\nCɡ(t) = [V(0)Cɡ(0) − κ∫₀ᵗ VQ dτ] / V(t)',
 'Bianchi I line element: ds²=−dt²+a⊥²(dx²+dy²)+a∥²dz²; H⊥=ȧ⊥/a⊥, H∥=ȧ∥/a∥, κ=8πG, V=a⊥²a∥. Spatial equations: Ḣ⊥=(Λ−κp∥−3H⊥²)/2 and Ḣ∥=Λ−κp⊥−Ḣ⊥−H⊥²−H∥²−H⊥H∥.',
 ['Ordinary Einstein spatial equations, regular nonzero scale factors, differentiable sources.', 'ρ, p⊥ and p∥ belong to the same stress tensor and state prescription.', 'Higher-curvature operators must be included or consistently order-reduced before using ordinary Einstein evolution.'],
 [('Differentiate the constraint directly','Substitute both spatial evolution equations and collect density and pressure terms.'),
  ('Identify the exact conservation residual','The remaining source is −κQ; this is an algebraic identity, not a new stress prescription.'),
  ('Solve the linear propagation equation','V̇=(2H⊥+H∥)V supplies the integrating factor and the displayed integral formula.'),
  ('Include support for an external current','For longitudinal fields Ė=−2H⊥E−Jq−Jext and Ḃ=−2H⊥B. Maxwell gives QEM=−E(Jq+Jext). If Qq=EJq, omitted external support leaves total Q=−EJext.')],
 ['Exact symbolic constraint propagation and electromagnetic exchange cancellation.', 'Explicit counterexample: omit the source-support sector during driving and Q generally remains nonzero.', 'Primary stress-renormalization source scope rechecked: a cited theorem does not complete the nonzero strong-field stress calculation.'],
 'A constraint-propagation identity cannot manufacture the renormalized directional quantum stresses. Omitting external-source stress or higher-curvature terms breaks the intended gravitational model.',
 'This is a conditional diagnostic for a future closure. The strong-field quantum stress and state prescription remain open, and the action alone is not a closed initial-value system.',
 'The force Ward identity supplies consistent energy exchange; the constraint lemma then tests gravitational evolution. The finite electric current alone does not supply ρq,pq⊥,pq∥.',
 'Common current/stress renormalization + source support → Q=0 → constraint propagation → candidate semiclassical evolution',
 ['Set Jext≠0 and omit supporting matter: the constraint acquires a source.', 'Cite a zero gauge-curvature theorem as if it covered the strong-field case: the missing premise remains.'],
 'No self-consistent Einstein–QED solution, black-hole interior, curved-space pair-production rate or desingularization is established.',
 doc='round5/research_bridge.md',related=('R3-M1','R6-L3'),sources=(),verification='Exact conditional identity and independent omitted-source counterexample.',scope='Ordinary Einstein Bianchi I reduction with a yet-to-be-completed matter stress.'))

claims.append(claim('R5-P1','Bidirectional proof planning with independent replay',
 'A finite rule library can be searched from known facts and backward from a target. The program checks the meeting point, replays the route and verifies its cost independently. The rules themselves still need mathematical review.',
 'Forward state F; backward obligation set G\nMeet only if G ⊆ F\nReplay every rule from admitted premises; compare total cost with independent uniform-cost search',
 'Horn rules require the conjunction of all their premises. A node may be a declared model assumption, theorem, numerical record or open obligation; those types are not interchangeable. The frozen selected route costs 14, with forward/backward meeting costs 8 and 6.',
 ['Finite frozen rule library with positive exact integer costs.', 'Only admissible premises and reviewed rules can justify an implication.', 'Backward regression opens sufficient premises; it never reverses an implication.'],
 [('Freeze the proof-planning contract','Validate node types, rule premises, costs and proof references before search.'),
  ('Expand forward and regress backward','Track known facts and all outstanding premises as sets; handle shared prerequisites without counting them as independent discoveries.'),
  ('Verify the meeting and replay','The backward obligations must all be in the forward set. Reconstruct a valid ordered rule sequence from initial premises.'),
  ('Use an independent cost oracle','Uniform-cost search and a separate subset-oracle test family check the selected route cost.'),
  ('Seal the external evidence','Round6 additionally binds referenced proof-file bytes in an immutable evidence manifest, verifies it before and after execution, and distinguishes declared assumptions from conjectures.')],
 ['24 unchanged planner compatibility tests pass.', 'Historical independent review: 19 gates, including 64 separate subset-oracle libraries.', 'New tests reject unsafe labels, changed proof bytes and source mutation, and preserve costs such as the exact integer 10⁴⁰⁰.'],
 'A successful search is not a proof of the admitted rules. Previously, a reference string hash did not bind the document bytes, and conditional:false could be misread as unconditional physics.',
 'New metadata explicitly states conditional-on-declared-assumptions and binds local proof artifacts. The UI calls this a proof planner, not a formal proof kernel; unsafe labels are rejected, but labels cannot certify truth.',
 'The planner organizes the proof obligations for finite continuation. New round6 lemmas are displayed as reviewed connections and are not silently inserted into the executable frozen rule library.',
 'Reviewed finite rules → bidirectional route → replay + independent cost check; external theorem truth remains a separate obligation',
 ['Modify a referenced proof after hashing: the new evidence guard must fail.', 'Present a proposed or unresolved theorem as a proved seed: validation must reject it.'],
 'Not Lean/Coq kernel verification; no automatic scientific discovery, optimal real-world research plan or proof of conjectural premises.',
 kind='check',doc='round5/search_contract.md',related=('R5-T1','R6-L2'),sources=(),verification='Independent replay/oracle checks, 24 compatibility tests and new metadata mutation regressions.',scope='A finite admitted Horn-rule library.'))

claims.append(claim('R6-L1','The exact finite-window coefficient and its maximum',
 'The continuous momentum integral can be evaluated exactly. Its coefficient is largest at zero potential, giving a sharp denominator bound for that integral model and a reference for testing quadrature.',
 'Pᴍ(y) = [u−u³/3]/M²,  u=y/√(M²+y²)\nCₙ,ₖ(a) = b/(16π²) Σₙdₙ[Pᴍₙ(K−a)+Pᴍₙ(K+a)]\nC(a)=C(−a); C′(a)<0 for a>0\nminₐ Z(a)=1+χᵦ−e²C(0)',
 'b>0, K>0, finite inclusive N≥0, Mₙ²=1+2bn, d₀=1 and dₙ=2 for n>0. The defining integral is b/(16π²)Σdₙ∫₋ₖᴷ Mₙ²/[Mₙ²+(k−a)²]⁵ᐟ² dk.',
 ['Continuous longitudinal integration over a fixed symmetric canonical window.', 'Positive field parameter, finite window and finite number of Landau levels.', 'No identification of this integral with a finite quadrature list.'],
 [('Find and verify the primitive','Set u=y/√(M²+y²). Differentiating P gives exactly M²/(M²+y²)⁵ᐟ².'),
  ('Evaluate both endpoints','Oddness of P produces the sum P(K−a)+P(K+a), immediately even in a.'),
  ('Prove the global maximum','The derivative is f(K+a)−f(K−a), where f is positive, even and strictly decreasing with |y|. For a,K>0, |K+a|>|K−a|, so each term is negative.'),
  ('Separate the algorithm from the formula','A floating-point difference between nearly saturated primitives can cancel. The implementation requires high-precision fallback and held-out large-potential tests.'),
  ('Test the forbidden transfer','A two-node positive Gauss rule can put a sharp integrand peak exactly on a node at nonzero a, exceeding the continuous maximum.')],
 ['135 independent SciPy integrations compared with the primitive on the contracted domain.', 'Independent 65-digit integration and symbolic differentiation by the skeptic.', 'Gauss nodes 32–512 compared with the exact integral, with coarse errors retained.', 'Held-out tiny-window/large-potential cancellation cases required after advisor found silent zeros.'],
 'The exact continuous maximum at a=0 does not imply a discrete quadrature maximum at a=0. A mathematically exact primitive can still be numerically evaluated incorrectly.',
 'A retained two-node counterexample refutes the discrete transfer. The primitive is used as an independently checked integration reference, while the discrete certificate uses a separate pointwise bound. Advisor-discovered cancellation and plot errors are repaired and rechecked before publication.',
 'The primitive supplies an exact finite-window reference; positive tails yield the all-N fixed-window certificate and the joint-cutoff obstruction.',
 'Positive even kernel → endpoint primitive → strict maximum → integral-only gap; discrete gap requires a separate argument',
 ['b=10,N=0,K=200,nk=2 at a Gauss node: discrete Z becomes negative while integral Z stays positive.', 'At a=10⁴…10⁷, a silent zero coefficient contradicts positive high-precision integration.'],
 'The sharp maximum is for continuous integration, not arbitrary quadrature. It is not a full trajectory or continuum-QED solution.',
 new=True,doc='round6/extensions.md',related=('R5-C1','R6-L2','R6-L3'),sources=('R6A04',),verification='Exact derivation with independent symbolic/integral checks and a retained discrete counterexample.',scope='Finite continuous momentum window and finite Landau sum.',plot='window'))

claims.append(claim('R6-L2','The gap survives every finite Landau cutoff at fixed window',
 'The original Z>3/4 certificate extends from five Landau levels to every finite number of levels, as long as b=10, K=20 and the positive quadrature assumptions are preserved.',
 'Σₙ₌₅∞(1+20n)⁻³ᐟ² ≤ ∫₄∞(1+20t)⁻³ᐟ²dt = 1/90\ne²C(a) < 67743204500/274510827927 < 1/4\nTherefore Z(a)>3/4 for every real a and every finite N.',
 'Inclusive cutoff n=0,…,N; positive longitudinal weights with sum 2K per level. This uniform coefficient estimate fixes K=20 and b=10. A nested coefficient family also has tail bound e²Σₙ>N Cₙ ≤ αK/[π√(1+2bN)], interpreted only as coefficient convergence.',
 ['Same exact-coefficient matching and α<1/137.', 'Every retained level uses positive quadrature exact on constants.', 'Fixed finite longitudinal window; an increasing mode dimension still needs a separate limiting theory.'],
 [('Retain the original pointwise estimate','C≤bK[1+2Σₙ₌₁ᴺ(1+2bn)⁻³ᐟ²]/(8π²). This is valid for every a and does not need a grid maximum.'),
  ('Control all omitted levels','For a positive decreasing function, each tail term is no larger than the integral over the preceding unit interval. The n≥5 tail is at most 1/90.'),
  ('Preserve exact rational arithmetic','Add this tail to the previous four conservative mass-cube bounds. The resulting rational remains strictly less than 1/4.'),
  ('Supply the theorem premise for each finite N','χ>0 gives Z>3/4, so each individual finite-dimensional system inherits the earlier continuation theorem.'),
  ('Stop before exchanging solution limits','A uniform denominator does not control the initial energy of arbitrarily excited ultraviolet modes or prove convergence of current, state and tangent.')],
 ['Exact rational fraction independently reconstructed by advisor, coder and skeptic formulations.', 'Tail integral 1/90 checked symbolically.', 'The strict gap comparison is integer arithmetic, not a rounded plot.'],
 'Uniformity in one coefficient and one cutoff does not prove convergence of an increasing-dimensional ODE system, and it says nothing uniform when K also grows.',
 'The theorem is deliberately stated for every finite N at fixed K. The coefficient-tail corollary is separate from current/stress/state convergence. The joint-cutoff negative result shows why the distinction matters.',
 'This closes a backward obligation of the finite existence theorem for a broader family. The next unclosed obligation is a common ultraviolet tail estimate for physical states and renormalized observables.',
 'Positive discrete weights + integrable Landau coefficient tail → all-finite-N gap at fixed K → separate finite-model existence theorems',
 ['Let K grow without a new estimate: the proof is not uniform in K.', 'Choose high-frequency excited initial states without energy-tail control: a gap alone cannot establish convergence.'],
 'No infinite-mode evolution, regulator removal or current/stress convergence theorem follows.',
 new=True,doc='round6/extensions.md',related=('R5-T1','R5-C1','R6-L3'),sources=('R6A03','R6A04'),verification='Exact rational tail certificate with independent reconstruction.',scope='Every finite discrete Landau cutoff, fixed b=10,K=20.'))

claims.append(claim('R6-L3','Why the unmodified joint-cutoff proof route fails',
 'When both cutoffs are removed with the existing fixed matching, the coefficient loses every uniform positive lower bound. This disproves a proposed extension of our finite proof route; it does not disprove continuum QED.',
 'Zₙ,∞ = 1 − e²/(12π²)[log(2b)+ψ(N+1+1/(2b))]\nN→∞ ⇒ Zₙ,∞→−∞\nK→∞ and N→∞ cofinally ⇒ Cₙ,ₖ(0)→+∞; Zₙ,ₖ(0)→−∞',
 'χᵦ=e²[b−log(2b)−ψ(1+1/(2b))]/(12π²) is held fixed. The longitudinal integration is continuous. Cofinal means both K and N eventually exceed any fixed finite thresholds; holding either cutoff fixed is a different question.',
 ['Fixed positive b,e² and the stated unmodified matching.', 'The same explicitly divided coefficient Z=1+χ−e²C.', 'Continuous integration and both regulators tending to infinity.'],
 [('Take the full momentum integral at fixed N','The integral per level equals 1/(3Mₙ²) when written with its 1/4 factor. The remaining Landau sum is harmonic at large n.'),
  ('Use an exact recurrence','Use the digamma recurrence to sum the finite harmonic terms, then combine them in Z=1+χᵦ−e²C with the unchanged susceptibility. The finite b-dependent pieces cancel, giving the displayed Z.'),
  ('Strengthen beyond an iterated limit','For any coefficient threshold choose a finite partial sum N₀ whose full-window value exceeds it; then choose finite K₀ large enough. Positivity ensures every N≥N₀,K≥K₀ exceeds that threshold.'),
  ('Identify exactly what fails','No global positive gap uniform in both cutoffs remains. Thus this positive-energy continuation route cannot be passed unchanged to that joint limit.'),
  ('Keep cancellations and renormalization open','Divergence of this separated coefficient alone does not prove divergence of the fully combined, consistently renormalized current. A new common current/energy/stress derivation may reorganize the equations.')],
 ['Finite harmonic sum versus digamma expression.', 'Independent high-precision matching cancellation checks.', 'Cofinal finite-path lower-bound checks illustrate the analytic proof; they do not establish an infinite limit by sampling.', 'Plot generated in log cutoff coordinates, with asymptotic rows labeled and no enormous mode allocation.'],
 'An iterated limit alone does not establish every joint path. Conversely, a divergent separated coefficient is not a theorem that continuum QED has no solution.',
 'Monotonicity supplies a genuine cofinal proof for this coefficient. The interpretation is restricted to uniform gap failure in the unmodified closure. It is neither a physical instability in the selected run nor a measured QED Landau pole.',
 'The obstruction redirects the continuum program toward common subtraction, a specified physical renormalization condition, state-tail control and the force Ward identity.',
 'Exact coefficient + harmonic tail + fixed matching → no joint uniform gap → rederive common renormalized closure before continuum evolution',
 ['A changed matching cannot be accepted as a repair unless current, energy and stress are rederived together.', 'A formal log-cutoff estimate must not be labeled an exact critical integer or a physical measurement.'],
 'This rejects one uniform-coercivity extension. It does not establish nonexistence of a consistently renormalized continuum theory or a trajectory singularity.',
 new=True,doc='round6/extensions.md',related=('R6-L1','R6-L2','R5-G1'),sources=('R6A01','R6A02'),verification='Analytic cofinal argument, exact recurrence and independent finite checks.',scope='Unmodified matched coefficient in the joint continuous-window/Landau limit.',plot='cutoff'))

claims.append(claim('R6-L4','A positive response energy at exact stationary vacuum',
 'At an exact stationary vacuum, a new positive quadratic energy bounds the electric tangent and transformed mode perturbations. The original potential and mode tangents can still grow with time.',
 'tᵢ = ∂p(hᵢ/ωᵢ) = êz/ωᵢ − pᵢhᵢ/ωᵢ³; ξᵢ = ηᵢ + q tᵢ\nZ₀u′=f−e²Σwᵢξᵢz; ξᵢ′=2hᵢ×ξᵢ+u tᵢ; v′=−u\nE₂ = Z₀u² + e²Σwᵢωᵢ|ξᵢ|²; E₂′=2uf\nf=0 ⇒ |u(s)|≤√(E₂(0)/Z₀)',
 'Stationary base: x=F=0, a=a₀, rᵢ=−hᵢ/ωᵢ; Z₀=Z(a₀)>0. Fixed-grid tangent: q=−v, ηᵢ=δrᵢ and hᵢ·ηᵢ=0. ξ is a transformed first variation. E₂ is the second variation of the energy on a twice differentiable pure-state family.',
 ['Exact stationary vacuum, a finite mode list and positive weights.', 'Z₀>0 at that base; no claim about every nonlinear neighboring trajectory.', 'Pure-state, norm-preserving tangent data: hᵢ·ηᵢ=0.', 'For the conserved bound f=0; a driven version uses ∫|f|.'],
 [('Reduce at the exact base','x=x′=0 makes the quadratic-field and quotient-variation terms vanish for a specified reason. The current variation becomes Σwξz.'),
  ('Remove the vacuum-preparation direction','Since q′=u, the transformed variable obeys ξ′=2h×ξ+u t. It stays perpendicular to h.'),
  ('Use the transverse cancellation','ωξ·t=ξz on h·ξ=0, so the feedback term cancels between the electric and mode contributions, giving E₂′=2uf.'),
  ('Relate it to second variation','Differentiate the pure-state norm twice and complete the square in δ²U. This yields ω|η+q t|², not the signed first variation δW.'),
  ('Keep the null and secular directions','E₂ is positive definite in (u,ξ), but only semidefinite in (v,u,η). An explicit one-mode solution has constant E₂ and linearly growing original η.')],
  ['Independent symbolic energy identity on the transverse tangent subspace.', 'Weighted matrix check AᵀG+GA=0 and matrix-exponential evolution; relative energy defect about 2.05e−14 for the stated small check, against a 5e−13 gate.', 'Executed algebraic counterexample: one mode h=(1,0,0), w=e²=1, χ=0, Z₀=3/4, u=1, q=s, η=(0,−1/2,−s), so E₂=1 stays constant while |η| grows. This is the lemma’s algebraic fixture, not the physical b=10 production setup.'],
 'A positive energy in transformed variables can be mistaken for full tangent stability. The cancellation fails for general norm-changing variations or a pumped base.',
 'The accepted result bounds electric and transformed transverse response only. The secular counterexample is retained. The stationary-vacuum family direction is not the simultaneous-grid gauge translation used in the earlier gauge test.',
 'This resolves the previous lack of a positive response norm at a restricted stationary base. The pumped case still needs a separate time-dependent symmetrizer or a rigorous counterexample.',
 'Exact stationary vacuum + transverse tangent + Z₀>0 → positive second variation → electric response bound; pumped/full-tangent stability still open',
 ['Reverse the feedback sign: the weighted skew identity must fail.', 'Drop the contact term or admit a longitudinal tangent: the cancellation is not justified.', 'Use the explicit secular solution to reject boundedness of the original full tangent.'],
 'No all-time bound on v or original η, pumped-trajectory stability, nonlinear orbital stability or quantum-noise control follows.',
 new=True,doc='round6/extensions.md',related=('R5-E1','R4-R1'),sources=(),verification='Independent exact identity, weighted-matrix check, numerical matrix exponential and a retained secular counterexample.',scope='Exact stationary-vacuum finite tangent system.'))

def csvrows(path):
    with path.open() as f:
        return list(csv.DictReader(f))

def make_plots():
    plots = {}
    q = csvrows(HERE/'plot_data/quadrature_refinement.csv')
    window = [r for r in q if int(r['nk'])==512]
    window.sort(key=lambda r:float(r['a']))
    if window:
        plots['window'] = dict(title='Exact coefficient against resolved quadrature', xLabel='Potential a = eA / mₑ', yLabel='Coefficient C(a)',
          series=[dict(name='Continuous integral',points=[[float(r['a']),float(r['exact'])] for r in window]),dict(name='512-node Gauss sum',points=[[float(r['a']),float(r['discrete'])] for r in window])],
          caption='b=10, N=4 inclusive, K=20. Points are recorded evaluations; connecting segments are visual guides. Agreement at these potentials does not turn the continuous maximum theorem into a certificate for every finite grid.', csv='/quadrature_refinement.csv',claim='R6-L1')
    errs={}
    for r in q: errs.setdefault(int(r['nk']),[]).append(float(r['abs_error']))
    plots['quadrature']=dict(title='Quadrature error against the exact integral',xLabel='log₂(number of Gauss nodes)',yLabel='log₁₀(max absolute C error)',
      series=[dict(name='Maximum over specified potentials',points=[[math.log2(k),math.log10(max(v))] for k,v in sorted(errs.items())])],
      caption='Fixed b=10,N=4,K=20. The maximum is over the contracted finite sample of potentials. Coarse failures are retained. This tests quadrature at fixed physical cutoffs, not regulator removal or a whole ODE trajectory.',csv='/quadrature_refinement.csv',claim='R6-L1')
    tail=csvrows(HERE/'plot_data/tail_behavior.csv')
    series=[]
    plotted_tail=[r for r in tail if r['log10_N_plus_1'] and r['Z_N_infinity']]
    for method in dict.fromkeys(r['method'] for r in plotted_tail):
        rows=[r for r in plotted_tail if r['method']==method]
        series.append(dict(name=method,points=[[float(r['log10_N_plus_1']),float(r['Z_N_infinity'])] for r in rows]))
    plots['cutoff']=dict(title='Formal full-window denominator at fixed matching',xLabel='log₁₀(N+1)',yLabel='Zₙ,∞ (dimensionless)',series=series,
      caption='b=10, continuous full momentum window, unmodified χ. Direct special-function evaluation and asymptotic extension are separate labeled series. The enormous formal cutoff is represented only by its logarithm. This is a coefficient obstruction, not a measured instability or a simulated trajectory.',csv='/tail_behavior.csv',claim='R6-L3',zero=True)
    rows=csvrows(HERE/'code_fix_convergence.csv')
    # Preserve the measured CSV schema in the snapshot and map by its known columns.
    if rows:
        plots['probe']=dict(title='The nonzero-probe comparison after repair',xLabel='log₁₀(finite-difference step ε)',yLabel='log₁₀(max electric-tangent error)',
         series=[dict(name=implementation,points=sorted([[math.log10(float(r['epsilon'])),math.log10(float(r['max_abs_tangent_error']))] for r in rows if r['implementation']==implementation])) for implementation in dict.fromkeys(r['implementation'] for r in rows)],
         caption='Same small fixture: b=1,N=0,K=3,nk=12,final time 1.2,61 samples,probe amplitude 0.5. The old comparison uses different source histories. The corrected error decreases over these steps; roundoff eventually limits finite differences. This is a code regression, not production or cutoff convergence.',csv='/code_fix_convergence.csv',claim='R4-R1')
    return plots

def build():
    content=json.loads((DIST/'content.json').read_text())
    audit=read('round6/code_audit.json')
    regressions=read('round6/code_regression_results.json')
    skeptic=read('round6/skeptic_checks_results.json')
    sources=[]
    for key,s in read('round5/guide_references.json').items():
        sources.append(dict(id=key,**s,use=s.get('role','')+' '+s.get('readdepth','')+' '+s.get('access','')))
    for s in read('round6/advisor_sources.json')['external']:
        sources.append(dict(**s,use=s['reading_scope']+' Does not establish: '+', '.join(s['does_not_support'])+'.'))
    documents={}
    for name in ['round5/theorem_advisor.md','round5/proof_critique.md','round5/research_bridge.md','round5/search_contract.md','round4/response_contract.md','round6/extensions.md','round6/advisor_plan.md','round6/advisor_experiment_contract.md','round6/code_audit.md','round6/skeptic_review.md','round6/experiment_readme.md','round6/advisor_experiment_review.md']:
        p=RESEARCH/name
        if p.exists(): documents[name]=p.read_text()
    sk_count=sum(c.get('passed') is True for c in skeptic['checks'])
    coverage=[ [c['file'],f"{c['line_count']} lines; {len(c['functions'])} functions",c['review']] for c in audit['coverage']]
    findings=[dict(id=f['id'],status=f['status'],title=f['title'],reproduction=f['observed']+' '+f['repro'],impact=f['impact'],fix=f['fix'],test='Covered by the named regression in the frozen code audit; full reproduction and source spans are in the audit notes.') for f in audit['findings']]
    rejections=[
      ['The exact integral maximum also bounds every finite grid','Two-node positive Gauss counterexample at a node; K=200 gives negative discrete Z','Rejected. Use a separate discrete coefficient certificate.'],
      ['A fixed-window gap proves joint cutoff removal','Exact harmonic/digamma identity and monotone cofinal argument','Rejected for unmodified fixed matching. Re-derive the common closure.'],
      ['Conserved signed δW is a positive tangent norm','Indefinite first variation and stationary-vacuum null/secular modes','Rejected. A new positive second variation exists only in stated transformed vacuum variables.'],
      ['A constraint identity supplies quantum stress','Strong-field stress and force Ward identity remain unclosed','Rejected. Directional stress, state and support sectors must be derived.'],
      ['A successful proof search certifies physics','Planner admits externally supplied Horn rules; old proof refs did not hash bytes','Rejected. New provenance guard binds evidence; theorem truth remains separate.'],
      ['Conservation alone proves physical charge matching','A consistently changed finite subtraction can conserve its own energy','Rejected. Keep independent low-field and matching tests.']]
    coefficient_review=read('round6/advisor_experiment_review.json')
    layers=[['Conditional mathematical proof','Finite continuation, coefficient bounds, forcing estimate, constraint identity, four restricted extensions','Conventional derivations under named assumptions; no formal kernel or novelty proof.'],
      ['Independent skeptical checks',f'{sk_count}/{len(skeptic["checks"])} checks pass; production solver not imported','Symbolic, exact rational, high-precision and small numerical tests; not an entire trajectory enclosure.'],
      ['Core code repair',f'{regressions["tests_run"]} new regressions; 24 unchanged compatibility tests; 16 symbolic checks (14 identities, 2 defect controls)','Small regression fixtures and selected static code scope; no exhaustive path coverage.'],
      ['Historical production response','512→1024 fixed-grid comparison passes; coarse pairs fail','Fixed K,N, prescribed state and sampled output times; not a continuum limit.'],
      ['Historical integrity','13 historical source/contract/result hashes match','Hashes bind bytes, not the physical truth of a calculation.'],
      ['New coefficient experiments','135 contracted integral comparisons; 29 independent advisor checks pass after seven defects were repaired','Finite quadrature and cancellation cases, including a=10³⁰; no all-input interval guarantee.']]
    experiments=[
      dict(id='E1',title='Exact coefficient and quadrature falsifier',status='Completed with counterexample retained',kind='check',cost='Small symbolic / integration task',hypothesis='The integral coefficient is maximal at a=0; a proposed transfer to a discrete maximum is tested separately.',forward='Exact primitive and positive even kernel.',backward='Show every derivative sign and independently evaluate the integral; test peak alignment with finite nodes.',method='Symbolic differentiation, adaptive quadrature, positive two-node adversary and fixed-window refinement.',reject='Reject the discrete transfer as soon as one admissible grid exceeds the integral maximum. Reject silent zero from cancellation.',decision='Integral theorem accepted; discrete transfer rejected; implementation corrected after advisor review.'),
      dict(id='E2',title='Uniform coefficient tail at fixed momentum window',status='Restricted theorem completed',kind='proof',cost='Exact rational / integral estimate',hypothesis='The Z>3/4 denominator bound survives every finite Landau cutoff at fixed b10,K20.',forward='Positive weights, original four-level rational bound and decreasing n⁻³ᐟ² tail.',backward='A global-a tail bound below the remaining 1/4 margin.',method='Integral comparison and exact Fraction arithmetic.',reject='If the upper bound reaches 1/4, this certificate cannot establish the target gap.',decision='Certificate passes. State/current/stress convergence still requires uniform physical ultraviolet tails.'),
      dict(id='E3',title='Joint cutoff removal with fixed matching',status='Uniform-gap hypothesis refuted',kind='rejected',cost='Analytic recurrence and monotonicity',hypothesis='The original positive-energy proof has a gap uniform when both K,N grow.',forward='Full-window harmonic sum and exact χ cancellation.',backward='Any claimed continuum passage must keep coefficient coercivity uniform, or use a different proof/closure.',method='Cofinal threshold argument, log-domain illustration, independent prefactor and index checks.',reject='Divergence of C refutes this uniform-gap claim. It does not by itself reject a combined renormalized current.',decision='Stop searching for a favorable cutoff plot. Next derive common regulated current, energy and stress under a physical matching condition.'),
      dict(id='E4',title='Stationary-vacuum positive response energy',status='Restricted theorem and checks completed',kind='proof',cost='Small exact matrix / matrix exponential',hypothesis='The electric tangent is bounded at exact stationary vacuum with transverse pure-state data and Z₀>0.',forward='Exact tangent equations and stationary preparation.',backward='A positive quadratic form in controlled variables with derivative 2uf.',method='Complete the second variation; check AᵀG+GA=0; retain the secular raw-tangent counterexample.',reject='Feedback sign or contact-term mutation must break the identity; a pumped base is outside the theorem.',decision='Electric/transformed response bound accepted. Full tangent stability rejected; pumped stability remains open.'),
      dict(id='E5',title='Common current and directional stress renormalization',status='Next physical obligation — not executed',kind='open',cost='Substantial analytic work before PDE solving',hypothesis='A declared regulator/state prescription can yield jointly finite current, energy and anisotropic stress satisfying the force Ward identity.',forward='Finite work identity, Bianchi constraint diagnostic, and the joint-cutoff obstruction.',backward='Need ρq,pq⊥,pq∥,Jq from the same effective prescription, external-source support and permitted counterterms.',method='First specify Hadamard/adiabatic state and subtraction order. Derive all variations from a common renormalized functional or equivalent covariant construction. Check ∇μTμν=Fνμjμ with explicit conventions.',reject='Reject if a regulator-dependent remainder cannot be removed by allowed common counterterms, or if current and stress use inconsistent matching.',decision='Do not evolve gravity or train a PINN until the closure, Ward identity and initial data are explicit.'),
      dict(id='E6',title='Pumped-base stability or a counterexample',status='Planned — no stability result yet',kind='open',cost='Bounded symbolic reduction, then small trajectory study',hypothesis='A time-dependent positive response energy may exist for a narrowly specified finite pumped base.',forward='Exact finite-time tangent and vacuum second-variation lemma.',backward='Need a controlled time-dependent symmetrizer and bounds on its derivative; signed δW is insufficient.',method='Derive the complete tangent matrix on the admissible subspace; search for a symmetrizer with explicit coercivity and a Grönwall bound; compare a held-out spinor variation.',reject='An unstable admissible mode, loss of coercivity, or unbounded coefficient integral blocks the desired bound.',decision='Treat counterexamples as information; do not tune the plot or source until the skeptic appears to lose.')]
    coverage_rooms=[
      dict(title='Math and physics foundations',href='#study',description='Arithmetic through calculus, linear algebra, differential equations, mechanics, electromagnetism, relativity and quantum theory. Prerequisites, practice and derivations live in each chapter.'),
      dict(title='Sound, geometry and the sky',href='#explore',description='Sound and waves, geometry and sacred-geometry history, astrophysics and astronomy have dedicated study rooms. Mathematical structure is distinguished from metaphysical claims.'),
      dict(title='Newton, Einstein and Tesla',href='#pioneers',description='Primary-work guides and historical context. Newton’s alchemical/theological interests and Tesla’s unusual proposals are treated as historical evidence, not established supernatural mechanisms.'),
      dict(title='Patents and unusual claims',href='#patents',description='Organized patent and claim investigation, with physical assumptions and evidence checks. A patent, government project or famous author does not verify performance.'),
      dict(title='Calculators and recorded experiments',href='#laboratory',description='Learning calculators expose assumptions and derivation steps. Research calculators, recorded fields and response tests use separate model contracts and documented controls.'),
      dict(title='The four unresolved interfaces',href='#research/evidence',description='Festina Lente / WGC, strong-field curved-space pair creation, Cauchy-horizon instability, and photon–graviton mixing remain research frontiers. The reduced model does not solve them.')]
    features=[
      dict(title='Result pages',href='#research/solutions',use='Read one claim completely, from definitions to objection.',inspect='Assumptions, exact equations, derivation, tests and the next missing premise.'),
      dict(title='Skeptic and code audit',href='#research/audit',use='See reproduced failures and the scope of fixes.',inspect='Affected inputs, source spans, test names and unchanged historical evidence.'),
      dict(title='Theory connections',href='#research/proof-map',use='Follow prerequisites and backward proof obligations.',inspect='Edge type: an unresolved bridge or analogy is not an implication.'),
      dict(title='Recorded fields',href='#research/results',use='Inspect the archived baseline and download its samples.',inspect='Finite cutoffs, source work, units and model exclusions.'),
      dict(title='Response test',href='#research/response',use='Compare field/current tangents and historical diagnostics.',inspect='Source preparation, finite-difference family and fixed-grid convergence.'),
      dict(title='Research calculators',href='#research/demonstrations',use='Vary reduced mixing, source-budget and detector formulas.',inspect='Assumptions and parameter domain; these calculators are not the coupled quantum-gravity solver.'),
      dict(title='Sources and paper discovery',href='#research/sources',use='Read versioned source records; use the Papers area for recent discovery.',inspect='Reading depth, original source, version and what it does not establish.'),
      dict(title='Next experiments',href='#research/next',use='Review a falsifiable hypothesis before running it.',inspect='Forward evidence, backward obligations, rejection rule and cost.'),
      dict(title='Study progress and backup',href='#study',use='Follow the learning chapters and export the local notebook.',inspect='Progress lives in browser storage; use Export backup to retain your notes.')]
    for c in claims:
        if c['id']=='R5-G1':c['sources']=['D014','D035','D037']
        if c['id']=='R5-P1':c['sources']=['D007','D008','D010']
        if c['id']=='R3-M1':c['sources']=['D041','D044']
        if c['id']=='R4-R1':c['sources']=['D001','D042','D043']
    hub=dict(round=6,date='9 September 2026',claims=claims,documents=documents,sources=sources,
      map=read('round5/theory_map.json'),plots=make_plots(),
      validation=dict(skepticChecks=sk_count,codeTests=regressions['tests_run'],layers=layers),
      audit=dict(scope=audit['scope'],coverage=coverage,findings=findings,rejections=rejections,coefficient_review=coefficient_review),
      coverage=dict(chapters=len(content['chapters']),resources=len(content['resources']),specialisms=len(content['specialisms']),rooms=coverage_rooms),
      features=features,experiments=experiments,
      connections=[['Finite physical modes + coefficient gap','R6-L2: every finite N at fixed K inherits a gap','Uniform energy/state/current/stress tails are still missing for an infinite-mode limit.'],['Positive continuous kernel','R6-L1: exact finite-window maximum','Discrete quadrature needs a separate certificate; a coarse counterexample blocks automatic transfer.'],['Harmonic full-window coefficient + fixed χ','R6-L3: no cofinal uniform positive gap','A common renormalized closure must be derived before passing to joint cutoff removal.'],['Finite tangent + exact stationary vacuum','R6-L4: positive second variation in (u,ξ)','Pumped stability, raw-tangent boundedness and quantum noise do not follow.'],['Force Ward identity + source support','R5-G1: Einstein constraint propagation','The strong-field quantum directional stress remains an open calculation.']])
    # Bind independent verdicts as data as well as readable notes.
    p=HERE/'claim_verdicts.json'
    if p.exists():hub['independentVerdicts']=json.loads(p.read_text())
    (DIST/'research-hub-data.js').write_text('window.OBSERVATORY_HUB = '+json.dumps(hub,ensure_ascii=False,allow_nan=False)+';\n')
    (DIST/'research-map.json').write_text(json.dumps(hub['map'],ensure_ascii=False,indent=2)+'\n')
    for name in ['finite_geometry.csv','quadrature_refinement.csv','tail_behavior.csv']:
        shutil.copy2(HERE/'plot_data'/name,DIST/name)
    shutil.copy2(HERE/'code_fix_convergence.csv',DIST/'code_fix_convergence.csv')
    (HERE/'homepage_claims.json').write_text(json.dumps(claims,ensure_ascii=False,indent=2)+'\n')
    print(f'Bound {len(claims)} dedicated result pages, {len(documents)} documents and {len(hub["plots"])} plots.')

if __name__=='__main__':
    build()
