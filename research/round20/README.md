# Round20 — ten paired research loops

All five goals D–H are complete with two accepted research loops each. The inherited Round19 C2 interval certificate is also closed, after the independent validator was repaired to reject coherent false envelopes and interval claims. It is separate from Round20's ten-loop count.

The prominent contributions are:

- **E2:** a literal finite-box local-state limit across every upper-boundary phase for the specified summable, fixed-spacing strip model.
- **F2:** the exact shared-middle gradient equation, including the required observable r, and a gap bound for the explicitly conditional diffusion family.
- **H2:** the exact vacuum variance `||V_q Omega||²=alpha²tau(q)²B(q²)/96`, proving actual global ground-state return to the selected-strip reference while the perturbation operator norm remains nonzero on the canonical uniform-budget ray.

The [contribution audit](advisor/contributions-audit.md) separates model-specific derivations, established methods and proven limits. The [post-ten skeptic roadmap](advisor/post-ten-roadmap.md) identifies the next missing premises. It preserves Round13's qualitative homogeneous lattice stability result: H2 limits a global absolute-sum budget route, not every local-stability method. No physical clock calibration, new universal axiom or continuum Yang–Mills solution is claimed.

| Goal | First loop | Evidence-selected second loop |
|---|---|---|
| D | [D1](advisor/d1-gate.json): complete finite factors and exact resolvent tails | [D2](advisor/d2-gate.json): ground energies, projections and observables |
| E | [E1](advisor/e1-gate.json): aligned literal boxes and energy subtraction | [E2](advisor/e2-gate.json): all upper-boundary local-state limits |
| F | [F1](advisor/f1-gate.json): static law does not fix a clock | [F2](advisor/f2-gate.json): shared-middle derivative closure and conditional bound |
| G | [G1](advisor/g1-gate.json): local dynamics and continuity exception | [G2](advisor/g2-gate.json): full-factor limiting-state GNS |
| H | [H1](advisor/h1-gate.json): continuous profile and exact budget | [H2](advisor/h2-gate.json): exact variance and endpoint state |

G and H were chosen only after D, E and F completed their six loops; [the adaptive record](advisor/roadmap-after-first-three.md) binds that decision. Each second-loop contract depends on its first-loop gate. The [team and method record](methods/team-and-protocol.md) describes the independent formulations, shared premises and review limits. The double spiral organizes the investigation; its physical significance is still a hypothesis.

From the repository root, use fresh output directories:

```bash
python -B research/round20/reproduce.py --output /tmp/ym20-normal
python -B research/round20/reproduce.py --output /tmp/ym20-optimized --optimized
python -B research/round19/reproduce.py --from-loop c2 --through c2 --output /tmp/ym19-c2
```

The Round20 driver verifies every admitted file hash, runs both independent sources for each loop and compares reproduced scientific result bytes. [Final validation](validation-final.json) records forty ordinary/optimized source executions and ten fresh comparisons. A separately assigned mathematical reviewer completed another full replay and an independent polynomial, geometry and variance audit: [review](external-audit/report.md), [evidence](external-audit/audit-evidence.json). These checks are AI-agent review and exact computation, not human peer review or proof-assistant formalization.

The interactive review is generated from `site-data.json` and gate-verified evidence. It highlights the E2, F2 and H2 contributions together with their equations and applicability. Its [exception ledger](advisor/exception-ledger.json) retains failed premises and the repairs that changed the next loop. To rebuild and check routes:

```bash
python research/round20/build_site.py
node research/round20/site_test.mjs
```
