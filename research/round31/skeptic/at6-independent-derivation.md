# AT6 independent continuous-window and all-node check

Written after AT6 freeze and before reading either current producer. The state and model remain the same AT5 zero-selected patterned AQ subfamily at tau=+10^-14, with fixed L=10^9 and physical clock s=alpha*t_E/hbar.

The admitted conservative comparison has D=2sqrt(49|tau|/3), mean cost 196|tau|/3, Duhamel slope k=49|tau|/4, and Poisson tail at most 4s/(pi L). To prove a uniform bound for every 0<s<=T=128, use

s log(1+(L/s)^2) <= 2s log(1+L/s) <= 2T log(1+L/T) < 32T.

The first inequality follows from 1+x²<=(1+x)². For the second, the derivative of g(s)=s log(1+L/s) is log(1+x)-x/(1+x), x=L/s. This is nonnegative for x>=0 because its derivative with respect to x is x/(1+x)² and it vanishes at zero. The last bound follows from log(1+10^9/128)<16. Independently, exp(1)>27/10 by a six-term positive series, and exact arithmetic verifies (27/10)^16>1+10^9/128. No sampled maximum is used.

Using pi>3 therefore gives the continuous-window absolute allowance

E_window = D + 196|tau|/3 + (32T/3)k + 4T/(3L) < 10^-6.

At s=0 the actual variance is q-m², not necessarily 1/4. The positive-effect trace estimate and mean-square allowance give |C(0)-1/4|<=D/2+196|tau|/3, also below the uniform budget. These are actual same-state estimates passed through the inherited AQ construction; no finite solver or uniqueness claim is introduced.

The checker independently generates every one of the 4097 reference proxies by a rigorous interval recurrence from exp(-3/32), using a degree-44 alternating bracket and directed rounding at denominator 10^45. Every row's complete actual-error allowance includes half its reference arithmetic bin. The j=0 row uses its separate centered-variance estimate. Each allowance is below 10^-6. The actual trapezoid is summed row by row with h/2 endpoint weights and h interior weights. No closed geometric sum replaces those rows.

With P the exact rational proxy trapezoid, Q=47/512000 and J=128*10^-6, the primary interval is [P-Q-J,P+J+D_mass], where D_mass=(504/125)exp(-8) is outward enclosed independently. Same-measure positive support x>=1/16 implies C(s)<=C(T)exp(-(s-T)/16) for s>=T, so the second interval replaces the tail by 16(d_N+10^-6). This endpoint includes its actual-state error; the bare reference endpoint is insufficient. Both widths meet their respective 1/500 and 1/2500 targets, and both contain 1/12. Thus the interaction-induced inverse correction remains unresolved.

The damaging slow spectral control eta=(delta_{1/16}+delta_{95/16})/8 has mass1/4, first moment3/4 and second moment below the inherited ceiling. Its omitted slow tail at T is at least 2exp(-8), larger than Q+J, so deleting the tail can exclude its exact infinite integral even after paying quadrature and sample allowances. It is a valid abstract control under the inherited moment constraints, not asserted to be an AQ realization. Wrong quadrature sign is separately defeated by the exact free inverse. Fully correlated node errors require J=T*epsilon; no root-N assumption is available.

Normal and optimized executions pass 4120 exact checks, including 4097 individual node-error checks, with identical JSON bytes. The checker does not import either current producer. It supplies a separate conservative route and all-node arithmetic; the forthcoming review will audit producer APIs, provenance rejection and tighter endpoint choices only after both packages freeze. No fourth investigation is authorized.
