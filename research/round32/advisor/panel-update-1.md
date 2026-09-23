# Panel update after sub-round 1 (AV1, AV2)

Date 2026-09-23. Inputs: the three lens updates (`experts/historical/update-1.md`, `experts/jung/update-1.md`, `experts/modern/update-1.md`), the three assistant packages (`experts/*/assistant-1/`), the AV1 gate and the AV2 reviews. This is a planning record; it admits nothing.

## What the assistants verified (zero research loops)

- Newton/Tesla assistant: exact Haar moments (0, 1/4, 0, 1/8) by two routes; the 49/15/82 enumeration rebuilt from the I1 table without the producers' code; the forward AV1 constant reproduced bit-for-bit; the window budget 1.832e-7 at tier (ii), 4.75e-5 at tier (i), crossover 6.237; the AT4 Poisson radius reproduced exactly as a rejected control.
- Jung/Pauli assistant: tau=0 null replay (state terms vanish exactly; window radius reduces to the arithmetic term); tau-scaling exponents 1.0000 (tiers) versus exactly 0.5 (square-root bound), with the label-swap mutation rejected; pre-registration audit: AV1 fully compliant; AV2's frozen contract lists 24 controls but its pre-registration mirror lists 23 (missing `c1_window_preview_only`). Both AV2 producers implemented the missing id anyway. The advisor records this in the AV2 gate as a non-blocking clerical defect and does not amend the frozen contract; the freezing tool now rejects such a mismatch.
- Modern assistant: reusable python-flint harness (exact Rayleigh bounds, Arb eigenvalue previews, containment); exhaustive flip-parity check (every plaquette meets E oddly on 6^3 and 9^3 blocks; numerical SU(2) fixture flips every plaquette trace); independent counts 49/15/82/10/72 (42+30); window constants confirmed by quadrature and Arb; radius 1.83196750e-7 reproduced.

## Panel decisions

1. Goals for sub-rounds 2–5 are kept as planned (all three lenses; the historical lens's scheduling preference for AZ2 remains non-blocking).
2. AW1 contract improvements adopted from the lenses: the free-link Haar cross-check for the parity theorem; full three-orientation enumeration for the flip lemma; K_2 terms pinned to the rebuilt enumeration with ||W Omega_R||=1/2 as a positive control; `wilson_face_separated`; a positive nonzero-kappa demonstration; the pre-frozen AW2 coupling rule evaluated inside AW2's checker from the AW1 gate.
3. AZ2 will read its cutoff as the polynomial degree D of the Round11 spec with nested D=6/D=8 enclosures and the assistant's harness.
4. No occult, mystical or historical source changed any premise in sub-round 1; the pre-registration discipline they motivated caught one clerical defect.
5. Assistant tests after sub-round 2: replay of the AW1-gate → AW2 coupling-rule chain; a sign-convention fixture; an exact re-derivation of the parity theorem; bracketing K_2^+ against the preview tiers; rehearsal of the Rayleigh/Arb harness on an 84x84 fixture.
