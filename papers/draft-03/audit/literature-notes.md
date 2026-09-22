# Literature audit notes

Date: 22 September 2026. Owner: literature/novelty audit only. No tests or physics loops were run for this task.

## Local records inspected

The audit read the round-25 historical ledger (`research/round25/all-results.json` and `ALL_RESULTS.md`), round-26 `SOURCES.md`, round-25 `sources.json` and `RESONANCE_AND_HISTORY.md`, the Newton/Tesla method README, and selected source manifests/reading notes from rounds 10, 11, 12, 14, 15, 20, 21, and 23. Paths are relative to `yang_mills_workbench/`. Fresh online inspection is distinguished from these inherited records in the source review.

The JSON ledger has 23 rounds (3–25), 111 runs, 35 studies and 76 physics loops, matching its declared counts. The per-round run counts are 4, 2, 3, 4, 3, 3, 3, 3, 3, 3, 4, 2, 6, 2, 6, 6, 6, 10, 10, 10, 6, 10, 2. Round 26 must be reported separately. The ledger is historical evidence, not proof that every archived computation was independently reproduced in this paper-writing task.

## Material corrections and guardrails

1. **One-plaquette reduction is prior art.** The inspected D’Andrea/Bauer/Grabowska/Freytsis preprint explicitly reduces the physical single-plaquette radial equation to Mathieu form. The workbench should emphasize its explicit certificates and normalization, not claim to invent the reduction.
2. **Unbounded block diagonalization is real prior work.** The finite-dimensional hypotheses of arXiv:2007.07667 cannot be generalized to the entire literature: arXiv:2108.13907 treats separable onsite spaces and relatively form-bounded interactions. Importing it still requires a domain/form/geometry dictionary and quantitative smallness analysis. “No rotor theorem exists” is unsupported.
3. **Local stability is not arbitrary gap stability.** Henheik–Teufel–Wessel Theorem 3 concerns distant ground-state effects and permits a local perturbation that closes the global gap.
4. **A locality bound must match its interaction norm.** Radius decay of a correction supported on a filled square does not establish an exponential support-cardinality norm. Failure of an upper-bound budget does not prove the actual operator norm diverges. Stronger volume-tail literature remains a prospective lead under different onsite hypotheses.
5. **Domains and time topology remain explicit.** Operator-norm convergence of bounded J_n does not in general imply norm convergence of [J_n,G] for unbounded G. Strong/weak operator calculus and spatial norm limits must not be relabeled full-algebra point-norm time continuity.
6. **Computed heat is an additional certificate.** A positive retained-center error δ produces exp(δt) drift in the ground mode. An arbitrarily accurate nonzero center therefore does not supply an all-time absolute error guarantee by itself. A rigorous repair uses a finite-time spectral evaluator with interval center/residual/rounding budgets and a late-time ground-projection branch with certified projection error and decaying-tail bound. Relative guarantees additionally require a nonzero output floor. These are elementary consequences to be supported by the local proof, not new literature theorems.
7. **Static, Markov, and physical-time gaps differ.** The strong-coupling stochastic paper is not a theorem identifying its Langevin generator with the canonical Kogut–Susskind Hamiltonian.
8. **OS reconstruction needs the full hierarchy.** Reflection positivity alone is insufficient. The 1975 article explicitly repairs a regularity gap in the earlier formulation; use the corrected regularity/growth hypotheses.
9. **Historical external-formula criticism is versioned.** Round 12 audited particular formulas under frozen conventions. The currently inspected arXiv:2608.05415v1 identifies formal continuum and closure steps. Before making a public paper-error claim, match the historical bytes/equations and cite the precise counterexample. No new reproduction was undertaken here.
10. **No priority conclusion.** This is a selected comparison of relevant methods. The candidate increment consists of particular graph calculations, complete budgets, and explicit scope counterexamples. Establishing scientific novelty requires a narrower claim and a dedicated priority search.

## Bibliographic decisions and access limits

- `bauer2023basis` preserves the identifier already supplied to the manuscript team, but uses the verified final record: Irian D’Andrea, Christian W. Bauer, Dorota M. Grabowska, Marat Freytsis, *New basis for Hamiltonian SU(2) simulations*, Physical Review D 109, 074501 (2024), DOI 10.1103/PhysRevD.109.074501. Equation locations refer to arXiv v1, whose title/author order differ.
- Kogut–Susskind metadata and abstract were inspected at the publisher. The original full text was unavailable through the tool; no claim of a full original-paper reading is made. Open formula provenance is supplied separately by the 2023 preprint.
- Osterwalder–Schrader II was inspected as an original-article PDF from a mirror; the official Project Euclid URL and DOI are retained. OCR was not trusted to transcribe the precise growth formula, so the review names the required condition and inspected location.
- Teschl and NIST DLMF are authoritative mathematical references, not the original historical publications of theorems or special functions. They are used for checkable statements, not priority attribution.
- Jaffe–Witten is cited as the official problem description without an unverified publication year or book pagination.
- Unverified journal metadata for preprints was omitted. The two historical references are primary texts, with a deliberately limited methodological role.

## Additional sources inspected but not needed in the focused bibliography

- Yarotsky, *Ground states in relatively bounded quantum perturbations of classical lattice systems*, arXiv:math-ph/0412040; Communications in Mathematical Physics 261, 799–819 (2006), DOI 10.1007/s00220-005-1456-9. Relevant broader stability context; the focused review uses the more directly matched product-vacuum source.
- Zhu, Argentati and Knyazev, *Bounds for the Rayleigh quotient and the spectrum of self-adjoint operators*, arXiv:1207.3240; SIAM Journal on Matrix Analysis and Applications 34(1), 244–256 (2013), DOI 10.1137/120884468. Supplementary residual-bound lead; Teschl’s exact inspected Temple statement suffices for this draft.
- Osterwalder–Schrader I, Communications in Mathematical Physics 31, 83–112 (1973), DOI 10.1007/BF01645738: historical predecessor. The focused bibliography cites the inspected 1975 correction rather than treating the earlier statement as unqualified.

## Files supplied

`sources/references.bib` has 24 focused entries. `sources/literature-review.json` records the exact inspected locations, theorem assumptions, contribution relationship, limitations, and stable URLs. `sources/literature-review.md` is the human-readable review. These files add no physics gates and change no historical result status.

## QED addendum for early-section integration

Three entries were added after the initial 21-source review. Fresh readings were matched to FT02, C03 and H04 in `evidence/qeg-research/round3/references.json`. The final count is 24. `mages2010euler` covers constant-field susceptibility and its explicit finite subtraction; `kluger1993pair` covers the homogeneous mean-field initial-value problem and separate scalar/spinor adiabatic current calculation; `zahn2014dirac` covers local covariance, current ambiguity, and restricted stress-conservation analysis. None is cited as an evaluated strong-field Bianchi-I current/pressure closure or an exact interacting-QED solution. The selected passages, not complete proofs or numerical reproductions, were checked.

Two bibliographic dates differ from the historical ledger: Kluger et al. was published in 1993 and posted to arXiv in 2003; Zahn’s final journal record is 2014, while arXiv v3 is dated 2013. Those are source-date clarifications, not changes to the historical run status. All new keys were supplied to the early-section writer.
