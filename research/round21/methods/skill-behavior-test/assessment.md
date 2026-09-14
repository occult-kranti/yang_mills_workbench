# Bounded Round19 C2 publication check

**Verdict: the narrow mathematical result is supported by fresh exact replay, but the inherited complete release gate is broken. These are different verdicts.** No historical gate, repository source, or external destination was changed.

The installed `paired-physics-research` skill and its admission/matching and reconstruction/interval lessons were applied. The relevant rule is explicit: an inherited inventory requiring an uncommitted interpreter cache remains a failed gate. A direct calculation can support the mathematics without repairing release admission.

## Original reproduction failure

The original guide is `research/round19/README.md`, headed “Reproduce the complete six-loop checkpoint.” Its command was attempted with a fresh output path, adding `-B` only to prevent repository cache writes:

```bash
python3 -B research/round19/reproduce.py --through c2 --output /workspace/scratch/82ba53fe7aca/skill-check-round21/original-reproduction
```

It exited 1 during inventory verification, before any requested calculation ran:

```text
ValueError: missing gate file: backward/c2/history/pre-round20-validator-audit/__pycache__/compare.cpython-312.pyc
```

The C2 gate has 65 entries. Its other 64 entries exist and match their recorded hashes. The missing cache is not Git-tracked. Its recorded expected SHA-256 is `ca7c11234bc4224161caa1eb442e1cacb731c109a832e208025c5a184bee6cca`. The original gate SHA-256 is `051629385aeb19476662ce2363617c26072519695aa2519358b39d19f565223c` and remained unchanged after this check.

The failure was also reproduced from files extracted from Git commit `89c1afb5ec2605112db18b4be7350661d54d1c52`, using only the Round19 tree:

```bash
git archive --format=tar 89c1afb5ec2605112db18b4be7350661d54d1c52 -- research/round19
python3 -B /workspace/scratch/82ba53fe7aca/skill-check-round21/git-tree/research/round19/reproduce.py --from-loop c2 --through c2 --output /workspace/scratch/82ba53fe7aca/skill-check-round21/git-tree-reproduction
```

The archive was saved and extracted under the assigned check directory. The `--from-loop c2` option still verifies all preceding dependency gates, as required by the unchanged reproducer; it encountered the same missing C2 cache. Earlier studies were not rerun or re-audited.

## Mathematical evidence actually rerun

Python 3.12.14 was used, with bytecode writing disabled. Unmodified forward and backward C2 scripts were run into fresh external directories. The original comparator was then run against the fresh forward outputs; it executes a fresh backward reconstruction itself. The normal and optimized paths both completed, and a normal Git-tree reconstruction also completed.

| Execution | Result |
|---|---|
| Original complete reproduction command | Failed in inventory verification |
| Direct forward C2, normal and optimized | Passed; all 9 declared output files byte-identical to accepted output |
| Direct backward C2, normal and optimized | Passed; all 8 declared output files byte-identical to accepted output |
| Direct comparator, normal and optimized | Accepted; 34 checks, including 27 mutation controls; no admission failures |
| Git-tree original gate command | Same missing-cache failure |
| Git-tree direct forward C2 | Passed; all 9 declared output files byte-identical |
| Git-tree comparator and its backward reconstruction | Accepted; 34 checks and 27 controls; all 8 backward output files byte-identical |

Exact attempted Python argument vectors, exit codes, captured output and elapsed times are in `attempts.json`. Copyable commands are in `commands-attempted.sh`. The Git archive command and commit binding are in `git-tree-extraction.json`. These commands are a record of executions; the output paths now contain evidence and must be changed to fresh paths for another run.

The important direct commands were:

```bash
python3 -B research/round19/forward/c2/check.py --output /workspace/scratch/82ba53fe7aca/skill-check-round21/direct-forward
python3 -B research/round19/backward/c2/check.py --output /workspace/scratch/82ba53fe7aca/skill-check-round21/direct-backward
python3 -B research/round19/backward/c2/compare.py --producer research/round19/forward/c2/check.py --evidence /workspace/scratch/82ba53fe7aca/skill-check-round21/direct-forward --output /workspace/scratch/82ba53fe7aca/skill-check-round21/direct-comparison
```

The ordinary and optimized executions are repeats, not additional research loops or independent physical observations. The backward coefficient reconstruction uses the inherited C1 graph, character-fusion and conditional-sphere routines; it is not merely a comparison of stored final numbers.

## Supported statement and mathematical reasoning

For the declared finite, exterior-fixed, common-V Haar integral,

\[
F(\kappa)=\frac{E[Oe^{\kappa S}]}{E[e^{\kappa S}]},\qquad
S=3x+y+z+w+t,\qquad
O=\frac{(4x^2-1)^3(4w^2-1)}{81},
\]

