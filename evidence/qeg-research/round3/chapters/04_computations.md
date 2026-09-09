## Executed causal calculation and its numerical limits

### Model, pump and measurement

The theory chapter calls the mode-current sum $S$ and the finite-window derivative coefficient $D$. The code calls these `J0` and `S`, respectively. This notation map matters: the code's `Sx2` is the theory's $Dx^2$. Define the effective numerator $Q=S+Dx^2$. It is not by itself the full physical renormalized current. In the theory's dimensionless matter-current units,

$$\mathcal J=\frac{j_{\rm matter}}{em^3}
=Q-Cx'+\frac{\chi_B}{e^2}x'
=\frac{F-x'}{e^2},\qquad x'=\frac{F-e^2Q}{Z}.$$

Moving polarization onto the Maxwell left side changes the named source, not the physical solution. The delivered refinement metadata records both $Q$ and $\mathcal J$. A previous draft called $Q$ the physical current; the theory reviewer and lead researcher independently caught this labeling error. The differential system and solver source did not change.

The executed pump is normalized by its integral:

$$F(s)=\frac{x_{\rm target}}{T_p I}
\exp\!\left[-\frac{1}{u(1-u)}\right],\quad
u=s/T_p\in(0,1),$$
$$I=\int_0^1\exp[-1/(u(1-u))]du,$$

and $F=0$ outside that interval. Thus $x_{\rm target}$ is the electric field an empty classical Maxwell system would acquire, not the actual peak in the responding vacuum. The first and last derivatives of every finite order vanish at the pump endpoints. Initially $x=a=0$ and all modes occupy the magnetic negative-energy state.

Production parameters are $b=10$, $T_p=4$, $x_{\rm target}=1$, $s_f=50$, Landau levels $0$ through $8$, canonical window $[-40,40]$ and 4096 Gauss–Legendre nodes per level. There are 36,864 Bloch modes. DOP853 uses relative tolerance $2\times10^{-10}$, absolute tolerance $2\times10^{-12}$ and maximum step $0.05$. The recorded history has 251 equally spaced times; a sampled maximum is not a continuous-time extremum.

### Results that survive the advisor's convergence challenge

| Quantity | Measured value | Interpretation |
|---|---:|---|
| Final field $x(50)$ | -0.037571642494 | Report approximately -0.03757 for this model |
| Final potential $a(50)$ | -26.5864064568 | Residual gauge convention $a(0)=0$ |
| Sampled maximum absolute field | 0.9893066812 | Sampling at intervals 0.2 misses the exact peak |
| Minimum effective coefficient $Z$ | 0.9960199826 | No ill-conditioned denominator on this trajectory |
| Maximum absolute energy/work residual | $5.89\times10^{-12}$ | Finite-grid conservation diagnostic |
| Physical energy/work scale | 0.4978069367 | Actual denominator used for relative error |
| Maximum relative energy/work residual | $1.18\times10^{-11}$ | Does not bound quadrature or model error |
| Maximum raw Bloch norm defect | $2.94\times10^{-8}$ | Reported without renormalizing trajectories |
| Final raw occupation range | about $-1.6\times10^{-15}$ to 0.04934 | Tiny negative floor is numerical; output is not clipped |

The source vanishes for $s\geq4$. Field reversal at late time is therefore an actual consequence of the computed matter current in this model, rather than an imposed reversal of the external electric profile. The background magnetic energy is constant and omitted from the energy *difference*; the pump supplies the changing system's energy. This observation does not imply energy extraction from an unprepared vacuum.

| Numerical axis | Comparison | Observed change |
|---|---|---:|
| Longitudinal quadrature, coarse | 1024 to 2048 nodes, fixed $K=40$, $n_{\max}=8$ | Endpoint $1.115\times10^{-5}$: initially unresolved |
| Longitudinal quadrature, refined | 2048 to 4096 nodes, same bounds | Maximum sampled field-history difference $3.257\times10^{-9}$ |
| Full matter current | Same fixed-window refinement | Maximum $|\Delta\mathcal J|=1.1315\times10^{-6}$ |
| Effective numerator source | Same fixed-window refinement | Maximum $|\Delta Q|=1.1270\times10^{-6}$ |
| Momentum window | $K=40$, 2048 nodes to $K=60$, 3072 nodes | Endpoint difference $4.107\times10^{-11}$ |
| Landau truncation | Levels through 8 to levels through 12, $K=40$, 2048 nodes | Endpoint difference $5.061\times10^{-8}$ |

The window comparison approximately preserves central node spacing; it cannot replace refinement at fixed window. That was the advisor's reason to require the 4096-node run. The largest recorded endpoint change among the final component tests is the Landau shift. No rigorous tail bound or simultaneous all-observable continuum extrapolation has been established. Full-current convergence is weaker than field convergence, because the field integrates a rapidly varying source. The raw mode current alone is regulator-dependent and cannot substitute for $\mathcal J$.

The initial 256-node result, $x(50)\simeq-0.03743286$, is superseded. Historical short-time scans and deliberately wrong controls remain in the package as audit evidence; their filenames do not designate accepted production results. `production_baseline.json` and `production_baseline.csv` identify the final 4096-node data. The earlier file named `production_baseline_converged` is an intermediate window check, not a stronger certificate.

### A physical matching test that conservation cannot fake

For $b=100$, $x_{\rm target}=0.01$, pump duration 20 and final time 40, the static linear prediction is $x_{\rm target}/(1+\chi_B)=0.00931301998$. The late-time mean averages the final 50 of 401 stored points, spanning $s=35.1$ through $40$. These control runs use maximum ODE step 0.08. The mean does not assert an exact stationary field.

| Prescription | Measured late mean | What it tests |
|---|---:|---|
| Matched physical susceptibility | 0.00931301064 | Finite response retained once |
| Subtraction with finite matching omitted | 0.00999998497 | Incorrectly erases nearly all static magnetic response |
| Sign-reversed finite matching | 0.01079637896 | Deliberately wrong finite response |
| Unrenormalized finite-cutoff model | 0.00926614690 | Different cutoff-dependent prescription |

The matched late mean differs from the static prediction by about $9.33\times10^{-9}$ in this finite-duration test. Its true relative work residual is $3.63\times10^{-9}$ at energy scale $4.66\times10^{-5}$. The omitted-matching model also conserves its own consistently defined energy very closely, while yielding the wrong physical static response. This is the central counterexample to treating conservation as sufficient validation.

### Independent checks and a retained failure

The separate verifier implements complex spinors, not production Bloch vectors, with no production import. On the shared small grid its sampled field and potential differ from production by at most $3.63\times10^{-12}$ and $4.62\times10^{-12}$. Exact spectra, boundary shifts, gauge-window changes and deliberately broken vacuum subtraction supply additional tests described next.

The advisor's independent high-precision Sauter formula identifies the prior expansion-only benchmark exactly. Its strictest double-precision target, absolute error below $10^{-18}$, **failed** at about $1.82\times10^{-18}$. That failed gate remains in `advisor_checks.json`. It concerns a benchmark precision target, not the larger-scale field reversal, but it prevents a blanket statement that every requested accuracy test passed.
