# Uniform norm averaging for the unilateral shift

**Result.** On H = ℓ²(ℕ₀), for every τ > 0 and T ≥ 0,

\[
 \sup_{|s|\le T}\|Z_\tau(s)-I\|
 \le \min\{2,\,2T,\,4\tau(1+2T)\}.
\]

Thus the convergence is in **operator norm, uniformly on compact slow-time intervals**. The same estimate holds for the adjoint and for the product with the two propagators in the opposite order. This special source permits a stronger topology than a general pure-point averaging argument guarantees. A positive ground gap alone would not imply this estimate for an arbitrary bounded source.

## Proof

Let D(K) = {x : ∑ n²|xₙ|² < ∞}. The diagonal operator K is self-adjoint on this domain. Both shifts preserve D(K):

\[
 \|KSx\|^2=\sum_{n\ge0}(n+1)^2|x_n|^2
 \le2\|Kx\|^2+2\|x\|^2,
 \qquad \|KS^*x\|\le\|Kx\|.
\]

Since A = S + S* is bounded self-adjoint with norm at most 2, Hτ = K/τ + A is self-adjoint on D(K) by the bounded perturbation theorem. The unitary groups of K/τ and Hτ preserve their common domain; their graph norms are equivalent. Differentiation of the displayed relative product on D(K), with continuity in those graph norms, gives

\[
 Z_\tau'(s)=-iA_\tau(s)Z_\tau(s),\qquad
 A_\tau(s)=e^{is/\tau}S+e^{-is/\tau}S^*.
\]

One may first integrate this identity strongly on D(K), then extend the integral equation to every vector by density and the uniform bound \(\|A_\tau(s)\|\le2\). Here the **actual** coefficient Aτ is norm continuous. The norm-continuous bounded-operator Volterra equation has a unique norm-C¹ solution; its strong uniqueness identifies that solution with Zτ. Consequently the following integration by parts is in operator norm. No norm continuity of either unbounded-generator group is asserted.

K has simple eigenvalues n. With Pₙ = |eₙ⟩⟨eₙ|, every complete diagonal block PₙAPₙ is zero. The averaged source \(\overline A=\sum_nP_nAP_n\) is therefore exactly zero. More directly, its oscillatory primitive is

\[
 B_\tau(s)=\int_0^s A_\tau(r)\,dr
 =-i\tau(e^{is/\tau}-1)S
  +i\tau(e^{-is/\tau}-1)S^*.
\]

Thus Bτ(0) = 0, Bτ′ = Aτ, and \(\|B_\tau(s)\|\le4\tau\), uniformly for all real s. Integration by parts yields

\[
 Z_\tau(s)-I=-iB_\tau(s)Z_\tau(s)
       +\int_0^s B_\tau(r)A_\tau(r)Z_\tau(r)\,dr.
\]

Unitarity now gives \(\|Z_\tau(s)-I\|\le4\tau+8\tau|s|\). The unitary bound 2 and the original integral-equation bound 2|s| give the stated minimum. For s < 0, reverse the integration orientation before taking the norm.

The adjoint has the actual order

\[
 W_\tau(s)=Z_\tau(s)^*=e^{isH_\tau}e^{-isK/\tau},
 \qquad W_\tau'(s)=iW_\tau(s)A_\tau(s).
\]

Here the coefficient multiplies on the **right**. Its corresponding identity is

\[
 W_\tau(s)-I=iW_\tau(s)B_\tau(s)
       +\int_0^s W_\tau(r)A_\tau(r)B_\tau(r)\,dr,
\]

which gives the same bound; equivalently \(\|Z_\tau^*-I\|=\|Z_\tau-I\|\). Also
\(e^{-isH_\tau}e^{isK/\tau}=e^{-isK/\tau}Z_\tau(s)e^{isK/\tau}\), so the opposite interaction-product order has the same distance to I. In particular both propagator factors in any bounded sandwich can be replaced, with a summed error bounded by twice the displayed certificate times the observable norm.

For a fixed **real** scalar c, replacing A by A + cI gives

\[
 \overline{A+cI}=cI,\qquad
 Z_{\tau,c}(s)=e^{-ics}Z_\tau(s),\qquad
 \sup_{|s|\le T}\|Z_{\tau,c}(s)-e^{-ics}I\|
 \le\min\{2,2T,4\tau(1+2T)\}.
\]

The proposed limit I therefore changes unless c = 0 (or one evaluates only isolated times with cs ∈ 2πℤ). For c ≠ 0 and every T > 0, the scalar phase differs from 1 somewhere in [−T,T]. It cannot be discarded in this single relative propagator. It does cancel from conjugation by that propagator. A complex c would violate the task's self-adjoint/unitary setting and is not covered by the stated bound.

## Exact evidence and its limits

`check.py` uses only the Python standard library and Gaussian rational arithmetic. It compares degree-six Taylor coefficients of the actual ordered exponentials against a separately implemented interaction-equation recurrence, on e₀, e₁ and e₇, with and without a scalar shift. Its adjoint check uses the right multiplication equation. Sparse actions remain on the half-line and impose no artificial upper boundary. It checks the symbolic oscillatory primitive and average, and exact arithmetic in the displayed majorant. Controls reject a reversed source phase, reversed primitive sign, erroneous adjoint multiplication side, bilateral-shift commutation at the boundary, retaining the unaveraged source as its average, discarding the scalar average/phase, and invalid parameter signs.

These finite algebra checks do **not** prove the unbounded-domain statements, convergence of exponential series on arbitrary vectors, the infinite-dimensional norm bound, or uniformity over all s and all vectors. Those conclusions follow from the proof above. The series calculations are finite coefficient identities on finite-support vectors and do not need a convergence claim. Their maximum coefficient degree is an explicit coverage limit.

`replay.py` binds all required sources and instruction snapshots, enforces exact Boolean statuses and control identities, reexecutes the checker into fresh external directories, and compares every declared output. It rejects coherent failed-status, missing-snapshot and changed-bound mutations, plus stale hashes and parent/leaf symlinks. Normal and optimized Python runs both execute these controls. Hashes and replays establish evidence integrity within this fixed checker; they are not an independent mathematical review or protection against replacement of the trusted validator itself.

This is one standalone method test, **zero physics roadmap loops**. The derivation, alternative coefficient reconstruction and critical controls are by the same agent. No Round24 producer or other method-test solution was consulted. The result applies the bounded perturbation theorem and elementary integration by parts in this model; scientific novelty is unverified. The skill snapshots supply methodology, not an external proof of this theorem. Newton/Tesla workflow references were read because of the ancestor AGENTS instruction; their historical claims were neither newly verified nor used as operator-theory premises.

From this directory, reproduce with:

```sh
python replay.py --record /tmp/norm-averaging-normal-record.json
python -O replay.py --record /tmp/norm-averaging-optimized-record.json
```

Each record destination must be new. All scientific inputs and bindings are relative to this directory. `source-readings.json` identifies the exact snapshots read, and `source-manifest.json` binds the final report, executable sources, contract, snapshots, and frozen `output/results.json` and `output/controls.json`. This task makes no assertion about a physical clock, Yang–Mills gap, infinite-volume limit, or a generic rate for all bounded A.
