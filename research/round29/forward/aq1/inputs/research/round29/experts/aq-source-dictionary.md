# AQ primary-source placement dictionary

Status: source placement for the panel-selected AQ goal. **No independent new proof, simulation or research loop is claimed.** The exact selection file hash is recorded in `aq-source-dictionary.json`.

## Source and prior-strategy boundary

Gauvin supplement A.10, ppS6–S8, is the closest explicit prior construction: compactness, dynamics, GNS implementation, gauge averaging and Fourier gap passage. This strategy retains that attribution. The proposed contribution is an actual SU(2) selected-strip application at AM2’s numerical cap. Pure-electric SU(3) link-energy estimates and constants1/648,2a/3 and8a/3 are not transferable.

Nachtergaele–Sims1410.8174v1, Section3 setup and Theorem4.1, and Nachtergaele–Sims–Young1810.02428v2, Theorems3.3–3.5, are the primary dynamics references. They distinguish local norm convergence as volume grows from continuity as time varies. NSY7.6 is not a direct rotor gap-transfer theorem. Exact reading depths are preserved in `sources.json`.

## Hypothesis dictionary

| Source object | Actual model placement | Obligation to retain |
|---|---|---|
| Countable metric lattice and full local algebras | The frozen coarse-site set Gamma (specified orthant or full-lattice exhaustion), l1 metric, H_b=L2(SU2^24), A_R=B(tensor_R H_b). Quasi-local algebra is norm closure of these full local B algebras. | Freeze Gamma/exhaustion; physical fixed algebra is imposed after the unreduced factor construction. Do not assume physical tensor-factorization. |
| Selfadjoint onsite Hamiltonians | Actual shifted selected-strip reference h_b, including the ten selected-strip links and fourteen free links of the complete factor; compact resolvent and unique reference vacuum. Physical onsite energy is delta h_b, delta=alpha/8. | This is not the pure-electric Haar onsite operator used by Gauvin. Domains and offsets remain the actual I1 objects. |
| Bounded interactions Phi(X) | Whole-star grouped omitted interaction on S={0,e_x,e_y,e_z}, diameter2; normalized per-star norm<=7\|tau\| and per-site incident sum J<=28\|tau\|. | Retain every anchor incidence and original omitted face; do not use a three-block or fine-vertex dictionary. |
| F-function placement | Candidate F(r)=(1+r)^-4 on the3D coarse lattice. The source convolution split gives finite convolution control; support diameter2 gives candidate F-norm ceiling81J in normalized units. | Producer must check actual geometry/incidence and F placement; this table is not a separately executed proof. A finite F-norm needs no additional small-coupling radius. |
| Time and energy units | Either apply source dynamics to normalized h at s=delta*t/hbar, or to physical frequency generator H/hbar, scaling onsite and Phi by delta/hbar. | An AM2 normalized gap1/2 means physical energy alpha/16, or frequency alpha/(16hbar). Do not mix conventions or use Gauvin8a/3. |
| Local compactness | Use the actual reset estimate for Tr(rho_Lambda,R h_R), h_R=sum_R h_b, with all incident groups charged. Compact resolvent yields finite-rank local spectral cutoffs and trace-norm precompactness. | Not an assumed pure-electric link-energy bound. No imported4\|S\|b/a estimate, no vacuum substitution, no extensive-volume energy bound. |
| Norm thermodynamic limit | For each fixed bounded local A, finite-region dynamics converge in operator norm uniformly over compact times. Extend by isometry to the quasi-local algebra. | This compares volume cutoffs. It does not say t->alpha_t(A) is norm-continuous on all full-B local observables. |
| GNS implementation and strong time continuity | Build an invariant locally normal subsequential state, then obtain Hilbert-space strong continuity using normal local densities, finite-region strong time continuity and compact-time uniform dynamics approximation. | Invariance, continuity and Stone generator are separate obligations; do not skip them by citing norm volume convergence. |
| Physical sector | Implement original endpoint SU2 gauge actions, prove strong continuity in the compact product group, average to the fixed sector and show local invariant vectors are dense there. | All original endpoint actions and gauge-invariant onsite/reference structure must remain intact. |
| Gap passage | Transfer centered bounded-local physical correlation spectra using an explicit Fourier-test argument at the AM2 cap; retain moving means and physical clock. | No automatic moment/domain equality; no use of NSY7.6 as a rotor gap theorem. Show a nonzero physical fluctuation and distinguish GNS vacuum simplicity from uniqueness of all ground states. |

## Saved and bound primary reading packets

Full primary PDFs and selected-page text packets are available in the shared temporary reading directory. The repository stores their URLs, byte hashes and exact selected pages in `aq-primary-bindings.json`. A saved packet includes surrounding context; it does not mean every assertion on those pages was independently proof-audited.

- nsy-2019: /tmp/ym29-source-read/nsy-2019.pdf; selected text /tmp/ym29-source-read/nsy-2019-reading-extract.txt. PDF pages 4,24,25,26,27,28,83,84,85,86. PDF SHA-256 `42fc3029fa582f14a01f858463f481d5cacf21ed785791d32c72dd9df97f66cd`.
- ns-2014: /tmp/ym29-source-read/ns-2014.pdf; selected text /tmp/ym29-source-read/ns-2014-reading-extract.txt. PDF pages 6,7,8,11,12,13. PDF SHA-256 `501af040512f2bdb62344ecbd093664e79ad1861338eabbce2c9791fca4e2fba`.
- gauvin-a10: /tmp/ym29-source-read/gauvin-supp.pdf; selected text /tmp/ym29-source-read/gauvin-a10-reading-extract.txt. PDF pages 6,7,8. PDF SHA-256 `dc0d5e590e3989bb421bcf55449f0216a1653b2832d3169e740e33a3a5af6a5d`.

The local-normal state may be subsequential. Do not assert old-state identity, whole-sequence convergence, boundary uniqueness, evaluated HTW constants, translation invariance or a continuum construction without separate arguments. Physical-sector vacuum simplicity, if established, is not uniqueness of every thermodynamic ground state.