the evidence supports

\[
F(0)=0,\qquad F(\kappa)\ge\frac{\kappa^2}{2048}
\quad (|\kappa|\le1/8),
\]

and

\[
F(\kappa)>F(-\kappa)\quad (0<\kappa\le1/64).
\]

Here x, y, z are normalized traces of U, V, W; w and t are normalized traces of UV-dagger and VW-dagger. All lie in [-1,1], so |S|<=7 and |O|<=1. The backward graph routine derives the seven affected face terms on the 18-vertex, 33-link, 20-face graph and retains the same V in both adjacent traces.

The recovered Taylor coefficients include N0=N1=0, N2=1/324, N3=13/1296, Z0=1, Z1=0, Z2=13/8 and Z3=1/4. The numerator remainder after degree 8 is bounded uniformly by E_K 7^9 |kappa|^9/9!, with a rational E_K >= exp(7K). At K=1/8 the exact positive coefficient C_N gives C_N/E_K approximately 0.0005887530023201035, exceeding 1/2048 by approximately 0.0001004717523201036. Because C_N>0, Z>0 and Z<=E_K, the denominator direction is valid. Zero is handled before division by kappa squared.

For the cross-difference D=N(kappa)Z(-kappa)-N(-kappa)Z(kappa), the leading coefficient is 13/648. Coefficient majorization bounds exact and retained factors by E_H. The two product errors are bounded by 4 E_H squared 7^9 |kappa|^9/9!. Dividing for strictly positive kappa and using kappa<=H produces a uniform remainder proportional to H^6, rather than dividing a fixed endpoint error by an arbitrarily small kappa. At H=1/64 the exact final lower coefficient is positive (approximately 0.020044909116843864).

The comparator reconstructs the rational exponential envelope, coefficient losses, tails and margin identities. Its executed controls reject an internally adjusted false E=1 envelope, an unsupported H=1000 asymmetry range, altered coefficients, incorrect denominator direction, missing zero-endpoint logic and other listed mutations.

At K=1/7 the degree-8 proof yields a weaker positive coefficient; at K=1/6 its numerator certificate is negative and therefore insufficient. This is not evidence that the actual integral becomes negative. The exploratory higher-degree probe is not an admitted wider theorem.

This is a reviewed analytic argument supported by exact arithmetic, not a proof-assistant formalization. It concerns a dimensionless static coupling with no identified physical clock. It establishes no homogeneous dense limit, Hamiltonian spectral gap, continuum Yang-Mills construction or Clay mass-gap result. Novelty/priority was not investigated by this bounded check.

## Required repair

1. Preserve the original C2 gate and its failed reproduction record. Do not delete its entry in place, generate a replacement cache, or describe direct replay as success of that original gate.
2. Create a separately identified, reviewed portable scientific inventory. Include the C2 contract, active forward/backward/checker/comparator sources, the executed C1 source dependencies, required input/output artifacts and advisor decision. Derive the required set from the execution/import structure, not only producer-provided manifest fields. Exclude interpreter caches and machine-local environment artifacts from this new inventory.
3. Record the explicit mapping from the old admission defect to the new inventory, with unchanged mathematical scope and source-byte changes, if any. Preserve historical source evidence relevant to the earlier validator correction as portable source rather than cache bytes.
4. Provide a reproduction entry point for the new inventory and declare the tested interpreter/dependencies (the present checked environment is Python 3.12.14, standard library).
5. Rerun and independently review the calculations, theorem-content controls and required output comparisons against the new inventory from a fresh Git-tree extraction. Only then give the repaired package a release-readiness verdict.

This check did not perform that repair and did not authorize a release. The mathematical result survived the attempted reproduction; the inherited packaging/admission claim did not.

## Reading depth and evidence location

The original Round19 reproduction guide, reproducer, C2 execution specification, frozen C2 contract, C2 gate, forward/backward C2 reports, C2 advisor decision, and C2 certificate/input/output/comparator code were reviewed. The backward C1 graph derivation and character/conditional moment-to-coefficient routines were read in depth because the actual C2 reconstruction executes them. Forward C1 imported coefficient/probe dependencies and accepted C1 artifacts were inspected where C2 uses them. Earlier full studies were not audited. No `research/round21` or other agents' current work was inspected.

`inspection-source-bindings.json` binds the principal reviewed files; it is explicitly an inspection record, not a replacement admission inventory. `c2-inventory-inspection.json` records the gate defect. `replay-validation.json` records byte comparisons, comparator results and final unchanged-gate confirmation. The Round19 Git status remained clean. All outputs are confined to this check directory.
