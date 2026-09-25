# BB1 repair record: the forward's Kotecký–Preiss citation against the committed Ueltschi excerpt

**Standing.** I am the BB1 skeptic, a model agent with correlated ancestry, not a human reviewer, writing after my post-comparison review (`bb1.md`, item 3). There I ruled that the forward cites the Kotecký–Preiss criterion without a committed source, that the packet's own lemmas do not prove the cited consequence, and that this is a limitation, not a blocking issue. The advisor accepted that ruling and applied the repair I proposed: it committed an excerpt of the source (commit `cca0584`, 2026-09-25T02:51:54Z).

This record compares the forward's statement and its use with that excerpt. It is a post-hoc check.
- The excerpt was committed after both BB1 freezes and is not in either packet's `inputs/`.
- Nothing in the frozen packets changes.
- No bound value changes.

Human author: Hruday N M (BUNZEEY).

**Compared texts.**
- **Forward:** `research/round33/forward/bb1/report.md` (frozen in `research/round33/forward/bb1/freeze.json`, sha256 `90ddc178…30e1d`), §6: Theorem 6.1 (cited), Proposition 6.2, Corollary 6.3 and Lemma 6.4. The attribution line (header) says the statement "is transcribed as known to this producer".
- **Source:** `research/round33/sources/ueltschi-math-ph-0304003v3.md`, file sha256 `17b0b3ffe86b9a17ff8b9e24511b28e974bc0397590b75f179411f6d2c0eed66`. It excerpts D. Ueltschi, *Cluster expansions and correlation functions*, arXiv:math-ph/0304003v3, Moscow Math. J. 4 (2004) 511–522; PDF sha256 `2cc3e036af5b2a46afe95acf0b5863fe5c7d31554debb10a2a5cade4122bdbfc`.
  - It covers Theorem 1 with (3)–(5), the weights `b`, `c` and Theorem 3 with (16)–(19), and §4.2 (hard-core lattice polymers).
  - Part A is a transcription checked against the rendered pages; Part B is the raw `pdftotext` text.
  - The original Kotecký–Preiss paper (Comm. Math. Phys. 103 (1986) 491–498) is not committed.

## 1. Dictionary

| Ueltschi (excerpt) | forward (report §§3, 6) |
|---|---|
| measure space `(𝔸, µ)`, complex `µ` with `|µ|(𝔸)<∞` | the finite set of polymers `γ=(𝓕,𝓕')` in `Λ'`, counting measure times the activity `w(γ)` (finite, so every integrability condition is automatic) |
| `ζ(A,A') = −1` if the two intersect, else `0` (§4.2, hard core) | incompatibility `γ ≁ γ'` iff `supp γ ∩ supp γ' ≠ ∅`; `ζ(γ,γ) = −1` since supports are nonempty |
| `|1+ζ_c| ≤ 1` | automatic: `c ≡ 0` and `1+ζ ∈ {0,1}` (§4.2 says so for the hard-core case) |
| `c ≡ 0` (allowed: "both can be identically zero") | no pair weight is used |
| `b(A) ≥ 0`, `µ_b = µ e^{b}` | the distance weight `d(γ) = μ Σ_{K∈γ} diam K`, `e^μ = v` (`v=128` at the headline, `390625/296` at the secondary cap); `d ≥ 0` because `v ≥ 1` |
| nonnegative `a(A)` | `a(γ) = a|supp γ|`, with `a = τ̄²` |
| (1) `Z = Σ_n (1/n!) ∫dµ… Π_{i<j}(1+ζ)` | `Z(Λ') = Σ_Γ Π_{γ∈Γ} w(γ)` over families of pairwise compatible polymers: ordered sequences of distinct compatible polymers, divided by `n!`; repeats and overlaps get the factor `1+ζ = 0` |
| (2) `φ(A_1,…,A_n)` (with the `1/n!`) summed over sequences | `Φ^T(X)` summed over connected multisets `X`: all orderings of a multiset give the same `φ`, so `|Φ^T(X)| = Σ_{sequences representing X} |φ| Π|w|` exactly |

## 2. Theorem 6.1 (the cited statement)

**Hypothesis.** The forward requires `Σ_{γ'≁γ} |w(γ')| e^{a(γ')+d(γ')} ≤ a(γ)` for every polymer `γ`. Ueltschi (16) with `c ≡ 0`, `b = d` reads `∫d|µ_b|(A') |ζ(A,A')| e^{a(A')} = Σ_{γ'≁γ} |w(γ')| e^{d(γ')} e^{a(γ')} ≤ a(γ)`. **Identical.** Both sums include `γ' = γ`.

**First conclusion: `Z(Λ') ≠ 0` and `Z(Λ') = exp Σ_{X⊂Λ'} Φ^T(X)`, absolutely convergent, for every `Λ' ⊂ Λ`.** This is Ueltschi Theorem 1.
- Its hypothesis (3) is (16) with `b ≡ 0`, and it follows from (16) because `b = d ≥ 0` gives `|µ| ≤ |µ_b|`.
- Restricting the polymer set to `Λ'` only removes terms, so (3) holds for every `Λ'`.
- `∫d|µ|e^{a} < ∞` holds because the set is finite.
- **Covered.** Independently, the packet proves `Z(Λ∖S) = ⟨ψ, P_S ψ⟩ ≥ 1` (Corollary 3.4).

