# Contributions and scientific novelty

This round separates **new results in this workbench** from **new results in the literature**. Scientific priority is unverified. None of the contributions is a solution to the four-dimensional Yang–Mills mass-gap problem.

## Closest checked prior work

* Nachtergaele–Sims, [arXiv:1410.8174v1](https://arxiv.org/html/1410.8174v1): strong operator evolution with unbounded onsite generators. This is an inherited mathematical framework, not a workbench invention.
* Ekert et al., [quant-ph/0203016](https://arxiv.org/abs/quant-ph/0203016): controlled-unitary interferometry for state functionals. The V readout applies this established primitive to the specific U observable; it does not invent interferometric estimation.
* Tong et al., [arXiv:2110.06942v2](https://arxiv.org/html/2110.06942v2): rigorous state and Hamiltonian truncation with assumptions on local quantum-number growth. Any truncation certificate here must distinguish its target, norm, finite graph and constants from this stronger existing literature. No priority claim follows from a new cutoff symbol.
* Burgarth, Facchi, Gramegna and Yuasa, [arXiv:2111.08961v2](https://arxiv.org/abs/2111.08961): an existing averaging/strong-coupling framework. The inspected Theorem 3 assumes bounded operators and finitely many distinct reference energies. It does not directly prove this workbench's infinite pure-point strong limit or its canonical endpoint statement; those obligations require their own argument.

Detailed reading limits are in `advisor/primary-reading.json` and the producer reports. A located source is not automatically a fully checked theorem application. Historical Newton/Tesla sources were reviewed in the inherited project studies; the modern proof arguments remain separate.

## Claim categories

**Known method applied:** finite spectral measurement, norm continuity of bounded correlators, controlled-unitary readout, positive filter averages, spectral cutoffs and residual estimates.

**Project-specific derivation:** a complete certificate for this workbench's explicitly named model and observable, admitted only after its paired proof and skeptical review.

**Obstruction:** a proved failure of a specified route or certificate. It is not failure of every alternative method or failure of Yang–Mills itself.

**Conditional result:** a conclusion with named premises still requiring a physical implementation or an all-stage proof. Such premises are not silently treated as solved.

Each loop page and gate gives its final category, supported equation, strongest limitation and next premise. No fitted variable, historical analogy, arbitrary constant or scalar upper-bound failure is promoted into a new physical law.

## Ten reviewed contributions

| Loops | Contribution in this workbench | Known ingredient and actual limit |
|---|---|---|
| V1 | Exact three-outcome spectral measurement for the fixed U observable; two-model correlation loss at most `8 delta+4 delta^2`; full-local-Haar Wilson-multiplier distance at least `1/2`. | Spectral measurement and operator-norm continuity are standard. The compact/multiplication obstruction is a norm-space-specific argument, not a Wilson-observable endpoint theorem. |
| V2 | Actual `||[H_q,W]|| <= alpha(9/2+eta/4)`; complete coherent readout and two explicitly different confidence/error conventions. | Controlled interferometry and concentration bounds are standard. The checked sufficient budget is `3.24e22` preparations and assumes extraordinary timing/control precision. No implemented experiment or optimal lower resource bound is claimed. |
| W1 | The actual indexed source has `h[v]=14 tau^2` and a positive retained filter residual `||R_Theta(A)|| >= (311/1664)||w||` for `0<|tau|<=5/1664`, `0<Theta<=1/16`. | Form comparison, spectral calculus and covariance monotonicity are known tools. The stronger exact-moment refinement originated in reverse reconstruction and passed separate review. It is not attributed as an independently duplicated discovery. |
| W2 | Exact residual retention at every step; vacuum-column graph convergence and fixed finite-volume strong convergence to spectral diagonal blocks. | Averaging and spectral decomposition are standard. Actual equal-energy blocks, full-source norm closure, infinite-volume all-sector closure and later-diagonal induction remain unproved. |
| X1 | Two distinct rigorous truncation bounds and an explicitly assembled common 21-state physical sector with actual spin-one leakage. | Gauge-compatible Peter-Weyl/Galerkin truncation is established. The larger certified cutoffs were not assembled; the kinetic/full-input and degree/retained-input results cannot be interchanged. |
| X2 | Complete 210-channel residual with norm factor `195/4`; certified true ground enclosure and a computed 21-state heat approximation with full-space error below `0.000085` for all admitted couplings and `sigma>=5`. | Variational, Temple and spectral projection methods are standard. The exact electric moment `295` and sharper variational improvement were forward-origin refinements separately reviewed. The finite graph's small error does not imply a continuum or homogeneous mass gap. |
| Y1 | Actual complete-factor collars and a full omitted-word tail uniform at the canonical endpoint; a fixed 98-link forward region retains a signal greater than `z/250` in liminf. | Connected-support localization and state norm transfer are known methods. The independent constructions use different retained-face conventions; finite spatial support still retains infinite spin spaces. |
| Y2 | For fixed eta in (0,1) and 0<z=C eta<=1e-6, the actual phase-removed canonical endpoint has a scalar limit, characterized by whole finite-region energy blocks and a uniform spatial tail. At `z=1e-6`, the disk centered at `1+i z/84` has radius below `1.89e-11`. | Strong averaging, energy pinching and uniform approximation are known methods. The actual scalar construction and sharper forward-origin disk were independently reviewed. The blocks and trajectory are unevaluated; no global operator-norm averaging or q=1 generator is claimed. |
| Z1 | Actual retained witnesses refute unrestricted all-time relative accuracy, despite a small absolute error. The exact-energy witness diverges; a computable Ritz-bright witness has true-relative error tending to one. | Spectral projection and denominator arguments are standard. Strict energy displacement and the actual vacuum row supply the model-specific ground-overlap fact. Generic nonzero leakage alone is insufficient, and zero coupling is an exact exception. |
| Z2 | Both directions independently compute the complete retained-to-omitted map with Gram `lambda^2(19I+J)/4`. Genuine early-time residual control joins a spectral bound to give all-time true-relative vacuum error below `0.00028` for every `0<=lambda<=0.01` and normalized retained radius-0.01 error below `0.00044`. | Duhamel, spectral estimates and overlap floors are standard. The actual map and continuous-coupling certificates are model-specific. Reverse's unnormalized radius-0.01 class has its own bound below `0.000720`; no unrestricted-input or growing-volume claim follows. |

The parameters in these certificates are defined in [PARAMETERS.md](PARAMETERS.md). They expose approximation errors and missing hypotheses; they do not fill a physical gap by inserting an arbitrary constant. Exactly ten new physics loops are reviewed: eight accepted within scope and two limited investigations. The next three goals are planned in the handoff and remain unexecuted.
