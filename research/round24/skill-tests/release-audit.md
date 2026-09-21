# Independent Round24 release-tooling audit

**Outcome:** the concrete defects found in the selected release checks were repaired by the root integrator and the targeted rejection controls passed. This is a tooling audit, not a completed ten-loop release certificate. It adds **zero physics loops and zero physics producer executions**.

The audit began with V1/V2/W1/W2/X1 reviewed and X2 running. It did not require the remaining gates to exist, launch new producers, alter reviewed evidence, or change the verifier. The auditor owns only this report. Temporary fixtures were removed automatically.

## Findings and repair verification

| Finding in the initial inspected source | Consequence | Repair and verification |
|---|---|---|
| `verify.py` replayed whichever gates happened to exist; the presentation test checked only ten rows. | Duplicated cards could conceal a missing gate while metadata claimed ten completed loops. | The verifier now supplies the exact ten IDs and checks the returned replay order. The builder and JS test require the exact ordered, unique ID list. Executing the current JS assertions rejects duplicated IDs and accepts the valid ordered fixture. |
| The Round24 test loaded the wrapper directly without inspecting the actual page entry point. | Its component checks could pass while the real site still loaded only Round23. | The test now requires the Round23 wrapper, Round24 data, Round24 wrapper, and app script exactly once and in order in both entry points. Current assertions reject missing and reversed scripts. The root explicitly deferred the real hookup until all ten loops are admitted; that is an intentional release-stage task. |
| `admission.source()` rejected a symlink only at the final file; output fences compared lexical paths. | An internal symlinked parent passed source validation; an external alias into the checkout passed the supposedly external output fence. | The original source-parent control was admitted. After repair, it is rejected. Running both real CLI entry points with an output alias into the checkout now fails at the output fence, before Git checks or producer execution, and creates no output. |
| The builder compared each card's verdict to its gate but did not bind its statement, equations, model, feedback, or limitations to a presentation review. | Unreviewed prose could appear beside an authentic gate hash. | The builder now requires a root-advisor presentation review binding the exact `contributions.json` bytes. An isolated component test changes a statement and removes its limitations after creating that binding; the current builder rejects it before generation. This test scopes the expected IDs to the five already reviewed rows solely to exercise presentation binding; it does not claim final release acceptance. |
| The receipt unconditionally reported scientific-figure visual inspection. The first repair allowed an empty figure file inventory. | The receipt could assert inspection without binding the inspected figure and its construction. | The verifier now requires the explicit inspection record plus the SVG, plotting source, and W1 gate entries. Executing the actual current figure-check AST accepts the existing record, rejects an empty inventory, and rejects a changed SVG hash. All three recorded hashes match. The visual inspection is the root advisor's attestation, not a new visual inspection by this auditor. |

The first two findings were reported before fixes. A temporary duplicate-card experiment was interrupted by the newly installed exact-ID guard and correctly rejected; it is not reported as a successful pre-fix end-to-end exploit. The initial source-symlink admission was directly reproduced. Other original defects were established by inspection of the recorded initial source.

## Integrity and historical-preservation assessment

The release verifier requires an expected committed tree, a detached clean checkout, the recorded baseline as ancestor, and no modification/deletion of historical research under `research/`. It also checks the named bound live guidance. Round23 reproduction remains explicit, now with its six-loop order and twelve executions checked per interpreter mode. Fresh site generation must reproduce the committed tree; the existing Round23/Round22/workbench/journey tests remain part of the release sequence.

The admission code requires contract-declared instruction and dependency bindings, exact submitted and reviewed payload equality, genuine Boolean control outcomes, the skeptical report, and the stated independent-model-agent attribution. Producer replay still compares both parsed payloads and exact output bytes. These checks support source integrity; they do not replace the mathematical reviews or establish the truth of arbitrary newly rebound source code. Presentation semantics are now explicitly assigned to a separate reviewed byte binding, without rewriting immutable gates.

No old research gates or sources were changed by this audit. The release comparison and historical replays were inspected, not run against the unfinished working tree. The revised negative controls above exercised the selected components only; the full verifier remains a future release gate.

## Concrete work remaining at the final release gate

1. After the authorized ten-loop program finishes, produce the final exact loop list, completion/stop metadata, and reviewed contribution text. Create its required `advisor/presentation-review.json` binding. This is pending work, not a defect in the current five-loop state.
2. Install the active Round24 entry-point scripts and regenerate both site trees only when the completion claims are true. The strengthened index checks will enforce the hookup at release.
3. Run the full verifier in its required fresh, detached, clean committed checkout, including both interpreter modes, exact replay inventories, fresh builds, and all site/history tests. No final-release pass is claimed here.

## Inspected source identities

Initial SHA-256 values, preserving the audit's original findings:

| File | Initial SHA-256 |
|---|---|
| `research/round24/release/verify.py` | `1349916a1f4dbcf50b27e650813a4e7f30bf5ea2f8f9e8e6a2ae8490c0969ef3` |
| `research/round24/admission.py` | `0f2b185b9efaeab71fd3977358b8a55f616f632de57e60a0c01a30d446a02cac` |
| `research/round24/build_site.py` | `1395dfb90f6e02cbad02d72251a85c999680bcdfe4002d5275b1bbce06619083` |
| `tests/test_round24.mjs` | `7a9528102910e8e781de81c4aad018aa4010134c465816e08ca739a11ca05711` |

Repaired versions last inspected during this audit:

| File | SHA-256 |
|---|---|
| `research/round24/release/verify.py` | `03c9410e3aa4b01762a8d00ed62dca7bc224cd2c576ccb3dc46396da9a92454b` |
| `research/round24/admission.py` | `8e8a997cb28d0741b555ce7f15bc65d9f47976c755e3dcfd8b432d075e5e6713` |
| `research/round24/build_site.py` | `faad1e3a4f201d7121efb1161f759d07d4adb309ba4d03b068af627970ae55ee` |
| `tests/test_round24.mjs` | `c7fff0e3867dd04ab95cd2bbe84cf2f3bee31749b084a35913acaac748c91fc3` |
| `research/round24/advisor/figure-review.json` | `897c383231d879ef4a741be4bc7e65f22aa56baf685a748311c402df93708045` |

The path-fence controls ran immediately before the admission output check was extracted into its `external_output()` helper; the extracted helper and call site were subsequently inspected and preserve the tested condition. This hash table is a scoped audit record, not a prohibition on further reviewed release-tool changes.

Supporting reading was limited to repository instructions, the selected release files, their admission mutation test, current presentation metadata and wrapper, page builder/entry point, and the existing historical presentation tests. No literature research or new physics derivation was performed. This is an independent tooling review by a model agent, not external peer review.