**Second conclusion: `Σ_{X≁γ} |Φ^T(X)| e^{d(X)} ≤ a(γ)`, with `d(X) = Σ_{γ'∈X} d(γ')`.** This follows from Ueltschi (19), `Σ_n ∫d|µ_b|(A_1)…d|µ_b|(A_n) (Σ_i |ζ(A,A_i)|) |φ(A_1,…,A_n)| ≤ a(A)`.

(19) is the `m = 1` case (18) of Theorem 3, multiplied by `|ζ(A,A_1)|` and integrated using (16). The excerpt shows that step, and the paper states it is proved the same way as (4)–(5). Two points of form need checking:
- **The weight `e^{d(X)}` is the `µ_b` weighting.** In (19) each entry `A_i` of the sequence carries `|µ_b|(A_i) = |w(A_i)| e^{b(A_i)}`. The product over the sequence is `Π|w| · e^{Σ_i d(A_i)}`, and `Σ_i d(A_i)` is `d(X)` with multiplicity, exactly the forward's `d(X) = Σ_{γ'∈X} d(γ')` over the multiset. **Same weight, no missing factor.** If `d(X)` were read over distinct polymers, the forward's left side would only be smaller, since `d ≥ 0`.
- **The incompatibility factor.** Ueltschi weights a cluster by `Σ_i |ζ(A,A_i)|`, the number of entries incompatible with `A`, counted with multiplicity. The forward uses the indicator `1[X ≁ γ]`. Every cluster incompatible with `γ` has count at least 1, and the others contribute 0 on both sides. So the forward's left side is at most Ueltschi's. **Covered, and the source is stronger.**

**The test-set clause.** The forward states the hypothesis "for every test set `γ` (a finite set of sites with `a(γ) = a|γ|`, treated as a polymer of activity 0, which leaves every other sum unchanged)". Ueltschi's theorem is stated on an arbitrary measure space, so the clause is an instance of it, not an extension:
1. Adjoin every finite site set `S ⊂ Λ` to `𝔸` as an atom of mass `µ({S}) = 0`.
2. Put `ζ(S,·) = −1` on sets and polymers meeting `S` (else `0`; symmetric, `|1+ζ| ≤ 1`), `a(S) = a|S|`, and any `b(S) ≥ 0`.
3. Mass-zero atoms change no integral. So `Z`, every cluster sum, and (16) at every genuine polymer are unchanged.
4. (16) must also hold at `A = S`. That is the forward's test-set hypothesis, `Σ_{supp γ' ∩ S ≠ ∅} |w(γ')| e^{a(γ')+d(γ')} ≤ a|S|`.
5. (19) at `A = S` then gives `Σ_{X ≁ S} |Φ^T(X)| e^{d(X)} ≤ a|S|` over clusters of genuine polymers.

The one sentence of argument that this needs is the forward's own parenthetical. **Covered.**

**Hypothesis verification (Proposition 6.2, the forward's own work).** The side conditions of the dictionary hold at every tier used; `check.py` and my post-review checker (check `kp_citation_checked_against_committed_excerpt`) re-verify them exactly:
- `a = τ̄²`, `a ≤ 2b` with `b ≥ ln(1001/1000) ≥ 1/1001`, `1 ≤ v ≤ w`, and hard-core `ζ`.
- Headline: `a ≈ 4.46206e-13`, `v = 128 ≤ w = 192`.
- Secondary: `a ≈ 7.05915e-11`, `v = 390625/296 ≤ w = 1171875/592`.
- Crude: `a ≈ 1.30232e-6`.

The per-site bound `Σ_{γ∋x} |w(γ)| e^{a(γ)+d(γ)} ≤ τ̄² ≤ a` then gives (16) at every polymer and every test set, summing over the sites of `γ` or `S`. It uses:
- the activity bound (Lemma 3.5);
- `a|supp γ| = (a/2) Σ_{K∈γ} |K|`, because each side is a disjoint union;
- the exploration count (Lemma 4.2 (P1));
- the mixed norm (Corollary 5.2).

None of this is taken from the source. The source needs only the resulting inequality.

## 3. The use: Corollary 6.3 and Lemma 6.4

- **Corollary 6.3** (`Σ_{X≁z, X≁s} |Φ^T(X)| ≤ a v^{−d(z,s)}`) combines the test-set conclusion at `S = {z}` (`a|{z}| = a`) with a geometric fact the forward proves itself:
  - A cluster touching `z` and `s` has connected support: incompatible polymers share sites, and each polymer is overlap-connected through its members, which is the definition of a polymer in §3.
  - So `d(z,s) ≤ Σ_{γ∈X} Σ_{K∈γ} diam K`, that is `e^{d(X)} ≥ v^{d(z,s)}`, with `v ≥ 1`.
  - **Covered.**
- **Lemma 6.4** takes `π_{Λ'}(γ) = exp(−Σ_{X⊂Λ', X≁γ} Φ^T(X))` from the two absolutely convergent expansions of `Z(Λ')` and `Z(Λ'∖supp γ)` (Theorem 1, applied twice).
  - The difference between `Λ` and `Λ∖S` is `Δ = Σ_{X≁γ, X≁S} Φ^T(X)`.
  - `|π_{Λ∖S} − π_Λ| ≤ |Δ|` follows because both probabilities are real, positive and at most 1 (Corollary 3.4). This is elementary and in the report.
  - Then Corollary 6.3 gives `Σ_{z∈supp γ} Σ_{s∈S} a v^{−d(z,s)}`.
  - **Covered.**

## 4. Differences recorded exactly

| # | difference | classification |
|---|---|---|
| 1 | The forward does not state Ueltschi's hypothesis `|1+ζ_c| ≤ 1`. | Not a gap: with hard-core `ζ ∈ {0,−1}` and `c ≡ 0` it holds identically, and §4.2 says so. |
| 2 | The forward does not state `∫d|µ| e^{a} < ∞` (Theorem 1). | Not a gap: the polymer set is finite. |
| 3 | Ueltschi carries the decay through `µ_b = µ e^{b}`; the forward writes `e^{a(γ')+d(γ')}` in the hypothesis and `e^{d(X)}` in the conclusion. | Same weighting (each cluster entry contributes `e^{d}`); no missing or extra factor. |
| 4 | Ueltschi's conclusion (19) weights clusters by the count `Σ_i |ζ(A,A_i)| ≥ 1`; the forward by the indicator. | The forward's statement is weaker; covered. |
| 5 | The test-set clause is not in Ueltschi's statement. | An instance (mass-zero atoms of the measure space); the extra argument is one sentence and is in the forward's parenthetical. |
| 6 | The forward attributes the criterion to Kotecký–Preiss 1986 "in the form of Ueltschi"; only Ueltschi is committed. | Ueltschi alone covers every step used. Ueltschi remarks that (3) is the Kotecký–Preiss criterion for lattice polymers. The original paper is not needed. |
| 7 | The source proves (18)–(19) by reference ("exactly the same way as (4) and (5)"). | Accepted as the published statement of a refereed paper, like any cited theorem; not re-proved here. |
| 8 | The forward's transcription was made from memory, before any source was committed. | Checked post hoc: it matches (16)/(19) in hypothesis form and conclusion. The check is recorded here, not in the frozen packet. |

**Missing factor: none. Different hypothesis form: none beyond the notation in rows 3 and 5. The `|1+ζ_c| ≤ 1` condition holds identically.**

## 5. Result

- **The forward's cited statement follows from the committed source,** using Ueltschi Theorem 1 and Theorem 3 with (16) and (18)–(19) at hard-core `ζ`, `c ≡ 0`, `b = d` and `a(γ) = a|supp γ|`, with test sets as mass-zero atoms.
- **Its use in Corollary 6.3 and Lemma 6.4 is covered.** The only extra arguments are the forward's own elementary steps, all present in the frozen report:
  - the sequence-to-multiset conversion;
  - the connectivity bound `e^{d(X)} ≥ v^{d(z,s)}`;
  - the real positivity of the vacuum probabilities;
  - the hypothesis verification of Proposition 6.2.
- **The polymer_kp route is complete from its declared premises together with a committed, hash-bound source.** The frozen packet itself still shows no source quotation.
- **The limitation therefore changes** from "complete only modulo the cited theorem" to "cited theorem checked post hoc against the committed excerpt: covered". It stays a limitation because the check is post hoc and outside the frozen packet.

**Effect on the gate.** The verdict stays `accepted_within_scope`. The bound values are unchanged:
- `C ≈ 8.905120e-7` and `c_site ≈ 8.768118e-7` (polymer_kp);
- `C_2 ≈ 9.689093e-6` and `c_site,2 ≈ 9.674431e-6` (iterated_split);
- the other route's values labelled.

The `conditional_alternative` in `bb1.json` (verdict `limited`, reverse constants bound, if plan rule P4 is held binding on the frozen producer itself) is retained as the advisor asked. After this comparison it is not recommended.

**What was not done.**
- The original Kotecký–Preiss paper was not read.
- The proof of Ueltschi's Theorem 3 was not re-derived.
- The excerpt's Part A transcription was not re-checked against the PDF: I have neither the PDF nor its rendered pages. I rely on the advisor's recorded check and on the Part B machine text, which agrees on (1)–(4), (16) and the definitions of `µ_b`, `ζ_c` and `φ_c`.
- Later expert-assistant files were not opened. In particular, `git log` displayed the subject of `d5709f2` ("… KP side-condition preview and self-containment finding …") and of `f411abb` (historical assistant), and I opened neither.
