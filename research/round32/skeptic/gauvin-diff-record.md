# Gauvin arXiv:2503.15539 v1/v2/v3 diff record (Round32 skeptic)

2026-09-23. Status `round32_skeptic_source_record`: not a contract, loop, gate or certificate. Human project author: Hruday N M (BUNZEEY). Written by the model-agent skeptic; this is not human peer review, and nothing here judges Gauvin's mathematics. It records only what each public version contains.

## Access and bytes

The abstract pages for v1, v2 and v3 returned HTTP 200 through curl. WebFetch cross-checked the v1 and v3 abstract pages and gave the same submission history. The files were downloaded to the session scratchpad as temporary reading copies; only metadata enters the repository, following Round29 `download-bindings.json`. Text was extracted with `pdftotext`, both raw and `-layout`, and the v2 supplement was read as LaTeX source.

| file | bytes | sha256 |
|---|---|---|
| v1 PDF (`/pdf/2503.15539v1`, 22 pp.) | 209576 | 22f345622c7680ce75d58e26bb689aee6bc7251199cc37a6465d39b817af3464 |
| v2 PDF (29 pp.) | 583961 | 10b1cf8eac5398b49de40d5ee44ad6990dddfe3ad569fa39698433b7ca858d8d |
| v3 PDF (29 pp.) | 584030 | f21a15cf26b916f008c3cf41b576682f2a81c8c53db860cec0c0f5a265a42a95 |
| v2 ancillary `PMAG_Supplement.tex` | 637694 | 45829586668ed19364cb1e556f9f25136211439d529df772ffdf870ee61beea7 |
| v3 ancillary `PinchedMultiAffineGeometry_Supplement.pdf` (67 pp.) | 971545 | dc0d5e590e3989bb421bcf55449f0216a1653b2832d3169e740e33a3a5af6a5d |

**Method limits.**
- For v1, the check is a full-text keyword search plus a reading of its section list and its §IV derivation.
- For v2 against v3 main text, the check is a diff of the extracted text.
- For the v2 supplement (.tex) against the v3 supplement (PDF), the check has three parts: the section structure; an 8-gram match of every prose sentence in the A.6–A.11 region (v2 .tex lines 227–431); and a manual grep of each fragment the 8-gram match flagged. This is not a line-by-line identity proof, because a compiled PDF cannot be diffed line by line against its source.

## The nine items

1. **History, sizes, category, title.**
   - Versions: v1 was submitted Thu 6 Mar 2025 14:54:42 UTC (18 KB), v2 Fri 11 Sep 2026 17:21:11 UTC (202 KB) and v3 Mon 14 Sep 2026 01:20:27 UTC (971 KB). The listed sizes are source sizes.
   - Category: physics.gen-ph for all three. No comments field in any version.
   - Title: the abstract-page title is identical in all three: "Pinched Multi Affine Geometry and Confinement: Describing the Yang-Mills Mass Gap". The v1 PDF title adds "Geometrically", and the PDF is marked "Dated: March 21, 2025" (University of Waterloo, RQI-Lab).
   - Ancillary files: v1 has none, v2 has `PMAG_Supplement.tex` and v3 has `PinchedMultiAffineGeometry_Supplement.pdf`, whose PDF CreationDate is 2026-09-13 11:28:01 UTC.
2. **Abstracts.**
   - v1: "We introduce a multi affine geometric framework in which spacetime curvature relaxes non-instantaneously, subject to a fundamental Planck-scale limit on volumetric contraction." The PDF abstract differs slightly from the listing: it has "a finite area defined by the dual affine connections ... energy requirement to pull apart quarks" where the listing has "a finite tension between non-Abelian color sources".
   - v2 and v3 are verbatim identical: "We give physical gap certificates for regulated Yang-Mills Hamiltonians and conditional continuum-transfer criteria. At fixed spatial cutoff, the physical SU(3) Hamiltonian has a volume-independent gap of at least 8a/3 for magnetic/electric ratio b/a<=1/648 ...". They end with "The interacting four-dimensional construction, nontrivial renormalized local fields and a uniform physical mass gap remain unproved."
3. **Regulated SU(3) Hamiltonian.**
   - v1: **absent**. §IV "Lower bound for mass excitations in non-Abelian gauge" gives only "We sketch a simplified derivation that merges the geometric pinning with canonical gauge-field arguments. Let H be the gauge-invariant Hamiltonian of the Yang–Mills field". It has no lattice form.
   - v2 and v3: **present, identical**, in §II.C "Fixed-cutoff interacting result", eq. (2.11): `H_Lambda = a sum_e L_e + b sum_p (1 - F_p)`, with `F_p = (1/3) Re tr U_p`, `a>0`, `b>=0`. The graphs are "open cubic boxes, finite outgoing-link block restrictions, or periodic cubic volumes of side at least four".
4. **Theorem 2.3 and constants.**
   - v1: **absent**. The strings 648, 8a/3, 1/24, 1/128, 47/48, SU(3), Kogut and cutoff all return zero hits. "Theorem" occurs only in "the Stokes theorem".
   - v2 and v3: **present, identical**. Theorem 2.3 (explicit finite-volume physical gap) reads: "if b/a <= 1/648, the actual Hamiltonian (2.11) has a unique normalized positive ground vector Psi_Lambda. It is physical, and H_{Lambda,phys} - E_Lambda >= (8a/3)(I - |Psi_Lambda><Psi_Lambda|)."
   - The proof strategy reads: "At J/delta <= 1/128, the creation equation contracts the radius-1/24 ball; its shifted equation has Lipschitz constant below 47/48 for energy differences below 2 delta." It also gives `delta=4a/3` and "The Wilson estimate J <= 27b/4 makes b/a <= 1/648 sufficient".
