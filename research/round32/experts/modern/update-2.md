# Modern lens (Penrose/Feynman), sub-round 2 update

2026-09-24. `round32_subround2_update`; not a contract, loop or gate. Read: `advisor/aw1-gate.json`, `skeptic/aw1.md`, `forward/aw1/report.md`, `reverse/aw1/report.md`, `forward/aw2/report.md`, `advisor/plan.json`, contracts `ax1.json`, `ax2.json`, `ay1.json`, `az1.json`, `az2.json`, `advisor/selection-ax1.md`, own `update-1.md`, `loop2-response.md`. AW2's gate is pending; this stays provisional there.

## 1. Technical assessment

**Parity theorem** (finite boxes, every `N>=2`, every on-site cutoff): the `tau`-derivative at `tau=0` of `omega_N(W^2)`, of `c_N(theta)=<chi,e^{i theta(G-E)}chi>` for every real `theta`, and of `C_N(s)=<chi,e^{-s(G-E)}chi>` for every `s>=0` vanishes, state/Duhamel/energy/vector-centring terms separately, from `E[W^3]=0`, `E[W^2 W_f]=0` (all omitted `f`, incl. `f=W`), `E[W^4]=1/8`, and zero splitting of the gauge-invariant energy-24 multiplet. In AQ limits only set-level evenness survives; the `tau^2` constant for `C(s)` is explicitly unbounded, not uniform in `N`.

**Flip lemma:** `E` meets every `Z^3` plaquette oddly; `U_E` gives `H_N(tau,kappa)->H_N(-tau,-kappa)` exactly, cutoff compressions included. At `kappa=0` this yields `omega_{N,-tau}(W)=-omega_{N,tau}(W)`; at `kappa!=0` no antisymmetry follows, because both arguments flip together. For AQ limits it is a whole-set statement (`S(-tau)=S(tau) o alpha_E`), never pointwise on one chosen limit. Oddness alone gives no `O(tau^3)` bound on `r(tau)`.

**Sign certificate** (AW2, provisional): `tau_AW2=10^-8` (the cap, by the pre-frozen decade rule), `omega_tau(W)` enclosed away from 0 at both signs with exclusion margin `m~206.0>=2` and sign margin `S=1/(144K_2^+tau)~207.0`; static, not dynamical.

**Three `K_2^+` values** (forward 3354.6383, reverse 3354.4994, skeptic 3354.8032) all use the same four real terms (AM2 remainder `rho`, straddling, two-creation, density) but pin the straddling/two-creation/density counts differently (6+33-face pinning vs. conservative `T*T`; AV1's `eps=2T+T^2` vs. the reverse's 82-face refinement). All three are valid exact-tier upper bounds on the same absolute quantity. **Binding the largest (skeptic's) is right**: it is built only from `T`, `rho`, `eps=2T+T^2` with no face-count refinement, so it survives even if a refinement is later disputed, it is exactly the forward's own labelled `unpinned_t_bounds` variant, and N8 already shows no producer checker pins individual terms — undercounts are caught only by cross-comparison, so the conservative bound is the only one an automated checker can trust unaided. The ample slack (any `K_2^+<=10^8/288~3.47e5` still gives `tau_AW2=10^-8`, and the bound is `~3355`) means nothing is lost by this choice.

**Modified-flip-set remark (recorded, not admitted).** `E*=E xor E''` (`delta E''`=selected-face indicator) would give `U_{E*}H(tau,kappa)U_{E*}^*=H(-tau,kappa)` — antisymmetry at *fixed nonzero* `kappa`. The combinatorics are independently checked; the operator consequence at `kappa!=0` is not. A future contract would need: I1.3's strip Hamiltonian read and reviewed as a declared premise; proof the on-site cutoffs at `kappa!=0` are genuinely spectral projections of `h_b(kappa)`; the triple held fixed independently of `tau`; and an AM2-type fixed point/uniqueness argument with the non-Haar reference (AT4 F01: Haar is not the ground state there). It is a model change, not an extension of AW1.

## 2. Goals for sub-rounds 3-5

- **AX1/AX2 (uniform):** keep, with one caution — AX1's own target `D_ii<=4/10^7` is ~30x looser than AV1's actual zero-selected `D_ii~1.36e-8`; carried into AX2's window budget this leaves the `1e-6` radius target with only ~4% margin (see §4), unlike AV2's ~5x margin. AX1 should report its exact enumerated tier, not settle for the loose target.
- **AY1/AY2 (state/density):** AY1 should read its first-order density `rho^(1)_R` and its second-order difference constant `2K_2'tau^2` directly off AW1's admitted `c^(1)=-(tau/72)sum W_f Omega_0` and its bound `K_2^+`, rather than re-deriving a generic AV1-only form — AW1 is now the frozen source for both.
- **AZ1/AZ2 (continuum/finite-graph):** keep; AZ2's comparison of its finite-graph first-order coefficient with `1/144` needs a stated normalization dictionary (its own `-tau_FG/3`-type convention against the Z^3 `alpha*tau/24` convention, and the graph's single-square geometry against the cubic-lattice `W`) before the numbers are set side by side — "consistency, not proof" per the contract, but only if the dictionary is explicit.

