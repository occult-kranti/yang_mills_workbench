# Round14: three research roles, two executed feedback loops

This round studies an explicitly deformed finite SU(2) Euclidean measure. It does not solve the four-dimensional Yang–Mills existence and mass-gap problem. No mathematical novelty is claimed for the underlying group integration, cumulant or Taylor techniques.

The advisor–skeptic freezes the model and accepts evidence. The forward researcher derives from the Haar integral and produces computations. The backward researcher reconstructs the required arithmetic through characters and exposes missing spectral premises. Loop2 starts after the recorded Loop1 gate; it addresses the failed sign target at `(k1,k2,eta)=(1,1,1/4)`.

Read the [team graph](https://occult-kranti.github.io/yang_mills_workbench/#research/team-map), [Loop1 derivations](https://occult-kranti.github.io/yang_mills_workbench/#research/team-loop1), [Loop2 certificate](https://occult-kranti.github.io/yang_mills_workbench/#research/team-loop2), and [forward/backward roadmap](https://occult-kranti.github.io/yang_mills_workbench/#research/team-roadmap).

## Equations and evidence

Use normalized Haar on `SU(2)^2`, with `x=Tr(U)/2`, `y=Tr(V)/2`, `z=Tr(UV)/2` and density proportional to `exp(k1*x+k2*y+eta*z)`. The eta term changes this finite action. It is not a physical mass. At eta0 the specified open-planar Wilson baseline factorizes.

The first loop derives the exact conditional marginal, `C'(0)=v1*v2`, and `|C''|<=7` for the covariance `C`. It also derives the solvable slice `C(0,0,eta)=u(eta)/4`. Existing exact variance evidence proves a small-deformation sign range. The sufficient estimate is inconclusive at the selected eta1/4 point.

The second loop uses rational Taylor polynomials and a geometric exponential remainder, with `Z>=1` and full signed normalization errors. The forward Haar moments use quaternion coordinates; independent reconstruction uses SU(2) character convolution. Inspect `central-certificate.json` for exact endpoints and `advisor/loop2_gate.json` for final scope and source bindings. Floating comparisons remain diagnostics.

## Launch website locally

From the repository root:

```bash
python3 start.py --no-browser
```

Open `http://127.0.0.1:8001/#research`. To preview the GitHub Pages base path, use the root README's Pages preview command. Static hosting does not execute scientific Python code. No API key is required by the site or solvers.

## Reproduce both scientific loops

Python3.11 or newer is required. Install the repository's scientific requirements for NumPy/SciPy numerical comparisons. Exact certificate generation and independent replay use the standard library. Run the following from the repository root. Generated reruns are separate from frozen historical outputs.

```bash
python3 research/round14/forward/test_forward.py --output research/round14/rerun/forward1
python3 research/round14/backward/oracle.py research/round14/rerun/backward1
python3 research/round14/forward/test_loop2.py --output research/round14/rerun/forward2
python3 research/round14/backward/verify_certificate.py research/round14/forward/loop2_output/certificates.json research/round14/forward/loop2_certificate.py research/round14/rerun/backward2
python3 research/round14/backward/review_advisor.py research/round14/advisor/advisor_checks.py research/round14/rerun/advisor-review
python3 research/round14/proof_routes.py --output research/round14/rerun/proof_results.json
python3 research/round14/test_proof_routes.py --output research/round14/rerun/proof_adapter_tests.json
```

Create the `rerun` directory before running an individual command whose output is a file. Replace `python3` with `py -3` on Windows. Use `python3 -O` for the recorded optimized-mode validation; acceptance checks must not disappear when assert statements are disabled. Rerunning in two modes does not create two independent scientific reviews.

For one exact computation without scientific dependencies:

```python
import sys
sys.path.insert(0, "research/round14/forward")
from loop2_certificate import certify, verify
c = certify("1", "1", "1/4", degree=24)
verify(c)
print(c["enclosures"]["covariance"])
print(c["width"])
```

The producer API supports its explicitly bounded rational parameter/degree domain; inspect `loop2_certificate.py` rather than interpreting an implementation cap as a mathematical restriction. Never coerce a Boolean into a degree. The independent verifier takes the actual producer source SHA and recomputes all fields; editing a certificate's status cannot make it pass.

## What the proof planner does

`proof_search.py` is the unchanged reviewed historical finite ground-Horn planner. `proof_routes.py` validates source-bound evidence before admission, explores both fronts, then checks the ordered route with a separate verifier. The two finite positive routes and the premise-withdrawal failures are recorded in `proof_results.json`. Rule search organizes conventional mathematical proofs; it is not a formal proof-assistant kernel or a search over every possible Yang–Mills argument.

The code replays exact evidence inside library construction rather than trusting an externally supplied pass record. Rule semantics are immutable and revalidated. The complete source fingerprint is checked. The original admission bypass and mutable-rule failures are retained in `history/` and the independent review history.

`proof_manifest.json` intentionally binds reviewed bytes. A mismatch stops replay. Do not automatically regenerate it to turn a stale review into a pass. Source modifications require a new independent review and explicit advisor gate before packaging.

## Structure and limitations

- `advisor/`: protocol, two gates, source audit and formal/transfer checks.
- `forward/`: both loop implementations, recorded comparisons, rational certificates and retained failures.
- `backward/`: independent character oracle, exact verifier, advisor and adapter reviews.
- `central-certificate.json`: unchanged selected certificate from the complete collection.
- `next-roadmap.md`: complete next-step obligations and rejection criteria in both directions.
- `proof_results.json`: actual search frontiers, meetings and ordered proof evidence.
- `site-validation.json`: interface checks, with their browser limitation.
- `vendor/`: exact earlier variance checker and certificate collection used in the transfer.

Source ledgers distinguish full derivations, theorem passages, metadata-only reading and access limitations. The numerical stability threshold remains unevaluated. A static moment countermodel blocks an unsupported generator inference. No matched continuum limit, physical mass gap or formal-kernel proof is claimed. Browser layout and keyboard behavior remain unverified; code-level routing and data checks are reported separately.
