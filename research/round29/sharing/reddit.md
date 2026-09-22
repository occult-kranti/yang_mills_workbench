# A regulated SU(2) result: vanishing local coefficients can still produce a nonzero long-time correlation difference

I'm Hruday N M (BUNZEEY). I've been building a reproducible gauge-theory workbench with AI-assisted derivations, code, and skeptical checks. I'd like feedback on a specific result and its assumptions. This is **not a claim to have solved the Yang–Mills mass-gap problem**.

The result I find most interesting is an endpoint nonconvergence witness in a **canonical summable full-link SU(2) model**.

Fix 0<η<1 and 0<q<1, and write ε=1−q. A local perturbation coefficient behaves as τ_q∼(8η/7)ε³. At the same time, choose the physical observation window T_q=C(ℏ/α)ε⁻³. For one explicitly constructed bounded gauge-invariant local rank observable, the stationary connected real-time autocorrelation C_q and its reference C_0 obey

    liminf |C_q(T_q) − C_0(T_q)|
      ≥ z/84 − (44/9)(80z/7)²/(1−80z/7)⁵
      > z/168 > 0,   for 0<z=Cη≤10⁻⁶.

The short derivation:

1. The actual resonant matrix element gives a leading demodulated response i s_q q⁴/96, with s_q=ατ_qt/ℏ.
2. Starting from eight complete reference factors, ordered connected commutators have at most 40(8+3k) available faces at step k. This bounds the order-n contribution by (10s_q)ⁿ(8/3)_n/n!.
3. Summing every order n≥2 gives a tail at most (44/9)x²/(1−x)⁵, x=10s_q<1. The separately bounded state-replacement error tends to zero.
4. At the chosen T_q, s_q→8z/7. The linear term survives and exceeds the complete quadratic remainder on the stated interval.

Thus the endpoint ε⁻³ cannot be added to a general convergence theorem for every bounded local observable in this model. Earlier results cover slower-growing windows.

Scope matters: the original witness is a rank observable, not a Wilson multiplication measurement; q=1 is outside the summable family; the total perturbation norm is exactly αη/8, constant in q; the lower bound is very small. This does not transfer automatically to the homogeneous model, an experiment, or the continuum theory.

The current draft indexes this endpoint nonconvergence witness as **HNM-C-RECENT25**, preserving its legacy ID **R23 U2**. That's a project label, not an established literature-priority claim. The underlying perturbative tools are standard. The original U2 had same-author model self-review, not independent human peer review.

The newest cycle also gives a separate fixed-lattice result: for the actual selected-strip model at |τ|≤10⁻⁸, a constructed infinite-volume physical representation has gap ≥α/16 and original Wilson variance ≥61999/250000>1/5. The complete Wilson region has 48 links, 36 endpoints and seven incident stars; the bound follows from its actual local energy budget and reference-state trace distance. This is a model-specific application of established creation and GNS methods, including the route in Gauvin’s Supplement A.10. It does not establish uniqueness of all thermodynamic states or a continuum theory.

We also checked the requested [Gauvin preprint, arXiv:2503.15539v3](https://arxiv.org/abs/2503.15539v3), which has methodological overlap and explicitly leaves the continuum construction unresolved. Its results retain their own attribution.

Links: [complete draft](https://occult-kranti.github.io/yang_mills_workbench/ym-draft-02.pdf) · [website](https://occult-kranti.github.io/yang_mills_workbench/) · [GitHub/code](https://github.com/occult-kranti/yang_mills_workbench).

Does the complete-factor counting and state-error treatment support the limiting step as stated? Are there closer prior results for this particular scoped endpoint witness? Specific corrections and references would be very useful.
