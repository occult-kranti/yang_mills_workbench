# Contributions and scientific novelty

This round separates **new results in this workbench** from **new results in the literature**. Scientific priority is unverified. None of the contributions is a solution to the four-dimensional Yang–Mills mass-gap problem.

## Closest checked prior work

* Nachtergaele–Sims, [arXiv:1410.8174v1](https://arxiv.org/html/1410.8174v1): strong operator evolution with unbounded onsite generators. This is an inherited mathematical framework, not a workbench invention.
* Ekert et al., [quant-ph/0203016](https://arxiv.org/abs/quant-ph/0203016): controlled-unitary interferometry for state functionals. The V readout applies this established primitive to the specific U observable; it does not invent interferometric estimation.
* Tong et al., [arXiv:2110.06942v2](https://arxiv.org/html/2110.06942v2): rigorous state and Hamiltonian truncation with assumptions on local quantum-number growth. Any truncation certificate here must distinguish its target, norm, finite graph and constants from this stronger existing literature. No priority claim follows from a new cutoff symbol.

Detailed reading limits are in `advisor/primary-reading.json` and the producer reports. A located source is not automatically a fully checked theorem application. Historical Newton/Tesla sources were reviewed in the inherited project studies; the modern proof arguments remain separate.

## Claim categories

**Known method applied:** finite spectral measurement, norm continuity of bounded correlators, controlled-unitary readout, positive filter averages, spectral cutoffs and residual estimates.

**Project-specific derivation:** a complete certificate for this workbench's explicitly named model and observable, admitted only after its paired proof and skeptical review.

**Obstruction:** a proved failure of a specified route or certificate. It is not failure of every alternative method or failure of Yang–Mills itself.

**Conditional result:** a conclusion with named premises still requiring a physical implementation or an all-stage proof. Such premises are not silently treated as solved.

Each loop page and gate gives its final category, supported equation, strongest limitation and next premise. No fitted variable, historical analogy, arbitrary constant or scalar upper-bound failure is promoted into a new physical law.

## Reviewed contributions through X2

| Loops | Contribution in this workbench | Known ingredient and actual limit |
|---|---|---|
| V1 | Exact three-outcome spectral measurement for the fixed U observable; two-model correlation loss at most `8 delta+4 delta^2`; full-local-Haar Wilson-multiplier distance at least `1/2`. | Spectral measurement and operator-norm continuity are standard. The compact/multiplication obstruction is a norm-space-specific argument, not a Wilson-observable endpoint theorem. |
| V2 | Actual `||[H_q,W]|| <= alpha(9/2+eta/4)`; complete coherent readout and two explicitly different confidence/error conventions. | Controlled interferometry and concentration bounds are standard. The checked sufficient budget is `3.24e22` preparations and assumes extraordinary timing/control precision. No implemented experiment or optimal lower resource bound is claimed. |
| W1 | The actual indexed source has `h[v]=14 tau^2` and a positive retained filter residual `||R_Theta(A)|| >= (311/1664)||w||`. | Form comparison, spectral calculus and covariance monotonicity are known tools. The stronger exact-moment refinement originated in reverse reconstruction and passed separate review. It is not attributed as an independently duplicated discovery. |
| W2 | Exact residual retention at every step; vacuum-column graph convergence and fixed finite-volume strong convergence to spectral diagonal blocks. | Averaging and spectral decomposition are standard. Actual equal-energy blocks, full-source norm closure, infinite-volume all-sector closure and later-diagonal induction remain unproved. |
| X1 | Two distinct rigorous truncation bounds and an explicitly assembled common 21-state physical sector with actual spin-one leakage. | Gauge-compatible Peter-Weyl/Galerkin truncation is established. The larger certified cutoffs were not assembled; the kinetic/full-input and degree/retained-input results cannot be interchanged. |
| X2 | Complete 210-channel residual with norm factor `195/4`; certified true ground enclosure and a computed 21-state heat approximation with full-space error below `0.000085` for all admitted couplings and `sigma>=5`. | Variational, Temple and spectral projection methods are standard. The exact electric moment `295` and sharper variational improvement were forward-origin refinements separately reviewed. The finite graph's small error does not imply a continuum or homogeneous mass gap. |

The parameters in these certificates are defined in [PARAMETERS.md](PARAMETERS.md). They expose approximation errors and missing hypotheses; they do not fill a physical gap by inserting an arbitrary constant. Later loop contributions are added only after their reviews.