5. **Lemmas 2.14–2.15, Theorem 2.5, Corollary 2.6.**
   - v1: **absent**.
   - v2 and v3 main text: **present, identical**. It says "Lemmas 2.14 and 2.15 adapt the creation-operator method [2, Sections 2.1-2.4] to gauge rotors". Reference [2] is Bravyi, DiVincenzo and Loss, CMP 284, 481–507 (2008), arXiv:0707.1894. The lemma statements themselves are in the supplement.
   - Theorem 2.5 is titled "thermodynamic Hamiltonian and complete physical gap". Its conclusion is `K_phys >= (8a/3)(I - P_Omega)`.
   - Corollary 2.6 is titled "two-sided Wilson correlations and finite spectral edge" and gives `s_F >= eta_0 > 1/60`.
6. **Supplement A.6–A.11.**
   - v1: **no supplement**.
   - v2 (.tex) and v3 (PDF): **present, with the same headings A.1–A.29**. They contain:
     - Lemma 2.14: `c_M^ = |c_M><Omega_M| (x) I`, with "Any two such creation operators commute, and their product is zero when their supports overlap". A.6 also has the active-link count: every nonvacuum physical block contains a cycle, giving at least four active links.
     - Lemma 2.15: the anchored norm `||c||_a = max_u sum_{I ni u}||c_I||` and the majorant `L_k = 8*6^k(1/4+7k/12)`. It states "The commutators vanish for k > 6", which is the termination order. It also gives the shifted-resolvent factor "at most two" for `|z|<2 delta`.
     - A.8 proves Theorem 2.3: the finite-cutoff eigenvector, the contraction, and "Removing the electric cutoff" by min-max for the first two physical eigenvalues.
     - A.9 proves Proposition 2.4, A.10 Theorem 2.5 (thermodynamic Hamiltonian) and A.11 Corollary 2.6.
   - Every prose sentence of the v2 A.6–A.11 region was found in the v3 text. Fourteen fragments were flagged by the 8-gram test; all were LaTeX or math-stripped artifacts, and the manual grep found each one. No substantive v2/v3 supplement change was detected by this method.
7. **Fixed cutoff versus untruncated rotors.**
   - v1: not applicable.
   - v2 and v3: "fixed spatial cutoff" means the fixed cubic lattice. The electric (rotor) spectral cutoff is auxiliary and is removed: "It removes the auxiliary electric spectral cutoff; space remains a cubic lattice and Hamiltonian time is continuous".
   - In the passage read (A.8), the removal is for eigenvalues and the gap, by min-max. No ground-vector convergence statement was found there. This is consistent with AV1 item 6.
8. **v2 against v3, first appearance.**
   - Main text: the extracted texts differ in one line only, the arXiv stamp ("v2 ... 11 Sep 2026" against "v3 ... 14 Sep 2026").
   - Supplement: v2 carries it as LaTeX source, and v3 replaces that with the compiled PDF.
   - **Every item 3–7 first appears publicly in v2 (2026-09-11 17:21:11 UTC). None appears in v1.**
9. **The project's own record.**
   - Round29 `experts/download-bindings.json` binds the v3 PDF (f21a15cf..., 584030 B) and the supplement (dc0d5e59..., 971545 B). These are byte-identical to today's downloads, so the project read exactly these files.
   - Round29 `experts/sources.json` was accessed 2026-09-22. It records the supplement's use as "AM template and attribution comparison".
   - AM1 reverse `primary-reading.json` binds the same supplement hash, with the reading note "A6-A8 pp S4-S6; A9-A11 context".
   - AQ1 forward states "direct prior overlap with Gauvin arXiv:2503.15539v3 Supplement A.10".
   - Commit dates:
     - The AM2 report's first commit is 2e64f6e at 2026-09-22T20:39:38Z. This holds both in this clone and in the public GitHub API for `occult-kranti/yang_mills_workbench`.
     - The workbench's first commit, c98c810, is dated 2026-09-09 19:53:58 UTC.
     - Commit dates are self-reported and are not trusted timestamps.
   - Keyword searches of v2, v3 and both supplements find no Hruday, BUNZEEY, workbench, GitHub, Claude, GPT or AI-assistance mention. They also find no Datta, Kennedy or Kirkwood hits. Yarotsky (2006) and Osterwalder–Seiler (1978) are cited.
   - No inference about the direction of influence is drawn.

## Consequence for wording (the advisor decides)

The version and date left open in the interim sentence are now fixed. Proposed replacement, still with no priority or independence claim:

> "The AM2 creation-expansion gap and the AQ construction follow strategies that first appear publicly in Gauvin arXiv:2503.15539v2 (2026-09-11; §II.C–D and supplement A.6–A.11). The project read them in v3 (2026-09-14) and records them as its template. Gauvin credits the creation-operator method to Bravyi–DiVincenzo–Loss (CMP 284, 2008, §§2.1–2.4). v1 (2025-03-06) contains none of these items. The SU(2) selected-reference application and its explicit constants are this project's record; scientific priority is not claimed."

`priority_statement_allowed` stays false.