## 3. AX1 specifics

Route B: four whole stars (`7|tau|` each, `28|tau|`) plus one single-factor group `psi_b` over the three selected xy faces (`||psi_b||<=|tau|`), giving `J'=29|tau|`. At the cap `J_0'=29/10^8`. Re-freeze inequalities, restated exactly: `J_0'*148/7=4292/700000000=1073/175000000`, and `1073*64=68672<175000000` so `<1/64`; `2*J_0'*352=20416/10^8=319/1562500`, and `319<1562500` so `<1`. Incidence on `R`: seven stars meet `R` (`49|tau|/8`) plus two single-factor selected groups (`2|tau|/8`), giving `||B_N||<=51|tau|/8`, `k'=51|tau|/4`; six selected faces sit inside `R`. First-order candidate count grows because route B moves the three selected faces per factor into the interaction on equal footing with the 21 omitted ones: 96 candidates per factor (four incoming stars x 24 faces) and 168 for `R` (seven factors x 24). **Transfer, not automatic:** the parity/flip identity does carry over, but only because route B ties `kappa` to `tau` uniformly (`uniform_sign_convention`) — flipping `tau` then flips the model's own `kappa` in lockstep, so AW1's "`kappa=0` only" restriction is not a real obstruction here, it is a different reason the same conclusion holds. The `+tau/144` coefficient transfers for the same reason plus `W` remaining an xz-type face outside the three xy selected faces at either site; both points should be proved, not merely cited, since `uniform_sign_convention` and `first_order_faces_uniform` are already itemized controls.

## 4. AX2 specifics

`k'=51|tau|/4=1.275e-7` at the cap. Using the frozen AV2 C^2 window (`M_0=2`, `M_1=4/pi` at `s=1`) with AX1's *target* `D'<=4e-7`: `E'~2(D')+k'M_1~8.00e-7+1.62e-7~9.62e-7`, clearing `1e-6` by only ~4%. This is the concrete case for §2's caution: AX1's exact tier, not its loose target, should be what AX2 actually uses.

## 5. WebSearch: 2025-2026 rigorous/certified uniform Kogut-Susskind SU(2) at strong coupling

Searched "rigorous certified uniform Kogut-Susskind SU(2) Hamiltonian strong coupling 2025 2026". Results were quantum-simulation papers, not rigorous strong-coupling perturbative certificates: an orbifold-lattice exponential-speedup reformulation of the Kogut-Susskind Hamiltonian (arXiv:2506.00755, 2025) and an SU(2) quantum-link-model scaling/Lüscher-term study (arXiv:2602.23213, 2026), neither addressing a rigorous mass-gap or Wilson-mean bound. **None found** matching a rigorous, certified uniform-Hamiltonian strong-coupling result; no paper opened past the abstract level.

## 6. Assistant tests after sub-round 3

- Re-run the AX2 window arithmetic with AX1's actual admitted `D_ii` (both tiers), not the `4e-7` target, and flag if the margin against `1e-6` falls below 2.
- On a small fixture, verify directly that `U_E` sends the *uniform* `H(tau)` to `H(-tau)` (kappa tied to tau throughout, no independent-kappa step), confirming §3's transfer argument rather than assuming it.
- From-scratch enumerate the uniform model's 96-per-factor / 168-for-`R` candidate counts and the route-B state-lemma tiers, mirroring S2's independent AW1 reproduction, before AX1 production is read.
- Draft the AZ2-to-`1/144` normalization-dictionary calculator (exact `Fraction`) now, so AZ2 in sub-round 5 has it ready rather than inventing the comparison late.
