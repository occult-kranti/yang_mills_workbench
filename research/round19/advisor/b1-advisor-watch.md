
# Round19 B1 advisor watch note

Status: **tracking only**. No B1 worker evidence is present yet under `forward/b1/` or `backward/b1/`, and B2 is not frozen.

This note records the advisor's independent bottleneck checklist for the frozen B1 contract. It does not alter `advisor/contract-b1.json`.

## Current locked inputs

- A2 gate after manifest refresh: `advisor/a2-gate.json`, SHA-256 `80c1dc9add22e4d042155017202534fc8ff5e977a445e655d6ada1d90726efe9`.
- Post-A decision inventory after refresh: `advisor/post-a-decision.json`, SHA-256 `48704238748bca15b03beee0f9bedd3308628372163530c7e9c746000bab2bbb`.
- B1 contract: `advisor/contract-b1.json`, SHA-256 `5bec22522df9f65f6eafc460087647de01713c46348f006ca260e45a62691af9`.
- Reconciled paired-physics skill path verified: `/root/.codex/skills/remote-skills/skill-6aa703b7e6f48191a700951cb36ce6a2/SKILL.md`. Repository snapshots remain authoritative for reproduction.

## Bottleneck 1: strict cutoff completeness

Round18 proved completeness below `9alpha/2` for `P = vacuum + eleven fundamental face characters`. Round19 B1 raises the projector target to the strict cutoff

```text
E_el < 6 alpha.
```

That admits fundamental six-edge simple cycles at energy `9alpha/2`; therefore the old Round18 projector is not the Round19 B1 projector. B1 must count all actual four- and six-edge simple cycles, including nonplanar cycles, and all gauge-invariant intertwiners.

A quick advisor-side graph sanity check using the Round18 actual two-cube graph found:

```text
support size <= 7 on the 20-link graph
size 0: 1 no-leaf support
size 4: 11 no-leaf/even supports
size 6: 36 no-leaf/even supports
size 7: 28 no-leaf supports, but 0 even-degree supports
simple cycles: 11 of length 4, 36 of length 6
```

This supports the expected four/six-cycle target but does not prove the physical channel theorem. The missing proof obligation is representation-theoretic: supports with branching or degree-three vertices can be physical with mixed spin labels even when they are not ordinary even-degree fundamental cycles.

B1 must therefore prove exclusion of branching/mixed channels below `6alpha`, not merely enumerate simple cycles. In particular:

- degree-two connected supports force constant spin around each cycle;
- four- and six-edge fundamental simple cycles lie below `6alpha`;
- disjoint pairs of four-edge fundamental cycles give an excluded threshold channel at exactly `6alpha` when available;
- seven-edge no-leaf supports require special handling because they are not even-degree cycles;
- possible theta supports must be excluded by graph topology and energy, including the likely minimal path-length pattern `1,3,3` on this cubic graph and the absence of a `K_{2,3}` path pattern `2,2,2`;
- mixed degree-three intertwiners such as half/half/integer labels must be bounded by the actual edge energy sum, not dismissed by fundamental parity alone.

## Bottleneck 2: exact cross Gram versus conservative substitutes

The original Goal B obligation is the full exact cross Gram

```text
W^*W = P V^2 P - (P V P)^2.
```

Round18 exact fourth-moment machinery is useful evidence, but B1's enlarged `P` changes the matrix dimension and admitted channels. The old face-only formula cannot be imported without recomputing all repeated moments and `PVP/PV^2P` against the new strict-cutoff basis.

The B1 gate should reject:

- `PV^2P` presented without the subtraction;
- a norm or row-sum bound presented as the exact Gram;
- a Gram computed for the old face-only `P`;
- a Gram computed on the outer boundary graph;
- a sampled/truncated spin basis presented as complete physical support.

If workers prove cutoff completeness but cannot compute the full Gram, the correct outcome is a **limited** B1 gate preserving the exact-Gram obligation for B2 or a repaired B1 loop. It should not be labeled fulfilled.

## Bottleneck 3: threshold witness

The strict cutoff requires an actual omitted channel at `E_el = 6 alpha`. The safest expected witness is a pair of disjoint four-edge fundamental cycles, if the actual two-cube graph contains a disjoint pair after the complete graph audit. If not, B1 must identify another actual threshold channel or prove absence and downgrade the target. A six-edge fundamental loop is below the cutoff, not the threshold witness.

## Gate posture

The eventual B1 gate should remain pending until both forward and reverse evidence are present, executable, source-bound and independently compared. Normal and optimized runs count once. B2 must be selected only after the B1 evidence says whether the strict projector and exact cross Gram were completed, limited or rejected.
