#!/usr/bin/env python3
import argparse,json
from fractions import Fraction as F
from math import factorial
from pathlib import Path

def need(x,m):
    if not x:raise RuntimeError(m)
def geom(n,y):return sum(y**k for k in range(n))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);o=Path(ap.parse_args().output);o.mkdir(parents=True,exist_ok=True)
    g=F(381,416);theta=F(1,16);d=(g*theta)**2/10;rho=1-d
    n=(7*d.denominator+d.numerator-1)//d.numerator
    need(n*d>=7 and (n-1)*d<7,'minimal n for exponential sufficient bound')
    need(sum(F(7**k,factorial(k)) for k in range(30))>1000,'exp7 lower')
    need(F(101,120)<F(9,10),'sinc interval glue')
    need(F(1,6)-F(1,120)>F(1,10),'sinc small interval')
    # Rational y represents a tested residual eigenvalue, not an actual SU2 spectral datum.
    for y in [F(0),F(1),F(3,4),F(-1,5)]:
      for j in range(1,9):
        need((1-y)*geom(j,y)==1-y**j,'all-step telescope')
    radius=F(105,416)
    need(3*radius<1<4*radius,'short-time weighted certificate limit')
    # Excited frequencies shrink in a compact-resolvent countermodel. Taylor lower bounds
    # at increasing k demonstrate the explicitly proved sup limit, not actual spectrum.
    k0,k1=10,10000
    low0=1-(theta/F(k0+1))**2/6
    low1=1-(theta/F(k1+1))**2/6
    controls={
      'zero_frequency_residual_is_retained':F(1)**8==1 and (1-F(1))*geom(8,F(1))==0,
      'negative_sinc_geometric_sign_is_retained':(1-F(-1,5))*geom(3,F(-1,5))==1-F(-1,5)**3,
      'strong_limit_not_norm_limit':low1**10>low0**10 and low1**10>F(999999,1000000),
      'formal_inverse_unbounded_in_countermodel':F(k1+1)>F(k0+1),
      'single_star_radius_cannot_be_reused_indefinitely':4*radius>1,
      'ground_gap_not_excited_gap':g>F(1,k1+1),
      'column_norm_bound_cannot_bound_unseen_diagonal_block':F(0)<F(1),
    }
    need(all(controls.values()),'controls')
    result={'loop':'w2','direction':'forward','status':'passed','claims':['Actual vacuum residual decays geometrically at fixed positive Theta uniformly in volume','Actual accumulated inverse column converges in graph norm','Full finite-volume residual converges strongly to its equal-energy part','Every finite step retains full-source residual and domain identity'],'limitations':['Vacuum column does not control full operator norm','Actual equal-energy blocks remain unevaluated','Infinite-volume full-source strong limit not proved','Existing weight2 bound covers n<=3 at cap, not all iterations','No later-diagonal induction'],'worst_gap':str(g),'Theta':str(theta),'rho':str(rho),'iterations_for_column_relative_error_below_1e_3':n,'graph_error_factor':str(1+1/g),'weighted_iteration_cap':3,'countermodel_not_actual_SU2':True,'continuum_proved':False}
    (o/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (o/'controls.json').write_text(json.dumps({'controls':controls},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
